# THESIS PROTOCOL GOVERNANCE PARAGRAPH v1

Drop-in text for the Black Book protocol section. Do not soften it; the value of the
disclosure is that it is volunteered rather than discovered.

---

## Version A — full disclosure (recommended; protocol / methodology chapter)

> **Official-test protocol and a disclosed governance inconsistency.**
> The official test partition of each scene was used twice in this project, for two
> different purposes. Notebook 03 evaluated a Cross-Entropy HybridSN baseline on the
> official test as part of reproducing a published benchmark, which is measured on that
> partition by definition; those nine inference artifacts are retained in the repository.
> Experiment B was then conducted entirely on a spatially disjoint validation protocol.
> Every Experiment-B decision — the choice of long-tail method, every hyperparameter
> (τ, γ, C, α, β), the `best_validation_AA` checkpoint policy, and the rank-1 method per
> scene — was frozen and recorded in content-hashed artifacts dated 20 August 2026, and
> each trained checkpoint carries the flag `official_test_used = false`.
>
> Two of those frozen artifacts, the Notebook 05 and Notebook 06B terminal decisions, also
> recorded `official_test_may_be_opened: false`, with Notebook 06B stating the required
> action as "stop method development and keep the official test sealed". That instruction
> was issued because the rarity-adaptive LTLC component had produced no robust recognition
> signal, and no further method development on the consumed validation splits was
> warranted.
>
> On 26 August 2026 a single confirmatory evaluation of the two already-frozen rank-1
> configurations was nevertheless executed on the official test. This is disclosed here
> deliberately. The evaluation took place six days after every relevant decision had been
> frozen; it scored only the pre-selected training-time baselines, not LTLC; it was run
> exactly once; and no method, hyperparameter, checkpoint, figure, table or conclusion in
> this thesis was altered in response to its outcome. Independent verification confirmed
> that the official-test pixels intersect neither the Experiment-B training set nor its
> validation set, and that all six checkpoints reproduced their recorded validation
> accuracies before the test partition was opened.
>
> The claim this supports is therefore narrow and specific: **no official-test result
> influenced Experiment-B model selection, hyperparameter selection, checkpoint selection,
> or LTLC method development.** It is not a claim that the official test was never opened,
> nor that the run complied with the earlier standing instruction to keep it sealed. The
> instruction and the later evaluation are both recorded, and the reported test numbers are
> presented as a post-development confirmatory measurement rather than as evidence that
> guided any part of the study.

---

## Version B — condensed (results chapter, where a short pointer is enough)

> The official-test numbers reported here are a **post-development confirmatory
> measurement**, not a development signal. All Experiment-B method, hyperparameter and
> checkpoint decisions were frozen on the spatially disjoint validation protocol six days
> earlier and were not revised afterwards. Earlier project artifacts had recorded an
> instruction to keep the official test sealed; that instruction, and the decision to
> nevertheless perform a single confirmatory evaluation, are disclosed in full in the
> protocol chapter.

---

## Required accompanying facts (cite at least these)

- Rank-1 freeze: `LTLC_Notebook06A_ExperimentB_VALIDATION_SUMMARY_FREEZE_v1.json`,
  `created_utc` 2026-08-20T15:37:38Z.
- Standing gate: `LTLC_Notebook06B_ExperimentB_Terminal_Scientific_Decision_v1.json`,
  `created_utc` 2026-08-20T16:27:43Z.
- Confirmatory run: `official_test_confirmation_results.json`,
  `timestamp_utc` 2026-08-26T16:58:29Z. Run once; result file retained.
- Disjointness: official test ∩ Experiment-B train = 0 px; ∩ Experiment-B validation = 0 px.
- Full audit: `FINAL_GOVERNANCE_AUDIT_v1.md`.

## Do not write

- "The test set was never opened."
- "The official test remained sealed throughout the project."
- "The confirmatory run was authorised by the protocol." (It was authorised by the project
  owner, against a standing instruction recorded in the artifacts.)
- Any test-set comparison against Cross-Entropy — no Experiment-B CE official-test result
  exists.
