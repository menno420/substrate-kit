# Self Improvement seat — heartbeat
updated: 2026-07-13T12:51Z · coordinator session live (v3.6 boot 2026-07-13) · phase: ACTIVE

## Routines (verified via paginated list_triggers, 2026-07-13T12:36Z audit)
- Failsafe: "Self Improvement failsafe wake" trig_01LsHxvnYnpQ59n7iQTPNNF3 · cron 0 */2 * * * · bound to live coordinator session · next ~14:06Z.
- Pacemaker: send_later chain live (~15 min cadence).
- Cutover: old-seat failsafe trig_01EMfauRqevNovFM8dz4NLdp DELETED 2026-07-13 (new failsafe verified armed first); the 11 old-seat one-shots are fired tombstones, no action.
- Business cron: kit-lab daily trig_01Jm57GAjNCFrYJn1oLMiYGE — fresh-session-per-fire, KEEP, never rebound · last fired 2026-07-13T06:10Z · next 2026-07-14T06:08Z · not wedged.

## Shipped
- PR #325 MERGED (squash d916d94, main HEAD): docs/adopters.md regenerated via dist/bootstrap.py currency (Generated: 2026-07-13T12:42:36Z · kit release: v1.15.0). Merge payload diff-verified: exactly adopters.md + session card; claim added-then-deleted in-PR.

## Parked
- PR #317 — owner ratification park (do-not-automerge), green @ 82fca96, no new commits. Landing path: owner-click. Never arm/close/rebase.

## Registry state
- Remaining DRIFT rows (reconcile at source, not kit writes): kit-self pin v1.0.0 · superbot-games v1.7.1 (two lanes) · fleet-manager v1.7.0.
kit: v1.15.0

## Next-2 baton
1. Owner sweeps #317 → then cut release wave (main is 34+ commits past v1.15.0) + adopter upgrade PRs.
2. Grounded-skills measurement window ~2026-07-19..26.

⚑ FOR OWNER (paste-ready, carried from the standing set — full field blocks verbatim in git history of this file @ 86d2a57, ⚑ OWNER-ACTION 2/6 + ⚑ FOR MANAGER):
- **P10 required-check swap (⚑ 2):** Settings → Rules → `main` ruleset → required status checks: remove "Kit test suite" + "Cold-adoption smoke (adopt + check --strict)"; add `kit-quality`; set "Require branches to be up to date" OFF. Reversible; ends the ~35-min queue-stall class. (No agent path to rulesets — verified 403/no-endpoint.)
- **fm #122 v3.4 restamp:** the owner reviews and merges fleet-manager PR #122 PERSONALLY — do NOT agent-merge.
- **UNIVERSAL wake fetch-list vN bump + re-paste:** add `docs/seat-digest.md` (+ `docs/SKILLS.md`) to the manager-authored wake fetch list, bump vN, owner re-pastes via fm's edit-registry-first flow.
- **⚑ 6 public-flip-or-PAT (pick one):** make this repo public (⚠️ effectively irreversible) OR mint a fine-grained read-only PAT into the fleet environments (reversible) — unblocks the B2–B4 cross-repo sweeps.
- **Grounded-skills measurement window:** proposal to run the before/after measurement pass ~2026-07-19..26 per docs/reports/2026-07-12-grounded-skills-wrap.md §3d — say nothing to accept the window; a successor fires it when it matures.

orders: acked=001–017 · done=001–017
