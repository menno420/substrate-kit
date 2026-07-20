# S13 — clone-depth provenance on results.json

> **Status:** `in-progress`

**Session:** 2026-07-20 · Self Improvement work-loop · substrate-kit
**Baton:** wave-2 groom rank S13 (docs/planning/2026-07-19-night-run-idea-groom-wave2.md line 35) — "clone-depth provenance on results.json (clone_depth + git_sha)." Provenance: fm ORDER 048 standing grant + coordinator dispatch (S12 shipped #535; baton advanced to S13).

## What I'm about to do

Extend `scripts/measure_grounded_skills.py`'s per-repo measurement to record
**clone-depth provenance** in the machine-readable `results.json` payload:
each `RepoResult` gains `clone_depth` (`full`/`shallow`/`unknown`, from the
S5-shared `_git_truth.require_full_history()` helper) and `git_sha` (the HEAD
commit SHA the measurement was taken against, or `null` when the tree isn't a
usable git repo). This turns the payload's existing shallow-guard signal
(currently only exposed as `merged["shallow"]`, a per-repo bool) into
first-class, self-describing provenance — a later reader of a frozen
`results.json` can see *which* commit of each repo the numbers were computed
against, and whether the clone was full/shallow, without re-running.
Read-only, standalone-script only (not in MODULE_ORDER → dist untouched);
+tests over fixture trees; no network.

- **📊 Model:** opus-4.7 · medium · feature build
