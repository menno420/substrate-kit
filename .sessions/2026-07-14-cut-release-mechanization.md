# 2026-07-14 — cut_release mechanization (release-cut preparation as one command)

> **Status:** `in-progress`

About to (opening declaration): build the Night-9 (#351 card) 💡 ender —
`scripts/cut_release.py`, a dry-run-by-default mechanization of the release
cut's PREPARATION (bump both version homes in one coherent edit, transform
CHANGELOG `[Unreleased]` → dated released section per the runbook +
`check_changelog_structure.py` shape, print the manual follow-up checklist);
it never commits, pushes, dispatches, or touches the network. Plus tests.

- **📊 Model:** Fable 5 · high · feature build

Run type: worker session (BUILD phase, coordinator-dispatched).
