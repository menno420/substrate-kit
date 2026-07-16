# Self Improvement seat — heartbeat
updated: 2026-07-16T00:20Z · phase: EAP EXTENSION ACTIVE (EAP through 2026-07-21; inbox consumed 001–024; failsafe wake 2026-07-16T00:05Z)

## This wake (2026-07-16 00:05Z failsafe fire · worker session)
- Wake source: the standing failsafe cron trig_01CUfSZo9Uky9DdpoqpZPcfT fired 00:04:30Z as designed (the ender left it armed as the dead-man bridge); no ORDER >024 found at HEAD; no open PRs at orient; `currency --check` exit 0 (registry current — no drift slice).
- Shipped: baton item 1 — archive-ready close-out slice S1 (checklist doctrine + note template, docs-only) per docs/planning/2026-07-15-archive-ready-close-out-plan.md §5. PR #412 (claude/archive-ready-s1): src/engine/templates/archive-ready.md.tmpl (plan-§2 sections in the KL-5 fill-slot grammar; routine state REQUIRES-PROBE; confirmation slot never drafted complete; badge token `archive` from the allowed set — an unresolved fill slot IS the draft-state signal), docs/operations/archive-ready-close-out.md (binding checklist doctrine, linked from the operations index), pointer-guard _KIT_SELF_REFS entry, CHANGELOG [Unreleased], dist regen (template embed only, no engine logic).
- Verified at b8250d9: scripts/preflight.py 9/9 green (pytest 1652 passed, 1 skipped); dist/bootstrap.py check --strict shows only the designed born-red HOLD (this session's card, pre-flip), the known staged-regen-lag ×3, and the required-unverified NOTE; guard-fires telemetry delta committed with the session.

## Routine state (observed facts)
- FAILSAFE "Self Improvement failsafe wake" trig_01CUfSZo9Uky9DdpoqpZPcfT (cron `0 */2 * * *`) remains ARMED as left by the 07-15 ender; this wake armed nothing, deleted nothing, sent nothing (send_later prohibited for this session).
- ⚑ FOR OWNER REVIEW: ORDER 024 (control/inbox.md @ 58b3f80) states "do NOT re-arm routines yet; wait for the owner's per-seat go (the v3.6 reboot prompt IS that go)". The observed failsafe above post-dates that order. This heartbeat records the discrepancy neutrally for the owner's review/veto; it does not adjudicate it. Prior heartbeat (git history @ 58b3f80) had recorded all seat routines verified DOWN; kit-lab daily loop re-arm recipe remains docs/operations/lab-loop.md.

## State
- kit: v1.17.0
- Archive-ready close-out surface: S1 SHIPPED (PR #412) — checklist doctrine (docs/operations/archive-ready-close-out.md) + note template (src/engine/templates/archive-ready.md.tmpl). Plan: docs/planning/2026-07-15-archive-ready-close-out-plan.md; next buildable increment is S2 (`archive-prep` draft verb — sibling of ensure_draft, add_parser + dispatch in src/engine/cli.py, fail-open, tests), then S3 (REQUIRES-PROBE slot semantics), S4 (`check --strict` advisory + red fixture), S5 (release-wave distribution).
- Registry (docs/adopters.md) current: `currency --check` exit 0 at this wake (last regen PR #409; all five tracked adopters at v1.17.0). Run the probe FROM THE REPO ROOT — elsewhere it exits 1 with "no roster", a cwd artifact, not a regen signal. A mid-scan `Connection reset by peer` traceback is a network blip — retry once before reading it as anything.
- Wake currency scan is turnkey (#392): `python3 dist/bootstrap.py currency --check` — exit 0 registry current / exit 1 regen slice due (changed rows printed). Use it instead of hand-fetching adopter `kit:` lines.
- Answer-time gate-safety advisory SHIPPED (#407); gate verify_command honored (#405); taxonomy-surface sync checker SHIPPED (#404); substrate-gate pytest step SHIPPED (#403); engagement-honesty pair SHIPPED (#402 + #401); template↔local-copy sync advisory SHIPPED (#399).
- Grounded-skills measurement: harness MERGED (#386) — turnkey: `python3 scripts/measure_grounded_skills.py --clone --workdir <dir> --json <f> --out <f>`; protocol pre-registered at docs/operations/grounded-skills-measurement.md.
- Revival boot reading: CONSTITUTION.md → control/inbox.md → this file → docs/eap-closeout-walkthrough-2026-07-14.md §E → docs/audits/eap-project-audit-2026-07-14.md.

## Next-2 baton
1. Archive-ready close-out slice S2 — the `archive-prep` draft verb (evidence-draft half: new loop module function sibling of ensure_draft in src/engine/loop/handoff.py or a new archive.py; add_parser + dispatch in src/engine/cli.py; fail-open; tests for draft/re-run/never-touch-complete). Plan: docs/planning/2026-07-15-archive-ready-close-out-plan.md §5 S2 — depends on S1's template (shipped, PR #412).
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
