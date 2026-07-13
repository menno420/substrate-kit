# Self Improvement seat — heartbeat
updated: 2026-07-13T14:41Z · coordinator session live (v3.6 boot 2026-07-13) · phase: ACTIVE

## Routines
- Failsafe: "Self Improvement failsafe wake" trig_01LsHxvnYnpQ59n7iQTPNNF3 · 0 */2 * * * · bound to live coordinator (verified fired 14:05Z, chain confirmed).
- Pacemaker send_later chain live (~15 min). Old-seat failsafe trig_01EMfauRqevNovFM8dz4NLdp deleted at cutover.
- Business cron: kit-lab daily trig_01Jm57GAjNCFrYJn1oLMiYGE — fresh-session-per-fire, KEEP · next 2026-07-14T06:08Z.

## ORDER 018 — done
done=018 · PR #332 merged-on-green (all 4 checks green at e7737e0) · check --strict now runs both CI legs locally: inbox merge-base derived from origin/main (§3.2 carve-out in cli.py only) + config preflight_scripts (default scripts/preflight.py) · 1265 tests · dist byte-stable 7ce45889. Note: idea-engine's CI check_ideas step is a hand-added host customization — becomes a harmless duplicate after its next kit upgrade.

## Shipped 2026-07-13 (this coordinator; all auto-merged on green, payloads verified)
- #325 adopters.md regen (d916d94) · #326 heartbeat landing (04ecd6e) · #327 DRIFT classify + outbox ask (dc75e0c) · #328 heartbeat prefix case-insensitive (76feb5d) · #330 heartbeat refresh (243dd57) · #331 guard-fires announce line + telemetry doctrine (f873eef) · #332 ORDER 018 (e7737e0).
- Verified read-only: "no template ships a dead boot pointer" TRUE at 481f682 (cold-adopt existence check + 2 adopter trees); enforcement gap found → guard in flight.

## In flight
- claude/template-pointer-guard — enforcing template↔ADOPT_PLAN pointer coherence test (⚑ self-initiated, dispatched 14:34Z).

## Parked
- PR #317 — owner ratification park (do-not-automerge), green @ 82fca96. Landing path: owner-click. Never arm/close/rebase.

## Registry state
- All reachable adopters tree-current at v1.15.0 (PR #327 evidence). DRIFT rows = self-report lag; resident-lane `kit:` line fixes requested via outbox 2026-07-13; rows clear at next adopters.md regen.
kit: v1.15.0

## Next-2 baton
1. Owner sweeps #317 → cut release wave (main 40+ commits past v1.15.0) + adopter upgrade PRs.
2. After resident lanes land `kit:` lines → regenerate docs/adopters.md; grounded-skills measurement window ~2026-07-19..26.

⚑ FOR OWNER (paste-ready, carried from the standing set — full field blocks verbatim in git history of this file @ 86d2a57, ⚑ OWNER-ACTION 2/6 + ⚑ FOR MANAGER):
- **P10 required-check swap (⚑ 2):** Settings → Rules → `main` ruleset → required status checks: remove "Kit test suite" + "Cold-adoption smoke (adopt + check --strict)"; add `kit-quality`; set "Require branches to be up to date" OFF. Reversible; ends the ~35-min queue-stall class. (No agent path to rulesets — verified 403/no-endpoint.)
- **fm #122 v3.4 restamp:** the owner reviews and merges fleet-manager PR #122 PERSONALLY — do NOT agent-merge.
- **UNIVERSAL wake fetch-list vN bump + re-paste:** add `docs/seat-digest.md` (+ `docs/SKILLS.md`) to the manager-authored wake fetch list, bump vN, owner re-pastes via fm's edit-registry-first flow.
- **⚑ 6 public-flip-or-PAT (pick one):** make this repo public (⚠️ effectively irreversible) OR mint a fine-grained read-only PAT into the fleet environments (reversible) — unblocks the B2–B4 cross-repo sweeps.
- **Grounded-skills measurement window:** proposal to run the before/after measurement pass ~2026-07-19..26 per docs/reports/2026-07-12-grounded-skills-wrap.md §3d — say nothing to accept the window; a successor fires it when it matures.

orders: acked=001–018 · done=001–018
