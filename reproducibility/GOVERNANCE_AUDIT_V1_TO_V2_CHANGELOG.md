# GOVERNANCE AUDIT — v1 → v2 CHANGELOG

**Date:** 2026-08-27
**Base:** `FINAL_GOVERNANCE_AUDIT_v1.md` (retained unchanged)
**Current:** `FINAL_GOVERNANCE_AUDIT_v2.md`

This changelog lists **only the new evidence added**. No prior finding was revised, softened,
or removed.

---

## New primary evidence

| Ref | Artifact | Why it is new |
|---|---|---|
| **L** | `LTLC/notebooks/Untitled1.ipynb` | Previously classified INVESTIGATE and not read. The 2026-08-27 read-only forensic review established it as the **primary execution record of a failed v1 sealed-test attempt**. |
| M | `Day1_Improvements_2026-08-26/scripts/SUPERSEDED_v1_DO_NOT_RUN__SEALED_TEST_run_once_in_colab.py` | Confirmed **byte-identical** to cells 0/1 of L (similarity 1.0000), fixing the v1 code as the thing that was launched. |

---

## New timeline events

| Row | Event | Timestamp |
|---|---|---|
| 10 (expanded) | **(A)** Day-1 package preparation — now names both sealed-test scripts (superseded v1 + corrected v2) | 2026-08-26 |
| **10a (new)** | **(B)** Failed v1 attempt: launched once on Colab Tesla T4 (python 3.13.15, torch 2.11.0+cu128); confirmation phrase entered. **(C)** Terminated by `FileNotFoundError` inside `recover_hybridsn_class()`, from `main()` line 319. **(D)** No checkpoint or official-test data accessed. **(E)** No result artifact written. | **2026-08-26T12:17:20.019717Z** |
| **10b (new)** | Two further cells attempted to `exec` **v2** in Colab with `PREFLIGHT_ONLY = True` asserted; both aborted at `drive.mount`. **No v2 execution occurred in Colab.** | 2026-08-26 |
| 11 (relabelled) | **(F)** Preflight of the corrected v2 pipeline, locally | 2026-08-26T16:53:39Z |
| 12 (relabelled) | **(F)** Validation reproduction — 6/6 checkpoints matched the frozen ledger to 5 decimals | 2026-08-26 ~16:54–16:57Z |
| 13 (relabelled) | **(G)** Successful one-time official-test evaluation, locally on CPU | 2026-08-26T16:58:29Z |

Events A–G are now explicitly labelled in the v2 timeline.

---

## New section

**§2a — "The failed v1 attempt did NOT spend the scientific seal."** Three independent lines
of evidence:

1. **Failure preceded all data loading** — the traceback terminates inside
   `recover_hybridsn_class()`, reached from `main()` before any checkpoint load, split read,
   or dataset construction.
2. **The v1 implementation had no functional test-data loading path** — its docstring declares
   Section 4 a stub ("a required plug-in point that you must fill in"), and static inspection
   confirms **zero** occurrences of `test_indices`, `test_labels_model`, or
   `fixed_split_seed2026` in the v1 source.
3. **No official-test result was produced** — the sole result file in the repository carries
   `timestamp_utc 2026-08-26T16:58:29Z`, from the later corrected run.

Conclusion recorded: the typed phrase at 12:17:20Z records an *intent* to open the test set,
not an opening of it.

---

## Amended answers

| Question | Amendment |
|---|---|
| Q10 — "Was the test scored exactly once?" | Still **Yes**. Now adds: one earlier launch occurred (12:17:20Z, v1 harness) but terminated before any data access and wrote no result. The count of official-test **scorings** remains exactly one. |
| §4 "Objectively verified" | One bullet added recording the failed launch and its evidence path. |

---

## What did NOT change

- The verdict: **PROTOCOL-GOVERNANCE INCONSISTENCY — NO SCIENTIFIC CONTAMINATION.**
- The contamination assessment (§6).
- The approved thesis claim (§8) and all prohibited phrasings.
- Both readings of the NB05/NB06B gate, including the literal
  `STOP_METHOD_DEVELOPMENT_AND_KEEP_OFFICIAL_TEST_SEALED` counter-reading.
- Every numerical result, table, and figure in the project.

**Scientific results changed: NONE.**
