# S15 — cut_release --rebuild-dist

> **Status:** `in-progress`

**Session:** 2026-07-20 · Self Improvement work-loop · substrate-kit
**Baton:** wave-2 groom rank S15 (docs/planning/2026-07-19-night-run-idea-groom-wave2.md line 37) — "cut_release --rebuild-dist — fold FOLLOWUP dist rebuild into the cut." Provenance: fm ORDER 048 standing grant + coordinator dispatch (S14 shipped #539; baton advanced to S15).

## What I'm about to do

Add a `--rebuild-dist` flag to `scripts/cut_release.py` that folds FOLLOWUP checklist step 2 (dist regen + byte-pin) into the `--write` cut: after the version-bump edits are applied, run the dist builder, verify the byte-pin, and mark step 2 done in the printed checklist. Tooling only — the flag is built + unit-tested in isolation against fixture repos; NO real release is cut (no KIT_VERSION bump, no tag, no workflow_dispatch, no release.json change).

HOLD (born-red): this card ships `in-progress` in the first commit; flipped to `complete` as the last commit once the build + tests + dist byte-pin are green.
