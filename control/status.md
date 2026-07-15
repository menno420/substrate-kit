# Self Improvement seat — heartbeat
updated: 2026-07-15T10:52Z · phase: EAP EXTENSION ACTIVE (EAP through 2026-07-21; inbox consumed 001–024; routines coordinator-managed)

## This wake (2026-07-15 · work slice · claude/grounded-skills-harness · PR #386)
- Self-initiated slice (no inbox ORDER above 024; control/claims/ held README only; zero open PRs at the 10:0xZ scan — no backpressure): pre-built the grounded-skills measurement harness so the ~07-19..26 window run is turnkey (baton item; wrap report §3d proposal, PR #247 methodology).
- Shipped on the PR branch: `scripts/measure_grounded_skills.py` (M1 skill-grounding · M2 owner-ask compliance · M3 capability-ledger activity · M4 merge-throughput proxy; grammar constants from `engine.grammar`, skill names live from the SKILLS list; honest nulls; shallow-clone guard), pre-registered protocol `docs/operations/grounded-skills-measurement.md` (frozen metrics, linked from the operations index), 15 fixture tests.
- Two instrument defects caught by PL-008 spot-check before first use, both fixed in the same commit (b6dd77e): the naive `⚑ OWNER-ACTION` token scan counted 29 prose mentions / 0 real blocks in the kit's own cards (detection now line-start `⚑` + `WHAT:`); shallow clones silently zeroed M4 (now a flagged null).
- Verify: preflight 7/7 legs green (pytest incl. the 15 new tests, ruff, dist-byte-pin, idea-index, changelog, program-law, bench-integrity); `dist/bootstrap.py check --strict` red only on the designed born-red hold for this session's own card.

## Routine state (observed facts — trigger inventory carried from the 2026-07-15 ~04:4xZ read-only list_triggers pass; this wake armed no triggers)
- This session armed no triggers. Routines are coordinator-managed this wake.
- Observed in the registry: "Self Improvement failsafe wake" trig_01CUfSZo9Uky9DdpoqpZPcfT — cron `0 */2 * * *`, enabled=true, created 2026-07-15T04:38:07Z via meta_mcp, bound to a coordinator session (persistent_session_id session_01SFVAo5bPD41RMx9TzGxnPY), next fire 06:04Z — plus one pending one-shot pacemaker (run_once_at 2026-07-15T04:55:00Z, same session binding). Not created by this session.
- The 06:05Z fire (recorded in the #384 heartbeat, git history of this file) matches that failsafe's scheduled 06:04Z next-fire.
- ⚑ FOR OWNER REVIEW: ORDER 024 (control/inbox.md @ 58b3f80) states "do NOT re-arm routines yet; wait for the owner's per-seat go (the v3.6 reboot prompt IS that go)". The observed failsafe above post-dates that order. This heartbeat records the discrepancy neutrally for the owner's review/veto; it does not adjudicate it. Prior heartbeat (git history @ 58b3f80) had recorded all seat routines verified DOWN; kit-lab daily loop re-arm recipe remains docs/operations/lab-loop.md.

## State
- kit: v1.17.0
- v1.17.0 distributed 9/9 engaged adopters (registry re-verified at the 04:37Z scan; zero kit-line bumps since).
- Grounded-skills measurement: protocol pre-registered + harness on PR #386 (docs/operations/grounded-skills-measurement.md — one command: `python3 scripts/measure_grounded_skills.py --clone --workdir <dir> --json <f> --out <f>`).
- Revival boot reading: CONSTITUTION.md → control/inbox.md → this file → docs/eap-closeout-walkthrough-2026-07-14.md §E → docs/audits/eap-project-audit-2026-07-14.md.

## Next-2 baton
1. Grounded-skills measurement window ~2026-07-19..26 — run per docs/operations/grounded-skills-measurement.md (turnkey after PR #386; PR #247 methodology; owner silence accepts); publish the findings report under docs/reports/ and link it from the operations index.
2. After adopter lanes bump their heartbeat `kit:` lines (and/or branch-sweep gets wired per-repo via `adopt --wire-enforcement` — owner/resident), re-run `python3 dist/bootstrap.py currency` to retire the remaining DRIFT rows (5 at the 04:37Z scan).

## ⚑ FOR OWNER (standing set carried forward — NO new asks this wake)

⚑ P10 required-check swap
WHAT: Swap which CI check main requires, from the two legacy names to the current one.
WHERE: repo Settings → Rules → the `main` ruleset → required status checks.
HOW: remove "Kit test suite" and "Cold-adoption smoke (adopt + check --strict)"; add `kit-quality` (source: GitHub Actions); set "Require branches to be up to date" OFF.
WHY: the legacy alias jobs exist purely to satisfy the old required names; the up-to-date requirement stalls green PRs `behind`.
UNBLOCKS: deleting the two legacy-alias jobs; ends the queue-stall class.
VERIFY: next kit PR shows kit-quality as the only required check; agent then removes the alias jobs.
RISK: ↩️ reversible — re-add the old required checks in the same ruleset panel.

⚑ public-flip-or-PAT (pick one)
WHAT: Let the other fleet repos read this one — either make it public or mint a read-only token.
WHERE: P11: Settings → General → Danger Zone → Change visibility · P13: github.com/settings/tokens → fine-grained read-only PAT scoped to this repo, then add it to the fleet environments.
HOW: P11 is click-through; P13 is create-token + paste into environment settings.
WHY: sibling repos cannot read kit data today, so cross-repo sweeps and the merged console run blind.
UNBLOCKS: B2–B4 cross-repo sweeps + kit data in the merged console.
VERIFY: a sibling-seat session fetches a kit file read-only without "Access denied: repository … is not configured for this session".
RISK: ⚠️ P11 effectively irreversible (history exposed once public) · ↩️ P13 reversible — revoke anytime.

Standing (full paste-ready blocks verbatim in git history of this file @ 86d2a57):
- fm #122 v3.4 restamp — owner reviews/merges PERSONALLY.
- UNIVERSAL wake fetch-list vN bump (+ docs/seat-digest.md, docs/SKILLS.md).
- Grounded-skills measurement window ~2026-07-19..26 — silence accepts.

orders: acked=001–024 · done=001–024
