# FINAL BLACK BOOK READINESS AUDIT v1

**Date:** 2026-08-27 · **Project:** CSE498R — LTLC, long-tail correction for hyperspectral
classification on the QUH benchmark.

Scores are deliberately uninflated. Where an axis is weak it is scored weak, even though the
weakness was handled honestly.

---

## Scorecard

| Axis | Score | Justification |
|---|:--:|---|
| Research problem | **8**/10 | Clear, well-motivated question: does frequency-based long-tail correction help HSI classification once patch-overlap leakage is removed? Sharpened by the discovery that leakage inflated Experiment A to ~99.99%. Not a novel problem framing, but a genuinely important one. |
| Dataset justification | **8**/10 | Three QUH scenes characterised in depth; Tangdaowan excluded on a **pre-declared, frozen geometric feasibility** ground (class 14 infeasible under 9×9 patch geometry) rather than post-hoc convenience. Loses points only because the exclusion narrows generalization. |
| Preprocessing rigor | **9**/10 | PCA (`covariance_eigh`, EVR ≥ 0.9998), row-wise min-max, cached frozen cubes, per-scene patch geometry, lazy zero-padded extraction. Cube files verified **byte-identical** to their frozen hashes in this audit. |
| Baseline quality | **7**/10 | Five methods (CE, Focal, LDAM-DRW, Balanced Softmax, LA-loss) × 3 seeds × tuning grids = 36 frozen runs. Competent and standard, but no recent long-tail method (e.g. decoupled training, LADE, PaCo) and a single backbone. |
| Experimental design | **9**/10 | Protocol frozen before split creation, model construction, inference and training, with those facts recorded as machine-checkable flags. 36/36 completion with a passing closing audit. Pre-registration quality is well above typical coursework. |
| Spatial validation rigor | **9**/10 | Guard-band exclusion, cluster-subset spatial partitioning, anti-overfitting flags (no best-of-multiple-splits, no post-hoc buffer changes). Zero train/val and train/test overlap independently re-verified. A genuine strength of the thesis. |
| Reproducibility | **8**/10 | Content hashes throughout, a 36-row run ledger, migration manifests, recovered environment records. The official-test split container question is now **fully resolved** (Category A benign re-serialization; array contents proven element-identical to Notebook 03's independently stored copy, and both hash epochs attested in the project's own artifacts). Remaining deductions: the significance JSON had been lost and needed regeneration; the Day-1 figures were never persisted to disk; two container-hash epochs exist for one logical filename, so container-level provenance for those two files must be cited via canonical array hashes. |
| Statistical reliability | **4**/10 | **The weakest axis.** n = 3 seeds. The exact sign-flip test cannot go below p = 0.25; the bootstrap over three points yields only 10 distinct means and its 95% endpoints are provably just the observed min/max. Nothing can be called significant. Handled with unusual honesty — but honesty about thin evidence does not make the evidence thick. |
| Proposed-method originality | **4**/10 | LTLC is a modest reparameterisation of logit adjustment (rarity-scaled τ). Revision R1 selected β = 0 on both scenes and is therefore **exactly identical** to Standard LA. The intended novelty did not survive its own test. |
| Mechanism analysis | **8**/10 | Genuinely strong and the intellectual core of the work: rarity-vs-difficulty correlation with opposite signs across scenes, the (τ, α) landscape showing a wide near-optimal plateau, the β profile, and the isolated-α contribution. Explains *why* the method fails, not merely *that* it fails. |
| Scientific interpretation | **9**/10 | Exemplary. Claim boundaries were frozen in machine-readable artifacts before writing; a null result is reported as a null result; calibration is explicitly kept separate from recognition. |
| Generalization evidence | **4**/10 | Two scenes, one backbone, three seeds, one sensor family. No cross-sensor or cross-backbone evidence. The honest scope is narrow. |
| Figure quality | **8**/10 | After this pass: 8 of 10 figures grade A/B; the Fig N5 label-overlap defect is fixed by a redesign; the CI-led forest plot is replaced by a per-seed design. Minor polish outstanding (Fig N3 independent colour scales, Fig N2 differing y-scales — both caption-fixable). |
| Table quality | **8**/10 | After this pass: 11 clean versioned tables, count semantics disambiguated across three concepts, paired-delta tables verified and clarified. Two label renames remain to apply at typesetting. |
| Claim discipline | **9**/10 | Outstanding. Frozen `may_claim_*` flags, an explicit prohibited-claims list, and a volunteered disclosure of the governance inconsistency rather than a concealment of it. |
| Thesis readiness | **8**/10 | Every scientific input exists, is verified, and is documented. What remains is writing plus small typesetting-time actions. |

---

## OVERALL CSE498R RESEARCH RATING: **7.5 / 10**

**Reading of that number.** This is a well-executed, methodologically rigorous, honestly
reported study whose headline finding is a **null result**. Process quality sits at the 9
level; novelty, statistical power and generalization sit at the 4 level. The rating is the
honest resolution of that split, not a compromise.

The project's real contribution is **not** a working method. It is (a) a demonstration that
conventional HSI validation can be catastrophically leaky — ~99.99% collapsing to 74–88%
— and (b) leakage-controlled evidence that class frequency alone is insufficient to
characterise hyperspectral class difficulty. Framed that way, it is a defensible and useful
piece of work. Framed as "we propose LTLC and it works", it would not survive examination.

**Do not inflate this in the write-up.** The strongest posture available is complete candour
about the null result, backed by an audit trail that is unusually strong for a project at
this level.

---

## Classification

> ## C. READY FOR BLACK BOOK WRITING

Not D (repository may be frozen) because a small number of non-scientific actions remain
outstanding — see below. None of them blocks writing, and none can change a scientific
conclusion.

---

## Remaining actions (all non-scientific)

| # | Action | Where | Blocking? |
|---|---|---|---|
| 1 | Apply two label renames (`LA + Global TS` → `POST-HOC STANDARD LA + Global TS`; `spearman_rarity_vs_LA_gain` → `..._posthoc_standard_LA_gain`) | Tables 03, 06 | No — typesetting |
| 2 | Add the mandated figure/table captions (count concept; POST-HOC vs TRAINED; validation-vs-test) | all chapters | No — writing |
| 3 | Fig N3: state independent colour scales, or regenerate shared | Mechanism chapter | No |
| 4 | Fig N2: state the differing y-axis scales | Appendix | No |
| 5 | Insert the governance paragraph verbatim | Protocol chapter | **Yes, for submission** |
| 6 | Cite **canonical array hashes** (not container hashes) for the two official-test split files, and note the two attested container epochs | Reproducibility appendix | No |

---

## Did any QA finding materially change the scientific conclusion?

**No.** Two findings changed *documentation*, and one strengthened an existing claim:

1. **The "stale paired-delta" claim was itself wrong.** The Qingyun seed-3407 zeros are an
   exact identity (τ = 0 selected ⇒ the LA transform is the identity). Correcting this
   **reinforces** the null result: the zeros are genuine collapses of LTLC onto the baseline,
   not missing data. Had the proposed "+0.004020 fix" been applied, it would have injected an
   error into a correct table.
2. **A third training-count concept exists**, and the guard band raises effective imbalance
   from 71×→397× (Pingan) and 28.5×→264× (Qingyun). This is new, substantive context that
   *strengthens* the framing — Experiment B is harder than its nominal IR suggests — but it
   changes no result.
3. **The bootstrap CI is vacuous at n = 3** (endpoints provably equal the observed min/max).
   This weakens how the statistics may be *described*, not what they are. No number changed.

The headline conclusion stands exactly as before: **standard long-tail prior correction can
help, especially on Pingan, but the additional frequency-only rarity-adaptive LTLC component
provides no robust recognition benefit.**
