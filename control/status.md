# Self Improvement seat — heartbeat
updated: 2026-07-14T14:29Z · phase: post-EAP — ORDER 022 shipped; release wave still gated on owner #317 click

## Routines
- Failsafe: "Self Improvement failsafe wake" trig_01LsHxvnYnpQ59n7iQTPNNF3 · 0 */2 * * * · bound live coordinator. Pacemaker idles to failsafe post-consolidation (backlog dry).
- Business cron: kit-lab daily trig_01Jm57GAjNCFrYJn1oLMiYGE — KEEP.

## Facts
done=022 facts: PR #371 — stop-hook merged-head final-push guard: guard merged to main; release + adopter regen ride v1.16.0 (in flight). `_stop_push_guard` (sixth `evaluate_stop` advisory): fetch → provable ancestry vs origin/main via the new dist-shipped `engine/lib/git_truth.py` (port of scripts/_git_truth.py, parity-pinned) → merged=loud SKIP line · unmerged=silent · unprovable=NOTE + push proceeds (fail-open). Suite 1550→1559 passed (1 skipped unchanged); preflight 7/7; dist byte-stable ×2; three decision points mutation-tested. Details: .sessions/2026-07-14-order-022-push-guard.md.
done=021 facts: PR #368 — EAP closeout walkthrough at docs/eap-closeout-walkthrough-2026-07-14.md (sections A–E; OWNER ACTIONS leads with the #317 click). #345 "green" retracted with evidence; #317/#345 park states verified live. Full detail: git history of this file @ 4f6e50c.
done=020 facts: PR #362 — ORDER 020 items d+e; (a)–(c) satisfied per thread premise-check. Detail in git history @ 4f6e50c.

## Parked (unchanged this session — see git history @ 4f6e50c for full landing notes)
- PR #317 — owner ratification park (do-not-automerge), head df7b324, mergeable_state=dirty vs moved main; landing: freshen → owner-click. Gates the release wave.
- PR #345 — regen-lag checker, do-not-automerge; no CI on final head a5d86a3 (conflicted-at-push class); landing: freshen → non-author review-merge.

## Registry state
- All adopters tree-current at v1.15.0. adopters.md regen waits on resident kit: lines.
kit: v1.15.0

## Next-2 baton
1. Owner clicks #317 → scripts/cut_release.py → v1.16.0 release wave (carries the ORDER 022 guard + #332 convergence + the checker/verb band) + adopter upgrade PRs → scripts/verify_release.py.
2. #345 review-merge · resident kit: lines → adopters regen · grounded-skills window ~07-19.

⚑ FOR OWNER (unchanged standing set — full paste-ready field blocks verbatim in git history of this file @ 86d2a57):
- P10 required-check swap (ruleset: require `kit-quality`, drop the two legacy contexts).
- fm #122 v3.4 restamp — owner reviews/merges PERSONALLY.
- UNIVERSAL wake fetch-list vN bump (+ docs/seat-digest.md, docs/SKILLS.md).
- ⚑ 6 public-flip-or-PAT (unblocks B2–B4 cross-repo sweeps).
- Grounded-skills measurement window ~2026-07-19..26 — silence accepts.

orders: acked=001–022 · done=001–022
