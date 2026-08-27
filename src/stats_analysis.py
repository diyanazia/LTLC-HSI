"""
Formal significance testing on Experiment B (Notebook 06A) validation results.
Source: LTLC_Notebook06A_ExperimentB_36of36_FINAL_RUN_LEDGER_v1.csv (36 rows, downloaded verbatim from Drive).
No GPU / no new training used — this is a re-analysis of already-logged per-seed AA values.
"""
import csv
import itertools
import json
import math
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy import stats

# Repository-relative resolution (public portable copy).
REPO_ROOT = Path(__file__).resolve().parent.parent
LEDGER = REPO_ROOT / "experiments" / "LTLC_Notebook06A_ExperimentB_36of36_FINAL_RUN_LEDGER_v1.csv"
OUT_DIR = REPO_ROOT / "reproducibility"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# The exact "selected" (winning) configuration per method/dataset, as recorded in
# LTLC_Notebook06A_ExperimentB_VALIDATION_SUMMARY_TABLE_v1.md (frozen at seed 42, before
# looking at seeds 123/3407). The candidate grid value is encoded in relative_path
# (e.g. ".../focal/pingan/gamma1/seed42/...", ".../ldam_drw/qingyun/c0p2500/seed42/...")
# rather than in the tau/gamma/C columns, which this ledger only populates for la_loss.
SELECTED_TOKEN = {
    ("Pingan", "balanced_softmax"): None,          # no tuning grid
    ("Pingan", "ce"): None,
    ("Pingan", "focal"): "gamma1",       # gamma = 1.0
    ("Pingan", "la_loss"): "tau1p0",     # tau = 1.0
    ("Pingan", "ldam_drw"): "c0p5000",   # C = 0.5
    ("Qingyun", "balanced_softmax"): None,
    ("Qingyun", "ce"): None,
    ("Qingyun", "focal"): "gamma1",      # gamma = 1.0
    ("Qingyun", "la_loss"): "tau0p5",    # tau = 0.5
    ("Qingyun", "ldam_drw"): "c0p2500",  # C = 0.25
}

rows = list(csv.DictReader(open(LEDGER, encoding="utf-8")))

# Build {(dataset, method): {seed: AA}} using only the selected configuration.
data = defaultdict(dict)
for r in rows:
    key = (r["dataset"], r["method_dir"])
    token = SELECTED_TOKEN[key]
    if token is not None and token not in r["relative_path"]:
        continue  # this is a losing tuning candidate, not the selected config
    seed = int(r["seed"])
    data[key][seed] = float(r["best_AA"])

# Sanity: every (dataset, method) must have exactly 3 seeds
for key, d in data.items():
    assert len(d) == 3, f"{key} has {len(d)} seeds: {d}"

SEEDS = [42, 123, 3407]
DATASETS = ["Pingan", "Qingyun"]
METHOD_LABELS = {
    "ce": "CE", "focal": "Focal", "ldam_drw": "LDAM-DRW",
    "balanced_softmax": "Balanced Softmax", "la_loss": "LA-loss",
}

results = []
for dataset in DATASETS:
    ce = np.array([data[(dataset, "ce")][s] for s in SEEDS])
    for method in ["focal", "ldam_drw", "balanced_softmax", "la_loss"]:
        m = np.array([data[(dataset, method)][s] for s in SEEDS])
        diff = m - ce  # paired per-seed delta

        # Paired t-test (parametric; n=3 -> 2 d.f., very low power, reported for completeness)
        t_stat, t_p = stats.ttest_rel(m, ce)

        # Exact Wilcoxon signed-rank test is degenerate at n=3 with no ties handling worth
        # reporting; with n=3 the sign test / exact permutation test is the honest choice.
        # Exact sign-flip permutation test on the paired differences (2^3 = 8 possible sign
        # patterns -> minimum achievable two-sided p-value is 2/8 = 0.25 unless diff has a
        # zero, so ANY result here is necessarily underpowered -- report the exact p-value
        # and say so explicitly rather than imply the test had real power.
        obs_mean = diff.mean()
        signs = list(itertools.product([1, -1], repeat=len(diff)))
        perm_means = [np.mean(diff * np.array(s)) for s in signs]
        p_perm = float(np.mean([abs(pm) >= abs(obs_mean) - 1e-12 for pm in perm_means]))

        # Paired bootstrap 95% CI on the mean difference (resample the 3 seeds with
        # replacement, 20,000 resamples). With n=3 this CI is wide and should be reported
        # as illustrative, not as proof of a tight effect.
        rng = np.random.default_rng(20260826)
        boot = rng.choice(diff, size=(20000, len(diff)), replace=True).mean(axis=1)
        ci_lo, ci_hi = np.percentile(boot, [2.5, 97.5])

        results.append({
            "dataset": dataset,
            "method": METHOD_LABELS[method],
            "seed_values_method": m.tolist(),
            "seed_values_CE": ce.tolist(),
            "mean_delta_AA": float(obs_mean),
            "sd_delta_AA": float(diff.std(ddof=1)),
            "paired_t_stat": float(t_stat),
            "paired_t_pvalue": float(t_p),
            "exact_sign_permutation_pvalue": p_perm,
            "bootstrap_95CI_low": float(ci_lo),
            "bootstrap_95CI_high": float(ci_hi),
            "ci_excludes_zero": bool(ci_lo > 0 or ci_hi < 0),
        })

print(json.dumps(results, indent=2))
with open(OUT_DIR / "significance_test_results.json", "w") as f:
    json.dump(results, f, indent=2)

# Also write a clean, thesis-ready CSV
import pandas as pd
df = pd.DataFrame(results)[[
    "dataset", "method", "mean_delta_AA", "sd_delta_AA",
    "paired_t_pvalue", "exact_sign_permutation_pvalue",
    "bootstrap_95CI_low", "bootstrap_95CI_high", "ci_excludes_zero",
]].round(4)
df.to_csv(OUT_DIR / "Table_Significance_Tests_vs_CE.csv", index=False)
print(df.to_string(index=False))
