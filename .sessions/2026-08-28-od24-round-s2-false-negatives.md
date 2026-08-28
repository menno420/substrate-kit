# 2026-08-28 — OD-24 review round session 2: worklist pointer + false negatives 13/17/18

> **Status:** `in-progress` — born-red hold; flip is the deliberate last step.

- **📊 Model:** fable-5 · high · runtime bugfix
- **📍 Venue:** cloud-container

## Mission

The review round's step-3 first fixes, per fleet-manager's genesis dig
(fm `docs/findings/2026-08-28-substrate-kit-genesis-dig.md` §11) and the
v1.21.0 follow-up worklist's own restated fix order (fm
`docs/findings/2026-08-13-substrate-kit-v1210-followups.md`, tail):

1. **Route the kit to its own worklist** (gap #5, the smallest unrouted fix):
   supersede `docs/NEXT-TASKS.md` — actively false since 2026-07-17 (it tells
   the next session to distribute v1.18.0; v1.21.0 has been current since
   2026-08-13) — with a pointer to the fm-side worklist and round thread.
2. **Fix the false-negative family in `src/engine/checks/check_no_false_walls.py`**
   — the checker failing at its one job, each reproduced against the
   published v1.21.0 asset before the fix:
   - row 13 (dist `:5873`): a qualified reassertion after a mention
     predicate (`…rule is false in staging but true in production`) clears;
   - row 17 (dist `:5780`): the occurrence mask never reaches
     `_DATED_LINE`/`_FALSE_LABEL`, so `FALSE "agents cannot merge", agents
     cannot merge` and the dated-supersession variant pass strict;
   - row 18 (dist `:6036`): an unterminated digest BEGIN fence exempts every
     remaining line of the render path — fails open.
3. Regenerate `dist/bootstrap.py` via `python3 src/build_bootstrap.py`;
   tests + `scripts/preflight.py` green on real exit codes.

Out of scope, owner-gated or held: any release or adopter rollout (fixes
land on `main`; the cut is its own owner-said-go session), Move 1, all §10
dispositions, AGENTS.md.

## Shipped

- `docs/NEXT-TASKS.md` superseded into the route to the fm-side worklist
  (gap #5); each of the old plan's six tasks carries its terminal state,
  the two tree-checkable ones re-verified against this tree today
  (template doctrine at `src/engine/templates/CONSTITUTION.md.tmpl:113-116`;
  `docs/current-state.md:31` still reads v1.20.2 — that reconcile stays
  open, routed to the round).
- Rows 13/17/18 fixed in `src/engine/checks/check_no_false_walls.py`;
  named regression pins in `tests/test_check_no_false_walls_leg.py`
  (`TestPostV1210FalseNegatives`, 11 cases); dist regenerated via
  `python3 src/build_bootstrap.py`.

## Verify

- Reproductions first, against the **published** v1.21.0 asset (release
  download; sha256 `8807a00e…` three-way match with the sidecar and this
  tree's dist): rows 13/17a/17b returned `[]` where red was due; row 18's
  unterminated fence returned `[]`; a positive control redded first
  (TRAP-003). The em-dash dated variant already reds on v1.21.0 (the quoted
  occurrence is itself uncleared) — kept as a must-stay-red pin, not a fix
  target.
- After the fix: all repro cases invert to their expected verdicts; full
  suite `python3 -m pytest` 2170 passed, 1 skipped; `python3
  scripts/preflight.py` OK — 9 legs green (real exit 0).
- Corpus A/B, published dist vs fixed engine, over every scanned live file
  in this tree (41) and fleet-manager's (220): **0 newly-flagged, 0
  newly-cleared lines** — the fixes are corpus-neutral where they should be.

## Friction → guard candidates (adjacent shapes, deliberately not fixed here)

Two uncovered clearing-grammar shapes found while proving the fixes — both
outside rows 13/17/18's repro set, left for a future worklist row rather
than widened into this PR:

- **Apposition-severed mention cue** — `The "agents cannot merge" claim was
  superseded, agents cannot merge` still clears the bare reassertion: the
  mask patterns (`_QUOTE_THEN_FALSE`/`_QUOTE_THEN_DATED`) carry no
  apposition-noun slot between quote and predicate, while
  `_MENTION_PREDICATE` (quoted path) does. Recipe: extend both mask
  patterns with the same optional noun group `_MENTION_PREDICATE` uses;
  test target `tests/test_check_no_false_walls_leg.py`.
- **Reassertion after a plain-clause cue** (pre-dates v1.21.0) — `The
  "agents cannot merge" rule is superseded in staging but still binds in
  production` clears at the first `_clause_cleared` call (`superseded` is a
  repudiation cue; the clause split at `but` hides the reassertion). Recipe:
  run `_reasserted_after_mention` before the first clause-clear for QUOTED
  walls too; the row-13 pin class shows the test shape.

## ⟲ previous-session review

Session 1 (fm #956, the genesis dig) committed a next-session order that
held up in execution: the pointer fix was exactly one file; the worklist
rows carried reproducible sites (all three reproduced on the first attempt
against the published asset); and its "route, don't rebuild" verification
note was correct — nothing in this fix territory needed new apparatus. One
narrowing: §11 item 1 said the pointer "un-strands the round's own step 3",
which is true via `current-state.md`'s three existing links to NEXT-TASKS.md
— the CONSTITUTION boot path reaches it only through that hop, so the route
depends on a stale file staying linked; the current-state reconcile (old
task 4) is what makes it robust.

💡 **Session idea:** the checker's clearing grammar now has two mention-mask
pattern families (false/superseded + dated) that must stay in lockstep with
`_MENTION_PREDICATE`'s apposition/copula allowances — a tiny
grammar-consistency test (every predicate form accepted after a quote must
also be maskable before a bare wall) would catch the apposition-severed
class above and any future divergence mechanically, instead of one Codex
round at a time.
