# Experiment B — Novelty-Strengthened Thesis Interpretation

## Recommended contribution framing

The strongest defensible contribution is not a claim that rarity-adaptive LTLC universally improves hyperspectral classification.

Instead, Experiment B provides a leakage-controlled robustness study of frequency-based long-tail correction under spatially disjoint hyperspectral validation.

The study makes four defensible contributions:

1. It evaluates long-tail correction under strict spatially separated train/validation construction rather than relying only on conventional overlap-prone spectral-spatial validation.

2. It separates the effect of ordinary training-prior correction from the additional rarity-adaptive term.

3. It demonstrates that the additional rarity coefficient is not robustly identifiable across datasets and seeds: Original LTLC selected a nonzero alpha in 2/6 runs, while R1 selected beta=0 for both datasets and therefore collapsed exactly to Standard Logit Adjustment.

4. It separates recognition from probability calibration. Temperature calibration substantially improves NLL, but does not alter predictions and does not consistently improve tail-class calibration.

## Mechanism analysis

The accompanying per-class analysis tests whether training-frequency rarity corresponds to empirical classification difficulty and whether rarer classes obtain larger accuracy gains from the adaptive alpha term.

The adaptive-alpha comparison is intentionally made against Standard LA using the SAME tau value. This isolates the effect of alpha rather than confounding it with a different global adjustment strength.

Spearman correlations are reported descriptively only. No p-value significance claims are made because there are few classes and hyperspectral pixels are spatially dependent.

## Parameter identifiability

The full pre-existing LTLC validation grid is analyzed without any additional tuning.

For each dataset and seed, the analysis reports:
- the best validation AA,
- the best AA available when alpha=0,
- the incremental best-AA contribution of allowing alpha>0,
- and the number of candidate settings lying within 0.1 and 0.25 percentage points of the optimum.

A wide near-optimal region or inconsistent alpha selections should be interpreted as evidence of parameter instability rather than evidence for a precise rarity-dependent correction.

## R1 mechanism

R1 is examined through the already-evaluated seed-42 beta profile. No additional beta values are introduced.

Both datasets selected beta=0 in the frozen R1 protocol. Thus the robustness result provides direct evidence that the additional rarity-specific correction was not required once ordinary Logit Adjustment had been accounted for.

## Calibration interpretation

LTLC Full reached the allowed a bound in 5/6 fits and the allowed b bound in 5/6 fits.

This repeated boundary saturation is a limitation and evidence that the fitted rarity-conditioned temperature should not be interpreted as a stable generalizable parameter.

Calibration improvements are therefore reported as probability-quality improvements only, not recognition improvements.

## Final thesis claim

A scientifically defensible conclusion is:

> Under spatially disjoint, leakage-controlled validation on QUH-Pingan and QUH-Qingyun, standard training-prior Logit Adjustment improved class-balanced recognition relative to Cross-Entropy, but adding a frequency-only rarity-adaptive correction did not produce a stable additional recognition advantage. The adaptive coefficients collapsed or varied across seeds, indicating that class frequency alone is insufficient to characterize hyperspectral class difficulty. Post-hoc temperature calibration substantially improved overall probabilistic metrics such as NLL, but these improvements preserved hard predictions and did not consistently improve tail-class calibration.

## Future method direction

A stronger future extension should test a difficulty-aware rather than frequency-only correction.

A suitable future hypothesis is to combine the training prior with a training-only class-difficulty signal such as:
- spectral/feature-space class separation,
- intra-class dispersion,
- classification margin,
- representation effective rank,
- or another pre-declared class-geometry statistic.

That method must be frozen BEFORE evaluation on an independent validation protocol. It must not be tuned now using the already-consumed Experiment-B validation sets.

## Official-test boundary

Robust LTLC recognition signal: FALSE

Further redesign on the same validation sets: NOT ALLOWED

Official test may be opened: FALSE

Official test status: SEALED
