# Guard-parity meta-test — kit-vs-adopter guard drift detector

> **Status:** `in-progress`

About to do: add `tests/test_guard_parity.py` — a meta-test that fails CI when
an enforcing `kit-quality` guard in `.github/workflows/ci.yml` has no mirrored
counterpart in the generated adopter CI (`src/engine/adopt.py`
`live_ci_workflow()`), unless allowlisted as kit-only with a reason. Closes the
drift class PR #457 had to close by hand.
