# Self Improvement seat — heartbeat
updated: 2026-07-15T22:47Z · phase: EAP EXTENSION ACTIVE (EAP through 2026-07-21; inbox consumed 001–024; routines coordinator-managed)

## This wake (2026-07-15 · work slice · claude/archive-ready-plan · PR #410)
- Slice: baton item 1 — the archive-ready close-out surface PLAN. Wake probe `python3 dist/bootstrap.py currency --check` exit 0 at sync HEAD 0984d95 (#409) — registry current, so the slice fell to the baton. Preconditions: no inbox ORDER above 024 (the "ORDER 025" text ~line 210 is the acked fm relay inside ORDER 019); control/claims/ README-only at scan; zero open PRs before this one (list_pull_requests, 22:43Z).
- Shipped: docs/planning/2026-07-15-archive-ready-close-out-plan.md — surface contract (`archive-prep` draft verb + REQUIRES-PROBE slot semantics + advisory-red `check --strict`), evidence-source split (tree-local fills vs session-resolved slots — engine stays stdlib-only/offline), 3 decide-and-flag design decisions, slices S1–S5 each a follow-up PR, verification incl. the "next real archive event runs the verb" done-measure. Idea flipped captured → routed (outcome stays open until a build slice merges); docs/ideas/README.md backlog line refreshed.
- Verify (at 4a98a34): `python3 scripts/preflight.py` → 9/9 legs green (pytest 1652 passed 1 skipped; dist-byte-pin; ruff; idea-index; retro-index; changelog-structure; taxonomy-sync; program-law; bench-integrity). `python3 dist/bootstrap.py check --strict` → exit 0; holds red only on this PR's own born-red card (designed hold); 3 staged-regen-lag advisories are pre-existing and never exit-affecting.

## Routine state (observed facts)
- This session armed no triggers and ran no new trigger inventory. Routines are coordinator-managed this wake.
- Carried observation (2026-07-15 ~04:4xZ read-only list_triggers pass): "Self Improvement failsafe wake" trig_01CUfSZo9Uky9DdpoqpZPcfT — cron `0 */2 * * *`, enabled=true, created 2026-07-15T04:38:07Z via meta_mcp, bound to a coordinator session (persistent_session_id session_01SFVAo5bPD41RMx9TzGxnPY) — plus one pending one-shot pacemaker (run_once_at 2026-07-15T04:55:00Z, same session binding). Not created by this seat's sessions.
- ⚑ FOR OWNER REVIEW: ORDER 024 (control/inbox.md @ 58b3f80) states "do NOT re-arm routines yet; wait for the owner's per-seat go (the v3.6 reboot prompt IS that go)". The observed failsafe above post-dates that order. This heartbeat records the discrepancy neutrally for the owner's review/veto; it does not adjudicate it. Prior heartbeat (git history @ 58b3f80) had recorded all seat routines verified DOWN; kit-lab daily loop re-arm recipe remains docs/operations/lab-loop.md.

## State
- kit: v1.17.0
- Archive-ready close-out surface: PLANNED (PR #410) — docs/planning/2026-07-15-archive-ready-close-out-plan.md; buildable next increment is S1 (checklist doctrine + note template, docs-only), then S2 (`archive-prep` draft verb), S3 (REQUIRES-PROBE slots), S4 (`check --strict` advisory + red fixture), S5 (release-wave distribution).
- Registry (docs/adopters.md) current: `currency --check` exit 0 at this wake's sync HEAD (last regen PR #409, gba-homebrew `kit:` line row). Run the probe FROM THE REPO ROOT — elsewhere it exits 1 with "no roster", a cwd artifact, not a regen signal. A mid-scan `Connection reset by peer` traceback is a network blip — retry once before reading it as anything.
- Wake currency scan is turnkey (#392): `python3 dist/bootstrap.py currency --check` — exit 0 registry current / exit 1 regen slice due (changed rows printed). Use it instead of hand-fetching adopter `kit:` lines.
- Answer-time gate-safety advisory SHIPPED (#407, main @ df686a0): the silent won't-drive-CI seam of the #405 honored lane surfaces the moment a prose-y `verify_command` is typed, with the runnable rewrite named.
- Gate verify_command honored (#405): the CI-runner⇄CLAUDE.md verify-line divergence class is closed — a confirmed, gate-safe, non-default `verify_command` interview slot drives the generated substrate-gate's test step; pytest fallback byte-identical otherwise; #407 adds the answer-time advisory half.
- Taxonomy-surface sync checker SHIPPED (#404); substrate-gate pytest step SHIPPED (#403); engagement-honesty pair SHIPPED (#402 + #401); template↔local-copy sync advisory SHIPPED (#399) + 4 findings hand-synced (#400).
- Grounded-skills measurement: harness MERGED (#386, main @ c5380dc) — turnkey: `python3 scripts/measure_grounded_skills.py --clone --workdir <dir> --json <f> --out <f>`; protocol pre-registered at docs/operations/grounded-skills-measurement.md.
- Revival boot reading: CONSTITUTION.md → control/inbox.md → this file → docs/eap-closeout-walkthrough-2026-07-14.md §E → docs/audits/eap-project-audit-2026-07-14.md.

## Next-2 baton
1. Archive-ready surface slice S1 — checklist doctrine + note template (`src/engine/templates/`, planted like the other doctrine surfaces; docs-only, smallest shippable) per docs/planning/2026-07-15-archive-ready-close-out-plan.md §5; contained alternates among the remaining captured Backlog: pinned-feed-contract-doctrine note (docs/ideas/pinned-feed-contract-doctrine-2026-07-09.md — a groomed-ideas doctrine-note increment) · make_seed yield-keyword fix (docs/ideas/make-seed-yield-keyword-bug-2026-07-09.md — buildable but `bench/seeds/` is a PIN PATH → rides `do-not-automerge`). Backlog NOT dry: those plus scan_fleet bounded per-fetch retry (#409 card 💡) and two non-kit-side captures (folded-gate → their lane; control-board cell → websites) remain.
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
