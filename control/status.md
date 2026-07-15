# Self Improvement seat — heartbeat
updated: 2026-07-15T05:10Z · phase: EAP EXTENSION ACTIVE (EAP through 2026-07-21; inbox consumed 001–024; routines coordinator-managed)

## This wake (2026-07-15, PR #383 · claude/idea-index-shipped-drift-2026-07-15)
- Idea-index shipped-drift fix (docs-only): a full frontmatter⇄README cross-check at main e900008 found 7 shipped ideas (#187 ×2, #342, #344, #346, #349, #351) still listed as buildable `state: captured` Backlog entries with `next:` build instructions — the dispatch-misdirection class from PR #311's provenance; entries moved to § Shipped with merge citations. Plus one un-flipped ship record: staged-artifact-regen-lag-checker frontmatter still `captured/open` while its PR #345 merged on main (c603cc9, 2026-07-14) — flipped per the idea-index outcome rules.
- Coverage note: README section placement is outside `check_idea_index`'s legs (leg 4 checks link resolution, leg 5 body-state, leg 6 merged-reality — skipped on shallow clones), so this drift sat checker-green; candidate future leg noted in the session card idea.
- Boot verify: preflight 7/7 legs green at origin/main e900008 (pytest 1568 passed, 1 skipped); re-run green on the fix.
- Landing path: PR #383 flips green at the card flip; auto-merge-enabler lands it on kit-quality green. No other open PRs; nothing parked.

## Routine state (observed facts — read-only list_triggers inventory this session, 2026-07-15 ~04:4xZ)
- This session armed no triggers. Routines are coordinator-managed this wake.
- Observed in the registry: "Self Improvement failsafe wake" trig_01CUfSZo9Uky9DdpoqpZPcfT — cron `0 */2 * * *`, enabled=true, created 2026-07-15T04:38:07Z via meta_mcp, bound to a coordinator session (persistent_session_id session_01SFVAo5bPD41RMx9TzGxnPY), next fire 06:04Z — plus one pending one-shot pacemaker (run_once_at 2026-07-15T04:55:00Z, same session binding). Not created by this session.
- ⚑ FOR OWNER REVIEW: ORDER 024 (control/inbox.md @ 58b3f80) states "do NOT re-arm routines yet; wait for the owner's per-seat go (the v3.6 reboot prompt IS that go)". The observed failsafe above post-dates that order. This heartbeat records the discrepancy neutrally for the owner's review/veto; it does not adjudicate it. Prior heartbeat (git history @ 58b3f80) had recorded all seat routines verified DOWN; kit-lab daily loop re-arm recipe remains docs/operations/lab-loop.md.

## State
- kit: v1.17.0
- v1.17.0 distributed 9/9 engaged adopters (registry re-verified this wake at live HEAD).
- Revival boot reading: CONSTITUTION.md → control/inbox.md → this file → docs/eap-closeout-walkthrough-2026-07-14.md §E → docs/audits/eap-project-audit-2026-07-14.md.

## Next-2 baton
1. After adopter lanes bump their heartbeat `kit:` lines (and/or branch-sweep gets wired per-repo via `adopt --wire-enforcement` — owner/resident), re-run `python3 dist/bootstrap.py currency` to retire the remaining DRIFT rows (5 at the 04:37Z scan).
2. Grounded-skills measurement window ~2026-07-19..26 — run the measurement per the proposal precedent (PR #247 methodology) when the window opens; owner silence accepts.

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
