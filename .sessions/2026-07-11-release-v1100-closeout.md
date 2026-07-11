# 2026-07-11 — release v1.10.0 close-out (currency regen + status heartbeat)

> **Status:** `complete`

- **📊 Model:** Claude (Fable family) · medium · release-close — v1.10.0
  published; this PR carries the adopters-registry regen + the status
  close-out

## Scope (what is about to happen)

Close-out of the release-v1.10.0 slice (claim #177 @ 7122aca, bump #178 @
1b5db16, release run 29142780212). Files: `docs/adopters.md` (regenerated
via `python3 dist/bootstrap.py currency` at kit v1.10.0 — adopter rows
flip stale vs 1.10.0), `control/status.md` (heartbeat overwrite
preserving orders 001–012 acked/done, ⚑ OWNER-ACTION 2–12, ROUTINE STATE
incl. the Q-0265 cutover record, wave/release records, the T5
DAYTIME-gate and run-6/P4 + B2–B4/OA-6 queue items; adds the v1.10.0
release record; next-slice = the v1.10.0 distribution wave, 7 adopters,
PRIORITY — it ships the gate-loophole fix),
`control/claims/release-v1.10.0.md` (deleted — claim cleared at close),
and this card. NEVER `control/inbox.md` or anything under `bench/`.

## Close-out

Shipped the declared scope exactly. `docs/adopters.md` regenerated at kit
v1.10.0 — all 7 engaged rows now read `stale (v1.9.0 < v1.10.0)`:
superbot-next, websites, superbot-games, trading-strategy, gba-homebrew,
venture-lab, fleet-manager (superbot stays pin-only stale v1.0.0;
pokemon-mod-lab not adopted; the kit's own row reads self-report v1.9.0 ·
DRIFT because the currency scan reads the REMOTE heartbeat and this PR is
what lands the v1.10.0 line — the expected mid-close state, self-heals at
the next regen, never hand-fixed). `control/status.md` overwritten with
the v1.10.0 release record; preserved: orders 001–012 acked/done, ⚑
OWNER-ACTION 2–12, ROUTINE STATE (Q-0265 cutover + failsafe trigger), all
wave/release/EAP records, the T5 DAYTIME-gated item, the run-6/P4-loop
item, the B2–B4/OA-6 item, QUEUED KIT FIXES, ⚑ FOR MANAGER, the B1 family
verdicts, PING-ACK, ORDER 010 RECORD, and the version-truth deference
flag (its dist mention bumped to v1.10.0; OWNER-ACTION 7's drift count
bumped to 11 releases). Next-slice set: the v1.10.0 distribution wave (7
adopters) — PRIORITY, it ships the gate-loophole fix. Claim
`control/claims/release-v1.10.0.md` deleted. Release facts recorded: run
29142780212 success · tag v1.10.0 (annotated eb1b6f3) → 1b5db16 · asset
sha256 ba69fc5cf21619cc85e4c733ebe3d9eda8803e678f810fcc39b94d60c2f3b5a4
three-way verified (downloaded asset = release.json = committed dist).
Verified locally on this branch: `python3.10 -m pytest tests/ -q` → 983
passed; `check_program_law` OK; `check_idea_index` OK; `check --strict`
sole pre-flip finding was this card's own designed born-red hold.

## 💡 Session idea

Release-run polling has a proven fast path and a proven dead end: direct
`api.github.com` curl through the session proxy returned nothing usable
(a 10-minute poll loop spun dry) while the GitHub MCP `actions_get`
answered the same question instantly. Worth one line in the runbook §4
("watch the run via the API toolset, not raw curl — the proxy wall is
live-hit") and a matching wall entry in `docs/CAPABILITIES.md` with the
discovery-rule citation, so no future cut burns ten minutes re-finding
it.

## ⟲ Previous-session review

The bump session (#178, same lane, minutes earlier) followed the runbook
end to end on its first live exercise and proved it accurate — claim
ordering, born-red flow, byte-pin, verify set, flip — and its card
recorded the runbook's one wording nit instead of silently normalizing
it, which is exactly what "the runbook's first exercise is itself a
deliverable" asked for. Improvement it leaves standing: its 💡 (a check
advisory that the bump branch was cut from post-claim main) is the third
consecutive release-lane idea aimed at mechanizing runbook ordering —
these should be groomed into one `docs/ideas/` file with a single owner
rather than accumulating as per-card one-liners.
