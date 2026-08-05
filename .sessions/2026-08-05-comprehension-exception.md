# 2026-08-05 · The comprehension exception — when reading IS the job

> **Status:** `in-progress`

- **📊 Model:** opus-5 · high · template + skill

💡 Session idea: the kit's boot template tells every adopter *"That is the
whole boot set"* and argues that reading further *"buys ceremony, not
context — measured."* That default is right and the measurement is real. But
it has no exception for the session whose job **is** the reading, and on
2026-08-05 that missing exception cost a fleet-manager session the single
document its own repo introduces as *"read this if you read nothing else."*

## previous-session review

`2026-08-04-seed-skill-router.md` (#552 family) closed the loop between
planting skills and getting them loaded — routing in the one file every
session reads. This session finds the adjacent hole: the same file tells
sessions where to **stop** reading, with no way to say "not this time." A
router that loads the right skill still loses if the orientation it sits on
declared itself complete.

## Scope

Two changes at the source, both propagating to every adopter:

1. `src/engine/templates/CLAUDE.md.tmpl` — the boot set is a **floor for
   acting**, not a ceiling on reading; name the comprehension exception.
2. `src/engine/skills/skills.py` — promote `continuation-prompt` into the
   kit. It is the skill that writes every handoff prompt in the estate and
   it currently exists in **exactly one repo** (verified: 15 repos probed,
   only fleet-manager has it), so a fix to it propagates nowhere.

## What landed

*(in progress — filled at close)*

## Verification

*(in progress — build, tests, ruff, gate; real exit codes)*
