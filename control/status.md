# Self Improvement seat — heartbeat
updated: 2026-07-15T23:05Z · phase: EAP EXTENSION ACTIVE (EAP through 2026-07-21; inbox consumed 001–024; session closed 2026-07-15 ~23:00Z)

## This wake (2026-07-15 ~23:00Z · session close-out · coordinator ender)
- 27 PRs shipped and merged today — #382–#392, #394–#410: registry currency ×5 (websites / fleet-manager / superbot-next / trading-strategy / gba-homebrew all at v1.17.0); measurement harness #386; checkers — retro-index #388, template-sync #399, taxonomy-sync #404; gate — pytest step #403, verify_command #405, answer-time advisory #407; doctrine/docs — #395, #397, #398, #400, #410 archive-ready PLAN; idea-index #383; model-line sweep #390; unrecorded marker #394; engagement #401/#402; ORDER 024 acked+done at #382.
- Parked PRs: none — all landed green via the enabler.

## Routine state (observed facts)
- Routine disposition at close (verified via exhaustive paginated list_triggers at ~22:55Z): pending pacemaker trig_01PbP6p59h8iKZzPNkKEGAeR DELETED + verified absent; 29 fired one-shot pacemakers self-disabled (run_once_fired), none pending; no business crons exist for this seat (kit-lab daily remains deleted per ORDER 024); nothing new armed at close.
- FAILSAFE "Self Improvement failsafe wake" trig_01CUfSZo9Uky9DdpoqpZPcfT (cron `0 */2 * * *`, next fire 2026-07-16T00:04:30Z) LEFT ARMED as the successor's dead-man bridge — successor boot cutover rebinds-then-deletes it.
- ⚑ FOR OWNER REVIEW: ORDER 024 (control/inbox.md @ 58b3f80) states "do NOT re-arm routines yet; wait for the owner's per-seat go (the v3.6 reboot prompt IS that go)". The observed failsafe above post-dates that order. This heartbeat records the discrepancy neutrally for the owner's review/veto; it does not adjudicate it. Prior heartbeat (git history @ 58b3f80) had recorded all seat routines verified DOWN; kit-lab daily loop re-arm recipe remains docs/operations/lab-loop.md.

## State
- kit: v1.17.0
- Archive-ready close-out surface: PLANNED (PR #410) — docs/planning/2026-07-15-archive-ready-close-out-plan.md; buildable next increment is S1 (checklist doctrine + note template, docs-only), then S2 (`archive-prep` draft verb), S3 (REQUIRES-PROBE slots), S4 (`check --strict` advisory + red fixture), S5 (release-wave distribution).
- Registry (docs/adopters.md) current: all five tracked adopters (websites, fleet-manager, superbot-next, trading-strategy, gba-homebrew) at v1.17.0; `currency --check` exit 0 (last regen PR #409). Run the probe FROM THE REPO ROOT — elsewhere it exits 1 with "no roster", a cwd artifact, not a regen signal. A mid-scan `Connection reset by peer` traceback is a network blip — retry once before reading it as anything.
- Wake currency scan is turnkey (#392): `python3 dist/bootstrap.py currency --check` — exit 0 registry current / exit 1 regen slice due (changed rows printed). Use it instead of hand-fetching adopter `kit:` lines.
- Answer-time gate-safety advisory SHIPPED (#407): the silent won't-drive-CI seam of the #405 honored lane surfaces the moment a prose-y `verify_command` is typed, with the runnable rewrite named.
- Gate verify_command honored (#405): the CI-runner⇄CLAUDE.md verify-line divergence class is closed — a confirmed, gate-safe, non-default `verify_command` interview slot drives the generated substrate-gate's test step; pytest fallback byte-identical otherwise; #407 adds the answer-time advisory half.
- Taxonomy-surface sync checker SHIPPED (#404); substrate-gate pytest step SHIPPED (#403); engagement-honesty pair SHIPPED (#402 + #401); template↔local-copy sync advisory SHIPPED (#399) + 4 findings hand-synced (#400).
- Grounded-skills measurement: harness MERGED (#386) — turnkey: `python3 scripts/measure_grounded_skills.py --clone --workdir <dir> --json <f> --out <f>`; protocol pre-registered at docs/operations/grounded-skills-measurement.md.
- Revival boot reading: CONSTITUTION.md → control/inbox.md → this file → docs/eap-closeout-walkthrough-2026-07-14.md §E → docs/audits/eap-project-audit-2026-07-14.md.

## Next-2 baton
1. Archive-ready close-out slice S1 — checklist doctrine + note template, docs-only (plan: docs/planning/2026-07-15-archive-ready-close-out-plan.md).
2. Grounded-skills measurement window ~2026-07-19..26 — run per docs/operations/grounded-skills-measurement.md, publish the findings report under docs/reports/.

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
