# Self Improvement seat — heartbeat
updated: 2026-07-14T14:36Z · phase: post-EAP — v1.16.0 cut in flight on PR #370 (ORDER 022 guard folded in); next = release dispatch + verify, then adopter wave

## Routines
- Failsafe: "Self Improvement failsafe wake" trig_01LsHxvnYnpQ59n7iQTPNNF3 · 0 */2 * * * · bound live coordinator. Pacemaker idles to failsafe post-consolidation (backlog dry).
- Business cron: kit-lab daily trig_01Jm57GAjNCFrYJn1oLMiYGE — KEEP.

## Facts
done=022 facts: PR #371 — stop-hook merged-head final-push guard: guard merged to main; release + adopter regen ride v1.16.0 (in flight). `_stop_push_guard` (sixth `evaluate_stop` advisory): fetch → provable ancestry vs origin/main via the new dist-shipped `engine/lib/git_truth.py` (port of scripts/_git_truth.py, parity-pinned) → merged=loud SKIP line · unmerged=silent · unprovable=NOTE + push proceeds (fail-open). Suite 1550→1559 passed (1 skipped unchanged); preflight 7/7; dist byte-stable ×2; three decision points mutation-tested. Details: .sessions/2026-07-14-order-022-push-guard.md.
done=021 facts: PR #368 — EAP closeout walkthrough at docs/eap-closeout-walkthrough-2026-07-14.md (sections A–E; OWNER ACTIONS leads with the #317 click). #345 "green" retracted with evidence; #317/#345 park states verified live. Full detail: git history of this file @ 4f6e50c.
done=020 facts: PR #362 — ORDER 020 items d+e; (a)–(c) satisfied per thread premise-check. Detail in git history @ 4f6e50c.

## Backlog state (honest)
Buildable backlog DRY as of 04:0xZ — 11/11 buildable ideas consumed or shipped. Former gates cleared 2026-07-14T14:0xZ: #317 and #345 both owner-ratified and merged (see Ratified/merged below). ORDER 022 guard landed on main as 39c6b20 (#371) and is folded into the v1.16.0 cut (PR #370) — release wave UNGATED, riding #370's green. Remaining: resident-lane kit: lines (→ adopters.md regen) · grounded-skills window ~07-19. No filler beyond this line (Q-0089).

## Parked
- (none — both former parks ratified 2026-07-14T14:0xZ, records below)

## Ratified/merged (2026-07-14 reconcile)
- PR #317 — RATIFIED + MERGED to main as 4f6e50c (2026-07-14T14:06:15Z, "Graduate the autonomy rider (Q-0271) + multi-repo reading path (Q-0272) into templates"). Payload verified on disk at HEAD: docs/program/rulings.md [PL-012] · src/engine/templates/reading-path.md.tmpl · tests/test_rider_graduation.py. Release wave UNGATED.
- PR #345 — RATIFIED + MERGED to main as c603cc9 (2026-07-14T14:06:12Z, "Add staged-artifact regen-lag checker (ORDER 019 item 6)"). Payload verified on disk at HEAD: src/engine/checks/check_staged_regen.py · tests/test_check_staged_regen.py.
- PR #371 — MERGED to main as 39c6b20 (2026-07-14T14:31:51Z, ORDER 022 stop-hook merged-head final-push guard). Folded into claude/release-v1.16.0 same hour; CHANGELOG entry re-cut into [1.16.0].

## Registry state
- All adopters tree-current at v1.15.0. adopters.md regen waits on resident kit: lines.
kit: v1.15.0

## Next-2 baton
1. v1.16.0 cut in flight on PR #370 (claude/release-v1.16.0) — carries the full band incl. the ORDER 022 guard (#371) re-cut into [1.16.0]; card flipped green → auto-merge lands it on CI green. Then: dispatch release.yml → scripts/verify_release.py → adopter upgrade wave.
2. Resident kit: lines → adopters regen · grounded-skills window ~07-19.

⚑ FOR OWNER (unchanged standing set — full paste-ready field blocks verbatim in git history of this file @ 86d2a57):
- P10 required-check swap (ruleset: require `kit-quality`, drop the two legacy contexts).
- fm #122 v3.4 restamp — owner reviews/merges PERSONALLY.
- UNIVERSAL wake fetch-list vN bump (+ docs/seat-digest.md, docs/SKILLS.md).
- ⚑ 6 public-flip-or-PAT (unblocks B2–B4 cross-repo sweeps).
- Grounded-skills measurement window ~2026-07-19..26 — silence accepts.

orders: acked=001–022 · done=001–022
