# 2026-07-12 — grounded-skills program, slice 6: single-source seat-digest render (kit side)

> **Status:** `in-progress`

- **📊 Model:** fable-5 · seat-worker · grounded-skills slice 6

## Scope (what is about to happen)

Implementing the KIT SIDE of §7 slice 6 of the grounded-skills program plan
(`docs/planning/2026-07-12-grounded-skills-program.md`, merged PR #263):
canonical machine-extractable seat-digest blocks — a skills-index digest and
a venue-filtered WALLS digest (Project-seat default `autonomous-project` +
`any`) — each wrapped in NEW prefix-matched fence constants in
`src/engine/grammar.py` (the capability-seed pattern), rendered into ONE
kit-generated planted doc (`docs/seat-digest.md`, digest + pointer, never
inline, per-block budget enforced), regenerable via a `bootstrap.py
seat-digest` CLI surface + refreshed at upgrade, with an advisory PL-008
drift-guard checker proving the planted file equals a fresh render
byte-for-byte. Extraction contract + no-third-copy deferral chain documented
in the generated doc itself. Tests + CHANGELOG `[Unreleased]` + dist
rebuild. **Fleet-manager-side wiring is explicitly OUT of scope** — fm moved
to prompt system v3.3 (fence-extraction/byte-match consumption; the plan's
`{{ORIENTATION_PATH}}`/`{{WALLS}}` slots are retired), so the fm regen-tool
integration ships as a separate coordinated PR.

**Provenance flag:** Coordinator proceeded on plan §8 default **Q3=A** (kit
ships canonical blocks; fleet-manager's regen tool renders seat prompts from
them) — the LEAST-confirmed default in the program; this slice's design is
therefore kept strictly additive and cleanly reversible (new module, new
planted doc, advisory-only checker; nothing existing changes behavior).

Lane claim: `control/claims/claude-slice-6-fleet-manager-render.md`
(deleted at close, last commit).
