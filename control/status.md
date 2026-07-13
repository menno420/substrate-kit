# substrate-kit · status
updated: 2026-07-13T05:17:00Z
phase: ORDER 016 COMPLETE — night-run tally posted 05:17Z; #317 awaiting owner ratification sweep
health: green — latest verified state: `python3 dist/bootstrap.py check --strict` exit 0 @ b171d02 · `python3 scripts/check_idea_index.py` OK (new body-state-drift guard live) · boot set 2862/7000 words (K0 gauge silent). Prior health record (PR #307): git history of this file.
kit: v1.15.0 · check: green · engaged: yes

SHIPPED (night run, ORDER 016):
- **#314** order landed verbatim (6ab5caa)
- **#315** seed skills → registry, 12 skills (2325e71)
- **#316** rationalize skill + checkpoint doctrine, 13 skills (817220d)
- **#317** GREEN-PARKED ratification: PL-012 autonomy rider (rulings.md + CONSTITUTION/routines tmpl) + reading-path.md.tmpl + 3 interview slots (head 82fca96)
- **#318** heartbeat (d4eb24e)
- **#319** adopter-outcome writeup: docs/reports/2026-07-13-night-run-adopter-outcomes.md + 3 guidance-delta ideas (c71f423+2cfc4b1)
- Evening pre-order: #308/#310/#311/#312/#313.

TALLY (ORDER 016 MORNING clause):
- slices landed = 11 merged PRs tonight (#308–#316, #318, #319) + 1 green-parked (#317)
- templates released = 0 tagged (graduation rides #317 ratification + next release wave — honest note)
- measurements written = 1 fleet report (14 seats: 12 SHIPPED / 2 IDLE-CLEAN / 0 STALLED; discrimination = honest null; failsafe bridged 4/4 platform wake-drops; substrate-gate flip-race fail-open bug surfaced → fix ask routed as idea)

ROUTINE DISPOSITION (as of this tally, 2026-07-13T05:17Z):
- **FAILSAFE:** trig_01EMfauRqevNovFM8dz4NLdp alive (fires 22:00/00:10/02:07/04:08Z verified).
- **Pacemaker:** one 01:49Z one-shot dropped platform-side, failsafe bridged; current tick per latest arm.
- **kit-lab loop untouched** (fires ~06:08Z — do not touch).

Parked PRs: #317 (claude/rider-graduation, head 82fca96) — Q-0271 rider graduation (PL-012 in docs/program/rulings.md + CONSTITUTION/routines tmpl) + Q-0272 reading-path.md.tmpl (+3 interview slots) — ALL CHECKS GREEN, card complete, do-not-automerge applied ~01:53Z (actor attributed menno420) = ratification park; landing path: owner sweep (label removal or manual merge). Never armed/closed/rebased by this seat. Open PRs: #317 only (parked). Claims: README-only.

⚑ FOR OWNER (paste-ready, carried from the standing set — full field blocks verbatim in git history of this file @ 86d2a57, ⚑ OWNER-ACTION 2/6 + ⚑ FOR MANAGER):
- **P10 required-check swap (⚑ 2):** Settings → Rules → `main` ruleset → required status checks: remove "Kit test suite" + "Cold-adoption smoke (adopt + check --strict)"; add `kit-quality`; set "Require branches to be up to date" OFF. Reversible; ends the ~35-min queue-stall class. (No agent path to rulesets — verified 403/no-endpoint.)
- **fm #122 v3.4 restamp:** the owner reviews and merges fleet-manager PR #122 PERSONALLY — do NOT agent-merge.
- **UNIVERSAL wake fetch-list vN bump + re-paste:** add `docs/seat-digest.md` (+ `docs/SKILLS.md`) to the manager-authored wake fetch list, bump vN, owner re-pastes via fm's edit-registry-first flow.
- **⚑ 6 public-flip-or-PAT (pick one):** make this repo public (⚠️ effectively irreversible) OR mint a fine-grained read-only PAT into the fleet environments (reversible) — unblocks the B2–B4 cross-repo sweeps.
- **Grounded-skills measurement window:** proposal to run the before/after measurement pass ~2026-07-19..26 per docs/reports/2026-07-12-grounded-skills-wrap.md §3d — say nothing to accept the window; a successor fires it when it matures.

B1 FAMILY VERDICTS (index truth at this close-out, bench/results/cold-start/index.json, 9 scored rows): run 1 **PASS** · run 2 **FAIL** · run 3 **FAIL** · run 4 **FAIL** · run 5 **FAIL** · run 6 **FAIL** · run 7 **ABORTED — harness environment seam, NOT SCORED, no row** · run 8 **FAIL** · run 9 **FAIL (near-miss — first ON M2+M3 double win via genuine behavior)** · run 10 **FAIL (ON wins M2 only; M1 tie, M3 tie; first coherent-pin, first non-degenerate T5 v3, #222 advisory lane validated)** — headline **1 PASS / 8 FAIL at 9 scored rows** (Reading A, ORDER 011 ruling). Full annotation: `bench/results/cold-start/f5-ruling-order-011.md` + each run dir.

next (the post-tally baton):
1. **Owner sweep of #317** → then release wave carrying rider+reading-path templates.
2. **Grounded-skills measurement window ~07-19..26.**
Backlog note: freeze still governs non-program surface; post-freeze quick-wins queued.

inbox: newest is ORDER 016 (owner night-run directive, landed verbatim via #314) — COMPLETE per the orders line below; no ORDER newer than 016.

orders: acked=001–016 · done=001–016 (016 tally posted; #317 ratification = owner-side residue)

blockers: none.

notes: this update = ORDER 016 morning tally 05:17Z (control-only diff, fast lane — no card): phase → ORDER 016 COMPLETE, SHIPPED consolidated to the night run, TALLY block posted (slices/templates/measurements), ROUTINE DISPOSITION refreshed, next-2 baton = owner sweep of #317 → release wave · grounded-skills window; matching tally entry appended to control/outbox.md (lane→manager). ⚑ FOR OWNER, kit line, B1 FAMILY VERDICTS kept verbatim. Prior standing record: git history of this file @ 917261b / 817220d / 86d2a57 — pointers over re-derivation.
