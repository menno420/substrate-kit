# R15 — exit-affecting effort gate on the born-red added card

> **Status:** `complete`

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

## What shipped (PR #514)

The segment-2 (effort) exit-gate — the last leg of the `📊 Model:` line
exit-gate trilogy (R13 = segment-3 task-class, R14 = segment-1 model-ID, R15 =
segment-2 effort). New private helper `_effort_findings_for_card` in
`src/engine/checks/check_session_log.py`, an exact one-conditional sibling of
R14's `_exact_model_id_findings_for_card`, wired into `check_added_card`'s
complete-branch beside the R13/R14 extends and scoped to the single added card.
An effort segment that is neither one of `MODEL_EFFORT_VALUES` = {low, medium,
high} nor the sanctioned `unrecorded` carve-out reds the PR's OWN complete card
at CI exactly like an unflipped born-red badge; fail-open on a missing/malformed
line. The canonical `MODEL_EFFORT_UNRECORDED = "unrecorded"` was relocated up to
the shared leaf `grammar.py` (beside `MODEL_EFFORT_VALUES`) so the fleet advisory
(`check_model_line`) and this exit-gate accept the carve-out from one source of
truth; `check_model_line` keeps a re-export. Underscore-named helper —
`EXPECTED_STRICT_SUBCHECKS` stays 7.

**Evidence.** `python3 -m pytest tests/ -q` → **1902 passed, 1 skipped** (1898
prior + 4 new R15 tests: valid-tier-passes, off-taxonomy-reds, `unrecorded`-
exempt, missing-line-fail-open). Dist rebuilt (`src/build_bootstrap.py`) and
byte-pinned. `dist/bootstrap.py check --strict` → exit 0. Namespace/symbol-guard
subset → 22 passed (no duplicate top-level `MODEL_EFFORT_UNRECORDED` after the
grammar relocation). Cold-adoption smoke reproduced locally step-for-step (bare
adopt RED → render+enforce+session-card → `check --strict` exit 0 → session-log
gate on `smoke · low · docs-only` exit 0): the R15 gate does not touch the
adopter template card or the smoke fixture (both file a valid `low` tier). Three
pre-existing added-card tests that used a placeholder `· e ·` effort were
retagged `· high ·` — a well-formed complete card now carries a taxonomy effort.

## 💡 Session idea

**A data-driven segment-gate table for `check_added_card`.** R13/R14/R15 shipped
three near-identical helpers — each reads `_last_model_payload`, tests ONE
`📊 Model:` segment against a set/regex (with an optional carve-out), and emits
one card-scoped finding quoting `MODEL_LINE_TAUGHT_FORMAT`. The next segment gate
(e.g. the optional 4th `tokens_out` integer, or a future segment) will be a
fourth copy. Idea: collapse the three into one table `((segment_key, validator,
carve_out, finding_kind), …)` iterated by a single `_segment_findings_for_card`,
so a new segment gate is a one-row addition, not a new helper + wiring +
docstring + four tests. Deduped against `docs/ideas/model-line-*` (those cover
the advisory lint, the false-red fix, and the `unrecorded` marker — none propose
consolidating the exit-affecting added-card gates). Small/decided-lane refactor;
a good grooming pick once the trilogy has settled a few sessions.

## ⟲ Previous-session review

**R14 (exact-model-ID gate, #513)** landed cleanly: it reused `_last_model_payload`
and `EXACT_MODEL_ID_RE` with zero duplication and scoped the gate to the single
added card — the exact template R15 followed. What it (and R13) missed, surfaced
only by R15: the 11 test fixtures carrying a placeholder `📊 Model: m · e ·
docs-only` line filed an off-taxonomy effort `e` that was invisible until R15
turned effort into a gated segment, then reddened 3 of them. **Workflow
improvement:** when a session adds a per-segment gate, the sibling test fixtures'
"well-formed" placeholder line should use ALL-valid segment values from the start
— ideally a shared `WELL_FORMED_MODEL_LINE` constant in the test module — so the
NEXT segment gate can't retroactively break fixtures that were only ever meant to
exercise a different segment. A single canonical fixture line is the enforce-
don't-exhort form of "a placeholder must be well-formed on every axis."
