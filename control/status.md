# Self Improvement seat — heartbeat
updated: 2026-07-15T12:14Z · phase: EAP EXTENSION ACTIVE (EAP through 2026-07-21; inbox consumed 001–024; routines coordinator-managed)

## This wake (2026-07-15 · work slice · claude/adopter-currency-websites-v1170 · PR #389)
- Coordinator-routed adopter-currency slice (baton item 2 of the previous heartbeat; no inbox ORDER above 024; control/claims/ held README only; zero open PRs at the 12:0xZ scan): re-ran `python3 dist/bootstrap.py currency` (12:09:23Z, 12 repos scanned read-only, exit 0 first try) after websites bumped its self-report to `kit: v1.17.0`. Registry regenerated: websites row now `current`; its DRIFT row retired. DRIFT 5 repos → 4 — remaining rows preserved per the benign-red doctrine: chronic lane-owed self-report lag (superbot-next v1.16.0, superbot-games status.md v1.15.0 + mining/exploration lanes v1.7.1, superbot-mineverse v1.16.0) + kit's known tree-internal config-pin v1.0.0 row. Docs-only slice — no engine change, dist byte-pin untouched.
- Claim hygiene: first claim bullet was hand-written and unparseable (`claims-format` advisory at check --strict); re-rendered via `bootstrap claim` (round-trip verified) same session.
- Verify: preflight 8/8 legs green (pytest 1594 passed, 1 skipped; ruff; dist-byte-pin; idea-index; retro-index; changelog-structure; program-law; bench-integrity); `dist/bootstrap.py check --strict` clean except the designed born-red session-gate HOLD + known advisories (staged-regen-lag ×3; model-line payload ×4 older cards — now baton item 2).

## Routine state (observed facts — trigger inventory carried from the 2026-07-15 ~04:4xZ read-only list_triggers pass; this wake armed no triggers)
- This session armed no triggers and ran no new trigger inventory. Routines are coordinator-managed this wake.
- Carried observation (04:4xZ pass): "Self Improvement failsafe wake" trig_01CUfSZo9Uky9DdpoqpZPcfT — cron `0 */2 * * *`, enabled=true, created 2026-07-15T04:38:07Z via meta_mcp, bound to a coordinator session (persistent_session_id session_01SFVAo5bPD41RMx9TzGxnPY) — plus one pending one-shot pacemaker (run_once_at 2026-07-15T04:55:00Z, same session binding). Not created by this seat's sessions.
- ⚑ FOR OWNER REVIEW: ORDER 024 (control/inbox.md @ 58b3f80) states "do NOT re-arm routines yet; wait for the owner's per-seat go (the v3.6 reboot prompt IS that go)". The observed failsafe above post-dates that order. This heartbeat records the discrepancy neutrally for the owner's review/veto; it does not adjudicate it. Prior heartbeat (git history @ 58b3f80) had recorded all seat routines verified DOWN; kit-lab daily loop re-arm recipe remains docs/operations/lab-loop.md.

## State
- kit: v1.17.0
- v1.17.0 distributed 9/9 engaged adopters; registry regenerated this wake (12:09:23Z scan): websites now current at v1.17.0; DRIFT 4 repos (superbot-next, superbot-games, superbot-mineverse self-report lag + kit's tree-internal pin row).
- Grounded-skills measurement: harness MERGED (#386, main @ c5380dc) — turnkey: `python3 scripts/measure_grounded_skills.py --clone --workdir <dir> --json <f> --out <f>`; protocol pre-registered at docs/operations/grounded-skills-measurement.md.
- Revival boot reading: CONSTITUTION.md → control/inbox.md → this file → docs/eap-closeout-walkthrough-2026-07-14.md §E → docs/audits/eap-project-audit-2026-07-14.md.

## Next-2 baton
1. Grounded-skills measurement window ~2026-07-19..26 — run per docs/operations/grounded-skills-measurement.md (turnkey since #386 merged; PR #247 methodology; owner silence accepts); publish the findings report under docs/reports/ and link it from the operations index.
2. Model-line payload sweep — fix the 4 older cards whose `📊 Model:` lines are off-taxonomy or malformed (named verbatim by `dist/bootstrap.py check --strict` advisories: 2026-07-14-seat-digest-adaptive-clip, 2026-07-14-v1.16.0-wave, 2026-07-15-adopters-currency-refresh, 2026-07-15-idea-index-shipped-drift) so the PL-004 harvest records them; the next currency re-run stays conditional on the remaining adopter lanes bumping their `kit:` lines (4 DRIFT repos at the 12:09Z scan).

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
