# Session · 2026-07-16 · staged-regen-render

> **Status:** `complete`

Intent: re-render the staged `.substrate/` tree so interview slots filled since #381 are actually rendered — clearing the 3 `staged-regen-lag` advisories that `check --strict` has been emitting on the kit's own tree.

- **📊 Model:** opus-4.8 · medium · docs-only (staged .substrate/ re-render)
- ⚑ Self-initiated: no — coordinator-dispatched contained slice under decide-and-flag ([PL-012]); the 3 staged-regen-lag advisories were the one visible buildable rung.

## What shipped (PR #432)

Three staged files under `.substrate/` carried unrendered `${slot}` tokens for interview slots filled since #381; the staged tree only re-renders on `upgrade`, so `check --strict` printed 3 `staged-regen-lag` advisories naming them. Ran the kit's own render path — `python3 dist/bootstrap.py agents --build` (regenerates the architect + reviewer personas) plus a scoped `adopt` keeping only `.substrate/claude/CLAUDE.md` and discarding every other adopt output — then verified the net diff is exactly 3 files:

- `.substrate/agents/architect.md` — filled slots `architecture_layers` / `ownership_model` / `mutation_seam`.
- `.substrate/agents/reviewer.md` — filled slots `architecture_layers` / `ownership_model` + a verify-command refresh (`python3 -m pytest` → `python3.10 -m pytest tests/ -q`).
- `.substrate/claude/CLAUDE.md` — filled slots `architecture_layers` / `owner_profile` (plus project-description + adoption-pace slot values), verify-command refresh, and a wholesale newer-template body (removed the "UNRENDERED SLOTS" banner, added the Preflight step 0 / HANDOFF.md / boot-set routing / Kit-machinery section). ~48-line refresh — expected, the staged tree regenerates wholesale.

Live diff was byte-identical to the pre-validated preview. Churn audit: every change traces to a filled slot or a newer template — nothing hand-edited, no anomalies. `check --strict` after the render: the 3 `staged-regen-lag` advisories are GONE (0 remaining); the only red left is the born-red HOLD on this card, cleared by this flip. Commit hygiene held: the re-render commit staged exactly the 3 files (no `git add -A`); the guard-fire telemetry delta rode the heartbeat commit per the checker's "commit the delta, do not revert" note.

## 💡 Session idea

Turnkey staged-regen remediation — a `python3 dist/bootstrap.py render --staged` (or `check --fix-staged`) that re-renders *only* the staged `.substrate/` tree in place, so clearing a `staged-regen-lag` advisory is one command instead of the `agents --build` + scoped-`adopt` + manual keep-filter dance this session performed. Dedup: idea #345 (`staged-artifact-regen-lag-checker`, shipped) is the *detector*; this is the missing *remediator* — no `render --staged` / `fix-staged` idea exists in docs/ideas/. Worth having: closes the enforce-don't-exhort loop (the checker that names the problem should ship the turnkey fix), and the current manual recipe is footgun-prone — a broad `adopt` writes docs/CI/skills output that is easy to commit by accident, exactly the churn this session had to hand-filter back out.

## ⟲ Previous-session review

The #430 registry-refresh session did the enforce-don't-exhort instinct well: rather than only regenerating `docs/adopters.md`, it filed an adopters-staleness self-signal idea (a timestamp-age advisory turning a silently-missing currency cron into a visible nudge) — surfacing the *root cause* of the drift it fixed, not just the symptom. Genuine miss: that same session ran `check --strict`, saw these 3 `staged-regen-lag` advisories in its own output, and still declared the buildable backlog "DRY beyond date-parked / owner-gated" — but a non-gating advisory with a contained, turnkey remediation (proven here: a 3-file render) *is* a buildable rung. Concrete system improvement: the heartbeat's "backlog DRY" claim should be cross-checked against live `check --strict` advisories — any advisory naming a self-contained fix contradicts a DRY declaration, so the seat shouldn't record the backlog empty while a remediable advisory sits in its own gate output. (This is the natural companion to my session idea above: a turnkey remediator would make such a rung unmissable.)
