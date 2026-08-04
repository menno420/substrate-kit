# 2026-08-04 · Seed the task→skill router into the working agreement

> **Status:** `complete`

- **📊 Model:** fable-5 · high · feature build

💡 Session idea: **the kit plants skills and plants the working agreement, but
until now nothing connected them — so every adopter's skill set depended on
sessions happening to read an index.** The router closes the loop the same way
`CAPABILITIES.md` closed the capability loop: put the routing in the one file
every session reads unconditionally, state the binding rule (PL-013: a skill
you didn't load can't bind you), and make a miss a named defect so reviews
have something to check. Proven in fleet-manager first (its 2026-08-04
router), generalized here with only the kit-shipped rows plus an explicit
local-extension clause — adopters append rows, never fork the section.

## previous-session review

`2026-08-04-gate-collision-and-effort-tiers.md` (PR #571, merged) fixed the
collision that silently dropped a gate from three skills' rituals. Same
family of problem, opposite direction: #571 fixed skills whose *content*
degraded on render; this seeds the mechanism that gets skills *loaded* at
all. Content and routing are the two halves of "the standard arrives with
the task."

## What shipped

- **`src/engine/templates/CLAUDE.md.tmpl`** — a "Task → skill routing"
  section: eight recurring kit task classes mapped to their skill, the
  binding rule with its PL-013 citation, the local-extension clause, and the
  defect framing. Every future seed and `upgrade --apply-docs` carries it.
- **`tests/test_skill_router_section.py`** — pins the section's doctrine
  phrases and asserts every recurring kit skill has a router row (the
  enforcing half; no checker consumes doctrine sentences).
- `dist/bootstrap.py` rebuilt.

## Honest null

The router's effectiveness is unmeasured kit-wide, as it is in fleet-manager:
the metric is future session cards showing skills firing unprompted.
fleet-manager's own richer router is untouched — plants are skip-if-exists
and its live `.claude/CLAUDE.md` is host-owned.

## Verify

```bash
python3 -m pytest        # 2083 passed, 1 skipped
```
