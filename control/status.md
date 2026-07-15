# Self Improvement seat — heartbeat
updated: 2026-07-15T04:40Z · phase: EAP EXTENSION ACTIVE (ORDER 024 acked + done on the seat's first rebooted wake; EAP through 2026-07-21; routines coordinator-managed this wake)

## This wake (2026-07-15, PR #382 · claude/adopters-currency-2026-07-15)
- ORDER 024 acknowledged on the first rebooted wake — its done-when. No routines re-armed; wake channel stays owner/coordinator until the owner's per-seat v3.6 reboot go.
- docs/adopters.md regenerated via `python3 dist/bootstrap.py currency` (04:37:23Z scan, 12 repos, read-only): DRIFT 7 repos → 5 — idea-engine + trading-strategy cleared, venture-lab now self-reports v1.17.0, superbot-next self-report advanced to v1.16.0. Remaining DRIFT = the chronic lane-owed heartbeat `kit:`-lag class (superbot-next, websites, superbot-games ×3 lanes, superbot-mineverse) + kit's own known tree-internal config-pin v1.0.0 row.
- Boot verify: preflight 7/7 legs green at origin/main 58b3f80 (pytest 1568 passed, 1 skipped).
- Landing path: PR #382 flips green at the card flip; auto-merge-enabler lands it on kit-quality green. No other open PRs; nothing parked.
- Friction note (no new ask): first push collided with the SPENT surviving branch `claude/adopters-currency-refresh` (its PR merged 2026-07-13; ref never auto-deleted — the ORDER 022/023 litter class). Resolved by taking a dated branch name; no force-push. branch-sweep.yml remains staged-only fleet-wide (`.substrate/ci/`); per-repo wiring is lane/owner-owed via `adopt --wire-enforcement`.

## Routine state
- routines coordinator-managed this wake. ALL seat routines remain DOWN per ORDER 024 (verified-down record: git history of this file @ 58b3f80; kit-lab daily loop re-arm recipe: docs/operations/lab-loop.md).

## State
- kit: v1.17.0
- v1.17.0 distributed 9/9 engaged adopters (registry re-verified this wake at live HEAD).
- Revival boot reading: CONSTITUTION.md → control/inbox.md → this file → docs/eap-closeout-walkthrough-2026-07-14.md §E → docs/audits/eap-project-audit-2026-07-14.md.

## Next-2 baton
1. Grounded-skills measurement window ~2026-07-19..26 — run the measurement per the proposal precedent (PR #247 methodology) when the window opens; owner silence accepts.
2. After adopter lanes bump their heartbeat `kit:` lines (and/or branch-sweep gets wired per-repo via `adopt --wire-enforcement` — owner/resident), re-run `python3 dist/bootstrap.py currency` to retire the remaining DRIFT rows.

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
