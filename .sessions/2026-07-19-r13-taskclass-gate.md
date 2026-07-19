# R13 — exit-affecting PL-004 task-class gate on the born-red added card

> **Status:** `in-progress`

**Session:** 2026-07-19 · Self Improvement work-loop · substrate-kit
**Baton:** R13 (fold the PL-004 task-class check into the exit-affecting born-red `check_added_card` grader, scoped to the PR's OWN added card) — fm ORDER 048 standing grant.

**About to do:** fold the PL-004 task-class check (segment-3 of the `📊 Model:`
line ∈ the 9 `MODEL_TASK_CLASSES`) into the EXIT-AFFECTING born-red
`check_added_card` grader in `src/engine/checks/check_session_log.py`, scoped
ONLY to the PR's own added card's complete-branch (the `check_log` branch, after
the born-red HOLD clears). An off-taxonomy `📊 Model:` class on the PR's OWN card
reds at CI exactly like an unflipped born-red badge does. Reuse the existing
`engine.grammar` parser + `MODEL_TASK_CLASSES` tuple (no duplication). Fail-open:
a card with no parseable `📊 Model:` line stays silent (the marker checks own the
missing-line case). The fleet-wide `check_model_line` advisory window STAYS
advisory+windowed — untouched. Add both-direction mutation tests; rebuild dist.

- **📊 Model:** Opus 4.8 · high · feature build (exit-affecting PL-004 task-class gate on the born-red added card + tests + dist rebuild)
- **⚑ Self-initiated:** R13 is baton work (fm ORDER 048 standing grant — decide, build, land on green). Decide-and-flag calls within it: (1) factored a private `_last_model_payload` last-valid-wins helper in `check_session_log` (reusing `engine.grammar.parse_model_payload` + the class tuple) rather than importing `check_model_line` — that module imports FROM `check_session_log`, so the reverse edge would be circular; the helper is underscore-named so it does not match the `check_*(` parity regex and STRICT_SUBCHECKS stays 7; (2) scoped strictly to the complete-branch of `check_added_card` (diff-aware, single added card) so no historical/merged card can be retroactively reddened.

## What shipped (PR #PENDING)

Folded the PL-004 task-class rule into the exit-affecting born-red added-card
grader. `check_added_card`'s complete-branch (`check_log`) now also appends a
task-class finding when the added card's `📊 Model:` line carries a task-class
segment that does NOT prefix-match one of the 9 `MODEL_TASK_CLASSES` — so an
off-taxonomy class (e.g. `kit-feature`) on the PR's OWN card reds at CI exactly
like an unflipped born-red badge. Two private helpers do it — `_last_model_payload`
(last-valid-wins scan reusing `engine.grammar.parse_model_payload`, code-span /
fence / `[[fill:]]` aware) and `_task_class_findings_for_card` (prefix-match vs
the shared 9-class tuple; fail-open on a missing/malformed line). No new
top-level `check_*(` call is registered in `_extra_check_findings` — the added-card
lane is extended in place — so `EXPECTED_STRICT_SUBCHECKS` stays 7 and the parity
test is untouched. The fleet-wide `check_model_line` advisory (windowed to the 10
newest cards) is unchanged; only the PR's own added card is graded exit-affecting,
so no historical card is retroactively reddened.

Files: `src/engine/checks/check_session_log.py` (grammar imports + two private
helpers + complete-branch wiring + docstring), `tests/test_checks.py` (three new
tests: valid class passes, off-taxonomy class reds, missing-line fail-open),
`dist/bootstrap.py` (rebuilt).

## 💡 Session idea

**Exit-affecting the exact-model-ID rule on the born-red added card too.** R13
folds only the task-class (segment-3) rule into the born-red gate; the sibling
`EXACT_MODEL_ID_RE` rule (segment-1: a card recording an exact model-ID token
instead of a family-level name — the ORDER 012 fleet-reporting bar) stays
advisory+windowed and can merge green on a NEW card the same way an off-taxonomy
class used to. The parser + regex are already shared in `engine.grammar`, and
`_last_model_payload` already extracts the model segment, so exit-affecting it on
the PR's own added card is a one-conditional follow-on with the same
no-retroactive-redden scoping. Deduped: grepped the groom doc + `docs/ideas` for
`exact-id` / `model-ID` / `family-level` — R11 recipes-applies-when, R12
folded-gate, R13 (this) task-class; none touch segment-1 enforcement. Distinct.

## ⟲ Previous-session review

Previous session — **R12 folded-gate remediation snippet (PR #510)**. Did well:
it kept the folded-gate work advisory-only and diff-aware, and carried the dist
rebuild + byte-pin cleanly. Concrete system/workflow improvement this session
surfaces: R13 is the natural exit-affecting complement to the advisory-first
`check_model_line` — the kit has repeatedly shipped a *fleet-wide advisory* first
(migration pressure, no locked door) and then, once the taxonomy is stable,
folded the same rule into the *PR's-own-card* born-red gate as exit-affecting.
That advisory→born-red-gate promotion is now a recognizable, repeatable pattern
(effort/exact-ID are the remaining un-promoted segments); worth naming it
explicitly in `docs/` as a standing "how a payload rule graduates" recipe so a
future session reaches for it instead of re-deriving the scoping each time.
