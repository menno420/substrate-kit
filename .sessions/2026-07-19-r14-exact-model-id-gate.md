# R14 — exit-affecting exact-model-ID gate on the born-red added card

> **Status:** `complete`

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
- **⚑ Self-initiated:** NOT self-initiated — R14 was **coordinator-directed**: a peer session relayed the owner's "word given" to build the segment-1 exact-model-ID analog of R13's segment-3 task-class gate, owner-authorized under the fm ORDER 048 standing grant. So this is a directed follow-on to R13 (#512), not an unprompted promotion. Decide-and-flag calls within it: (1) reused R13's private `_last_model_payload` last-valid-wins helper to extract the model segment and `engine.grammar.EXACT_MODEL_ID_RE` for detection — no new regex, no reverse import of `check_model_line` (that module imports FROM `check_session_log`, so the edge would be circular); the new helper is underscore-named so it does not match the `check_*(` parity regex and STRICT_SUBCHECKS stays 7; (2) scoped strictly to the complete-branch of `check_added_card` (diff-aware, single added card) so no historical/merged card can be retroactively reddened.

## What shipped (PR #513)

Folded the segment-1 exact-model-ID rule into the exit-affecting born-red
added-card grader, as an exact sibling of R13's segment-3 task-class gate.
`check_added_card`'s complete-branch (`check_log`) now ALSO appends an
exact-model-ID finding when the added card's `📊 Model:` model segment matches
`engine.grammar.EXACT_MODEL_ID_RE` — an exact model-ID token (`claude-opus-4-8`
and co.) instead of a family-level name (the ORDER 012 fleet-reporting bar) — so
an exact-ID segment-1 on the PR's OWN card reds at CI exactly like an unflipped
born-red badge. One new private helper does it — `_exact_model_id_findings_for_card`
— reusing R13's `_last_model_payload` (last-valid-wins scan, code-span / fence /
`[[fill:]]` aware) to extract the model segment and the shared
`EXACT_MODEL_ID_RE` for detection. No new top-level `check_*(` call is registered
in `_extra_check_findings` — the added-card lane is extended in place — so
`EXPECTED_STRICT_SUBCHECKS` stays 7 and the parity test is untouched. Fail-open:
a card with no parseable `📊 Model:` line, or a `[[fill:]]` / code-span /
family-level segment, yields nothing (the missing-line case is owned by the
marker checks, and a family-level name is exactly what the rule wants). The
fleet-wide `check_model_line` advisory (windowed to the 10 newest cards) is
unchanged; only the PR's own added card is graded exit-affecting, so no
historical card is retroactively reddened.

Files: `src/engine/checks/check_session_log.py` (grammar import + one private
helper + complete-branch wiring + docstring), `tests/test_checks.py` (three new
tests: exact-model-ID reds, family-level passes, missing-line fail-open),
`dist/bootstrap.py` (rebuilt + byte-pinned).

**Evidence.** PR #513, branch `claude/r14-exact-model-id-gate`. Commits:
`1f61980` (born-red card open), `49a5abd` (impl + tests + dist rebuild),
`824a6b0` (guard-fire telemetry from `check --strict` runs), + this flip commit.
The finding an exact-model-ID segment emits (from
`_exact_model_id_findings_for_card`): ``an exact-model-ID `📊 Model:` model
segment '<model-id>' on this added card — record the family-level model name only
(e.g. `fable-5`, `opus-4.8`), never an exact model ID, dated or not (fleet
reporting bar, ORDER 012); fix this card's line to the taught form … (family-level
model · effort · PL-004 task class; see .sessions/README.md)``. Verification:
full suite `1898 passed`; `dist/bootstrap.py check --strict` exit 0 after this
flip (born-red HOLD cleared by the badge → auto-merge lands on green, armed
SQUASH). CI cross-check before flip (run 29688990712, head `824a6b0`): kit-quality
real pytest `1897 passed, 2 skipped`, the cold-adoption smoke step reached
`check: all checks passed.` (the new exact-model-ID gate did NOT red the planted
`📊 Model: smoke · low · docs-only` card), and the sole `##[error]` in the log was
the designed born-red session-gate HOLD on this in-progress card.

## 💡 Session idea

**Name the advisory→born-red-gate graduation as a `docs/recipes/` pattern.** R13
(#512) folded segment-3 (task-class) and R14 (#513, this) folds segment-1
(exact-ID) into the exit-affecting born-red added-card grader — both via the
*identical* move: a fleet-wide *advisory* (`check_model_line`, windowed, no locked
door) ships first for migration pressure, then, once the taxonomy is stable, the
same rule is promoted to *the PR's-own-card* born-red gate as exit-affecting, with
the same no-retroactive-redden diff-scoping and the same `_last_model_payload`
reuse. That promotion is now a proven, twice-walked pattern (R13's own ⟲ review
flagged it but left it as prose). Graduate it into a `docs/recipes/` file — "how a
payload rule graduates from fleet-advisory to born-red exit-gate" — carrying the
R11 `> **applies-when:**` structural-signature badge (`content:_last_model_payload`,
`content:EXPECTED_STRICT_SUBCHECKS`) so a future session reaches for the recipe
instead of re-deriving the scoping. Its first named application is the last
un-promoted segment: **segment-2 (effort) exit-gating on the added card** — a
one-conditional sibling, with the one subtlety that the `MODEL_EFFORT_UNRECORDED`
retro-sweep carve-out must stay accepted on a real card. Deduped: grepped
`docs/recipes/`, `docs/ideas/`, and the groom doc — the only recipe today is
`pinned-feed-contract.md`; the payload-lint idea
(`model-line-payload-lint-advisory-2026-07-11.md`) is the *advisory* side only, and
no idea names the advisory→exit-gate *graduation as a recipe* or the segment-2
exit-gate. Distinct.

## ⟲ Previous-session review

Previous session — **R13 PL-004 task-class gate (PR #512)**. Did well: it reused
the `engine.grammar` parser and the shared class tuple rather than duplicating,
avoided the circular `check_model_line` import with an underscore-named helper
(keeping `EXPECTED_STRICT_SUBCHECKS` at 7), and scoped strictly to the added
card's complete-branch so nothing historical reddened — that clean scaffold is
exactly what let R14 land segment-1 as a near-mechanical sibling in one session.
What it left on the table: its own ⟲ review *identified* the advisory→born-red-gate
graduation as "a recognizable, repeatable pattern … worth naming explicitly in
`docs/`", but left that insight as prose inside the session card, where it is easy
to lose — the pattern only got re-surfaced this session because R14 happened to be
its next instance. Concrete system/workflow improvement: **when a ⟲
previous-session review surfaces a nameable, reusable pattern, route it into the
idea conveyor (`docs/ideas/` + README index) the same session** rather than leaving
it in the card's review prose. The ⟲ ender is a *detector* of durable patterns; the
`docs/ideas/` conveyor is where a detected pattern actually survives to be built.
This session acts on exactly that — the 💡 above promotes R13's flagged pattern into
a concrete recipe idea instead of re-flagging it.
