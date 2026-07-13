# substrate-kit · status
updated: 2026-07-13T10:44:30Z
phase: SEAT CLOSED — coordinator ender complete 2026-07-13; successor boots per CONSTITUTION → inbox → status
health: green — latest verified state: `python3 dist/bootstrap.py check --strict` exit 0 @ b171d02 · `python3 scripts/check_idea_index.py` OK (body-state-drift guard live) · boot set 2862/7000 words (K0 gauge silent). Prior health record (PR #307): git history of this file.
kit: v1.15.0 · check: green · engaged: yes

orders: acked=001–017 · done=001–017

ROUTINE DISPOSITION AS VERIFIED (2026-07-13T10:40Z audit, 13-page pagination):
- **ids closed = none-to-close** — all 11 session one-shots already fired, `ended_reason=run_once_fired`, verified across the full 13-page `list_triggers` pagination at 10:40Z.
- **Failsafe trig_01EMfauRqevNovFM8dz4NLdp LEFT ARMED** as successor bridge F-1 (cron `0 */2`, bound session_01MSze9jQLdxByyv2j6rm29c, next ~12:07Z; successor cutover rebinds-then-deletes).
- **Business cron trig_01Jm57GAjNCFrYJn1oLMiYGE** recorded — fresh-session-per-fire, NEVER rebound, next 2026-07-14T06:08Z.
- **Uncloseable = none.** No new routine armed at close.

PARKED: #317 rider+reading-path graduation (head 82fca96, all checks green, `do-not-automerge` ratification park) — landing path owner review-merge. No other open PRs beyond this ender.

Retro pointer: `.sessions/2026-07-13-si-coordinator-close.md` (full seat retro: shipped/parked, struggles, went-well, surprises).

Next-2 baton:
1. **Owner sweeps #317** → cut release wave (main 34+ commits past v1.15.0) + adopter upgrade PRs.
2. **Grounded-skills measurement window ~2026-07-19..26.**

⚑ FOR OWNER (paste-ready, carried from the standing set — full field blocks verbatim in git history of this file @ 86d2a57, ⚑ OWNER-ACTION 2/6 + ⚑ FOR MANAGER):
- **P10 required-check swap (⚑ 2):** Settings → Rules → `main` ruleset → required status checks: remove "Kit test suite" + "Cold-adoption smoke (adopt + check --strict)"; add `kit-quality`; set "Require branches to be up to date" OFF. Reversible; ends the ~35-min queue-stall class. (No agent path to rulesets — verified 403/no-endpoint.)
- **fm #122 v3.4 restamp:** the owner reviews and merges fleet-manager PR #122 PERSONALLY — do NOT agent-merge.
- **UNIVERSAL wake fetch-list vN bump + re-paste:** add `docs/seat-digest.md` (+ `docs/SKILLS.md`) to the manager-authored wake fetch list, bump vN, owner re-pastes via fm's edit-registry-first flow.
- **⚑ 6 public-flip-or-PAT (pick one):** make this repo public (⚠️ effectively irreversible) OR mint a fine-grained read-only PAT into the fleet environments (reversible) — unblocks the B2–B4 cross-repo sweeps.
- **Grounded-skills measurement window:** proposal to run the before/after measurement pass ~2026-07-19..26 per docs/reports/2026-07-12-grounded-skills-wrap.md §3d — say nothing to accept the window; a successor fires it when it matures.

B1 FAMILY VERDICTS (index truth at this close-out, bench/results/cold-start/index.json, 9 scored rows): run 1 **PASS** · run 2 **FAIL** · run 3 **FAIL** · run 4 **FAIL** · run 5 **FAIL** · run 6 **FAIL** · run 7 **ABORTED — harness environment seam, NOT SCORED, no row** · run 8 **FAIL** · run 9 **FAIL (near-miss — first ON M2+M3 double win via genuine behavior)** · run 10 **FAIL (ON wins M2 only; M1 tie, M3 tie; first coherent-pin, first non-degenerate T5 v3, #222 advisory lane validated)** — headline **1 PASS / 8 FAIL at 9 scored rows** (Reading A, ORDER 011 ruling). Full annotation: `bench/results/cold-start/f5-ruling-order-011.md` + each run dir.

inbox: newest is ORDER 017 (served, PR #323); no ORDER newer than 017.

blockers: none.

notes: this update = coordinator seat-close ender 2026-07-13 (PR #324): SEAT CLOSED phase, routine disposition as verified, parked/baton/retro pointer refreshed; capability bake (send_later tombstone-less drop) in docs/CAPABILITIES.md and two prompt-delta proposals in control/outbox.md ship in the same PR. ⚑ FOR OWNER, kit line, B1 FAMILY VERDICTS kept verbatim. Prior standing record: git history of this file @ df6fa9c / 847e7df — pointers over re-derivation.
