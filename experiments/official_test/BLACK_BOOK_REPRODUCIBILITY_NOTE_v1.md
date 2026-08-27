# BLACK BOOK REPRODUCIBILITY NOTE v1 — official-test split integrity

**Date:** 2026-08-27
Thesis-ready text plus the supporting hash table. Detailed container forensics stay in
`OFFICIAL_TEST_TECHNICAL_VERIFICATION_v1.md` §5 — **do not** put ZIP/DEFLATE internals in the
main thesis.

---

## A. Drop-in text for the reproducibility appendix

> **Official-test split integrity.**
> The official-test partition for each scene is distributed as a compressed NumPy archive.
> These archives were serialized at two attested points in the project's history, so the
> outer container checksums recorded early in the pipeline (Notebooks 01–03) differ from those
> recorded later (Notebooks 05 and 06A) and from the files as they now stand. A container
> checksum covers archive metadata and compression settings as well as data, so it is not a
> reliable identifier for the scientific content of the split.
>
> Integrity was therefore established at the level of the arrays themselves. For each scene,
> canonical SHA-256 digests were computed over a deterministic representation of each array —
> its key, dtype, shape and contiguous raw bytes — and the two arrays that determine the
> evaluation, `test_indices` and `test_labels_model`, were additionally compared
> element-by-element against an independent copy serialized by Notebook 03 before the later
> container was written. Across all six Notebook-03 runs the indices and labels were identical
> in value **and in identical order**, so no reordering occurred and the evaluation is
> invariant to the container difference.
>
> The split used was further confirmed to contain no duplicate or out-of-range indices, to
> have labels corresponding exactly to their indices under the Notebook-01 class mapping, and
> to form a true partition of the labelled pixels. Its intersection with the Experiment-B
> training set, the Experiment-B validation set, and the Experiment-B guard band was **zero
> pixels in every case, for both scenes**.
>
> Provenance for these two files should therefore be cited by canonical array digest rather
> than by container checksum. The Experiment-B split archive and both PCA cubes, by contrast,
> remain byte-identical to their originally recorded container checksums.

---

## B. Canonical array digests (cite these)

SHA-256 over `key | dtype | shape | C-contiguous raw bytes`.

### Pingan — `split_indices/pingan_fixed_split_seed2026.npz`

| Array | dtype | shape | n | canonical SHA-256 |
|---|---|---|---:|---|
| `test_indices` | int64 | (1026838,) | 1,026,838 | `0cd6c34db9fc61b1e120a178bff93f014383ecb6a21bdd6064c804b5a3419357` |
| `test_labels_model` | int64 | (1026838,) | 1,026,838 | `451608235b26d260ac09964481e9bac29d7b198e7b46e19f7fc8d6beaaed6fb1` |

### Qingyun — `split_indices/qingyun_fixed_split_seed2026.npz`

| Array | dtype | shape | n | canonical SHA-256 |
|---|---|---|---:|---|
| `test_indices` | int64 | (859401,) | 859,401 | `239a0f85d3f6e63f3f090adf012eda41d02804415395a0d685dfa0567bbe8f9d` |
| `test_labels_model` | int64 | (859401,) | 859,401 | `64cc441cf817b33072534eda5bb0c128c4ad863dbf8e691f7a5edc32aa13e2f1` |

Whole-file aggregate canonical digests (ordered over the 15-member list):
Pingan `d04556293aeecf77cbffaebaac08fd67e8aa3eb74c319469524dba3b39437ab6`;
Qingyun `70b47e9f798a3770208941eda953a4ef46445e31c559bc439e9718e3cf4d136b`.

---

## C. Container-checksum epochs (appendix footnote only)

| Stage | Recorded in | Pingan | Qingyun |
|---|---|---|---|
| Notebooks 01–03 | protocol metadata; preprocessing audit; `pingan_seed42_best_validation.json` | `738703dd…` | `57607a2a…` |
| Notebooks 05 & 06A, and current files | `notebook05_best_valAA_train_val_split_audit.json`; `experiment_b_split_construction_attempt_v1.json` | `788ee600…` | `8d09ab91…` |

Both epochs are attested in the project's own artifacts. Notebook 06A constructed the
Experiment-B spatially disjoint split from the file bearing the **current** checksum, and the
one-time official-test evaluation loaded that same file.

---

## D. Verification summary table (appendix)

| Check | Pingan | Qingyun |
|---|---|---|
| Test samples | 1,026,838 | 859,401 |
| `test_indices` identical to NB03 copy, same order | ✔ (3/3 seeds) | ✔ (3/3 seeds) |
| `test_labels_model` identical to NB03 copy, same order | ✔ (3/3 seeds) | ✔ (3/3 seeds) |
| `(index, label)` pairs identical, in order and as a set | ✔ | ✔ |
| Duplicate test indices | 0 | 0 |
| Out-of-range test indices | 0 | 0 |
| Label↔index correspondence under NB01 mapping | ✔ | ✔ |
| train / val / test form a true partition | ✔ 1,140,937 | ✔ 954,893 |
| Experiment-B **train** ∩ official test | **0** | **0** |
| Experiment-B **validation** ∩ official test | **0** | **0** |
| Experiment-B **guard band** ∩ official test | **0** | **0** |

**Classification:** benign serialization difference. Same arrays, same values, same dtypes,
same shapes, same ordering.

---

## E. Cross-references

- Full forensics, including the empirical demonstration that identical arrays yield five
  different container checksums under different writer settings:
  `OFFICIAL_TEST_TECHNICAL_VERIFICATION_v1.md` §5 (graded **PASS**).
- Environment manifests: `FINAL_QA_ENVIRONMENT_v1.txt`.
- Official-test result and checkpoint digests: `official_test_confirmation_results.json`,
  `Thesis_Table_09_OfficialTest_Confirmation_v1.csv`.
