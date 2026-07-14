# 2026-07-14 — verify_release mechanization (release runbook §5 as one command)

> **Status:** `in-progress`

About to (opening declaration): build the #356 card's 💡 ender —
`scripts/verify_release.py <version>`, mechanizing the runbook §5 three-way
post-release verification (tag → bump commit · release.json sha256 == downloaded
asset sha256 == committed dist/bootstrap.py at the bump SHA · release.yml run
green), PASS/FAIL/SKIPPED per leg with expected-vs-actual, honest degradation on
network walls, read-only (never pushes/dispatches). Plus tests.

- **📊 Model:** Fable 5 · high · feature build

Run type: worker session (post-EAP backlog build, coordinator-dispatched).
