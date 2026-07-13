# 2026-07-13 — heartbeat `updated:` prefix case-insensitivity

> **Status:** `in-progress`

⚑ Self-initiated: friction → guard from PR #326 — a live heartbeat written
as `Updated:` failed `[status-no-heartbeat]` because `UPDATED_LINE_RE`
requires a lowercase prefix; this session makes the enforcer accept the
casing variant (checker fix over exhortation, PL-007) with tests + dist
regen.

About to happen: make `engine.grammar.UPDATED_LINE_RE` match the `updated:`
prefix case-insensitively, pin both casings in the test suite, regenerate
`dist/bootstrap.py` via `python3 src/build_bootstrap.py`, verify with the
full pytest suite + `python3 dist/bootstrap.py check --strict`.
