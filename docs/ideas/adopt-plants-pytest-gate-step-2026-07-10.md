---
state: promoted
origin: consumer:menno420/superbot-games
shipped_pr: 403
shipped_repo: menno420/substrate-kit
merged_date: 2026-07-15
outcome: shipped
---

# `adopt --wire-enforcement` plants a pytest step when tests/ exists (2026-07-10)

> **Status:** `ideas`
>
> **State:** promoted → **shipped** kit PR #403 (2026-07-15, anticipated
> in-PR date): the generated substrate-gate carries a pytest step behind
> the control-fast-lane short-circuit — always planted, self-skips in-job
> when `tests/` is absent (the simpler self-healing variant named below),
> installs pytest + the host's `requirements.txt` when present, runs
> `-m pytest tests/ -q` on the gate's configured interpreter.
> **Origin:** consumer — superbot-games lived its whole gen-1 life with a
> tests-blind gate: `substrate-gate` ran only `check --strict` while the repo's
> 73 pure-domain tests never ran in CI (fixed consumer-side in games#16; both
> lanes had assumed CI ran their tests).

**One line:** when `adopt --wire-enforcement` writes the substrate-gate workflow into a
host that has a `tests/` directory, plant a pytest step behind the same
control-fast-lane short-circuit — a convention ships with its checker, and a test suite
ships with its CI runner.

**Shape:** template addition in the generated workflow (conditional on `tests/`
existing at adopt time, or always-planted-but-short-circuiting when `tests/` is absent —
the second is simpler and self-heals when tests arrive later). Ordinary lane; engine
change → dist byte-pin.

**Size:** small (template + one adoption-smoke assertion).
