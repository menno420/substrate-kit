# Self Improvement seat — heartbeat
updated: 2026-07-14T21:03Z · phase: post-EAP — v1.17.0 adopter wave COMPLETE (9/9 merged) + registry regenerated; ORDER 023 done-when COMPLETE

## Routines
- Failsafe: "Self Improvement failsafe wake" trig_01LsHxvnYnpQ59n7iQTPNNF3 · 0 */2 * * * · bound live coordinator. Pacemaker idles to failsafe post-consolidation (backlog dry).
- Business cron: kit-lab daily trig_01Jm57GAjNCFrYJn1oLMiYGE — KEEP.

## Facts
- v1.17.0 adopter upgrade wave COMPLETE (2026-07-14): all 9 engaged adopters upgraded v1.16.0 → v1.17.0 and MERGED — superbot-next #487 (main ba92416) · websites #339 · fleet-manager #211 (main 1c5f421) · superbot-games #144 (squash 42a31c5) · gba-homebrew #138 · venture-lab #199 · idea-engine #423 (main d086bfa) · superbot-mineverse #112 · trading-strategy #126. Asset three-way sha256-verified everywhere (0d08b8aa9efc30178cf8e8befcfa28dd2b65e02106cc9ba6d520133017955521, 995446 B); apply-docs a legitimate no-op on all 9 (v1.17.0 shipped zero doc-template deltas); branch-sweep.yml landed STAGED-only (.substrate/ci/) on all 9, none wired live (lane-owed); host workflow carve-outs restored byte-identical (superbot-next + gba-homebrew enabler skip-arming, idea-engine gate wake-preflight + enabler skip-arming); zero platform denials. Excluded per orders: pokemon-mod-lab (Game-project lane, v1.15.0) · superbot (pin-only v1.0.0, owner-held). Wave record: .sessions/2026-07-14-v1.17.0-wave.md.
- ORDER 023 state: done-when COMPLETE — sweep workflow template released ✓ at v1.17.0 (tag c9ae7e8 / kit main 4a2d4ec; BUILD #376, release #377, run 29359896797) AND adopters regenerated ✓ (9/9 merged + registry regen, wave PR this session).
- release v1.17.0 CUT + VERIFIED (2026-07-14): bump PR #377 merged as 4a2d4ecddd63; release.yml run 29359896797 SUCCESS; verify_release.py → tag leg PASS (tag c9ae7e885009 → 4a2d4ecddd63) · three-way sha256 PASS (0d08b8aa…5521, 995446 B) · workflow-API leg SKIPPED on the documented api.github.com proxy 403, covered by watched run 29359896797. Aftermath PR #378. Detail: .sessions/2026-07-14-release-v1.17.0-aftermath.md.
- release v1.16.0 CUT + VERIFIED (2026-07-14): PR #370 merged as 93aa377; run 29342538960 SUCCESS; sha256 bba34e2102cbaf09394f39992f0501ea5cfd542d90301ef67e31a0854ca59170 (980026 B). Full record: git history of this file @ 0dc104b.

## Backlog state (honest)
Buildable backlog DRY. ORDER 023 fully closed with this wave. Remaining: chronic adopter heartbeat `kit:` self-report lag (6 repos lane-owed, see docs/adopters.md drift report) · grounded-skills window ~07-19. No filler beyond this line (Q-0089).

## Parked
- (none)

## Ratified/merged (2026-07-14 reconcile)
- PR #317 — RATIFIED + MERGED as 4f6e50c. PR #345 — RATIFIED + MERGED as c603cc9. PR #371 — MERGED as 39c6b20 (rode v1.16.0). PR #376 — MERGED as 0dc104b via the auto-merge enabler (ORDER 023 BUILD half). PR #377 — MERGED as 4a2d4ec (v1.17.0 bump). PR #378 — MERGED (v1.17.0 aftermath).

## Registry state
- adopters.md regenerated post-wave (this session's PR): all 9 engaged adopter trees at v1.17.0; pokemon-mod-lab v1.15.0 (excluded lane); superbot pin-only v1.0.0 (owner-held). Remaining DRIFT rows = chronic self-report heartbeat lag (lane-owed) + the kit's chronic config-pin v1.0.0.
kit: v1.17.0

## Next-2 baton
1. Grounded-skills measurement window ~2026-07-19..26.
2. Adopter heartbeat `kit:` self-report lag — consider graduating the chronic 6-repo class to inbox ORDERs (lane-owed today).

⚑ FOR OWNER (unchanged standing set — full paste-ready field blocks verbatim in git history of this file @ 86d2a57):
- P10 required-check swap (ruleset: require `kit-quality`, drop the two legacy contexts).
- fm #122 v3.4 restamp — owner reviews/merges PERSONALLY.
- UNIVERSAL wake fetch-list vN bump (+ docs/seat-digest.md, docs/SKILLS.md).
- ⚑ 6 public-flip-or-PAT (unblocks B2–B4 cross-repo sweeps).
- Grounded-skills measurement window ~2026-07-19..26 — silence accepts.

orders: acked=001–023 · done=001–023 (023: BUILD #376 + release #377 + run 29359896797 publish + registry regen wave COMPLETE — 9/9 adopters merged, .sessions/2026-07-14-v1.17.0-wave.md)
