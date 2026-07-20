# S14 — dateless-wall advisory

> **Status:** `in-progress`

**Session:** 2026-07-20 · Self Improvement work-loop · substrate-kit
**Baton:** wave-2 groom rank S14 (docs/planning/2026-07-19-night-run-idea-groom-wave2.md line 36) — "dateless-wall advisory — flag wall rows with no parseable date." Provenance: fm ORDER 048 standing grant + coordinator dispatch (S13 shipped #537; baton advanced to S14).

## What I am about to do

Build `src/engine/checks/check_dateless_walls.py` — a warn-only advisory (never exit-affecting) that surfaces any `wall` row in `docs/CAPABILITIES.md` (a `## Walls` seed row, or a `· wall ·` append-log row) carrying **no parseable date**. This is the exact NEGATIVE complement of R5's `check_stale_walls`, which explicitly skips dateless rows as "a separate concern" (check_stale_walls.py:24): a wall with no date can never trip the >14d re-verify staleness rule, so it silently escapes the DISCOVERY RULE's re-verify cadence forever. Flagging it nudges the owner to add a `LAST-VERIFIED:` stamp (seed row) or a leading append-log date so the staleness rule can fire. Wired on the `posture="advisory"` seam in cli.py; off STRICT_SUBCHECKS; a `check_remediate.REMEDIATIONS` entry for the new `dateless-wall` kind (S8 coverage-gap lesson); dist rebuilt (cli.py is dist-shipped). Tests mirror `tests/test_check_stale_walls.py`.

- **📊 Model:** opus-4.8 · medium · feature build

<!-- close-out markers (💡 Session idea, ⟲ Previous-session review, ⚑ Self-initiated) added at the flip -->
