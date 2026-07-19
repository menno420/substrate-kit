# R15 — exit-affecting effort gate on the born-red added card

> **Status:** `in-progress`

**Session:** 2026-07-19 · Self Improvement work-loop · substrate-kit
**Baton:** R15 (fold the segment-2 effort check into the exit-affecting born-red `check_added_card` grader, scoped to the PR's OWN added card) — fm ORDER 048 standing grant + coordinator follow-on to PR #513 (R14) / #512 (R13). Completes the `📊 Model:` line exit-gate trilogy.

**About to do:** fold the segment-2 effort check (the `📊 Model:` line's effort
segment must be one of `MODEL_EFFORT_VALUES` = {low, medium, high} OR the
sanctioned terminal carve-out `MODEL_EFFORT_UNRECORDED` = `unrecorded`) into the
EXIT-AFFECTING born-red `check_added_card` grader in
`src/engine/checks/check_session_log.py`, scoped ONLY to the PR's own added
card's complete-branch (the `check_log` branch, after the born-red HOLD clears),
as a one-conditional sibling of R14's `_exact_model_id_findings_for_card` and
R13's `_task_class_findings_for_card`. An off-value effort segment on the PR's
OWN card reds at CI exactly like an unflipped born-red badge does. The one
subtlety: relocate the canonical `MODEL_EFFORT_UNRECORDED = "unrecorded"`
definition from `check_model_line.py` up to the shared leaf `grammar.py` (next to
`MODEL_EFFORT_VALUES`) so BOTH the fleet advisory and this exit-gate accept the
retro-sweep honest marker from one source of truth (keeping a re-export in
`check_model_line` for the test that imports it there). Reuse the existing
`_last_model_payload` (no duplication); no reverse import of `check_model_line`
(that module imports FROM `check_session_log`, so the edge would be circular).
Fail-open: a card with no parseable `📊 Model:` line, or a missing effort
segment, stays silent. The fleet-wide `check_model_line` advisory window STAYS
advisory+windowed — untouched. `EXPECTED_STRICT_SUBCHECKS` stays 7
(underscore-named helper, no new top-level `check_*(`). Add both-direction
mutation tests + the `unrecorded` carve-out test; rebuild dist.

- **📊 Model:** opus-4.8 · high · feature build (exit-affecting effort gate on the born-red added card + grammar relocation + tests + dist rebuild)
- **⚑ Self-initiated:** NOT self-initiated — R15 was **coordinator-directed**: a peer session relayed the owner's authorization to build the last un-promoted segment-2 (effort) analog of R13's segment-3 and R14's segment-1 gates, owner-authorized under the fm ORDER 048 standing grant. A directed follow-on to R14 (#513), not an unprompted promotion. Decide-and-flag calls: (1) relocated `MODEL_EFFORT_UNRECORDED` to `grammar.py` as the single source of truth so the `unrecorded` carve-out survives in both the advisory and the exit-gate, keeping a re-export in `check_model_line` so `tests/test_check_model_line.py`'s import-from-that-module still resolves; (2) reused R13/R14's private `_last_model_payload` extractor — no new parser, no reverse import of `check_model_line`; the new helper is underscore-named so it does not match the `check_*(` parity regex and STRICT_SUBCHECKS stays 7; (3) scoped strictly to the complete-branch of `check_added_card` (diff-aware, single added card) so no historical/merged card is retroactively reddened.

## What shipped (PR [[fill: PR number]])

[[fill: what shipped summary]]

**Evidence.** [[fill: evidence]]

## 💡 Session idea

[[fill: idea]]

## ⟲ Previous-session review

[[fill: review]]
