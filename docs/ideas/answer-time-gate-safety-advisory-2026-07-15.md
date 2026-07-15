---
state: promoted
origin: lab
shipped_pr: 407
shipped_repo: menno420/substrate-kit
merged_date: 2026-07-15
outcome: shipped
---

# Answer-time gate-safety advisory for `verify_command` (2026-07-15)

> **Status:** `ideas`
>
> **State:** promoted → **shipped** kit PR #407 (2026-07-15, anticipated
> in-PR date; captured with the increment — the 💡 lived on the #405 card
> `.sessions/2026-07-15-gate-verify-command.md`, built the next wake):
> `engine.adopt.gate_test_command_advisory` + the `bootstrap answer` /
> `confirm` wiring (`cli._emit_gate_safety_advisory`).
> **Origin:** lab — the #405 session (gate-verify-command) shipped the
> honored-lane contract and immediately saw its silent-failure seam.

**One line:** a prose-y verify answer (`bootstrap answer verify_command
"pytest -q (all suites)"`) records silently today, and its gate-unsafety
surfaces only as the *absence* of the honored gate lane at the next
adopt/upgrade — the owner never learns their verify line cannot drive CI;
run `gate_test_command`'s gate-safety legs at the moment the value is
typed, when fixing it costs one retype instead of an adopt-cycle
round-trip.

## The shape

`gate_test_command_advisory(value, interpreter)` in `engine.adopt` — the
same one-slot shape legs the honored lane gates on (newline, unfilled
`${...}`, the `_GATE_TEST_COMMAND_SAFE_RE` allowlist), returned as a NOTE
that names the offending shape/characters plus a runnable rewrite when
stripping parenthetical annotations recovers a gate-safe command (the
observed websites shape). Honesty guards: an annotated *default* pytest
value is told the fallback already runs the equivalent (no "would drive
it" over-promise); a multi-line value never gets a rewrite (the whitespace
collapse would suggest a broken joined command); gate-safe values stay
silent. Wired at both filled-making moments — `cmd_answer` and
`cmd_confirm` — advisory prose only, recorded state and exit codes
untouched (the slot is still a fine CLAUDE.md verify line).

## Guard recipe

Tests pin the verdict matrix (`test_gate_test_command_advisory_verdicts`)
and the CLI emission at both moments incl. the other-slot no-op
(`test_cmd_answer_and_confirm_emit_the_gate_safety_advisory`) in
`tests/test_adopt.py`. Engine change → dist byte-pin.
