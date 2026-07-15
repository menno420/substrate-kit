# Self Improvement seat — heartbeat
updated: 2026-07-15T12:52Z · phase: EAP EXTENSION ACTIVE (EAP through 2026-07-21; inbox consumed 001–024; routines coordinator-managed)

## This wake (2026-07-15 · work slice · claude/model-line-payload-sweep · PR #390)
- Coordinator-routed baton item 2 (no inbox ORDER above 024; control/claims/ held README only at open; zero open PRs at the 12:3xZ scan): model-line payload sweep — retro-fixed the 4 session cards `check --strict` named verbatim (2026-07-14-seat-digest-adaptive-clip, 2026-07-14-v1.16.0-wave, 2026-07-15-adopters-currency-refresh, 2026-07-15-idea-index-shipped-drift). All 4 now carry shape-valid three-field payloads, so the PL-004 harvest records them; the off-taxonomy `distribution/ceremony` class was mapped to `docs-only` with the original wording kept as decoration.
- Retro-fix honesty rule (decide-and-flag): original self-reported model tokens preserved verbatim; effort backfilled ONLY where the authoring session recorded it. Three cards never self-reported effort — their effort segment reads `unrecorded` rather than an invented tier, which trades the 4 shape/class advisories for 3 `model-line-effort` nags (advisory-only, never exit-affecting; they age out of the 10-card lint window as new cards land). TERMINAL disposition: do NOT "re-fix" these by inventing low/medium/high — the truthful value is unrecorded; the sanctioned-marker idea is captured in docs/ideas/ (see PR #390 card 💡).
- Adopter-bump precheck (before picking the slice): live raw-content scan of all registry rows at 12:3xZ matched docs/adopters.md @ 30a2a53 byte-for-byte (websites/venture-lab/idea-engine v1.17.0 current; superbot-next + superbot-mineverse v1.16.0, superbot-games v1.15.0 + lanes v1.7.1 — known DRIFT, already recorded) — no currency re-run warranted.
- Verify: preflight 8/8 legs green (pytest 1594 passed, 1 skipped; ruff; dist-byte-pin; idea-index; retro-index; changelog-structure; program-law; bench-integrity); `check --strict` clean except the designed born-red session-gate HOLD + known staged-regen-lag ×3 + the 3 honest `unrecorded` effort nags above.

## Routine state (observed facts — trigger inventory carried from the 2026-07-15 ~04:4xZ read-only list_triggers pass; this wake armed no triggers)
- This session armed no triggers and ran no new trigger inventory. Routines are coordinator-managed this wake.
- Carried observation (04:4xZ pass): "Self Improvement failsafe wake" trig_01CUfSZo9Uky9DdpoqpZPcfT — cron `0 */2 * * *`, enabled=true, created 2026-07-15T04:38:07Z via meta_mcp, bound to a coordinator session (persistent_session_id session_01SFVAo5bPD41RMx9TzGxnPY) — plus one pending one-shot pacemaker (run_once_at 2026-07-15T04:55:00Z, same session binding). Not created by this seat's sessions.
- ⚑ FOR OWNER REVIEW: ORDER 024 (control/inbox.md @ 58b3f80) states "do NOT re-arm routines yet; wait for the owner's per-seat go (the v3.6 reboot prompt IS that go)". The observed failsafe above post-dates that order. This heartbeat records the discrepancy neutrally for the owner's review/veto; it does not adjudicate it. Prior heartbeat (git history @ 58b3f80) had recorded all seat routines verified DOWN; kit-lab daily loop re-arm recipe remains docs/operations/lab-loop.md.

## State
- kit: v1.17.0
- v1.17.0 distributed 9/9 engaged adopters; registry (docs/adopters.md, generated 12:09:23Z) verified still-current by this wake's live rescan: websites current at v1.17.0; DRIFT 4 repos (superbot-next, superbot-games, superbot-mineverse self-report lag + kit's tree-internal pin row).
- Grounded-skills measurement: harness MERGED (#386, main @ c5380dc) — turnkey: `python3 scripts/measure_grounded_skills.py --clone --workdir <dir> --json <f> --out <f>`; protocol pre-registered at docs/operations/grounded-skills-measurement.md.
- Revival boot reading: CONSTITUTION.md → control/inbox.md → this file → docs/eap-closeout-walkthrough-2026-07-14.md §E → docs/audits/eap-project-audit-2026-07-14.md.

## Next-2 baton
1. Grounded-skills measurement window ~2026-07-19..26 — run per docs/operations/grounded-skills-measurement.md (turnkey since #386 merged; PR #247 methodology; owner silence accepts); publish the findings report under docs/reports/ and link it from the operations index.
2. Currency re-run — conditional on the lagging adopter lanes bumping their `kit:` self-report lines (4 DRIFT repos verified still lagging at this wake's 12:3xZ live scan: superbot-next v1.16.0, superbot-games v1.15.0 + lanes v1.7.1, superbot-mineverse v1.16.0, plus kit's tree-internal v1.0.0 pin row); when any bump lands, `python3 dist/bootstrap.py currency` + regenerate docs/adopters.md. Else: pick the next buildable idea from docs/ideas/README.md § Backlog (candidate noted earlier: a `currency --check` registry-delta preflight verb).

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
