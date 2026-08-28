# 2026-08-28 — OD-24 review round session 2: worklist pointer + false negatives 13/17/18

> **Status:** `complete` — landed after three Codex rounds (5+6 conceded and
> fixed; R3's 4 conceded and routed to the fm worklist — the cap's land
> condition).

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
  (`TestPostV1210FalseNegatives`, 12 cases — an earlier draft of this card
  said 11, caught by the verification pass — plus
  `TestRound2AdversarialHardening`, 8); dist regenerated via
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
  newly-cleared lines** — the fixes are corpus-neutral where they should be
  (re-run after round 2 below; still 0/0).
- **Pre-push adversarial round (four independent verifier lanes executing
  counterexamples against the published asset and the fixed engine; ~380
  distinct inputs including a 3,000-doc fence fuzz): two REAL regressions
  found and fixed, two design holes closed.** (1) The first cut's mask
  blanked clause separators inside mention spans, merging clauses — a cue
  the raw line isolated cleared a bare wall v1.21.0 flagged (two shapes:
  `…"wall" — SUPERSEDED…, does not reproduce` and cue-before-quote via
  `based on a false … wall` swallowing ` and `); clause bounds now come
  from the RAW line and are sliced out of the masked copy. (2) The dated
  mask patterns over-masked a wall's OWN dated record when a quoted name
  merely shared the capability family (`the "push mirror" LAST-VERIFIED…`
  went red); they now mask only when the quoted content is itself a wall.
  (3) The reassertion gate read `but it no longer holds` as a reassertion
  (negation-blind) and gated affirmations about OTHER capabilities'
  walls; it is now negation-aware and family-gated, covers the cross-line
  bridges, and the sentence split survives `...`/`e.g.`. (4) Row 18's
  orphan-region scan let a generated `## Append log` heading set
  historical state that leaked past a later well-formed pair (4 of 3,000
  fuzz docs); orphan-region lines never establish document state. The
  paren/middot bare-date mention forms (`"…" (2026-08-14), <bare wall>` —
  pre-existing, not a regression) joined the mask in the same round.

## Codex review (kit #587)

- **R1 on head `e54664a`: 5 inline findings (4 P1 · 1 P2) — 5 `[conceded]`,
  0 survived, each reproduced by execution before its fix and pinned in
  `TestCodexRound1Pins`:** (1) the reassertion tail missed wrapped lines —
  now extended under the G1 block boundaries minus the contrast stop;
  (2) contracted/modal negations (`doesn't hold`, `cannot remain in
  force`) read as reassertions — negation is now judged over the whole
  matched span (token lookbehinds could not see phrase scope: the engine
  backtracks past an excluded token to an unguarded one); (3) the mask
  blanked single-quoted mentions' own spans (single quotes are not
  `_WALL_QUOTE`-quoted, so they grade through the bare path) — the span
  holding the graded occurrence is never masked now; (4) masking an
  unrelated capability's mention stripped the family evidence and let the
  orphaned `was superseded` clear a deploy wall — every mask branch now
  requires family/phrase relation; (5) the first clause-clear's
  mention-scoped cues bypassed the reassertion gate — the verdict is now
  computed first and gates that path too. Suite 2183 passed; corpus A/B
  re-run: 0/0 on both trees.

- **R2 on head `6dacdaf`: 6 inline findings (5 P1 · 1 P2) — 6 `[conceded]`,
  0 survived, each reproduced by execution and pinned in
  `TestCodexRound2Pins`:** (1) the whole-span negation check
  over-suppressed — "not retired AND remains" reasserts, so negation scope
  is now token-directed and sealed by coordination; (2) the single-quoted
  mention path (bare, since `_WALL_QUOTE` excludes single quotes) bypassed
  the reassertion gate — an enclosing mention span now gates it with the
  tail starting after the mention; (3) digest fences now pair BY NAME (a
  walls END no longer terminates a skills BEGIN); (4) entering an orphan
  region clears inherited historical state; (5) the reassertion family
  check reads the whole contrast segment, not the truncated match; (6)
  nevertheless/nonetheless joined the contrast list. Suite 2189 passed;
  corpus A/B: 0/0 on both trees. **This exhausts the two-re-review cap:
  the next round's outcome lands with any open findings named, per the
  close discipline.**

- **R3 on head `28d4729`: 4 inline findings (2 P1 · 2 P2) — 4 `[conceded —
  deferred]`, each verified real by execution, NONE fixed in this PR.** The
  two-re-review cap is spent, and the round tally (5 → 6 → 4) is the
  measured non-convergence pattern the cap exists for (each round probes
  the previous round's new grammar). The four, verified 2026-08-28: (1) an
  `or`-coordinated negated complement pair reads as affirmative — new FP,
  cheap direction; (2) a later `whereas <other-capability>` clause
  suppresses the family gate over a real earlier reassertion — FN; (3) the
  truth-token vocabulary omits direct state predicates (`active`,
  `enforced`, `operative`, `valid`) — FN; (4) the cross-line tail treats a
  Markdown table row as prose continuation — new FP. None fires on either
  live tree (corpus A/B at this head: 0 newly-flagged, 0 newly-cleared).
  **Routed to the fm worklist as a new row in the same fm batch** — the
  round's own mechanism for dist defects — rather than looped here.
- **Flip exemption taken, per the close discipline:** the reviewed SHA is
  `28d4729` (R3's `Reviewed commit`), and the only commit after it is this
  card's own close-out and badge flip — nothing reviewable changed.

## Friction → guard candidates (adjacent shapes, deliberately not fixed here)

Uncovered clearing-grammar shapes found while proving the fixes — all
outside rows 13/17/18's repro set and all **pre-existing on v1.21.0** (each
verified green-on-both, so none is this PR's regression), left for a future
worklist row rather than widened into this PR:

- **Empty-family comma-cue baseline** — `agents cannot merge, does not
  reproduce anyway.` clears on both versions: a plain comma never splits
  clauses, so a capability-agnostic cue beside a bare wall clears it. The
  row-17 fix inherits this boundary (a second unrelated cue in the same
  comma stretch still clears a bare reassertion after the mask removes the
  mention's marker).
- **FALSE-label family-blindness** — `FALSE "agents cannot deploy", agents
  cannot merge` clears the merge wall on both versions: `_FALSE_LABEL` is
  not family-gated, so a FALSE-labelled mention of a DIFFERENT capability
  clears a comma-adjacent bare wall.
- **Reassertion shapes outside the contrast-conjunction list** — `and true
  in production`, semicolon/em-dash/colon continuations, reassertion
  BEFORE the mention, relative clauses, >60-char gaps; and a dotted title
  (`per Dr. Smith's audit but true…`) still ends the inspected sentence
  early. All green on both versions.
- **Fence-marker-line prose and cross-variant pairing** — wall text sharing
  a physical line with a fence marker is never scanned, and a
  skills-digest BEGIN accepts a walls-digest END; both faithful to
  v1.21.0's loop semantics.
- **A but-clause about the RECORD gates a repudiation** — `…is false and no
  longer applies, but the dated ledger row remains.` reds at HEAD (green on
  v1.21.0): the reassertion gate cannot tell an affirmation about the
  ledger entry from one about the wall when no capability is named. NEW at
  HEAD, deliberate cheap-direction trade, 0 live corpus hits — recorded as
  the one known new false-positive class this PR accepts.

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
