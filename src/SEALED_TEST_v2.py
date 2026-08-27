"""
================================================================================================
LTLC — OFFICIAL TEST-SET CONFIRMATION RUN  (v2, corrected 2026-08-26)
================================================================================================
Local-run adaptation of the handoff script. The ONLY change from the delivered
v2 text is PROJECT_ROOT, which now points at the local project copy instead of a
Colab Drive mount. mount_drive() no-ops outside Colab, as designed.

The seal, stated precisely:
  "No official-test result influenced any Experiment-B decision. Method
   selection, hyperparameter selection, and checkpoint selection were all
   performed on the spatially-disjoint validation split alone."

Step 1: leave PREFLIGHT_ONLY = True and run. Validates every path, loads the
        model, loads the cube, confirms split members exist -- WITHOUT reading
        a single test index or label VALUE.
Step 2: only when preflight prints ALL CHECKS PASSED, set PREFLIGHT_ONLY = False
        and run once.
================================================================================================
"""

import ast
import hashlib
import json
import platform
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset

# ================================================================================================
# SET THIS TO False ONLY AFTER PREFLIGHT PASSES
# ================================================================================================
PREFLIGHT_ONLY = False


# ================================================================================================
# 0. MOUNT DRIVE  (no-op outside Colab)
# ================================================================================================
def mount_drive():
    try:
        from google.colab import drive
    except ImportError:
        print("Not running in Colab -- skipping drive.mount(). "
              "Make sure PROJECT_ROOT below points at your real project.")
        return
    try:
        drive.mount("/content/drive", force_remount=True)
    except ValueError as e:
        print("Mount failed even with force_remount=True:", e)
        print("Fix: Runtime -> Restart session (NOT Factory reset), then re-run this cell.")
        raise


PROJECT_ROOT = Path(__file__).resolve().parent / "LTLC"

AUDIT_ROOT = PROJECT_ROOT / "audit"
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"
RUNS_ROOT = PROJECT_ROOT / "runs" / "experiment_b_spatial_validation_v1"
PCA_DIR = PROJECT_ROOT / "data_cache" / "pca_normalized_cubes"
SPLIT_DIR = PROJECT_ROOT / "split_indices"

SEALED_TEST_DIR = AUDIT_ROOT / "sealed_test_confirmation_run"   # created later, not at import
RESULT_JSON = SEALED_TEST_DIR / "official_test_confirmation_results.json"
RUN_LOG_MD = SEALED_TEST_DIR / "OFFICIAL_TEST_RUN_LOG.md"

NOTEBOOK03_PATH = (
    NOTEBOOKS_DIR / "03_HybridSN_Baseline_Training_and_Benchmark_Reproduction.ipynb"
)

# ================================================================================================
# 1. THE TWO WINNING CONFIGURATIONS, copied verbatim from the frozen
#    LTLC_Notebook06A_ExperimentB_VALIDATION_SUMMARY_TABLE_v1.md (rank 1 per scene).
#    Nothing here was chosen by looking at test performance.
# ================================================================================================
SELECTED_CONFIGS = {
    "Pingan": {
        "method": "balanced_softmax",
        "config_dir": None,             # balanced softmax had no tuning grid
        "config_token": None,
        "num_classes": 10,
        "height": 1230,
        "width": 1000,
        "spectral_depth": 15,
        "patch_size": 13,
        "radius": 6,
        "expected_param_count": 519546,   # verified for Pingan / 10 classes
    },
    "Qingyun": {
        "method": "la_loss",
        "config_dir": "tau0p5",
        "config_token": "tau0p5",
        "num_classes": 6,
        "height": 880,
        "width": 1360,
        "spectral_depth": 15,
        # CORRECTED 2026-08-26: the handoff notes said patch_size=13 / radius=6 for BOTH
        # scenes. That is wrong for Qingyun. Every Qingyun la_loss tau0p5 checkpoint
        # self-reports architecture={"patch_size": 11, ..., "parameter_count": 256886},
        # and loading it into a patch_size=13 model fails with
        #   size mismatch for fc1.weight: checkpoint [256, 576] vs model [256, 1600].
        # radius MUST stay (patch_size - 1) // 2 = 5, otherwise the zero-padding offset
        # and the slice window disagree and every patch is extracted off-centre -- which
        # would NOT raise, it would just silently produce wrong predictions.
        # Verified by reproducing the frozen validation AA; see check_architecture_matches().
        "patch_size": 11,
        "radius": 5,
        "expected_param_count": 256886,
    },
}
SEEDS = [42, 123, 3407]


def checkpoint_path_for(dataset_name: str, cfg: dict, seed: int) -> Path:
    """Rebuild the exact Experiment-B checkpoint path from the run-ledger layout."""
    ds = dataset_name.lower()
    parts = [cfg["method"], ds]
    if cfg["config_dir"]:
        parts.append(cfg["config_dir"])
    parts.append(f"seed{seed}")
    run_dir = RUNS_ROOT.joinpath(*parts)

    name_parts = [cfg["method"], ds]
    if cfg["config_token"]:
        name_parts.append(cfg["config_token"])
    name_parts.append(f"seed{seed}")
    filename = "__".join(name_parts) + "__best_valAA.pt"
    return run_dir / filename


# ================================================================================================
# 2. RECOVER THE FROZEN HybridSN CLASS FROM NOTEBOOK 03 (AST-checked, then exec'd).
# ================================================================================================
def recover_hybridsn_class():
    if not NOTEBOOK03_PATH.exists():
        listing = ""
        if NOTEBOOKS_DIR.is_dir():
            listing = "\n".join(f"    {p.name}" for p in sorted(NOTEBOOKS_DIR.iterdir()))
            listing = f"\nnotebooks/ actually contains:\n{listing}"
        else:
            listing = (f"\n{NOTEBOOKS_DIR} does not exist either -- "
                       "Drive is probably not mounted, or PROJECT_ROOT is wrong.")
        raise FileNotFoundError(
            f"STOP: frozen HybridSN source notebook not found:\n{NOTEBOOK03_PATH}{listing}"
        )

    nb = json.loads(NOTEBOOK03_PATH.read_text(encoding="utf-8"))
    hybridsn_source = None
    for cell in nb["cells"]:
        if cell.get("cell_type") != "code":
            continue
        src = "".join(cell.get("source", []))
        if "class HybridSN" in src:
            hybridsn_source = src
            break
    if hybridsn_source is None:
        raise RuntimeError("STOP: no cell defining 'class HybridSN' found in Notebook 03.")

    ast.parse(hybridsn_source)   # fail loudly on a truncated cell rather than exec partial code
    namespace = {"torch": torch, "nn": nn, "np": np, "F": torch.nn.functional}
    exec(compile(hybridsn_source, str(NOTEBOOK03_PATH), "exec"), namespace)
    if "HybridSN" not in namespace:
        raise RuntimeError("STOP: cell executed but did not define 'HybridSN'.")

    digest = hashlib.sha256(hybridsn_source.encode()).hexdigest()[:16]
    print(f"  Recovered HybridSN from {NOTEBOOK03_PATH.name} (source sha256 {digest}...)")
    return namespace["HybridSN"]


def build_model(HybridSN, cfg, device):
    model = HybridSN(
        spectral_depth=cfg["spectral_depth"],
        patch_size=cfg["patch_size"],
        num_classes=cfg["num_classes"],
        dropout=0.4,
    )
    n_params = int(sum(p.numel() for p in model.parameters()))
    if cfg["expected_param_count"] is not None and n_params != cfg["expected_param_count"]:
        raise RuntimeError(
            f"STOP: parameter-count mismatch: got {n_params}, "
            f"expected {cfg['expected_param_count']}."
        )
    return model.to(device), n_params


# ================================================================================================
# 3. PATCH DATASET -- copied from ExperimentBHSIPatchDataset (Notebook 06A cell 13A),
#    reformatted but functionally identical.
# ================================================================================================
class HSIPatchDataset(Dataset):
    def __init__(self, padded_cube, flat_indices, model_labels, image_width, patch_size):
        self.padded_cube = padded_cube
        self.flat_indices = np.asarray(flat_indices, dtype=np.int64)
        self.model_labels = np.asarray(model_labels, dtype=np.int64)
        self.image_width = int(image_width)
        self.patch_size = int(patch_size)

    def __len__(self):
        return int(self.flat_indices.size)

    def __getitem__(self, position):
        flat_index = int(self.flat_indices[int(position)])
        row = flat_index // self.image_width
        col = flat_index % self.image_width
        patch_hwc = np.asarray(
            self.padded_cube[row:row + self.patch_size, col:col + self.patch_size, :],
            dtype=np.float32,
        )
        patch_chw = np.ascontiguousarray(np.transpose(patch_hwc, (2, 0, 1)))
        sample = torch.from_numpy(patch_chw).unsqueeze(0)
        label = torch.tensor(int(self.model_labels[int(position)]), dtype=torch.long)
        return sample, label


def load_padded_cube(dataset_name: str, cfg: dict):
    pca_path = PCA_DIR / f"{dataset_name.lower()}_pca15_rowminmax_float32.npy"
    if not pca_path.exists():
        raise FileNotFoundError(f"STOP: PCA cube not found:\n{pca_path}")
    cube = np.load(pca_path, mmap_mode="r", allow_pickle=False)
    if cube.shape[0] != cfg["height"] or cube.shape[1] != cfg["width"]:
        raise RuntimeError(
            f"STOP: {dataset_name} cube geometry {cube.shape[:2]} != "
            f"expected ({cfg['height']}, {cfg['width']})."
        )
    r = cfg["radius"]
    padded = np.pad(cube, ((r, r), (r, r), (0, 0)),
                    mode="constant", constant_values=0).astype(np.float32, copy=False)
    del cube
    return padded, pca_path


def official_test_split_path(dataset_name: str) -> Path:
    return SPLIT_DIR / f"{dataset_name.lower()}_fixed_split_seed2026.npz"


def inspect_test_split(dataset_name: str):
    """PREFLIGHT-SAFE: confirms the split file and its test members exist.
    Reads member NAMES and SHAPES only -- never label or index VALUES."""
    path = official_test_split_path(dataset_name)
    if not path.exists():
        raise FileNotFoundError(f"STOP: official split file not found:\n{path}")
    with np.load(path, allow_pickle=False) as z:
        members = list(z.files)
        missing = [m for m in ("test_indices", "test_labels_model") if m not in members]
        if missing:
            raise RuntimeError(
                f"STOP: {path.name} is missing {missing}. Members present: {members}"
            )
        shapes = {m: z[m].shape for m in ("test_indices", "test_labels_model")}
    return path, members, shapes


def load_official_test_dataset(dataset_name: str, cfg: dict, padded_cube):
    """THE REAL READ. This is the step that opens the test set."""
    path = official_test_split_path(dataset_name)
    with np.load(path, allow_pickle=False) as z:
        test_indices = np.asarray(z["test_indices"], dtype=np.int64).copy()
        test_labels = np.asarray(z["test_labels_model"], dtype=np.int64).copy()

    if test_indices.size != test_labels.size:
        raise RuntimeError("STOP: test_indices / test_labels_model length mismatch.")
    lo, hi = int(test_labels.min()), int(test_labels.max())
    if lo < 0 or hi >= cfg["num_classes"]:
        raise RuntimeError(
            f"STOP: test_labels_model range [{lo},{hi}] is outside "
            f"[0,{cfg['num_classes'] - 1}] -- the class-id mapping does not match "
            "this scene's Experiment-B mapping. Do NOT proceed; reconcile first."
        )
    max_flat = cfg["height"] * cfg["width"]
    if int(test_indices.max()) >= max_flat:
        raise RuntimeError("STOP: a test flat index exceeds the cube's pixel count.")

    ds = HSIPatchDataset(padded_cube, test_indices, test_labels,
                         cfg["width"], cfg["patch_size"])
    return ds, test_indices.size


# ================================================================================================
# 4. METRICS + EVALUATION
# ================================================================================================
def sha256_of_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def check_architecture_matches(ckpt: dict, cfg: dict, ckpt_path: Path):
    """Guard against the class of bug that broke the Qingyun load.

    Every Experiment-B checkpoint records the exact constructor arguments it was
    built with under `architecture`. Trusting the notes instead of that record is
    what produced a patch_size mismatch. A wrong patch_size raises loudly; a wrong
    RADIUS does not -- it silently decentres every patch. So verify both against
    the checkpoint's own record before any inference happens.
    """
    arch = ckpt.get("architecture")
    if not isinstance(arch, dict):
        print(f"    NOTE: {ckpt_path.name} records no 'architecture' block; "
              "cannot cross-check constructor arguments.")
        return
    for key in ("spectral_depth", "patch_size", "num_classes"):
        if key in arch and int(arch[key]) != int(cfg[key]):
            raise RuntimeError(
                f"STOP: {ckpt_path.name} was trained with {key}={arch[key]}, but this run "
                f"is configured with {key}={cfg[key]}. Reconcile before proceeding."
            )
    if "patch_size" in arch:
        expected_radius = (int(arch["patch_size"]) - 1) // 2
        if int(cfg["radius"]) != expected_radius:
            raise RuntimeError(
                f"STOP: radius={cfg['radius']} is inconsistent with patch_size="
                f"{arch['patch_size']} (needs {expected_radius}). Patches would be "
                "extracted off-centre WITHOUT raising an error."
            )
    if "parameter_count" in arch and cfg["expected_param_count"] is not None:
        if int(arch["parameter_count"]) != int(cfg["expected_param_count"]):
            raise RuntimeError(
                f"STOP: {ckpt_path.name} records parameter_count="
                f"{arch['parameter_count']}, config expects {cfg['expected_param_count']}."
            )


def load_checkpoint_into(model, ckpt_path: Path, dataset_name: str, seed: int, device,
                         cfg: dict = None):
    ckpt = torch.load(ckpt_path, map_location="cpu", weights_only=False)
    if "model_state_dict" not in ckpt:
        raise RuntimeError(
            f"STOP: {ckpt_path.name} has no 'model_state_dict' "
            f"(keys: {sorted(ckpt.keys())[:12]})."
        )
    # identity guard, mirroring Notebook 06A cell 13A check
    if ckpt.get("dataset") not in (None, dataset_name):
        raise RuntimeError(f"STOP: checkpoint dataset {ckpt.get('dataset')!r} != {dataset_name!r}")
    if ckpt.get("seed") is not None and int(ckpt["seed"]) != seed:
        raise RuntimeError(f"STOP: checkpoint seed {ckpt.get('seed')} != {seed}")
    if cfg is not None:
        check_architecture_matches(ckpt, cfg, ckpt_path)
    model.load_state_dict(ckpt["model_state_dict"])
    model.eval()
    return ckpt


@torch.no_grad()
def evaluate(model, dataset, num_classes, device, batch_size=256):
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=False,
                        num_workers=0, pin_memory=True, drop_last=False)
    preds, trues = [], []
    for batch_x, batch_y in loader:
        batch_x = batch_x.to(device, non_blocking=True)
        logits = model(batch_x)
        preds.append(logits.argmax(dim=1).cpu().numpy())
        trues.append(batch_y.numpy())
    y_pred = np.concatenate(preds)
    y_true = np.concatenate(trues)

    oa = float((y_pred == y_true).mean())
    per_class, f1s = [], []
    for c in range(num_classes):
        mask = y_true == c
        if mask.sum():
            per_class.append(float((y_pred[mask] == c).mean()))
        tp = int(((y_pred == c) & (y_true == c)).sum())
        fp = int(((y_pred == c) & (y_true != c)).sum())
        fn = int(((y_pred != c) & (y_true == c)).sum())
        prec = tp / (tp + fp) if (tp + fp) else 0.0
        rec = tp / (tp + fn) if (tp + fn) else 0.0
        f1s.append(2 * prec * rec / (prec + rec) if (prec + rec) else 0.0)
    aa = float(np.mean(per_class))
    macro_f1 = float(np.mean(f1s))
    n = y_true.size
    pe = sum((np.sum(y_true == c) / n) * (np.sum(y_pred == c) / n) for c in range(num_classes))
    kappa = float((oa - pe) / (1 - pe)) if pe != 1 else float("nan")
    return {"OA": oa, "AA": aa, "MacroF1": macro_f1, "Kappa": kappa,
            "per_class_accuracy": per_class, "n_test_pixels": int(n)}


# ================================================================================================
# 5. PREFLIGHT -- validates everything, opens nothing
# ================================================================================================
def preflight(device):
    print("\n" + "=" * 100)
    print("PREFLIGHT - validating paths, model, cube and split members.")
    print("NO test index or label VALUES are read in this mode.")
    print("=" * 100)

    problems = []
    print(f"\n[1] PROJECT_ROOT exists: {PROJECT_ROOT.is_dir()}  ({PROJECT_ROOT})")
    if not PROJECT_ROOT.is_dir():
        problems.append("PROJECT_ROOT missing -- check the path at the top of this script.")
        print("\nPREFLIGHT FAILED:\n  - " + "\n  - ".join(problems))
        return False

    print("\n[2] Recovering HybridSN from Notebook 03")
    try:
        HybridSN = recover_hybridsn_class()
    except Exception as exc:
        print(f"  FAILED: {exc}")
        return False

    for dataset_name, cfg in SELECTED_CONFIGS.items():
        print(f"\n[3] {dataset_name} - {cfg['method']}"
              + (f" ({cfg['config_dir']})" if cfg["config_dir"] else ""))
        for seed in SEEDS:
            p = checkpoint_path_for(dataset_name, cfg, seed)
            if p.exists():
                print(f"    seed {seed}: checkpoint OK  ({p.name})")
            else:
                problems.append(f"{dataset_name} seed {seed}: missing {p}")
                print(f"    seed {seed}: MISSING -> {p}")
                if p.parent.is_dir():
                    print("      that directory contains:")
                    for q in sorted(p.parent.iterdir()):
                        print(f"        {q.name}")
                elif p.parent.parent.is_dir():
                    print(f"      {p.parent} does not exist; {p.parent.parent} contains:")
                    for q in sorted(p.parent.parent.iterdir()):
                        print(f"        {q.name}")

        try:
            model, n_params = build_model(HybridSN, cfg, device)
            print(f"    model builds OK ({n_params:,} parameters)")
            del model
        except Exception as exc:
            problems.append(f"{dataset_name}: model build failed: {exc}")
            print(f"    model build FAILED: {exc}")

        try:
            padded, pca_path = load_padded_cube(dataset_name, cfg)
            print(f"    PCA cube OK  {pca_path.name}  padded shape {padded.shape}")
            del padded
        except Exception as exc:
            problems.append(f"{dataset_name}: PCA cube failed: {exc}")
            print(f"    PCA cube FAILED: {exc}")

        try:
            path, members, shapes = inspect_test_split(dataset_name)
            print(f"    split OK  {path.name}")
            print(f"      test_indices shape      : {shapes['test_indices']}")
            print(f"      test_labels_model shape : {shapes['test_labels_model']}")
        except Exception as exc:
            problems.append(f"{dataset_name}: split failed: {exc}")
            print(f"    split FAILED: {exc}")

    print("\n" + "=" * 100)
    if problems:
        print("PREFLIGHT FAILED - fix these before setting PREFLIGHT_ONLY = False:")
        for p in problems:
            print("  - " + p)
        print("=" * 100)
        return False
    print("ALL CHECKS PASSED.")
    print("Set PREFLIGHT_ONLY = False and run once to open the official test set.")
    print("=" * 100)
    return True


# ================================================================================================
# 6. MAIN
# ================================================================================================
def main():
    mount_drive()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    env_info = {
        "python": platform.python_version(),
        "torch": torch.__version__,
        "cuda_available": torch.cuda.is_available(),
        "device_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else "cpu",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }
    print("Environment:", json.dumps(env_info, indent=2))

    if PREFLIGHT_ONLY:
        preflight(device)
        return

    # ---- real run from here ----
    if RESULT_JSON.exists():
        raise RuntimeError(
            f"STOP: {RESULT_JSON} already exists - the official test has already been\n"
            "scored for Experiment B. Re-running would give you a second look and let\n"
            "you pick the better number, which is exactly what the protocol forbids.\n"
            "If the previous run was mechanically broken and produced no valid numbers,\n"
            f"move that file aside, record why in {RUN_LOG_MD.name}, and only then re-run."
        )

    print("=" * 100)
    print("YOU ARE ABOUT TO SCORE EXPERIMENT B ON THE OFFICIAL TEST SET.")
    print("No Experiment-B decision has ever been informed by this data.")
    print("Report whatever comes out. Do not iterate.")
    print("=" * 100)
    phrase = input("Type exactly:  I ONLY RUN THIS ONCE AND WILL REPORT WHATEVER I GET\n> ")
    if phrase.strip() != "I ONLY RUN THIS ONCE AND WILL REPORT WHATEVER I GET":
        raise RuntimeError("Confirmation phrase did not match. Aborting - nothing was opened.")

    HybridSN = recover_hybridsn_class()
    results = {}

    for dataset_name, cfg in SELECTED_CONFIGS.items():
        print(f"\n=== {dataset_name}: {cfg['method']}"
              + (f" ({cfg['config_dir']})" if cfg["config_dir"] else "") + " ===")
        padded_cube, pca_path = load_padded_cube(dataset_name, cfg)
        test_ds, n_test = load_official_test_dataset(dataset_name, cfg, padded_cube)
        print(f"  official test pixels: {n_test:,}")

        per_seed = {}
        for seed in SEEDS:
            ckpt_path = checkpoint_path_for(dataset_name, cfg, seed)
            if not ckpt_path.exists():
                raise FileNotFoundError(f"STOP: checkpoint not found:\n{ckpt_path}")
            model, _ = build_model(HybridSN, cfg, device)
            load_checkpoint_into(model, ckpt_path, dataset_name, seed, device, cfg)
            m = evaluate(model, test_ds, cfg["num_classes"], device)
            m["checkpoint_sha256"] = sha256_of_file(ckpt_path)
            m["checkpoint"] = ckpt_path.name
            print(f"  seed {seed}: OA={m['OA']:.4f}  AA={m['AA']:.4f}  "
                  f"MacroF1={m['MacroF1']:.4f}  Kappa={m['Kappa']:.4f}")
            per_seed[str(seed)] = m
            del model
            if device.type == "cuda":
                torch.cuda.empty_cache()

        aa = [m["AA"] for m in per_seed.values()]
        oa = [m["OA"] for m in per_seed.values()]
        results[dataset_name] = {
            "method": cfg["method"],
            "config": cfg["config_dir"] or "training_counts",
            "pca_cube": pca_path.name,
            "split_file": official_test_split_path(dataset_name).name,
            "per_seed": per_seed,
            "AA_mean": float(np.mean(aa)), "AA_sd": float(np.std(aa, ddof=1)),
            "OA_mean": float(np.mean(oa)), "OA_sd": float(np.std(oa, ddof=1)),
        }
        del padded_cube, test_ds

    SEALED_TEST_DIR.mkdir(parents=True, exist_ok=True)
    RESULT_JSON.write_text(json.dumps({"environment": env_info, "results": results}, indent=2))
    RUN_LOG_MD.write_text(
        "# Official-test confirmation run (Experiment B)\n\n"
        f"Run once at {env_info['timestamp_utc']} on {env_info['device_name']}.\n\n"
        f"Result file: `{RESULT_JSON.name}` (sha256 {sha256_of_file(RESULT_JSON)}).\n\n"
        "Scope of the claim this supports: no official-test result influenced any\n"
        "Experiment-B method, hyperparameter, or checkpoint selection. It does NOT\n"
        "claim the official test was never read at all -- Notebook 03's CE benchmark\n"
        "reproduction evaluated on it earlier, by design.\n\n"
        "This file existing means Experiment B has been scored on official test. Do not\n"
        "delete it to try again. If a mechanical failure forces a re-run, document what\n"
        "failed below this line first.\n"
    )
    print(f"\nWrote {RESULT_JSON}")
    print(f"Wrote {RUN_LOG_MD}")
    print("\nDone. Report these numbers once, as-is.")


if __name__ == "__main__":
    main()
