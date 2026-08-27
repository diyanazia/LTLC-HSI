# STATISTICAL ANALYSIS VERIFICATION v1

**Date:** 2026-08-27
**Regenerated:** `significance_test_results_v1.json` (the original output JSON was absent
from the repository; only the script and the derived CSV survived).

---

## 1. Script audit — `Day1_Improvements_2026-08-26/scripts/stats_analysis.py`

| Question | Finding |
|---|---|
| **What values does it compare?** | `best_AA` from the Experiment-B 36-run ledger — i.e. **TRAINED method vs TRAINED CE**, validation AA. It is *not* the post-hoc logit comparison. |
| **Is pairing seed-by-seed?** | **Yes, correctly.** `ce` and `m` are both indexed over `SEEDS = [42,123,3407]` in the same order; `diff = m − ce` is a genuine paired difference. |
| **Are the selected configs the frozen ones?** | Yes. Tokens `gamma1`, `tau1p0` (Pingan), `tau0p5` (Qingyun), `c0p5000`, `c0p2500` match the frozen validation summary and the closing audit (`la_loss` selected τ: Pingan 1.0, Qingyun 0.5). Selection is unambiguous — the script asserts exactly 3 seeds per (dataset, method) and the assert passes for all 10 pairs. |
| **Bootstrap implementation** | `rng.choice(diff, size=(20000,3), replace=True).mean(axis=1)`, percentile CI at 2.5/97.5. Mechanically correct **but see §3**. The RNG is re-seeded inside the loop, so every method uses the same resample pattern — reproducible, though it means the CIs are not independent across rows. |
| **Exact sign-flip enumeration** | `itertools.product([1,-1], repeat=3)` → all 8 sign patterns; `p = mean(|perm_mean| ≥ |obs_mean| − 1e-12)`. **Correct exact test.** Because the observed pattern and its exact negation always qualify, `p ≥ 2/8 = 0.25` is a hard floor. |
| **Multiplicity** | 8 comparisons (2 datasets × 4 methods), **no correction applied**. |

**Distinction to preserve:** this analysis is **TRAINED LA-LOSS vs TRAINED CE**. The
Notebook 06B paired-delta tables are **POST-HOC STANDARD LA vs CE**. Never merge or compare
the two.

---

## 2. Recomputation from the authoritative ledger

`Thesis_Table_02_Significance_Tests_vs_CE.csv` **fully reproduced** — every mean delta,
sign-flip p, bootstrap bound and `ci_excludes_zero` flag matches.

| Dataset | Method | seed42 | seed123 | seed3407 | mean Δ | SD | sign-flip p | boot95 lo | boot95 hi |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Pingan | Focal | −0.0190 | 0.0128 | 0.0054 | −0.0003 | 0.0167 | 1.00 | −0.0190 | 0.0128 |
| Pingan | LDAM-DRW | −0.0320 | −0.0392 | −0.0337 | −0.0350 | 0.0038 | 0.25 | −0.0392 | −0.0320 |
| Pingan | Balanced Softmax | 0.0087 | 0.0625 | 0.0194 | 0.0302 | 0.0285 | 0.25 | 0.0087 | 0.0625 |
| Pingan | LA-loss | 0.0059 | 0.0333 | 0.0279 | 0.0224 | 0.0145 | 0.25 | 0.0059 | 0.0333 |
| Qingyun | Focal | 0.0011 | 0.0095 | −0.0113 | −0.0002 | 0.0105 | 1.00 | −0.0113 | 0.0095 |
| Qingyun | LDAM-DRW | −0.0086 | −0.0058 | −0.0013 | −0.0052 | 0.0037 | 0.25 | −0.0086 | −0.0013 |
| Qingyun | Balanced Softmax | −0.0145 | 0.0080 | 0.0050 | −0.0005 | 0.0122 | 1.00 | −0.0145 | 0.0080 |
| Qingyun | LA-loss | 0.0003 | 0.0126 | 0.0040 | 0.0057 | 0.0063 | 0.25 | 0.0003 | 0.0126 |

(Per-seed deltas rounded to 4 dp; full precision in the regenerated JSON.)

**Look at the last two columns against the first three.** In **all 8 rows** the bootstrap
"95% CI" endpoints are exactly the **minimum and maximum of the three observed per-seed
deltas** — verified programmatically to within 1e-12. The interval adds no information
whatsoever beyond the range of the three numbers already shown.

---

## 3. The inferential limitation, stated precisely

**Exact sign-flip test.** With n = 3 paired observations there are 2³ = 8 possible sign
patterns. The observed pattern and its negation always have |mean| ≥ |observed mean|, so the
smallest attainable two-sided p-value is **2/8 = 0.25**. Every "significant-looking" row in
this table sits exactly at that floor. **p = 0.25 here means "the most extreme result this
test can possibly produce", not "not significant" — and it can never reach 0.05.** The test
is structurally incapable of conventional significance at n = 3.

**Bootstrap CI — a stronger criticism than "wide".** With n = 3, resampling 3 values with
replacement yields only 3³ = 27 ordered resamples and **just 10 distinct possible mean
values**. Verified empirically: 20,000 bootstrap draws produced exactly **10 distinct means**
for every one of the 8 comparisons.

Worse, the CI is provably vacuous here: **in all 8 rows the 2.5th/97.5th percentile endpoints
equal exactly the minimum and maximum of the three observed deltas** (verified to within
1e-12). The reason is structural — with n = 3, the resample "all three draws identical" has
probability 1/9 for each of the three values, so the extreme resample means (each equal to a
single observed value) sit well inside the 2.5%/97.5% tails. The percentile CI is therefore
**not an estimate of sampling uncertainty at all**; it is an arithmetically guaranteed
restatement of the observed range.

The "20,000 resamples" figure conveys false precision. **Recommendation: do not lead with the
bootstrap CI, and never convert "CI excludes zero" into a significance claim.**

**Paired t-test.** Reported by the script for completeness at 2 d.f. Pingan LDAM-DRW yields
p = 0.0039, which will read as "significant" to a casual reader. With n = 3, no normality
check, and 8 uncorrected comparisons, this is not trustworthy. **Recommendation: omit the
t-test from the thesis entirely**, or report it only in an appendix with this caveat.

---

## 4. Final recommendation per statistical output

| Output | Recommendation | Note |
|---|---|---|
| **Per-seed paired deltas** | **USE** — make this the primary reporting form | Fully transparent; lets the reader see all the evidence |
| **Mean ± SD of paired deltas** | **USE** — primary summary | Honest, standard, no inferential over-claim |
| **Exact sign-flip p-value** | **USE WITH CAVEAT** | Only if the 0.25 floor is stated in the same sentence |
| **Bootstrap 95% CI** | **USE WITH CAVEAT** — descriptive/supporting only | Must carry: "Bootstrap intervals are reported descriptively because only three random seeds are available." Never phrase as significance |
| **`ci_excludes_zero` flag** | **DO NOT USE** as a significance criterion | May be retained as a descriptive consistency-of-sign indicator, explicitly labelled as such |
| **Paired t-test p-value** | **DO NOT USE** in the main text | n = 3, 2 d.f., no multiplicity control; p = 0.0039 would mislead |
| **Any multiplicity-corrected claim** | **DO NOT USE** | Not computed, and not meaningful at this n |

---

## 5. Approved thesis wording

> Observed paired improvements are **suggestive rather than confirmatory** because only three
> random seeds were evaluated. With n = 3, an exact sign-flip test has a minimum attainable
> two-sided p-value of 0.25, and a bootstrap over three observations can take only ten
> distinct mean values; bootstrap intervals are therefore reported descriptively, not as
> inferential guarantees.

Consistent-sign observations that may be reported descriptively (all three seeds agreeing in
direction): Pingan Balanced Softmax (+3.0 pp mean), Pingan LA-loss (+2.2 pp), Pingan LDAM-DRW
(−3.5 pp), Qingyun LA-loss (+0.6 pp), Qingyun LDAM-DRW (−0.5 pp). Focal on both datasets and
Balanced Softmax on Qingyun show **sign changes across seeds** and should be reported as
indistinguishable from CE.

---

## 6. Artifacts

- `LTLC/final_qa_2026-08-27/significance_test_results_v1.json` — regenerated, now including
  `per_seed_delta`, `comparison_object` and `distinct_bootstrap_means` fields.
- `LTLC/results/final_thesis_tables_v1/Thesis_Table_02_PerSeed_Deltas_vs_CE_v1.csv` — per-seed
  deltas first, bootstrap columns renamed `*_descriptive`, `inferential_status` column added.
- `LTLC/results/final_thesis_figures_v1/Fig_PerSeed_Delta_vs_CE.png` — replaces the
  CI-led forest plot with a per-seed-led design.
- Original `Thesis_Table_02_Significance_Tests_vs_CE.csv` retained unchanged.
