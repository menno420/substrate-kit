# R10 — harness `--freeze` self-citing reproduce block

> **Status:** `complete`

**Session:** 2026-07-19 · Self Improvement work-loop · substrate-kit
**Baton:** R10 (harness `--freeze` self-citing reproduce block) from docs/planning/2026-07-19-night-run-idea-groom.md — the #2 baton after R9 (#501) shipped.

**About to do:** add a `--freeze` flag to `scripts/measure_grounded_skills.py` that, given `--json`/`--commit-results`, also emits the output's sha256 + a paste-ready reproduce block and writes a `<output>.freeze` sidecar — every window run becomes self-citing and tamper-evident.

- **📊 Model:** Opus 4.8 · high · feature build (harness --freeze self-citing reproduce block + 7 tests)
- **⚑ Self-initiated:** R10 is baton work (#2 baton, taken after R9/#501 shipped). Decide-and-flag calls within it: (1) the sha256 is over the exact `blob` bytes written and lives in a `.freeze` SIDECAR, not inside the payload, so `sha256sum <output>` verifies with no canonicalization and there is no self-referential hash; (2) `--freeze` errors if neither `--json` nor `--commit-results` is present (fail-fast, not a silent no-op); (3) the emission runs INSIDE the R3 shallow-clone REFUSE guard so a frozen artifact can never ship off a shallow clone whose M4 metrics are zeroed; (4) the reproduce command is reconstructed from the effective argv + repo-relative script path so it is paste-ready and exact.

## What shipped (PR #505)
`--freeze` on `scripts/measure_grounded_skills.py`: with `--json`/`--commit-results` it computes `sha256(blob)` over the exact bytes written, reconstructs the exact reproduce command, writes a `<output>.freeze` sidecar (JSON: `tool`/`algo`/`sha256`/`bytes`/`reproduce`/`note`) next to each artifact, and prints a paste-ready citation block to stderr. Verifiable with a plain `sha256sum <output>`. Standalone `scripts/` file — not in MODULE_ORDER, no dist rebuild. Files: `scripts/measure_grounded_skills.py` (`--freeze` flag + `_render_freeze_block` + `_SCRIPT_REL` + hashlib/shlex imports + docstring line), `tests/test_measure_grounded_skills.py` (7 new tests: sidecar+stderr block, exact sha256 match, exact reproduce command, `--json`/`--commit-results` requirement, default-off, shallow refuse, both-sinks-share-digest). Full suite 1880 passed / 1 skipped; `check --strict` exit 0 after this flip. Claim PR #504 MERGED (fast lane); build PR #505 auto-merges on green after this flip.

## 💡 Session idea
`--freeze --verify <output>`: a companion verify mode that reads the `<output>.freeze` sidecar, re-hashes the named artifact, and exits non-zero on mismatch — turning the self-citing sidecar into a one-command tamper check a CI step or a later measure→verify→publish stage can gate on. It closes the loop R10 opens (emit a citation) with the read side (enforce it), and reuses the existing exit-2 refuse convention. Small; deduped against groom R11–R13 and docs/ideas/ (no freeze/verify entry present).

## ⟲ Previous-session review
R9 (#501, `--commit-results PATH`) did the harder-than-it-looks thing well: it reused `--json`'s shallow-clone REFUSE gate rather than re-deriving it, and its heartbeat proactively reconciled a sibling's mid-flight R8 narrative drift instead of leaving it — the fix-on-sight the doctrine wants. Could-do-better: R9 pinned its "commits = write file, not git" decision only in prose; R10 makes that class of decision testable (the sha256/reproduce contract is pinned by 7 tests), the more durable form. **System improvement:** the three harness flags (`--json` R3, `--commit-results` R9, `--freeze` R10) now overlap heavily in the JSON-emit block and its shallow-guard; extracting a single `_emit_machine_readable(payload, args)` helper would stop the next flag copy-pasting the guard — captured as a groom candidate so it's visible, not silently deferred.
