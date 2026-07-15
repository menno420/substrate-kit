# Self Improvement seat — heartbeat
updated: 2026-07-15T18:05Z · phase: EAP EXTENSION ACTIVE (EAP through 2026-07-21; inbox consumed 001–024; routines coordinator-managed)

## This wake (2026-07-15 · work slice · claude/engagement-native-gate · PR #401)
- Baton item 1 executed (no inbox ORDER above 024 at sync HEAD 193bdb5; control/claims/ held README only at the 17:5xZ scan; zero open PRs at open; `currency --check` exit 0 from repo root — no regen slice due): shipped the engagement native-consumer state (idea engagement-native-consumer-state-2026-07-12, superbot friction #37, fix shape 1). `substrate.config.json` gains the opt-in `native_gate` declaration (`workflow` repo-relative path + informational `required_context`); when no workflow runs `check --strict`, the engagement gate accepts a declaration whose named workflow exists on disk instead of redding `enforcement-unwired` — acceptance surfaces as the `enforcement-native` NOTE in `check`'s full lane (visible, never silent); a dead declaration keeps the gate red with the path named in the finding; malformed declarations read as undeclared (misconfiguration never widens the gate). Guard recipe honored: pin + declaration + existing workflow + no strict-needle workflow reads engaged-native; same fixture undeclared stays `enforcement-unwired`; dead-declaration fixture stays red. Engine change → dist byte-pin regenerated; idea frontmatter/index flipped shipped (window closes 2026-08-14); CHANGELOG under [Unreleased] ### Added.
- Verify (at 43028da): `python3 scripts/preflight.py` → 8/8 legs green (pytest 1624 passed 1 skipped in 49.67s; dist-byte-pin; ruff; idea-index; retro-index; changelog-structure; program-law; bench-integrity). `dist/bootstrap.py check --strict` → designed born-red HOLD (this wake's card, pre-flip) + known staged-regen-lag ×3 + one model-line-shape advisory on the PREVIOUS wake's card (2026-07-15-template-local-sync.md payload has one `·` too few — telemetry-only, noted for the next tidy pass, not this PR's scope).

## Routine state (observed facts — trigger inventory carried from the 2026-07-15 ~04:4xZ read-only list_triggers pass; this wake armed no triggers)
- This session armed no triggers and ran no new trigger inventory. Routines are coordinator-managed this wake.
- Carried observation (04:4xZ pass): "Self Improvement failsafe wake" trig_01CUfSZo9Uky9DdpoqpZPcfT — cron `0 */2 * * *`, enabled=true, created 2026-07-15T04:38:07Z via meta_mcp, bound to a coordinator session (persistent_session_id session_01SFVAo5bPD41RMx9TzGxnPY) — plus one pending one-shot pacemaker (run_once_at 2026-07-15T04:55:00Z, same session binding). Not created by this seat's sessions.
- ⚑ FOR OWNER REVIEW: ORDER 024 (control/inbox.md @ 58b3f80) states "do NOT re-arm routines yet; wait for the owner's per-seat go (the v3.6 reboot prompt IS that go)". The observed failsafe above post-dates that order. This heartbeat records the discrepancy neutrally for the owner's review/veto; it does not adjudicate it. Prior heartbeat (git history @ 58b3f80) had recorded all seat routines verified DOWN; kit-lab daily loop re-arm recipe remains docs/operations/lab-loop.md.

## State
- kit: v1.17.0
- v1.17.0 distributed 9/9 engaged adopters; registry (docs/adopters.md, generated 13:14:20Z at #391) current — the 17:5xZ `currency --check` live run confirmed exit 0 (12 repos, rows-only compare, zero delta); DRIFT rows unchanged. Wake note: run the probe FROM THE REPO ROOT — from elsewhere it exits 1 with "no roster", a cwd artifact, not a regen signal.
- Wake currency scan is turnkey (#392): `python3 dist/bootstrap.py currency --check` — exit 0 registry current / exit 1 regen slice due (changed rows printed). Use it instead of hand-fetching adopter `kit:` lines.
- Engagement native-consumer state SHIPPED (PR #401, this wake): pin-only adopters with real native enforcement (the superbot shape) declare `native_gate` in `substrate.config.json` and stop false-redding `enforcement-unwired`; acceptance is the visible `enforcement-native` NOTE. Adopters inherit on the next upgrade/regen wave; the sibling captured idea (wiring-STRENGTH advisory, engagement-wiring-strength-verification-2026-07-12) is the natural follow-on.
- Template↔local-copy sync: advisory SHIPPED (#399) and its 4 first-run findings HAND-SYNCED (#400) — the kit tree is heading-set clean; the checker guards the class mechanically going forward. Adopters inherit the enriched ideas-README template on the next upgrade/regen wave.
- Dispatch-race re-verify doctrine shipped (#398): lab-loop STEP 2 carries both halves of the parallel-lane guard — CLAIM BEFORE BUILD (#397) + RE-VERIFY THEN STAND DOWN (#398). Console re-paste of the fenced prompt pending post-merge (one re-paste covers #397+#398).
- Cross-branch ORDER-collision guard fully closed (#365 mechanism + #397 doc segments): work claims carry `--order NNN`, `check_claims` emits `claims-order-collision`, the claim verb refuses cross-branch duplicates, and the lab-loop prompt claims-before-build.
- Plain-adopt lane-drift advisory (#396): `adopt` without `--lane` into a lane-shaped repo (non-default `heartbeat_files`) nudges `adopt --lane <name>` as the first report line — advisory, never a refusal; adopters inherit on next upgrade/regen wave.
- Delegated-tally doctrine (#395): coordinator-written heartbeats are marked, member repos carry a live-tally pointer, sweeps classify by PR record + coordinator status — `control/README.md` § "Delegated tally" (template: control-README.md.tmpl; adopters inherit on next upgrade/regen wave).
- Grounded-skills measurement: harness MERGED (#386, main @ c5380dc) — turnkey: `python3 scripts/measure_grounded_skills.py --clone --workdir <dir> --json <f> --out <f>`; protocol pre-registered at docs/operations/grounded-skills-measurement.md.
- Revival boot reading: CONSTITUTION.md → control/inbox.md → this file → docs/eap-closeout-walkthrough-2026-07-14.md §E → docs/audits/eap-project-audit-2026-07-14.md.

## Next-2 baton
1. Engagement wiring-STRENGTH advisory quick-win (docs/ideas/engagement-wiring-strength-verification-2026-07-12.md): advisory-only strength + required-ness-honesty notes in the engagement checker (plain-form `check --strict` reads fully wired while missing the session-log/diff-aware/inbox legs) — contained checker change, the idea carries the design; natural sibling of the #401 native-gate class.
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
