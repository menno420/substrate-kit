# substrate-kit · status
updated: 2026-07-13T09:20:00Z
phase: ORDER 017 COMPLETE — thorough night report posted 09:20Z (heartbeat + outbox, this PR); #317 awaiting owner ratification sweep
health: green — latest verified state: `python3 dist/bootstrap.py check --strict` exit 0 @ b171d02 · `python3 scripts/check_idea_index.py` OK (new body-state-drift guard live) · boot set 2862/7000 words (K0 gauge silent). Prior health record (PR #307): git history of this file.
kit: v1.15.0 · check: green · engaged: yes

NIGHT REPORT (ORDER 017, owner ask via Fleet Manager — window 2026-07-12T22:30Z → 2026-07-13T09:20Z):
- **SHIPPED (merges, numbers + SHAs):** #308 K0 gauge (174b113) · #310 condensation (c5ef5b9) · #311 gate proof (cf0fa24) · #312 idea-drift guard (1086dd5) · #313 heartbeat (ebc1be9) · #314 ORDER 016 verbatim (6ab5caa) · #315 seed skills (2325e71) · #316 rationalize (817220d) · #318 heartbeat (~d4eb24e squash) · #319 adopter-outcome report (b171d02; branch c71f423+2cfc4b1) · #320 ORDER 016 tally (847e7df) · #321 enabler branch-allowlist preflight (45fb77c — **another lane's work**, attribution note, not this seat's) · #322 ORDER 017 order-landing (3a95004, Fleet Manager filing — found already MERGED at report time).
- **OPEN PRs + check states:** #317 rider+reading-path graduation (head 82fca96) — ALL CHECKS GREEN (kit-quality, Kit test suite, Cold-adoption smoke, disarm, enable-auto-merge), `do-not-automerge` = ratification park, landing path owner review-merge. No other open PRs.
- **ORDERS served + outstanding:** 001–015 done (pre-existing) · 016 DONE (tally posted 05:17Z, PR #320) · 017 = this report · outstanding: none beyond the #317 owner sweep.
- **SIM-REQUESTs / asks pending:** SIM-REQUESTs filed tonight: none. ⚑ owner set unchanged (full blocks below): P10 required-check swap · fm #122 owner-personal merge · UNIVERSAL fetch-list bump · ⚑ 6 public-flip-or-PAT (gates B2–B4) · grounded-skills window ~07-19..26.
- **STALLS / DENIALS (verbatim-error rule):** none retried; zero platform denials. One platform anomaly: pacemaker one-shot trig_01USg5i3qna4fCX5ZeePg7Gj (fire_at 01:49Z) never delivered — failsafe bridged at 02:07Z. #314 transient red = inbox-order-grammar check (fixed in-PR, owner verbatim text untouched).
- **WAKE-CHAIN HEALTH:** failsafe trig_01EMfauRqevNovFM8dz4NLdp (cron `0 */2`, bound session_01MSze9jQLdxByyv2j6rm29c) fired 22:00/00:10/02:07/04:08/06:08/08:08Z — 6/6 delivered. Pacemaker chain ran 15-min ticks through the work loop (one drop, above); currently DOWN by design (seat settled; failsafe = bridge). kit-lab daily trig_01Jm57GAjNCFrYJn1oLMiYGE delivered ON SCHEDULE 06:10Z — first proven fresh-session-per-fire scheduled delivery (trigger-forensics data point).
- **NEXT-3:** (1) owner sweeps #317 → cut release wave (main 34+ commits past v1.15.0) + adopter upgrade PRs; (2) grounded-skills measurement pass ~07-19..26; (3) substrate-gate flip-race fail-open fix (idea filed from mineverse finding) + post-freeze quick-wins when the freeze lifts.

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

inbox: newest is ORDER 017 (thorough night report request, filed by the Fleet Manager via #322 @ 3a95004) — served by this update; no ORDER newer than 017.

orders: acked=001–017 · done=001–017 (017 = this report, posted heartbeat + outbox in this PR; #317 ratification = owner-side residue)

blockers: none.

notes: this update = ORDER 017 thorough night report 09:20Z (control-only diff, fast lane — no card): NIGHT REPORT block added (shipped SHAs · open-PR check states · orders · asks · stalls · wake-chain health · next-3), phase/updated/inbox/orders lines refreshed, matching full report appended to control/outbox.md (lane→manager). ⚑ FOR OWNER, kit line, B1 FAMILY VERDICTS, ORDER 016 tally blocks kept verbatim. Prior standing record: git history of this file @ 847e7df / 917261b / 817220d — pointers over re-derivation.
