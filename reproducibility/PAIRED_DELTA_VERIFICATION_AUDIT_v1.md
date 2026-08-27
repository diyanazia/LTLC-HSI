# PAIRED-DELTA VERIFICATION AUDIT v1

**Date:** 2026-08-27
**Outcome: the v2 tables are CORRECT. No numerical repair was required or performed.**

This audit was commissioned to repair a suspected stale value. Recomputation from primary
records shows the suspicion was mistaken. The v2 tables are preserved unchanged, and a
clarity-only v3 was produced with identical numbers and unambiguous column names.

---

## 1. Files audited

| File | Verdict |
|---|---|
| `results/notebook06b_experiment_b_thesis_ready_v2/Table_Paired_Recognition_Deltas_v2.csv` | **CORRECT — all 6 rows reproduce exactly** |
| `results/notebook06b_experiment_b_thesis_ready_v2/Table_Paired_Recognition_Deltas_MeanStd_v2.csv` | **CORRECT — all means and SDs reproduce exactly** |

**Source of truth used:**
`posthoc/notebook06b_experiment_b/recognition_search_v1/LTLC_Notebook06B_ExperimentB_Posthoc_Selected_Recognition_v1.csv`
(frozen post-hoc recognition selections), with parameters frozen in
`LTLC_Notebook06B_ExperimentB_Posthoc_Recognition_Freeze_v1.json` (`created_utc`
2026-08-20T16:23:29Z).

---

## 2. What these tables actually measure

This is the crux of the whole issue.

These tables compare **three post-hoc transformations of the SAME frozen Experiment-B CE
validation logits**:

```
CE                 : z                                (raw CE logits)
POST-HOC STANDARD LA: z - tau * log(pi + eps)
ORIGINAL LTLC      : z - tau * (1 + alpha * rarity) * log(pi + eps)
```

No model is retrained. `tau` and `alpha` are selected per seed on validation from the frozen
grids. The columns therefore measure *what a post-hoc logit transform adds on top of one
fixed CE model*.

They are **NOT** the Experiment-B run-ledger comparison between a **separately TRAINED
LA-loss model** and a **separately TRAINED CE model**. That is a different experiment with
different weights, and it lives in the run ledger.

---

## 3. Row-by-row verification (per-seed table)

Recomputed as `AA(Standard_LA) − AA(CE)` and `AA(Original_LTLC) − AA(Standard_LA)` from the
frozen selections. All values agree to the full 18 decimal places printed.

| dataset/seed | selected LA τ | v2 `LA_minus_CE_AA` | recomputed | match | v2 `LTLC_minus_LA_AA` | recomputed | match |
|---|---:|---:|---:|:--:|---:|---:|:--:|
| Pingan/42 | 0.5 | 0.014710283287985959 | 0.014710283287985959 | ✔ | 0.0 | 0.0 | ✔ |
| Pingan/123 | 1.75 | 0.017010421682198462 | 0.017010421682198462 | ✔ | 0.003274896114514481 | 0.003274896114514481 | ✔ |
| Pingan/3407 | 1.0 | 0.014876891139380843 | 0.014876891139380843 | ✔ | 0.0 | 0.0 | ✔ |
| Qingyun/42 | 2.0 | 0.007206238129680465 | 0.007206238129680465 | ✔ | 0.0 | 0.0 | ✔ |
| Qingyun/123 | 0.5 | 0.000354967521459248 | 0.000354967521459248 | ✔ | 0.000134371674309630 | 0.000134371674309630 | ✔ |
| **Qingyun/3407** | **0.0** | **0.0** | **0.0** | ✔ | 0.0 | 0.0 | ✔ |

Mean/SD table: all 12 aggregate values (means and `ddof=1` SDs) recompute exactly from the
per-seed rows.

---

## 4. Qingyun seed 3407 — why 0.0 is exactly right

The post-hoc recognition search selected **τ = 0** for Qingyun seed 3407.

Substituting τ = 0 into the Standard-LA formula:

```
z_LA = z_CE - 0 * log(pi + eps) = z_CE
```

The transform is the **identity**. The logits are unchanged, therefore the predictions are
unchanged, therefore every metric is unchanged:

```
AA_LA        = AA_CE        = 0.7466855642251226
LA_minus_CE_AA = 0.0                      (exact, by construction)
```

Original LTLC for that run selected τ = 0 **and** α = 0, so it too collapses to the identity
and `LTLC_minus_LA_AA = 0.0` exactly.

This is a **mathematical identity, not a missing or stale value.** A non-zero number in that
cell would be the error.

The same reasoning explains the four other exact zeros in the `LTLC_minus_LA_AA` column:
Pingan/42, Pingan/3407 and Qingyun/42 all selected **α = 0**, so LTLC ≡ Standard LA for those
runs. Only 2 of 6 runs (Pingan/123 with α = 0.75, Qingyun/123 with α = 0.5) selected a
non-zero α — which is exactly the `2/6` figure recorded in the Notebook 06B release. **The
zeros in this table are the evidence for the null result, not a defect in it.**

---

## 5. Why the previously suggested +0.004020 is a different quantity

The earlier `DATA_INTEGRITY_NOTES.md` proposed replacing the Qingyun/3407 cell with
`+0.004020`, derived from the Experiment-B run ledger:

| seed | ledger CE AA | ledger **TRAINED LA-loss** (τ=0.5) AA | difference |
|---|---:|---:|---:|
| 42 | 0.763832 | 0.764169 | +0.000337 |
| 123 | 0.750969 | 0.763574 | +0.012606 |
| 3407 | 0.746686 | 0.750706 | **+0.004020** |

Those numbers are correct **for what they measure** — two *separately trained models*. They
are not comparable to this table, which measures a *post-hoc transform of one fixed CE
model*. Two different objects were conflated because both were called "LA".

Independent confirmation that the two are distinct: the v2 table's Qingyun/42 value is
`0.007206`, whereas the trained-model ledger difference for the same seed is `0.000337`.
Different quantities, different values, both correct in their own frame.

**Substituting +0.004020 into this table would have introduced an error into a correct
table.**

---

## 6. Action taken

- `Table_Paired_Recognition_Deltas_v2.csv` — **preserved unchanged**.
- `Table_Paired_Recognition_Deltas_MeanStd_v2.csv` — **preserved unchanged**.
- Created `results/final_thesis_tables_v1/Table_Paired_Recognition_Deltas_v3.csv`
  (sha256 `66f7fe2ff86fe6be4f39f9aac82efe4581db3f479a7fc89d0a58f0c8191997a7`)
- Created `results/final_thesis_tables_v1/Table_Paired_Recognition_Deltas_MeanStd_v3.csv`
  (sha256 `3b14fd222c99475a1a48eb9b331cfa77538c6567d6596545777861a5f502670f`)

### v3 is a clarity-only reissue — ZERO numerical change

Verified programmatically: every numeric field in v3 is the **byte-identical string** copied
from v2. Only column names and added context columns differ.

| v2 column | v3 column |
|---|---|
| `LA_minus_CE_AA` | `posthoc_standard_LA_minus_CE_AA` |
| `LTLC_minus_LA_AA` | `posthoc_LTLC_minus_standard_LA_AA` |
| `LA_minus_CE_TailAcc` | `posthoc_standard_LA_minus_CE_TailAcc` |
| `LTLC_minus_LA_TailAcc` | `posthoc_LTLC_minus_standard_LA_TailAcc` |
| — | `posthoc_selected_LA_tau` (new) |
| — | `posthoc_selected_LTLC_tau`, `posthoc_selected_LTLC_alpha` (new) |
| — | `comparison_object` (new, constant, states the frame explicitly) |

The new `posthoc_selected_LA_tau` column makes the Qingyun/3407 zero self-explanatory: the
reader sees `τ = 0` next to the `0.0`.

---

## 7. Does any thesis narrative or figure change?

**No.** No number changed, so nothing downstream moves:

- Fig N2 (`Rarity_vs_Adaptive_LTLC_Gain`) is unaffected.
- The `2/6 non-zero α` and `β = 0 on both datasets` findings are unaffected — and are in fact
  *reinforced*, since the zeros are now shown to be genuine collapses to the baseline.
- The main conclusion (frequency-only rarity adaptation gives no robust recognition benefit)
  is unaffected.

The only change is documentary: an incorrect "stale data" claim in two older documents is
superseded by `PAIRED_DELTA_CORRECTION_NOTICE_v1.md`.

---

## 8. Naming rule to carry into the Black Book

Never write unqualified "Logit Adjustment" where both objects could be meant:

- **POST-HOC STANDARD LA** — a logit transform applied to frozen CE validation logits
  (Notebook 06B; these tables).
- **TRAINED LA-LOSS** — a separately trained Experiment-B model (run ledger; Thesis Table 01).

These must be distinguished in every table, figure caption, and sentence.
