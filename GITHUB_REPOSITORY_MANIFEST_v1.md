# GITHUB REPOSITORY MANIFEST v1

**Date:** 2026-08-27 · **Repository:** `CSE498/LTLC_GITHUB/`
**Canonical sources (unmodified):** `CSE498/LTLC/` and `CSE498/LTLC_BLACKBOOK_FINAL/`

**150 files · 9.01 MB**

Per-file provenance, both SHA-256 digests and derivation reasons are in
`GITHUB_REPOSITORY_MANIFEST_v1.csv`.

---

## Provenance categories

| Category | Files | Meaning |
|---|---:|---|
| `BYTE_IDENTICAL_COPY` | 137 | Copied unchanged; `github_sha256` equals `canonical_source_sha256` |
| `DERIVED_PUBLIC_SANITIZED_COPY` | 1 | Content redacted for public release; **no scientific value altered** |
| `DERIVED_PORTABLE_PUBLIC_COPY` | 3 | Path resolution made repository-relative; **no scientific logic altered** |
| `AUTHORED_GITHUB_DOCUMENT` | 9 | Written for this repository; no upstream source |

**Byte-identical hash mismatches: 0.**

## The four derived files

### `experiments/official_test/OFFICIAL_TEST_TECHNICAL_VERIFICATION_v1.md`

- **Category:** `DERIVED_PUBLIC_SANITIZED_COPY`
- **Canonical source:** `CSE498/LTLC_BLACKBOOK_FINAL/08_official_test/OFFICIAL_TEST_TECHNICAL_VERIFICATION_v1.md`
- **Canonical source SHA-256:** `f51219ba43b041d9f891c2b0b06a88429addbe6db69a7049e780311c6fdd8d8a`
- **Public SHA-256:** `3eba9b57c96803d3f9e2bb3bce9892565e5b6283a6a8b064286c93cc710fb63f`
- **Reason:** Replaced two absolute local Windows paths with <LOCAL_PROJECT_ROOT>/... to avoid publishing a machine username. No scientific value, hash, timestamp, conclusion or finding changed.

### `src/build_clean_tables.py`

- **Category:** `DERIVED_PORTABLE_PUBLIC_COPY`
- **Canonical source:** `CSE498/LTLC_BLACKBOOK_FINAL/05_code/build_clean_tables.py`
- **Canonical source SHA-256:** `61bef4ec10987db1649419e9780113111a5c44c461295c74bcdb7a296354c7c1`
- **Public SHA-256:** `b63e98faff6398b1bbdf834ad8bd4365a9e01599581157eb665226fce5261a1c`
- **Reason:** Replaced hardcoded sandbox output path with pathlib repository-relative resolution and removed a private Google Drive folder identifier from the docstring. No table content, formula or numerical value changed.

### `src/make_figures_finalqa_v1.py`

- **Category:** `DERIVED_PORTABLE_PUBLIC_COPY`
- **Canonical source:** `CSE498/LTLC_BLACKBOOK_FINAL/05_code/make_figures_finalqa_v1.py`
- **Canonical source SHA-256:** `2095c14edea18815c4b1358c374177cbb37e113f3d42e3ba67815101bd1c2e74`
- **Public SHA-256:** `59315ca51bf6e50e3936a8fa2a36e9d78a7b29ab01f8a46d909928b847c28deb`
- **Reason:** Replaced master-archive-relative paths with pathlib repository-relative resolution matching the public layout. No plotted value, palette, axis or scientific content changed.

### `src/stats_analysis.py`

- **Category:** `DERIVED_PORTABLE_PUBLIC_COPY`
- **Canonical source:** `CSE498/LTLC_BLACKBOOK_FINAL/05_code/stats_analysis.py`
- **Canonical source SHA-256:** `70b0af381a6fe9e5eebdcd39fe8ba43458a3d9b7dd5be0de954146dc25343277`
- **Public SHA-256:** `7f167a1af6028f13b8019ae4e6462a3e0ef778fab11f5382d52ef104a8825660`
- **Reason:** Replaced hardcoded sandbox paths (sandbox-absolute) with pathlib repository-relative resolution; added explicit utf-8 encoding on the ledger read. No formula, parameter, selection logic or numerical computation changed.

---

## Contents by directory

| Directory | Files |
|---|---:|
| `(root)` | 7 |
| `dataset_metadata` | 14 |
| `docs` | 9 |
| `experiments` | 11 |
| `experiments/official_test` | 4 |
| `posthoc` | 17 |
| `preprocessing` | 9 |
| `protocol` | 12 |
| `reproducibility` | 30 |
| `results/figures` | 9 |
| `results/tables` | 11 |
| `splits` | 4 |
| `src` | 13 |

---

## Public-release sanitization pass (2026-08-27)

| Check | Result |
|---|---|
| Windows user paths (`C:\Users\...`) | **0** |
| macOS user paths (`/Users/...`) | **0** |
| Linux home paths (`/home/<user>/...`) | **0** |
| Email addresses | **0** |
| AWS keys / GitHub tokens / private keys / API secrets | **0** |
| Inline password/secret assignments | **0** |
| Private Drive folder identifiers | **0** (one removed from a script docstring) |
| Files > 25 MB / 50 MB / 100 MB | **0 / 0 / 0** |
| Raw cubes, PCA caches, split arrays, checkpoints, archives | **none** |
| Virtual environments | **none** |

All detection patterns were self-tested against known-positive probes before the scan, so a
zero result reflects absence rather than a silently broken regular expression.

## Known remaining paths — reviewed and retained

`/content/drive/MyDrive/...` appears **272 times** across 8 notebooks and 5 frozen JSON
artifacts. These are retained deliberately:

- It is the **standard Colab mount point**, identical for every Colab user, and contains **no
  personal identifier** — it is machine-generic, not machine-specific.
- The frozen JSON artifacts are **scientific provenance records**; editing them would break
  hash-match with the master archive and alter recorded evidence.
- The notebooks are published byte-identical to the frozen originals.

`http://www.w3.org/...` appears in notebook outputs as SVG namespace declarations, and
`https://localhost:8080/` as Colab widget endpoints. Both are inert.

## Portability of published scripts

| Script | Classification |
|---|---|
| `src/stats_analysis.py` | **PORTABLE AFTER CURRENT SANITIZATION** — now repo-relative |
| `src/build_clean_tables.py` | **PORTABLE AFTER CURRENT SANITIZATION** — now repo-relative |
| `src/make_figures_finalqa_v1.py` | **PORTABLE AFTER CURRENT SANITIZATION** — repo-relative; the split-map figure additionally needs a local copy of the split arrays, which are not redistributed |
| `src/VALIDATION_REPRO_CHECK.py` | **PORTABLE AS-IS** — no absolute paths |
| `src/SEALED_TEST_v2.py` | **PORTABLE AS-IS** — `PROJECT_ROOT` is `Path(__file__)`-relative. Contains a `/content/drive` argument inside an optional Colab `drive.mount()` call that no-ops outside Colab. Left byte-identical because this is the script that produced the one-time official-test result |
| `src/*.ipynb` (7 notebooks) | **DOCUMENTED ONLY** — Colab-authored, retain original mount paths; published unchanged as the historical record |

## Licensing status

**PENDING.** `LICENSE` was removed and replaced with `LICENSE_PENDING.md`. `CITATION.cff`
carries **no `license:` field**, and `README.md` section 19 states that no permission should
be inferred. The QUH dataset, HybridSN, and every third-party long-tail method remain under
their own terms; this project claims ownership of none of them.

## Not published

Raw QUH cubes · derived PCA cubes · split `.npz` label arrays · official-test index/label
arrays · model checkpoints · migration and persistence archives · virtual environments ·
scratch notebooks · the superseded `Fig_N5` figure · pre-terminology table versions · the
superseded v1 sealed-test script. See `README.md` §11 for dataset acquisition and
`reproducibility/MASTER_ARCHIVE_PATH_MAP_v1.md` for where each item lives.
