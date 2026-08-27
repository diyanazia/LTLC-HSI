# TRAINING-COUNT SEMANTICS AUDIT v1

**Date:** 2026-08-27

The brief anticipated **two** count concepts. Primary records show **three**. All three are
legitimate; none is a bug; none may be merged.

---

## 1. The three concepts

| Name to use | Definition | Authoritative source |
|---|---|---|
| **OFFICIAL TRAINING-MASK COUNT** | Per-class pixel count in the published QUH training mask | `audit/{scene}_frequency_groups.csv` → `official_train` |
| **NB01 PIXEL-RANDOM 70% TRAIN COUNT** | The 70% share of the official mask under the seed-2026 pixel-random split (Experiment A / Notebook 03 training set) | same file → `actual_train_70pct` |
| **EXPERIMENT-B POST-GUARD TRAIN COUNT** | Training pixels surviving the Experiment-B spatially disjoint split **after guard-band exclusion** | `audit/notebook06a_spatial_validation/experiment_b_training_class_statistics_v1_frozen.json` → `class_statistics[*].train_count` |

### Dataset-level reconciliation

| Dataset | Concept | Total | Min class | Max class | **IR** |
|---|---|---:|---:|---:|---:|
| Pingan | official training-mask | 114,099 | 814 | 57,811 | **71.0** |
| Pingan | NB01 pixel-random 70% | 79,869 | 570 | 40,468 | **71.0** |
| Pingan | **Experiment-B post-guard** | **65,710** | **85** | **33,783** | **397.4** |
| Qingyun | official training-mask | 95,492 | 977 | 27,817 | **28.5** |
| Qingyun | NB01 pixel-random 70% | 66,844 | 684 | 19,472 | **28.5** |
| Qingyun | **Experiment-B post-guard** | **63,179** | **74** | **19,556** | **264.3** |

Experiment-B totals match `final_train_count` in the frozen statistics and the
`train_indices` length in the split files (65,710 / 63,179) exactly.

**Cross-verification:** the Qingyun LA-loss checkpoint records its training prior as
`class_counts: [19556, 11807, 967, 74, 15220, 15555]` — identical to the Experiment-B
post-guard counts. The trained long-tail methods used **concept 3**, not concepts 1 or 2.

---

## 2. A scientifically substantive consequence (not merely nomenclature)

The guard band does not remove pixels uniformly. Rare, spatially clustered classes lose far
more than head classes:

| Pingan class | official | 70% split | post-guard | retained vs 70% |
|---|---:|---:|---:|---:|
| 5 (Medium) | 2,076 | 1,453 | **85** | 5.9% |
| 7 (Tail) | 1,398 | 979 | **110** | 11.2% |
| 3 (Tail) | 835 | 585 | **219** | 37.4% |
| 2 (Head) | 57,811 | 40,468 | 33,783 | 83.5% |

**Effective imbalance therefore rises sharply once leakage is controlled: 71× → 397×
(Pingan) and 28.5× → 264× (Qingyun).**

This is worth stating in the thesis. Experiment B is a *substantially harder* long-tail
problem than the nominal dataset IR suggests, which strengthens the framing of the study and
partly explains why validation accuracies fall so far from Experiment A's leaked ~100%.

**Caution:** the Experiment-B training set is **not a subset** of the 70% split — it is a
different spatial partition. Qingyun classes 1 and 3 actually have slightly *more* post-guard
training pixels (19,556 and 967) than in the 70% split (19,472 and 966). Do not describe
concept 3 as "concept 2 minus the guard band".

---

## 3. File-by-file audit

| FILE | COLUMN | CURRENT MEANING | SOURCE | RENAME REQUIRED? | SAFE FOR THESIS? |
|---|---|---|---|---|---|
| `Day1/tables/Thesis_Table_07_Dataset_Overview.csv` | `total_train_samples`, `min_class_count`, `max_class_count`, `imbalance_ratio_max_over_min` | official training-mask | concept 1 | **YES — ambiguous** | not as-is → **v2 issued** |
| `results/final_thesis_tables_v1/Thesis_Table_07_Dataset_Overview_v2.csv` | `official_train_mask_*` | official training-mask | concept 1 | no | **YES** |
| `Day1/tables/Thesis_Table_04_PerClass_Frequency_and_Mechanism.csv` | `expB_split_train_count` | Experiment-B post-guard | concept 3 | partially — `rarity` unlabelled | borderline → **v2 issued** |
| `results/final_thesis_tables_v1/Thesis_Table_04_..._v2.csv` | `expB_post_guard_train_count`, `rarity_from_expB_post_guard_count` | Experiment-B post-guard | concept 3 | no | **YES** |
| `results/notebook06b.../Table_ClassLevel_Mechanism_Summary_v2.csv` | `train_count`, `rarity` | Experiment-B post-guard | concept 3 | **YES — bare `train_count`** | **NO** as-is; cite Table 04 v2 instead |
| `results/notebook06b.../Table_PerClass_Rarity_Difficulty_and_AdaptiveGain_v2.csv` | `train_count`, `rarity` | Experiment-B post-guard | concept 3 | **YES — bare `train_count`** | appendix only, with caption |
| `results/notebook06b.../Table_Rarity_Mechanism_Descriptive_Correlations_v2.csv` | correlations over `rarity` | Experiment-B post-guard | concept 3 | caption required | **YES with caption** |
| `audit/{scene}_ltlc_class_statistics.csv` | `train_count`, `prior`, `rarity` | **NB01 pixel-random 70%** (concept 2 — e.g. Pingan class 1 = 3,425) | concept 2 | **YES — highest-risk file** | **NO** for Experiment-B tables |
| `audit/final_training_imbalance_summary.csv` | `largest_count`, `smallest_count`, `final_IR` | concept 2 (40,468 / 570, IR 71.0) — "final" is misleading | concept 2 | **YES** | **NO** — do not cite as Experiment-B IR |
| `audit/official_imbalance_summary.csv` | `official_IR` | concept 1 | concept 1 | no | **YES** |
| `audit/{scene}_frequency_groups.csv` | `official_train`, `actual_train_70pct` | concepts 1 and 2, both explicitly named | 1 & 2 | no — exemplary naming | **YES** |
| `results/final_thesis_tables_v1/Thesis_Table_08_TrainingCount_Reconciliation_v1.csv` | all three, explicitly named | all | — | no | **YES — new** |
| `Fig_ClassFrequency_LongTail_Distribution.png` | y-axis | concept 1 | concept 1 | fixed — axis now reads "Official training-mask pixels" | **YES** |
| `Fig_N1`, `Fig_N2` | "Training-frequency rarity" | concept 3 | concept 3 | caption required | **YES with caption** |

---

## 4. Two highest-risk items

1. **`audit/{scene}_ltlc_class_statistics.csv`** carries a bare `train_count` holding
   **concept 2** values, while every other file with a bare `train_count` holds **concept 3**.
   Same column name, different concept. If any Experiment-B rarity analysis were rebuilt from
   this file it would silently use the wrong priors. Do not use it for Experiment-B work.

2. **`audit/final_training_imbalance_summary.csv`** is named "final" but reports **concept 2**
   (IR 71.0). The *actual* final Experiment-B IR is **397.4**. Citing this file as the
   Experiment-B imbalance ratio would understate the difficulty of the study by 5.6×.

---

## 5. Actions taken

- Issued `Thesis_Table_07_Dataset_Overview_v2.csv` with `official_train_mask_*` naming.
- Issued `Thesis_Table_04_PerClass_Frequency_and_Mechanism_v2.csv` with
  `expB_post_guard_train_count` and `rarity_from_expB_post_guard_count`.
- Created `Thesis_Table_08_TrainingCount_Reconciliation_v1.csv` giving all three concepts
  side by side, per class, plus `expB_guard_excluded_count`.
- Corrected the class-frequency figure's y-axis and title to name the concept.
- **No original file was overwritten or deleted.**

## 6. Rule for the Black Book

Every count, rarity value, prior and imbalance ratio must state which concept it uses, on
first use in each chapter and in every table header and figure caption. When reporting "the"
imbalance ratio of the study, report **both**: the dataset's nominal official IR (71× / 28.5×)
**and** the Experiment-B post-guard IR (397× / 264×), and explain the difference.
