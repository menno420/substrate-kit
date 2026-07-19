# R14 — exit-affecting exact-model-ID gate on the born-red added card

> **Status:** `in-progress`

**Session:** 2026-07-19 · Self Improvement work-loop · substrate-kit
**Baton:** R14 (fold the segment-1 `EXACT_MODEL_ID_RE` check into the exit-affecting born-red `check_added_card` grader, scoped to the PR's OWN added card) — fm ORDER 048 standing grant + coordinator follow-on to PR #512 (R13).

**About to do:** fold the segment-1 exact-model-ID check (the `📊 Model:` line's
model segment must be a FAMILY-LEVEL name, never an exact model-ID token like
`claude-opus-4-8` — the ORDER 012 fleet-reporting bar) into the EXIT-AFFECTING
born-red `check_added_card` grader in `src/engine/checks/check_session_log.py`,
scoped ONLY to the PR's own added card's complete-branch (the `check_log` branch,
after the born-red HOLD clears), as an exact sibling of R13's
`_task_class_findings_for_card`. An exact-model-ID segment-1 on the PR's OWN card
reds at CI exactly like an unflipped born-red badge does. Reuse the existing
`engine.grammar.EXACT_MODEL_ID_RE` + `_last_model_payload` (no duplication).
Fail-open: a card with no parseable `📊 Model:` line, or a `[[fill:]]` /
code-span / family-level segment-1, stays silent. The fleet-wide
`check_model_line` advisory window STAYS advisory+windowed — untouched.
`EXPECTED_STRICT_SUBCHECKS` stays 7 (underscore-named helper, no new top-level
`check_*(`). Add both-direction mutation tests; rebuild dist.

- **📊 Model:** opus-4.8 · high · feature build (exit-affecting exact-model-ID gate on the born-red added card + tests + dist rebuild)
- **⚑ Self-initiated:** R14 is baton work (fm ORDER 048 standing grant + coordinator follow-on to R13 — decide, build, land on green). Decide-and-flag calls within it: (1) reused R13's private `_last_model_payload` last-valid-wins helper to extract the model segment and `engine.grammar.EXACT_MODEL_ID_RE` for detection — no new regex, no reverse import of `check_model_line` (that module imports FROM `check_session_log`, so the edge would be circular); the new helper is underscore-named so it does not match the `check_*(` parity regex and STRICT_SUBCHECKS stays 7; (2) scoped strictly to the complete-branch of `check_added_card` (diff-aware, single added card) so no historical/merged card can be retroactively reddened.

## What shipped (PR #TBD)

_pending — filled at flip._

## 💡 Session idea

_pending — filled at flip._

## ⟲ Previous-session review

_pending — filled at flip._
