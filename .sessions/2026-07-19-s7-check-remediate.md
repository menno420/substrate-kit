# S7 — `check --remediate <finding-kind>` (paste-ready remediation lookup)

> **Status:** `in-progress`

**Session:** 2026-07-19 · Self Improvement work-loop · substrate-kit
**Baton:** wave-2 groom rank S7 (docs/planning/2026-07-19-night-run-idea-groom-wave2.md) — `check --remediate <finding-kind>` prints the paste-ready remediation block for a finding kind, print-only (exits 0, never a gate, never modifies files). Provenance: fm ORDER 048 standing grant + coordinator dispatch (S6 shipped #522; baton advanced to S7).

## What I'm about to do

Add a print-only `check --remediate <finding-kind>` CLI lookup (mirrors R6's `check --explain-wall`): given a `check` finding kind, print a paste-ready remediation block a host can apply to clear that finding. A pure lookup — always exits 0, touches no files, is never a gate — so the S7 guard rails (opt-in flag, never default, dry-run-friendly, scoped) hold by construction. Seed a `REMEDIATIONS` registry keyed by finding kind, reusing existing source-of-truth remediation content (import `check_folded_gate.REMEDIATION_SNIPPET`), plus tests including one asserting the command modifies nothing.

- **📊 Model:** opus-4.8 · medium · feature build
