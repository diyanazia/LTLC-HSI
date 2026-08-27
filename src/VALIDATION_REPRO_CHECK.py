"""
Pre-seal sanity check (touches NO official-test data).

Runs the six selected Experiment-B checkpoints back through the Experiment-B
SPATIAL VALIDATION split and compares the resulting AA against the frozen
run-ledger values. This is the check the handoff calls for in section 4.1:

  "If, after extracting a checkpoint and running it back through the
   Experiment-B validation split, you get numbers wildly different from this
   table, you have the wrong checkpoint -- stop and re-locate before touching
   the test set."

It reads only:
  split_indices/experiment_b_spatial_validation_v1/<ds>_experiment_b_spatial_split_v1.npz
    -> members val_indices / val_labels_model
which is the split every Experiment-B decision was already made on. The
official test split file is never opened here.

Purpose: prove the whole pipeline (HybridSN recovery, state-dict load, patch
extraction, label mapping, metric code) reproduces known numbers BEFORE the
one-shot test run, so the sealed run cannot be wasted on a mechanical bug.
"""

import time

import numpy as np
import torch

import SEALED_TEST_v2 as S

# Frozen validation AA per seed, from run_ledger.csv (handoff section 4.1)
LEDGER_VAL_AA = {
    ("Pingan", 42): 0.76552,
    ("Pingan", 123): 0.77674,
    ("Pingan", 3407): 0.76626,
    ("Qingyun", 42): 0.76417,
    ("Qingyun", 123): 0.76357,
    ("Qingyun", 3407): 0.75071,
}

TOLERANCE = 0.005   # anything beyond this is a red flag worth stopping for


def validation_split_path(dataset_name: str):
    return (S.SPLIT_DIR / "experiment_b_spatial_validation_v1"
            / f"{dataset_name.lower()}_experiment_b_spatial_split_v1.npz")


def main():
    torch.set_num_threads(max(1, (torch.get_num_threads() or 4)))
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"device: {device}  threads: {torch.get_num_threads()}")

    HybridSN = S.recover_hybridsn_class()
    all_ok = True

    for dataset_name, cfg in S.SELECTED_CONFIGS.items():
        print(f"\n=== {dataset_name}: {cfg['method']}"
              + (f" ({cfg['config_dir']})" if cfg["config_dir"] else "") + " ===")
        padded_cube, _ = S.load_padded_cube(dataset_name, cfg)

        vpath = validation_split_path(dataset_name)
        with np.load(vpath, allow_pickle=False) as z:
            val_idx = np.asarray(z["val_indices"], dtype=np.int64).copy()
            val_lab = np.asarray(z["val_labels_model"], dtype=np.int64).copy()
        print(f"  validation pixels: {val_idx.size:,}   ({vpath.name})")

        ds = S.HSIPatchDataset(padded_cube, val_idx, val_lab,
                               cfg["width"], cfg["patch_size"])

        for seed in S.SEEDS:
            ckpt_path = S.checkpoint_path_for(dataset_name, cfg, seed)
            model, _ = S.build_model(HybridSN, cfg, device)
            ckpt = S.load_checkpoint_into(model, ckpt_path, dataset_name, seed, device, cfg)
            t0 = time.time()
            m = S.evaluate(model, ds, cfg["num_classes"], device)
            dt = time.time() - t0

            expected = LEDGER_VAL_AA[(dataset_name, seed)]
            delta = m["AA"] - expected
            flag = "OK " if abs(delta) <= TOLERANCE else "MISMATCH"
            if abs(delta) > TOLERANCE:
                all_ok = False
            print(f"  seed {seed:<5} AA={m['AA']:.5f}  ledger={expected:.5f}  "
                  f"delta={delta:+.5f}  [{flag}]   OA={m['OA']:.5f}  "
                  f"({dt:.1f}s for {val_idx.size:,} px)")
            rate = val_idx.size / dt
            print(f"          throughput {rate:,.0f} px/s")
            del model

        del padded_cube, ds

    print("\n" + "=" * 90)
    if all_ok:
        print("VALIDATION REPRODUCTION OK - pipeline reproduces the frozen ledger AA.")
        print("Safe to proceed to the one-shot official-test run.")
    else:
        print("VALIDATION REPRODUCTION MISMATCH - do NOT touch the test set.")
        print("Re-locate the checkpoints or fix the pipeline first.")
    print("=" * 90)
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
