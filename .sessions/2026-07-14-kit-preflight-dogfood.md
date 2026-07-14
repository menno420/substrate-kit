# 2026-07-14 · kit-side scripts/preflight.py (CI-convergence dogfood)

> **Status:** `in-progress`

About to happen (opening declaration): build the kit-repo-local
`scripts/preflight.py` so the kit dogfoods its own ORDER 018 preflight
mechanism — `config.py::_default_preflight_scripts()` defaults to
`["scripts/preflight.py"]` but the file doesn't exist here, so every full
`check` prints a standing NOTE and local `check --strict` runs none of the
7 CI kit-quality legs (the local-green→CI-red class from ASK 002 /
idea-engine #274/#299). Pure kit-repo addition: no engine/src change, no
dist regen, no adopter surface.

- **📊 Model:** fable-5 · high · feature build

Run type: worker session (coordinator-dispatched BUILD+LAND).
