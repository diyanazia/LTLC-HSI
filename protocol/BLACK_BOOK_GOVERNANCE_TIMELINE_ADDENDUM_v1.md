# BLACK BOOK GOVERNANCE TIMELINE ADDENDUM v1

**Date:** 2026-08-27 · Additive note. `BLACK_BOOK_WRITING_HANDOFF_v1.md` and its Addendum A
are **not** rewritten; this supplements them.

---

## 1. The authoritative governance source is now v2

| Use | Document |
|---|---|
| **Governance facts, timeline, evidence** | **`FINAL_GOVERNANCE_AUDIT_v2.md`** ← authoritative |
| What changed from v1 | `GOVERNANCE_AUDIT_V1_TO_V2_CHANGELOG.md` |
| Superseded (retained, do not cite as current) | `FINAL_GOVERNANCE_AUDIT_v1.md` |
| **Text to insert into the thesis** | `THESIS_PROTOCOL_GOVERNANCE_PARAGRAPH_v1.md` — **unchanged and still correct** |

The governance paragraph itself needs no revision. v2 adds an event to the *audit* timeline;
it does not change what the thesis claims.

---

## 2. If — and only if — you mention the failed v1 attempt

Use this wording:

> "A preliminary sealed-test harness was launched once but terminated before model or
> test-data loading because the frozen HybridSN source could not be recovered. No test result
> was produced. A later corrected pipeline was independently validated before the one-time
> confirmatory evaluation."

**Keep it to that.** One or two sentences in the protocol chapter, at most, and only where the
sequence of events is being described. It is a tooling failure, not a scientific event.

---

## 3. Do not overemphasise it

- **Do not** give it its own subsection, figure, or table.
- **Do not** put the traceback, the T4 environment block, or the notebook path in the main
  text. Detailed evidence belongs in the **reproducibility / audit appendix**, cited to
  `FINAL_GOVERNANCE_AUDIT_v2.md` §2a and §10a.
- **Do not** describe it as a near-miss, a breach, or an aborted opening of the test set. It
  never reached the data. Saying so invites a question that the evidence already answers.
- **Do not** let it displace the substantive disclosure. The governance point that matters is
  the one in `THESIS_PROTOCOL_GOVERNANCE_PARAGRAPH_v1.md`: two frozen artifacts recorded that
  the test should remain sealed, and a one-time confirmatory evaluation was nevertheless run
  after all decisions were frozen.

---

## 4. Why it is defensible to state plainly

The failed launch **did not spend the seal**, on three independent grounds (v2 §2a):

1. Execution terminated inside `recover_hybridsn_class()` — before any checkpoint load, split
   read, or dataset construction.
2. The v1 script had **no functional test-data loading path**: its own docstring declares
   Section 4 a stub, and the source contains zero occurrences of `test_indices`,
   `test_labels_model`, or `fixed_split_seed2026`.
3. No result artifact was written. The sole official-test result file carries
   `timestamp_utc 2026-08-26T16:58:29Z`, from the later corrected run.

The official test was scored **exactly once**.

---

## 5. Primary evidence — cite by path, do not copy

Canonical master path:

```
CSE498/LTLC/notebooks/Untitled1.ipynb
```

Classification **KEEP_AUDIT**. Retained unchanged and **unrenamed** in the master archive.

**It is not copied into `LTLC_BLACKBOOK_FINAL/`.** Reference it by the path above in the
reproducibility appendix. Copy it under `11_reproducibility/` **only** if the submission
package must itself physically contain the primary failed-attempt execution record — otherwise
this is unnecessary duplication.

The same policy applies to `CSE498/LTLC/notebooks/Untitled0.ipynb` (KEEP_AUDIT, sole
provenance for `LTLC_Kaggle_Notebook04.zip`): **master archive only**, not copied, and not
mentioned in the thesis unless the Notebook-04 migration is being described.

---

## 6. Chapter placement

| Content | Where |
|---|---|
| Governance disclosure paragraph (Version A) | Chapter 4 — Method / experimental protocol |
| Condensed pointer (Version B) | Chapter 10 — Official-test confirmation |
| One-sentence mention of the failed v1 launch, if used at all | Chapter 4, alongside the disclosure |
| Traceback, environment block, notebook path, §2a evidence | Chapter 14 — Reproducibility appendix |
