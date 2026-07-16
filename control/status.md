# Self Improvement seat — heartbeat
updated: 2026-07-16T01:17Z · phase: EAP EXTENSION ACTIVE (EAP through 2026-07-21; inbox consumed 001–024; worker-slice wake 2026-07-16T01:05Z)

## This wake (2026-07-16 01:05Z worker session)
- Wake source: coordinator-dispatched worker slice; hard-sync landed on efec845 (#413 merge); no ORDER >024 at HEAD; zero open PRs at orient; preflight 9/9 green at boot.
- Shipped: baton item 1 — archive-ready close-out slice S3 (REQUIRES-PROBE resolve-time semantics) per docs/planning/2026-07-15-archive-ready-close-out-plan.md §5. PR #414 (claude/archive-probe-s3): `probe_slot_residue` in src/engine/loop/archive.py fingerprints the guarded slot bodies from the shipped template (whitespace-normalized 8-word shingles, re-wrap-proof); `archive-prep` reports a zero-slot note carrying marker-stripped templated default text as NOT complete — touched by nobody, never silently superseded by a fresh draft; a genuine wholesale replacement (template preamble kept) still reads complete. +7 tests incl. a dist-built-artifact drive of the sham path; dist regenerated; doctrine doc + CHANGELOG updated.
- Verified at e423880: scripts/preflight.py 9/9 green (pytest "1671 passed, 1 skipped in 37.90s"); dist/bootstrap.py check --strict shows only the designed born-red HOLD (this session's card, pre-flip), the known staged-regen-lag ×3, and the required-unverified NOTE. A claims-format advisory fired on this session's own claim (timestamp-with-time rejected) — fixed to plain YYYY-MM-DD in the same session.
- Wall hit (verbatim, twice): `enable_pr_auto_merge` on #414 → "Failed to look up pull request menno420/substrate-kit#414: API rate limit already exceeded for user ID 225413533." Working alternative taken: the repo's auto-merge-enabler workflow re-arms on `pull_request: synchronize`, and this session's post-open pushes (work commit, heartbeat, card flip) fire it — arming lands via the backstop; verify on the PR after flip.

## Routine state (observed facts)
- FAILSAFE "Self Improvement failsafe wake" trig_01CUfSZo9Uky9DdpoqpZPcfT (cron `0 */2 * * *`) remains ARMED as left by the 07-15 ender; this wake armed nothing, deleted nothing, sent nothing (trigger/send_later prohibited for this worker session by standing rules).
- ⚑ FOR OWNER REVIEW (carried forward): ORDER 024 (control/inbox.md @ 58b3f80) says "do NOT re-arm routines yet; wait for the owner's per-seat go". The armed failsafe above post-dates that order. Recorded neutrally for owner review/veto; not adjudicated here. Kit-lab daily loop re-arm recipe: docs/operations/lab-loop.md.

## State
- kit: v1.17.0
- Archive-ready close-out surface: S1 (#412) + S2 (#413) + S3 (PR #414, open at write time — lands on green via enabler backstop) — doctrine (docs/operations/archive-ready-close-out.md) + template (src/engine/templates/archive-ready.md.tmpl) + `archive-prep` verb + resolve-time residue guard (src/engine/loop/archive.py::probe_slot_residue, the seam S4 reuses). Plan: docs/planning/2026-07-15-archive-ready-close-out-plan.md; next increment S4 (`check --strict` advisory + PL-008 header + one red fixture), then S5 (release-wave distribution).
- Registry (docs/adopters.md): `currency --check` was exit 0 at the predecessor wake (00:39Z); not re-probed this wake (no adopter-facing change shipped). Run the probe FROM THE REPO ROOT; a mid-scan `Connection reset by peer` is a network blip — retry once.
- Wake currency scan is turnkey (#392): `python3 dist/bootstrap.py currency --check` — exit 0 registry current / exit 1 regen slice due.
- Grounded-skills measurement: harness MERGED (#386) — turnkey: `python3 scripts/measure_grounded_skills.py --clone --workdir <dir> --json <f> --out <f>`; protocol pre-registered at docs/operations/grounded-skills-measurement.md.
- Revival boot reading: CONSTITUTION.md → control/inbox.md → this file → docs/eap-closeout-walkthrough-2026-07-14.md §E → docs/audits/eap-project-audit-2026-07-14.md.

## Next-2 baton
1. Archive-ready close-out slice S4 — `check --strict` advisory when an archive-ready draft has unresolved `[[fill:]]` slots OR guarded-slot residue (reuse `probe_slot_residue`, src/engine/loop/archive.py); PL-008 unverified header; one deliberate red fixture. Plan: docs/planning/2026-07-15-archive-ready-close-out-plan.md §5 S4. Graduation to a preflight leg stays a later, separate decision.
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
