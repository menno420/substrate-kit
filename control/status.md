# Self Improvement seat — heartbeat
updated: 2026-07-15T20:20Z · phase: EAP EXTENSION ACTIVE (EAP through 2026-07-21; inbox consumed 001–024; routines coordinator-managed)

## This wake (2026-07-15 · work slice · claude/gate-verify-command · PR #405)
- Baton item 1 executed (no inbox ORDER above 024 at sync HEAD e196936; control/claims/ held README only at the 20:0xZ scan; zero open PRs at open; `currency --check` exit 0 from repo root — no regen slice due): the substrate-gate test step honors the interview's `verify_command` slot (the 💡 captured on the #403 card; idea file gate-verify-command-slot-2026-07-15 captured with the increment per the baton note). New `engine.adopt.gate_test_command`: a FILLED (user-confirmed — provisional/derived never drives a workflow every PR executes), GATE-SAFE (single line, conservative shell-safe allowlist, no unfilled `${...}` — the slot is free prose routed into CLAUDE.md; websites' real value carries parenthetical annotations that are documentation, not shell), NON-DEFAULT (plain pytest keeps the strictly-more-robust fallback) slot value drives the generated gate's test step verbatim via `live_ci_workflow(test_command=…)`; `None` keeps the #403 fallback byte-identical (zero gate churn for non-qualifying adopters). Honored lane: no tests/-absent self-skip (a confirmed command is a runnable promise), requirements.txt install kept, pytest installed only when the command mentions it. Writer/scanner symmetry: `upgrade.scan_gate_carveouts` loads state.json fail-open and computes the same verdict, so kit-owned verify-step bytes never rescan as a phantom carve-out. Tests: verdict matrix (filled/provisional/default/unsafe/chained), template branch, adopt end-to-end (staged+installed+report line), upgrade regen keep + read-only rescan clean. CHANGELOG under [Unreleased] ### Changed; dist byte-pin regenerated.
- Verify (at 79b1d76): `python3 scripts/preflight.py` → 9/9 legs green (pytest 1650 passed 1 skipped in 34.75s; dist-byte-pin; ruff; idea-index; retro-index; changelog-structure; taxonomy-sync; program-law; bench-integrity). `dist/bootstrap.py check --strict` → designed born-red HOLD only (this wake's card, pre-flip) + known staged-regen-lag ×3 + the required-unverified NOTE; guard-fires telemetry delta committed with the session (07982e5).

## Routine state (observed facts)
- This session armed no triggers and ran no new trigger inventory. Routines are coordinator-managed this wake.
- Carried observation (2026-07-15 ~04:4xZ read-only list_triggers pass): "Self Improvement failsafe wake" trig_01CUfSZo9Uky9DdpoqpZPcfT — cron `0 */2 * * *`, enabled=true, created 2026-07-15T04:38:07Z via meta_mcp, bound to a coordinator session (persistent_session_id session_01SFVAo5bPD41RMx9TzGxnPY) — plus one pending one-shot pacemaker (run_once_at 2026-07-15T04:55:00Z, same session binding). Not created by this seat's sessions.
- ⚑ FOR OWNER REVIEW: ORDER 024 (control/inbox.md @ 58b3f80) states "do NOT re-arm routines yet; wait for the owner's per-seat go (the v3.6 reboot prompt IS that go)". The observed failsafe above post-dates that order. This heartbeat records the discrepancy neutrally for the owner's review/veto; it does not adjudicate it. Prior heartbeat (git history @ 58b3f80) had recorded all seat routines verified DOWN; kit-lab daily loop re-arm recipe remains docs/operations/lab-loop.md.

## State
- kit: v1.17.0
- v1.17.0 distributed 9/9 engaged adopters; registry (docs/adopters.md, generated 13:14:20Z at #391) current — this wake's `currency --check` run confirmed exit 0 (12 repos, rows-only compare, zero delta); DRIFT rows unchanged. Wake note: run the probe FROM THE REPO ROOT — from elsewhere it exits 1 with "no roster", a cwd artifact, not a regen signal.
- Wake currency scan is turnkey (#392): `python3 dist/bootstrap.py currency --check` — exit 0 registry current / exit 1 regen slice due (changed rows printed). Use it instead of hand-fetching adopter `kit:` lines.
- Gate verify_command honored (PR #405, this wake): the CI-runner⇄CLAUDE.md verify-line divergence class is closed — a confirmed, gate-safe, non-default `verify_command` interview slot drives the generated substrate-gate's test step; pytest fallback byte-identical otherwise; carve-out rescan reads the same slot.
- Taxonomy-surface sync checker SHIPPED (#404, prior wake): TASK_CLASSES ⇄ ladder ⇄ telemetry README set-equality (plus README count honesty) reds kit-quality on the next silent desync.
- Substrate-gate pytest step SHIPPED (#403): the tests-blind-gate class is closed template-side — every wired adopter's test suite ships with its CI runner on the next upgrade/regen wave; self-skips when `tests/` is absent.
- Engagement wiring-STRENGTH advisory SHIPPED (#402) + native-consumer state (#401): the engagement-honesty pair — weak-form nudge with exact missing legs; `native_gate` declared-evidence class with the visible `enforcement-native` NOTE.
- Template↔local-copy sync: advisory SHIPPED (#399), 4 first-run findings HAND-SYNCED (#400) — the kit tree is heading-set clean; the checker guards the class mechanically going forward.
- Grounded-skills measurement: harness MERGED (#386, main @ c5380dc) — turnkey: `python3 scripts/measure_grounded_skills.py --clone --workdir <dir> --json <f> --out <f>`; protocol pre-registered at docs/operations/grounded-skills-measurement.md.
- Revival boot reading: CONSTITUTION.md → control/inbox.md → this file → docs/eap-closeout-walkthrough-2026-07-14.md §E → docs/audits/eap-project-audit-2026-07-14.md.

## Next-2 baton
1. Archive-ready close-out surface (docs/ideas/archive-ready-close-out-surface-2026-07-11.md — the alternate the #404 baton named): build if genuinely contained after re-reading the idea file at HEAD; second alternate control-board-readiness-cell (docs/ideas/control-board-kit-readiness-cell-2026-07-09.md, kit side rides the ORDER 003 `kit:` line + docs/adopters.md already shipped — re-verify what remains). Before either: re-scan the idea index Backlog for anything higher-evidence captured since this stamp.
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
