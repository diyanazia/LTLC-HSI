# BLACK BOOK TERMINOLOGY FINALIZATION v1

**Date:** 2026-08-27 · **Wording-only. No numerical value was changed anywhere.**
All corrections are new versioned copies in `LTLC/results/final_thesis_tables_v1/`.
No historical source table was overwritten or deleted.

---

## 1. The two terms

| Term | Meaning | Where it appears |
|---|---|---|
| **POST-HOC STANDARD LA** | Logit adjustment `z − τ·log(π+ε)` applied to **frozen CE validation logits**. No retraining. | Notebook 06B post-hoc analysis: Tables 03, 04, 05, 06, paired-delta v3 |
| **TRAINED LA-LOSS** | A **separately trained** Experiment-B model using the LA loss function | 36-run ledger: Tables 01, 02, 09 |

These are different experimental objects. Conflating them already caused one documented error
(see `PAIRED_DELTA_CORRECTION_NOTICE_v1.md`), where a trained-model delta was proposed as a
"fix" for a post-hoc table.

---

## 2. Sweep performed

All **11** tables in `final_thesis_tables_v1/` were searched for ambiguous "LA" usage, in both
column headers and cell values. The sweep found **more than the two items originally
flagged**: Table 03 contained **two** distinct ambiguous method labels (not one), and Tables
01 and 05 carried no marker at all distinguishing trained from post-hoc results.

| Table | Ambiguity found | Action |
|---|---|---|
| Table 01 | method value `LA-loss` with no trained/post-hoc marker | **v2 issued** — added `comparison_object` |
| Table 02 | `LA-loss`, but `comparison_object` already states "TRAINED method vs TRAINED CE" | **compliant — no change** |
| Table 03 | `LA + Global TS` **and** `Standard LA (uncalibrated)` | **v2 issued** — 4 value renames |
| Table 04 | already `posthoc_standard_LA_minus_CE_mean` | compliant |
| Table 05 | no marker distinguishing post-hoc grid from trained results | **v2 issued** — added `comparison_object` |
| Table 06 | column `spearman_rarity_vs_LA_gain` | **v2 issued** — column renamed |
| Table 07 | no LA terminology | compliant |
| Table 08 | no LA terminology | compliant |
| Table 09 | `la_loss` as the trained method; `config` `tau0p5` | compliant in context; caption must say TRAINED |
| Paired deltas v3 | `posthoc_*` prefixes + `comparison_object` | compliant |
| Paired deltas MeanStd v3 | as above | compliant |

---

## 3. Every wording-only change, itemised

### `Thesis_Table_03_Calibration_Tradeoff_v2.csv` — 4 cell-value renames

| Row (dataset) | Column | Before | After |
|---|---|---|---|
| Pingan | `method` | `LA + Global TS` | `POST-HOC STANDARD LA + Global TS` |
| Pingan | `method` | `Standard LA (uncalibrated)` | `POST-HOC STANDARD LA (uncalibrated)` |
| Qingyun | `method` | `LA + Global TS` | `POST-HOC STANDARD LA + Global TS` |
| Qingyun | `method` | `Standard LA (uncalibrated)` | `POST-HOC STANDARD LA (uncalibrated)` |

*`Standard LA (uncalibrated)` was **not** in the original brief but is equally ambiguous — it
denotes post-hoc logit adjustment before temperature scaling, not the trained LA-loss model.*

### `Thesis_Table_06_Rarity_Mechanism_Correlations_v2.csv` — 1 column rename

| Before | After |
|---|---|
| `spearman_rarity_vs_LA_gain` | `spearman_rarity_vs_posthoc_standard_LA_gain` |

### `Thesis_Table_01_ExperimentB_Master_Results_v2.csv` — 1 column added

New `comparison_object` column, constant value:
`TRAINED Experiment-B model; spatially disjoint validation`

### `Thesis_Table_05_LTLC_Parameter_Stability_v2.csv` — 1 column added

New `comparison_object` column, constant value:
`POST-HOC LTLC grid over frozen Experiment-B CE validation logits`

---

## 4. Numerical invariance — verified programmatically

Every numeric field was extracted from v1 and v2 in order and compared:

| File | Numeric fields v1 → v2 | Identical |
|---|---|:--:|
| `Thesis_Table_01_..._v2.csv` | 100 → 100 | **True** |
| `Thesis_Table_03_..._v2.csv` | 64 → 64 | **True** |
| `Thesis_Table_05_..._v2.csv` | 60 → 60 | **True** |
| `Thesis_Table_06_..._v2.csv` | 6 → 6 | **True** |

## 5. New file hashes

```
15d0c82d3d026229  Thesis_Table_01_ExperimentB_Master_Results_v2.csv
a08bb638b33e64f6  Thesis_Table_03_Calibration_Tradeoff_v2.csv
fa26c3f71e48c0b4  Thesis_Table_05_LTLC_Parameter_Stability_v2.csv
71a6023d830728fe  Thesis_Table_06_Rarity_Mechanism_Correlations_v2.csv
```
(First 16 hex characters.) The v1 files are retained unchanged alongside them.

---

## 6. Which version to cite

| Purpose | Cite |
|---|---|
| Experiment-B validation ranking | `Thesis_Table_01_..._v2.csv` |
| Per-seed deltas vs CE | `Thesis_Table_02_PerSeed_Deltas_vs_CE_v1.csv` |
| Calibration trade-off | `Thesis_Table_03_..._v2.csv` |
| Per-class mechanism | `Thesis_Table_04_..._v2.csv` |
| LTLC parameter stability | `Thesis_Table_05_..._v2.csv` |
| Rarity correlations | `Thesis_Table_06_..._v2.csv` |
| Dataset overview | `Thesis_Table_07_Dataset_Overview_v2.csv` |
| Training-count reconciliation | `Thesis_Table_08_..._v1.csv` |
| Official-test confirmation | `Thesis_Table_09_..._v1.csv` |
| Post-hoc paired deltas | `Table_Paired_Recognition_Deltas_v3.csv` + `_MeanStd_v3.csv` |

---

## 7. Prose rules for the Black Book

1. Never write "Logit Adjustment", "LA", or "Standard LA" unqualified where both objects could
   be meant. Write **POST-HOC STANDARD LA** or **TRAINED LA-LOSS**.
2. On first use in each chapter, define both terms.
3. Figure captions carry the same obligation — see
   `BLACK_BOOK_FINAL_FIGURE_MANIFEST_v1.md` (F4, F5, F8, F9 all state which object they show).
4. Related naming discipline, same rule, different quantity: **OFFICIAL TRAINING-MASK COUNT**
   vs **EXPERIMENT-B POST-GUARD TRAINING COUNT** vs **NB01 PIXEL-RANDOM 70% TRAIN COUNT**
   (see `TRAINING_COUNT_SEMANTICS_AUDIT_v1.md`).
5. R1 with β = 0 **is** POST-HOC STANDARD LA exactly — say so rather than presenting R1 as a
   distinct method.
