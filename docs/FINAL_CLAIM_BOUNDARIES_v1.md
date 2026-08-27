# FINAL CLAIM BOUNDARIES v1

**Date:** 2026-08-27 · Authoritative for all Black Book writing.
Derived from frozen artifacts and the 2026-08-27 QA pass. Supersedes nothing; consolidates
`FINAL_GOVERNANCE_AUDIT_v1.md`, `OFFICIAL_TEST_TECHNICAL_VERIFICATION_v1.md`,
`PAIRED_DELTA_VERIFICATION_AUDIT_v1.md`, `PAIRED_DELTA_CORRECTION_NOTICE_v1.md`,
`TRAINING_COUNT_SEMANTICS_AUDIT_v1.md`, `STATISTICAL_ANALYSIS_VERIFICATION_v1.md`.

---

## Naming rules (binding, all chapters)

| Use this | For this | Never write |
|---|---|---|
| **POST-HOC STANDARD LA** | `z − τ·log(π+ε)` applied to frozen CE validation logits | "Logit Adjustment" unqualified |
| **TRAINED LA-LOSS** | separately trained Experiment-B model using the LA loss | "LA" unqualified |
| **OFFICIAL TRAINING-MASK COUNT** | published QUH training-mask per-class count | bare "train_count" |
| **EXPERIMENT-B POST-GUARD TRAINING COUNT** | training pixels after guard-band exclusion | bare "train_count" |
| **NB01 PIXEL-RANDOM 70% TRAIN COUNT** | Experiment-A / Notebook-03 training count | bare "train_count" |

---

## YOU MAY SAFELY CLAIM

### Protocol and leakage
1. Spatially disjoint validation with guard-band exclusion removed the severe patch-context
   overlap present in Experiment A. Under the pixel-random split, CE validation accuracy is
   ≈ 99.99% (Pingan) and ≈ 99.98% (Qingyun); under the corrected split it falls to
   OA 88.2% / AA 73.9% (Pingan) and OA 74.3% / AA 75.4% (Qingyun).
2. Experiment-B split and training protocols were frozen **before** split creation, model
   construction, inference and training, with those properties recorded as explicit flags in
   content-hashed artifacts.
3. Guard-band exclusion **increases effective class imbalance substantially**: Pingan
   71.0× → **397.4×**, Qingyun 28.5× → **264.3×**. Experiment B is therefore a harder
   long-tail problem than the nominal dataset IR implies.
4. Tangdaowan was excluded from Experiment B because a strict all-class patch-disjoint split
   is geometrically infeasible for its class 14 under the frozen 9×9 patch geometry
   (Chebyshev diameter 7, training pool 62) — a pre-declared, frozen reason.

### Recognition (validation)
5. On Pingan validation, **TRAINED** Balanced Softmax (+3.0 pp AA) and **TRAINED** LA-loss
   (+2.2 pp AA) showed **suggestive** class-balanced recognition gains over CE, consistent in
   sign across all three seeds.
6. Qingyun gains were **much smaller**: TRAINED LA-loss +0.6 pp AA; Balanced Softmax and Focal
   were indistinguishable from CE (sign changes across seeds).
7. LDAM-DRW **underperformed** CE on both scenes (Pingan −3.5 pp, Qingyun −0.5 pp), consistent
   in sign across seeds.
8. Rank-1 per scene, selected on validation alone: Pingan **Balanced Softmax**
   (training_counts); Qingyun **TRAINED LA-loss τ = 0.5**.

### The LTLC null result
9. The frequency-only rarity-adaptive LTLC component did **not** produce a robust additional
   recognition gain.
10. Original LTLC selected a non-zero α in only **2 of 6** runs; the other four collapsed
    exactly to POST-HOC STANDARD LA.
11. **R1 selected β = 0 on both datasets**, so R1 is exactly equal to the frozen POST-HOC
    STANDARD LA (`exact_logit_equal: true`, ΔAA = ΔOA = ΔMacro-F1 = 0.0 for all six runs).
12. Rarity was **not a consistent proxy** for CE difficulty: Spearman ρ = **+0.406** (Pingan)
    versus **−0.371** (Qingyun) — opposite signs across scenes. Descriptive only.
13. LTLC's near-optimal region is wide and its selected parameters vary by seed, indicating
    parameter non-identifiability rather than a precise rarity-dependent correction.

### Calibration
14. Global temperature scaling **substantially improved NLL** on validation (e.g. Pingan
    3.733 → 0.670).
15. Calibration **did not imply recognition improvement** — a positive scalar temperature is
    order-preserving and leaves hard predictions unchanged.
16. LTLC's rarity-conditioned scaling attained the lowest NLL but **markedly worse tail-class
    ECE** (Pingan 0.594 vs 0.233 for global TS; Qingyun 0.520 vs 0.152).
17. LTLC Full hit its allowed temperature bounds in **5 of 6** fits (both `a` and `b`),
    evidence that the fitted parameters are not stable or generalizable.

### Official test
18. Official-test results were obtained **only after** all model, configuration and checkpoint
    decisions were frozen — six days after, and with no subsequent iteration.
19. Official-test performance of the frozen rank-1 configurations: Pingan Balanced Softmax
    AA 0.6962 ± 0.0039, OA 0.8341 ± 0.0212; Qingyun LA-loss τ=0.5 AA 0.7374 ± 0.0145,
    OA 0.7373 ± 0.0158.
20. Official-test pixels intersect **neither** the Experiment-B training set **nor** its
    validation set (0 pixels, both scenes).
21. Both scenes score **below** their validation AA on official test (Pingan −7.3 pp,
    Qingyun −2.2 pp).

### Statistics
22. All reported recognition differences are **suggestive, not confirmatory** — only three
    seeds were evaluated.
23. With n = 3, the exact sign-flip test has a hard minimum two-sided p of 0.25; bootstrap
    intervals over three observations take only ten distinct mean values and their 95%
    endpoints coincide exactly with the observed min/max.

---

## DO NOT CLAIM

1. ❌ **LTLC is a successful improved recognition method.** (`may_claim_successful_final_ltlc_recognition_method: false`)
2. ❌ **LTLC beats all baselines** — or any baseline — on recognition.
3. ❌ **State-of-the-art performance.** No SOTA comparison was run.
4. ❌ **Statistical significance.** No result meets a conventional threshold; the tests cannot
   reach one at n = 3. Do not convert "CI excludes zero" into significance.
5. ❌ **Robust generalization across all QUH datasets.** Only two of three scenes were studied.
6. ❌ **Any Tangdaowan Experiment-B performance.** Tangdaowan was never trained under
   Experiment B.
7. ❌ **Test-set improvement over CE.** No Experiment-B CE official-test result exists. Do not
   substitute Notebook 03's CE official-test numbers — those models trained on the leaky
   pixel-random split, so the comparison would confound the split fix with the method change.
8. ❌ **The official test was never opened.** Notebook 03 opened it by design in
   2026-08-12, and a one-time Experiment-B confirmatory run opened it on 2026-08-26.
9. ❌ **The official test remained sealed throughout**, or that the confirmatory run was
   protocol-authorised. Two frozen artifacts instructed the opposite; the run was authorised
   by the project owner. Disclose, do not paraphrase away.
10. ❌ **Calibration improved recognition.**
11. ❌ **Uniform tail-class calibration improvement.** (`tail_ece_uniformly_improved: false`)
12. ❌ **R1 is a distinct method from Standard LA.** With β = 0 it is exactly identical.
13. ❌ **The Qingyun seed-3407 zero paired delta is missing/stale data.** It is an exact
    identity (τ = 0). See `PAIRED_DELTA_CORRECTION_NOTICE_v1.md`.
14. ❌ **Any merged or unlabelled training-count / rarity / IR figure.** Always name the
    concept.
15. ❌ **That Experiment-B post-guard training counts are a subset of the 70% split.** They are
    a different spatial partition; some Qingyun classes have slightly more post-guard pixels.
16. ❌ **Experiment-A numbers as evidence of method quality.** Experiment A is retained solely
    as the leaky precursor that motivates Experiment B.

---

## Standing prohibitions (unchanged)

- Method development on the current validation splits is **closed** — both splits are fully
  consumed.
- No new training, no new hyperparameter tuning, no new method.
- The official test may **not** be rerun; the result file must not be deleted.
- Experiment-B CE must **not** be scored on official test without explicit new authorisation.
- All future method ideas belong in **Future Work** only, frozen before any evaluation on an
  independent protocol.
