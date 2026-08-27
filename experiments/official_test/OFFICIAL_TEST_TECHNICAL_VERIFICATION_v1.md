# OFFICIAL-TEST TECHNICAL VERIFICATION v1

> **DERIVED_PUBLIC_SANITIZED_COPY.** This is the public release copy. Two absolute local
> filesystem paths in section 5.6 were replaced with `<LOCAL_PROJECT_ROOT>/...` so that a local
> machine username is not published. **No scientific value, hash, timestamp, conclusion, test
> result or technical finding was altered.** Canonical master copy:
> `CSE498/LTLC/final_qa_2026-08-27/OFFICIAL_TEST_TECHNICAL_VERIFICATION_v1.md`
> SHA-256 `f51219ba43b041d9f891c2b0b06a88429addbe6db69a7049e780311c6fdd8d8a`


**Date:** 2026-08-27 · **Method:** inspection of the executed script, checkpoint metadata,
frozen preprocessing artifacts, split files and the result JSON.
**No official-test inference was rerun.** No model was executed against the test partition
during this audit.

---

## 1. Final status

> ## PASS

All six evaluations are technically sound and the reported numbers are safe to report.

The official-test split container-hash discrepancy noted in the first draft of this document
has been **fully resolved** by the forensic analysis in §5. It is a **benign serialization
difference (Category A)**: the array contents are proven element-identical to an independently
stored copy written before the container changed, and both container hashes are themselves
recorded in the project's own frozen artifacts at their respective dates. No provenance gap
remains, so the earlier "WITH DOCUMENTATION ISSUE" qualifier has been withdrawn.

---

## 2. Per-evaluation verification (6 rows)

| # | Dataset | Method | Seed | Checkpoint | Epoch | Sel. metric | Experiment id | Classes | Spec. depth | Patch | Radius | Params | `official_test_used` | ckpt SHA-256 (file == result JSON) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Pingan | BalancedSoftmax | 42 | `balanced_softmax__pingan__seed42__best_valAA.pt` | 44 | best_validation_AA | Experiment B | 10 | 15 | 13 | 6 | 519,546 | false | ✔ `c233ab73a8ae1cc5…` |
| 2 | Pingan | BalancedSoftmax | 123 | `…seed123__best_valAA.pt` | 86 | best_validation_AA | Experiment B | 10 | 15 | 13 | 6 | 519,546 | false | ✔ `cf1162fd0b97b23f…` |
| 3 | Pingan | BalancedSoftmax | 3407 | `…seed3407__best_valAA.pt` | 5 | best_validation_AA | Experiment B | 10 | 15 | 13 | 6 | 519,546 | false | ✔ `e311dc7e67695332…` |
| 4 | Qingyun | LA_Loss τ=0.5 | 42 | `la_loss__qingyun__tau0p5__seed42__best_valAA.pt` | 29 | best_validation_AA | experiment_b_spatial_validation_v1 | 6 | 15 | **11** | **5** | 256,886 | false | ✔ `ee25de80c873e05c…` |
| 5 | Qingyun | LA_Loss τ=0.5 | 123 | `…seed123__best_valAA.pt` | 50 | best_validation_AA | experiment_b_spatial_validation_v1 | 6 | 15 | **11** | **5** | 256,886 | false | ✔ `7cef532a3222a7ba…` |
| 6 | Qingyun | LA_Loss τ=0.5 | 3407 | `…seed3407__best_valAA.pt` | 52 | best_validation_AA | experiment_b_spatial_validation_v1 | 6 | 15 | **11** | **5** | 256,886 | false | ✔ `ba4579589489c419…` |

Full hashes:
```
Pingan  42   c233ab73a8ae1cc58279d8a7285b644cf4dc648173fc69d435ab36a93731483e
Pingan  123  cf1162fd0b97b23f6455d9fcd75f45a9460f5d54a9cc519ab41f6f63a3279294
Pingan  3407 e311dc7e676953327835a6625bf84bff2b61ba259d94fc3d6351b6899151cf8d
Qingyun 42   ee25de80c873e05c94e3806869d7b5efc656c31bf008c6571563d4935490f9aa
Qingyun 123  7cef532a3222a7baff696016bf882d8878510177c08df7e70d3f9fcd48c942e8
Qingyun 3407 ba4579589489c419d9133a3f43f7160f58b1693acdab1dd52fda3dd8c67deeb2
```
Every on-disk checkpoint hash equals the hash recorded in
`official_test_confirmation_results.json` — the evaluated weights are the retained weights.

**Note on row 3 (epoch 5):** this is not an anomaly. The frozen run ledger independently
records `best_AA_epoch = 5` for Pingan / balanced_softmax / seed 3407 (with
`best_OA_epoch = 79`). Balanced Softmax up-weights tail classes from the first epochs, so an
early AA peak under a `best_validation_AA` policy is expected. Worth one sentence in the
thesis; not a defect.

---

## 3. CRITICAL QINGYUN GEOMETRY CHECK

Working notes claimed `patch_size = 13, radius = 6` for **both** scenes. That is wrong for
Qingyun. Four independent frozen sources agree on the correct values:

| Source | Pingan | Qingyun |
|---|---|---|
| `experiment_b_training_protocol_v1_frozen.json` → `training_engine.backbone.dataset_specific_only` | patch 13, 519,546 params | **patch 11, 256,886 params** |
| `audit/notebook02_preprocessing/canonical_patch_manifest.json` | patch_size 13, **margin 6** | patch_size 11, **margin 5** |
| `audit/notebook03_hybridsn/notebook03_master_audit.json` | patch `[13,13,15]` | patch `[11,11,15]` |
| Each checkpoint's own `architecture` block | patch 13 | patch 11 |

**Rule enforced:** `radius == (patch_size - 1) // 2`
- Pingan: (13−1)//2 = 6 = frozen margin 6 ✔
- Qingyun: (11−1)//2 = 5 = frozen margin 5 ✔

**Why this matters more than an ordinary typo.** A wrong `patch_size` raises immediately
(`size mismatch for fc1.weight: checkpoint [256,576] vs model [256,1600]`). A wrong `radius`
raises **nothing** — radius sets only the zero-pad offset, so an inconsistent radius silently
decentres every extracted patch and produces plausible but wrong predictions. The run used
the correct 11/5, and `SEALED_TEST_v2.py::check_architecture_matches()` now enforces both the
checkpoint's recorded architecture and the radius rule at load time.

---

## 4. Shared-condition verification

| Check | Result | Evidence |
|---|---|---|
| PCA configuration | Pingan PCA-15, Qingyun PCA-15, `covariance_eigh`, EVR ≥ 0.9998 | NB02 preprocessing summary |
| PCA cube integrity | **byte-identical** to frozen NB02 `normalized_cube_sha256` (Pingan `857ffcb8…`, Qingyun `15d94523…`) | recomputed 2026-08-27 |
| Input normalization | frozen NB02 row-wise min-max over retained PCA channels; no recomputation | `training_engine.preprocessing`, `full_cube_pca_recomputed: false` |
| Padding | zero padding, lazy patch extraction | NB02 `lazy_zero_padding_v1`; frozen protocol `padding: "zero"` |
| Class mapping | Pingan 1–10 → 0–9; Qingyun 1–6 → 0–5; test label ranges observed `[0,9]` and `[0,5]` | NB01 protocol metadata; split files |
| Correct test indices/labels | members `test_indices`, `test_labels_model`; n = 1,026,838 (Pingan) and 859,401 (Qingyun) — equal to frozen NB02 `test_centers` | recomputed |
| Train ∩ test | **0 pixels** (both scenes) | recomputed |
| Validation ∩ test | **0 pixels** (both scenes) | recomputed |
| Guard band ∩ test | **0 pixels** (both scenes) | recomputed (§5.3) |
| No duplicate / out-of-range test indices | **0 duplicates**; all indices < H·W | recomputed (§5.3) |
| Official split is a true partition | train+val+test == unique union (1,140,937 / 954,893) | recomputed (§5.3) |
| Test arrays identical to NB03's independent copy | element-identical, same order, 6/6 runs | §5.2 |
| `model.eval()` used | yes — `SEALED_TEST_v2.py:344` | source |
| Gradients disabled | yes — `@torch.no_grad()` at `:348` | source |
| No optimizer step | **zero** occurrences of `optimizer`, `.step()`, `.backward()` | source scan |
| No training | **zero** occurrences of `.train()` | source scan |
| No augmentation | dataset applies no transform; `shuffle=False`, `drop_last=False` | source `:350–351` |
| Validation AA reproduced **before** test scoring | 6/6 exact to 5 decimals | §5 below |

### Validation AA reproduction (executed before the test partition was opened)

| Dataset | Seed | Reproduced val AA | Frozen ledger val AA | Δ |
|---|---:|---:|---:|---:|
| Pingan | 42 | 0.76552 | 0.76552 | 0.00000 |
| Pingan | 123 | 0.77674 | 0.77674 | 0.00000 |
| Pingan | 3407 | 0.76626 | 0.76626 | 0.00000 |
| Qingyun | 42 | 0.76417 | 0.76417 | 0.00000 |
| Qingyun | 123 | 0.76357 | 0.76357 | 0.00000 |
| Qingyun | 3407 | 0.75071 | 0.75071 | 0.00000 |

Six exact reproductions establish that architecture recovery, state-dict loading, patch
extraction, label mapping and metric computation were all correct before the one-time
measurement was taken.

---

## 5. OFFICIAL-TEST SPLIT CONTAINER FORENSICS (resolved)

### 5.0 The question

The official-test split files on disk do not match the `split_sha256` recorded in the
Notebook-02 canonical patch manifest. A `.npz` is a ZIP archive, so a container hash can
change without any array changing. The container hash alone is therefore **not** evidence
that the scientific split changed, and was not treated as such.

| File | NB01/NB02/NB03 recorded | On disk now |
|---|---|---|
| `pingan_fixed_split_seed2026.npz` | `738703dd…` | `788ee600…` |
| `qingyun_fixed_split_seed2026.npz` | `57607a2a…` | `8d09ab91…` |
| `tangdaowan_fixed_split_seed2026.npz` | `b5283f3a…` | `4a85ae8e…` |

All **three** files differ — a systematic, not targeted, difference.

### 5.1 Member inventory and canonical content hashes

Each file holds 15 members, all `int64` except `validation_fraction` (`float64`), DEFLATE-
compressed, ZIP timestamps normalised to `(1980,1,1)`. Canonical hashes below are computed
over a deterministic representation of the **array content**, not the container:

```
sha256( key | dtype | shape | C-contiguous raw bytes )
```

**Pingan** (`train 79,869 / val 34,230 / test 1,026,838`):

| key | dtype | shape | n | canonical sha256 |
|---|---|---|---:|---|
| `train_indices` | int64 | (79869,) | 79,869 | `a19234c6bdc6f50a6811e8c77ccbc2f080d183f8e2b9785681656a7e310329db` |
| `val_indices` | int64 | (34230,) | 34,230 | `60ae9b5e61b84cefb91cdb7dc2d6eab0861f7bd88450035449b89091df1803f9` |
| **`test_indices`** | int64 | (1026838,) | 1,026,838 | `0cd6c34db9fc61b1e120a178bff93f014383ecb6a21bdd6064c804b5a3419357` |
| `train_labels_original` | int64 | (79869,) | 79,869 | `9eefd9e3c6dc9c1b5842c94a65e0efe091015cb7184ef58a6318ba3e4b099aee` |
| `val_labels_original` | int64 | (34230,) | 34,230 | `3732fa2915bd1e609603dc2ef3f0462272c62d43107d44affa761e33e8e6b6d3` |
| `test_labels_original` | int64 | (1026838,) | 1,026,838 | `f101d17ad358d9197a4bfc07de92e5c2a0c860f238c14aa7de04e5a1e29aa0c3` |
| `train_labels_model` | int64 | (79869,) | 79,869 | `2f862ea58d9b278e6954906811651d07b67dc4ed7dbdd644126ed94273286530` |
| `val_labels_model` | int64 | (34230,) | 34,230 | `f2c6c6a6818c0119ec3b8d4295ab1ab4e184f93468c89d6b9f6ce643b798c22b` |
| **`test_labels_model`** | int64 | (1026838,) | 1,026,838 | `451608235b26d260ac09964481e9bac29d7b198e7b46e19f7fc8d6beaaed6fb1` |
| `evaluation_class_ids` | int64 | (10,) | 10 | `ec7625c9f64290b2e9a3e00cffde2e7fb3f583ebba91e0401224397f894d5fca` |
| `full_gt_class_ids` | int64 | (10,) | 10 | `9f70f7082ea11701e16d477b04d84a026cf7e22f659e1ba36ca97876992aa014` |
| `spatial_shape` | int64 | (2,) | 2 | `70ec801fac96699aa7ff364d61df83085a7c07f2c1bb1dfc3984392521741aa6` |
| `spectral_bands` | int64 | (1,) | 1 | `efb8f6d94502036df374726cdde0221e7c3a4a8960c41267c21fb770bf9ab18d` |
| `validation_split_seed` | int64 | (1,) | 1 | `be69fb578d698312c68e8b070263afafc7d6dab7533e2778d60f1536e132a83f` |
| `validation_fraction` | float64 | (1,) | 1 | `0d55db59e09e3649f61b1ea0eba52a1df44ea77be3d588813ed7efdf90bf3835` |

Aggregate canonical digest: `d04556293aeecf77cbffaebaac08fd67e8aa3eb74c319469524dba3b39437ab6`

**Qingyun** (`train 66,844 / val 28,648 / test 859,401`), same schema:
`test_indices` = `239a0f85d3f6e63f3f090adf012eda41d02804415395a0d685dfa0567bbe8f9d`;
`test_labels_model` = `64cc441cf817b33072534eda5bb0c128c4ad863dbf8e691f7a5edc32aa13e2f1`.
Aggregate: `70b47e9f798a3770208941eda953a4ef46445e31c559bc439e9718e3cf4d136b`

**Tangdaowan** aggregate: `e88c87df8ba06ab59e0fc5628cd6d77eeb51e638fcd2cdf3347c9f465e7b3b2b`
(recorded for completeness; not used in Experiment B).

### 5.2 Element-by-element comparison against an independent stored copy — the decisive test

Only one version of each split file exists on disk, so a file-to-file diff is impossible.
However, **Notebook 03 independently serialized its own copy of the official-test indices and
labels on 2026-08-12**, in nine `*_official_test_outputs.npz` files under
`runs/hybridsn_ce_baseline/logits/official_test/`, each containing `indices`, `labels`,
`predictions` and `logits`. Those files were written **before** the container change (NB03
records the OLD hash, §5.4) and are a genuine second copy of the arrays.

Comparison of the current split file against all six relevant NB03 files
(2 scenes × 3 seeds):

| Check | Pingan (3 seeds) | Qingyun (3 seeds) |
|---|---|---|
| Same number of test samples | ✔ 1,026,838 | ✔ 859,401 |
| `test_indices` identical **and in identical order** | ✔ | ✔ |
| Same index **set** (order-independent) | ✔ | ✔ |
| NB03 `labels` == `test_labels_model`, elementwise in order | ✔ | ✔ |
| `(index, label)` pairs identical in order | ✔ | ✔ |
| `(index, label)` pairs identical as a set | ✔ | ✔ |
| Canonical `test_indices` hash equal | ✔ `0cd6c34d…` | ✔ `239a0f85…` |
| Canonical `test_labels_model` hash equal | ✔ `45160823…` | ✔ `64cc441c…` |

**Order does not differ.** The arrays are identical in content *and* ordering, so the
order-contingency case does not arise. (NB03 `labels` correctly match `test_labels_model`,
not `test_labels_original` — the expected 0-based model encoding.)

### 5.3 Internal integrity of the split actually used

| Check | Pingan | Qingyun |
|---|---|---|
| Duplicate test indices | **0** | **0** |
| Test indices within cube bounds | ✔ [25, 1,229,999] < 1,230,000 | ✔ [82, 1,196,729] < 1,196,800 |
| `len(test_indices) == len(labels)` | ✔ | ✔ |
| `test_labels_model` range | [0, 9] = expected | [0, 5] = expected |
| `original → model` mapping matches NB01 exactly | ✔ | ✔ |
| train ∩ test / val ∩ test / train ∩ val | 0 / 0 / 0 | 0 / 0 / 0 |
| train+val+test == unique union (true partition) | ✔ 1,140,937 | ✔ 954,893 |
| **Experiment-B train ∩ official test** | **0** | **0** |
| **Experiment-B val ∩ official test** | **0** | **0** |
| **Experiment-B guard-band ∩ official test** | **0** | **0** |

No duplicates, no missing indices, no out-of-range indices, labels correspond exactly to their
indices, and the official test partition is disjoint from every Experiment-B partition
including the guard band.

### 5.4 Why the container hashes differ — with dates

Both hash values are recorded in the project's own artifacts, at different stages:

| Era | Artifact | Pingan hash | Qingyun hash |
|---|---|---|---|
| NB01 | `notebook01_protocol_metadata.json` | `738703dd…` | `57607a2a…` |
| NB02 | `notebook02_master_preprocessing_audit.json`, `canonical_patch_manifest.json` | `738703dd…` | `57607a2a…` |
| NB03 | `runs/hybridsn_ce_baseline/metrics/pingan_seed42_best_validation.json` → `split_sha256` | `738703dd…` | — |
| **NB05** | `notebook05_best_valAA_train_val_split_audit.json` → `archive_sha256` for `split_indices/{scene}_fixed_split_seed2026.npz` | **`788ee600…`** | **`8d09ab91…`** |
| **NB06A** | `experiment_b_split_construction_attempt_v1.json` → `historical_split_source` | **`788ee600…`** | **`8d09ab91…`** |

So the container was re-written **once, between Notebook 03 and Notebook 05**, and the
project's audit trail **records both epochs against the same logical filename**. The current
hash is not unattested — it is pinned in two later frozen artifacts.

Critically, **Notebook 06A built the Experiment-B spatially disjoint split from the file with
the CURRENT hash** (`historical_split_source` + `788ee600…`, alongside
`guard_excluded_count: 14144`). Experiment B and the sealed run therefore used the same
container, and the NB03-era content is proven equal to it (§5.2).

Mechanism, demonstrated empirically on these exact arrays — identical content, five different
container hashes:

| Writer setting | container sha256 (first 16) |
|---|---|
| `np.savez` (STORED) | `9bf7568ada7b7e1a` |
| `np.savez_compressed` (default) | `d630f835c25e8be1` |
| DEFLATE level 1 | `3cd1c7d4fc9c7a9b` |
| DEFLATE level 6 | `5c961ce36af63dd6` |
| DEFLATE level 9 | `bb47b2aaa562fb9d` |
| **actual on-disk** | `788ee600b0375d77` |

A `.npz` hash is a function of the writer, zlib build and compression settings; it is not a
function of array content. The systematic change across all three scene files is consistent
with a single bulk re-save/transfer step, not with a scientific edit.

### 5.5 Classification

> **A — benign serialization / container difference.**
> Same arrays, same values, same dtypes, same shapes, **same ordering**. Not B (ordering is
> identical), not C, not D.

Predictions and metrics are invariant to this difference because **nothing the model consumes
changed**: `test_indices` and `test_labels_model` are element-identical in identical order, so
patch extraction, batching order, and every metric are bit-for-bit unaffected. The evaluation
would produce the same numbers from either container.

### 5.6 Which file the one-time run actually loaded

`SEALED_TEST_v2.py:236` — `official_test_split_path()` returns
`SPLIT_DIR / f"{dataset.lower()}_fixed_split_seed2026.npz"`, with
`SPLIT_DIR = PROJECT_ROOT/"split_indices"` and
`PROJECT_ROOT = Path(__file__).resolve().parent/"LTLC"`. Resolved concretely:

```
<LOCAL_PROJECT_ROOT>/CSE498/LTLC/split_indices/pingan_fixed_split_seed2026.npz    (exists)
<LOCAL_PROJECT_ROOT>/CSE498/LTLC/split_indices/qingyun_fixed_split_seed2026.npz   (exists)
```

`official_test_confirmation_results.json` independently records
`split_file: pingan_fixed_split_seed2026.npz` / `qingyun_fixed_split_seed2026.npz`. Only one
copy of each exists in the repository. **The run loaded exactly the files audited above**
(container `788ee600…` / `8d09ab91…`, canonical test-array hashes `0cd6c34d…` / `239a0f85…`).

### 5.7 Residual disclosure

The only remaining item is documentary, and is now fully explained rather than open: **two
container-hash epochs exist for the same logical file**, both attested in the project's own
artifacts, with content proven identical across the boundary. Record this in the
reproducibility appendix; cite the **canonical array hashes** (§5.1) rather than container
hashes when asserting provenance for these two files.

For contrast, the **Experiment-B split** file is byte-identical to the `split_sha256` recorded
inside the Pingan checkpoint (`7e7c6f5832…`), and both PCA cubes are byte-identical to their
frozen NB02 hashes — those provenance chains are unbroken at the container level.

---

## 6. Conclusion

All six evaluations used the correct architecture, correct per-scene geometry, correct frozen
inputs, correct test indices and labels, inference-only execution, and test pixels disjoint
from every Experiment-B partition — with the whole pipeline validated against the frozen
ledger beforehand. The one outstanding provenance question has been resolved to Category A
(benign serialization) with element-level proof.

**PASS.** The official-test numbers are safe to report, subject to the governance disclosure
in `THESIS_PROTOCOL_GOVERNANCE_PARAGRAPH_v1.md`.
