# Official-test confirmation run (Experiment B)

Run once at 2026-08-26T16:58:29.860956+00:00 on cpu.

Result file: `official_test_confirmation_results.json` (sha256 a492833cacb53f4318ecde8a30fb3898936ef40a85570b5fdc3906697d16955a).

Scope of the claim this supports: no official-test result influenced any
Experiment-B method, hyperparameter, or checkpoint selection. It does NOT
claim the official test was never read at all -- Notebook 03's CE benchmark
reproduction evaluated on it earlier, by design.

This file existing means Experiment B has been scored on official test. Do not
delete it to try again. If a mechanical failure forces a re-run, document what
failed below this line first.

---

## Pre-run record (no mechanical failure occurred; this is provenance, not a re-run)

Executed once, locally, on CPU (torch 2.13.0+cpu, no GPU). Inference-only, `model.eval()`,
so CPU execution is numerically valid.

### Checkpoint provenance
Six checkpoints, all carrying `experiment: "Experiment B"`, `official_test_status: SEALED`,
`official_test_values_accessed: false`, `official_test_used: false`:
- Pingan balanced_softmax x3 seeds, from `LTLC_Notebook06A_ExperimentB_28of36_PreLA_...MIGRATION_v1.zip`
  (internal prefix `LTLC/runs/experiment_b_spatial_validation_v1/balanced_softmax/pingan/seed<N>/`).
  That archive's manifest reports `la_loss_completed: 0`, confirming it is the pre-LA base.
- Qingyun la_loss tau0p5 x3 seeds, from the 33of36 / 35of36 / 36of36 FULL DELTA archives, each
  hash-verified against its sibling `__SHA256.txt`.

Nothing under `audit/notebook04_longtail/` was extracted or read (the known Experiment-A
contamination trap `pingan_balanced_softmax_three_seed_manifest.json` IS present inside the
28of36 archive; extraction was restricted to the `runs/.../balanced_softmax/pingan/` prefix).
Nothing from `kaggle_exports/` was used.

### Configuration correction made BEFORE the run
The working notes specified `patch_size=13, radius=6` for BOTH scenes. That is correct for
Pingan but WRONG for Qingyun. Every Qingyun la_loss tau0p5 checkpoint self-reports
`architecture = {spectral_depth: 15, patch_size: 11, num_classes: 6, dropout: 0.4,
parameter_count: 256886}`. Loading at patch_size=13 fails with
`size mismatch for fc1.weight: checkpoint [256, 576] vs model [256, 1600]`.

The `radius` half of that error is the dangerous one: radius only sets the zero-pad offset, so
a radius inconsistent with patch_size decentres every extracted patch WITHOUT raising. The run
therefore uses `patch_size=11, radius=5` for Qingyun, and `check_architecture_matches()` now
enforces the checkpoint's own recorded architecture plus `radius == (patch_size-1)//2`.

This changed no scientific selection: the frozen rank-1 choices (Pingan balanced_softmax
training_counts; Qingyun la_loss tau=0.5) are untouched.

### Pipeline verified before the seal was spent
All six checkpoints were replayed through the Experiment-B SPATIAL VALIDATION split (already
fully used for selection; the official test file was not opened). Every seed reproduced the
frozen `run_ledger.csv` AA to 5 decimals:

| Scene | Seed | Reproduced val AA | Ledger val AA |
|---|---:|---:|---:|
| Pingan  | 42   | 0.76552 | 0.76552 |
| Pingan  | 123  | 0.77674 | 0.77674 |
| Pingan  | 3407 | 0.76626 | 0.76626 |
| Qingyun | 42   | 0.76417 | 0.76417 |
| Qingyun | 123  | 0.76357 | 0.76357 |
| Qingyun | 3407 | 0.75071 | 0.75071 |

Six independent exact reproductions establish that the recovered architecture, state-dict load,
patch extraction, label mapping and metric code are all correct, so the one-shot test run could
not be wasted on a mechanical bug.

### Split disjointness (measured after the run)
Official test indices vs Experiment-B indices:
- Pingan : test 1,026,838 px; intersection with ExpB train = 0; with ExpB val = 0.
- Qingyun: test   859,401 px; intersection with ExpB train = 0; with ExpB val = 0.

No test pixel was seen in Experiment-B training or validation.
