# 2026-07-11 — P4 investigation (run-6 unblock) + v1.10.1-wave mechanical fixes

> **Status:** `in-progress`

- **📊 Model:** fable-5 · medium · runtime bugfix

## Scope (what is about to happen)

One bounded slice, claim `control/claims/p4-unblock-run6.md` (#194 @ 5b71234, on
main before build). Part 1: identify what "the P4 loop" gating bench run-6
actually is (queue-state crosswalk / lab-loop.md / founding plan §7.2 / status
OWNER-ACTION 3), then either build/arm the minimal agent-side version or record
the wall verbatim — NEVER fake what's missing; the bench itself is NOT run this
slice. Part 2, mechanical fixes from the v1.10.1 wave findings: (a) currency
`kit:`-line parser accepts a markdown-bullet-embedded heartbeat line
(venture-lab's `- **kit heartbeat:** kit: v…` shape — the #192-wave card
finding); (b) generated gate workflow action majors bumped off Node-20-deprecated
pins (actions/checkout@v4→v5, actions/setup-python@v5→v6) + test pins + dist
regen; (c) the guard-fires.jsonl dedupe idea filed on trading-strategy #57's
card — implement if genuinely small, else queue with reason. CHANGELOG
[Unreleased] entries for whatever ships; NO release cut. Close-out: status.md
overwrite (preserving orders through 012 + ⚑ OWNER-ACTION 2–13, adding the
v1.10.1 wave record) as the deliberate last step before this card's flip.
Files: src/engine/{grammar,adopt,loop/telemetry}.py + tests + dist/bootstrap.py
+ CHANGELOG.md + control/status.md + this card. NEVER control/inbox.md, bench/,
sibling cards, or PR #181.
