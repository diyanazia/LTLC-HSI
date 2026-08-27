# BLACK BOOK SOURCE MAP v1

**Date:** 2026-08-27 · Working copy: `CSE498/LTLC_BLACKBOOK_FINAL/`
Master scientific archive: `CSE498/LTLC/` — **read-only, never modified.**

Paths below are relative to `LTLC_BLACKBOOK_FINAL/` unless prefixed `MASTER:`.
No thesis prose has been written. This maps chapters to evidence only.

Binding constraints while writing: `12_black_book/FINAL_CLAIM_BOUNDARIES_v1.md` and
`12_black_book/BLACK_BOOK_PREWRITING_CHECKLIST_v1.md`.

---

## Chapter 1 — Introduction

| Need | Source |
|---|---|
| Problem framing, contributions | `12_black_book/BLACK_BOOK_WRITING_HANDOFF_v1.md` §2, §3, §20 |
| Headline leakage finding | `09_results/figures/Fig_ExperimentA_vs_B_Leakage_Comparison.png` |
| What may / may not be claimed | `12_black_book/FINAL_CLAIM_BOUNDARIES_v1.md` |
| Scope + honest appraisal | `10_final_qa/FINAL_BLACK_BOOK_READINESS_AUDIT_v1.md` |

## Chapter 2 — Literature review

| Need | Source |
|---|---|
| Backbone lineage (HybridSN) | `05_code/03_HybridSN_Baseline_Training_and_Benchmark_Reproduction.ipynb` |
| Long-tail method definitions as implemented | `05_code/04_LongTail_Training_Baselines.ipynb`, `05_code/06A_…ipynb` |
| LTLC / R1 formulations | `07_posthoc/LTLC_Notebook06B_ExperimentB_Posthoc_Recognition_Freeze_v1.json` (`formulas` block) |
| Future direction | `12_black_book/BLACK_BOOK_WRITING_HANDOFF_v1.md` §21 |

**No external literature is stored here** — bibliography is the writer's to assemble.

## Chapter 3 — Datasets and preprocessing

| Need | Source |
|---|---|
| Cube shapes, class mappings, split seed | `02_dataset_metadata/notebook01_protocol_metadata.json` |
| **OFFICIAL TRAINING-MASK counts** | `02_dataset_metadata/{scene}_frequency_groups.csv`, `{scene}_official_class_counts.csv`, `official_imbalance_summary.csv` |
| **EXPERIMENT-B POST-GUARD counts** | `02_dataset_metadata/experiment_b_training_class_statistics_v1_frozen.json` |
| Three-concept reconciliation | `09_results/tables/Thesis_Table_08_TrainingCount_Reconciliation_v1.csv` |
| Scene overview + Tangdaowan exclusion | `09_results/tables/Thesis_Table_07_Dataset_Overview_v2.csv` |
| PCA config, patch sizes, margins, normalization, cube hashes | `03_preprocessing/canonical_patch_manifest.json`, `notebook02_master_preprocessing_audit.json`, `notebook02_preprocessing_summary.csv` |
| Class-frequency figure | `09_results/figures/Fig_ClassFrequency_LongTail_Distribution.png` |

**Canonical geometry — state explicitly:** Pingan patch 13 / margin 6 · Qingyun patch 11 /
margin 5 · Tangdaowan patch 9 / margin 4. Report **both** imbalance ratios (official 71.0× /
28.5×; Experiment-B post-guard 397.4× / 264.3×) — see
`10_final_qa/TRAINING_COUNT_SEMANTICS_AUDIT_v1.md`.

## Chapter 4 — Experiment A → B protocol evidence and governance

| Need | Source |
|---|---|
| Frozen split + training protocols | `01_protocol/experiment_b_spatial_validation_protocol_v1_frozen.json`, `experiment_b_training_protocol_v1_frozen.json` (+2 clarifications) |
| Rank-1 freeze (validation-only selection) | `01_protocol/LTLC_Notebook06A_ExperimentB_VALIDATION_SUMMARY_FREEZE_v1.json` |
| NB05 / NB06B terminal decisions (the sealed gate) | `01_protocol/notebook05_terminal_validation_scientific_decision.json`, `LTLC_Notebook06B_ExperimentB_Terminal_Scientific_Decision_v1.json`, `LTLC_Notebook06B_ExperimentB_FINAL_RELEASE_v2.json` |
| **Governance audit (authoritative)** | `01_protocol/FINAL_GOVERNANCE_AUDIT_v2.md` |
| **Paragraph to insert verbatim** | `01_protocol/THESIS_PROTOCOL_GOVERNANCE_PARAGRAPH_v1.md` (Version A) |
| How to mention the failed v1 attempt | `01_protocol/BLACK_BOOK_GOVERNANCE_TIMELINE_ADDENDUM_v1.md` |
| Experiment-A leakage evidence | `09_results/figures/Fig_ExperimentA_vs_B_Leakage_Comparison.png`; `05_code/04_LongTail_Training_Baselines.ipynb` |

**Experiment A is methodological history only** — never a source of method-quality claims.

## Chapter 5 — Experimental design

| Need | Source |
|---|---|
| Spatial split files | `04_splits/{pingan,qingyun}_experiment_b_spatial_split_v1.npz` |
| Split construction + freeze metadata | `04_splits/experiment_b_spatial_split_manifest_v1_frozen.json`, `experiment_b_split_construction_attempt_v1.json`, `experiment_b_split_artifact_linkage_correction_v1.json` |
| Guard-band geometry + Tangdaowan infeasibility | `01_protocol/experiment_b_spatial_validation_protocol_v1_frozen.json` (`cell3_geometric_feasibility`) |
| Split map figure | `09_results/figures/Fig_Spatial_TrainVal_Split_Map.png` |
| 36-run design | `06_experiment_b/…FINAL_RUN_LEDGER_v1.csv`, `…FINAL_CLOSING_AUDIT_v1.json` |
| Checkpoint provenance (archives stay in master) | `06_experiment_b/CHECKPOINT_PROVENANCE_NOTE_v1.md` |

## Chapter 6 — Results (validation) and Chapter 10 — Official test

| Need | Source |
|---|---|
| **Authoritative ledger** | `06_experiment_b/LTLC_Notebook06A_ExperimentB_36of36_FINAL_RUN_LEDGER_v1.csv` |
| Validation summary + consolidation | `06_experiment_b/…VALIDATION_SUMMARY_TABLE_v1.md`, `…VALIDATION_MEAN_STD_v1.csv`, `…ALL36…`, `…SELECTED30…`, `baseline_selection.csv` |
| Master results table | `09_results/tables/Thesis_Table_01_ExperimentB_Master_Results_v2.csv` |
| Per-seed deltas + statistics caveat | `09_results/tables/Thesis_Table_02_PerSeed_Deltas_vs_CE_v1.csv`; `09_results/figures/Fig_PerSeed_Delta_vs_CE.png`; `10_final_qa/STATISTICAL_ANALYSIS_VERIFICATION_v1.md` |
| **Official-test result** | `08_official_test/official_test_confirmation_results.json`; `09_results/tables/Thesis_Table_09_OfficialTest_Confirmation_v1.csv` |
| Official-test verification + run log | `08_official_test/OFFICIAL_TEST_TECHNICAL_VERIFICATION_v1.md`, `OFFICIAL_TEST_RUN_LOG.md` |

**No Experiment-B CE exists on official test — never claim a test-set improvement over CE.**

## Chapter 7 — Discussion

| Need | Source |
|---|---|
| Final findings narrative | `07_posthoc/ExperimentB_Novelty_Strengthened_Findings_v2.md` |
| Claim discipline | `12_black_book/FINAL_CLAIM_BOUNDARIES_v1.md` |
| Statistical honesty wording | `10_final_qa/STATISTICAL_ANALYSIS_VERIFICATION_v1.md` §5 |
| Paired-delta correction (τ=0 identity) | `10_final_qa/PAIRED_DELTA_VERIFICATION_AUDIT_v1.md`, `PAIRED_DELTA_CORRECTION_NOTICE_v1.md` |

## Chapter 8 — Mechanism analysis *(the intellectual core)*

| Need | Source |
|---|---|
| Frozen recognition grid + selections | `07_posthoc/LTLC_Notebook06B_ExperimentB_Posthoc_Recognition_Grid_v1.csv`, `…Selected_Recognition_v1.csv`, `…Recognition_Freeze_v1.json` |
| Rarity vs difficulty | `09_results/figures/Fig_N1_Rarity_vs_CE_Difficulty_v2.png`; `09_results/tables/Thesis_Table_04_…_v2.csv`, `Thesis_Table_06_…_v2.csv` |
| Parameter landscape / identifiability | `09_results/figures/Fig_N3_LTLC_Seed42_Parameter_Landscape_v2.png`; `Thesis_Table_05_…_v2.csv` |
| R1 β profile | `09_results/figures/Fig_N4_R1_Beta_Profile_v2.png` |
| Post-hoc paired deltas | `09_results/tables/Table_Paired_Recognition_Deltas_v3.csv` + `_MeanStd_v3.csv` |
| Isolated α contribution (appendix) | `09_results/figures/Fig_N2_Rarity_vs_Adaptive_LTLC_Gain_v2.png` |

## Chapter 9 — Calibration

| Need | Source |
|---|---|
| Calibration trade-off table | `09_results/tables/Thesis_Table_03_Calibration_Tradeoff_v2.csv` |
| Calibration figure | `09_results/figures/Fig_Calibration_Tradeoff_Redesigned.png` |
| Calibration parameters / terminal results | `07_posthoc/LTLC_Notebook06B_ExperimentB_Calibration_Parameters_v1.csv`, `…Final_Validation_Results_v1.csv`, `…Final_Validation_MeanStd_v1.csv` |

Calibration is **never** a recognition result.

## Chapter 11 — Conclusion and future work

`12_black_book/BLACK_BOOK_WRITING_HANDOFF_v1.md` §19 (limitations), §20 (contribution),
§21 (future work).

## Chapter 12–14 — Appendices

| Need | Source |
|---|---|
| Reproducibility prose + canonical array hashes | `08_official_test/BLACK_BOOK_REPRODUCIBILITY_NOTE_v1.md` |
| Environment manifests | `11_reproducibility/FINAL_QA_ENVIRONMENT_v1.txt` |
| Archive manifests / hash records | `11_reproducibility/*__MANIFEST.json`, `*__SHA256.txt` |
| Master path map (what stayed behind, and why) | `11_reproducibility/MASTER_ARCHIVE_PATH_MAP_v1.md` |
| Working-copy integrity | `BLACKBOOK_WORKING_COPY_MANIFEST_v1.csv` / `.md` |
| Full audit chain | `10_final_qa/` (14 documents) |
| Figure captions + placement | `12_black_book/BLACK_BOOK_FINAL_FIGURE_MANIFEST_v1.md` |

---

## Chapter → figure/table quick index

| Ch | Figures | Tables |
|---|---|---|
| 3 | ClassFrequency | 07 v2, 08 v1 |
| 4 | ExperimentA_vs_B | — |
| 5 | Spatial_TrainVal_Split_Map | — |
| 6 | PerSeed_Delta_vs_CE | 01 v2, 02 v1 |
| 8 | N1, N3, N4 | 04 v2, 05 v2, 06 v2, Paired v3 + MeanStd v3 |
| 9 | Calibration_Tradeoff_Redesigned | 03 v2 |
| 10 | — | 09 v1 |
| Appendix | N2 | 08 v1 |

`Fig_N5_Calibration_NLL_vs_TailECE_v2.png` is **EXCLUDED** and is not present in this working
copy. Its replacement is `Fig_Calibration_Tradeoff_Redesigned.png`.
