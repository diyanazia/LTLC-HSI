# FINAL FIGURE QA v1

**Date:** 2026-08-27 · **Output folder:** `LTLC/results/final_thesis_figures_v1/`
**Generator:** `LTLC/final_qa_2026-08-27/make_figures_finalqa_v1.py` (path-fixed, versioned
copy of the Day-1 script; original retained unchanged)

Only file paths, labels/captions and presentation were changed. **No scientific data was
altered.** Every hardcoded value in the generator was verified against primary sources before
regeneration (see §4).

Grades: **A** = thesis/publication ready · **B** = minor polish · **C** = redesign needed ·
**D** = unsafe · **F** = scientifically misleading. Main Black Book takes A/B only.

---

## 1. Scorecard

| # | Figure | Role | Grade | Placement |
|---|---|---|:--:|---|
| 1 | `Fig_ClassFrequency_LongTail_Distribution.png` | Long-tail class distribution, 3 scenes | **A** | Main — Data chapter |
| 2 | `Fig_ExperimentA_vs_B_Leakage_Comparison.png` | Leakage collapse ~100% → 74–88% | **A** | Main — Motivation |
| 3 | `Fig_Spatial_TrainVal_Split_Map.png` | Spatially disjoint split + guard band | **B** | Main — Method |
| 4 | `Fig_PerSeed_Delta_vs_CE.png` | Per-seed ΔAA vs CE (replaces forest plot) | **A** | Main — Results |
| 5 | `Fig_Calibration_Tradeoff_Redesigned.png` | NLL vs Tail-ECE (**supersedes Fig N5**) | **A** | Main — Calibration |
| 6 | `Fig_N1_Rarity_vs_CE_Difficulty_v2.png` | Rarity vs CE difficulty | **A** | Main — Mechanism |
| 7 | `Fig_N3_LTLC_Seed42_Parameter_Landscape_v2.png` | LTLC (τ, α) AA landscape | **B** | Main — Mechanism |
| 8 | `Fig_N4_R1_Beta_Profile_v2.png` | R1 β profile | **A** | Main — Mechanism |
| 9 | `Fig_N2_Rarity_vs_Adaptive_LTLC_Gain_v2.png` | Isolated α contribution | **B** | **Appendix** (per instruction) |
| 10 | `Fig_N5_Calibration_NLL_vs_TailECE_v2.png` | Original calibration scatter | **C** | **Retired** — superseded by #5; retained as history |
| 11 | Validation correctness map | — | — | **Not produced** (see §5) |

All figures: 200 dpi savefig, matplotlib 3.11.1, top/right spines removed, categorical
palette consistent across the set.

---

## 2. Per-figure findings

### 1. `Fig_ClassFrequency_LongTail_Distribution.png` — A
3 panels (Pingan/Qingyun/Tangdaowan), log-scale bars, Head/Medium/Tail colour coding, IR
annotated per scene. Legible tick labels, no overlap, colour-blind-distinguishable palette.
**Fixed this pass:** y-axis now reads "Official training-mask pixels (log scale)" and the
title names the count concept, removing the ambiguity flagged in
`TRAINING_COUNT_SEMANTICS_AUDIT_v1.md`.
*Caption must state:* counts are **OFFICIAL TRAINING-MASK COUNTS**; Tangdaowan is shown for
dataset context only and is excluded from Experiment B.

### 2. `Fig_ExperimentA_vs_B_Leakage_Comparison.png` — A
The single most persuasive figure in the project: CE validation accuracy collapsing from
~100% (pixel-random) to 88.2%/73.9% (Pingan OA/AA) and 74.3%/75.4% (Qingyun OA/AA). Values
annotated on bars; percent-formatted axis.
*Minor:* the legend sits over the lower-left plot area — readable, but could be moved outside
for print.
*Caption must state:* Experiment-A values are Notebook-03 CE validation
(`ce_checkpoint_manifest.csv`); the **split** changed, not the method.

### 3. `Fig_Spatial_TrainVal_Split_Map.png` — B
Real `.npz` split indices (not a schematic); blocks are visibly disjoint; guard band renders
as a thin grey seam between train and validation regions — which is exactly correct, but easy
to miss at print size.
*Polish needed:* the two panel titles sit at different heights because `aspect="equal"` gives
the panels different heights; the grey guard band deserves a callout or inset.
*Caption must state:* guard-excluded pixels are used for **neither** training nor validation.

### 4. `Fig_PerSeed_Delta_vs_CE.png` — A *(new this pass)*
Replaces the CI-led forest plot. Per-seed markers (circle/square/triangle for 42/123/3407),
black mean ± SD bar, and the bootstrap interval demoted to a faint grey band explicitly
labelled "descriptive only". Title carries "n=3 seeds: suggestive, not confirmatory".
This directly implements `STATISTICAL_ANALYSIS_VERIFICATION_v1.md`: the reader sees all three
observations rather than an interval that is merely their range.
*Caption must state:* **TRAINED method vs TRAINED CE**, Experiment-B validation AA.

### 5. `Fig_Calibration_Tradeoff_Redesigned.png` — A
**Supersedes Fig N5 and fixes its defect.** Uses a legend instead of per-point text labels, so
the overlap is eliminated by construction.
*Fixed this pass:* (a) Global-TS and LA+global-TS sat almost on top of each other — Global TS
is now drawn as a larger hollow ring so both remain visible **without moving any data point**;
(b) legend renamed to **POST-HOC STANDARD LA** per the naming rule; (c) title changed to
"Calibration trade-off (validation only; NOT a recognition result)", removing the earlier
"wins on NLL" phrasing that brushed against the claim boundary.

### 6. `Fig_N1_Rarity_vs_CE_Difficulty_v2.png` — A
Class-labelled scatter with Spearman ρ per scene. Carries the mechanism argument on its own:
**ρ = +0.406 (Pingan) vs −0.371 (Qingyun) — opposite signs**, which is precisely the evidence
that rarity is not a consistent proxy for difficulty.
*Caption must state:* rarity derives from **EXPERIMENT-B POST-GUARD** counts; ρ is descriptive
only — no p-values, few classes, spatially dependent pixels.

### 7. `Fig_N3_LTLC_Seed42_Parameter_Landscape_v2.png` — B
Viridis heatmaps over the (τ, α) grid; the broad yellow plateau at low α is exactly the
non-identifiability evidence.
*Issue:* the two panels use **independent colour scales** (Pingan ≈ 0.68–0.77, Qingyun ≈
0.63–0.76). Cross-panel visual comparison is therefore invalid.
*Required:* either state this explicitly in the caption or regenerate with a shared scale.
Seed 42 only — say so.

### 8. `Fig_N4_R1_Beta_Profile_v2.png` — A
Monotone decline in validation AA as β increases, on both scenes, with the maximum at β = 0.
Clean, unambiguous, directly supports "R1 selected β = 0 and collapses to POST-HOC STANDARD LA".
*Caption must state:* y-range spans only ≈ 0.750–0.771, so the visual slope exaggerates a
~2 pp effect; seed 42.

### 9. `Fig_N2_Rarity_vs_Adaptive_LTLC_Gain_v2.png` — B, **appendix**
Retained as supporting mechanism evidence per instruction, not silently retired.
*Issue — must be captioned:* the two panels have **very different y-scales** (Pingan ±0.02;
Qingyun ±0.003, roughly 10× smaller). A reader scanning across would wrongly infer comparable
effect sizes. In fact Qingyun's isolated α contribution is ≈ 0.3 pp at most — essentially nil,
which reinforces the null result.

### 10. `Fig_N5_Calibration_NLL_vs_TailECE_v2.png` — C, **retired**
Confirmed defect: the `LA_Global_TS` and `Global_TS` text labels collide illegibly in both
clusters (visually verified this pass). Superseded by figure #5. Retained unchanged as a
historical artifact; **do not place in the Black Book**.

---

## 3. Cross-figure consistency

| Check | Status |
|---|---|
| Method naming (`CE`, `Focal`, `LDAM-DRW`, `Balanced Softmax`, `LA-loss`) | consistent |
| POST-HOC STANDARD LA vs TRAINED LA-LOSS distinction | enforced in #4 and #5; **required in captions of #6, #7, #9** |
| Dataset naming (`Pingan`, `Qingyun`, `Tangdaowan`) | consistent |
| Rounding | 1 dp percentages in #2; 4 dp elsewhere — consistent |
| Values match source CSV/JSON | verified, §4 |
| Colour palette | one categorical palette across #1–#5; #6–#9 use the older 06B default — acceptable, but note the visual break |

---

## 4. Source verification of generator constants

| Constant block | Verified against | Result |
|---|---|---|
| Per-class frequencies (fig 1) | `audit/{scene}_frequency_groups.csv` → `official_train` | exact match |
| Experiment-A CE validation OA/AA (fig 2) | `audit/notebook03_hybridsn/ce_checkpoint_manifest.csv` | exact match, all 6 values |
| Experiment-B CE validation OA/AA (fig 2) | validation summary table | exact match |
| Calibration NLL / Tail-ECE (fig 5) | `Table_Calibration_Tradeoff_v2.csv` `nll_mean`/`tail_ece_mean` | exact match, all 8 points |
| Significance inputs (fig 4) | regenerated `significance_test_results_v1.json` from the 36-run ledger | exact match |
| Split maps (fig 3) | live `.npz` Experiment-B split indices | loaded directly |

---

## 5. Validation correctness map — not produced (justified)

A full-scene classification map would require new full-cube inference and is prohibited. The
permitted alternative — a validation-pixel-only correctness map — was evaluated and **dropped**:

- Frozen validation logits exist only for **CE** (`posthoc/.../validation_logits_v1/`, 6 files),
  not for the rank-1 Balanced Softmax / LA-loss models, so any such map would depict the CE
  baseline rather than the selected methods.
- Experiment-B validation covers 34,245 (Pingan) and 28,581 (Qingyun) scattered pixels — under
  3% of each scene. As shown by figure #3, these form sparse blocks on a mostly empty
  background, so a correctness map would be visually thin and easy to mistake for a full
  classification map.
- It would add no evidence not already carried by the per-class tables.

Per the instruction not to manufacture a qualitative map merely because HSI papers usually
have one, this figure is **deliberately omitted**. Figure #3 already provides the spatial
evidence that matters.

---

## 6. Required actions before writing

1. Add the mandated captions listed per figure above — especially the count-concept and
   POST-HOC/TRAINED distinctions.
2. Fig N3: state the independent colour scales, or regenerate with a shared scale.
3. Fig N2: state the differing y-axis scales in the caption.
4. Fig 3: optionally move panel titles to a common baseline and call out the guard band.
5. Do not place Fig N5 v2 in the Black Book.
