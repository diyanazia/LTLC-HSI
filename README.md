# LTLC — Leakage-Controlled Evaluation of Long-Tail Correction for Hyperspectral Image Classification

**Why Class Frequency Alone Is Not Enough**

CSE498R undergraduate research project · QUH hyperspectral benchmark · HybridSN backbone

---

## Abstract

Hyperspectral land-cover datasets are severely class-imbalanced, and a common remedy is *logit
adjustment*: shifting each class's score by its training log-prior. This study asks whether an
*additional rarity-adaptive term* — making the adjustment stronger for rarer classes — improves
class-balanced recognition once the evaluation protocol is corrected.

Correcting the protocol turned out to be the precondition for asking the question at all. A
conventional pixel-random split returned ≈99.99% Cross-Entropy validation accuracy, because the
classifier consumes spatial patches and patches around adjacent pixels overlap heavily. Under a
spatially disjoint split with a guard band that removes any training pixel within Chebyshev
distance `2·radius` of a validation pixel, the same model family scores 74–88%.

Under that stricter protocol, standard training-prior correction gives a suggestive
class-balanced gain on one scene (Balanced Softmax, +3.0 pp AA on Pingan) and a much smaller one
on the other (trained LA-loss, +0.6 pp on Qingyun). The proposed rarity-adaptive term, however,
**was not selected**: a revised, identifiable formulation chose a rarity coefficient of exactly
zero on both scenes, making it arithmetically identical to standard logit adjustment. A mechanism
analysis explains why — training-frequency rarity correlates with Cross-Entropy class error at
**ρ = +0.41 on one scene and ρ = −0.37 on the other**. Class frequency is not a consistent proxy
for class difficulty.

All differences are reported as **suggestive rather than confirmatory**: with three random seeds,
an exact sign-flip test cannot produce a p-value below 0.25.

---

## 1. Research motivation

Rare land-cover classes are systematically under-recognised by standard training, and Overall
Accuracy hides this because it is dominated by common classes. This project evaluates on
**Average Accuracy (AA)** — the mean of per-class accuracies — so tail-class failures are visible.

## 2. The original hypothesis

> Weighting the logit-adjustment strength by class rarity would yield additional class-balanced
> recognition gains over standard logit adjustment, **because rarer classes were expected to be
> systematically harder** and thus to benefit from stronger correction.

The proposal was named **LTLC** (Long-Tail Logit Correction).

## 3. Experiment A → Experiment B

**Experiment A** ran the full long-tail comparison on the conventional pixel-random split and
returned ≈99.99% Cross-Entropy validation accuracy. That is a methodological warning, not a
result.

The cause is **patch-neighbourhood overlap**. The split makes *centre pixels* disjoint, but the
model sees a `13×13` patch around each centre. If validation takes pixel `(100,100)` and training
takes `(100,101)`, their patches share about 92% of their pixels. The model can succeed by
recognising a neighbourhood it has already been trained on.

This is a **protocol design flaw**, widespread in the hyperspectral literature — not misconduct.
Experiment A is retained in the project archive as the motivation for Experiment B and is **never
used as evidence of method quality**.

**Experiment B** is the primary study.

## 4. Spatially disjoint validation

1. The scene is partitioned into spatial clusters; a frozen rule selects the validation subset.
   Assignment is by **region**, not by pixel.
2. Two patches of radius `r` overlap when their centres are within Chebyshev distance `2r`.
3. A **guard band** discards every training-side pixel within that distance of a validation pixel.
   Guard pixels are used for neither training nor validation.

| Scene | Patch radius | Guard threshold | Guard-excluded | Exp-B train | Exp-B validation |
|---|---:|---:|---:|---:|---:|
| Pingan | 6 | Chebyshev ≤ 12 | 14,144 | 65,710 | 34,245 |
| Qingyun | 5 | Chebyshev ≤ 10 | 3,732 | 63,179 | 28,581 |

Train ∩ validation = **0 pixels**, verified numerically.

**Side effect worth reporting:** the guard band removes spatially clustered rare-class pixels
disproportionately, so effective imbalance *rises* from **71.0× to 397.4×** (Pingan) and **28.5×
to 264.3×** (Qingyun). Experiment B is a harder long-tail problem than the nominal ratios suggest.

## 5. Datasets

The **QUH** UAV hyperspectral benchmark. **This repository does not redistribute the dataset** —
see §11.

| Scene | Cube (H×W×bands) | Classes | Patch | PCA | Official train-mask | Official IR | Role |
|---|---|---:|---:|---:|---:|---|
| **Pingan** | 1230 × 1000 × 176 | 10 | 13×13 | 15 | 114,099 | 71.0× | Primary Experiment-B scene |
| **Qingyun** | 880 × 1360 × 176 | 6 | 11×11 | 15 | 95,492 | 28.5× | Primary Experiment-B scene |
| Tangdaowan | 1740 × 860 × 176 | 16 | 9×9 | 20 | 35,372 | 189.7× | Notebooks 01–03 only; **excluded from Experiment B** |

**Tangdaowan exclusion is geometric, decided before any Experiment-B training and recorded in the
frozen protocol.** Its class 14 has a training pool of 62 pixels with a Chebyshev diameter of 7 and
row/column spans of 8, against a required centre separation above 8 under the frozen 9×9 patch
geometry — a strict all-class patch-disjoint split is impossible. **No Experiment-B result exists
for Tangdaowan**, so none is reported.

## 6. Preprocessing pipeline

```
Raw HSI (176 bands)
  → PCA (covariance_eigh; 15 components Pingan/Qingyun, 20 Tangdaowan; EVR ≥ 0.9998)
  → row-wise min-max normalization  (minmax_scale(axis=1))
  → zero padding by margin
  → patch extraction (margin = (patch_size − 1) // 2)
  → HybridSN input, shape (1, PCA, patch, patch)
```

Per-scene geometry: **Pingan 13/6 · Qingyun 11/5 · Tangdaowan 9/4**. The `margin` rule is enforced
in code, because an inconsistent margin silently decentres every patch without raising an error.

**Disclosed caveat — transductive preprocessing.** PCA was fitted on the full cube rather than on
training pixels alone. It is **unsupervised**: no label, and specifically no test label, was used
at any point, and one frozen cube is reused everywhere (`full_cube_pca_recomputed: false`) so no
split-dependent refitting occurs. This follows the convention in the hyperspectral literature and
keeps results comparable, but it is not strictly inductive and is stated here rather than omitted.

## 7. Backbone — HybridSN

```
conv3d_1 : 1  -> 8   kernel (7,3,3)
conv3d_2 : 8  -> 16  kernel (5,3,3)
conv3d_3 : 16 -> 32  kernel (3,3,3)
reshape  : spectral depth folded into Conv2D channels
conv2d   : -> 64     kernel 3
fc1 256 -> fc2 128 -> linear classifier
dropout 0.4 (x2)
```

Parameters: 519,546 (Pingan, 10 classes) · 256,886 (Qingyun, 6 classes).
Training: Adam, base LR 1e-3 with inverse-time decay `0.001/(1+1e-6·step)`, batch 256, 100 epochs,
no augmentation, no mixed precision, deterministic algorithms enabled. Checkpoints selected on
**best validation AA**.

**HybridSN is an existing published backbone and is not a contribution of this work.** It was held
fixed across every run so that differences in AA are attributable to the long-tail method rather
than to architecture.

## 8. Compared methods

| Method | Changes training or post-processing? | Tuned parameter |
|---|---|---|
| Cross-Entropy (CE) | training (reference) | — |
| Focal Loss | training | γ (selected γ=1, both scenes) |
| LDAM-DRW | training | C (0.5 Pingan, 0.25 Qingyun) |
| Balanced Softmax | training | none (counts are the parameter) |
| **TRAINED LA-LOSS** | **training** | τ (1.0 Pingan, 0.5 Qingyun) |
| **POST-HOC STANDARD LA** | **post-processing only** | τ (grid search) |
| Global Temperature Scaling | post-processing only | T |

### 8.1 TRAINED LA-LOSS vs POST-HOC STANDARD LA — a required distinction

These share a formula shape and nothing else.

|  | **TRAINED LA-LOSS** | **POST-HOC STANDARD LA** |
|---|---|---|
| When applied | during training, inside the loss | after training, to frozen logits |
| Produces new weights? | **Yes** — its own checkpoint | **No** — reuses the CE model |
| Compared against | the trained CE model | the same CE model's own logits |
| Reported in | run ledger; Tables 01, 02, 09 | Tables 03–06; paired-delta v3 |

Conflating them has already produced a documented error in this project's own audit trail (see
`reproducibility/PAIRED_DELTA_CORRECTION_NOTICE_v1.md`). **Never write "LA" unqualified.**

## 9. LTLC and R1

**Original LTLC** — applied post-hoc to frozen CE validation logits:

```
z_LTLC = z − τ · (1 + α · rarity) · log(π + ε)
```

with `τ ∈ {0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2}` and
`α ∈ {0, 0.25, 0.5, 0.75, 1, 1.5, 2}`. With **α = 0 this is exactly standard logit adjustment**.

**A flaw in that parameterisation:** α is *multiplied* by τ, so when τ = 0 the rarity term vanishes
entirely regardless of α — which actually occurred (Qingyun, seed 3407). τ and α are entangled, so
"how much rarity adaptation was selected" has no clean answer.

**Revision R1** makes the rarity strength additive and independent:

```
z_R1 = z − (τ + β · rarity) · log(π + ε)
```

R1 was frozen *before* being evaluated and compared against seed-42-frozen Standard-LA parameters.

Reference: `standard_LA : z − τ · log(π + ε)`.

## 10. Results

### 10.1 Experiment-B validation (TRAINED models, spatially disjoint)

AA mean ± SD over seeds 42 / 123 / 3407 — `results/tables/Thesis_Table_01_ExperimentB_Master_Results_v2.csv`

| Rank | Scene | Method | Config | **AA** | ΔAA vs CE |
|---:|---|---|---|---:|---:|
| **1** | Pingan | **Balanced Softmax** | training_counts | **0.7695 ± 0.0063** | **+0.0302** |
| 2 | Pingan | TRAINED LA-loss | τ=1 | 0.7617 ± 0.0136 | +0.0224 |
| 3 | Pingan | CE | — | 0.7393 ± 0.0223 | 0 |
| 4 | Pingan | Focal | γ=1 | 0.7391 ± 0.0127 | −0.0003 |
| 5 | Pingan | LDAM-DRW | C=0.5 | 0.7044 ± 0.0260 | −0.0350 |
| **1** | Qingyun | **TRAINED LA-loss** | τ=0.5 | **0.7595 ± 0.0076** | **+0.0057** |
| 2 | Qingyun | CE | — | 0.7538 ± 0.0089 | 0 |
| 3 | Qingyun | Focal | γ=1 | 0.7536 ± 0.0160 | −0.0002 |
| 4 | Qingyun | Balanced Softmax | training_counts | 0.7533 ± 0.0050 | −0.0005 |
| 5 | Qingyun | LDAM-DRW | C=0.25 | 0.7486 ± 0.0058 | −0.0052 |

Gains are clearer on Pingan and marginal on Qingyun; the winning method **differs between scenes**;
LDAM-DRW underperforms CE on both. All statements are **suggestive, not confirmatory**.

### 10.2 The main negative result

- Original LTLC selected a **non-zero α in only 2 of 6 runs**; in the other four it collapsed
  exactly onto POST-HOC STANDARD LA. The two non-zero cases gave **+0.0033** and **+0.0001** AA,
  both on a single seed.
- **R1 selected β = 0 on both datasets** (`exact_logit_equal: true`; all deltas 0.0), making it
  arithmetically identical to standard logit adjustment.
- The (τ, α) landscape shows a broad near-optimal plateau — **α is not identifiable from the data**.

**Under this protocol, additional frequency-only rarity weighting was not useful.**

### 10.3 Mechanism — why

`results/tables/Thesis_Table_06_Rarity_Mechanism_Correlations_v2.csv`

| Scene | Spearman ρ (rarity vs CE class error) |
|---|---:|
| Pingan | **+0.4061** |
| Qingyun | **−0.3714** |

**Opposite signs on two scenes of the same benchmark.** A correction driven purely by frequency
assumes a stable frequency→difficulty relationship; that relationship does not exist consistently.
Correlations are **descriptive only** — no p-values are claimed, because there are few classes
(10 and 6) and hyperspectral pixels are spatially dependent.

Intuition: a rare class can be spectrally distinctive and easy, while a common class can overlap
spectrally with a neighbour and be hard. **Rarity is not difficulty.**

### 10.4 Calibration

`results/tables/Thesis_Table_03_Calibration_Tradeoff_v2.csv`

| Scene | Method | NLL | Tail-ECE |
|---|---|---:|---:|
| Pingan | POST-HOC STANDARD LA (uncalibrated) | 3.7333 | **0.1505** |
| Pingan | Global Temp. Scaling | 0.6701 | 0.2334 |
| Pingan | LTLC (rarity-conditioned TS) | **0.6390** | **0.5936** |
| Qingyun | POST-HOC STANDARD LA (uncalibrated) | 4.7366 | 0.2069 |
| Qingyun | Global Temp. Scaling | 0.9809 | **0.1523** |
| Qingyun | LTLC (rarity-conditioned TS) | **0.9652** | **0.5196** |

Global temperature scaling improved NLL substantially. **It is not a recognition improvement:** a
positive scalar temperature is order-preserving, so `argmax` — and therefore OA, AA, Macro-F1 and
Kappa — is unchanged for every pixel.

The rarity-conditioned variant attained the **best NLL** and the **worst Tail-ECE** (2.5–3.4×
worse than global TS), and hit its allowed temperature bounds in 5 of 6 fits. A method optimised
for an aggregate probabilistic metric degraded the subgroup it was designed to serve.

### 10.5 Official test — scope and limitation

The official test partition was evaluated **once** for Experiment B, after every method,
hyperparameter and checkpoint decision had been frozen.

| Scene | Method | AA (mean ± SD) | OA (mean ± SD) | Test pixels |
|---|---|---|---|---:|
| Pingan | Balanced Softmax | 0.69617 ± 0.00390 | 0.83412 ± 0.02116 | 1,026,838 |
| Qingyun | TRAINED LA-loss τ=0.5 | 0.73738 ± 0.01448 | 0.73734 ± 0.01579 | 859,401 |

Official-test pixels intersect neither the Experiment-B training set, nor its validation set, nor
the guard band (0 pixels in every case).

**The claim this supports, and no more:**

> No official-test result influenced Experiment-B model selection, hyperparameter selection,
> checkpoint selection, or LTLC method development. All such decisions were frozen using the
> spatially disjoint validation protocol before the one-time confirmatory test evaluation.

**This is not a claim that the official test was never opened** — an earlier notebook legitimately
evaluated a Cross-Entropy baseline on it for published-benchmark reproduction. The full timeline,
including a disclosed governance inconsistency, is in
`protocol/FINAL_GOVERNANCE_AUDIT_v2.md`.

> **Limitation:** only the rank-1 method per scene was scored. **There is no Experiment-B
> Cross-Entropy result on the official test, so no test-set comparison against CE is possible and
> none is made.** The ΔAA-vs-CE comparison in §10.1 is validation-only.

---

## 11. Dataset acquisition — the data is NOT in this repository

This repository contains **no hyperspectral cubes, no ground-truth masks, and no split label
arrays**. Obtain the QUH benchmark from its original publisher and cite the original authors.

Expected local layout once obtained:

```
<your-data-root>/
    data_raw/
        Pingan/      QUH-Pingan.mat      QUH-Pingan_GT.mat      Pingan_train.mat      Pingan_test.mat
        Qingyun/     QUH-Qingyun.mat     QUH-Qingyun_GT.mat     Qingyun_train.mat     Qingyun_test.mat
        Tangdaowan/  QUH-Tangdaowan.mat  QUH-Tangdaowan_GT.mat  Tangdaowan_train.mat  Tangdaowan_test.mat
```

Reference values for verifying your copy are published in `preprocessing/` and
`dataset_metadata/` — cube shapes, per-class counts, class mappings, and the SHA-256 of the
derived PCA cubes.

> **Please cite the original QUH dataset authors** in any work using it. This repository claims no
> rights over the dataset and redistributes none of it.

## 12. Environment setup

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Exact pinned versions of both environments actually used — the analysis/plotting environment and
the CPU inference environment used for the one-time official-test evaluation — are recorded in
`reproducibility/FINAL_QA_ENVIRONMENT_v1.txt`.

## 13. Reproduction workflow

1. **Obtain the QUH dataset** (§11) and place it at your data root.
2. **Preprocessing** — run `src/02_QUH_Benchmark_Preprocessing_and_Patch_Cache.ipynb`. Verify the
   derived PCA cubes against the SHA-256 values in `preprocessing/canonical_patch_manifest.json`.
3. **Backbone** — `src/03_HybridSN_Baseline_Training_and_Benchmark_Reproduction.ipynb` defines
   HybridSN. Downstream code recovers the class from this notebook by AST parsing rather than
   re-typing it, so the architecture cannot drift between copies.
4. **Experiment B** — `src/06A_Spatially_Disjoint_Validation_Robustness_Study.ipynb` constructs the
   spatially disjoint split and runs the 36 training jobs. Split parameters and hashes are in
   `splits/`; regenerated splits can be verified against the published canonical hashes.
5. **Post-hoc analysis** — `src/06B_ExperimentB_Posthoc_LTLC_and_Calibration_Evaluation.ipynb`
   performs the LTLC / R1 recognition search and the calibration study over frozen CE validation
   logits.
6. **Statistics** — `src/stats_analysis.py` recomputes per-seed paired deltas from the run ledger
   in `experiments/`.
7. **Figures and tables** — `src/make_figures_finalqa_v1.py` and `src/build_clean_tables.py`.

Model checkpoints and large archives are **not** in this repository; see
`reproducibility/MASTER_ARCHIVE_PATH_MAP_v1.md` for what exists and where.

## 14. Repository structure

```
docs/               Full study explanation, claim boundaries, figure manifest, findings narrative
protocol/           Frozen protocols, rank-1 freeze, governance audit and disclosure text
dataset_metadata/   Class mappings, per-class counts, imbalance ratios (all three count concepts)
preprocessing/      PCA configuration, patch geometry, normalization, cube/split hashes
splits/             Split construction records and frozen manifests (metadata only — see splits/README.md)
src/                Notebooks and analysis scripts
experiments/        36-run ledger, closing audit, validation summaries
  official_test/    One-time official-test result, run log, technical verification
posthoc/            Frozen recognition grid/selections, calibration parameters, mechanism tables
results/figures/    The 9 approved figures
results/tables/     The 11 active terminology-finalized tables
reproducibility/    Environment manifest, archive hash records, final QA audit chain
```

## 15. Statistical reporting

Three random seeds were used. With n = 3:

- an exact sign-flip test has **2³ = 8** possible sign patterns, so the minimum attainable
  two-sided p-value is **0.25**;
- a bootstrap over three observations takes only **10 distinct mean values**, and its 95%
  percentile endpoints coincide exactly with the observed minimum and maximum.

Bootstrap intervals are therefore reported **descriptively**. **No result in this work is claimed
to be statistically significant.** The standing wording is *"suggestive rather than confirmatory."*

## 16. Limitations

1. Two primary Experiment-B scenes, one sensor family, one backbone, three seeds.
2. Tangdaowan — the highest-imbalance scene — is excluded on geometric grounds, narrowing scope.
3. Statistical power is insufficient for conventional inference (§15).
4. PCA is transductive (unsupervised, label-free) rather than strictly inductive.
5. **No novel recognition gain was obtained**; R1 collapsed to standard logit adjustment.
6. **No Experiment-B CE result on the official test**, so no test-set comparison against CE.
7. Method ranking is dataset-dependent.
8. Both validation splits are fully consumed by selection, so method development is closed on this
   data; any new method must be frozen before evaluation on an independent protocol.
9. No modern long-tail baselines (decoupled training, LADE, PaCo).
10. A governance inconsistency regarding official-test access is disclosed in
    `protocol/FINAL_GOVERNANCE_AUDIT_v2.md` rather than reconciled silently.

## 17. What this work does and does not claim

**Supported.** Spatially disjoint, guard-banded validation removes the patch-context overlap
present in the pixel-random protocol; guard-band exclusion raises effective imbalance; standard
training-prior correction gives suggestive gains on Pingan and marginal gains on Qingyun; LDAM-DRW
underperforms CE on both; the frequency-only rarity term gives no robust additional gain; R1
selected β = 0 on both scenes; rarity is not a consistent proxy for difficulty; global temperature
scaling improves NLL without changing predictions.

**Not claimed.** LTLC is not presented as a successful recognition method. No state-of-the-art
claim, no statistical significance, no robust generalization across all QUH scenes, no Tangdaowan
Experiment-B result, no official-test improvement over CE, no claim that the official test was
never opened, and no claim that calibration improved recognition.

The binding list is `docs/FINAL_CLAIM_BOUNDARIES_v1.md`.

## 18. Citation

See `CITATION.cff`. Please also cite the original QUH dataset authors and the original HybridSN
paper; neither is a contribution of this work.

## 19. License

**Repository licensing is pending confirmation — see `LICENSE_PENDING.md`.**

No licence has been granted yet. Until one is added, no permission to copy, modify, redistribute
or reuse this repository'''s contents should be inferred.

Third-party datasets, models and methods remain subject to their respective original licenses and
terms. This project claims no ownership of the QUH dataset (not redistributed here), the HybridSN
architecture, or any third-party long-tail method reimplemented for comparison. Please cite their
original authors.
