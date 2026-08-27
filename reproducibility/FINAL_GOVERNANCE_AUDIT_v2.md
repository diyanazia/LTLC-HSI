# FINAL GOVERNANCE AUDIT v2 — official-test access

> **v2 supersedes v1.** `FINAL_GOVERNANCE_AUDIT_v1.md` is retained unchanged.
> v2 adds one newly verified event to the timeline — a **failed v1 sealed-test attempt at
> 2026-08-26T12:17:20.019717Z** — together with the primary evidence that it accessed no
> checkpoint or official-test data and produced no result. **The scientific conclusion of v1
> is unchanged.** See `GOVERNANCE_AUDIT_V1_TO_V2_CHANGELOG.md`.

**Date:** 2026-08-27 · **Scope:** Experiment B (Pingan, Qingyun) · **Status:** see Verdict (§7)

This audit was performed by reading primary artifacts, not the handoff summaries.
Filesystem mtimes are **unreliable** (every `LTLC/` file reads `2026-08-26 19:43`, a sync
artifact). All dates below are **embedded `created_utc` / `completed_at` fields**.

---

## 1. Artifacts consulted (primary)

| Ref | Path | Embedded date |
|---|---|---|
| A | `audit/notebook05_posthoc_ltlc/notebook05_terminal_validation_scientific_decision.json` | none embedded |
| B | `posthoc/notebook06b_experiment_b/terminal_validation_v1/LTLC_Notebook06B_ExperimentB_Terminal_Scientific_Decision_v1.json` | 2026-08-20T16:27:43Z |
| C | `releases/notebook06b_experiment_b_posthoc_v2/LTLC_Notebook06B_ExperimentB_FINAL_RELEASE_v2.json` | 2026-08-20T16:41:40Z |
| D | `audit/notebook06a_spatial_validation/experiment_b_training_protocol_v1_frozen.json` | pre-training (flags) |
| E | `audit/notebook06a_spatial_validation/experiment_b_spatial_validation_protocol_v1_frozen.json` | pre-split (flags) |
| F | `final_audits/notebook06a_experiment_b/..._36of36_FINAL_CLOSING_AUDIT_v1.json` | 2026-08-20T15:09:15Z |
| G | `results/notebook06a_experiment_b/..._VALIDATION_SUMMARY_FREEZE_v1.json` | 2026-08-20T15:37:38Z |
| H | `posthoc/.../recognition_search_v1/..._Posthoc_Recognition_Freeze_v1.json` | 2026-08-20T16:23:29Z |
| I | `audit/sealed_test_confirmation_run/official_test_confirmation_results.json` | 2026-08-26T16:58:29Z |
| J | `audit/notebook03_hybridsn/notebook03_master_audit.json` | 2026-08-12T21:49:18 |
| K | `Day1_Improvements_2026-08-26/README_DAY1_IMPROVEMENTS.md` | 2026-08-26 |
| **L** | **`LTLC/notebooks/Untitled1.ipynb`** — primary execution record of the failed v1 attempt (forensic review 2026-08-27) | **2026-08-26T12:17:20Z** |
| M | `Day1_Improvements_2026-08-26/scripts/SUPERSEDED_v1_DO_NOT_RUN__SEALED_TEST_run_once_in_colab.py` — the v1 code, byte-identical to cells 0/1 of L | 2026-08-26 |

---

## 2. Timeline (objectively established)

| # | Event | Evidence | Date |
|---|---|---|---|
| 1 | Protocol v3.1 fixed (split seed 2026, val fraction 0.3, seeds 42/123/3407) | `notebook01_protocol_metadata.json` | 2026-08-12T16:35Z |
| 2 | **Notebook 03 opens the official test** for HybridSN benchmark reproduction. Gate `official_test_authorized: true`. Nine `*_official_test_outputs.npz` produced. | J | 2026-08-12T21:49Z |
| 3 | Experiment-B **split protocol frozen** before split creation, before training, before any performance was seen (`split_rule_frozen_before_model_performance: true`, `performance_results_seen_before_freeze: false`, `official_test_used_for_split_design: false`) | E | pre-training |
| 4 | Experiment-B **training protocol frozen** before model construction, dataloader creation, inference and GPU training (`protocol_frozen_before_experiment_b_performance: true`). Per-dataset geometry pre-registered: Pingan patch 13 / 519,546 params; Qingyun patch 11 / 256,886 params. Official-test block: inference, dataset creation, dataloader creation, hyperparameter selection and checkpoint selection **all `false`**. | D | pre-training |
| 5 | 36/36 Experiment-B runs complete; closing audit PASS; 530 explicit official-test safety assertions, 0 violations | F | 2026-08-20T15:09Z |
| 6 | **Rank-1 method per dataset frozen** on validation only (Pingan Balanced Softmax; Qingyun LA-loss τ=0.5). Boundary text: *"These are Experiment-B spatial-validation robustness results. They must not be described as official-test performance."* | G | 2026-08-20T15:37:38Z |
| 7 | Post-hoc recognition parameters frozen (α/β/τ grids, R1 β=0 both datasets) | H | 2026-08-20T16:23Z |
| 8 | **NB06B terminal decision**: `official_test_may_be_opened: false`, `required_action: STOP_METHOD_DEVELOPMENT_AND_KEEP_OFFICIAL_TEST_SEALED` | B | 2026-08-20T16:27Z |
| 9 | **NB06B final release**: `scientific_conclusion.official_test_may_be_opened: false`, `safety.official_test_accessed: false` | C | 2026-08-20T16:41Z |
| 10 | **(A) Day-1 package preparation.** Package assembled: significance tests, figures, cleaned tables, integrity notes, and both sealed-test scripts (superseded v1 + corrected v2). README §4 instructs the one-time sealed test as a required user action. | K, M | 2026-08-26 |
| **10a** | **(B) FAILED v1 ATTEMPT — 12:17:20.019717Z.** The v1 harness was launched once, in Colab on a Tesla T4 (python 3.13.15, torch 2.11.0+cu128). The one-time confirmation phrase *was* entered. **(C) Precise failure location:** `FileNotFoundError` raised inside `recover_hybridsn_class()`, called from `main()` at line 319 — the frozen HybridSN source notebook path did not resolve under the Colab mount. **(D) No checkpoint and no official-test data were accessed** (see §2a). **(E) No result artifact was written.** | **L** | **2026-08-26T12:17:20Z** |
| 10b | Two further cells in the same notebook attempted to `exec` the corrected **v2** script in Colab with `PREFLIGHT_ONLY = True` asserted; both aborted at `drive.mount` (`ValueError: Mountpoint must not already contain files`). **No v2 execution occurred in Colab.** | L | 2026-08-26 |
| 11 | **(F) Preflight** of the corrected v2 pipeline, locally (paths/shapes/member names only; **no test index or label VALUE read**) | session log | 2026-08-26T16:53:39Z |
| 12 | **(F) Validation reproduction** — `VALIDATION_REPRO_CHECK.py` executed against the Experiment-B **validation** split only; all six checkpoints reproduced their frozen ledger AA to five decimals; official-test file never opened | session log | 2026-08-26 ~16:54–16:57Z |
| 13 | **(G) SUCCESSFUL ONE-TIME OFFICIAL-TEST EVALUATION.** `SEALED_TEST_v2.py` executed once, locally on CPU (python 3.12.0, torch 2.13.0+cpu); official test scored for Experiment B; result file written and retained | I | **2026-08-26T16:58:29Z** |

Notebook 05 (A) carries the same gate (`official_test_may_be_opened: false`,
`required_action: STOP_METHOD_DEVELOPMENT_ON_CURRENT_VALIDATION_SPLITS`) but has no
embedded timestamp; it precedes NB06A/06B in the pipeline.

---

## 2a. The failed v1 attempt did NOT spend the scientific seal

Three independent lines of evidence, all from primary artifacts:

1. **Failure preceded all data loading.** The traceback in `notebooks/Untitled1.ipynb` shows
   execution terminating inside `recover_hybridsn_class()` — the architecture-recovery step —
   reached from `main()` before any checkpoint load, any split read, or any dataset
   construction. Nothing downstream of that call ran.

2. **The v1 implementation had no functional test-data loading path.** Its own docstring
   states that Section 4 (data loading) *"is a required plug-in point that you must fill in"*.
   Static inspection confirms it: the v1 source contains **zero** occurrences of
   `test_indices`, `test_labels_model`, or `fixed_split_seed2026`. Even had it passed the
   architecture step, it was structurally incapable of reading the official test set.

3. **No official-test result was produced.** No result artifact was written by that run, and
   `audit/sealed_test_confirmation_run/official_test_confirmation_results.json` — the only
   official-test result file in the repository — carries `timestamp_utc`
   `2026-08-26T16:58:29Z`, from the later corrected run, not 12:17:20Z.

The typed confirmation phrase at 12:17:20Z therefore records an *intent* to open the test set,
not an opening of it. **The official test was scored exactly once, at 16:58:29Z.** This does
not alter the contamination assessment (§6) or the verdict (§7).

---

## 3. Answers to the twelve audit questions

1. **Experiment-B model configurations frozen?** Before any Experiment-B model was
   constructed or trained (D, flags in §2 row 4). Pre-registered per-dataset geometry.
2. **Checkpoint selections frozen?** Policy `best_validation_AA` was fixed in the frozen
   training protocol (D, `checkpoint_policy`), with
   `official_test_used_for_checkpoint_selection: false`. Realised at 36/36 closing audit
   (F, 2026-08-20T15:09Z).
3. **Rank-1 per dataset frozen?** 2026-08-20T15:37:38Z (G) — six days before test access.
4. **What did Notebook 05 state?** `official_test_may_be_opened: false`,
   `official_test_used: false`, `official_test_dataset_created: false`,
   `official_test_dataloader_created: false`,
   `required_action: STOP_METHOD_DEVELOPMENT_ON_CURRENT_VALIDATION_SPLITS`.
   Disclosure: *"No Notebook 05 development decision used the official test set."*
5. **What did Notebook 06B state?** Terminal decision (B):
   `official_test_may_be_opened: false`, `official_test_status: SEALED`,
   `required_action: STOP_METHOD_DEVELOPMENT_AND_KEEP_OFFICIAL_TEST_SEALED`. Final release
   (C) repeats `official_test_may_be_opened: false`.
   **Note the wording: NB06B does not only stop method development — it explicitly says
   keep the official test sealed.** This is stronger than a development-only restriction
   and must not be paraphrased away.
6. **What did the Day-1 package instruct?** README §4: *"One-time sealed-test confirmation
   — YOU MUST RUN THIS YOURSELF."* This directly contradicts B and C.
7. **When was `VALIDATION_REPRO_CHECK.py` executed?** 2026-08-26, between the preflight
   (16:53:39Z) and the sealed run (16:58:29Z).
8. **Did it touch test data?** **No.** It reads only
   `split_indices/experiment_b_spatial_validation_v1/*_experiment_b_spatial_split_v1.npz`
   members `val_indices` / `val_labels_model`. The official split file is not opened by
   that script.
9. **When was `SEALED_TEST_v2.py` executed?** 2026-08-26T16:58:29Z.
10. **Was the test scored exactly once?** Yes. A single `environment` block with one
    timestamp; the script hard-refuses to run while `official_test_confirmation_results.json`
    exists; the file exists and has not been moved or deleted. No second result file exists
    anywhere in the repository. **One earlier launch occurred (12:17:20Z, v1 harness) but
    terminated before any data access and produced no result — see §2a.** The count of
    official-test *scorings* remains exactly one.
11. **Was anything changed after seeing official-test results?** **No scientific change.**
    One documentation-level configuration correction was made **before** the run, not after:
    the Qingyun `patch_size` was corrected from an erroneous working note (13) to the value
    pre-registered in the frozen protocol (11). That correction restores agreement with D,
    NB02 and NB03; it does not alter any selection. No method, hyperparameter, checkpoint,
    figure or conclusion was changed after the test results were seen.
12. **Was any test result used to rescue LTLC or select a different method?** **No.** LTLC
    was not evaluated on the official test at all. Only the two already-frozen rank-1
    *training-time* baselines were scored. The LTLC null result (B, C) stands unchanged and
    unrescued.

---

## 4. Objectively verified

- Every Experiment-B decision artifact predates test access by **six days**.
- All six evaluated checkpoints carry `official_test_used: false` in their own metadata.
- Official test ∩ Experiment-B train = **0** pixels; ∩ Experiment-B validation = **0**
  pixels, both scenes (recomputed 2026-08-26).
- All six checkpoints reproduced their frozen run-ledger validation AA to five decimals
  **before** the test set was opened.
- The Experiment-B split file is **byte-identical** to the `split_sha256` recorded inside
  the Pingan checkpoint (`7e7c6f58…`). Both PCA cubes are byte-identical to their frozen
  NB02 hashes.
- The test was scored once and the result file is intact.
- An earlier v1 launch (12:17:20Z) failed before model or test-data loading and wrote no
  result; evidence retained at `notebooks/Untitled1.ipynb` (KEEP_AUDIT, master archive).

## 5. Interpretation (explicitly labelled as such)

The following is **reasoning, not fact**:

> The NB05/NB06B gate travels with `STOP_METHOD_DEVELOPMENT…`, and its stated rationale is
> the absence of a robust LTLC recognition signal. On that reading it forbids opening the
> test set *to rescue or continue developing LTLC*, and today's run — scoring already-frozen
> training-time baselines, once, without iteration — falls outside its intent.

**Counter-reading that must be acknowledged:** NB06B's `required_action` string is
`STOP_METHOD_DEVELOPMENT_AND_KEEP_OFFICIAL_TEST_SEALED`. Taken literally, "keep the official
test sealed" is unconditional and is not limited to LTLC. Under that literal reading the run
violated the standing instruction regardless of what was scored.

Both readings are defensible. This audit does **not** adjudicate between them; it records
that the project owner authorised the run with full knowledge of the gate, and that the
scientific integrity of the number is unaffected either way (§4).

## 6. Contamination assessment

**No scientific contamination occurred.** Contamination would require an official-test
result to have influenced a method, hyperparameter, checkpoint, or method-development
decision. Every such decision is timestamped six days earlier, is recorded in frozen
artifacts with explicit `official_test_used: false` flags, and none has been modified since.

**A protocol-governance inconsistency does exist**, and it is documented rather than
concealed: two frozen artifacts instruct that the official test remain sealed, and a later
one-time confirmatory evaluation was nevertheless executed.

## 7. Verdict

> **PROTOCOL-GOVERNANCE INCONSISTENCY — NO SCIENTIFIC CONTAMINATION.**

## 8. The exact claim the thesis may safely make

The preferred claim **is supported** and may be used verbatim:

> "No official-test result influenced Experiment-B model selection, hyperparameter
> selection, checkpoint selection, or LTLC method development. All such decisions were
> frozen using the spatially disjoint validation protocol before the one-time confirmatory
> test evaluation."

It **must** be accompanied by the disclosure in
`THESIS_PROTOCOL_GOVERNANCE_PARAGRAPH_v1.md`. The claim above is about *influence*; it is
not a claim that the test was never opened, and it is not a claim that the run complied with
the earlier standing instruction.

**Prohibited phrasings:** "the official test was never opened" (Notebook 03 opened it by
design); "the official test remained sealed throughout" (it did not); any wording implying
the NB06B gate authorised the run.
