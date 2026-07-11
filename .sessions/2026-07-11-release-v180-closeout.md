# 2026-07-11 — release v1.8.0 close-out (currency regen + status heartbeat)

> **Status:** `in-progress`

- **📊 Model:** claude-fable-5 · medium · release-close — v1.8.0 published;
  this PR carries the adopters-registry regen + the status close-out

## Scope (what is about to happen)

Close-out of the release-v1.8.0 slice (claim #158 @ c7c430f, bump #159 @
63c6b39, release run 29133041799). Files: `docs/adopters.md` (regenerated
via `python3 dist/bootstrap.py currency` at kit v1.8.0 — adopter rows flip
stale vs 1.8.0), `control/status.md` (heartbeat overwrite preserving
orders 001–011, ⚑ OWNER-ACTION 2–12, ROUTINE STATE incl. the Q-0265
cutover record, wave records, the §6-COMPLETE note; adds the v1.8.0
release record; next-slice = the v1.8.0 distribution wave),
`control/claims/release-v1.8.0.md` (deleted — claim cleared at close), and
this card. NEVER `control/inbox.md` or anything under `bench/`.
