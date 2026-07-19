# Session · 2026-07-19 · r3-shallow-refuse

> **Status:** `in-progress`

Intent: task R3 under ORDER 048 — turn the shallow-clone prose trap in
`scripts/measure_grounded_skills.py` into an enforced refuse-to-publish: when
`--json` is requested and any measured repo is a shallow clone (whose M4
git-history metrics would be silently zeroed), refuse to write the JSON, print
a loud machine-greppable `REFUSE:` marker to stderr, and exit non-zero (2).

- **📊 Model:** Opus 4.8 · high · guard build
- ⚑ Self-initiated: no — owner-directed slice (ORDER 048 / task R3).

About to: add the refuse condition to `main()`'s `--json` publish path only
(reuse the existing per-repo `shallow` flag already carried on
`counts["shallow"]` / `RepoResult.merged`), leaving the markdown/stdout path
unchanged (it already soft-nulls shallow rows); add a shallow-refuse test plus
a positive full-clone-writes-JSON test to
`tests/test_measure_grounded_skills.py`.
