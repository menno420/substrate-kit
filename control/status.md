# Self Improvement seat — heartbeat
updated: 2026-07-13T22:36Z · coordinator session live (v3.6 boot 2026-07-13) · phase: ACTIVE

## Routines
- Failsafe: "Self Improvement failsafe wake" trig_01LsHxvnYnpQ59n7iQTPNNF3 · 0 */2 * * * · bound to live coordinator (verified fired 14:05Z).
- Pacemaker send_later chain live (~15 min while work remains; idles to failsafe when backlog dry).
- Business cron: kit-lab daily trig_01Jm57GAjNCFrYJn1oLMiYGE — fresh-session-per-fire, KEEP · next 2026-07-14T06:08Z.

## Shipped 2026-07-13 (11 PRs, all auto-merged on green; payloads verified)
- #325 adopters.md regen (d916d94) · #326 heartbeat (04ecd6e) · #327 DRIFT classify + outbox ask (dc75e0c) · #328 heartbeat prefix case-insensitive (76feb5d) · #330 heartbeat refresh (243dd57) · #331 guard-fires announce + telemetry doctrine (f873eef) · #332 ORDER 018: check --strict runs both CI legs locally (e7737e0, done=018) · #333 heartbeat done=018 (1e50427) · #334 template-pointer guard, mutation-verified (7c736fa) · #335 skill-pointer guard kit-side (26bc73b) · #336 check_skill_grounds dead-pointer detection engine-side, advisory, 0 false findings fleet-wide (2410554). Suite: 1284 tests.
- ORDER 019 item 2 = no-op/already-satisfied — enabler allowlist ("claude/*","claim/*") since #300 @ 18e5adc, predates ASK 001 by ~3h; idea-engine #271 merged 2026-07-12; report PR #339 (in flight).

## Parked
- PR #317 — owner ratification park (do-not-automerge), green @ 82fca96. Landing path: owner-click. Never arm/close/rebase.

## Registry state
- All reachable adopters tree-current at v1.15.0 (PR #327 evidence). DRIFT rows = self-report lag; resident-lane `kit:` fixes requested via outbox 2026-07-13.
kit: v1.15.0

## Backlog state (honest)
- Rungs (a)–(c) exhausted this session: inbox clear (done=001–018), adopters current, template+skill pointer truth verified AND now CI-enforced. Remaining work is gated: owner #317 sweep (→ release wave, main 45+ commits past v1.15.0), resident-lane kit: lines (→ adopters regen), grounded-skills window ~2026-07-19..26. No forced filler beyond this point (Q-0089 honesty guard).

## Next-2 baton
1. Owner sweeps #317 → cut release wave + adopter render refresh (adopters run pre-#334 template renders; superbot-next/websites boot sets lag HEAD templates — wave material, not drift).
2. After resident lanes land `kit:` lines → regenerate docs/adopters.md.

⚑ FOR OWNER (paste-ready, carried from the standing set — full field blocks verbatim in git history of this file @ 86d2a57, ⚑ OWNER-ACTION 2/6 + ⚑ FOR MANAGER):
- **P10 required-check swap (⚑ 2):** Settings → Rules → `main` ruleset → required status checks: remove "Kit test suite" + "Cold-adoption smoke (adopt + check --strict)"; add `kit-quality`; set "Require branches to be up to date" OFF. Reversible; ends the ~35-min queue-stall class. (No agent path to rulesets — verified 403/no-endpoint.)
- **fm #122 v3.4 restamp:** the owner reviews and merges fleet-manager PR #122 PERSONALLY — do NOT agent-merge.
- **UNIVERSAL wake fetch-list vN bump + re-paste:** add `docs/seat-digest.md` (+ `docs/SKILLS.md`) to the manager-authored wake fetch list, bump vN, owner re-pastes via fm's edit-registry-first flow.
- **⚑ 6 public-flip-or-PAT (pick one):** make this repo public (⚠️ effectively irreversible) OR mint a fine-grained read-only PAT into the fleet environments (reversible) — unblocks the B2–B4 cross-repo sweeps.
- **Grounded-skills measurement window:** proposal to run the before/after measurement pass ~2026-07-19..26 per docs/reports/2026-07-12-grounded-skills-wrap.md §3d — say nothing to accept the window; a successor fires it when it matures.

orders: acked=001–018 · done=001–018
