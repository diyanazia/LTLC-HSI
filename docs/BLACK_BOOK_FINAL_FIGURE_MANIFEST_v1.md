# BLACK BOOK FINAL FIGURE MANIFEST v1

**Date:** 2026-08-27
**Rule: ONE canonical path per approved scientific figure. No duplicates were created.**

Figures live in two physical directories for a deliberate reason: the five regenerated
figures were rebuilt during the 2026-08-27 QA pass, while the four mechanism figures needed
no scientific change and therefore remain at their original Notebook-06B paths. **Nothing was
copied, renamed, or re-exported to make the directories look uniform.** This manifest, not the
directory layout, is the index.

Grades are quoted from `FINAL_FIGURE_QA_v1.md` (A = publication ready, B = minor polish,
C = redesign needed).

---

## APPROVED — MAIN THESIS

### F1 · Class-frequency long-tail distribution
- **Canonical filename:** `Fig_ClassFrequency_LongTail_Distribution.png`
- **Canonical path:** `LTLC/results/final_thesis_figures_v1/Fig_ClassFrequency_LongTail_Distribution.png`
- **Source data:** `audit/{scene}_frequency_groups.csv` → `official_train` (OFFICIAL TRAINING-MASK COUNT)
- **Grade:** A · **Placement:** Main · **Chapter:** 3 — Datasets and Preprocessing
- **Purpose:** Establish the long-tail structure of all three QUH scenes.
- **Approved caption:** *Per-class OFFICIAL TRAINING-MASK pixel counts for the three QUH
  scenes (log scale), coloured by Head/Medium/Tail frequency group, with the official
  imbalance ratio annotated per scene. These are official training-mask counts, not
  Experiment-B post-guard counts; the corresponding Experiment-B post-guard imbalance ratios
  are substantially higher (397.4× Pingan, 264.3× Qingyun). Tangdaowan is shown for dataset
  context only and is excluded from Experiment B.*
- **Superseded:** No

### F2 · Experiment A vs Experiment B leakage comparison
- **Canonical filename:** `Fig_ExperimentA_vs_B_Leakage_Comparison.png`
- **Canonical path:** `LTLC/results/final_thesis_figures_v1/Fig_ExperimentA_vs_B_Leakage_Comparison.png`
- **Source data:** `audit/notebook03_hybridsn/ce_checkpoint_manifest.csv` (Experiment A);
  Experiment-B validation summary (Experiment B)
- **Grade:** A · **Placement:** Main · **Chapter:** 5 — Experiment A: the leaky precursor
- **Purpose:** Quantify how far conventional pixel-random validation overstates performance.
- **Approved caption:** *Cross-Entropy validation accuracy before and after correcting the
  patch-overlap leakage, same backbone and same scenes. Under the pixel-random split
  (Experiment A) accuracy is ≈99.99%; under the spatially disjoint guard-banded split
  (Experiment B) it falls to 88.2% OA / 73.9% AA (Pingan) and 74.3% OA / 75.4% AA (Qingyun).
  The split changed, not the method.*
- **Superseded:** No

### F3 · Spatial train/validation split map
- **Canonical filename:** `Fig_Spatial_TrainVal_Split_Map.png`
- **Canonical path:** `LTLC/results/final_thesis_figures_v1/Fig_Spatial_TrainVal_Split_Map.png`
- **Source data:** `split_indices/experiment_b_spatial_validation_v1/{scene}_experiment_b_spatial_split_v1.npz`
- **Grade:** B · **Placement:** Main · **Chapter:** 6 — Experiment B: design
- **Purpose:** Visual proof of zero train/validation patch-footprint overlap.
- **Approved caption:** *Experiment-B spatially disjoint train/validation partition, plotted
  from the frozen split indices rather than schematically. Guard-band pixels (grey) are
  excluded from both training and validation and appear as a thin seam between the blue and
  orange regions. Train–validation patch-footprint overlap is zero by construction.*
- **Superseded:** No

### F4 · Per-seed ΔAA versus Cross-Entropy
- **Canonical filename:** `Fig_PerSeed_Delta_vs_CE.png`
- **Canonical path:** `LTLC/results/final_thesis_figures_v1/Fig_PerSeed_Delta_vs_CE.png`
- **Source data:** `final_qa_2026-08-27/significance_test_results_v1.json`, regenerated from
  the 36-run ledger
- **Grade:** A · **Placement:** Main · **Chapter:** 7 — Experiment B: recognition results
- **Purpose:** Show all three seed observations rather than an interval that merely restates
  their range.
- **Approved caption:** *Per-seed paired differences in class-balanced accuracy versus
  Cross-Entropy on Experiment-B spatially disjoint validation, for **TRAINED** long-tail
  methods (not post-hoc logit adjustment). Individual seeds are shown as markers, the black
  bar is mean ± SD, and the faint grey band is a bootstrap 95% interval reported
  descriptively only: with n = 3 seeds its endpoints coincide exactly with the observed
  minimum and maximum. Differences are suggestive, not confirmatory.*
- **Superseded:** No

### F5 · Calibration trade-off (redesigned)
- **Canonical filename:** `Fig_Calibration_Tradeoff_Redesigned.png`
- **Canonical path:** `LTLC/results/final_thesis_figures_v1/Fig_Calibration_Tradeoff_Redesigned.png`
- **Source data:** `Table_Calibration_Tradeoff_v2.csv` (`nll_mean`, `tail_ece_mean`)
- **Grade:** A · **Placement:** Main · **Chapter:** 9 — Calibration
- **Purpose:** Show that the lowest NLL coincides with the worst tail-class calibration.
- **Approved caption:** *Validation calibration trade-off between overall negative
  log-likelihood and tail-class expected calibration error. Rarity-conditioned LTLC attains
  the lowest NLL but markedly worse tail-class ECE than a single global temperature. "POST-HOC
  STANDARD LA" denotes logit adjustment applied to frozen CE validation logits, not the
  separately trained LA-loss model. This is a calibration result only and does not constitute
  a recognition improvement: a positive scalar temperature is order-preserving and leaves hard
  predictions unchanged.*
- **Superseded:** No — **this figure is the approved replacement for the excluded Fig N5.**

### F6 · Rarity versus CE difficulty
- **Canonical filename:** `Fig_N1_Rarity_vs_CE_Difficulty_v2.png`
- **Canonical path:** `LTLC/results/notebook06b_experiment_b_thesis_ready_v2/Fig_N1_Rarity_vs_CE_Difficulty_v2.png`
- **Source data:** `Table_ClassLevel_Mechanism_Summary_v2.csv` / `Table_PerClass_Rarity_Difficulty_and_AdaptiveGain_v2.csv`
- **Grade:** A · **Placement:** Main · **Chapter:** 8 — Mechanism analysis
- **Purpose:** Test the hypothesis' antecedent — that rarer classes are harder.
- **Approved caption:** *Per-class training-frequency rarity against mean Cross-Entropy class
  error, with class identifiers labelled. Rarity is computed from **EXPERIMENT-B POST-GUARD**
  training counts. The Spearman correlations have opposite signs across scenes (ρ = +0.406 on
  Pingan, ρ = −0.371 on Qingyun), indicating that class frequency is not a consistent proxy
  for empirical class difficulty. Correlations are descriptive only; no p-values are claimed,
  as there are few classes and hyperspectral pixels are spatially dependent.*
- **Superseded:** No

### F7 · LTLC seed-42 parameter landscape
- **Canonical filename:** `Fig_N3_LTLC_Seed42_Parameter_Landscape_v2.png`
- **Canonical path:** `LTLC/results/notebook06b_experiment_b_thesis_ready_v2/Fig_N3_LTLC_Seed42_Parameter_Landscape_v2.png`
- **Source data:** `LTLC_Notebook06B_ExperimentB_Posthoc_Recognition_Grid_v1.csv`
- **Grade:** B · **Placement:** Main · **Chapter:** 8 — Mechanism analysis
- **Purpose:** Show the wide near-optimal plateau, i.e. α non-identifiability.
- **Approved caption:** *Validation class-balanced accuracy across the post-hoc LTLC (τ, α)
  grid for seed 42, per scene. The broad high-accuracy plateau at low α indicates that the
  rarity-adaptive coefficient is not sharply identifiable. **Colour scales are independently
  normalized within each dataset panel to emphasize the within-dataset parameter-response
  landscape; colours should therefore not be compared quantitatively across panels.** Seed 42
  only.*
- **Superseded:** No
- **Note:** Not regenerated. The independent normalization is a presentation property and is
  disclosed in the caption rather than altered, per instruction.

### F8 · R1 β profile
- **Canonical filename:** `Fig_N4_R1_Beta_Profile_v2.png`
- **Canonical path:** `LTLC/results/notebook06b_experiment_b_thesis_ready_v2/Fig_N4_R1_Beta_Profile_v2.png`
- **Source data:** `Table_R1_Beta_Profile_v2.csv`
- **Grade:** A · **Placement:** Main · **Chapter:** 8 — Mechanism analysis
- **Purpose:** Show that additional rarity weighting monotonically degrades accuracy.
- **Approved caption:** *Best validation class-balanced accuracy over τ as a function of the
  R1 adaptive coefficient β, seed 42. Accuracy declines monotonically with β on both scenes
  and is maximised at β = 0, consistent with the frozen protocol selecting β = 0 for both
  datasets — at which point R1 is exactly identical to POST-HOC STANDARD LA. Note the
  compressed vertical range (≈0.750–0.771): the visual slope corresponds to roughly a two
  percentage-point effect.*
- **Superseded:** No

---

## APPROVED — APPENDIX

### F9 · Isolated contribution of the rarity-adaptive α term
- **Canonical filename:** `Fig_N2_Rarity_vs_Adaptive_LTLC_Gain_v2.png`
- **Canonical path:** `LTLC/results/notebook06b_experiment_b_thesis_ready_v2/Fig_N2_Rarity_vs_Adaptive_LTLC_Gain_v2.png`
- **Source data:** `Table_PerClass_Rarity_Difficulty_and_AdaptiveGain_v2.csv`
- **Grade:** B · **Placement:** **Appendix** · **Chapter:** 14 — Appendices (supporting
  mechanism evidence)
- **Purpose:** Isolate the α term's per-class effect against the same-τ POST-HOC STANDARD LA
  comparator, so the adaptive term is not confounded with a different global adjustment
  strength.
- **Approved caption:** *Per-class accuracy difference between Original LTLC and same-τ
  POST-HOC STANDARD LA, plotted against **EXPERIMENT-B POST-GUARD** training-frequency
  rarity. **The two panels use different y-axis ranges (Pingan approximately ±0.02; Qingyun
  approximately ±0.003, roughly an order of magnitude smaller); vertical magnitudes and
  visual slopes must therefore not be compared directly across datasets.** On Qingyun the
  isolated α contribution reaches at most ≈0.3 percentage points, effectively nil.*
- **Superseded:** No
- **Note:** Retained deliberately as supporting evidence, not silently retired. Not
  regenerated to force a shared y-axis: the QA pass did **not** find it scientifically
  misleading, only requiring disclosure.

---

## EXCLUDED / SUPERSEDED

### X1 · Original calibration scatter (Notebook 06B v2)
- **Canonical filename:** `Fig_N5_Calibration_NLL_vs_TailECE_v2.png`
- **Canonical path:** `LTLC/results/notebook06b_experiment_b_thesis_ready_v2/Fig_N5_Calibration_NLL_vs_TailECE_v2.png`
- **Grade:** **C — redesign needed**
- **Status:** **EXCLUDED / SUPERSEDED — DO NOT PLACE IN THE BLACK BOOK**
- **Defect:** the `LA_Global_TS` and `Global_TS` point labels collide illegibly in both
  clusters; visually confirmed during the 2026-08-27 QA pass.
- **Exact replacement:** **`Fig_Calibration_Tradeoff_Redesigned.png`** (entry **F5** above),
  canonical path
  `LTLC/results/final_thesis_figures_v1/Fig_Calibration_Tradeoff_Redesigned.png`.
  Same underlying values; the redesign replaces point labels with a legend, separates the two
  occluding markers without moving any data point, and applies the POST-HOC STANDARD LA
  naming.
- **Retention:** the file is retained unchanged at its path as a historical artifact.

---

## Summary

| ID | Figure | Grade | Placement | Directory |
|---|---|:--:|---|---|
| F1 | Class-frequency long-tail | A | Main ch.3 | `final_thesis_figures_v1/` |
| F2 | Experiment A vs B leakage | A | Main ch.5 | `final_thesis_figures_v1/` |
| F3 | Spatial split map | B | Main ch.6 | `final_thesis_figures_v1/` |
| F4 | Per-seed ΔAA vs CE | A | Main ch.7 | `final_thesis_figures_v1/` |
| F5 | Calibration trade-off (redesigned) | A | Main ch.9 | `final_thesis_figures_v1/` |
| F6 | Rarity vs CE difficulty (N1) | A | Main ch.8 | `notebook06b_..._v2/` |
| F7 | LTLC parameter landscape (N3) | B | Main ch.8 | `notebook06b_..._v2/` |
| F8 | R1 β profile (N4) | A | Main ch.8 | `notebook06b_..._v2/` |
| F9 | Isolated α contribution (N2) | B | **Appendix** | `notebook06b_..._v2/` |
| X1 | Calibration scatter (N5) | C | **EXCLUDED** | `notebook06b_..._v2/` |

**9 approved figures · 1 excluded · 0 duplicates created · 1 canonical path each.**
