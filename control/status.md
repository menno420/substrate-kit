# Self Improvement seat — heartbeat
updated: 2026-07-14T01:59:21Z · worker session (coordinator-dispatched) · phase: post-EAP backlog build

## Routines
- Failsafe: "Self Improvement failsafe wake" trig_01LsHxvnYnpQ59n7iQTPNNF3 · 0 */2 * * * · bound live coordinator. Pacemaker chain live (~15 min).
- Business cron: kit-lab daily trig_01Jm57GAjNCFrYJn1oLMiYGE — KEEP · next 2026-07-14T06:08Z.

## This session
- Built the `check_idea_index` merged-reality leg (💡 ender from the #349 card, Night-12 triage #2, `docs/ideas/idea-index-merged-reality-2026-07-14.md`): shipped-idea frontmatter verified against local git history — shipped_pr merge marker on main, real-merge-date reconciliation, optional merged_sha ancestry. Advisory-first + 7-day grace window (no false reds on in-flight/parked shipping PRs); only malformed merged_sha syntax enforcing; self-skips on shallow/gitless trees (this session's own container clone WAS shallow, 51/441 commits — live proof of the degradation rule). PR #355 OPEN (born-red card, flips at close); suite 1410 → 1425; dist untouched, byte-stable (scripts/-side only). Landing: park-green, non-author review-merge.

## Open PRs
- PR #355 — this session (merged-reality leg). Landing: park-green, non-author review-merge.
- PR #317 — owner ratification park (do-not-automerge), green, payload byte-identical. Landing: owner-click. Gates the release wave.
- PR #345 — regen-lag checker, do-not-automerge until review. Landing: owner-click / non-author review-merge.
- PR #347 — external fleet-cleanup audit (read-only docs). Landing: review-merge.

## Recently merged
- PR #354 — kit-side scripts/preflight.py dogfood, merged 2026-07-14T01:33Z (87aeb4d). PR #353 — check_claims own-date fix (a67ccda). PR #352 — model-line payload lint (a9145ee). PR #351 — CHANGELOG structure checker (727f5db). PR #350 — heartbeat correction (8cf4597). PR #349 — seat-digest adaptive clip, merged 2026-07-14T00:04Z (ee3b962) by the enabler on green.

## Registry state
- Adopters tree-current at v1.15.0. adopters.md regen still waits on resident `kit:` lines (outbox ask).
kit: v1.15.0

## Next-2 baton
1. Owner clicks #317 → cut release wave (main now ~65 commits past v1.15.0) + adopter upgrade PRs.
2. Review-merge #355 + #345 + #347 · resident lanes' kit: lines → adopters.md regen · grounded-skills window ~07-19.

⚑ FOR OWNER (unchanged standing set — full paste-ready field blocks verbatim in git history of this file @ 86d2a57):
- P10 required-check swap (ruleset: require `kit-quality`, drop the two legacy contexts).
- fm #122 v3.4 restamp — owner reviews/merges PERSONALLY.
- UNIVERSAL wake fetch-list vN bump (+ docs/seat-digest.md, docs/SKILLS.md).
- ⚑ 6 public-flip-or-PAT (unblocks B2–B4 cross-repo sweeps).
- Grounded-skills measurement window ~2026-07-19..26 — silence accepts.

orders: acked=001–019 · done=001–019
