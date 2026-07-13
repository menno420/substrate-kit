# 2026-07-13 — announce guard-fire ledger writes during `check`

> **Status:** `in-progress`

About to happen: make `cmd_check` aggregate its `record_guard_fires()`
return counts and print one summary line when a run appended records to
`.substrate/guard-fires.jsonl` (naming it the telemetry ledger — commit the
delta with your session, do not revert), add the commit-the-delta doctrine
note to `telemetry/README.md`, pin the behavior in tests, regenerate
`dist/bootstrap.py`, and verify with the full pytest suite +
`python3 dist/bootstrap.py check --strict`.
