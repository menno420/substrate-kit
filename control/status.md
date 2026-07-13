# substrate-kit · status
updated: 2026-07-13T02:11:22Z
phase: NIGHT RUN (ORDER 016) — items 1–3 shipped, item 4 green-parked for ratification, item 5 + tally due by 06:00Z
health: green — latest verified state: `python3 dist/bootstrap.py check --strict` exit 0 @ 1086dd5 · `python3 scripts/check_idea_index.py` OK (new body-state-drift guard live) · boot set 2862/7000 words (K0 gauge silent). Prior health record (PR #307): git history of this file.
kit: v1.15.0 · check: green · engaged: yes

SHIPPED THIS SESSION (work loop, cited):
- **#308** K0 orientation-headroom gauge (merged 21:15Z, HEAD-verified 174b113)
- **#310** current-state.md condensation 6913→2862 words, history → docs/reports/2026-07-12-current-state-archive.md (c5ef5b9)
- **#311** gate multi-card shadowing: already fixed v1.10.1 (#187/#226), idea file reconciled + ground-truth proof (cf0fa24)
- **#312** idea-drift guard (body-state-drift check in check_idea_index.py) + 4 idea files reconciled (1086dd5)
- **#314** ORDER 016 landed verbatim (6ab5caa; grammar-framing fix 07c097f-branch)
- **#315** seed skills chase-references + prep-owner-steps into registry, 12 skills + seat-digest clip fix (2325e71)
- **#316** rationalization checkpoint doctrine + `rationalize` skill, 13 skills (817220d)

ROUTINE DISPOSITION (as of this heartbeat, 2026-07-13T02:1xZ):
- **FAILSAFE (this seat's dead-man bridge):** trig_01EMfauRqevNovFM8dz4NLdp "Self Improvement failsafe wake" · cron `0 */2 * * *` · self-bound to session_01MSze9jQLdxByyv2j6rm29c · verified firing (22:00Z, 00:10Z, 02:07Z wakes delivered).
- **Pacemaker chain: active** (~15 min per working turn) — NOTE: the 01:49Z one-shot (trig_01USg5i3qna4fCX5ZeePg7Gj) never delivered its wake (platform drop; failsafe bridged at 02:07Z; candidate CAPABILITIES.md entry). Current tick trig_01QsU2UCJ5q6KbNCMn8HcsqR → 02:24Z.
- **BUSINESS cron recorded (never rebind, never delete):** trig_01Jm57GAjNCFrYJn1oLMiYGE "kit-lab loop" · untouched · next fire 2026-07-13T06:08Z.
- **Registry oddity still recorded, NOT touched, not this seat's:** trig_018wP6XTPmf9DLnxrG4RpGVh "suberbot docs reconciliation" shows enabled with next_run_at "0001-01-01T00:00:00Z".
- Full prior ROUTINE STATE record (re-arm provenance, the 3-for-3 fresh-session non-delivery finding, stopgap doctrine): git history of this file @ 86d2a57.

Parked PRs: #317 (claude/rider-graduation, head 82fca96) — Q-0271 rider graduation (PL-012 in docs/program/rulings.md + CONSTITUTION/routines tmpl) + Q-0272 reading-path.md.tmpl (+3 interview slots) — ALL CHECKS GREEN, card complete, do-not-automerge applied ~01:53Z (actor attributed menno420) = ratification park; landing path: owner sweep (label removal or manual merge). Never armed/closed/rebased by this seat. Open PRs: #317 only (parked). Claims: README-only.

⚑ FOR OWNER (paste-ready, carried from the standing set — full field blocks verbatim in git history of this file @ 86d2a57, ⚑ OWNER-ACTION 2/6 + ⚑ FOR MANAGER):
- **P10 required-check swap (⚑ 2):** Settings → Rules → `main` ruleset → required status checks: remove "Kit test suite" + "Cold-adoption smoke (adopt + check --strict)"; add `kit-quality`; set "Require branches to be up to date" OFF. Reversible; ends the ~35-min queue-stall class. (No agent path to rulesets — verified 403/no-endpoint.)
- **fm #122 v3.4 restamp:** the owner reviews and merges fleet-manager PR #122 PERSONALLY — do NOT agent-merge.
- **UNIVERSAL wake fetch-list vN bump + re-paste:** add `docs/seat-digest.md` (+ `docs/SKILLS.md`) to the manager-authored wake fetch list, bump vN, owner re-pastes via fm's edit-registry-first flow.
- **⚑ 6 public-flip-or-PAT (pick one):** make this repo public (⚠️ effectively irreversible) OR mint a fine-grained read-only PAT into the fleet environments (reversible) — unblocks the B2–B4 cross-repo sweeps.
- **Grounded-skills measurement window:** proposal to run the before/after measurement pass ~2026-07-19..26 per docs/reports/2026-07-12-grounded-skills-wrap.md §3d — say nothing to accept the window; a successor fires it when it matures.

B1 FAMILY VERDICTS (index truth at this close-out, bench/results/cold-start/index.json, 9 scored rows): run 1 **PASS** · run 2 **FAIL** · run 3 **FAIL** · run 4 **FAIL** · run 5 **FAIL** · run 6 **FAIL** · run 7 **ABORTED — harness environment seam, NOT SCORED, no row** · run 8 **FAIL** · run 9 **FAIL (near-miss — first ON M2+M3 double win via genuine behavior)** · run 10 **FAIL (ON wins M2 only; M1 tie, M3 tie; first coherent-pin, first non-degenerate T5 v3, #222 advisory lane validated)** — headline **1 PASS / 8 FAIL at 9 scored rows** (Reading A, ORDER 011 ruling). Full annotation: `bench/results/cold-start/f5-ruling-order-011.md` + each run dir.

next (the night-run baton):
1. **ORDER 016 item 5 — adopter-outcome writeup** (~04:30–05:30Z).
2. **06:00Z tally** in heartbeat + control/outbox.md (lane→manager).

inbox: newest is ORDER 016 (owner night-run directive, landed verbatim via #314) — acked and IN PROGRESS per the orders line below; no ORDER newer than 016.

orders: acked=001–016 · done=001–015 · 016 IN PROGRESS (night run)

blockers: none.

notes: this update = night-run heartbeat 02:1xZ (control-only diff, fast lane — no card): phase → NIGHT RUN (ORDER 016), SHIPPED block extended (#314 #315 #316), #317 recorded as ratification park, ROUTINE DISPOSITION refreshed (failsafe 3-for-3 wakes; 01:49Z one-shot non-delivery noted; kit-lab loop untouched), next-2 baton = ORDER 016 item 5 + 06:00Z tally; ⚑ FOR OWNER, kit line, B1 FAMILY VERDICTS kept verbatim. Prior standing record: git history of this file @ 817220d / 1086dd5 / 86d2a57 — pointers over re-derivation.
