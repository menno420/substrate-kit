# Self Improvement seat — heartbeat
updated: 2026-07-14T00:19:52Z · worker session (coordinator-dispatched) · phase: post-EAP backlog build

## Routines
- Failsafe: "Self Improvement failsafe wake" trig_01LsHxvnYnpQ59n7iQTPNNF3 · 0 */2 * * * · bound live coordinator. Pacemaker chain live (~15 min).
- Business cron: kit-lab daily trig_01Jm57GAjNCFrYJn1oLMiYGE — KEEP · next 2026-07-14T06:08Z.

## This session
- Built the CHANGELOG `[Unreleased]` structure checker (next-ranked backlog idea, `docs/ideas/changelog-unreleased-structure-checker-2026-07-09.md`): `scripts/check_changelog_structure.py` + 22 tests + ci.yml kit-quality step — kit-repo-only scoping, no adopter surface. PR #351 OPEN (born-red card flipped complete at close); suite 1344 → 1366; dist untouched, byte-stable. Landing: review-merge by a different session (server enabler may arm on green as with #349).

## Open PRs
- PR #354 — kit-side scripts/preflight.py dogfood (worker session 2026-07-14): the config-default preflight wrapper planted (7 ci.yml kit-quality legs, worst-exit, SUBSTRATE_KIT_PREFLIGHT self-skip) — standing check NOTE retired; suite 1394 → 1410; dist untouched, byte-stable. Landing: parked green, non-author review-merge / enabler-on-green.
- PR #353 — check_claims own-date fix (worker session 2026-07-14): false claims-stale from dated filenames in claim scope text fixed (claim date = last date on the bullet line, the #352 card's guard recipe); suite 1391 → 1394; dist byte-stable. Landing: non-author review-merge / enabler-on-green.
- PR #352 — model-line payload lint (advisory; worker session 2026-07-14): backlog idea `model-line-payload-lint-advisory-2026-07-11` built; suite 1366 → 1391; drift measured 124/178 completed cards, shipping newest-10 window 10/10. Landing: parked green, non-author review-merge / enabler-on-green.
- PR #351 — this session (changelog structure checker). Landing: non-author review-merge / enabler-on-green.
- PR #317 — owner ratification park (do-not-automerge), green, payload byte-identical. Landing: owner-click. Gates the release wave.
- PR #345 — regen-lag checker, green-pending, do-not-automerge until review. Landing: owner-click / non-author review-merge.
- PR #347 — external fleet-cleanup audit (read-only docs). Landing: review-merge.

## Recently merged
- PR #349 — seat-digest adaptive clip, merged 2026-07-14T00:04Z (ee3b962) by the enabler on green. ORDER 019 fully done before it (see git history of this file @ 8cf4597 for the full night tally).

## Registry state
- Adopters tree-current at v1.15.0. adopters.md regen still waits on resident `kit:` lines (outbox ask).
kit: v1.15.0

## Next-2 baton
1. Owner clicks #317 → cut release wave (main now ~60 commits past v1.15.0) + adopter upgrade PRs.
2. Review-merge #351 + #345 · resident lanes' kit: lines → adopters.md regen · grounded-skills window ~07-19.

⚑ FOR OWNER (unchanged standing set — full paste-ready field blocks verbatim in git history of this file @ 86d2a57):
- P10 required-check swap (ruleset: require `kit-quality`, drop the two legacy contexts).
- fm #122 v3.4 restamp — owner reviews/merges PERSONALLY.
- UNIVERSAL wake fetch-list vN bump (+ docs/seat-digest.md, docs/SKILLS.md).
- ⚑ 6 public-flip-or-PAT (unblocks B2–B4 cross-repo sweeps).
- Grounded-skills measurement window ~2026-07-19..26 — silence accepts.

orders: acked=001–019 · done=001–019
