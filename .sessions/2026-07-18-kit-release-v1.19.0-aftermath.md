# Session · 2026-07-18 · kit-release-v1.19.0-aftermath

> **Status:** `in-progress`

Intent: release aftermath — regen `docs/adopters.md` + update `docs/current-state.md`
to v1.19.0 released (self-row v1.19.0; adopters stay stale pending the owner-gated wave).

About to: regenerate the adopter registry via `python3 dist/bootstrap.py currency`
(self-row → v1.19.0, adopter rows correctly stale), update `docs/current-state.md`
v1.18.0-released-not-distributed → v1.19.0 released + verified, and correct
`control/status.md`'s Recently-shipped release record to the completed truth
(tag v1.19.0, run success, sha256 three-way PASS, release URL). Card holds the PR
red until the deliberate final flip.

Scope: `docs/adopters.md` · `docs/current-state.md` · `control/status.md` · this
card · `control/claims/release-v1-19-0-aftermath.md`.
