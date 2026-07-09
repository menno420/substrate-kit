# Session 2026-07-09 — KL-5 (1/2): auto-drafted handoff

> **Status:** `in-progress` *(born-red — flip to `complete` as the deliberate last step.)*

**About to do (founding plan §10 KL-5 row, first half — the ruled prerequisite
for B1):** mechanize session write-back per
`docs/ideas/substrate-kit-auto-drafted-handoff-2026-07-07.md` (canonical copy
superbot-resident) — `session-close` + the Stop hook auto-draft the session
card's close-out from evidence (files touched since the session-start anchor,
git HEAD movement read from `.git` by pure file parsing, the derived verify
command), a missing card gets a drafted skeleton, and the session-log checker
gains the **drafted-vs-completed** distinction (`[[fill:]]` slots + a
`drafted` status token hold the born-red gate). Engine rules: stdlib-only, no
print/assert/subprocess, fail-open on agent-blocking paths, atomic writes.
Second half of the band (the `bench/` tree) follows as a separate
`do-not-automerge` PR per §5.0.
