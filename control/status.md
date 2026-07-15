# Self Improvement seat — heartbeat
updated: 2026-07-15T14:25Z · phase: EAP EXTENSION ACTIVE (EAP through 2026-07-21; inbox consumed 001–024; routines coordinator-managed)

## This wake (2026-07-15 · work slice · claude/model-line-unrecorded-marker · PR #394)
- Baton item 2 built (no inbox ORDER above 024; control/claims/ held README only at the ~14:1xZ scan; zero open PRs at open): the model-line `unrecorded` effort marker (idea docs/ideas/model-line-unrecorded-effort-marker-2026-07-15.md, captured at #390) — `MODEL_EFFORT_UNRECORDED` carve-out in `check_model_line` (commit 2c0ba8d): an effort segment of exactly `unrecorded` no longer fires `model-line-effort` (the honest retro-backfill for cards whose authors never self-reported a tier; a standing nag invited a later wake to invent one), `MODEL_EFFORT_VALUES` stays `(low, medium, high)` (any other off-taxonomy value still nags), harvest records `unrecorded` verbatim (test-pinned). Plus the `.sessions/README.md` reservation line, 3 new tests, dist byte-pin regen, idea lifecycle flip (frontmatter shipped_pr 394 + README Backlog → Shipped), CHANGELOG [Unreleased] ### Changed entry.
- Fix-on-sight rider (7e71513, flagged on the session card): the #393 merge-verification-probe card's Model line was shape-malformed (Model + Run-type merged on one line — the new lint fired `model-line-shape`; harvest recorded NOTHING). Split to the taught form as the mechanism's first live use: `sonnet-5 · unrecorded · docs-only` (author self-report kept · no invented tier · factual class). All model-line payload advisories on this tree are now zero.
- Verify (at 7e71513): `python3 scripts/preflight.py` → 8/8 legs green (pytest 1604 passed, 1 skipped — 3 new tests; ruff; dist-byte-pin; idea-index; retro-index; changelog-structure; program-law; bench-integrity). `dist/bootstrap.py check --strict` → designed born-red HOLD only (this wake's card, pre-flip) + known staged-regen-lag ×3; the two standing `unrecorded` model-line-effort nags are GONE (silenced honestly, per the idea) and no model-line advisory remains. Guard-fires telemetry delta committed per checker instruction (7e71513).

## Routine state (observed facts — trigger inventory carried from the 2026-07-15 ~04:4xZ read-only list_triggers pass; this wake armed no triggers)
- This session armed no triggers and ran no new trigger inventory. Routines are coordinator-managed this wake.
- Carried observation (04:4xZ pass): "Self Improvement failsafe wake" trig_01CUfSZo9Uky9DdpoqpZPcfT — cron `0 */2 * * *`, enabled=true, created 2026-07-15T04:38:07Z via meta_mcp, bound to a coordinator session (persistent_session_id session_01SFVAo5bPD41RMx9TzGxnPY) — plus one pending one-shot pacemaker (run_once_at 2026-07-15T04:55:00Z, same session binding). Not created by this seat's sessions.
- ⚑ FOR OWNER REVIEW: ORDER 024 (control/inbox.md @ 58b3f80) states "do NOT re-arm routines yet; wait for the owner's per-seat go (the v3.6 reboot prompt IS that go)". The observed failsafe above post-dates that order. This heartbeat records the discrepancy neutrally for the owner's review/veto; it does not adjudicate it. Prior heartbeat (git history @ 58b3f80) had recorded all seat routines verified DOWN; kit-lab daily loop re-arm recipe remains docs/operations/lab-loop.md.

## State
- kit: v1.17.0
- v1.17.0 distributed 9/9 engaged adopters; registry (docs/adopters.md, generated 13:14:20Z at #391) current — the #392 wake's `currency --check` live run confirmed zero row delta; DRIFT 4 repos (superbot-next, superbot-games, superbot-mineverse self-report lag + kit's tree-internal pin row) — unchanged; this wake ran no currency scan (exit-code-driven: fire a regen slice only when `currency --check` exits 1).
- Wake currency scan is turnkey (#392): `python3 dist/bootstrap.py currency --check` — exit 0 registry current / exit 1 regen slice due (changed rows printed). Use it instead of hand-fetching adopter `kit:` lines.
- Model-line effort taxonomy (#394): `unrecorded` is the sanctioned terminal value for retro-repaired cards whose authors never self-reported effort — advisory-silent, harvested verbatim; live sessions still report `low|medium|high` (.sessions/README.md teaches the reservation).
- Grounded-skills measurement: harness MERGED (#386, main @ c5380dc) — turnkey: `python3 scripts/measure_grounded_skills.py --clone --workdir <dir> --json <f> --out <f>`; protocol pre-registered at docs/operations/grounded-skills-measurement.md.
- Revival boot reading: CONSTITUTION.md → control/inbox.md → this file → docs/eap-closeout-walkthrough-2026-07-14.md §E → docs/audits/eap-project-audit-2026-07-14.md.

## Next-2 baton
1. Grounded-skills measurement window ~2026-07-19..26 — run per docs/operations/grounded-skills-measurement.md (turnkey since #386 merged; PR #247 methodology; owner silence accepts); publish the findings report under docs/reports/ and link it from the operations index.
2. Next buildable idea from the Backlog (14 captured rows remain — not dry): heartbeat delegated-tally guidance (docs/ideas/heartbeat-delegated-tally-guidance-2026-07-13.md) — a docs-guidance quick-win documenting the coordinator delegated-tally pattern the mineverse consumer evidenced; alternative if a live-repo signal preempts: the plain-adopt lane-drift advisory (docs/ideas/plain-adopt-lane-drift-advisory-2026-07-10.md).

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
