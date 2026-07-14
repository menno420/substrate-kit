# Self Improvement seat — heartbeat
updated: 2026-07-14T19:0xZ · phase: post-EAP — v1.17.0 bump PR OPEN (#377, born-red by design until its card flips); ORDER 023 release half in flight; next = #377 lands on green → release.yml dispatch + verify + adopter regen wave

## Routines
- Failsafe: "Self Improvement failsafe wake" trig_01LsHxvnYnpQ59n7iQTPNNF3 · 0 */2 * * * · bound live coordinator. Pacemaker idles to failsafe post-consolidation (backlog dry).
- Business cron: kit-lab daily trig_01Jm57GAjNCFrYJn1oLMiYGE — KEEP.

## Facts
- v1.17.0 bump PR #377 OPEN (branch claude/release-v1.17.0): cut via scripts/cut_release.py 1.17.0 --write — KIT_VERSION + pyproject 1.16.0 → 1.17.0; [Unreleased] → [1.17.0] - 2026-07-14 (payload: branch-sweep workflow template, PR #376 merged as 0dc104b — sole user-visible change since v1.16.0); dist regen byte-stable ×2 (sha256 0d08b8aa9efc30178cf8e8befcfa28dd2b65e02106cc9ba6d520133017955521, 995446 bytes); pytest 1568 passed / 1 skipped; ruff clean; build_release_json --verify-only green; check --strict red only on the session card's designed born-red hold. Auto-merge NOT self-armed (enabler handles landing). Detail: .sessions/2026-07-14-release-v1.17.0.md.
- Heartbeat correction shipped in #377: the prior #376 line's "PR parks green for review-merge — auto-merge NOT armed by design" was falsified — #376 merged via the auto-merge enabler as 0dc104b.
- release v1.16.0 CUT + VERIFIED (2026-07-14): PR #370 merged as 93aa377; release.yml run 29342538960 SUCCESS; three-way sha256 PASS (bba34e2102cbaf09394f39992f0501ea5cfd542d90301ef67e31a0854ca59170, 980026 bytes). Full record: git history of this file @ 0dc104b.
- ORDER 023 state: BUILD half done (#376, merged 0dc104b); release half = this #377 bump; done-when completes at release.yml dispatch + adopter regen wave after #377 lands.

## Backlog state (honest)
Buildable backlog DRY (11/11 consumed or shipped, per the 2026-07-14 04:0xZ audit). Current work is the ORDER 023 release half (#377 in flight). Remaining after: release.yml dispatch on the bump merge SHA + scripts/verify_release.py three-way check + adopters regen + upgrade wave · resident kit: lines → adopters.md regen · grounded-skills window ~07-19. No filler beyond this line (Q-0089).

## Parked
- (none)

## Ratified/merged (2026-07-14 reconcile)
- PR #317 — RATIFIED + MERGED as 4f6e50c. PR #345 — RATIFIED + MERGED as c603cc9. PR #371 — MERGED as 39c6b20 (rode v1.16.0). PR #376 — MERGED as 0dc104b via the auto-merge enabler (ORDER 023 BUILD half).

## Registry state
- adopters.md last regenerated post-v1.16.0: all 9 adopter rows stale vs v1.16.0 (upgrade wave pending; v1.17.0 wave supersedes it once #377 lands + publishes). Kit self-row DRIFT = known mid-close artifact, self-heals next regen.
kit: v1.16.0 (v1.17.0 pending #377 merge + release.yml publish)

## Next-2 baton
1. #377 lands on green (enabler) → dispatch release.yml (version=1.17.0, on main at the bump merge SHA) → scripts/verify_release.py 1.17.0 → release record + claim delete (control/claims/claude-release-v1.17.0.md).
2. v1.17.0 adopter upgrade wave (upgrade each adopter, merged on green, then registry regen) — closes ORDER 022/023 done-when.

⚑ FOR OWNER (unchanged standing set — full paste-ready field blocks verbatim in git history of this file @ 86d2a57):
- P10 required-check swap (ruleset: require `kit-quality`, drop the two legacy contexts).
- fm #122 v3.4 restamp — owner reviews/merges PERSONALLY.
- UNIVERSAL wake fetch-list vN bump (+ docs/seat-digest.md, docs/SKILLS.md).
- ⚑ 6 public-flip-or-PAT (unblocks B2–B4 cross-repo sweeps).
- Grounded-skills measurement window ~2026-07-19..26 — silence accepts.

orders: acked=001–023 · done=001–022 (023 BUILD half done #376 merged 0dc104b; release half in flight as PR #377; done-when completes at the v1.17.0 publish + regen wave)
