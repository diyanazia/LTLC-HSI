# LTLC THESIS — COMPLETE UNDERSTANDING GUIDE FOR SUPERVISOR AND GROUPMATES

**Date:** 2026-08-27 · **Source:** `CSE498/LTLC_BLACKBOOK_FINAL/` (frozen working copy)
**Status:** understanding & explanation only — no research file was modified, no model trained,
no inference run, no official-test access.

Every number in this document is taken from the frozen workspace. Where a figure or table is
cited, the path is given so you can check it yourself.

---

## SOURCE CONFLICT IDENTIFIED (not silently reconciled)

`12_black_book/BLACK_BOOK_WRITING_HANDOFF_v1.md` §15 and §23 instruct citing
`Thesis_Table_01_..._v1.csv`, `_03_..._v1`, `_05_..._v1`, `_06_..._v1`. Its own **Addendum A
§A.3** — added later the same day — supersedes those four with the `_v2` versions.

**Authoritative resolution:** Addendum A wins; it is later and explicitly marked as
superseding. The v2 files differ in *wording only* (numerical invariance was verified
field-by-field in `10_final_qa/BLACK_BOOK_TERMINOLOGY_FINALIZATION_v1.md` §4). The active
tables copied into `09_results/tables/` are already the v2 set. **No numbers are in dispute.**

---

# PART 1 — WHAT YOUR THESIS ACTUALLY IS

## ORIGINAL THESIS IDEA

**1. The original research idea.** Hyperspectral land-cover datasets are severely
class-imbalanced. A standard fix is *logit adjustment* — at prediction time, shift each class's
score by its training frequency so rare classes are not systematically suppressed. Your idea
was that a *single global* adjustment strength treats all classes alike, and that rarer classes
might deserve a *stronger* correction. You called that idea **LTLC** (Long-Tail Logit
Correction).

**2. The original hypothesis.** From `BLACK_BOOK_WRITING_HANDOFF_v1.md` §4:

> Weighting the logit-adjustment strength by class rarity would yield additional
> class-balanced recognition gains over standard logit adjustment, **because rarer classes
> were expected to be systematically harder** and thus to benefit from stronger correction.

**3. What you hoped LTLC would achieve.** A measurable improvement in **Average Accuracy (AA)**
and tail-class accuracy over standard logit adjustment, holding the backbone and everything
else fixed — i.e. a small, clean, defensible methodological contribution.

**4. What changed during the research.** Three things, in order:

- **Experiment A's validation was overlap-prone.** Its pixel-random split produced ≈99.99%
  Cross-Entropy validation accuracy — a number no honest hyperspectral classifier reaches. That
  is a *methodological warning sign*, not a good result.
- **You rebuilt the evaluation** as Experiment B: spatially disjoint train/validation with a
  guard band, so a validation patch can never overlap a training patch.
- **Under that stricter protocol, the rarity term stopped being selected.** Original LTLC chose
  a non-zero α in only 2 of 6 runs; the cleaner revision **R1 chose β = 0 on both scenes**,
  making it *exactly identical* to standard logit adjustment.

**5. The final research question.** From `BLACK_BOOK_WRITING_HANDOFF_v1.md` §2:

> Does frequency-based long-tail correction — and specifically an additional rarity-adaptive
> term beyond standard logit adjustment — improve class-balanced recognition in hyperspectral
> image classification when validation is constructed to eliminate patch-neighbourhood overlap?

with five sub-questions (RQ1–RQ5 in §3): how much does overlap-prone validation overstate
performance; do standard long-tail objectives help; does the extra rarity term help; **is rarity
a reliable proxy for difficulty**; and does calibration constitute a recognition improvement.

## FINAL THESIS STORY

**6. What the thesis contributes.**

> Under leakage-controlled, spatially disjoint validation on QUH-Pingan and QUH-Qingyun,
> standard training-prior correction gives a suggestive class-balanced gain on Pingan and a much
> smaller one on Qingyun — but an **additional frequency-only rarity term gives no robust
> further gain**, and the mechanism analysis shows *why*: **class frequency is not a consistent
> proxy for class difficulty.**

Plus a second, arguably more useful contribution: a quantified demonstration that conventional
hyperspectral validation can be catastrophically optimistic (≈99.99% → 74–88% for the same
model family once patch overlap is removed).

**7. What the thesis does NOT contribute.** It does **not** present a working improved
recognition method. LTLC did not survive its own test. It does not claim state-of-the-art, does
not claim statistical significance, does not claim generalization beyond two scenes and one
backbone, and does not claim a test-set improvement over Cross-Entropy.

**A thesis is allowed to evolve.** An unsupported hypothesis, honestly established under a
protocol frozen *before* the results were seen, is a legitimate scientific outcome. What makes
it publishable-grade work is not that the method won — it is that the evaluation was designed
so the answer could have gone either way, and the negative answer is explained mechanistically
rather than merely reported.

---

# PART 2 — THE PROBLEM FROM ZERO

*(For a CSE student who has never seen hyperspectral imaging.)*

**A normal RGB image** stores three numbers per pixel: red, green, blue. A 1000×1000 photo is a
1000×1000×3 array.

**A hyperspectral image (HSI)** stores *hundreds* of numbers per pixel — one per narrow
wavelength band, often spanning beyond visible light. Your Pingan scene is
**1230 × 1000 × 176**: 176 bands per pixel. Think of each pixel not as a colour but as a *curve*
of reflectance across wavelengths.

**Spectral information** = that curve. Different materials reflect light differently, so the
curve is close to a chemical fingerprint. **Spatial information** = where the pixel sits and what
surrounds it. Roof pixels cluster into roof-shaped regions; roads are long and thin.

**Hyperspectral image classification** = assign each pixel a **land-cover class** (a physical
surface category: building roof, road, tree, water, bare soil, …). Your Pingan scene has 10
evaluated classes, Qingyun 6.

**Class imbalance** means classes appear in wildly different amounts. **A long-tail
distribution** is the extreme case: a few classes dominate and many are rare. Sorted by
frequency, the curve has a tall "head" and a long thin "tail".

Your project groups classes into **Head / Medium / Tail** (defined per scene in
`02_dataset_metadata/{scene}_frequency_groups.csv`). Concretely on Pingan, class 2 has **57,811**
official training pixels while class 9 has **814** — a ratio of **71×**.

**Why minority classes are hard.** The model sees them rarely, so gradient updates are dominated
by head classes; predicting a head class is usually "safe"; and rare classes are often
spectrally close to a common neighbour. **Why they matter:** the rare classes are frequently the
ones you care about — a small contaminated area, a rare crop, a narrow structure. A model that
ignores them is useless for those tasks.

**Why Overall Accuracy (OA) alone misleads.** OA = fraction of *all pixels* correct. If one
class is 50% of pixels, a model that only ever predicts that class already scores 50% while
being worthless. **Average Accuracy (AA)** = mean of *per-class* accuracies — every class counts
equally, so tail failures are visible. **Macro-F1** averages per-class F1 (precision/recall
balance), also class-equal. **Kappa** corrects agreement for chance.

**Connection to your research.** Your thesis is about the *AA* column. Every method you compare
exists to raise class-balanced accuracy, your checkpoints were selected on **best validation
AA**, and your headline results are AA. That is why your Pingan Experiment-B numbers look odd at
first glance — OA 0.8821 but AA 0.7393. The gap *is* the long-tail problem, quantified.

---

# PART 3 — THE DATASET

**QUH** is a UAV-borne hyperspectral benchmark with three scenes. All numbers below are from
`09_results/tables/Thesis_Table_07_Dataset_Overview_v2.csv` and
`02_dataset_metadata/notebook01_protocol_metadata.json`.

| Scene | Cube (H×W×bands) | Evaluated classes | Patch | PCA | Official train-mask total | Official IR | Role |
|---|---|---:|---:|---:|---:|---:|---|
| **Pingan** | 1230 × 1000 × 176 | 10 | **13×13** | 15 | 114,099 | **71.0×** | **Primary Experiment-B scene** |
| **Qingyun** | 880 × 1360 × 176 | 6 | **11×11** | 15 | 95,492 | **28.5×** | **Primary Experiment-B scene** |
| Tangdaowan | 1740 × 860 × 176 | 16 | 9×9 | 20 | 35,372 | 189.7× | Notebooks 01–03 only; **excluded from Experiment B** |

**Official train/test masks.** QUH ships fixed masks. Notebook 01 froze the protocol: split seed
**2026**, validation fraction **0.3**, model seeds **42 / 123 / 3407**. The official test
partition is large — **1,026,838** pixels for Pingan and **859,401** for Qingyun.

**Why Pingan and Qingyun are the primary scenes.** They are the two where a strict all-class
patch-disjoint spatial split is **geometrically feasible**. That is the whole reason.

**Why Tangdaowan was excluded — and it is NOT about poor results.** From the frozen
`01_protocol/experiment_b_spatial_validation_protocol_v1_frozen.json` (`cell3_geometric_feasibility`),
recorded **before any Experiment-B training ran**:

- Pingan: `strict_all_class_patch_disjoint_feasible: true`, `impossible_classes: []`
- Qingyun: `strict_all_class_patch_disjoint_feasible: true`, `impossible_classes: []`
- Tangdaowan: `impossible_classes: [14]` — class 14 has a **training pool of 62 pixels**, a
  Chebyshev diameter of **7**, row and column spans of **8**, against a strict required centre
  separation of **> 8** under the frozen 9×9 patch geometry.

In plain words: class 14's pixels are so few and so tightly clustered that you *cannot* place any
training and validation pixel of that class far enough apart to stop their 9×9 patches touching.
The split is impossible by geometry, not undesirable by outcome. **Tangdaowan was never trained
under Experiment B, so no Experiment-B Tangdaowan result exists to be good or bad.** Say it that
way.

---

# PART 4 — PREPROCESSING

Pipeline: **Raw HSI → PCA → row-wise min-max normalization → zero padding → patch extraction →
HybridSN**. Configuration from `03_preprocessing/canonical_patch_manifest.json` and
`notebook02_preprocessing_summary.csv`.

**1. Raw HSI.** 176 bands per pixel. Adjacent bands are heavily correlated and noisy.

**2. PCA (Principal Component Analysis).** Projects the 176 bands onto a small number of
uncorrelated components ordered by variance explained.
*Why:* removes redundancy, cuts memory and compute, reduces noise, and shrinks the 3-D
convolution's spectral depth to something trainable.
*Config:* solver `covariance_eigh`; **15 components for Pingan and Qingyun**, **20 for
Tangdaowan**; explained variance retained **≥ 0.9998** on all three.
*Why PCA15 vs PCA20:* Tangdaowan has 16 classes versus 10 and 6, so more spectral directions
were retained to preserve separability. The choice is frozen and pre-declared, not tuned on
results.
*Caveat:* see the transductive note below.

**3. Row-wise min-max normalization.** `minmax_scale(axis=1)` — each pixel's retained-PCA vector
is scaled to a common range.
*Why:* puts every pixel on the same numeric footing so no component dominates the first
convolution; stabilises optimisation.
*Caveat:* it normalises *within* a pixel, so absolute magnitude information across pixels is
discarded — a deliberate trade.

**4. Zero padding.** The cube is padded with zeros by the **margin/radius** so a patch can be
extracted even for a pixel on the image border.
*Config:* Pingan margin **6**, Qingyun **5**, Tangdaowan **4**.
*Caveat:* border patches contain artificial zeros. Unavoidable; affects a thin frame only.

**5. Patch extraction.** For each labelled centre pixel, cut a `patch × patch × PCA` cube around
it. **Pingan 13×13×15, Qingyun 11×11×15, Tangdaowan 9×9×20.**
*Why:* the classifier must see the pixel's neighbourhood, because spatial context is a large
part of what distinguishes land-cover classes.
*Critical rule:* `margin = (patch_size − 1) // 2`. Pingan 6, Qingyun 5, Tangdaowan 4. Getting
this wrong does **not** raise an error — it silently decentres every patch.
*Caveat and this is the key one:* **the patch is exactly the mechanism that made Experiment A's
validation overlap-prone.** See Part 8.

**6. HybridSN input.** Each patch is transposed to channels-first and given a singleton channel
dimension: shape `(1, PCA, patch, patch)`.

### The full-cube PCA caveat — say this out loud in the viva

PCA was fitted on the **entire cube**, not on training pixels only. That makes the preprocessing
**transductive**: unlabelled test *pixels* influenced the projection basis.

**Why it is defensible:** PCA is **unsupervised**. No label — and specifically **no test label** —
was used at any point. The frozen record states `full_cube_pca_recomputed: false`, i.e. one
frozen cube is reused everywhere with no per-split refitting, so no split-dependent leakage of
label information exists. It is also the standard convention in the HSI literature, which keeps
your numbers comparable to published work.

**Why you must still disclose it:** a strict inductive reading would fit PCA on training pixels
alone. State the choice, state that it is unsupervised and label-free, and move on. Do not hide
it and do not over-apologise for it.

---

# PART 5 — HYBRIDSN

**What it is.** A spectral-spatial CNN for hyperspectral classification that uses **3-D
convolutions first, then a 2-D convolution**. Architecture recovered verbatim from Notebook 03
(`05_code/03_HybridSN_Baseline_Training_and_Benchmark_Reproduction.ipynb`):

```
conv3d_1 : 1  -> 8   kernel (7,3,3)
conv3d_2 : 8  -> 16  kernel (5,3,3)
conv3d_3 : 16 -> 32  kernel (3,3,3)
reshape  : spectral-depth folded into Conv2D channels
conv2d   : -> 64     kernel 3
fc1 256 -> fc2 128 -> linear classifier (no internal softmax)
dropout 0.4 (x2)
```

Parameters: **519,546** on Pingan (10 classes), **256,886** on Qingyun (6 classes).
Training: Adam, base LR 1e-3 with inverse-time decay `0.001/(1+1e-6·step)`, batch 256,
**100 epochs**, no augmentation, no mixed precision, deterministic algorithms enabled.

**3-D convolutions** slide a kernel across *height, width and wavelength together*, so early
filters learn joint spectral-spatial patterns — "this material, in this spatial arrangement".
**The transition to 2-D**: after three 3-D layers, the spectral dimension is folded into the
channel dimension and a cheaper 2-D convolution refines purely spatial structure. That hybrid is
the point: full 3-D throughout is expensive; 2-D alone discards spectral structure.

**Why HybridSN was selected:** it is an established, widely reproduced HSI baseline, so Notebook
03 could reproduce a published benchmark and anchor the pipeline against known behaviour.

**Why the backbone was frozen.** Every long-tail method is a change to the *loss* or to
*post-processing*. If the backbone had also changed between runs, a difference in AA could not be
attributed to the long-tail method — architecture and method would be confounded. Holding
HybridSN fixed is what makes the comparison a comparison.

> **HybridSN is not your contribution.** It is a borrowed, unmodified, published backbone. Your
> contribution is the evaluation protocol and the long-tail analysis built on top of it. Say this
> before your supervisor asks.

---

# PART 6 — THE BASELINE METHODS

| # | Method | Changes training or post-processing? |
|---|---|---|
| 1 | Cross-Entropy (CE) | training (reference point) |
| 2 | Focal Loss | training |
| 3 | LDAM-DRW | training |
| 4 | Balanced Softmax | training |
| 5 | **TRAINED LA-LOSS** | **training** |
| 6 | **POST-HOC STANDARD LA** | **post-processing only** |
| 7 | Global Temperature Scaling | post-processing only |

**1. Cross-Entropy.** The standard classification loss. Every pixel contributes equally, so head
classes dominate the gradient. *Included as the reference against which every other method is
measured.*

**2. Focal Loss.** Down-weights examples the model already classifies confidently, concentrating
learning on hard examples. Parameter **γ**; γ=1 selected on both scenes. *Solves: easy head
examples drowning out hard ones.*

**3. LDAM-DRW.** Two parts. **LDAM** enforces a larger decision margin for rarer classes
(margin scaled roughly as an inverse power of class count). **DRW** (Deferred Re-Weighting)
trains normally first, then switches on class re-weighting late in training. Parameter **C**;
C=0.5 on Pingan, C=0.25 on Qingyun. *Solves: rare classes getting thin, fragile decision
boundaries.*

**4. Balanced Softmax.** Adds `log(training class counts)` inside the softmax during training, so
the loss is computed as if the classes were balanced. No tuning grid — the counts *are* the
parameter. *Solves: prior bias baked in during training.*

**5. TRAINED LA-LOSS.** Logit adjustment applied **inside the loss during training**: the model's
weights are learned with the prior-correction term present. Parameter **τ**; **τ=1.0 on Pingan,
τ=0.5 on Qingyun**. *This is a separately trained model with its own weights and its own
checkpoint.*

**6. POST-HOC STANDARD LA.** The **same mathematical form**, but applied **after training, to the
frozen logits of an already-trained CE model**. No retraining, no new weights. Parameter τ chosen
on validation. Formula (frozen): `z − τ·log(π+ε)`.

**7. Global Temperature Scaling.** Divides all logits by a single scalar T fitted on validation.
Purely a confidence rescaling — see Part 16.

## THE DISTINCTION YOU MUST NEVER BLUR

|  | **TRAINED LA-LOSS** | **POST-HOC STANDARD LA** |
|---|---|---|
| When applied | during training, inside the loss | after training, to frozen logits |
| Produces new weights? | **Yes** — its own checkpoint | **No** — reuses the CE model |
| What it is compared against | the **trained CE model** | the **same CE model's own logits** |
| Where its numbers live | run ledger; Tables 01, 02, 09 | Tables 03, 04, 05, 06; paired-delta v3 |
| Cost | a full training run | milliseconds |

**They are different experimental objects.** They share the word "LA" and the same formula shape,
and nothing else.

**Why this matters concretely — it already caused a real error.** An earlier document claimed a
value in the post-hoc paired-delta table was "stale" and proposed replacing it with `+0.004020`
taken from the *trained* LA-loss ledger. Recomputation proved the post-hoc table **correct** and
the proposed "fix" wrong: it would have injected a trained-model number into a post-hoc table.
The full account is in `10_final_qa/PAIRED_DELTA_CORRECTION_NOTICE_v1.md`. If a professional
audit trail can trip over this, so can a viva answer. **Always say which one you mean.**

---

# PART 7 — YOUR PROPOSED LTLC

## In words first

Standard logit adjustment says: *subtract a multiple of each class's log-prior from its score, so
common classes get penalised and rare classes get helped — using the same strength τ for every
class.*

Your LTLC says: *do that, but make the strength larger for rarer classes.* Each class gets a
**rarity score** between 0 (most common) and 1 (rarest), and the adjustment strength becomes
`τ · (1 + α · rarity)`. With α = 0 every class gets the same τ. With α > 0 the rarest class gets
up to `τ·(1+α)` — a stronger push.

## The ingredients

- **n_k** — the number of training pixels of class *k*. **Use the EXPERIMENT-B POST-GUARD count**,
  not the official mask count (see Part 9).
- **π_k** — the class prior, `n_k / Σn`. The empirical probability of class *k* in training.
- **r_k** — the rarity score, a normalised transform of frequency mapping most-common → 0 and
  rarest → 1 (per-class values in `09_results/tables/Thesis_Table_04_..._v2.csv`, column
  `rarity_from_expB_post_guard_count`).
- **τ** — global adjustment strength. Grid `{0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2}`.
- **α** — rarity-adaptive coefficient. Grid `{0, 0.25, 0.5, 0.75, 1, 1.5, 2}`.

## The formulas (frozen, `07_posthoc/..._Posthoc_Recognition_Freeze_v1.json`)

```
standard_LA   :  z − τ · log(π + ε)
original_LTLC :  z − τ · (1 + α · rarity) · log(π + ε)
```

Applied **post-hoc to frozen CE validation logits**. Prediction rule: `argmax` of adjusted logits.

**Why the extra term was introduced.** The hypothesis: rarer classes are systematically harder,
so a one-size-fits-all τ under-corrects the tail. α buys a rarity-proportional boost.

**The collapse property — memorise this.** If **α = 0**, then `(1 + 0·rarity) = 1` and the
formula becomes exactly `z − τ·log(π+ε)`. **LTLC with α = 0 *is* standard logit adjustment,
identically.** This matters enormously in Part 12: when the search selects α = 0, LTLC has not
"performed similarly" to the baseline — it *has become* the baseline.

---

# PART 8 — EXPERIMENT A

**Why it was created.** Notebook 04 was the first full long-tail comparison: 5 methods × 3 scenes
× 3 seeds = 45 runs, using the conventional pixel-random split (the 70/30 split from the fixed
seed-2026 protocol).

**What happened.** Cross-Entropy validation accuracy came out at roughly **99.99%**. From
`audit/notebook03_hybridsn/ce_checkpoint_manifest.csv` (Experiment-A-era split): Pingan
val_OA 0.99991 / val_AA 0.99998; Qingyun val_OA 0.99976 / val_AA 0.99869.

**Why that is a warning, not a triumph.** Hyperspectral land-cover classification does not reach
99.99%. When a number is too good, the first hypothesis must be that the evaluation is measuring
something other than generalization.

## The cause: disjoint centres, overlapping patches

Here is the whole issue in one picture. Suppose validation takes pixel **(100, 100)** and
training takes pixel **(100, 101)** — different pixels, correctly disjoint as *centre pixels*.

But the model does not see single pixels. It sees **13×13 patches**:

- training patch covers rows 94–106, columns 95–107
- validation patch covers rows 94–106, columns 94–106

Those two patches share **12 of 13 columns** — around **92% of the same pixels**. The model was
trained on almost exactly the image content it is now being "tested" on. It can succeed by
recognising the neighbourhood rather than by generalising.

Random pixel splitting guarantees this happens constantly, because neighbouring pixels land on
opposite sides of the split by chance. This is **spatial-context overlap** — also called
**patch-neighbourhood overlap** or **overlap-prone validation**.

**Terminology discipline.** The frozen sources describe this as *patch-neighbourhood overlap* and
*leakage-controlled* / *overlap-prone* validation. It is a **protocol design flaw**, not
misconduct, not fabrication, not anything malicious. It is an extremely common oversight in the
HSI literature — which is exactly what makes documenting it worthwhile. Never call it cheating.

**Why Experiment A was frozen, not deleted.** Three reasons: (1) it is the *evidence* that
motivates Experiment B — without the ≈99.99% number, the reader has no reason to care about the
guard band; (2) deleting inconvenient prior results is itself a research-integrity problem;
(3) `FINAL_CLAIM_BOUNDARIES_v1.md` classifies Experiment-A artifacts as never-deletable audit
history. It is retained **solely as methodological motivation** and never as evidence of method
quality.

---

# PART 9 — EXPERIMENT B

**Why it exists.** To answer the original research question under an evaluation where a
validation patch *cannot* overlap a training patch.

**How it works.**

1. **Spatial clustering.** The scene is partitioned into spatial clusters; a frozen rule selects
   which cluster subset becomes validation. Assignment is by *region*, not by individual pixel.
2. **Patch radius.** Pingan **6**, Qingyun **5** — i.e. `(patch−1)//2`.
3. **Required centre separation.** Two patches of radius *r* overlap if their centres are within
   Chebyshev distance `2r`. The frozen thresholds are exactly that:
   **Pingan `guard_threshold_chebyshev_leq: 12`** (= 2×6), **Qingyun `10`** (= 2×5).
4. **Guard-band exclusion.** Any training-side pixel within that distance of a validation pixel
   is **thrown away entirely** — used for neither training nor validation.

**Result: zero train/validation patch-footprint overlap by construction**, verified numerically
(train ∩ val = 0 pixels).

**Exact sizes** (`04_splits/experiment_b_split_construction_attempt_v1.json`,
`02_dataset_metadata/experiment_b_training_class_statistics_v1_frozen.json`):

| Scene | Patch radius | Guard threshold | Guard-excluded | Exp-B train | Exp-B validation |
|---|---:|---:|---:|---:|---:|
| Pingan | 6 | Chebyshev ≤ 12 | **14,144** | **65,710** | **34,245** |
| Qingyun | 5 | Chebyshev ≤ 10 | **3,732** | **63,179** | **28,581** |

**Why this is harder but more realistic.** The model can no longer lean on memorised
neighbourhoods; it must generalise to spatially unseen regions — which is what deployment
actually asks of it. CE validation AA falls from ≈99.99% to **0.7393 (Pingan)** and **0.7538
(Qingyun)**.

## The guard band also makes the imbalance worse — a finding in its own right

The guard band does not remove pixels uniformly. Rare classes are spatially *clustered*, so they
lose proportionally far more:

| Pingan class | official mask | NB01 70% split | **Exp-B post-guard** | retained vs 70% |
|---|---:|---:|---:|---:|
| 5 (Medium) | 2,076 | 1,453 | **85** | 5.9% |
| 7 (Tail) | 1,398 | 979 | **110** | 11.2% |
| 2 (Head) | 57,811 | 40,468 | 33,783 | 83.5% |

**Effective imbalance rises from 71.0× to 397.4× (Pingan) and 28.5× to 264.3× (Qingyun).**
Experiment B is a substantially harder long-tail problem than the dataset's nominal IR suggests.
Report **both** ratios.

**Warning — three different "training counts" exist** (`10_final_qa/TRAINING_COUNT_SEMANTICS_AUDIT_v1.md`):
**official training-mask count**, **NB01 pixel-random 70% count**, and **Experiment-B post-guard
count**. They are not interchangeable, and the Experiment-B post-guard set is **not a subset** of
the 70% split — it is a different spatial partition. Always name which one you mean.

**Why everything was retrained.** Changing the split changes the training data. Weights learned
on the old split are invalid for the new one, and the class priors themselves changed (that is
what the table above shows). All 36 Experiment-B runs are fresh.

---

# PART 10 — WHY 36 TRAINING JOBS

**Per scene (18 runs):**

| Method | Runs | Composition |
|---|---:|---|
| CE | 3 | 3 seeds, no tuning grid |
| Balanced Softmax | 3 | 3 seeds, no tuning grid (counts are the parameter) |
| Focal | 4 | γ grid at seed 42, then 3 seeds at the selected γ |
| TRAINED LA-loss | 4 | τ grid at seed 42, then 3 seeds at the selected τ |
| LDAM-DRW | 4 | C grid at seed 42, then 3 seeds at the selected C |

**18 × 2 scenes = 36 runs**, all `COMPLETE` in the frozen ledger
(`06_experiment_b/LTLC_Notebook06A_ExperimentB_36of36_FINAL_RUN_LEDGER_v1.csv`).

**Which parameter each method tuned:** Focal → γ (selected **γ=1** both scenes); LA-loss → τ
(**τ=1.0 Pingan, τ=0.5 Qingyun**); LDAM-DRW → C (**0.5 Pingan, 0.25 Qingyun**); CE and Balanced
Softmax → nothing.

**Why seed 42 for selection and 123/3407 for robustness.** Hyperparameters were chosen on **seed
42 only**, then **frozen**, then re-run on two unseen seeds. If you tuned on all three and
reported the mean, you would be reporting a best-case fit to the very seeds you are measuring on.
Freezing at one seed means seeds 123 and 3407 are genuine out-of-sample evidence about whether
the choice was stable.

**Why this beats one run per model.** A single run confounds method quality with seed luck. Three
seeds give a mean *and* a spread, let you compute per-seed **paired** differences (same seed,
both methods — removing seed-level variance), and expose sign flips. Focal, for example, is
positive on some seeds and negative on others — visible only because there is more than one run.

**Be honest about the ceiling:** three seeds is enough to *see* instability but not enough for
conventional significance (Part 17).

---

# PART 11 — EXPERIMENT-B RESULTS

Source: `09_results/tables/Thesis_Table_01_ExperimentB_Master_Results_v2.csv`. All numbers are
**TRAINED models** on **spatially disjoint validation**, AA mean over 3 seeds.

## Pingan

| Rank | Method | Config | **AA** | ΔAA vs CE | CI excludes 0? |
|---:|---|---|---:|---:|---|
| **1** | **Balanced Softmax** | training_counts | **0.7695 ± 0.0063** | **+0.0302** | yes |
| 2 | TRAINED LA-loss | τ=1 | 0.7617 ± 0.0136 | +0.0224 | yes |
| 3 | CE | — | 0.7393 ± 0.0223 | 0 | reference |
| 4 | Focal | γ=1 | 0.7391 ± 0.0127 | −0.0003 | no |
| 5 | LDAM-DRW | C=0.5 | 0.7044 ± 0.0260 | −0.0350 | yes (worse) |

**Reading:** Balanced Softmax ranks first, **+3.0 percentage points AA** over CE, with all three
seeds agreeing in sign. TRAINED LA-loss is second at +2.2 pp, also sign-consistent. Focal is
indistinguishable from CE (sign flips across seeds). **LDAM-DRW is clearly worse than CE**
(−3.5 pp) — report that; a negative result for a strong published method is informative.

## Qingyun

| Rank | Method | Config | **AA** | ΔAA vs CE | CI excludes 0? |
|---:|---|---|---:|---:|---|
| **1** | **TRAINED LA-loss** | τ=0.5 | **0.7595 ± 0.0076** | **+0.0057** | yes |
| 2 | CE | — | 0.7538 ± 0.0089 | 0 | reference |
| 3 | Focal | γ=1 | 0.7536 ± 0.0160 | −0.0002 | no |
| 4 | Balanced Softmax | training_counts | 0.7533 ± 0.0050 | −0.0005 | no |
| 5 | LDAM-DRW | C=0.25 | 0.7486 ± 0.0058 | −0.0052 | yes (worse) |

**Reading:** the gains largely evaporate. The winner improves by **+0.6 pp**. Balanced Softmax —
the *Pingan* winner — is **slightly below CE** here. Focal again indistinguishable.

## What you may and may not say

- **Say:** "On Pingan, Balanced Softmax and TRAINED LA-loss showed **suggestive** class-balanced
  gains (+3.0 pp and +2.2 pp AA), consistent in sign across all three seeds."
- **Say:** "On Qingyun the effect is much smaller (+0.6 pp) and method ranking does not transfer
  between scenes."
- **Say:** "LDAM-DRW underperformed CE on both scenes."
- **Do NOT say:** "long-tail correction robustly improves HSI classification." Two scenes, one
  backbone, three seeds, and a winner that changes between scenes do not support that.
- **Do NOT say "statistically significant"** — see Part 17.

**The honest one-liner:** *standard long-tail prior correction can help, clearly on Pingan and
marginally on Qingyun, and which method wins is dataset-dependent.*

---

# PART 12 — ORIGINAL POST-HOC LTLC RESULT

Everything here is **POST-HOC**, applied to **frozen CE validation logits**. No retraining.

**How the search ran.** For each scene × seed: sweep τ over the 9-value grid for Standard LA and
pick the best validation AA; sweep (τ, α) over 9 × 7 = 63 combinations for LTLC and pick the best
validation AA. **6 runs total** (2 scenes × 3 seeds).

**What was selected** (`09_results/tables/Thesis_Table_05_LTLC_Parameter_Stability_v2.csv`):

| Scene | Seed | selected τ | **selected α** | best AA | best AA at α=0 | **α's contribution** |
|---|---:|---:|---:|---:|---:|---:|
| Pingan | 42 | 0.5 | **0.0** | 0.7716 | 0.7716 | **0.0000** |
| Pingan | 123 | 2.0 | 0.75 | 0.7346 | 0.7313 | +0.0033 |
| Pingan | 3407 | 1.0 | **0.0** | 0.7617 | 0.7617 | **0.0000** |
| Qingyun | 42 | 2.0 | **0.0** | 0.7710 | 0.7710 | **0.0000** |
| Qingyun | 123 | 0.25 | 0.5 | 0.7515 | 0.7513 | +0.0001 |
| Qingyun | 3407 | 0.0 | **0.0** | 0.7467 | 0.7467 | **0.0000** |

**The result in one line: a non-zero α was selected in only 2 of 6 runs.** In the other four,
α = 0 — and by the collapse property in Part 7, **LTLC became standard logit adjustment exactly**.

**Why the two "wins" are not a scientific improvement.**

- **Magnitude.** +0.0033 AA (0.33 pp) and **+0.0001 AA (0.01 pp)**. The second is roughly a
  hundredth of a percentage point — smaller than the seed-to-seed spread of every method in
  Part 11.
- **Inconsistency.** Both occurred on **seed 123** and nowhere else. Same method, same data,
  different seed, opposite conclusion.
- **Selection artefact.** Searching 63 combinations and reporting the best will find *some*
  positive value by chance. That is a maximum over a grid, not an effect.
- **No mechanism.** The chosen α values (0.75 and 0.5) share no pattern with each other or with τ.

**A robust improvement would look like:** consistent non-zero α across seeds and scenes, gains
exceeding seed variance, and a coherent relationship with the data. **None of those holds.**

Additional evidence of non-identifiability: the (τ, α) landscape (Fig N3) shows a **broad
near-optimal plateau** — many parameter settings score almost identically, so α is not pinned
down by the data.

**Say it this way:** "Original LTLC selected a non-zero α in 2 of 6 runs; in the remaining four
it collapsed exactly onto post-hoc standard logit adjustment, and the two non-zero cases produced
gains of 0.33 and 0.01 percentage points on a single seed."

---

# PART 13 — WHY R1 WAS CREATED

## The flaw in the original formulation

```
z_LTLC = z − τ · (1 + α · rarity) · log(π + ε)
```

The adaptive strength is `τ · α` — **α is multiplied by τ**. Consequences:

- If **τ = 0**, the whole bracket is multiplied by zero. **α has no effect whatsoever**, no matter
  its value. This is not hypothetical: Qingyun seed 3407 selected **τ = 0**, so its α was
  meaningless by construction.
- τ and α are **entangled**. A large α with small τ can equal a small α with large τ, so "how
  much rarity adaptation was chosen" has no clean answer.
- **Interpretation becomes impossible.** You cannot say "the rarity term contributed X" when its
  scale depends on a second parameter that is also being optimised.

In short: the original parameterisation could not cleanly test its own hypothesis.

## The R1 fix

```
z_R1 = z − (τ + β · rarity) · log(π + ε)
```

The strength is now a **sum**, not a product. **τ** is the global adjustment; **β** is an
*independent, additive* rarity-specific strength. β's effect no longer vanishes when τ = 0, and
"how much rarity adaptation was selected" is answered directly by β.

**Why this is the cleaner test.** R1 isolates the actual research question — *does frequency-based
rarity deserve its own correction strength beyond the global prior term?* — as a single
identifiable parameter. β = 0 means "no", β > 0 means "yes, this much". The β grid matched α's:
`{0, 0.25, 0.5, 0.75, 1, 1.5, 2}`.

**Important protocol point:** R1 was **frozen before R1 was evaluated**, and it was compared
against **seed-42-frozen Standard-LA parameters** — a fair comparator, not a re-tuned one. That
fairness correction is itself recorded in the NB05 disclosures (an earlier intermediate R1 result
was superseded after a comparator mismatch was detected).

---

# PART 14 — THE R1 RESULT

## β = 0 was selected on **both** datasets

From `07_posthoc/..._Posthoc_Recognition_Freeze_v1.json`:

```
Pingan  : beta = 0.0,  tau = 0.5   (standard_LA_seed42_frozen_tau = 0.5)
Qingyun : beta = 0.0,  tau = 2.0   (standard_LA_seed42_frozen_tau = 2.0)
```

And from the terminal decision: `r1_differs_from_frozen_standard_la: false`,
`datasets_selecting_nonzero_beta: []`, with every robustness row showing
`exact_logit_equal: true` and `delta_AA = delta_OA = delta_Macro_F1 = 0.0`.

**With β = 0, R1 is not merely similar to standard logit adjustment — it is arithmetically
identical to it.** Same logits, same predictions, same metrics, exactly.

## Fig N4 — the β profile

`09_results/figures/Fig_N4_R1_Beta_Profile_v2.png`. X-axis: β from 0 to 2. Y-axis: best seed-42
validation AA over τ. Two lines (Pingan, Qingyun).

**Both curves decline monotonically as β increases**, and both are highest at β = 0. Adding
rarity-specific strength does not help at any tested level — it **hurts, increasingly**.

*Caveat for the caption:* the y-range spans only ≈0.750–0.771, so the visual slope corresponds to
roughly a two-percentage-point effect. The *shape* is the finding, not the steepness.

## What this means

**Under the frozen Experiment-B protocol, additional frequency-only rarity weighting was not
useful.** Once the ordinary training-prior correction is in place, weighting it further by class
frequency adds nothing and degrades performance as it grows.

## How to say it without saying "failed"

- ✅ "The original hypothesis was not supported under the stricter evaluation protocol."
- ✅ "R1 selected β = 0 on both scenes, collapsing exactly to standard logit adjustment."
- ✅ "The rarity-adaptive component was not robustly identifiable."
- ✅ "This is an informative negative result: it localises *where* the hypothesis breaks."
- ❌ "My method failed." / "LTLC doesn't work." / "The thesis didn't work out."

**The framing that is both honest and strong:** you built an experiment capable of detecting the
effect if it existed, and it returned a clean, interpretable "no" — plus a mechanistic explanation
of why. That is a result, not an absence of one.

---

# PART 15 — MECHANISM ANALYSIS: *WHY* IT DIDN'T HELP

This is the intellectual core of the thesis. A negative result that merely says "it didn't work"
is weak; one that says "it didn't work, **and here is the assumption that fails**" is strong.

## The hypothesis had a hidden premise

"Rarer classes deserve stronger correction" only makes sense if **rarer ⇒ harder**. That premise
was never tested — until now.

## Fig N1 — rarity versus CE difficulty

`09_results/figures/Fig_N1_Rarity_vs_CE_Difficulty_v2.png`. X-axis: training-frequency rarity
(0 = most common, 1 = rarest, from **Experiment-B post-guard counts**). Y-axis: mean CE per-class
error. Each point is a class, labelled by class id. One panel per scene.

Spearman correlations (`09_results/tables/Thesis_Table_06_..._v2.csv`):

| Scene | ρ (rarity vs CE error) |
|---|---:|
| **Pingan** | **+0.4061** |
| **Qingyun** | **−0.3714** |

**The signs are opposite.** On Pingan, rarer classes tend to be somewhat harder. On Qingyun,
rarer classes tend to be somewhat *easier*. Neither correlation is strong, and they point in
opposite directions across two scenes of the same benchmark, same sensor, same backbone.

**This is the explanation for Parts 12 and 14.** A correction driven purely by frequency assumes a
stable frequency→difficulty relationship. That relationship does not exist consistently. On
Qingyun, boosting rare classes more would push harder on classes that were *already easier* — so
it is unsurprising that β = 0 was selected.

**Statistical discipline:** these are **descriptive only**. `p_values_reported: False` is recorded
in the frozen table, because there are few classes (10 and 6) and hyperspectral pixels are
spatially dependent, violating independence. Report ρ; do **not** attach p-values.

## The intuition — use this in the viva

> Imagine classifying vehicles in a car park. **"Ambulance" is rare but easy** — distinctive
> shape and colour, hard to confuse. **"Silver sedan" is common but hard** — dozens of nearly
> identical silver sedans of different makes.
>
> Frequency tells you *how often* you see a class. It does not tell you *how confusable* it is.
> In spectral terms: a rare roof made of an unusual material has a distinctive signature and is
> easy; a common vegetation class that overlaps spectrally with another vegetation class is hard
> despite being everywhere.

**Rarity ≠ difficulty. That is the thesis's transferable insight.**

## Fig N2 — the isolated α contribution (appendix)

`09_results/figures/Fig_N2_Rarity_vs_Adaptive_LTLC_Gain_v2.png`. X-axis: rarity. Y-axis: per-class
accuracy difference between Original LTLC and **same-τ** POST-HOC STANDARD LA — the comparator is
held at the same τ so the α term is isolated rather than confounded with a different global
strength.

**Mandatory caption disclosure:** the two panels use **different y-axis ranges** (Pingan ≈ ±0.02,
Qingyun ≈ ±0.003 — roughly an order of magnitude smaller). Vertical magnitudes must **not** be
compared across panels. On Qingyun the isolated α contribution peaks around **0.3 percentage
points** — effectively nil, reinforcing the null result.

## Fig N3 — the parameter landscape

`09_results/figures/Fig_N3_LTLC_Seed42_Parameter_Landscape_v2.png`. X-axis: τ. Y-axis: α. Colour:
validation AA (viridis, brighter = higher). Seed 42, one panel per scene.

**What to notice:** a **broad bright plateau at low α**. Many (τ, α) settings score almost
identically, so the optimum is not sharp — **α is not identifiable from the data**. Performance
degrades toward the top-right (high τ *and* high α), i.e. over-correction.

**Mandatory caption disclosure:** *"Colour scales are independently normalized within each dataset
panel to emphasize the within-dataset parameter-response landscape; colours should therefore not
be compared quantitatively across panels."*

---

# PART 16 — CALIBRATION

## The concepts

- **Confidence** — the probability the model attaches to its prediction. Saying "roof, 0.95".
- **Calibration** — whether that number is *truthful*. Well-calibrated: of all predictions made
  at 0.90 confidence, about 90% are correct. Modern networks are typically **over-confident**.
- **NLL (Negative Log-Likelihood)** — penalises assigning low probability to the true class.
  Punishes confident mistakes harshly. Lower is better.
- **ECE (Expected Calibration Error)** — bin predictions by confidence, measure the average gap
  between confidence and accuracy in each bin (15 bins here). Lower is better.
- **Tail-ECE** — the same measure restricted to **tail classes**. This is the one your thesis
  cares about.
- **Brier score** — mean squared error between the predicted probability vector and the one-hot
  truth. Lower is better.
- **Temperature scaling (TS)** — divide all logits by one scalar **T** fitted on validation.
  T > 1 softens over-confidence.

## Why temperature scaling cannot change recognition

Dividing every logit by the same positive T does not change their **order**. The largest logit
stays the largest, so `argmax` — the predicted class — is **unchanged for every pixel**. It is an
**order-preserving** transform.

**Therefore OA, AA, Macro-F1 and Kappa are all mathematically unchanged by temperature scaling.**
Only probability-quality metrics (NLL, ECE, Brier) move.

> **Recognition improvement** = the model gets more pixels *right*.
> **Calibration improvement** = the model's *confidence numbers* become more truthful, with the
> same pixels right.
>
> Your frozen claim boundaries record `temperature_calibration_is_recognition_improvement: false`.

## What actually happened

`09_results/tables/Thesis_Table_03_Calibration_Tradeoff_v2.csv` and
`09_results/figures/Fig_Calibration_Tradeoff_Redesigned.png` (x = NLL, y = Tail-ECE, both
lower-is-better; markers = methods):

| Scene | Method | NLL | **Tail-ECE** |
|---|---|---:|---:|
| Pingan | POST-HOC STANDARD LA (uncalibrated) | 3.7333 | **0.1505** |
| Pingan | Global Temp. Scaling | 0.6701 | 0.2334 |
| Pingan | POST-HOC STANDARD LA + Global TS | 0.6888 | 0.2361 |
| Pingan | LTLC (rarity-conditioned TS) | **0.6390** | **0.5936** |
| Qingyun | POST-HOC STANDARD LA (uncalibrated) | 4.7366 | **0.2069** |
| Qingyun | Global Temp. Scaling | 0.9809 | 0.1523 |
| Qingyun | POST-HOC STANDARD LA + Global TS | 1.0272 | 0.1560 |
| Qingyun | LTLC (rarity-conditioned TS) | **0.9652** | **0.5196** |

**Three readings:**

1. **Global TS massively improves NLL** — Pingan 3.7333 → 0.6701, Qingyun 4.7366 → 0.9809. The
   uncalibrated post-hoc-LA logits were badly over-confident.
2. **Tail-class calibration did not consistently improve.** On Pingan the *uncalibrated* variant
   has the **best** Tail-ECE (0.1505); calibrating made tail calibration worse.
3. **The rarity-conditioned LTLC variant attains the best NLL but by far the worst Tail-ECE** —
   0.5936 vs 0.2334 (Pingan) and 0.5196 vs 0.1523 (Qingyun), roughly 2.5–3.4× worse on the exact
   subgroup it was designed to serve.

**Additional instability:** LTLC Full hit its allowed temperature bounds in **5 of 6** fits (both
the `a` and `b` parameters), which means the fitted parameters are saturating against the search
limits rather than settling at an interior optimum — they should not be read as stable,
generalizable values.

**Why this is scientifically interesting.** A method optimised for an aggregate probabilistic
metric can *degrade* the subgroup it targets. Aggregate NLL is dominated by the head classes,
which are numerous; the tail contributes little to it. Optimising the average therefore says
almost nothing about the tail. **That is a genuine, transferable methodological caution**, and it
is one of the more quotable findings in the thesis.

---

# PART 17 — STATISTICS

Source: `10_final_qa/STATISTICAL_ANALYSIS_VERIFICATION_v1.md`.

## The concepts

- **Mean** — average AA across the 3 seeds. **Standard deviation (SD)** — spread across seeds.
- **Paired delta** — for each seed, `AA(method) − AA(CE)` *using the same seed*. Pairing removes
  seed-level variance and is the right comparison.
- **Bootstrap CI** — resample the observations with replacement many times and take percentiles
  of the resampled means.
- **Sign-flip / permutation test** — under the null "no effect", each paired difference is equally
  likely to be positive or negative. Enumerate every possible sign assignment and see how extreme
  the observed mean is.

## Why n = 3 is a hard ceiling

**Sign-flip:** with 3 paired differences there are exactly **2³ = 8** sign patterns. The observed
pattern and its exact negation always qualify as "at least as extreme", so the smallest attainable
two-sided p-value is **2/8 = 0.25**. Every "significant-looking" row in your analysis sits exactly
at that floor. **The test cannot reach 0.05 at this sample size — as a matter of arithmetic, not
of effect strength.**

**Bootstrap:** with 3 values there are only 3³ = 27 ordered resamples and **10 distinct possible
mean values**. Verified empirically: 20,000 bootstrap draws produced exactly **10 distinct means**
for all 8 comparisons. Worse, in **all 8 comparisons the 95% CI endpoints equal exactly the
minimum and maximum of the three observed deltas** (verified to 1e-12). The "20,000 resamples"
figure conveys false precision; the interval is an arithmetically guaranteed restatement of the
observed range.

**Paired t-test:** reported for completeness at 2 degrees of freedom. Pingan LDAM-DRW yields
p = 0.0039, which *looks* significant — with n = 3, no normality check, and 8 uncorrected
comparisons, it is not trustworthy. **Recommendation: omit it from the main text.**

## The wording to use

> "Observed paired improvements are **suggestive rather than confirmatory** because only three
> random seeds were evaluated. With n = 3, an exact sign-flip test has a minimum attainable
> two-sided p-value of 0.25, and a bootstrap over three observations can take only ten distinct
> mean values; bootstrap intervals are therefore reported descriptively, not as inferential
> guarantees."

**What you may report descriptively:** consistency of sign across seeds. Sign-consistent:
Pingan Balanced Softmax (+3.0 pp), Pingan LA-loss (+2.2 pp), Pingan LDAM-DRW (−3.5 pp), Qingyun
LA-loss (+0.6 pp), Qingyun LDAM-DRW (−0.5 pp). Sign-**inconsistent** (report as indistinguishable
from CE): Focal on both scenes, Balanced Softmax on Qingyun.

**Never write "statistically significant" anywhere in this thesis.**

---

# PART 18 — THE OFFICIAL TEST

Source: `01_protocol/FINAL_GOVERNANCE_AUDIT_v2.md` (authoritative) and
`08_official_test/OFFICIAL_TEST_TECHNICAL_VERIFICATION_v1.md`.

## Two separate events — do not merge them

**Event 1 — Notebook 03, 2026-08-12.** The CE HybridSN baseline was evaluated on the official
test to **reproduce a published benchmark**. Benchmark reproduction is *measured* on the official
test by definition. The gate `official_test_authorized: true` is recorded. Nine
`*_official_test_outputs.npz` files exist as evidence. **This is normal and defensible.**

**Event 2 — 2026-08-26T16:58:29Z.** A one-time confirmatory evaluation of the two frozen
Experiment-B rank-1 configurations.

## The governance issue — disclose it, do not bury it

Two frozen artifacts — the Notebook 05 and Notebook 06B terminal decisions — record
`official_test_may_be_opened: false`. Notebook 06B's required action string is literally
`STOP_METHOD_DEVELOPMENT_AND_KEEP_OFFICIAL_TEST_SEALED`. The confirmatory evaluation was
nevertheless run **six days after** every relevant decision was frozen.

**The timeline (v2, events A–G):**

| | Event | When |
|---|---|---|
| — | Experiment-B protocols frozen *before* split creation, model construction, inference and training | pre-training |
| — | 36/36 runs complete; closing audit PASS | 2026-08-20 15:09Z |
| — | **Rank-1 per scene frozen** on validation alone | 2026-08-20 **15:37:38Z** |
| — | Post-hoc recognition parameters frozen (β = 0 both scenes) | 2026-08-20 16:23Z |
| — | NB06B terminal decision: `official_test_may_be_opened: false` | 2026-08-20 16:27Z |
| A | Day-1 package prepared (README instructs the sealed test) | 2026-08-26 |
| **B–E** | **Failed v1 attempt.** Confirmation phrase entered; terminated by `FileNotFoundError` inside `recover_hybridsn_class()` **before any checkpoint or test-data access**; **no result written** | 2026-08-26 **12:17:20Z** |
| F | Preflight (paths/shapes only, no test values) | 16:53:39Z |
| F | **Validation reproduction** — all 6 checkpoints reproduced their frozen ledger AA to 5 decimals | ~16:54–16:57Z |
| **G** | **Successful one-time official-test evaluation**, CPU, result written and retained | **16:58:29Z** |

**The failed v1 attempt did not spend the seal**, on three independent grounds (v2 §2a): failure
preceded all data loading; the v1 script had **no functional test-data loading path** (its
Section 4 was a declared stub, and the source contains **zero** occurrences of `test_indices`,
`test_labels_model`, or `fixed_split_seed2026`); and no result artifact was produced. **The
official test was scored exactly once.**

## The exact claim you may make

> **"No official-test result influenced Experiment-B model selection, hyperparameter selection,
> checkpoint selection, or LTLC method development. All such decisions were frozen using the
> spatially disjoint validation protocol before the one-time confirmatory test evaluation."**

Insert `01_protocol/THESIS_PROTOCOL_GOVERNANCE_PARAGRAPH_v1.md` **Version A verbatim** into the
protocol chapter. If you mention the failed v1 attempt at all, use the one approved sentence from
`01_protocol/BLACK_BOOK_GOVERNANCE_TIMELINE_ADDENDUM_v1.md` §2 and keep the traceback in the
appendix.

**Never write:** "the official test was never opened" · "the official test remained sealed
throughout" · anything implying the protocol authorised the run.

## The results

`09_results/tables/Thesis_Table_09_OfficialTest_Confirmation_v1.csv`:

| Scene | Method | Seed | AA | OA | Macro-F1 | Kappa |
|---|---|---:|---:|---:|---:|---:|
| Pingan | Balanced Softmax | 42 | 0.700305 | 0.824501 | 0.615754 | 0.746130 |
| Pingan | Balanced Softmax | 123 | 0.692554 | 0.858384 | 0.661700 | 0.792102 |
| Pingan | Balanced Softmax | 3407 | 0.695654 | 0.819490 | 0.587476 | 0.740111 |
| **Pingan** | **mean** | | **0.69617 ± 0.00390** | **0.83412 ± 0.02116** | | |
| Qingyun | LA-loss τ=0.5 | 42 | 0.743297 | 0.739920 | 0.686617 | 0.663245 |
| Qingyun | LA-loss τ=0.5 | 123 | 0.720876 | 0.720426 | 0.671780 | 0.638310 |
| Qingyun | LA-loss τ=0.5 | 3407 | 0.747970 | 0.751685 | 0.686857 | 0.677595 |
| **Qingyun** | **mean** | | **0.73738 ± 0.01448** | **0.73734 ± 0.01579** | | |

Test sizes: **1,026,838** (Pingan) and **859,401** (Qingyun) pixels.
Both scenes score **below** their validation AA: Pingan 0.7695 → 0.6962 (**−7.3 pp**), Qingyun
0.7595 → 0.7374 (**−2.2 pp**). That direction is expected and healthy — it is what an honest
held-out measurement looks like.

**Integrity:** official test ∩ Experiment-B train = **0** pixels; ∩ Experiment-B validation =
**0**; ∩ guard band = **0**, both scenes. All six checkpoints carry `official_test_used: false`
and reproduced their frozen validation AA to five decimals *before* the test was opened. Verdict:
**PASS**.

## The limitation you must state

**There is no Experiment-B CE result on the official test.** Only the rank-1 method per scene was
scored.

- **Do NOT** claim any test-set improvement over CE — the comparison does not exist in your data.
- **Do NOT** substitute Notebook 03's official-test CE numbers. Those models were trained on the
  overlap-prone pixel-random split, so the comparison would confound the split fix with the method
  change.
- The ΔAA-vs-CE comparison is **validation-only**, and must be labelled as such every time.

---

# PART 19 — WHAT THE THESIS PROVES

## STRONGLY SUPPORTED FINDINGS

1. Spatially disjoint validation with guard-band exclusion removed the patch-context overlap
   present in Experiment A; CE validation accuracy falls from ≈99.99% to OA 88.2% / AA 73.9%
   (Pingan) and OA 74.3% / AA 75.4% (Qingyun).
2. Experiment-B split and training protocols were frozen **before** split creation, model
   construction, inference and training, recorded as machine-checkable flags.
3. Guard-band exclusion **raises effective imbalance**: 71.0× → **397.4×** (Pingan), 28.5× →
   **264.3×** (Qingyun).
4. Tangdaowan's exclusion is a **pre-declared geometric infeasibility** (class 14), not a
   results-driven choice.
5. On Pingan validation, TRAINED Balanced Softmax (+3.0 pp AA) and TRAINED LA-loss (+2.2 pp)
   showed **suggestive** class-balanced gains, sign-consistent across seeds.
6. Qingyun gains are **much smaller** (+0.6 pp); Balanced Softmax and Focal are indistinguishable
   from CE there.
7. LDAM-DRW **underperformed** CE on both scenes.
8. The frequency-only rarity-adaptive LTLC component gave **no robust additional recognition
   gain**; non-zero α in only **2 of 6** runs.
9. **R1 selected β = 0 on both datasets** — exactly identical to POST-HOC STANDARD LA
   (`exact_logit_equal: true`, all deltas 0.0).
10. **Rarity is not a consistent proxy for CE difficulty**: Spearman ρ = **+0.4061** (Pingan) vs
    **−0.3714** (Qingyun) — opposite signs. Descriptive only.
11. LTLC's near-optimal (τ, α) region is wide and its selections vary by seed → **parameter
    non-identifiability**.
12. Global temperature scaling **substantially improved NLL** (Pingan 3.7333 → 0.6701).
13. Calibration **did not** imply recognition improvement — positive scalar temperature is
    order-preserving.
14. LTLC's rarity-conditioned scaling achieved the best NLL but **markedly worse Tail-ECE**
    (0.5936 vs 0.2334 Pingan; 0.5196 vs 0.1523 Qingyun).
15. LTLC Full hit its temperature bounds in **5 of 6** fits → unstable parameters.
16. Official-test results were obtained **only after** all decisions were frozen, six days later,
    with no subsequent iteration.
17. Official-test pixels intersect **neither** Experiment-B train, validation, **nor** guard band.
18. Official-test performance: Pingan AA 0.69617 ± 0.00390; Qingyun AA 0.73738 ± 0.01448.
19. Both scenes score **below** validation AA on official test.
20. All reported differences are **suggestive, not confirmatory** — n = 3.

## NOT SUPPORTED / DO NOT CLAIM

1. ❌ LTLC is a successful improved recognition method.
2. ❌ LTLC beats any baseline on recognition.
3. ❌ State-of-the-art performance.
4. ❌ Statistical significance of any kind; never convert "CI excludes zero" into significance.
5. ❌ Robust generalization across all QUH datasets.
6. ❌ Any Tangdaowan Experiment-B performance.
7. ❌ Test-set improvement over CE (no Experiment-B CE test result exists).
8. ❌ "The official test was never opened."
9. ❌ "The official test remained sealed throughout" / that the run was protocol-authorised.
10. ❌ Calibration improved recognition.
11. ❌ Uniform tail-class calibration improvement.
12. ❌ R1 is a distinct method from Standard LA (with β = 0 it is identical).
13. ❌ The Qingyun seed-3407 zero paired delta is missing or stale data (it is an exact τ = 0
    identity).
14. ❌ Any unlabelled training-count / rarity / imbalance-ratio figure.
15. ❌ That Experiment-B post-guard counts are a subset of the 70% split.
16. ❌ Experiment-A numbers as evidence of method quality.

---

# PART 20 — FINAL CONTRIBUTIONS

**1. Experimental contribution.** 36 fully frozen, content-hashed Experiment-B training runs
across 5 long-tail methods, 2 scenes, 3 seeds, with per-method hyperparameter grids selected at a
single seed and then held fixed.

**2. Validation / methodological contribution.** A spatially disjoint, guard-banded evaluation
protocol for hyperspectral long-tail work, with the guard threshold derived directly from patch
geometry (Chebyshev ≤ 2r), pre-registered before any result was seen, and verified to give zero
train/validation patch-footprint overlap.

**3. Long-tail comparison contribution.** A leakage-controlled comparison of CE, Focal, LDAM-DRW,
Balanced Softmax and TRAINED LA-loss, showing that gains are real but modest on Pingan, marginal
on Qingyun, that ranking does not transfer between scenes, and that LDAM-DRW underperforms CE on
both.

**4. LTLC ablation contribution.** A clean, identifiable ablation of the rarity term — including
the diagnosis that the *original* parameterisation (`τ·α`) could not test its own hypothesis, and
its replacement by R1 (`τ + β·rarity`), which returned β = 0 on both scenes.

**5. Mechanism-analysis contribution.** Evidence that the hypothesis' hidden premise is false:
**rarity does not track difficulty consistently** (ρ = +0.41 vs −0.37), plus a parameter landscape
showing α is non-identifiable.

**6. Calibration contribution.** A clean separation of recognition from calibration, and the
finding that a method optimised for aggregate NLL can *degrade* tail-class calibration by
2.5–3.4×.

**7. Reproducibility contribution.** A complete audit trail: content-hashed frozen protocols, a
36-row run ledger byte-verified against its own closing audit, canonical array-level hashes for
the official-test split, environment manifests, and a volunteered governance disclosure.

**8. Negative-result contribution.** A properly designed, adequately powered-for-its-claims,
honestly reported negative result — published rather than buried.

## The strongest contribution

**Contribution 5, supported by 2.** The single most transferable sentence in the thesis is
**"class frequency alone is insufficient to characterise hyperspectral class difficulty"** — it
explains your own negative result, and it generalises to *any* frequency-based long-tail method in
this domain. Contribution 2 is what makes it credible: without the leakage-controlled protocol,
the finding could be dismissed as an artefact of a leaky evaluation.

Contribution 6 is the best "bonus" finding and the most quotable single number
(0.5936 vs 0.2334 Tail-ECE).

---

# PART 21 — LIMITATIONS

1. **Only two primary Experiment-B scenes.** Pingan and Qingyun, same sensor family. Cross-sensor
   and cross-dataset behaviour is unknown.
2. **Tangdaowan excluded.** The highest-imbalance scene (189.7×) is untested under Experiment B,
   for a valid geometric reason — but its absence still narrows the evidence.
3. **Only three seeds.** Enough to see instability, not enough for inference.
4. **Inferential weakness.** Sign-flip floors at p = 0.25; the bootstrap CI is provably just the
   observed min/max. Nothing can be called significant.
5. **Full-cube PCA (transductive).** Unsupervised and label-free, but not strictly inductive.
6. **No successful novel recognition gain.** LTLC did not survive; R1 collapsed to standard LA.
7. **No Experiment-B CE official-test comparison.** Only rank-1 methods were scored.
8. **Dataset-specific behaviour.** The winning method differs between the two scenes.
9. **Validation sets fully consumed.** Both splits were used for all method, hyperparameter and
   checkpoint selection. No held-out validation remains, so **method development is closed** on
   this data.
10. **Single backbone; no modern long-tail baselines** (decoupled training, LADE, PaCo).
11. **A governance inconsistency exists and is disclosed** — two frozen artifacts said keep the
    test sealed; a one-time confirmatory evaluation was run anyway, after all decisions were
    frozen.

**Why these limit rather than invalidate.** Every limitation constrains the *scope* of the claims,
not their *validity*. The protocol was frozen before results were seen; the numbers reproduce
exactly from a content-hashed ledger; the negative result is stated as negative; and the claims
in Part 19 are already scoped to exactly what the evidence supports. A study that says "two
scenes, three seeds, suggestive not confirmatory" is not weak — it is correctly calibrated.

---

# PART 22 — FUTURE WORK

**Why more frequency-only tuning is not justified.** The mechanism analysis shows the *premise*
fails: rarity does not consistently track difficulty (ρ = +0.41 vs −0.37). Searching harder over
τ and α would be optimising a signal that is not reliably there — and the (τ, α) landscape already
shows a wide plateau, so a "better" setting would be a selection artefact. Both validation splits
are also fully consumed, so any new tuning on them would be tuning on used data.

**The actual direction: difficulty-aware rather than rarity-only correction.** Replace "how rare
is this class?" with "how hard is this class?", estimated from **training data only**:

- **feature-space class separation** — how far apart classes sit in the learned embedding
- **intra-class dispersion** — how tightly a class clusters
- **classification margin** — distance to the decision boundary
- **predictive uncertainty** — entropy or disagreement over the class
- **representation effective rank** — dimensionality of the class's feature subspace

**Non-negotiable protocol requirement:** any such method must be **frozen before evaluation on an
independent protocol**, and must **not** be tuned on the consumed Experiment-B validation splits.
Also worth adding: more seeds, more scenes, additional backbones, and modern long-tail baselines.

> **This is Future Work. It is not part of the completed thesis and must not be presented as a
> result.**

---

# PART 23 — THE STORY IN SIX LENGTHS

## A. ONE SENTENCE

> Under a leakage-controlled, spatially disjoint evaluation of hyperspectral long-tail
> classification, standard training-prior correction helps modestly, but an additional
> frequency-only rarity term gives no robust benefit — because class frequency turns out not to be
> a consistent proxy for class difficulty.

## B. 30 SECONDS

> Hyperspectral land-cover datasets are severely imbalanced. I proposed LTLC: make the logit
> adjustment stronger for rarer classes. To test it fairly I first had to fix the evaluation — the
> conventional pixel-random split let training and validation patches overlap, giving a
> not-credible 99.99% accuracy. With a spatially disjoint, guard-banded split, accuracy drops to a
> realistic 74–88%. Under that stricter protocol, standard methods give a suggestive +3 pp on
> Pingan and +0.6 pp on Qingyun, but my rarity term was selected as zero on both scenes. The
> mechanism analysis explains why: rarity correlates with difficulty **positively** on one scene
> and **negatively** on the other.

## C. 2 MINUTES (supervisor)

> My thesis studies long-tail correction for hyperspectral image classification on the QUH
> benchmark, using HybridSN as a fixed backbone.
>
> My original hypothesis was that rarer classes deserve a stronger logit adjustment than common
> ones. I called that LTLC: instead of one global strength τ, the strength becomes τ(1 + α·rarity).
>
> Before testing it I ran Experiment A on the conventional pixel-random split and got roughly
> 99.99% Cross-Entropy validation accuracy. That is not a good result — it is a warning. The cause
> is patch-neighbourhood overlap: centre pixels are disjoint, but 13×13 patches around adjacent
> pixels share about 92% of their content.
>
> So I built Experiment B: spatially disjoint splits with a guard band that removes any training
> pixel within Chebyshev distance 2r of a validation pixel. That guarantees zero patch overlap.
> Accuracy falls to a realistic level, and effective imbalance actually rises from 71× to 397× on
> Pingan, because the guard band removes clustered rare-class pixels disproportionately.
>
> I retrained everything — 36 frozen runs, 5 methods, 2 scenes, 3 seeds, hyperparameters selected
> at seed 42 only and then frozen. Balanced Softmax wins on Pingan at +3.0 pp AA; trained LA-loss
> wins on Qingyun at +0.6 pp. Suggestive, not confirmatory — with 3 seeds a sign-flip test cannot
> go below p = 0.25.
>
> LTLC itself: a non-zero α was selected in only 2 of 6 runs. I then found a flaw in my own
> formulation — α was multiplied by τ, so when τ = 0 the rarity term vanished entirely. I
> reformulated as R1, with an additive independent β. **R1 selected β = 0 on both scenes**, making
> it exactly identical to standard logit adjustment.
>
> The mechanism analysis explains it: rarity versus CE difficulty gives Spearman +0.41 on Pingan
> and −0.37 on Qingyun. Opposite signs. Rarity is not difficulty. That is my main finding.

## D. 5 MINUTES (technical)

Deliver C, then add:

> **Preprocessing.** PCA via covariance_eigh, 15 components for Pingan and Qingyun retaining
> ≥99.98% variance, row-wise min-max normalisation, zero padding, lazy patch extraction. Patch
> sizes are per-scene: 13 for Pingan, 11 for Qingyun, 9 for Tangdaowan, with margin = (patch−1)/2.
> PCA was fitted on the full cube — transductive but unsupervised, no labels and no test labels
> used.
>
> **Tangdaowan** was excluded on pre-declared geometric grounds: its class 14 has 62 training
> pixels with a Chebyshev diameter of 7 against a required separation above 8, so a strict
> all-class patch-disjoint split is impossible. It was never trained under Experiment B, so there
> is no Experiment-B result for it.
>
> **The LA distinction.** TRAINED LA-loss is a separately trained model with its own weights.
> POST-HOC STANDARD LA is the same formula applied to frozen CE logits with no retraining. My
> paired-delta tables measure the post-hoc object; the run ledger measures the trained one. An
> earlier audit note actually conflated them and proposed an incorrect "fix" — the correction is
> documented.
>
> **Parameter identifiability.** The (τ, α) landscape shows a broad near-optimal plateau, so α is
> not pinned down by the data. The two non-zero α selections gave +0.33 pp and +0.01 pp, both on
> seed 123 only.
>
> **Calibration.** Global temperature scaling cut NLL from 3.73 to 0.67 on Pingan. But temperature
> scaling is order-preserving, so predictions and therefore OA/AA/Macro-F1/Kappa are mathematically
> unchanged — it is not a recognition improvement. And the rarity-conditioned variant achieved the
> best NLL while producing the *worst* Tail-ECE, 0.59 versus 0.23. A method optimised for an
> aggregate metric degraded the subgroup it targeted.
>
> **Official test.** Scored exactly once, on 26 August, six days after every decision was frozen.
> Pingan AA 0.696, Qingyun AA 0.737 — both below validation, as expected. I disclose a governance
> inconsistency: two earlier frozen artifacts recorded that the test should stay sealed. The claim
> I make is narrow and precise: no official-test result influenced any Experiment-B decision. I do
> not claim the test was never opened — Notebook 03 opened it legitimately for benchmark
> reproduction. And there is no Experiment-B CE test result, so I make no test-set claim relative
> to CE.

## E. 10 MINUTES (full)

Deliver D, then walk Parts 15, 19, 20, 21 and 22 in order: the mechanism analysis with Figs N1/N3/N4;
the supported-findings list; the eight contributions with contribution 5 identified as strongest;
the eleven limitations stated without hedging; and future work as difficulty-aware rather than
rarity-only correction, explicitly labelled as not part of the thesis.

## F. GROUPMATE VERSION (very easy words)

> You know how a normal photo has 3 colours per pixel? These images have **176**. Each pixel is
> basically a fingerprint of what material is there. My job: label every pixel — roof, road, tree,
> water.
>
> Problem: some labels are everywhere and some are almost nowhere. On my Pingan image the commonest
> class has 57,811 training pixels and the rarest has 814. The model learns to ignore the rare
> ones, because guessing "common" is usually safe.
>
> There's a known fix that gives rare classes a score boost. **My idea:** boost the *rarest*
> classes even more. That's LTLC.
>
> **But first I found a bug in how everyone tests these models.** The model doesn't look at one
> pixel — it looks at a 13×13 square around it. If pixel (100,100) goes to testing and pixel
> (100,101) goes to training, those two squares overlap by about 92%. So the model has basically
> already seen the answer. That's why my first experiment got 99.99% accuracy — which is fake-good,
> not good.
>
> So I rebuilt the test properly: split by **regions**, not pixels, and throw away a buffer zone in
> between so the squares can never touch. Accuracy dropped to 74–88%. That's the real number.
>
> **Then the honest part.** With the proper test, my idea got picked as "use zero extra boost" on
> both images. Meaning: my addition did nothing.
>
> **And I found out why**, which is the actually interesting bit. My whole idea assumed *rare =
> hard*. It isn't. On one image rare classes were a bit harder; on the other they were a bit
> **easier**. Think of a car park: "ambulance" is rare but super easy to spot, while "silver sedan"
> is everywhere and hard to tell apart. Rare doesn't mean hard.
>
> So my thesis isn't "here's my method and it works". It's "here's proof the usual testing is too
> easy, here's an honest comparison, and here's why the popular assumption that rare = hard is
> wrong." That's a real result — and I have receipts for every number.

---

# PART 24 — FACULTY MEETING SCRIPT

*Use a calm, factual tone. You are reporting findings, not defending yourself.*

**1. The problem.**
"My thesis is on long-tail class imbalance in hyperspectral image classification, using the QUH
benchmark with HybridSN as a fixed backbone. Rare land-cover classes are systematically
under-recognised, and Overall Accuracy hides that, so I evaluate primarily on Average Accuracy."

**2. What I originally proposed.**
"Standard logit adjustment applies one global strength τ to every class. I proposed making the
strength rarity-dependent — τ(1 + α·rarity) — on the hypothesis that rarer classes are
systematically harder and need a stronger correction. I called it LTLC."

**3. Experiment A.**
"My first full comparison used the conventional pixel-random split and returned about 99.99%
Cross-Entropy validation accuracy. I treated that as a methodological warning rather than a
result. The cause is patch-neighbourhood overlap: the split makes centre pixels disjoint, but the
model consumes 13×13 patches, and patches around adjacent pixels share roughly 92% of their
content. I've kept Experiment A frozen as motivation — it's the reason the rest of the work
exists — but I never use its numbers as evidence of method quality."

**4. Why I redesigned.**
"Any comparison run on that split would be measuring memorised neighbourhoods rather than
generalization, so the original research question couldn't be answered on it."

**5. Experiment B.**
"I built a spatially disjoint protocol: split by spatial clusters, then apply a guard band that
removes every training pixel within Chebyshev distance 2r of a validation pixel — 12 for Pingan,
10 for Qingyun. That guarantees zero patch-footprint overlap by construction, and I verified it
numerically. Accuracy fell to a realistic level. One thing I didn't expect: the guard band raises
effective imbalance from 71× to 397× on Pingan, because rare classes are spatially clustered and
lose proportionally more pixels. So Experiment B is a genuinely harder problem than the dataset's
nominal ratio suggests. Everything was retrained — 36 runs, all frozen and content-hashed."

**6. What the baselines showed.**
"On Pingan, Balanced Softmax is first at +3.0 percentage points AA over CE and trained LA-loss
second at +2.2, both sign-consistent across seeds. On Qingyun the effect largely disappears — the
winner is trained LA-loss at +0.6 pp, and Balanced Softmax is actually marginally below CE.
LDAM-DRW underperformed CE on both. I describe these as suggestive rather than confirmatory: with
three seeds, an exact sign-flip test cannot produce a p-value below 0.25."

**7. What happened to LTLC.**
"Applied post-hoc to frozen CE validation logits, a non-zero α was selected in only 2 of 6 runs.
Both were on seed 123, and the gains were 0.33 and 0.01 percentage points. The parameter landscape
shows a broad near-optimal plateau, so α isn't identifiable from the data."

**8. Why R1 was needed.**
"I also found a structural flaw in my own formulation. Because α is multiplied by τ, the rarity
term disappears entirely when τ = 0 — which actually occurred, on Qingyun seed 3407. So the
original parameterisation couldn't cleanly test its own hypothesis. I reformulated as R1, with an
additive independent coefficient: τ + β·rarity. I froze R1 before evaluating it and compared it
against seed-42-frozen Standard-LA parameters so the comparator was fair. R1 selected β = 0 on
both scenes, which makes it arithmetically identical to standard logit adjustment — the frozen
record shows exact_logit_equal true and all deltas zero."

**9. The mechanism analysis.**
"This is the part I think is the actual contribution. My hypothesis had a hidden premise: that
rarer means harder. I tested it directly. Spearman correlation between rarity and Cross-Entropy
class error is +0.41 on Pingan but −0.37 on Qingyun — opposite signs on two scenes of the same
benchmark. Rarity is not a reliable proxy for difficulty, which explains why a purely
frequency-driven correction has nothing stable to exploit. I report those correlations
descriptively only, without p-values, because there are few classes and the pixels are spatially
dependent."

**10. Calibration.**
"Separately, global temperature scaling cut NLL substantially — 3.73 to 0.67 on Pingan. But
temperature scaling is order-preserving, so predictions don't change and it's explicitly not a
recognition improvement. More interestingly, the rarity-conditioned variant achieved the best NLL
while producing the worst tail-class calibration, 0.59 against 0.23. A method optimised for an
aggregate probabilistic metric degraded the exact subgroup it was designed to help."

**11. The contribution.**
"The contribution isn't a working new method — the original hypothesis wasn't supported under the
stricter protocol. It's three things: a leakage-controlled evaluation protocol for hyperspectral
long-tail work; an honest comparison of five methods under it; and leakage-controlled evidence
that class frequency alone is insufficient to characterise hyperspectral class difficulty. The
last one is the transferable finding, and it generalises to any frequency-only long-tail method in
this domain."

**12. What goes in the Black Book.**
"I'll frame it as a leakage-controlled robustness study, with the negative result reported as a
result and the mechanism analysis as the core chapter. I'll disclose one governance point openly:
two earlier frozen artifacts recorded that the official test should remain sealed, and a one-time
confirmatory evaluation was nevertheless run six days after all decisions were frozen. The claim I
make is narrow — no official-test result influenced any Experiment-B selection decision. I won't
claim the test was never opened, because Notebook 03 legitimately used it for benchmark
reproduction. And since I only scored the winning method per scene, I make no test-set claim
relative to Cross-Entropy."

**Closing.**
"I'd value your view on two things: whether the mechanism finding is the right thing to lead with,
and how much space the calibration result deserves."

---

# PART 25 — QUESTIONS YOUR SUPERVISOR MAY ASK

*(Short answer → deeper answer → answer to avoid.)*

**1. Why QUH?** UAV hyperspectral benchmark with fixed official masks, three scenes, and real
long-tail structure. → Fixed masks make results comparable; three scenes allow a feasibility
choice; imbalance ratios span 28.5× to 189.7×. → *Avoid:* "it was available."

**2. Why HybridSN?** Established, widely reproduced HSI baseline; Notebook 03 reproduces a
published benchmark with it. → Its 3D→2D hybrid is standard for spectral-spatial learning, and
using a known backbone anchors the pipeline. → *Avoid:* claiming any part of it as your
contribution.

**3. Why PCA?** 176 bands are correlated and noisy; PCA cuts redundancy and makes 3-D convolution
tractable. → covariance_eigh, ≥99.98% variance retained. → *Avoid:* "to make it faster" alone.

**4. Why full-cube PCA — isn't that leakage?** It is transductive but **unsupervised**; no label
and no test label was used. → One frozen cube, `full_cube_pca_recomputed: false`, so no
split-dependent refitting; it is also the field convention, keeping results comparable. → *Avoid:*
denying it is transductive.

**5. Why do patch sizes differ per scene?** They are frozen per-scene properties from Notebook 02,
matched to scene characteristics. → 13/11/9 with margins 6/5/4; `margin = (patch−1)//2` is
enforced in code because a wrong margin silently decentres every patch. → *Avoid:* implying you
tuned patch size on results.

**6. Why PCA15 vs PCA20?** Tangdaowan has 16 classes vs 10 and 6, so more spectral directions were
retained. → All three exceed 99.98% explained variance. → *Avoid:* "arbitrary."

**7. Why three seeds?** Compute budget across 36 full runs. → Enough to expose sign instability
and compute paired deltas; explicitly not enough for inference, which is why I never claim
significance. → *Avoid:* pretending three is adequate.

**8. Why 36 runs?** 18 per scene × 2 scenes: CE 3, Balanced Softmax 3, and 4 each for Focal,
LA-loss and LDAM-DRW (grid at seed 42 + 3 seeds at the selection). → *Avoid:* vagueness about the
composition.

**9. Why tune at seed 42 only?** So seeds 123 and 3407 are genuine out-of-sample evidence. → Tuning
on all three and reporting the mean would report a best-case fit to the seeds being measured. →
*Avoid:* "convention."

**10. Why was Tangdaowan dropped?** Pre-declared geometric infeasibility: class 14 has 62 training
pixels, Chebyshev diameter 7, spans 8, against required separation > 8. → Recorded in the frozen
protocol before any Experiment-B training. → *Avoid, emphatically:* any suggestion its results were
poor. **No Experiment-B Tangdaowan result exists.**

**11. Why were Experiment A results so high?** Patch-neighbourhood overlap. → Centre pixels
disjoint, but 13×13 patches around adjacent pixels share ~92% of content. → *Avoid:* "the model
was very good."

**12. Was that leakage — did you cheat?** It is a protocol design flaw, not misconduct. → Standard
terminology: spatial-context overlap / overlap-prone validation. Extremely common in the HSI
literature, which is why documenting it has value. → *Avoid:* the words "cheating" or "fraud."

**13. Why not just use Experiment A?** It cannot answer the research question — it measures
memorised neighbourhoods. → Retained frozen as motivation only. → *Avoid:* using any Exp-A number
as evidence of method quality.

**14. Why did you keep Experiment A instead of deleting it?** It is the evidence that motivates
Experiment B, and deleting inconvenient prior results is itself an integrity problem. → It is
classified as never-deletable audit history. → *Avoid:* "I forgot to clean it up."

**15. Why Logit Adjustment specifically?** It is principled — a Bayes-optimal correction for known
prior shift — cheap, and applicable both in-loss and post-hoc. → That dual applicability is what let
me separate the trained and post-hoc objects cleanly. → *Avoid:* "it was popular."

**16. Difference between trained LA-loss and post-hoc standard LA?** Trained LA-loss is a
separately trained model with its own weights; post-hoc LA transforms a frozen CE model's logits
with no retraining. → Same formula shape, different experimental objects, different tables. →
*Avoid:* saying "LA" unqualified.

**17. What exactly is LTLC?** `z − τ(1 + α·rarity)·log(π+ε)`, applied post-hoc to frozen CE
validation logits. → With α = 0 it is exactly standard LA. → *Avoid:* describing it as a training
method.

**18. Why introduce α at all?** To let rarer classes receive stronger correction, on the hypothesis
that rarer ⇒ harder. → That premise is exactly what the mechanism analysis later falsified. →
*Avoid:* post-hoc rationalisation.

**19. Why did you need R1?** Because α was multiplied by τ, so at τ = 0 the rarity term vanished
entirely — which actually occurred on Qingyun seed 3407. → R1 makes it additive and independent:
`τ + β·rarity`. → *Avoid:* presenting R1 as an improvement in performance rather than in
identifiability.

**20. Why β = 0?** The search selected it on both scenes. → Fig N4 shows AA declining monotonically
with β on both; β = 0 is the maximum. → *Avoid:* "it was close to zero" — it was exactly zero.

**21. What does Fig N4 prove?** Under this protocol, additional frequency-only rarity weighting
does not help at any tested strength and degrades performance as it grows. → *Does not* prove no
rarity-aware method could ever work — only frequency-only, on these two scenes. → *Avoid:*
over-generalising.

**22. Does rarity equal difficulty?** No — Spearman +0.41 on Pingan, −0.37 on Qingyun. → Opposite
signs on two scenes of the same benchmark. → *Avoid:* attaching p-values.

**23. Why no p-values on the correlations?** Few classes (10 and 6) and spatially dependent pixels
violate independence. → `p_values_reported: False` is frozen in the table. → *Avoid:* computing
them "just to show."

**24. Why did calibration help NLL but not Tail-ECE?** NLL is an aggregate dominated by numerous
head classes; the tail barely contributes. → Optimising the average therefore says little about the
tail, and the rarity-conditioned variant actively worsened it (0.59 vs 0.23). → *Avoid:* implying
calibration improved recognition.

**25. Does temperature scaling change predictions?** No — it is order-preserving, so argmax is
unchanged for every pixel. → OA/AA/Macro-F1/Kappa are mathematically identical. → *Avoid:* listing
it as a recognition method.

**26. Why no statistical significance?** With n = 3, the exact sign-flip test floors at p = 0.25.
→ The bootstrap over three points yields only 10 distinct means, and its 95% endpoints are provably
the observed min and max. → *Avoid:* "the effect was too small" — the *test* is the limit.

**27. Then why report a bootstrap CI at all?** As a descriptive summary of the observed range,
clearly labelled. → It is demoted to a faint band in Fig_PerSeed_Delta_vs_CE; per-seed points lead.
→ *Avoid:* "CI excludes zero, therefore significant."

**28. Why was the official test opened after a gate said false?** Two frozen artifacts did record
`official_test_may_be_opened: false`; a one-time confirmatory evaluation was nevertheless run six
days after all decisions were frozen. → I disclose it rather than reconcile it, and the claim I
make is only about *influence*. → *Avoid:* claiming the protocol authorised it.

**29. Did the test influence development?** No. → Every decision is timestamped 2026-08-20; the test
ran 2026-08-26 16:58:29Z; all six checkpoints carry `official_test_used: false` and reproduced
their frozen validation AA to five decimals beforehand; nothing was changed afterwards. → *Avoid:*
"the test was never opened."

**30. What was the failed v1 attempt?** A preliminary harness launched once at 12:17:20Z that
terminated inside `recover_hybridsn_class()` before any model or test-data loading; no result was
written. → It could not have read the test set: its data-loading section was a declared stub with
zero references to `test_indices`. → *Avoid:* describing it as a near-miss.

**31. Why is there no Experiment-B CE official-test comparison?** Only the rank-1 method per scene
was scored, to keep the one-time evaluation minimal. → So the ΔAA-vs-CE comparison is
validation-only. → *Avoid:* substituting Notebook 03's CE test numbers — different training split.

**32. Could you just run CE on the test now?** It would be a second opening of the test set. → It is
a pre-specified baseline rather than a re-roll, so it would be defensible if decided and documented
in advance — but it is not in the current thesis. → *Avoid:* doing it casually.

**33. Why is official-test AA lower than validation AA?** Expected — held-out performance below
validation is normal and healthy. Pingan −7.3 pp, Qingyun −2.2 pp. → *Avoid:* explaining it away.

**34. What is actually novel here?** Not the backbone, not the losses, not LTLC (which didn't
survive). → The leakage-controlled protocol, the clean identifiable ablation, and the
rarity≠difficulty evidence. → *Avoid:* inflating LTLC into a contribution.

**35. Isn't a negative result a weak thesis?** Only if it is uninformative. → This one is
pre-registered, mechanistically explained, and localises exactly which assumption fails — which is
useful to anyone else considering frequency-based correction. → *Avoid:* apologising.

**36. What could you publish from this?** Most plausibly a short methodological paper on
overlap-prone validation in HSI plus the rarity≠difficulty finding. → The calibration trade-off is a
strong secondary result. → *Avoid:* claiming a method paper.

**37. What would you do next?** Difficulty-aware rather than frequency-only correction — feature
separation, intra-class dispersion, margin, uncertainty, effective rank — frozen before evaluation
on an independent protocol. → *Avoid:* presenting it as done.

**38. Why can't you tune more on the current validation sets?** They are fully consumed by method,
hyperparameter and checkpoint selection. → Further tuning would be tuning on used data. → *Avoid:*
"I could try a few more values."

**39. Why does the winning method differ between scenes?** Balanced Softmax wins on Pingan,
trained LA-loss on Qingyun. → Consistent with the mechanism finding: the frequency→difficulty
relationship differs between scenes, so frequency-driven methods behave differently. → *Avoid:*
picking the better scene and generalising.

**40. Why did LDAM-DRW do worse than CE?** It underperformed on both scenes (−3.5 pp Pingan,
−0.5 pp Qingyun), consistent in sign. → I report it as observed; margin-based methods can be
sensitive to the very small post-guard tail counts (Pingan class 5 falls to 85 pixels). → *Avoid:*
asserting the cause as established.

**41. What is the effective imbalance in Experiment B?** 397.4× on Pingan and 264.3× on Qingyun,
versus nominal 71.0× and 28.5×. → The guard band removes clustered rare-class pixels
disproportionately. → *Avoid:* quoting only the nominal ratio.

**42. Which training count did you use for the priors?** Experiment-B post-guard counts. → Verified:
the Qingyun LA-loss checkpoint records `class_counts: [19556, 11807, 967, 74, 15220, 15555]`,
matching the post-guard record exactly. → *Avoid:* saying "the training counts" unqualified.

**43. Why are some paired deltas exactly zero?** Because τ = 0 was selected for that run, making
the LA transform the identity — so LA = CE = LTLC exactly. → This is a mathematical identity, and
an earlier note wrongly called it stale data; the correction is documented. → *Avoid:* calling it
missing data.

**44. How do I know the results are reproducible?** A 36-row content-hashed ledger byte-verified
against its own closing audit; PCA cubes and the Experiment-B split byte-identical to their frozen
hashes; canonical array hashes for the official-test split; full environment manifests. → *Avoid:*
"trust me."

---

# PART 26 — GLOSSARY

| Term | Meaning |
|---|---|
| **HSI** | Hyperspectral Image — hundreds of narrow wavelength bands per pixel instead of 3 colours. |
| **UAV** | Unmanned Aerial Vehicle — the drone platform the QUH scenes were captured from. |
| **QUH** | The hyperspectral benchmark used here; three scenes (Pingan, Qingyun, Tangdaowan). |
| **PCA** | Principal Component Analysis — compresses correlated bands into fewer uncorrelated components. |
| **CNN** | Convolutional Neural Network — learns spatial filters over image patches. |
| **HybridSN** | The fixed backbone: three 3-D convolutions, then a 2-D convolution, then fully-connected layers. |
| **CE** | Cross-Entropy — the standard classification loss and the reference baseline. |
| **Focal** | A loss that down-weights easy examples to focus on hard ones; parameter γ. |
| **LDAM** | Label-Distribution-Aware Margin — enforces larger decision margins for rarer classes. |
| **DRW** | Deferred Re-Weighting — turns on class re-weighting only late in training. |
| **Balanced Softmax** | Adds log training counts inside the softmax so the loss behaves as if classes were balanced. |
| **LA** | Logit Adjustment — shifting class scores by their log prior. Never use unqualified. |
| **TRAINED LA-LOSS** | A **separately trained** model with the adjustment inside the loss. Own weights, own checkpoint. |
| **POST-HOC STANDARD LA** | The same formula applied **after training** to a frozen CE model's logits. No retraining. |
| **LTLC** | Your proposal: `z − τ(1 + α·rarity)·log(π+ε)`. With α = 0 it is exactly standard LA. |
| **R1** | The revised formulation: `z − (τ + β·rarity)·log(π+ε)`. β is independent of τ. Selected β = 0. |
| **TS** | Temperature Scaling — divide logits by one scalar T. Order-preserving, so predictions never change. |
| **NLL** | Negative Log-Likelihood — penalises low probability on the true class. Lower is better. |
| **ECE** | Expected Calibration Error — average gap between confidence and accuracy across bins. |
| **Tail-ECE** | ECE computed only on tail classes — the calibration metric your thesis cares about. |
| **Brier** | Mean squared error between the predicted probability vector and the one-hot truth. |
| **OA** | Overall Accuracy — fraction of all pixels correct. Dominated by head classes. |
| **AA** | Average Accuracy — mean of per-class accuracies. **Your primary metric.** |
| **Macro-F1** | Mean per-class F1 score; balances precision and recall, class-equally. |
| **Kappa** | Cohen's Kappa — agreement corrected for chance. |
| **Head / Medium / Tail** | Frequency groups: most common / intermediate / rarest classes. |
| **Class prior (π_k)** | The empirical training probability of class *k*: `n_k / Σn`. |
| **Rarity (r_k)** | Normalised inverse-frequency score; 0 = most common, 1 = rarest. |
| **Seed** | Random-number seed controlling initialisation and shuffling. Yours: 42, 123, 3407. |
| **Checkpoint** | Saved model weights. Yours were selected on **best validation AA**. |
| **Guard band** | Training pixels within Chebyshev distance 2r of a validation pixel, discarded entirely. |
| **Spatially disjoint validation** | Splitting by spatial region rather than by pixel, so patches cannot overlap. |
| **Patch overlap** | Two patches sharing pixels because their centres are close — the Experiment-A flaw. |
| **Calibration** | Whether predicted confidences are truthful, independent of whether predictions are right. |
| **Transductive preprocessing** | Preprocessing fitted using all pixels including unlabelled test pixels. Unsupervised here — no labels used. |

---

# PART 27 — FIGURE EXPLANATION GUIDE

Source: `12_black_book/BLACK_BOOK_FINAL_FIGURE_MANIFEST_v1.md`. Nine approved figures; **Fig N5 is
excluded and must not appear.**

### F1 · `Fig_ClassFrequency_LongTail_Distribution.png` — Ch3
X: class id (sorted by frequency). Y: **official training-mask** pixels, log scale. Colours:
Head (blue) / Medium (yellow) / Tail (red); IR annotated per scene.
**Notice first:** the log-scale cliff — the head classes tower over the tail.
**Supports:** the datasets are genuinely long-tailed; the problem is real.
**Does NOT prove:** anything about Experiment-B difficulty — these are *official mask* counts, not
post-guard counts.
**20 seconds:** "All three QUH scenes are long-tailed on a log scale. Pingan spans 71×, Qingyun
28.5×, Tangdaowan 190×. These are official training-mask counts; under Experiment B's guard band
the effective ratios are much worse."

### F2 · `Fig_ExperimentA_vs_B_Leakage_Comparison.png` — Ch5 ⭐
X: four groups (Pingan OA/AA, Qingyun OA/AA). Y: CE validation accuracy, 0–100%. Red = Experiment A
(pixel-random), blue = Experiment B (spatially disjoint). Values annotated on bars.
**Notice first:** red bars pinned at ~100%, blue bars at 74–88%.
**Supports:** conventional pixel-random validation drastically overstates HSI performance.
**Does NOT prove:** the models got worse — the *measurement* got honest. Same backbone, same data,
different split.
**20 seconds:** "Same model, same scenes, only the split changed. Under pixel-random validation
Cross-Entropy scores about 99.99%. Under spatially disjoint validation with a guard band it drops
to 88% OA and 74% AA on Pingan. The first number was measuring patch overlap."

### F3 · `Fig_Spatial_TrainVal_Split_Map.png` — Ch6
X: image column. Y: image row (inverted). Blue = train, orange = validation, grey = guard-excluded.
Plotted from the actual `.npz` split indices, not a schematic.
**Notice first:** train and validation occupy **separate spatial blocks**, with a thin grey seam
between them.
**Supports:** the split is genuinely spatial; zero train/validation patch-footprint overlap.
**Does NOT prove:** anything about accuracy.
**20 seconds:** "This is the real split, drawn from the index files. Blue trains, orange validates,
grey is the discarded guard band. Because they're separate regions with a buffer, no validation
patch can overlap a training patch."

### F4 · `Fig_PerSeed_Delta_vs_CE.png` — Ch7 ⭐
X: ΔAA vs Cross-Entropy (percent). Y: one row per dataset×method. Markers: circle/square/triangle =
seeds 42/123/3407. Black bar = mean ± SD. Faint grey band = bootstrap CI, **descriptive only**.
Dashed line at zero.
**Notice first:** which rows have all three markers on the same side of zero.
**Supports:** Pingan Balanced Softmax and LA-loss are sign-consistent; Focal straddles zero.
**Does NOT prove:** significance. With n = 3 the grey band's endpoints are just the observed min and
max.
**20 seconds:** "Each row is a method; the three markers are the three seeds, and the black bar is
mean ± SD. Balanced Softmax on Pingan has all three seeds positive, around +3 points. Focal
straddles zero. The grey band is a bootstrap interval shown descriptively — with three seeds it's
literally the observed range."

### F5 · `Fig_Calibration_Tradeoff_Redesigned.png` — Ch9 ⭐
X: NLL (lower better). Y: Tail-ECE (lower better). Markers by method; **hollow blue ring** = global
TS, purple square = post-hoc LA + global TS, red diamond = LTLC, grey triangle = uncalibrated
post-hoc LA. One panel per scene.
**Notice first:** the red diamond sits at the **far left** (best NLL) and the **top** (worst
Tail-ECE).
**Supports:** the rarity-conditioned variant wins the aggregate metric while losing badly on the
subgroup it targets.
**Does NOT prove:** anything about recognition — this is calibration only.
**20 seconds:** "Left is better NLL, down is better tail calibration. LTLC is furthest left — best
overall likelihood — but highest up, worst tail calibration, 0.59 against 0.23. Optimising the
aggregate metric hurt the tail. And none of this changes predictions, because temperature scaling
is order-preserving."
**This figure replaces the excluded Fig N5.**

### F6 · `Fig_N1_Rarity_vs_CE_Difficulty_v2.png` — Ch8 ⭐
X: training-frequency rarity (**Experiment-B post-guard**), 0 = most common, 1 = rarest.
Y: mean CE per-class error. Each point is a class, labelled by class id. Spearman ρ in each panel
title.
**Notice first:** the **opposite tilt** between panels — ρ = +0.406 (Pingan) vs −0.371 (Qingyun).
**Supports:** rarity is not a consistent proxy for difficulty — the mechanistic explanation for
β = 0.
**Does NOT prove:** causation, and no p-values are claimed (few classes, spatially dependent pixels).
**20 seconds:** "Rarity on the x-axis, Cross-Entropy error on the y-axis, one point per class. On
Pingan rarer classes are somewhat harder, ρ = +0.41. On Qingyun the correlation is *negative*,
−0.37. Same benchmark, same backbone, opposite signs. That's why a frequency-only correction has
nothing stable to exploit."

### F7 · `Fig_N3_LTLC_Seed42_Parameter_Landscape_v2.png` — Ch8
X: τ. Y: α. Colour: validation AA (viridis, brighter = higher). Seed 42, one panel per scene.
**Notice first:** the **broad bright plateau at low α** — many settings score nearly identically.
**Supports:** α is not identifiable from the data; the "optimum" is not sharp.
**Does NOT prove:** cross-panel comparisons — **the colour scales are independently normalized per
panel** and must be captioned as such.
**20 seconds:** "This is validation AA across the tau-alpha grid for seed 42. The large bright
plateau at low alpha means many settings perform almost the same — alpha isn't pinned down by the
data. Note the colour scales are normalised per panel, so don't compare colours across scenes."

### F8 · `Fig_N4_R1_Beta_Profile_v2.png` — Ch8 ⭐
X: R1 coefficient β, 0 → 2. Y: best seed-42 validation AA over τ. Two lines (Pingan, Qingyun).
**Notice first:** both curves **decline monotonically**, both peak at β = 0.
**Supports:** additional frequency-only rarity weighting does not help at any tested strength.
**Does NOT prove:** that no rarity-aware method could work — only frequency-only, on these scenes,
under this protocol. Note the compressed y-range (~0.750–0.771 ≈ two percentage points).
**20 seconds:** "Beta is the independent rarity strength in my revised formulation. Both scenes peak
at beta equals zero and fall monotonically as beta grows. That's the clearest single statement of
the negative result — the extra rarity term isn't just unhelpful, it's actively harmful as it
increases."

### F9 · `Fig_N2_Rarity_vs_Adaptive_LTLC_Gain_v2.png` — **Appendix**
X: rarity. Y: per-class accuracy difference, Original LTLC minus **same-τ** post-hoc standard LA.
**Notice first:** how tiny the Qingyun values are.
**Supports:** the isolated α contribution is negligible, especially on Qingyun (≤ ~0.3 pp).
**Does NOT prove:** cross-panel magnitude comparison — **the y-axis ranges differ by roughly an
order of magnitude** (Pingan ±0.02, Qingyun ±0.003) and must be captioned as such.
**20 seconds:** "This isolates just the alpha term against a same-tau comparator, so it's not
confounded with a different global strength. On Qingyun the effect maxes out around 0.3 percentage
points. Careful — the two panels use different y-scales."

## TOP 5 TO SHOW YOUR SUPERVISOR

1. **F2 — Experiment A vs B** — the reason the whole project exists.
2. **F8 — Fig N4 β profile** — the cleanest statement of the negative result.
3. **F6 — Fig N1 rarity vs difficulty** — *why* it's negative; your strongest contribution.
4. **F4 — Per-seed ΔAA** — honest presentation of the baseline comparison.
5. **F5 — Calibration trade-off** — the best secondary finding.

Show them in that order: motivation → result → explanation → rigour → bonus.

---

# PART 28 — TABLE EXPLANATION GUIDE

All in `09_results/tables/`. Always cite the versions listed here.

### `Thesis_Table_01_ExperimentB_Master_Results_v2.csv` — **MAIN, Ch6**
**Purpose:** Experiment-B validation ranking of all five methods on both scenes.
**Key columns:** `comparison_object` (= TRAINED Experiment-B model), `AA_mean`/`AA_sd` (primary
metric), `delta_AA_vs_CE`, plus OA/Macro-F1/Kappa.
**Key values:** Pingan Balanced Softmax 0.7695 (+0.0302); Qingyun LA-loss 0.7595 (+0.0057).
**Supports:** long-tail correction helps on Pingan, marginally on Qingyun, and ranking doesn't
transfer.
**Mistake to avoid:** reading these as official-test numbers. They are **validation**. Also: "LA-loss"
here means **TRAINED**, not post-hoc.

### `Thesis_Table_02_PerSeed_Deltas_vs_CE_v1.csv` — **MAIN, Ch6**
**Purpose:** per-seed paired differences vs CE, with descriptive intervals.
**Key columns:** `delta_seed42/123/3407` (lead with these), `mean_delta_AA`, `sd_delta_AA`,
`exact_sign_flip_p_min_0p25`, `bootstrap95_*_descriptive`, `inferential_status`.
**Key values:** the p-column is **0.25 or 1.00 everywhere** — 0.25 is the floor.
**Supports:** sign-consistency claims, honestly bounded.
**Mistake to avoid:** treating "CI excludes zero" as significance. The CI endpoints are literally the
observed min and max.

### `Thesis_Table_03_Calibration_Tradeoff_v2.csv` — **MAIN, Ch9**
**Purpose:** NLL / ECE / Tail-ECE / Brier per calibration method.
**Key columns:** `method` (now explicitly `POST-HOC STANDARD LA + Global TS` and `POST-HOC STANDARD
LA (uncalibrated)`), `NLL_mean`, `TailECE_mean`.
**Key values:** Pingan LTLC NLL 0.6390 (best) with Tail-ECE 0.5936 (worst).
**Supports:** the NLL/Tail-ECE trade-off.
**Mistake to avoid:** calling any of it a recognition result. Use v2 — v1 said ambiguous "LA".

### `Thesis_Table_04_PerClass_Frequency_and_Mechanism_v2.csv` — **MAIN, Ch8**
**Purpose:** per-class rarity, CE difficulty, post-hoc LA gain, isolated α gain.
**Key columns:** `expB_post_guard_train_count`, `rarity_from_expB_post_guard_count`,
`ce_accuracy_mean`, `posthoc_standard_LA_minus_CE_mean`, `adaptive_alpha_gain_mean`.
**Supports:** the per-class mechanism story behind Fig N1.
**Mistake to avoid:** confusing these counts with official mask counts. The column names now say
post-guard explicitly — use them.

### `Thesis_Table_05_LTLC_Parameter_Stability_v2.csv` — **MAIN, Ch8**
**Purpose:** which (τ, α) was selected per run, and what α actually bought.
**Key columns:** `comparison_object` (= POST-HOC grid over frozen CE logits), `selected_tau`,
`selected_alpha`, `best_AA`, `best_AA_alpha0`, `adaptive_minus_alpha0`, near-optimal counts.
**Key values:** α = 0 in **4 of 6** runs; the two non-zero cases give **+0.0033** and **+0.0001**.
**Supports:** α non-identifiability and negligible contribution.
**Mistake to avoid:** reading `best_AA` as a trained-model result — it is a post-hoc grid maximum.

### `Thesis_Table_06_Rarity_Mechanism_Correlations_v2.csv` — **MAIN, Ch8**
**Purpose:** Spearman correlations for the mechanism analysis.
**Key columns:** `spearman_rarity_vs_CE_error`, `spearman_rarity_vs_posthoc_standard_LA_gain`,
`spearman_rarity_vs_adaptive_alpha_gain`, `p_values_reported` (= False).
**Key values:** **+0.4061** vs **−0.3714**.
**Supports:** rarity ≠ difficulty.
**Mistake to avoid:** adding p-values. `p_values_reported: False` is a deliberate, frozen decision.

### `Thesis_Table_07_Dataset_Overview_v2.csv` — **MAIN, Ch3**
**Purpose:** scene overview and the Tangdaowan exclusion reason.
**Key columns:** `official_train_mask_total/min/max/IR`, `used_in_experiment_B`,
`reason_if_excluded`.
**Mistake to avoid:** quoting the official IR (71.0 / 28.5) as the Experiment-B imbalance. Pair it
with Table 08.

### `Thesis_Table_08_TrainingCount_Reconciliation_v1.csv` — **APPENDIX (or Ch3)**
**Purpose:** all three count concepts side by side, per class.
**Key columns:** `official_train_mask_count`, `nb01_pixel_random_70pct_train_count`,
`expB_post_guard_train_count`, `expB_guard_excluded_count`.
**Key values:** Pingan class 5: 2,076 → 1,453 → **85**.
**Supports:** the guard band raises effective imbalance to 397.4× / 264.3×.
**Mistake to avoid:** treating the post-guard set as a subset of the 70% split. It is a different
spatial partition — some Qingyun classes have slightly *more* post-guard pixels.

### `Thesis_Table_09_OfficialTest_Confirmation_v1.csv` — **MAIN, Ch10**
**Purpose:** the one-time official-test result per seed, with checkpoint hashes.
**Key columns:** `test_AA`, `test_OA`, `test_MacroF1`, `test_Kappa`, `n_test_pixels`,
`checkpoint_sha256`.
**Key values:** Pingan AA 0.69617 ± 0.00390; Qingyun AA 0.73738 ± 0.01448.
**Mistake to avoid — the big one:** there is **no CE row and no delta column**, by design. Do not
form a test-set comparison against CE.

### `Table_Paired_Recognition_Deltas_v3.csv` + `_MeanStd_v3.csv` — **MAIN, Ch8**
**Purpose:** per-seed post-hoc deltas with unambiguous names.
**Key columns:** `comparison_object`, `posthoc_selected_LA_tau`, `posthoc_standard_LA_minus_CE_AA`,
`posthoc_LTLC_minus_standard_LA_AA`.
**Key values:** Qingyun seed 3407 is **all zeros** — because `posthoc_selected_LA_tau = 0`.
**Supports:** LTLC collapsing onto the baseline in 4 of 6 runs.
**Mistake to avoid:** calling the zeros stale or missing. They are an **exact identity**: τ = 0 makes
the transform the identity. v3 is numerically identical to v2, which was verified correct.

---

# PART 29 — FINAL QUALITY CHECK

Checked against `FINAL_CLAIM_BOUNDARIES_v1.md`, `FINAL_GOVERNANCE_AUDIT_v2.md`,
`FINAL_TABLE_QA_v1.md`, `FINAL_FIGURE_QA_v1.md`, `BLACK_BOOK_PREWRITING_CHECKLIST_v1.md`.

| Prohibited error | Status |
|---|---|
| Claimed LTLC robust recognition improvement | **No** — Parts 12, 14, 19 all state the opposite |
| Confused TRAINED LA-LOSS with POST-HOC STANDARD LA | **No** — separated in Part 6 with a comparison table, and labelled at every use |
| Confused official counts with Experiment-B post-guard counts | **No** — three concepts named in Parts 3, 7, 9; both IRs always paired |
| Used Experiment A as primary evidence | **No** — Part 8 frames it as motivation only, explicitly barred as method evidence |
| Claimed Tangdaowan Experiment-B results | **No** — Part 3 states no such result exists |
| Claimed conventional statistical significance | **No** — Part 17; "suggestive, not confirmatory" throughout |
| Claimed official-test improvement over CE | **No** — Part 18 states no Experiment-B CE test result exists |
| Claimed the test was never opened | **No** — Part 18 documents both openings |
| Claimed calibration improved recognition | **No** — Part 16 explains order-preservation |

Additional discipline applied: the paired-delta zeros are presented as an exact τ = 0 identity, not
as stale data; Fig N3's independent colour scales and Fig N2's differing y-axis ranges are stated
wherever those figures appear; Fig N5 is excluded throughout; and the one source conflict found
(handoff §15/§23 vs Addendum A §A.3) is reported at the top rather than silently reconciled.

---

```
SOURCE-GROUNDED:                              YES
SCIENTIFIC CLAIM BOUNDARIES RESPECTED:        YES
TRAINED LA-LOSS VS POST-HOC LA DISTINGUISHED: YES
EXPERIMENT A VS B DISTINGUISHED:              YES
VALIDATION VS OFFICIAL TEST DISTINGUISHED:    YES
READY FOR SUPERVISOR/GROUPMATE EXPLANATION:   YES
```
