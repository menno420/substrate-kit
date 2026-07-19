# R8 — fast-lane prefix symmetry as a runtime check --strict sub-check

> **Status:** `in-progress`

**Session:** 2026-07-19 · Self Improvement work-loop · substrate-kit
**Baton:** R8 (fast-lane prefix symmetry runtime advisory) from docs/planning/2026-07-19-night-run-idea-groom.md

**About to do:** promote the B-3 kit-only pytest meta-test
(`tests/test_fastlane_prefix_symmetry.py`) to a runtime check
`src/engine/checks/check_fastlane_symmetry.py` so ADOPTERS catch their own
enabler↔guard prefix drift under `bootstrap check --strict`; wire it into
`cli._extra_check_findings` + `guards.STRICT_SUBCHECKS` (per the R8 recipe body,
which explicitly names both — the exit-affecting seam, distinct from R5/R7's
advisory-only seam), add it to `build_bootstrap.MODULE_ORDER`, rebuild dist, and
add a test. Then register the R7-surfaced `📊 Model`/`kit-feature` gate gap as a
cited idea (do not build it).
