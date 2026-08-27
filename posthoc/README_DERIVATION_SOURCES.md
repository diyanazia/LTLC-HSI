# 07_posthoc — DERIVATION SOURCES, NOT ACTIVE THESIS TABLES

The Notebook-06B `*_v2.csv` files here are the **derivation sources** behind the mechanism and
calibration analysis. They are provided so the numbers can be traced.

**The ACTIVE thesis tables are in `../09_results/tables/`.** Where a terminology-finalized
version exists, cite that one.

## Terminology (binding)

- **POST-HOC STANDARD LA** — `z - tau * log(pi + eps)` applied to **frozen CE validation
  logits**. No retraining. This is what the paired-delta and calibration tables measure.
- **TRAINED LA-LOSS** — a **separately trained** Experiment-B model. This is what the run
  ledger and Tables 01/02/09 measure.

Never conflate them. Conflating them already caused one documented error - see
`../10_final_qa/PAIRED_DELTA_CORRECTION_NOTICE_v1.md`.

## Do not cite directly

- `Table_ClassLevel_Mechanism_Summary_v2.csv` - bare `train_count` (post-guard). Cite
  `../09_results/tables/Thesis_Table_04_PerClass_Frequency_and_Mechanism_v2.csv`.
- `Table_Paired_Recognition_Deltas_v2.csv` / `_MeanStd_v2.csv` - **verified correct**, but cite
  the v3 reissue in `../09_results/tables/` for unambiguous column names.
- `Table_PerClass_Rarity_Difficulty_and_AdaptiveGain_v2.csv` - appendix only, with the
  count-concept caption.

## Qingyun seed 3407

The exact zeros in the paired-delta tables are a **mathematical identity**: the post-hoc search
selected tau = 0, making the LA transform the identity, so LA = CE = LTLC exactly. They are not
missing or stale data.
