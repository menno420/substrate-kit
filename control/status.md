# Self Improvement seat — heartbeat
updated: 2026-07-15T18:50Z · phase: EAP EXTENSION ACTIVE (EAP through 2026-07-21; inbox consumed 001–024; routines coordinator-managed)

## This wake (2026-07-15 · work slice · claude/engagement-wiring-strength · PR #402)
- Baton item 1 executed (no inbox ORDER above 024 at sync HEAD ee081ed; control/claims/ held README only at the 18:3xZ scan; zero open PRs at open; `currency --check` exit 0 from repo root — no regen slice due): shipped the engagement wiring-STRENGTH advisory (idea engagement-wiring-strength-verification-2026-07-12, friction #36 r3 + #38 residuals, both layers). Layer 1: `check_enforcement_strength` fires the advisory-only `enforcement-weak-form` finding when the wired plain-form `check --strict` door skips staged-gate legs (`--require-session-log`, diff-aware `--session-log`, `--inbox-base`) that the staged `<state_dir>/ci/substrate-gate.yml` carries — missing legs named, staged file named as the one-copy fix, never strict-red (a hand-rolled gate is legitimate; the kit's own ci.yml carries all three legs and self-silences). Token-boundary matching (`--require-session-log` never satisfies the `--session-log` leg) on comment-stripped text only. Layer 2: `required_unverified_note` emits the `enforcement-required-unverified` honesty NOTE on `check`'s full lane whenever a CI door exists (kit-shaped or accepted native_gate) — required-check status is owner-UI state the stdlib engine cannot read; the note names the expected context. Idea flipped shipped (window closes 2026-08-14); dist byte-pin regenerated; CHANGELOG under [Unreleased] ### Added.
- Verify (at ed04666): `python3 scripts/preflight.py` → 8/8 legs green (pytest 1629 passed 1 skipped in 48.11s; dist-byte-pin; ruff; idea-index; retro-index; changelog-structure; program-law; bench-integrity). `dist/bootstrap.py check --strict` → designed born-red HOLD only (this wake's card, pre-flip) + known staged-regen-lag ×3; the required-unverified NOTE fires live on the kit tree; no weak-form advisory (kit ci.yml is strong-form — the designed self-silence). The #400 card's model-line-shape advisory (payload one `·` short) fixed in the flip commit — one-token copy-edit, self-silences that advisory.

## Routine state (observed facts — trigger inventory carried from the 2026-07-15 ~04:4xZ read-only list_triggers pass; this wake armed no triggers)
- This session armed no triggers and ran no new trigger inventory. Routines are coordinator-managed this wake.
- Carried observation (04:4xZ pass): "Self Improvement failsafe wake" trig_01CUfSZo9Uky9DdpoqpZPcfT — cron `0 */2 * * *`, enabled=true, created 2026-07-15T04:38:07Z via meta_mcp, bound to a coordinator session (persistent_session_id session_01SFVAo5bPD41RMx9TzGxnPY) — plus one pending one-shot pacemaker (run_once_at 2026-07-15T04:55:00Z, same session binding). Not created by this seat's sessions.
- ⚑ FOR OWNER REVIEW: ORDER 024 (control/inbox.md @ 58b3f80) states "do NOT re-arm routines yet; wait for the owner's per-seat go (the v3.6 reboot prompt IS that go)". The observed failsafe above post-dates that order. This heartbeat records the discrepancy neutrally for the owner's review/veto; it does not adjudicate it. Prior heartbeat (git history @ 58b3f80) had recorded all seat routines verified DOWN; kit-lab daily loop re-arm recipe remains docs/operations/lab-loop.md.

## State
- kit: v1.17.0
- v1.17.0 distributed 9/9 engaged adopters; registry (docs/adopters.md, generated 13:14:20Z at #391) current — the 18:2xZ `currency --check` live run confirmed exit 0 (12 repos, rows-only compare, zero delta); DRIFT rows unchanged. Wake note: run the probe FROM THE REPO ROOT — from elsewhere it exits 1 with "no roster", a cwd artifact, not a regen signal.
- Wake currency scan is turnkey (#392): `python3 dist/bootstrap.py currency --check` — exit 0 registry current / exit 1 regen slice due (changed rows printed). Use it instead of hand-fetching adopter `kit:` lines.
- Engagement wiring-STRENGTH advisory SHIPPED (PR #402, this wake): the weak-form class (#38 — plain-form wiring read as fully wired) now nudges with the exact missing legs + the staged one-copy fix, and the gate says honestly that required-check status is owner-UI state (#36 r3). Closes the engagement-honesty pair opened by #401 (native_gate) — adopters inherit on the next upgrade/regen wave.
- Engagement native-consumer state SHIPPED (#401, prior wake): pin-only adopters with real native enforcement (the superbot shape) declare `native_gate` in `substrate.config.json` and stop false-redding `enforcement-unwired`; acceptance is the visible `enforcement-native` NOTE.
- Template↔local-copy sync: advisory SHIPPED (#399) and its 4 first-run findings HAND-SYNCED (#400) — the kit tree is heading-set clean; the checker guards the class mechanically going forward. Adopters inherit the enriched ideas-README template on the next upgrade/regen wave.
- Dispatch-race re-verify doctrine shipped (#398): lab-loop STEP 2 carries both halves of the parallel-lane guard — CLAIM BEFORE BUILD (#397) + RE-VERIFY THEN STAND DOWN (#398). Console re-paste of the fenced prompt pending post-merge (one re-paste covers #397+#398).
- Cross-branch ORDER-collision guard fully closed (#365 mechanism + #397 doc segments): work claims carry `--order NNN`, `check_claims` emits `claims-order-collision`, the claim verb refuses cross-branch duplicates, and the lab-loop prompt claims-before-build.
- Grounded-skills measurement: harness MERGED (#386, main @ c5380dc) — turnkey: `python3 scripts/measure_grounded_skills.py --clone --workdir <dir> --json <f> --out <f>`; protocol pre-registered at docs/operations/grounded-skills-measurement.md.
- Revival boot reading: CONSTITUTION.md → control/inbox.md → this file → docs/eap-closeout-walkthrough-2026-07-14.md §E → docs/audits/eap-project-audit-2026-07-14.md.

## Next-2 baton
1. `adopt --wire-enforcement` plants a pytest step when tests/ exists (docs/ideas/adopt-plants-pytest-gate-step-2026-07-10.md): captured, ordinary lane — the superbot-games gen-1 tests-blind-gate class (73 tests never in CI, fixed consumer-side games#16); contained template addition, engine change → dist byte-pin. Smallest genuine backlog win now that the engagement-honesty pair (#401+#402) is closed.
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
