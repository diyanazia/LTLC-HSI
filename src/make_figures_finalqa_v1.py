"""
Build the canonical figures flagged as MISSING in the supervisor audit (Part 8/9):
  1. Class-frequency / long-tail distribution bar charts (Pingan, Qingyun, Tangdaowan)
  2. Experiment A (leakage) vs Experiment B (corrected) validation-accuracy comparison
  3. Spatial train/validation split map (visualizes the zero-overlap leakage fix)
  4. Redesigned calibration trade-off figure (Fig N5 fix: declutter overlapping labels)
  5. Forest plot of the new bootstrap significance results (Part 6/7 statistics addendum)

All built from data already logged in the project's own Drive folder — no new
training, no GPU. Palette: validated categorical palette from the dataviz skill
(references/palette.md), used consistently across all figures for series identity.
"""
import json
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

plt.rcParams.update({
    "font.size": 12,
    "axes.titlesize": 14,
    "axes.labelsize": 12,
    "figure.dpi": 150,
    "savefig.dpi": 200,
    "axes.spines.top": False,
    "axes.spines.right": False,
})

# Validated categorical palette (dataviz skill, references/palette.md)
BLUE, ORANGE, AQUA, YELLOW, MAGENTA, GREEN, VIOLET, RED = (
    "#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7", "#e34948"
)
GRAY = "#9a9990"
# Repository-relative resolution (public portable copy).
REPO_ROOT = Path(__file__).resolve().parent.parent
FIGDIR = str(REPO_ROOT / "results" / "figures")
Path(FIGDIR).mkdir(parents=True, exist_ok=True)
# NOTE: split arrays are NOT redistributed in this repository (see splits/README.md).
# Point SPLIT_DIR at a local copy to regenerate the spatial split map figure.
SPLIT_DIR = REPO_ROOT / "splits"

# ---------------------------------------------------------------------------
# 1. Class-frequency / long-tail distribution bar charts
# ---------------------------------------------------------------------------
freq = {  # OFFICIAL TRAINING-MASK COUNT (not Experiment-B post-guard count)
    "Pingan": {  # class_id: (official_train_mask_count, frequency_group)
        1: (4893, "Medium"), 2: (57811, "Head"), 3: (835, "Tail"), 4: (8899, "Head"),
        5: (2076, "Medium"), 6: (1409, "Medium"), 7: (1398, "Tail"), 8: (8312, "Medium"),
        9: (814, "Tail"), 10: (27652, "Head"),
    },
    "Qingyun": {
        1: (27817, "Head"), 2: (17951, "Medium"), 3: (1380, "Tail"), 4: (977, "Tail"),
        5: (21774, "Medium"), 6: (25593, "Head"),
    },
    "Tangdaowan": {
        1: (1816, "Medium"), 2: (3890, "Head"), 3: (2383, "Medium"), 4: (4248, "Head"),
        5: (130, "Tail"), 6: (2598, "Head"), 7: (989, "Medium"), 8: (4486, "Head"),
        9: (2148, "Medium"), 10: (124, "Tail"), 11: (1486, "Medium"), 12: (52, "Tail"),
        13: (118, "Tail"), 14: (62, "Tail"), 15: (979, "Medium"), 16: (9863, "Head"),
    },
}
GROUP_COLOR = {"Head": BLUE, "Medium": YELLOW, "Tail": RED}
IR = {"Pingan": 71, "Qingyun": 28, "Tangdaowan": 190}

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
for ax, (dataset, classes) in zip(axes, freq.items()):
    items = sorted(classes.items(), key=lambda kv: kv[1][0], reverse=True)
    labels = [f"C{cid}" for cid, _ in items]
    counts = [v[0] for _, v in items]
    colors = [GROUP_COLOR[v[1]] for _, v in items]
    ax.bar(labels, counts, color=colors, width=0.7)
    ax.set_yscale("log")
    ax.set_title(f"{dataset}  (IR ≈ {IR[dataset]})")
    ax.set_ylabel("Official training samples (log scale)")
    ax.tick_params(axis="x", rotation=45)
    ax.grid(axis="y", which="major", alpha=0.25)
handles = [plt.Rectangle((0, 0), 1, 1, color=GROUP_COLOR[g]) for g in ["Head", "Medium", "Tail"]]
fig.legend(handles, ["Head", "Medium", "Tail"], loc="upper center", ncol=3,
           bbox_to_anchor=(0.5, 1.06), frameon=False)
fig.suptitle("Per-class OFFICIAL TRAINING-MASK counts across the three QUH scenes", y=1.12, fontsize=15)
fig.tight_layout()
fig.savefig(f"{FIGDIR}/Fig_ClassFrequency_LongTail_Distribution.png", bbox_inches="tight")
plt.close(fig)
print("Saved Fig_ClassFrequency_LongTail_Distribution.png")

# ---------------------------------------------------------------------------
# 2. Experiment A (leakage) vs Experiment B (corrected) validation accuracy
# ---------------------------------------------------------------------------
# Experiment A numbers: CE-only validation OA/AA under the original pixel-random
# split, from Notebook 03's ce_checkpoint_manifest.json (Notebook 04 reuses the
# identical split for its long-tail baselines, so CE is a valid, directly
# comparable stand-in — the split, not the method, is what changed).
expA_pingan_oa = np.mean([0.9999123575810692, 0.9998831434414257, 0.9998539293017821])
expA_pingan_aa = np.mean([0.9999827019546791, 0.9997898743118686, 0.9997841082967616])
expA_qingyun_oa = np.mean([0.9997556548450154, 0.9998254677464395, 0.9998254677464395])
expA_qingyun_aa = np.mean([0.998692396612749, 0.9994938555819277, 0.9987505914504914])

# Experiment B (corrected, spatially-disjoint) CE validation, mean over 3 seeds
expB_pingan_oa, expB_pingan_aa = 0.8820752421278045, 0.7393284635530666
expB_qingyun_oa, expB_qingyun_aa = 0.7426378829758696, 0.7538288811036186

datasets = ["Pingan", "Qingyun"]
metrics = ["OA", "AA"]
expA = {"Pingan": (expA_pingan_oa, expA_pingan_aa), "Qingyun": (expA_qingyun_oa, expA_qingyun_aa)}
expB = {"Pingan": (expB_pingan_oa, expB_pingan_aa), "Qingyun": (expB_qingyun_oa, expB_qingyun_aa)}

fig, ax = plt.subplots(figsize=(8, 5.5))
x = np.arange(4)
labels = ["Pingan\nOA", "Pingan\nAA", "Qingyun\nOA", "Qingyun\nAA"]
a_vals = [expA["Pingan"][0], expA["Pingan"][1], expA["Qingyun"][0], expA["Qingyun"][1]]
b_vals = [expB["Pingan"][0], expB["Pingan"][1], expB["Qingyun"][0], expB["Qingyun"][1]]
w = 0.35
bars_a = ax.bar(x - w/2, a_vals, width=w, label="Experiment A\n(pixel-random split — leakage)", color=RED)
bars_b = ax.bar(x + w/2, b_vals, width=w, label="Experiment B\n(spatially disjoint — corrected)", color=BLUE)
for bars in (bars_a, bars_b):
    for rect in bars:
        h = rect.get_height()
        ax.annotate(f"{h*100:.1f}%", (rect.get_x() + rect.get_width()/2, h),
                    xytext=(0, 3), textcoords="offset points", ha="center", fontsize=10)
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.set_ylabel("Cross-Entropy validation accuracy")
ax.set_ylim(0, 1.12)
ax.yaxis.set_major_formatter(mticker.PercentFormatter(1.0))
ax.set_title("Validation accuracy before vs. after fixing the patch-overlap leakage\n(Cross-Entropy, same backbone, same datasets)")
ax.legend(loc="lower left", frameon=False, fontsize=10)
fig.tight_layout()
fig.savefig(f"{FIGDIR}/Fig_ExperimentA_vs_B_Leakage_Comparison.png", bbox_inches="tight")
plt.close(fig)
print("Saved Fig_ExperimentA_vs_B_Leakage_Comparison.png")

# ---------------------------------------------------------------------------
# 3. Spatial train/validation split map (zero patch-overlap visualization)
# ---------------------------------------------------------------------------
cube_shape = {"Pingan": (1230, 1000), "Qingyun": (880, 1360)}
fig, axes = plt.subplots(1, 2, figsize=(13, 6.5))
for ax, dataset in zip(axes, ["Pingan", "Qingyun"]):
    npz = np.load(SPLIT_DIR / f"{dataset.lower()}_experiment_b_spatial_split_v1.npz")
    H, W = cube_shape[dataset]
    train_rc = np.stack(np.unravel_index(npz["train_indices"], (H, W)), axis=1)
    val_rc = np.stack(np.unravel_index(npz["val_indices"], (H, W)), axis=1)
    guard_rc = np.stack(np.unravel_index(npz["guard_excluded_indices"], (H, W)), axis=1)
    ax.scatter(guard_rc[:, 1], guard_rc[:, 0], s=1, color=GRAY, alpha=0.35, label="Guard-band excluded", rasterized=True)
    ax.scatter(train_rc[:, 1], train_rc[:, 0], s=1, color=BLUE, alpha=0.55, label="Train", rasterized=True)
    ax.scatter(val_rc[:, 1], val_rc[:, 0], s=1, color=ORANGE, alpha=0.55, label="Validation", rasterized=True)
    ax.invert_yaxis()
    ax.set_xlim(0, W)
    ax.set_ylim(H, 0)
    ax.set_aspect("equal")
    ax.set_title(dataset)
    ax.set_xlabel("column")
    ax.set_ylabel("row")
leg = fig.legend(*axes[0].get_legend_handles_labels(), loc="upper center", ncol=3,
                  bbox_to_anchor=(0.5, 1.04), frameon=False, markerscale=8)
fig.suptitle("Experiment B spatial train/validation split\n(zero train–validation patch-footprint overlap by construction)",
             y=1.12, fontsize=14)
fig.tight_layout()
fig.savefig(f"{FIGDIR}/Fig_Spatial_TrainVal_Split_Map.png", bbox_inches="tight")
plt.close(fig)
print("Saved Fig_Spatial_TrainVal_Split_Map.png")

# ---------------------------------------------------------------------------
# 4. Redesigned calibration trade-off figure (fixes overlapping labels in Fig N5)
# ---------------------------------------------------------------------------
calib = {
    "Pingan": {
        "Global_TS": (0.6701120994978699, 0.23342388141219517),
        "LA_Global_TS": (0.6888281819081422, 0.23614026458511117),
        "LTLC_Full": (0.6390498033622368, 0.593614933976922),
        "Standard_LA": (3.733328401114248, 0.1504950842598279),
    },
    "Qingyun": {
        "Global_TS": (0.9809442952635062, 0.1522501675608444),
        "LA_Global_TS": (1.0272118444191043, 0.1560496728146989),
        "LTLC_Full": (0.965159300229518, 0.5196115039619587),
        "Standard_LA": (4.736595585194628, 0.206925365706033),
    },
}
MARKER = {"Global_TS": "o", "LA_Global_TS": "s", "LTLC_Full": "D", "Standard_LA": "^"}
COLOR = {"Global_TS": BLUE, "LA_Global_TS": VIOLET, "LTLC_Full": RED, "Standard_LA": GRAY}
NICE = {"Global_TS": "Global temperature scaling",
        "LA_Global_TS": "Post-hoc Standard LA + global TS",
        "LTLC_Full": "LTLC (rarity-conditioned TS)",
        "Standard_LA": "Post-hoc Standard LA (uncalibrated)"}
# Global_TS and LA_Global_TS sit almost on top of each other; draw the first larger and
# hollow so BOTH remain visible without moving any data point.
MSIZE = {"Global_TS": 340, "LA_Global_TS": 110, "LTLC_Full": 170, "Standard_LA": 170}
FACE  = {"Global_TS": "none", "LA_Global_TS": None, "LTLC_Full": None, "Standard_LA": None}

fig, axes = plt.subplots(1, 2, figsize=(12.5, 5.5))
for ax, dataset in zip(axes, ["Pingan", "Qingyun"]):
    for method, (nll, tail_ece) in calib[dataset].items():
        fc = COLOR[method] if FACE[method] is None else "none"
        ax.scatter(nll, tail_ece, s=MSIZE[method], marker=MARKER[method],
                   facecolor=fc, edgecolor=COLOR[method] if fc == "none" else "black",
                   linewidth=2.0 if fc == "none" else 0.6, zorder=3, label=NICE[method])
    ax.set_xlabel("Negative log-likelihood (lower = better)")
    ax.set_ylabel("Tail-class ECE (lower = better)")
    ax.set_title(dataset)
    ax.grid(alpha=0.25)
axes[0].legend(loc="upper right", frameon=True, fontsize=9.5, framealpha=0.9)
fig.suptitle("Calibration trade-off (validation only; NOT a recognition result)" + chr(10) +
             "Rarity-conditioned LTLC attains the lowest NLL but markedly worse tail-class ECE",
             y=1.06, fontsize=13)
fig.tight_layout()
fig.savefig(f"{FIGDIR}/Fig_Calibration_Tradeoff_Redesigned.png", bbox_inches="tight")
plt.close(fig)
print("Saved Fig_Calibration_Tradeoff_Redesigned.png")

# ---------------------------------------------------------------------------
# 5. Per-seed paired deltas (primary) with mean +/- SD; bootstrap CI shown only
#    as a faint secondary band. With n=3 the bootstrap mean takes just 10
#    distinct values, so the CI is descriptive, NOT an inferential guarantee.
#    Comparison object: TRAINED method vs TRAINED CE (Experiment-B validation AA).
# ---------------------------------------------------------------------------
sig = json.load(open(REPO_ROOT / "reproducibility" / "significance_test_results_v1.json", encoding="utf-8"))
sig_sorted = sorted(sig, key=lambda r: (r["dataset"], r["mean_delta_AA"]))
fig, ax = plt.subplots(figsize=(9.5, 6.4))
ypos = np.arange(len(sig_sorted))
SEEDMARK = ["o", "s", "^"]
for y, r in zip(ypos, sig_sorted):
    lo, hi = r["bootstrap_95CI_low"], r["bootstrap_95CI_high"]
    ax.plot([lo, hi], [y, y], color=GRAY, lw=7, alpha=0.28,
            solid_capstyle="butt", zorder=1)
    m, sd = r["mean_delta_AA"], r["sd_delta_AA"]
    ax.plot([m - sd, m + sd], [y, y], color="black", lw=2.0,
            solid_capstyle="round", zorder=3)
    for k, dv in enumerate(r["per_seed_delta"]):
        ax.plot(dv, y, SEEDMARK[k], color=BLUE, markersize=6.5,
                markeredgecolor="black", markeredgewidth=0.5, zorder=4)
    ax.plot(m, y, "|", color="black", markersize=16, markeredgewidth=2.2, zorder=5)
ax.axvline(0, color="black", lw=1, linestyle="--", alpha=0.6)
ax.set_yticks(ypos)
ax.set_yticklabels([f"{r['dataset']} - {r['method']}" for r in sig_sorted])
ax.set_xlabel("Delta AA vs Cross-Entropy (Experiment-B validation, trained methods)")
ax.xaxis.set_major_formatter(mticker.PercentFormatter(1.0))
ax.set_title("Per-seed paired AA differences vs Cross-Entropy" + chr(10) +
             "n=3 seeds: suggestive, not confirmatory", fontsize=13)
from matplotlib.lines import Line2D
ax.legend(handles=[
    Line2D([], [], color=BLUE, marker="o", ls="", markeredgecolor="black", label="seed 42"),
    Line2D([], [], color=BLUE, marker="s", ls="", markeredgecolor="black", label="seed 123"),
    Line2D([], [], color=BLUE, marker="^", ls="", markeredgecolor="black", label="seed 3407"),
    Line2D([], [], color="black", lw=2, label="mean +/- SD"),
    Line2D([], [], color=GRAY, lw=7, alpha=0.28, label="bootstrap 95% CI (descriptive only)"),
], loc="lower right", frameon=True, fontsize=9, framealpha=0.92)
ax.grid(axis="x", alpha=0.25)
fig.tight_layout()
fig.savefig(f"{FIGDIR}/Fig_PerSeed_Delta_vs_CE.png", bbox_inches="tight")
plt.close(fig)
print("Saved Fig_PerSeed_Delta_vs_CE.png")

print(chr(10) + "All figures written to", FIGDIR)
