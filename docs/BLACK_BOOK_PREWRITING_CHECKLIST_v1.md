# BLACK BOOK PREWRITING CHECKLIST v1

**Date:** 2026-08-27 · Writing-time items only. All scientific QA is complete.
No experiment, inference, training, tuning or method development remains.

---

## Checklist

- [ ] **Insert governance paragraph** — `THESIS_PROTOCOL_GOVERNANCE_PARAGRAPH_v1.md`,
      Version A, into the experimental protocol / methodology chapter.
- [ ] **Use POST-HOC STANDARD LA vs TRAINED LA-LOSS terminology** — define both on first use
      in each chapter; never write "LA" or "Logit Adjustment" unqualified.
- [ ] **Apply corrected Table 03 label** — cite `Thesis_Table_03_Calibration_Tradeoff_v2.csv`
      (`POST-HOC STANDARD LA + Global TS`, and also `POST-HOC STANDARD LA (uncalibrated)`).
- [ ] **Apply corrected Table 06 label** — cite
      `Thesis_Table_06_Rarity_Mechanism_Correlations_v2.csv`
      (`spearman_rarity_vs_posthoc_standard_LA_gain`).
- [ ] **Use approved figure captions** — verbatim from
      `BLACK_BOOK_FINAL_FIGURE_MANIFEST_v1.md` (F1–F9).
- [ ] **State Fig N3 independent colour scales** — "Colour scales are independently normalized
      within each dataset panel to emphasize the within-dataset parameter-response landscape;
      colours should therefore not be compared quantitatively across panels."
- [ ] **State Fig N2 differing y-axis scales** — panels use different y-ranges (Pingan ≈±0.02,
      Qingyun ≈±0.003); vertical magnitudes and slopes must not be compared across datasets.
- [ ] **Use redesigned calibration figure, not superseded Fig N5** — use
      `Fig_Calibration_Tradeoff_Redesigned.png`; `Fig_N5_Calibration_NLL_vs_TailECE_v2.png` is
      EXCLUDED (Grade C, label overlap).
- [ ] **Use canonical official-test array hashes in reproducibility appendix** — from
      `BLACK_BOOK_REPRODUCIBILITY_NOTE_v1.md` §B, not container SHA-256.
- [ ] **Distinguish official training-mask counts from Experiment-B post-guard counts** —
      report both imbalance ratios (71.0×/28.5× nominal vs 397.4×/264.3× post-guard) and
      explain the difference.
- [ ] **Distinguish validation findings from official-test findings** — never present
      Experiment-B validation numbers as test performance, or vice versa.
- [ ] **Do not claim test-set improvement over CE** — no Experiment-B CE official-test result
      exists; do not substitute Notebook 03's CE test numbers.
- [ ] **Do not claim LTLC robust recognition improvement** — `may_claim_*` flags are all false;
      R1 with β = 0 is exactly POST-HOC STANDARD LA.
- [ ] **Do not claim conventional statistical significance** — n = 3; the exact sign-flip test
      floors at p = 0.25 and the bootstrap interval is just the observed min/max. Use
      "suggestive, not confirmatory".

---

## Additional items surfaced by the QA pass (not in the original list)

- [ ] **Cite Table 01 v2 and Table 05 v2**, which carry the new `comparison_object` markers
      distinguishing TRAINED from POST-HOC results
      (`BLACK_BOOK_TERMINOLOGY_FINALIZATION_v1.md` §3).
- [ ] **Never write "the official test was never opened"** — Notebook 03 opened it by design
      on 2026-08-12, and the one-time confirmatory run opened it on 2026-08-26.
- [ ] **State that Experiment-B post-guard counts are not a subset** of the 70% pixel-random
      split — some Qingyun classes have slightly more post-guard training pixels.
- [ ] **Do not cite** `Table_ClassLevel_Mechanism_Summary_v2.csv`,
      `audit/{scene}_ltlc_class_statistics.csv`, or
      `audit/final_training_imbalance_summary.csv` — all carry counts under bare or
      misleading names (`FINAL_TABLE_QA_v1.md` §1, restricted list).
- [ ] **Present the Qingyun seed-3407 zero paired deltas as an exact identity** (τ = 0), never
      as missing or stale data (`PAIRED_DELTA_CORRECTION_NOTICE_v1.md`).

---

## Binding references

| Need | Document |
|---|---|
| What may / may not be claimed | `FINAL_CLAIM_BOUNDARIES_v1.md` |
| Chapter structure and all 25 content sections | `BLACK_BOOK_WRITING_HANDOFF_v1.md` |
| Figure paths, grades, captions | `BLACK_BOOK_FINAL_FIGURE_MANIFEST_v1.md` |
| Which table version to cite | `BLACK_BOOK_TERMINOLOGY_FINALIZATION_v1.md` §6 |
| Reproducibility appendix text | `BLACK_BOOK_REPRODUCIBILITY_NOTE_v1.md` |
| Governance disclosure | `THESIS_PROTOCOL_GOVERNANCE_PARAGRAPH_v1.md` |

## Standing prohibitions during writing

No new training · no new inference · no official-test rerun · no Experiment-B CE on official
test · no hyperparameter tuning · no method development · no deletion or overwriting of
historical artifacts. Future method ideas belong in **Future Work** only.
