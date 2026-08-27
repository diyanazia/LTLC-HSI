# MASTER ARCHIVE PATH MAP v1

**Date:** 2026-08-27
**Master scientific archive:** `CSE498/LTLC/` — read-only, unmodified, 4,536.5 MB, 582 files.
**This working copy:** `CSE498/LTLC_BLACKBOOK_FINAL/` — 9.4 MB.

Everything deliberately left behind is listed here with its canonical master path, so nothing
has to be hunted for later.

---

## 1. Checkpoints and archives — master only

The working copy contains **no model checkpoints and no ZIP archives**. Their manifests and
SHA-256 records *are* included (`11_reproducibility/*__MANIFEST.json`, `*__SHA256.txt`).

| What | Canonical master path | Size |
|---|---|---|
| **Sole source of 24 of 36 Experiment-B checkpoints** | `LTLC/migrations/LTLC_Notebook06A_ExperimentB_28of36_PreLA_Kaggle_to_Colab_SELF_CONTAINED_MIGRATION_v1.zip` | 358.2 MB |
| Cumulative LA-loss delta (supersedes 29–35of36) | `LTLC/experiment_b_colab_persistence/LTLC_Notebook06A_ExperimentB_36of36_Post_Qingyun_LA_tau0p5_Seed3407_FULL_DELTA_FROM_28of36_MIGRATION_v1.zip` | 63.1 MB |
| Intermediate deltas 29–35of36 (redundant; payload ⊂ 36of36) | `LTLC/experiment_b_colab_persistence/…{29,30,31,32,33,34,35}of36…zip` | 263.0 MB |
| Earlier migration (⊂ 28of36) | `LTLC/migrations/notebook06a_post_cell17f_kaggle_v1/LTLC_Notebook06A_PostCell17F_Kaggle_Migration_v1.zip` | 155.1 MB |
| Experiment-A Notebook-04 export | `LTLC/LTLC_Kaggle_Notebook04.zip`; `LTLC_backups/notebook04/LTLC_Notebook04_FINAL_Kaggle_export.zip` | 141.1 / 60.5 MB |
| Per-method Experiment-A exports (4 of 5 ⊂ NB04 export) | `LTLC/kaggle_exports/*.zip` | 33.2 MB |
| Loose Experiment-B checkpoints | `LTLC/runs/experiment_b_spatial_validation_v1/` | 55.6 MB |
| Experiment-A checkpoints | `LTLC/runs/longtail_training_baselines/` | 60.9 MB |

**`28of36` + `36of36` together cover all 41 distinct `best_valAA` filenames.** Both are
KEEP_CORE and irreplaceable.

## 2. Bulk data — master only

| What | Canonical master path | Size |
|---|---|---|
| Raw QUH cubes | `LTLC/data_raw/{Pingan,Qingyun,Tangdaowan}/` | 2,777.6 MB |
| Frozen PCA cubes (model inputs) | `LTLC/data_cache/pca_normalized_cubes/{pingan,qingyun}_pca15_rowminmax_float32.npy` | 145.6 MB |
| Tangdaowan PCA cube (scene excluded from Experiment B) | `LTLC/data_cache/pca_normalized_cubes/tangdaowan_pca20_rowminmax_float32.npy` | 119.7 MB |
| **Notebook-03 official-test logits/indices/labels** | `LTLC/runs/hybridsn_ce_baseline/logits/official_test/` | 263.6 MB |

The Notebook-03 official-test outputs are **not** bulk: they are the independent copy of
`test_indices` / `test_labels_model` that proved the official-test split unchanged
(`08_official_test/OFFICIAL_TEST_TECHNICAL_VERIFICATION_v1.md` §5.2). Cite by path.

### Official-test split files — deliberately NOT copied

`LTLC/split_indices/{pingan,qingyun}_fixed_split_seed2026.npz` are **not** in this working
copy: they contain raw official-test indices and labels, and the thesis needs only their
canonical array digests. Those digests are in
`08_official_test/BLACK_BOOK_REPRODUCIBILITY_NOTE_v1.md` §B:

```
Pingan  test_indices       0cd6c34db9fc61b1e120a178bff93f014383ecb6a21bdd6064c804b5a3419357
Pingan  test_labels_model  451608235b26d260ac09964481e9bac29d7b198e7b46e19f7fc8d6beaaed6fb1
Qingyun test_indices       239a0f85d3f6e63f3f090adf012eda41d02804415395a0d685dfa0567bbe8f9d
Qingyun test_labels_model  64cc441cf817b33072534eda5bb0c128c4ad863dbf8e691f7a5edc32aa13e2f1
```

## 3. Authoritative hashes to quote

| Artifact | SHA-256 (first 16) | Verified against |
|---|---|---|
| 36-run ledger | `6335262b572a389a` | `external_run_ledger.sha256` in the closing audit — **match** |
| Validation summary table | `daf365de9ac96278` | `outputs.summary_markdown.sha256` in the freeze — **match** |
| Official-test result JSON | `a492833cacb53f43` | present, retained, single-use |
| Experiment-B split (Pingan) | `7e7c6f583223a43e` | `split_sha256` recorded inside the Pingan checkpoint — **byte-identical** |
| PCA cube (Pingan) | `857ffcb8f1a3837f` | NB02 `normalized_cube_sha256` — **byte-identical** |
| PCA cube (Qingyun) | `15d94523dbf5708d` | NB02 `normalized_cube_sha256` — **byte-identical** |

## 4. Environments — master only

`CSE498/.venv_sealed/` (687.4 MB, 22,268 files) — runtime of the one-time official-test
confirmation; **treat conservatively, do not delete.**
`CSE498/.venv_finalqa/` (335.5 MB, 10,441 files) — QA/plotting environment.

Neither is copied here. Full `pip freeze` for both:
`11_reproducibility/FINAL_QA_ENVIRONMENT_v1.txt`.

## 5. Historical notebooks — master only, cited not copied

| Notebook | Canonical master path | Why it matters |
|---|---|---|
| `Untitled0.ipynb` | `CSE498/LTLC/notebooks/Untitled0.ipynb` | **Sole provenance** for `LTLC_Kaggle_Notebook04.zip` (141 MB). No training, no inference, no scientific read of official-test data. |
| `Untitled1.ipynb` | `CSE498/LTLC/notebooks/Untitled1.ipynb` | **Primary execution record of the failed v1 official-test attempt**, 2026-08-26T12:17:20.019717Z. Confirmation phrase entered; `FileNotFoundError` inside `recover_hybridsn_class()` before any checkpoint or test-data access; no result written. |

Both are **KEEP_AUDIT**, retained unchanged and unrenamed in the master. Neither is copied
here — see `01_protocol/BLACK_BOOK_GOVERNANCE_TIMELINE_ADDENDUM_v1.md` §5 for the copy policy
and the single circumstance under which `Untitled1.ipynb` should be added to
`11_reproducibility/`.

## 6. Superseded artifacts — master only

Retained unchanged as correction history; **must not appear as active thesis results**:

- `LTLC/results/notebook06b_experiment_b_thesis_ready_v2/Fig_N5_Calibration_NLL_vs_TailECE_v2.png` (Grade C)
- `LTLC/results/final_thesis_tables_v1/Thesis_Table_{01,03,05,06}_…_v1.csv` (pre-terminology)
- `LTLC/results/notebook06b_experiment_b_thesis_ready_v2/Table_Paired_Recognition_Deltas_{v2,MeanStd_v2}.csv` (**correct**, superseded only for clarity)
- `Day1_Improvements_2026-08-26/DATA_INTEGRITY_NOTES.md` and `PROJECT_HANDOFF_2026-08-26.md` (contain the later-corrected "stale paired-delta" claim)
- `LTLC/final_qa_2026-08-27/FINAL_GOVERNANCE_AUDIT_v1.md`, `FINAL_REPOSITORY_CLEANUP_AUDIT_v1.{md,csv}`

## 7. Restricted — do not cite

| File | Reason |
|---|---|
| `LTLC/audit/{scene}_ltlc_class_statistics.csv` | bare `train_count` holds **NB01 70% pixel-random** counts (concept 2) while every other bare `train_count` holds post-guard counts |
| `LTLC/audit/final_training_imbalance_summary.csv` | named "final" but reports IR 71.0 (concept 2); the Experiment-B IR is 397.4 — copied here **only** as labelled context |
| `LTLC/results/notebook06b_…/Table_ClassLevel_Mechanism_Summary_v2.csv` | bare `train_count`; cite Table 04 v2 instead |
| Anything under `LTLC/audit/notebook04_longtail/` | Experiment-A, includes the known contamination-trap manifest |
