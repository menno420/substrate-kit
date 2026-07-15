# 2026-07-15 · groom-sync-advisory

> **Status:** `complete`

- **📊 Model:** Fable (Claude 5 family) · medium · docs-only
- Scope: baton item 2 — groom the template↔local-copy sync advisory (the
  #395 card-only 💡, fresh evidence in PR #397) into docs/ideas/; plus one
  contained build from the captured backlog: the dispatch-race
  re-verify-then-stand-down clause (docs/ideas/
  dispatch-race-reverify-clause-2026-07-10.md) into the lab-loop prompt
  STEP 2 — docs-only, rides the console re-paste already pending from #397.

About to (opening declaration, retained): file the sync-advisory idea with
its two live instances as evidence, index it in the README Backlog, land the
re-verify clause in docs/operations/lab-loop.md, flip the shipped idea's
lifecycle, refresh the heartbeat baton.

## Record

- Boot: hard-synced to origin/main 6a88392 (#397); inbox tops at ORDER 024
  (all acked+done per the heartbeat orders line; the "ORDER 025" text at
  ~line 210 is the fm relay inside ORDER 019, not a new order);
  control/claims/ held README only; zero open PRs at the ~16:2xZ scan;
  `currency --check` exit 0 from the repo root — the first probe from
  outside the repo exited 1 with "no roster at /home/user/docs/
  fleet-repos.txt", a cwd artifact recorded on the heartbeat so no wake
  misreads it as a regen signal. Born-red card + claim (written by the
  `bootstrap claim` verb — note it prefixes the branch, writing
  `claude-groom-sync-advisory.md`) = first commit f777450; PR #398 opened
  READY immediately after.
- Shipped (6c79a1a): (1) docs/ideas/template-local-copy-sync-advisory-
  2026-07-15.md — the twice-paid-in-one-day class (kit-local planted-doc
  copies hand-synced with src/engine/templates/; #395 observed
  control/README.md divergence, #397 hand-fixed control/claims/README.md
  lagging its template by a whole feature paragraph), quick-win shape:
  advisory-only `## ` heading-set compare per `ADOPT_PLAN` pair
  (src/engine/adopt.py) whose destination exists in the kit's own tree;
  README Backlog row added. (2) ⚑ Self-initiated: dispatch-race
  re-verify-then-stand-down clause shipped into lab-loop STEP 2, adjacent
  to #397's CLAIM BEFORE BUILD (the two halves of the parallel-lane
  guard); idea flipped promoted/shipped_pr 398/outcome shipped, README row
  Backlog → Shipped (window closes 2026-08-14); console re-paste rides the
  one already pending from #397. (3) ⚑ Self-initiated rider (the #397
  card's ⟲ improvement, "small enough to ride any docs slice"):
  frontmatter-grammar comment atop the README Backlog section (`state:`
  vocabulary vs `outcome: shipped` — two sessions paid a red preflight
  round on it). (4) Fix-on-sight (2c41257): #397's card task-class
  `docs+drift-fix` → `docs-only` — the `model-line-class` advisory named
  the exact fix; stops a newest-10-window repeat nag.
- Verify (at 6c79a1a): `python3 scripts/preflight.py` → 8/8 legs green
  (pytest 1608 passed, 1 skipped; dist-byte-pin; ruff; idea-index;
  retro-index; changelog-structure; program-law; bench-integrity).
  `dist/bootstrap.py check --strict` → designed born-red HOLD only (this
  card, pre-flip) + known staged-regen-lag ×3 + the #397 model-line-class
  advisory (fixed same wake, above); guard-fires telemetry delta committed
  with the heartbeat (2c41257).

## Session enders

- 💡 Session idea: **claim-verb filename echo in the success line.** The
  `bootstrap claim <slug>` success message says it "wrote
  control/claims/claude-<slug>.md" but a session that read the README's
  `control/claims/<branch-or-scope>.md` convention naturally expects the
  bare slug — this wake's `cat control/claims/groom-sync-advisory.md`
  failed before re-reading the verb output. Cheap fix: the verb's report
  line already names the real path; also print the matching `--delete`
  invocation with the SAME slug (it does) plus one clause "(file is
  branch-prefixed)" — or simpler, have the README's step 2 name the
  branch-prefixed form the verb actually writes. Dedup-grep docs/ideas/
  (`claim.*filename|branch-prefix`): no existing capture; small enough to
  ride any docs slice, recorded here card-only by the same rule the
  README grammar comment graduated under (twice-paid → file it).
- ⟲ Previous-session review (2026-07-15-order-claim-collision-completion,
  PR #397): honest re-scoping done right — it discovered the mechanism had
  already shipped in #365 and completed only the true residue (doc
  segments), recording the split (`shipped_pr: 365` + #397 doc note)
  instead of inflating its slice. Two of its outputs paid off THIS wake:
  its baton line 2 named the groom target with evidence pre-attached, and
  its ⟲ improvement (the grammar comment) was sized to ride along.
  Improvement it surfaces: its own card's `docs+drift-fix` task-class was
  off-taxonomy and became a standing advisory nag — a session inventing a
  compound class is exactly what the PL-004 prefix-match advisory exists
  to catch, but the card contract in .sessions/README.md never lists the 9
  classes inline; the checker message does. One line in the README naming
  the class list would close the invent-a-class loop at write time.
