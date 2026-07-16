# Self Improvement seat — heartbeat
updated: 2026-07-16T02:16:31Z · phase: EAP EXTENSION ACTIVE (EAP through 2026-07-21; inbox consumed 001–024; worker-slice wake 2026-07-16T02:05Z)

## This wake (2026-07-16 02:05Z worker session) — RELEASE v1.18.0 CUT

- Wake source: coordinator-dispatched worker slice; hard-sync landed on edbf73a (#417 merge); no ORDER >024 at HEAD; baton item 1 (archive-ready S5 — release-wave distribution) executed per docs/planning/2026-07-15-archive-ready-close-out-plan.md §5 S5 + docs/operations/release-runbook.md.
- RELEASE RECORD: v1.18.0 · release.yml run 29466068874 (workflow_dispatch, completed success 2026-07-16T02:13:45Z) · tag object cd4f84281925 → commit 4c8e1d1f6141 (the #418 bump squash-merge) · sha256 d83a8a29bce90188ac4a6d01ebbfe1190e4568a85d12c63e7dbd23d9a5eef6c1 three-way PASS (downloaded asset == release.json field == committed dist/bootstrap.py @ 4c8e1d1, 1075538 bytes; scripts/verify_release.py tag+sha256 legs PASS; its workflow leg SKIPPED on the known proxy wall — "HTTP Error 403: Forbidden" on api.github.com Actions REST — run verified green via GitHub MCP instead, disclosed per doctrine).
- Merged: PR #418 (bump: both version homes → 1.18.0, CHANGELOG [Unreleased] → [1.18.0] - 2026-07-16, dist regen byte-pin 1075538, plus a runbook-§0 payload fix — the missing #386 grounded-skills-harness CHANGELOG entry, found by the pre-cut sweep and backfilled). No KF-5 benchmark blocks in [Unreleased] this cycle — nothing to hand-move.
- This close-out PR (#419): adopters regen + this heartbeat + claim delete (runbook §6). One red round-trip on its first kit-quality run (29466263869): the PR shipped card-less, but `docs/adopters.md` takes the full lane (card required in the merge-base diff) — only pure-`control/**` PRs ride the fast lane. Fixed with a close-out card + a runbook §6 clause; the same run's advisory also flagged the #418 card's invented task-class `release cut` → retro-fixed to `mechanical refactor (release cut)` (PL-004 prefix rule, #390 sweep class).
- Verified pre-flip at a2bea44: scripts/preflight.py all legs PASS (pytest 1679 passed, 1 skipped; dist-byte-pin green); build_release_json --verify-only "preconditions all green"; dist/bootstrap.py check --strict exit 0 post-flip.
- WALL STATUS CHANGES (both re-probed live this wake): (1) `enable_pr_auto_merge` SUCCEEDED on #418 at 2026-07-16T02:06:41Z — the GraphQL quota wall recorded on the #414/#415/#416 sessions ("API rate limit already exceeded for user ID 225413533") has CLEARED; (2) `release.yml` workflow_dispatch from a WORKER session SUCCEEDED (204, run queued) — the v1.17.0-cut worker-classifier wall ("workers cannot dispatch workflow_dispatch") did NOT reproduce. Walls are dated observations, not permanent state.
- Registry regen note: `currency` now reports superbot-games DRIFT (tree vs self-report disagree) alongside the kit's own expected mid-close DRIFT row; superbot-games not chased (adopter repos read-only from this lane) — recorded for the manager sweep. All other adopters read stale v1.17.0 < v1.18.0, as expected the minute a release cuts; their upgrade PRs are their own seats' work (KF-2).
- Decide-and-flag (S5 "release-notes line in the adopter upgrade checklist"): the published v1.18.0 notes already carry the full S1–S4 archive-ready payload entries; the checklist itself is a deliberately release-agnostic template in src/build_release_json.py (ADOPTER_CHECKLIST, "enforce, don't exhort" — appended to EVERY release), so a v1.18.0-specific feature line there would pollute all future notes. Declined the template edit; flagged here for veto. Follow-up candidate (not started): a generic checklist line pointing adopters at the release's "Added" section for newly planted verbs/templates.

## Routine state (carried from the 01:53Z heartbeat — this wake armed nothing, deleted nothing, sent nothing)
- This seat's ONLY trigger: `Self Improvement failsafe wake` trig_01AHRsGDBmbSDAc8AkjU2zJN · cron `0 */2 * * *` · ENABLED · bound to persistent session session_01TEnyj8QTuxfywgYwWP75Am (verified exhaustively at 2026-07-16T01:52Z; not re-probed this wake — no trigger writes occurred).
- ⚑ FOR OWNER REVIEW (carried forward): ORDER 024 says "do NOT re-arm routines yet; wait for the owner's per-seat go". The enabled failsafe above (created 2026-07-16T01:09Z) post-dates that order. Recorded neutrally for owner review/veto; not adjudicated here. Kit-lab daily loop re-arm recipe: docs/operations/lab-loop.md.

## State
- kit: v1.18.0
- Archive-ready close-out program COMPLETE: S1 (#412) + S2 (#413) + S3 (#414) + S4 (#416) + S5 (this release, v1.18.0) — doctrine + template + `archive-prep` verb + resolve-time residue guard + `check --strict` advisory, now distributed via the normal release channel; adopters inherit on their next `bootstrap.py upgrade`. Plan: docs/planning/2026-07-15-archive-ready-close-out-plan.md (all five slices shipped).
- Registry (docs/adopters.md): regenerated this wake at v1.18.0 (this PR); every adopter row reads stale until its own upgrade wave; kit's own DRIFT row is the known mid-close self-healing quirk — do not chase.
- Wake currency scan is turnkey (#392): `python3 dist/bootstrap.py currency --check` — exit 0 registry current / exit 1 regen slice due.
- Grounded-skills measurement: harness MERGED (#386, now also in the v1.18.0 CHANGELOG payload) — turnkey: `python3 scripts/measure_grounded_skills.py --clone --workdir <dir> --json <f> --out <f>`; protocol pre-registered at docs/operations/grounded-skills-measurement.md.
- Revival boot reading: CONSTITUTION.md → control/inbox.md → this file → docs/eap-closeout-walkthrough-2026-07-14.md §E → docs/audits/eap-project-audit-2026-07-14.md.

## Next-2 baton
1. KL-5 generalization of `probe_slot_residue` (idea already filed: probe_slot_residue KL-5 generalization) — deliberately NOT started this wake (release slice kept surgical); next buildable kit-internal improvement.
2. Grounded-skills measurement window ~2026-07-19..26 — run per docs/operations/grounded-skills-measurement.md, publish the findings report under docs/reports/.

## ⚑ FOR OWNER (standing set carried forward unchanged — NO new asks this wake)

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
