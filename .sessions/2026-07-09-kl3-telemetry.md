# Session 2026-07-09 — KL-3: telemetry substrate

> **Status:** `in-progress`

**About to do (founding plan §10 KL-3 row + §5.2/§5.3):** guard-fire JSONL
writers at the two choke points (`cmd_check`'s finding loop + `cmd_hook`'s
dispatch) appending to `.substrate/guard-fires.jsonl` (`did_not_run` stays
reader-derived from the Checks API, never written in CI); the
reasons-required allowlist port (`check-exceptions.yml` — reason-less entries
are refused, an entry IS the false-positive/accepted-risk verdict event); the
`📊 Model:` run-report line + session-close harvest into
`telemetry/model-usage.jsonl` (PL-004 record shape, `tokens_out`
null-tolerated per KF-9); the session-log checker needle for the line;
`telemetry/allocation-ladder.md` seeded with the §5.2 ladder + KF-8 numbers.
Dogfood: this card carries the line; session-close writes the kit repo's
first model-usage row (D6's kit-side half).
