# Splits — metadata only

This directory contains the **construction records and frozen manifests** for the Experiment-B
spatially disjoint splits. It deliberately does **not** contain the split `.npz` arrays.

## Why the `.npz` files are not published here

`pingan_experiment_b_spatial_split_v1.npz` and `qingyun_experiment_b_spatial_split_v1.npz` contain
per-pixel **ground-truth label arrays** derived from the QUH dataset
(`train_labels_original`, `val_labels_original`, `guard_excluded_labels_original`, and their
model-encoded counterparts). Publishing them would redistribute a substantial portion of QUH's
ground truth, whose redistribution rights are not ours to grant.

The same reasoning applies, more strongly, to the official-test split files
(`*_fixed_split_seed2026.npz`), which are likewise not published.

## What is published instead

| File | Contents |
|---|---|
| `experiment_b_spatial_split_manifest_v1_frozen.json` | Frozen split manifest |
| `experiment_b_split_construction_attempt_v1.json` | Full construction record: cluster parameters, guard thresholds, per-class train/val/guard counts, and the source split container hash |
| `experiment_b_split_artifact_linkage_correction_v1.json` | Linkage correction record |

Together these fully specify **how** the split was built and **what it contains**, without
redistributing labels.

## Reproducing and verifying the split

1. Obtain the QUH dataset (README §11).
2. Run `src/06A_Spatially_Disjoint_Validation_Robustness_Study.ipynb`, which contains the split
   construction code.
3. Verify your regenerated split against the counts and hashes recorded here.

Reference geometry and counts:

| Scene | Patch radius | Guard threshold | Guard-excluded | Train | Validation |
|---|---:|---:|---:|---:|---:|
| Pingan | 6 | Chebyshev ≤ 12 | 14,144 | 65,710 | 34,245 |
| Qingyun | 5 | Chebyshev ≤ 10 | 3,732 | 63,179 | 28,581 |

The Experiment-B Pingan split container is recorded as SHA-256
`7e7c6f583223a43e8e37db2dad7052fc16b2d42ff3e674a4134acdb51608d1fb` — byte-identical to the value
stored inside the trained Pingan checkpoints, so a regenerated file can be checked against an
independently attested reference.

Canonical **array-content** digests for the official-test arrays (independent of container
serialization) are published in
`experiments/official_test/BLACK_BOOK_REPRODUCIBILITY_NOTE_v1.md`.

## If you decide to publish the split arrays anyway

That is a licensing judgement for the dataset owner, not a technical obstacle. The files are
`188,685` and `156,711` bytes and live in the project master archive at
`LTLC/split_indices/experiment_b_spatial_validation_v1/`. If you add them, also add matching
negation rules to `.gitignore`, which currently excludes all `*.npz`.
