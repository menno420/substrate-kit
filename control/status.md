# Self Improvement seat — heartbeat
updated: 2026-07-16T03:17:07Z · phase: EAP EXTENSION ACTIVE (EAP through 2026-07-21; inbox consumed 001–024; worker-slice wake 2026-07-16T03:08Z)

## This wake (2026-07-16 03:08Z worker session) — STATUS-BADGE VALUE-PARSE FIX

- Wake source: coordinator-dispatched worker slice (bugs-first); hard-sync landed on 0bda967 (#421 merge); no ORDER >024 at inbox HEAD; slice = the #420 card's filed 💡 bug — the status-badge substring false-hold.
- Open PR: **#422** (`claude/status-badge-value-parse`, auto-merge armed SQUASH at 2026-07-16T03:08:51Z via `enable_pr_auto_merge`). What it lands: `status_in_progress` (the MERGE-BLOCKING session gate's card-status detection) stops substring-matching hold tokens across the badge LINE — the auto-draft parenthetical "*(auto-drafted by substrate-kit …)*" contains "drafted", so a card whose Status VALUE reads `complete` was false-held red. Root fix by value-parsing: shared `_status_badge_value` (backticked span preferred — the `_STATUS_VALUE_RE` mechanism `_status_value_drafted` already used, now reused by it — bare line-remainder fallback keeps the `> **Status:** in progress` grammar working) + `_value_declares` (token must match the VALUE at its start on a word boundary: `` `hold` — waiting`` holds, `holding` and prose mentions never do). Regression tests pin the auto-drafted pair (same prose: `in-progress` HOLDS, `complete` RELEASES) end-to-end through the added-card lane.
- Sweep (in the PR body): old vs new parser over all 238 existing `.sessions/*.md` cards — **0 flips** (1 HOLD agree = this PR's own born-red card; 237 RELEASE agree).
- Verified at f592411: `scripts/preflight.py` 9/9 PASS (pytest `1705 passed, 1 skipped` — was 1702, +3 new); dist regen byte-pin green (1089816 bytes); `dist/bootstrap.py check --strict` shows only the designed born-red HOLD (own card, pre-flip — the NEW parser producing the designed hold), the known staged-regen-lag ×3, and the required-unverified NOTE.
- Merged this calendar day (earlier wakes): #412 S1 · #413 S2 · #414 S3 · #415 claim prune · #416 S4 · #417 claim prune · #418 v1.18.0 bump · #419 close-out · #420 KL-5 residue generalization · #421 claim prune. Release v1.18.0 out (run 29466068874, sha256 three-way PASS — full record in this file's history @ 13a0b44).
- Slice 2 (conditional, this session, only if #422 reaches terminal cleanly): uncovered residue surfaces — S2 evidence-judgment hints + adopt-planted doc `[[fill:]]` slots — as a SEPARATE PR with its own card + claim; gate-lane graduation of check_card_residue stays PARKED.

## Routine / denial state (carried)
- This seat's ONLY trigger: `Self Improvement failsafe wake` trig_01AHRsGDBmbSDAc8AkjU2zJN · cron `0 */2 * * *` · ENABLED · bound to persistent session session_01TEnyj8QTuxfywgYwWP75Am (verified exhaustively 2026-07-16T01:52Z; no trigger writes this wake).
- ⚑ FOR OWNER REVIEW (carried forward): ORDER 024 says "do NOT re-arm routines yet; wait for the owner's per-seat go". The enabled failsafe above (created 2026-07-16T01:09Z) post-dates that order. Recorded neutrally for owner review/veto; not adjudicated here. Kit-lab daily loop re-arm recipe: docs/operations/lab-loop.md.
- **DENIAL RECORD (2026-07-16): v1.18.0 adopter-upgrade wave PARKED.** A proposed adopter-wave dispatch was permission-denied by the seat session's classifier — verbatim: "[External System Writes] …clone, branch, commit, push, and open PRs against ~15 separate adopter repositories… no genuine user message anywhere in the transcript authorizing writes outside the single-repo mandate." Routed per denial-routing doctrine (⚑ ask below); do NOT retry that dispatch shape without owner provenance — coordinator relay alone is not authorization. Adopter repos are read-only from this lane until the owner speaks.

## State
- kit: v1.18.0
- Status-badge value-parse fix IN FLIGHT (#422, auto-merge armed): the session gate judges the badge VALUE, not line prose — a latent false-hold class on the merge-blocking gate closed at root. KL-5 residue generalization MERGED (#420).
- Registry (docs/adopters.md): regenerated at v1.18.0 (#419); every adopter row reads stale until its own upgrade wave (parked — see denial record + ⚑ ask).
- Wake currency scan turnkey (#392): `python3 dist/bootstrap.py currency --check`.
- Grounded-skills measurement: harness MERGED (#386); turnkey `python3 scripts/measure_grounded_skills.py --clone --workdir <dir> --json <f> --out <f>`; protocol pre-registered at docs/operations/grounded-skills-measurement.md.
- Revival boot reading: CONSTITUTION.md → control/inbox.md → this file → docs/eap-closeout-walkthrough-2026-07-14.md §E → docs/audits/eap-project-audit-2026-07-14.md.

## Next-2 baton
1. Grounded-skills measurement window ~2026-07-19..26 — run per docs/operations/grounded-skills-measurement.md, publish the findings report under docs/reports/.
2. KL-5 residue follow-through: (a) graduate `session-card-slot-residue` into the merge-blocking gate lanes once the advisory proves quiet on genuine cards across a few sessions (PL-008 graduation); (b) remaining uncovered drafted-fill surfaces — the archive note's S2 *evidence-judgment* hints (claims disposition / ⚑ verify / payload park — only the two doctrine-guarded slots are fingerprinted today) and adopt-planted doc `[[fill:]]` slots (partially covered by check_staged_regen — dedupe, don't double-report). (Slice 2 of the 2026-07-16 03:08Z wake may consume (b) — check open PRs before starting.)

## ⚑ FOR OWNER (standing set carried forward — no new ask this wake)

⚑ v1.18.0 adopter-wave authorization — WHAT: authorize the v1.18.0 adopter-upgrade wave. WHERE: any seat session, one live owner turn. HOW: say 'run the v1.18.0 adopter wave'. WHY: the seat session's permission classifier denied adopter-repo writes dispatched on coordinator relay alone — verbatim: '[External System Writes] …clone, branch, commit, push, and open PRs against ~15 separate adopter repositories… no genuine user message anywhere in the transcript authorizing writes outside the single-repo mandate.' UNBLOCKS: ~15 adopter currency PRs to v1.18.0. VERIFY: wave report with per-adopter PR list. RISK: ↩️ reversible, distribution-only diffs.

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
