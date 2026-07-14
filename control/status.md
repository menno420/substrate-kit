# Self Improvement seat — heartbeat
updated: 2026-07-14T03:50:00Z · worker session (coordinator-dispatched) · phase: post-EAP backlog build

## Routines
- Failsafe: "Self Improvement failsafe wake" trig_01LsHxvnYnpQ59n7iQTPNNF3 · 0 */2 * * * · bound live coordinator. Pacemaker chain live (~15 min).
- Business cron: kit-lab daily trig_01Jm57GAjNCFrYJn1oLMiYGE — KEEP · next 2026-07-14T06:08Z.

## This session
- Shipped `bootstrap claim` — mechanical grammar-valid work-claim writer/deleter (the #358 card's 💡 ender): `src/engine/claim.py` + CLI verb (write-by-default + `--dry-run`, `--delete` refuses foreign claims), renders from and round-trips through the SAME grammar constants check_claims consumes; claims README (template + planted) now teaches the verb; ride-alongs: FOLLOWUP_CHECKLIST ↔ release-runbook keyword drift pin, this heartbeat's #358 merged-restamp. Dogfooded on this session's own claim (verb-deleted, verb-recreated, zero findings). Suite 1476 → 1495 (+19); preflight 7 legs green; dist regenerated, byte-stable. PR #359 parked for review-merge (auto-merge not armed by this session; the enabler may arm claude/* PRs at open by design).

## Previous session
- Extracted the shared git-truth helper (#357 card's 💡 ender): `scripts/_git_truth.py` (is_shallow / provable_ancestry → yes|no|unprovable) now owns the shallow/graft ancestry degradation rule; check_idea_index + verify_release refit behavior-preserving; CAPABILITIES.md wall+recipe appended. Suite 1463 → 1476 (+13); preflight 7 legs green; src/engine + dist untouched in that PR.

## Open PRs
- PR #359 — this session (`bootstrap claim` verb + drift pin). Landing: green on the card flip; enabler-armed auto-merge is the sanctioned path if it fires.
- PR #317 — owner ratification park (do-not-automerge), green, payload byte-identical. Landing: owner-click. Gates the release wave.
- PR #345 — regen-lag checker, do-not-automerge until review. Landing: owner-click / non-author review-merge.
- PR #347 — external fleet-cleanup audit (read-only docs). Landing: review-merge.

## Recently merged
- PR #358 — shared git-truth helper: MERGED 2026-07-14T03:18Z (squash e564b2d).
- PR #357 — verify_release mechanization: MERGED 2026-07-14T02:58Z (squash 0d0aac4).
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
