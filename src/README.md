# src — code

Notebooks are copied **unchanged** from the project master so that their hashes match the frozen
originals. That means they carry their original execution outputs and, in two scripts, hardcoded
paths from the machine they were run on. Nothing here has been rewritten.

## Notebooks (execution order)

| File | Role |
|---|---|
| `01_QUH_Data_Preflight_Integrity_Audit.ipynb` | Protocol freeze: split seed 2026, validation fraction 0.3, seeds 42/123/3407, class mappings, frequency groups |
| `02_QUH_Benchmark_Preprocessing_and_Patch_Cache.ipynb` | PCA, row-wise min-max normalization, cached cubes, patch geometry (13/6, 11/5, 9/4) |
| `03_HybridSN_Baseline_Training_and_Benchmark_Reproduction.ipynb` | **Canonical HybridSN definition.** Downstream code recovers the class from this file by AST parsing rather than re-typing it, so the architecture cannot drift between copies. Also reproduces the published CE benchmark |
| `04_LongTail_Training_Baselines.ipynb` | **Experiment A** — the pixel-random precursor. Retained as methodological motivation only; **never** cite its numbers as evidence of method quality |
| `05_Posthoc_Calibration_LTLC.ipynb` | Post-hoc LTLC and calibration, Experiment-A era |
| `06A_Spatially_Disjoint_Validation_Robustness_Study.ipynb` | **Experiment B** — spatial split construction, guard band, the 36 training runs |
| `06B_ExperimentB_Posthoc_LTLC_and_Calibration_Evaluation.ipynb` | Experiment-B post-hoc LTLC / R1 recognition search and calibration study over frozen CE validation logits |

## Scripts

| File | Role | Note |
|---|---|---|
| `VALIDATION_REPRO_CHECK.py` | Replays checkpoints against the Experiment-B **validation** split and compares AA to the frozen run ledger | Touches no official-test data. Run this before any irreversible evaluation |
| `SEALED_TEST_v2.py` | The script that performed the one-time official-test evaluation | Defaults to `PREFLIGHT_ONLY = True`; refuses to run twice while a result file exists |
| `stats_analysis.py` | Per-seed paired deltas, exact sign-flip test, bootstrap intervals | **Hardcoded paths** — see below |
| `build_clean_tables.py` | Builds the cleaned thesis tables | **Hardcoded paths** — see below |
| `make_figures_finalqa_v1.py` | Generates the five regenerated approved figures | Paths already corrected to repository-relative form |

## Path handling in the public copies

Three scripts were made **repository-portable** for public release. They originally carried
absolute paths from the environments they were executed in; those were replaced with
`pathlib` resolution relative to the repository root:

```python
REPO_ROOT = Path(__file__).resolve().parent.parent
```

| Script | Resolves to |
|---|---|
| `stats_analysis.py` | reads `experiments/…FINAL_RUN_LEDGER_v1.csv`; writes to `reproducibility/` |
| `build_clean_tables.py` | writes to `results/tables/` |
| `make_figures_finalqa_v1.py` | writes to `results/figures/`; reads `reproducibility/significance_test_results_v1.json` |

**Only path resolution changed.** No formula, parameter, selection rule, table content or
numerical computation was altered. Each is marked `DERIVED_PORTABLE_PUBLIC_COPY` in
`GITHUB_REPOSITORY_MANIFEST_v1.csv`, which records the canonical master SHA-256 alongside the
public one so the change is auditable.

One caveat: `make_figures_finalqa_v1.py` regenerates the spatial split-map figure from the split
`.npz` arrays, which are **not redistributed** here (see `../splits/README.md`). Point
`SPLIT_DIR` at a local copy to reproduce that one figure; the other four regenerate as-is.

The notebooks are copied **unchanged** and retain their original Colab mount paths
(`/content/drive/MyDrive/...`) in code cells and stored outputs. These are the standard Colab
mount point, identical for every Colab user and containing no personal identifier. They were left
intact so the notebooks stay byte-identical to the frozen originals.

## Not included

`SUPERSEDED_v1_DO_NOT_RUN__SEALED_TEST_run_once_in_colab.py` — a superseded, buggy first version
of the sealed-test harness. It is retained in the project master archive as audit history and is
deliberately excluded from this repository.
