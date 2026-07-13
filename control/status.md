# Self Improvement seat — heartbeat
updated: 2026-07-13T13:47:34Z · coordinator session live (v3.6 boot 2026-07-13) · phase: ACTIVE

## Routines
- Failsafe: "Self Improvement failsafe wake" trig_01LsHxvnYnpQ59n7iQTPNNF3 · 0 */2 * * * · bound to live coordinator · verified via full paginated list_triggers audit 12:36Z.
- Pacemaker send_later chain live (~15 min). Old-seat failsafe trig_01EMfauRqevNovFM8dz4NLdp deleted at cutover (new verified first).
- Business cron: kit-lab daily trig_01Jm57GAjNCFrYJn1oLMiYGE — fresh-session-per-fire, KEEP · next 2026-07-14T06:08Z · not wedged.

## Shipped 2026-07-13 (this coordinator, all auto-merged on green; payload diffs verified)
- #325 docs/adopters.md regenerated (squash d916d94).
- #326 heartbeat landing, control fast lane (04ecd6e).
- #327 DRIFT-row classification + outbox ask to manager (dc75e0c): ZERO real upgrade work — fleet-manager and both superbot-games lanes are tree-current at v1.15.0 with stale/missing `kit:` self-report lines (fixes routed to resident lanes via outbox); kit-self v1.0.0 pin = owner-held (c).
- #328 heartbeat prefix now case-insensitive (76feb5d; grammar.py + dist regen, 1247 tests).

## Parked
- PR #317 — owner ratification park (do-not-automerge), green @ 82fca96. Landing path: owner-click. Never arm/close/rebase.

## Registry state
- All reachable adopters tree-current at v1.15.0 (verified against trees, PR #327 evidence). DRIFT rows clear at next adopters.md regen once resident lanes land their `kit:` lines.
kit: v1.15.0

## Next-2 baton
1. Owner sweeps #317 → cut release wave (main 38+ commits past v1.15.0) + adopter upgrade PRs.
2. After resident lanes land `kit:` lines → regenerate docs/adopters.md; grounded-skills measurement window ~2026-07-19..26.

⚑ FOR OWNER (paste-ready, carried from the standing set — full field blocks verbatim in git history of this file @ 86d2a57, ⚑ OWNER-ACTION 2/6 + ⚑ FOR MANAGER):
- **P10 required-check swap (⚑ 2):** Settings → Rules → `main` ruleset → required status checks: remove "Kit test suite" + "Cold-adoption smoke (adopt + check --strict)"; add `kit-quality`; set "Require branches to be up to date" OFF. Reversible; ends the ~35-min queue-stall class. (No agent path to rulesets — verified 403/no-endpoint.)
- **fm #122 v3.4 restamp:** the owner reviews and merges fleet-manager PR #122 PERSONALLY — do NOT agent-merge.
- **UNIVERSAL wake fetch-list vN bump + re-paste:** add `docs/seat-digest.md` (+ `docs/SKILLS.md`) to the manager-authored wake fetch list, bump vN, owner re-pastes via fm's edit-registry-first flow.
- **⚑ 6 public-flip-or-PAT (pick one):** make this repo public (⚠️ effectively irreversible) OR mint a fine-grained read-only PAT into the fleet environments (reversible) — unblocks the B2–B4 cross-repo sweeps.
- **Grounded-skills measurement window:** proposal to run the before/after measurement pass ~2026-07-19..26 per docs/reports/2026-07-12-grounded-skills-wrap.md §3d — say nothing to accept the window; a successor fires it when it matures.

orders: acked=001–017 · done=001–017
