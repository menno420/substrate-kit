---
state: captured
origin: consumer:menno420/superbot-games
shipped_pr: null
shipped_repo: null
merged_date: null
outcome: open
---

# `adopt --wire-enforcement` plants a pytest step when tests/ exists (2026-07-10)

> **Status:** `ideas`
>
> **State:** captured (gen-2 night-prep seed by the grand-review session).
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
