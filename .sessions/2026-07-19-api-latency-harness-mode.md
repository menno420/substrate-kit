# Session card — graduate PR-latency into the harness as `--api-latency`

> **Status:** `in-progress`

## What I'm about to do
Add an opt-in `--api-latency` mode to `scripts/measure_grounded_skills.py` that
reuses `scripts/measure_pr_latency.py`'s pure logic (no duplication) and cleanly
SKIPS (not errors) when no token is present or the network fails — plus tests and
a docs update. Byte-identical default behavior when the flag is off.
