# Self Improvement seat — heartbeat
updated: 2026-07-14T03:55:00Z · worker session (coordinator-dispatched) · phase: post-EAP backlog build

## Routines
- Failsafe: "Self Improvement failsafe wake" trig_01LsHxvnYnpQ59n7iQTPNNF3 · 0 */2 * * * · bound live coordinator. Pacemaker chain live (~15 min).
- Business cron: kit-lab daily trig_01Jm57GAjNCFrYJn1oLMiYGE — KEEP · next 2026-07-14T06:08Z.

## This session
- Built the verify_release mechanization (💡 ender from the #356 Night-14 card, completing the cut_release pair): `scripts/verify_release.py <version>` — runbook §5's post-release verification as one read-only command: tag→bump-commit leg (shallow-aware ancestry — a grafted clone's negative answer SKIPs, never false-FAILs; live-hit on this container's own clone vs v1.15.0), three-way sha256 leg (release.json field == downloaded asset == committed dist at the tag commit, github.com download path only), release.yml-run leg (SKIPs with the verbatim api.github.com 403 here); exit 1 iff any FAIL, all-skip exits 0 + NOTHING-WAS-VERIFIED warning; paste-ready record line. Live golden vs real v1.15.0: 2 PASS · 0 FAIL · 1 SKIPPED, hash 25d22af9…650e three-way agreed. PR #357 OPEN (born-red card, flips at close; landing mode: enabler arms on the flip push, merges on green). Suite 1444 → 1463 (+19 run, +20 tests incl. one env-gated live); `src/engine/` untouched, no dist regen; preflight 7 legs green.

## Open PRs
- PR #357 — this session (verify_release mechanization). Landing: enabler merge on green after the card flip.
- PR #317 — owner ratification park (do-not-automerge), green, payload byte-identical. Landing: owner-click. Gates the release wave.
- PR #345 — regen-lag checker, do-not-automerge until review. Landing: owner-click / non-author review-merge.
- PR #347 — external fleet-cleanup audit (read-only docs). Landing: review-merge.

## Recently merged
- PR #356 — cut_release mechanization: MERGED 2026-07-14T02:33Z (squash 6b9cdd4), enabler on green after the card flip.
- PR #355 — merged-reality leg: MERGED 2026-07-14T02:02:13Z by github-actions[bot]. Squash bf231c3.
- PR #354 — kit-side scripts/preflight.py dogfood, merged 2026-07-14T01:33Z (87aeb4d). PR #353 — check_claims own-date fix (a67ccda). PR #352 — model-line payload lint (a9145ee). PR #351 — CHANGELOG structure checker (727f5db). PR #350 — heartbeat correction (8cf4597).

## Registry state
- Adopters tree-current at v1.15.0. adopters.md regen still waits on resident `kit:` lines (outbox ask).
kit: v1.15.0

## Next-2 baton
1. Owner clicks #317 → cut release wave (main now ~70 commits past v1.15.0; `scripts/cut_release.py` mechanizes the bump prep, `scripts/verify_release.py` the §5 post-verification) + adopter upgrade PRs.
2. Review-merge #345 + #347 · resident lanes' kit: lines → adopters.md regen · grounded-skills window ~07-19.

⚑ FOR OWNER (unchanged standing set — full paste-ready field blocks verbatim in git history of this file @ 86d2a57):
- P10 required-check swap (ruleset: require `kit-quality`, drop the two legacy contexts).
- fm #122 v3.4 restamp — owner reviews/merges PERSONALLY.
- UNIVERSAL wake fetch-list vN bump (+ docs/seat-digest.md, docs/SKILLS.md).
- ⚑ 6 public-flip-or-PAT (unblocks B2–B4 cross-repo sweeps).
- Grounded-skills measurement window ~2026-07-19..26 — silence accepts.

orders: acked=001–019 · done=001–019
