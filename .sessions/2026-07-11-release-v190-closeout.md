# 2026-07-11 — release v1.9.0 close-out (currency regen + status heartbeat)

> **Status:** `in-progress`

- **📊 Model:** fable-5 · medium · release-close — v1.9.0 published;
  this PR carries the adopters-registry regen + the status close-out

## Scope (what is about to happen)

Close-out of the release-v1.9.0 slice (claim #171 @ 180876c, bump #172 @
2a779b5, release run 29139623697). Files: `docs/adopters.md` (regenerated
via `python3 dist/bootstrap.py currency` at kit v1.9.0 — adopter rows flip
stale vs 1.9.0), `control/status.md` (heartbeat overwrite preserving
orders 001–012 acked/done, ⚑ OWNER-ACTION 2–12, ROUTINE STATE incl. the
Q-0265 cutover record, wave/release records, the T5 DAYTIME-gate and
run-6/P4 queue items; adds the v1.9.0 release record; next-slice = the
v1.9.0 distribution wave, 7 adopters),
`control/claims/release-v1.9.0.md` (deleted — claim cleared at close), and
this card. NEVER `control/inbox.md` or anything under `bench/`.
