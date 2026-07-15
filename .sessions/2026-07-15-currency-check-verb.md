# 2026-07-15 · currency-check-verb

> **Status:** `in-progress`

About to: build the `currency --check` registry-delta preflight (baton item 2,
idea docs/ideas/currency-check-registry-delta-preflight-2026-07-15.md) — a
no-write flag on the existing currency verb that compares a fresh in-memory
scan against the committed docs/adopters.md rows-only (timestamp ignored,
dark repos never read as delta) and exits 0/1; engine + tests + dist byte-pin
regen in the same PR; idea lifecycle flipped in-PR.
