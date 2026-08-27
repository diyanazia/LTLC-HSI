# FINAL TABLE QA v1

**Date:** 2026-08-27 · **Clean output folder:** `LTLC/results/final_thesis_tables_v1/`
No original table was overwritten or deleted; every correction is a new versioned file.

---

## 1. Scorecard

| TABLE | PURPOSE | SOURCE | PLACEMENT | GRADE | ISSUES | FINAL STATUS |
|---|---|---|---|:--:|---|---|
| `Thesis_Table_01_ExperimentB_Master_Results_v1.csv` | Experiment-B validation ranking, 5 methods × 2 scenes | 36-run ledger via validation summary freeze | **Main — Results** | **A** | none; verified against `VALIDATION_SUMMARY_TABLE_v1.md` | **USE** |
| `Thesis_Table_02_PerSeed_Deltas_vs_CE_v1.csv` | Per-seed ΔAA vs CE, mean ± SD, descriptive interval | regenerated `significance_test_results_v1.json` | **Main — Results** | **A** | supersedes the CI-led Table 02 | **USE** |
| `Thesis_Table_03_Calibration_Tradeoff_v1.csv` | NLL / ECE / Tail-ECE / Brier by calibration method | `Table_Calibration_Tradeoff_v2.csv` | **Main — Calibration** | **B** | method column says "LA + Global TS" — rename to **POST-HOC STANDARD LA + Global TS** | **USE after rename** |
| `Thesis_Table_04_PerClass_Frequency_and_Mechanism_v2.csv` | Per-class rarity, CE difficulty, LA gain, α gain | 06B mechanism summary | **Main — Mechanism** | **A** | count/rarity columns now explicitly post-guard | **USE** |
| `Thesis_Table_05_LTLC_Parameter_Stability_v1.csv` | Selected τ/α, α=0 comparison, near-optimal counts | 06B parameter stability | **Main — Mechanism** | **A** | none | **USE** |
| `Thesis_Table_06_Rarity_Mechanism_Correlations_v1.csv` | Spearman ρ, descriptive | 06B correlations | **Main — Mechanism** | **B** | `spearman_rarity_vs_LA_gain` is ambiguous → **post-hoc standard LA**; `p_values_reported=False` is correct and must stay | **USE after rename** |
| `Thesis_Table_07_Dataset_Overview_v2.csv` | Scene overview, official IR, Tangdaowan exclusion | frequency-group records | **Main — Data** | **A** | columns renamed `official_train_mask_*` | **USE** |
| `Thesis_Table_08_TrainingCount_Reconciliation_v1.csv` | All three count concepts side by side, per class | frozen Exp-B class statistics + frequency groups | **Appendix** (or Data chapter) | **A** | new this pass | **USE** |
| `Thesis_Table_09_OfficialTest_Confirmation_v1.csv` | Official-test AA/OA/F1/κ per seed + checkpoint SHA-256 | `official_test_confirmation_results.json` | **Main — Results** | **A** | must carry the governance disclosure | **USE with disclosure** |
| `Table_Paired_Recognition_Deltas_v3.csv` | Post-hoc per-seed deltas, unambiguous names | frozen post-hoc selections | **Main — Mechanism** | **A** | zero numerical change from v2 | **USE** |
| `Table_Paired_Recognition_Deltas_MeanStd_v3.csv` | Aggregates of the above | as above | **Main — Mechanism** | **A** | zero numerical change from v2 | **USE** |

### Superseded / restricted (retained, not deleted)

| TABLE | STATUS |
|---|---|
| `Day1/tables/Thesis_Table_02_Significance_Tests_vs_CE.csv` | **APPENDIX ONLY.** Numerically correct (fully reproduced) but leads with bootstrap CI and includes a paired-t p of 0.0039 that reads as significant. Superseded by Table 02 v1. |
| `Day1/tables/Thesis_Table_04`, `_07` | superseded by v2 reissues (naming only) |
| `Table_ClassLevel_Mechanism_Summary_v2.csv` | **DO NOT cite directly** — bare `train_count` (post-guard) invites the concept confusion. Cite Table 04 v2. |
| `Table_PerClass_Rarity_Difficulty_and_AdaptiveGain_v2.csv` | **Appendix only**, with count-concept caption |
| `Table_Paired_Recognition_Deltas_v2.csv` / `_MeanStd_v2.csv` | **CORRECT and retained.** Cite v3 for clarity. See `PAIRED_DELTA_CORRECTION_NOTICE_v1.md` |
| `audit/{scene}_ltlc_class_statistics.csv` | **DO NOT use for Experiment B** — `train_count` is the NB01 pixel-random 70% count |
| `audit/final_training_imbalance_summary.csv` | **DO NOT cite as Experiment-B IR** — reports 71.0, the concept-2 value; Experiment-B post-guard IR is 397.4 |

---

## 2. Checks applied

| Check | Result |
|---|---|
| Correct source | ✔ every retained table traced to a frozen primary artifact |
| Version | ✔ all clean outputs carry `_v1`/`_v2`/`_v3` suffixes |
| Rounding | ✔ 4 dp throughout the clean set; **fixed** — v3 and Table 08 no longer expose 15–18 dp floats in thesis-facing columns (full precision remains in the JSON/v2 originals) |
| Mean ± SD present | ✔ Tables 01, 02, 03 |
| No 15-decimal floats in main tables | ✔ (Table 02 v1 rounds to 6 dp; Table 01/03 to 4 dp) |
| Method naming consistency | ⚠ **two renames required** (Tables 03 and 06) — see §1 |
| Class-count semantics | ✔ resolved via Tables 04 v2, 07 v2, 08 |
| No stale paired-delta data | ✔ v2 verified correct; v3 issued for clarity |
| No SHA columns outside reproducibility context | ⚠ Table 09 carries `checkpoint_sha256` **by design** — keep it, but place Table 09's hash column in the reproducibility appendix if the main-text version needs to be narrow |
| Correct datasets | ✔ Pingan + Qingyun only in all Experiment-B tables; Tangdaowan appears **only** in Table 07 (overview) with its exclusion reason |
| Correct configs | ✔ Pingan LA-loss τ=1, Qingyun LA-loss τ=0.5, Focal γ=1, LDAM C=0.5/0.25 — match the closing audit |
| Correct seeds | ✔ 42 / 123 / 3407 everywhere |
| Experiment-B-only claims | ✔ no Experiment-A value appears in any Experiment-B table |
| **No test-set ΔAA-vs-CE claim** | ✔ **Table 09 contains no CE row and no delta column** — no Experiment-B CE official-test result exists, so no such comparison can be formed |

---

## 3. Two renames still required

Both are label-only edits to be applied when the tables are typeset:

1. `Thesis_Table_03_Calibration_Tradeoff_v1.csv` — `method` value
   `LA + Global TS` → `POST-HOC STANDARD LA + Global TS`.
2. `Thesis_Table_06_Rarity_Mechanism_Correlations_v1.csv` — column
   `spearman_rarity_vs_LA_gain` → `spearman_rarity_vs_posthoc_standard_LA_gain`.

These were left as-is rather than silently rewritten, so the change is visible and
deliberate. Neither affects any number.

---

## 4. Mandatory table captions

- **Table 01:** Experiment-B **validation** results (spatially disjoint). Not official-test
  performance. Mean ± SD over seeds 42/123/3407.
- **Table 02:** **TRAINED method vs TRAINED CE.** n = 3 seeds — suggestive, not confirmatory.
  Bootstrap columns are descriptive; with n = 3 their endpoints equal the observed min/max.
- **Table 03:** Validation calibration only. Calibration is **not** a recognition result.
- **Tables 04 / 08:** counts are **EXPERIMENT-B POST-GUARD** (Table 08 shows all three
  concepts); post-guard IR is 397.4 (Pingan) and 264.3 (Qingyun) versus nominal 71.0/28.5.
- **Table 06:** Spearman ρ descriptive only; no p-values; few classes; spatially dependent
  pixels.
- **Table 07:** counts are **OFFICIAL TRAINING-MASK**; Tangdaowan listed for context and
  excluded from Experiment B.
- **Table 09:** one-time post-development confirmatory evaluation; see
  `THESIS_PROTOCOL_GOVERNANCE_PARAGRAPH_v1.md`. **No CE comparison is available on official
  test.**
- **v3 paired deltas:** **POST-HOC STANDARD LA / LTLC applied to frozen CE validation
  logits** — not the trained-model comparison. Qingyun seed 3407 shows exact zeros because
  τ = 0 was selected (identity transform).

---

## 5. SHA-256 of the clean table set

```
4e5d1f4d2874e404  Thesis_Table_01_ExperimentB_Master_Results_v1.csv
54a6bb1e0a491000  Thesis_Table_02_PerSeed_Deltas_vs_CE_v1.csv
f2972ce39acc04bd  Thesis_Table_03_Calibration_Tradeoff_v1.csv
a7140adbfdb25f73  Thesis_Table_04_PerClass_Frequency_and_Mechanism_v2.csv
97a891e5d67ef435  Thesis_Table_05_LTLC_Parameter_Stability_v1.csv
e56d745d7cf79886  Thesis_Table_06_Rarity_Mechanism_Correlations_v1.csv
4d0a5ad4d6bc26b2  Thesis_Table_07_Dataset_Overview_v2.csv
4950fff06b42c1a3  Thesis_Table_08_TrainingCount_Reconciliation_v1.csv
699f83ee5a796746  Thesis_Table_09_OfficialTest_Confirmation_v1.csv
66f7fe2ff86fe6be  Table_Paired_Recognition_Deltas_v3.csv
3b14fd222c99475a  Table_Paired_Recognition_Deltas_MeanStd_v3.csv
```
(First 16 hex characters; full digests reproducible from the files.)
