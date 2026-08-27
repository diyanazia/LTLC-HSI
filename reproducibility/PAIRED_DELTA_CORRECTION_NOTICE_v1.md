# PAIRED-DELTA CORRECTION NOTICE v1

**Date:** 2026-08-27
**Supersedes:** one specific claim, in two documents, and nothing else.

---

## 1. The claim that was wrong

Two earlier documents asserted that the Qingyun seed-3407 row of
`Table_Paired_Recognition_Deltas_v2.csv` contained a **stale** value — an artifact of a
partial re-run — and that the "true" value was approximately `+0.004020`:

- `Day1_Improvements_2026-08-26/DATA_INTEGRITY_NOTES.md` (§1)
- `PROJECT_HANDOFF_2026-08-26.md` (§7.2), which repeated the claim without independent check

**That claim is incorrect.** The v2 value of `0.0` is exact and correct.

---

## 2. Why the error was made

Two different experimental objects were both referred to as "LA" and were compared to each
other:

| Object | What it is | Where it lives |
|---|---|---|
| **TRAINED LA-LOSS** | A separately trained Experiment-B model using the LA loss function | `run_ledger.csv`, Thesis Table 01 |
| **POST-HOC STANDARD LA** | A logit transform `z − τ·log(π+ε)` applied to *frozen CE validation logits*; no retraining | Notebook 06B post-hoc tables |

`Table_Paired_Recognition_Deltas_v2.csv` measures the **post-hoc** object. The proposed
`+0.004020` was computed from the **trained** object. Both figures are individually correct;
they simply describe different experiments and are not interchangeable.

The discrepancy that triggered the alarm — "the ledger says +0.004020, the table says 0.0" —
was therefore never evidence of staleness. It was evidence that two different quantities were
being compared.

---

## 3. Why 0.0 is correct

For Qingyun seed 3407 the frozen post-hoc recognition search selected **τ = 0**. With τ = 0:

```
z_LA = z_CE − 0 · log(π + ε) = z_CE
```

The transform is the identity, so predictions and every metric are unchanged:

```
AA_LA = AA_CE = 0.7466855642251226   ⟹   LA_minus_CE_AA = 0.0   (exact)
```

Original LTLC for that run selected τ = 0 **and** α = 0, so it also collapses to the
identity, giving `LTLC_minus_LA_AA = 0.0`.

---

## 4. Independent recomputation

Both v2 tables were recomputed from the frozen primary source
(`LTLC_Notebook06B_ExperimentB_Posthoc_Selected_Recognition_v1.csv`):

- **All 6 per-seed rows** reproduce exactly (agreement to 18 decimal places).
- **All 12 aggregate values** in the MeanStd table reproduce exactly.

Full evidence: `PAIRED_DELTA_VERIFICATION_AUDIT_v1.md`.

---

## 5. Status of the old documents

`DATA_INTEGRITY_NOTES.md` and `PROJECT_HANDOFF_2026-08-26.md` are **retained unchanged** as
historical audit artifacts. They have not been edited, overwritten or deleted. This notice
supersedes **only** their claim about the Qingyun seed-3407 paired-delta value.

**Everything else in those documents stands**, including — importantly — the separate and
still-valid finding about two different training-count columns (now expanded to three
concepts in `TRAINING_COUNT_SEMANTICS_AUDIT_v1.md`).

---

## 6. Consequences

| Item | Status |
|---|---|
| `Table_Paired_Recognition_Deltas_v2.csv` | correct; safe to cite |
| `Table_Paired_Recognition_Deltas_MeanStd_v2.csv` | correct; safe to cite |
| Recommended citation | the clarity-only **v3** reissue (identical numbers, unambiguous names) |
| Regenerating these tables from the run ledger | **DO NOT** — it would inject an error |
| Any thesis narrative, figure or conclusion | unchanged |

---

## 7. Rule adopted to prevent recurrence

From this point onward, the unqualified term "Logit Adjustment" is not used where the two
objects could be confused. Every table, figure caption, audit note and thesis sentence must
say either **POST-HOC STANDARD LA** or **TRAINED LA-LOSS**.

The v3 tables enforce this in their column names and carry an explicit `comparison_object`
column, plus a `posthoc_selected_LA_tau` column that makes the Qingyun/3407 zero
self-explanatory at a glance.

---

## 8. Referenced from

- `FINAL_CLAIM_BOUNDARIES_v1.md`
- `BLACK_BOOK_WRITING_HANDOFF_v1.md`
- `FINAL_TABLE_QA_v1.md`
