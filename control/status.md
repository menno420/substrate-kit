# Self Improvement seat — heartbeat
updated: 2026-07-15T19:41Z · phase: EAP EXTENSION ACTIVE (EAP through 2026-07-21; inbox consumed 001–024; routines coordinator-managed)

## This wake (2026-07-15 · work slice · claude/taxonomy-sync-checker · PR #404)
- Baton item 1 executed (no inbox ORDER above 024 at sync HEAD f3ab863; control/claims/ held README only at the 19:3xZ scan; zero open PRs at open; `currency --check` exit 0 from repo root — no regen slice due): shipped the taxonomy-surface sync checker (idea taxonomy-surface-sync-checker-2026-07-09, the PL-010 hand-sync friction). `scripts/check_taxonomy_sync.py` (stdlib, import-free, PL-008 header) asserts set-equality between the canonical `MODEL_TASK_CLASSES` tuple (src/engine/grammar.py), the allocation-ladder table's first column (emphasis/flags stripped, revision-log table ignored), and the telemetry/README.md class list, plus the README's "the N PL-004 classes" count honesty; parse failure on any surface is a finding, never a silent pass. Wired as a kit-quality CI step (lane-conditioned — heartbeat PRs never pay it) and a `preflight.py` leg (`taxonomy-sync`); deliberately-desynced fixtures red in tests/test_check_taxonomy_sync.py (15 tests, incl. the pinning real-repo-in-sync fixture), the real repo passes. Idea flipped shipped (window closes 2026-08-14); CHANGELOG under [Unreleased] ### Added. Repo-level guard, not engine code — dist byte-pin unchanged (verified byte-identical by the preflight leg).
- Verify (at 7767707): `python3 scripts/preflight.py` → 9/9 legs green (pytest 1645 passed 1 skipped in 39.74s; dist-byte-pin; ruff; idea-index; retro-index; changelog-structure; taxonomy-sync; program-law; bench-integrity). `dist/bootstrap.py check --strict` → designed born-red HOLD only (this wake's card, pre-flip) + known staged-regen-lag ×3 + the required-unverified NOTE; guard-fires telemetry delta committed with the session.

## Routine state (observed facts)
- This session armed no triggers and ran no new trigger inventory. Routines are coordinator-managed this wake.
- Carried observation (2026-07-15 ~04:4xZ read-only list_triggers pass): "Self Improvement failsafe wake" trig_01CUfSZo9Uky9DdpoqpZPcfT — cron `0 */2 * * *`, enabled=true, created 2026-07-15T04:38:07Z via meta_mcp, bound to a coordinator session (persistent_session_id session_01SFVAo5bPD41RMx9TzGxnPY) — plus one pending one-shot pacemaker (run_once_at 2026-07-15T04:55:00Z, same session binding). Not created by this seat's sessions.
- ⚑ FOR OWNER REVIEW: ORDER 024 (control/inbox.md @ 58b3f80) states "do NOT re-arm routines yet; wait for the owner's per-seat go (the v3.6 reboot prompt IS that go)". The observed failsafe above post-dates that order. This heartbeat records the discrepancy neutrally for the owner's review/veto; it does not adjudicate it. Prior heartbeat (git history @ 58b3f80) had recorded all seat routines verified DOWN; kit-lab daily loop re-arm recipe remains docs/operations/lab-loop.md.

## State
- kit: v1.17.0
- v1.17.0 distributed 9/9 engaged adopters; registry (docs/adopters.md, generated 13:14:20Z at #391) current — this wake's `currency --check` run confirmed exit 0 (12 repos, rows-only compare, zero delta); DRIFT rows unchanged. Wake note: run the probe FROM THE REPO ROOT — from elsewhere it exits 1 with "no roster", a cwd artifact, not a regen signal.
- Wake currency scan is turnkey (#392): `python3 dist/bootstrap.py currency --check` — exit 0 registry current / exit 1 regen slice due (changed rows printed). Use it instead of hand-fetching adopter `kit:` lines.
- Taxonomy-surface sync checker SHIPPED (PR #404, this wake): the PL-010 three-surface hand-sync class is enforced — TASK_CLASSES ⇄ ladder ⇄ telemetry README set-equality (plus README count honesty) reds kit-quality on the next silent desync.
- Substrate-gate pytest step SHIPPED (#403, prior wake): the tests-blind-gate class is closed template-side — every wired adopter's test suite ships with its CI runner on the next upgrade/regen wave; self-skips when `tests/` is absent.
- Engagement wiring-STRENGTH advisory SHIPPED (#402): the weak-form class (#38) nudges with the exact missing legs + the staged one-copy fix; the gate says honestly that required-check status is owner-UI state (#36 r3). Closes the engagement-honesty pair opened by #401 (native_gate).
- Engagement native-consumer state SHIPPED (#401): pin-only adopters with real native enforcement (the superbot shape) declare `native_gate` in `substrate.config.json` and stop false-redding `enforcement-unwired`; acceptance is the visible `enforcement-native` NOTE.
- Template↔local-copy sync: advisory SHIPPED (#399), 4 first-run findings HAND-SYNCED (#400) — the kit tree is heading-set clean; the checker guards the class mechanically going forward.
- Grounded-skills measurement: harness MERGED (#386, main @ c5380dc) — turnkey: `python3 scripts/measure_grounded_skills.py --clone --workdir <dir> --json <f> --out <f>`; protocol pre-registered at docs/operations/grounded-skills-measurement.md.
- Revival boot reading: CONSTITUTION.md → control/inbox.md → this file → docs/eap-closeout-walkthrough-2026-07-14.md §E → docs/audits/eap-project-audit-2026-07-14.md.

## Next-2 baton
1. Gate test step honors the interview's `verify_command` slot (💡 on the #403 card, .sessions/2026-07-15-adopt-pytest-gate-step.md — dedup'd against docs/ideas/ that session; needs its idea file captured with the increment): `live_ci_workflow` hardcodes `-m pytest tests/ -q` while the adopt interview already records `verify_command` (src/engine/interview/question_bank.py:86, routed to templates/CLAUDE.md) — prefer the state-recorded slot (filled + non-default) as the test-step command, pytest as fallback, so the CI runner stops diverging from the verify line CLAUDE.md teaches. Alternates if judged bigger than one slice: archive-ready-close-out-surface · control-board-readiness-cell.
2. Grounded-skills measurement window ~2026-07-19..26 — run per docs/operations/grounded-skills-measurement.md (turnkey since #386 merged; PR #247 methodology; owner silence accepts); publish the findings report under docs/reports/ and link it from the operations index.

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
