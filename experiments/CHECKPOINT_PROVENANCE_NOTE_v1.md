# CHECKPOINT PROVENANCE NOTE v1

No model checkpoints are stored in this working copy. All 36 Experiment-B checkpoints remain
in the master archive `CSE498/LTLC/`, together with their manifests and hash records.

## Where the checkpoints live

| Set | Canonical master path |
|---|---|
| Loose Experiment-B checkpoints (CE, Pingan Balanced Softmax, Qingyun LA-loss tau0p5) | `LTLC/runs/experiment_b_spatial_validation_v1/<method>/<scene>/[<config>/]seed<N>/` |
| 24 of 36 checkpoints available ONLY here | `LTLC/migrations/LTLC_Notebook06A_ExperimentB_28of36_PreLA_Kaggle_to_Colab_SELF_CONTAINED_MIGRATION_v1.zip` |
| Pingan LA-loss set, cumulative | `LTLC/experiment_b_colab_persistence/...36of36...MIGRATION_v1.zip` |

`28of36` + `36of36` together cover all 41 distinct `best_valAA` filenames. Internal prefixes:
`LTLC/` in the 28of36 base, `LTLC_DELTA/` in the deltas.

## The six checkpoints scored on official test

Full SHA-256 digests are recorded in
`../08_official_test/official_test_confirmation_results.json` and in
`../09_results/tables/Thesis_Table_09_OfficialTest_Confirmation_v1.csv`:

```
Pingan  42   c233ab73a8ae1cc58279d8a7285b644cf4dc648173fc69d435ab36a93731483e
Pingan  123  cf1162fd0b97b23f6455d9fcd75f45a9460f5d54a9cc519ab41f6f63a3279294
Pingan  3407 e311dc7e676953327835a6625bf84bff2b61ba259d94fc3d6351b6899151cf8d
Qingyun 42   ee25de80c873e05c94e3806869d7b5efc656c31bf008c6571563d4935490f9aa
Qingyun 123  7cef532a3222a7baff696016bf882d8878510177c08df7e70d3f9fcd48c942e8
Qingyun 3407 ba4579589489c419d9133a3f43f7160f58b1693acdab1dd52fda3dd8c67deeb2
```

Each on-disk file hash equals the hash recorded in the result JSON: the evaluated weights are
the retained weights. Per-scene geometry (Pingan patch 13 / radius 6, 519,546 params; Qingyun
patch 11 / radius 5, 256,886 params) is verified in
`../08_official_test/OFFICIAL_TEST_TECHNICAL_VERIFICATION_v1.md` sections 2-3.

Archive manifests and hash records are in `../11_reproducibility/`.
