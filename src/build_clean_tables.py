"""
Clean, thesis-ready reformatting of the project's existing Table_*.csv exports.
Source content pasted verbatim from the project Drive folder
on 2026-08-26 — not re-derived,
not re-computed from scratch (except where explicitly marked "cross-checked against
run_ledger.csv", the frozen, SHA-256-hashed source of truth for Experiment B).

Outputs -> <repo>/results/tables/Thesis_Table_*.csv (+ one .md flag doc)
"""
import io
from pathlib import Path

import pandas as pd

# Repository-relative resolution (public portable copy).
REPO_ROOT = Path(__file__).resolve().parent.parent
OUT = REPO_ROOT / "results" / "tables"
OUT.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Table 1: Experiment B master result table (from
# LTLC_Notebook06A_ExperimentB_VALIDATION_SUMMARY_TABLE_v1.md), method names
# normalized, columns split into separate mean/SD, rounded to 4 dp.
# ---------------------------------------------------------------------------
master_raw = """dataset,rank,method,config,AA_mean,AA_sd,MacroF1_mean,MacroF1_sd,OA_mean,OA_sd,Kappa_mean,Kappa_sd,delta_AA_vs_CE
Pingan,1,Balanced Softmax,training_counts,0.769507,0.006274,0.713225,0.043342,0.895196,0.009722,0.843670,0.013927,0.030178
Pingan,2,LA-loss,tau=1,0.761707,0.013613,0.698220,0.022144,0.886202,0.009409,0.830633,0.013549,0.022378
Pingan,3,CE,CrossEntropy,0.739328,0.022255,0.699395,0.029926,0.882075,0.013073,0.823502,0.019112,0.000000
Pingan,4,Focal,gamma=1,0.739056,0.012653,0.704205,0.040970,0.891566,0.006192,0.837820,0.008774,-0.000272
Pingan,5,LDAM-DRW,C=0.5,0.704360,0.026028,0.704443,0.026532,0.884918,0.007106,0.827364,0.010436,-0.034969
Qingyun,1,LA-loss,tau=0.5,0.759483,0.007607,0.706771,0.008198,0.750848,0.008455,0.677271,0.010433,0.005654
Qingyun,2,CE,CrossEntropy,0.753829,0.008924,0.699573,0.004631,0.742638,0.004959,0.664513,0.007436,0.000000
Qingyun,3,Focal,gamma=1,0.753580,0.015953,0.704217,0.012406,0.752283,0.006229,0.677432,0.006858,-0.000249
Qingyun,4,Balanced Softmax,training_counts,0.753308,0.005003,0.680293,0.016507,0.726823,0.020194,0.649737,0.024470,-0.000521
Qingyun,5,LDAM-DRW,C=0.25,0.748608,0.005761,0.702640,0.002838,0.742463,0.007927,0.663239,0.009145,-0.005221
"""
df1 = pd.read_csv(io.StringIO(master_raw))
num_cols = [c for c in df1.columns if c not in ("dataset", "rank", "method", "config")]
df1[num_cols] = df1[num_cols].round(4)
df1.to_csv(f"{OUT}/Thesis_Table_01_ExperimentB_Master_Results.csv", index=False)

# ---------------------------------------------------------------------------
# Table 2: significance tests -- already built by stats_analysis.py, just
# re-round/re-normalize column order and method spelling for consistency.
# ---------------------------------------------------------------------------
df2 = pd.read_csv(f"{OUT}/Table_Significance_Tests_vs_CE.csv")
df2 = df2.rename(columns={
    "mean_delta_AA": "delta_AA_mean", "sd_delta_AA": "delta_AA_sd",
    "paired_t_pvalue": "paired_t_p", "exact_sign_permutation_pvalue": "sign_perm_p",
    "bootstrap_95CI_low": "boot95_lo", "bootstrap_95CI_high": "boot95_hi",
})
df2.to_csv(f"{OUT}/Thesis_Table_02_Significance_Tests_vs_CE.csv", index=False)

# ---------------------------------------------------------------------------
# Table 3: calibration trade-off (verbatim from Table_Calibration_Tradeoff_v2.csv,
# confirms the numbers already used in Fig_Calibration_Tradeoff_Redesigned.png),
# renamed methods, rounded to 4 dp.
# ---------------------------------------------------------------------------
calib_raw = """dataset,method,NLL_mean,NLL_sd,ECE_mean,ECE_sd,TailECE_mean,TailECE_sd,Brier_mean,Brier_sd
Pingan,Global Temp. Scaling,0.6701,0.1334,0.0456,0.0096,0.2334,0.1234,0.1857,0.0103
Pingan,LA + Global TS,0.6888,0.1390,0.0391,0.0126,0.2361,0.1157,0.1895,0.0140
Pingan,LTLC (rarity-conditioned TS),0.6390,0.1095,0.0682,0.0290,0.5936,0.1016,0.2072,0.0113
Pingan,Standard LA (uncalibrated),3.7333,0.9734,0.1038,0.0167,0.1505,0.0310,0.2226,0.0301
Qingyun,Global Temp. Scaling,0.9809,0.1121,0.0490,0.0178,0.1523,0.0815,0.3865,0.0053
Qingyun,LA + Global TS,1.0272,0.1278,0.0540,0.0138,0.1560,0.0577,0.4009,0.0203
Qingyun,LTLC (rarity-conditioned TS),0.9652,0.0921,0.0635,0.0188,0.5196,0.0482,0.3895,0.0126
Qingyun,Standard LA (uncalibrated),4.7366,1.7785,0.2368,0.0117,0.2069,0.0783,0.4951,0.0245
"""
df3 = pd.read_csv(io.StringIO(calib_raw))
df3.to_csv(f"{OUT}/Thesis_Table_03_Calibration_Tradeoff.csv", index=False)

# ---------------------------------------------------------------------------
# Table 4: per-class training count / rarity / mechanism summary, combined
# across Pingan + Qingyun, from Table_ClassLevel_Mechanism_Summary_v2.csv.
# Also used to derive the combined dataset-statistics table below.
# ---------------------------------------------------------------------------
mech_raw = """dataset,class_id,train_count,rarity,ce_accuracy_mean,ce_error_mean,la_minus_ce_mean,adaptive_alpha_gain_mean
Pingan,1,3322,0.3875,0.7392,0.2608,-0.0263,-0.0231
Pingan,2,33783,0.0000,0.9948,0.0052,-0.0031,-0.0012
Pingan,3,219,0.8419,0.8048,0.1952,0.1062,0.0226
Pingan,4,6229,0.2825,0.1366,0.8634,-0.0283,-0.0011
Pingan,5,85,1.0000,0.7428,0.2572,0.0472,0.0150
Pingan,6,683,0.6518,0.9489,0.0511,0.0118,-0.0047
Pingan,7,110,0.9569,0.7675,0.2325,0.0413,0.0079
Pingan,8,4485,0.3374,0.8058,0.1942,-0.0228,-0.0215
Pingan,9,440,0.7253,0.4918,0.5082,0.0369,0.0232
Pingan,10,16354,0.1212,0.9612,0.0388,-0.0075,-0.0032
Qingyun,1,19556,0.0000,0.7555,0.2445,-0.0102,-0.0006
Qingyun,2,11807,0.0905,0.8644,0.1356,-0.0136,-0.0003
Qingyun,3,967,0.5392,0.5521,0.4479,0.0517,0.0032
Qingyun,4,74,1.0000,0.9977,0.0023,0.0023,0.0000
Qingyun,5,15220,0.0449,0.5151,0.4849,-0.0006,-0.0001
Qingyun,6,15555,0.0410,0.8383,0.1617,-0.0144,-0.0006
"""
df4 = pd.read_csv(io.StringIO(mech_raw))
df4 = df4.rename(columns={"train_count": "expB_split_train_count"})
df4.to_csv(f"{OUT}/Thesis_Table_04_PerClass_Frequency_and_Mechanism.csv", index=False)

# ---------------------------------------------------------------------------
# Table 5: LTLC parameter (tau/alpha) stability across seeds, from
# Table_LTLC_Parameter_Stability_v2.csv, rounded + relabeled.
# ---------------------------------------------------------------------------
stab_raw = """dataset,seed,selected_tau,selected_alpha,best_AA,best_AA_alpha0,adaptive_minus_alpha0,candidates_within_0.1pp,frac_within_0.1pp,candidates_within_0.25pp,frac_within_0.25pp
Pingan,42,0.50,0.00,0.7716,0.7716,0.0000,5,0.0794,11,0.1746
Pingan,123,2.00,0.75,0.7346,0.7313,0.0033,5,0.0794,12,0.1905
Pingan,3407,1.00,0.00,0.7617,0.7617,0.0000,11,0.1746,21,0.3333
Qingyun,42,2.00,0.00,0.7710,0.7710,0.0000,1,0.0159,6,0.0952
Qingyun,123,0.25,0.50,0.7515,0.7513,0.0001,15,0.2381,19,0.3016
Qingyun,3407,0.00,0.00,0.7467,0.7467,0.0000,12,0.1905,18,0.2857
"""
df5 = pd.read_csv(io.StringIO(stab_raw))
df5.to_csv(f"{OUT}/Thesis_Table_05_LTLC_Parameter_Stability.csv", index=False)

# ---------------------------------------------------------------------------
# Table 6: descriptive Spearman correlations (rarity vs. CE error / LA gain /
# adaptive-alpha gain). Explicitly descriptive-only, no p-values -- carried
# over from Table_Rarity_Mechanism_Descriptive_Correlations_v2.csv verbatim.
# ---------------------------------------------------------------------------
corr_raw = """dataset,spearman_rarity_vs_CE_error,spearman_rarity_vs_LA_gain,spearman_rarity_vs_adaptive_alpha_gain,p_values_reported,interpretation
Pingan,0.4061,0.7576,0.5394,False,descriptive_only_small_K_and_spatial_dependence
Qingyun,-0.3714,0.6571,0.8286,False,descriptive_only_small_K_and_spatial_dependence
"""
df6 = pd.read_csv(io.StringIO(corr_raw))
df6.to_csv(f"{OUT}/Thesis_Table_06_Rarity_Mechanism_Correlations.csv", index=False)

# ---------------------------------------------------------------------------
# Table 7 (NEW, combined): dataset statistics table.
#
# IMPORTANT -- this is deliberately built from the OFFICIAL full-dataset
# per-class counts (the same numbers used in
# Fig_ClassFrequency_LongTail_Distribution.png, whose IR annotations of
# ~71 / ~28 / ~190 are the project's own documented imbalance ratios), NOT
# from Table_ClassLevel_Mechanism_Summary_v2.csv's "train_count" column
# (used in Table 4 above). Cross-checking those two sources against each
# other during this cleanup surfaced a real discrepancy: Table 4's
# train_count for Pingan implies max/min = 33783/85 = 397x, but the
# project's own documented/official IR for Pingan is ~71x. The two numbers
# are evidently counting different things (most likely: official full
# training split vs. one seed's post-guard-band Experiment-B training
# subset), not the same quantity re-measured twice. See
# DATA_INTEGRITY_NOTES.md -- do not silently merge these two tables.
# ---------------------------------------------------------------------------
official_freq = {
    "Pingan": [4893, 57811, 835, 8899, 2076, 1409, 1398, 8312, 814, 27652],
    "Qingyun": [27817, 17951, 1380, 977, 21774, 25593],
    "Tangdaowan": [1816, 3890, 2383, 4248, 130, 2598, 989, 4486, 2148, 124, 1486, 52, 118, 62, 979, 9863],
}
rows7 = []
for ds, counts in official_freq.items():
    rows7.append({
        "dataset": ds,
        "num_classes": len(counts),
        "total_train_samples": sum(counts),
        "min_class_count": min(counts),
        "max_class_count": max(counts),
        "imbalance_ratio_max_over_min": round(max(counts) / min(counts), 1),
        "used_in_experiment_B": ds in ("Pingan", "Qingyun"),
        "reason_if_excluded": "" if ds in ("Pingan", "Qingyun")
            else "guard-band radius geometrically infeasible for rarest class (see audit Part 5)",
    })
agg = pd.DataFrame(rows7)
agg.to_csv(f"{OUT}/Thesis_Table_07_Dataset_Overview.csv", index=False)

print("Wrote:")
for p in ["01_ExperimentB_Master_Results", "02_Significance_Tests_vs_CE",
          "03_Calibration_Tradeoff", "04_PerClass_Frequency_and_Mechanism",
          "05_LTLC_Parameter_Stability", "06_Rarity_Mechanism_Correlations",
          "07_Dataset_Overview"]:
    print(" -", f"Thesis_Table_{p}.csv")
