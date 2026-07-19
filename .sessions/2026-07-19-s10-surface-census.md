# S10 — `check_surface_census` (surface the guards/jobs/hooks census in `check` output)

> **Status:** `in-progress`

**Session:** 2026-07-19 · Self Improvement work-loop · substrate-kit
**Baton:** wave-2 groom rank S10 (docs/planning/2026-07-19-night-run-idea-groom-wave2.md) — "`check_surface_census` advisory — surface guards/jobs/hooks census in check output." Provenance: fm ORDER 048 standing grant + coordinator dispatch (S9 shipped #529; baton advanced to S10).

## What I'm about to do (HOLD — born-red)

Surface the guard-surface census `guards.py` already pins — `REGISTRY` (ci.yml kit-quality steps), `WORKFLOW_JOB_CENSUS` (workflow jobs), `STRICT_SUBCHECKS` (`check --strict` sub-checks), and `HOOK_CENSUS` (lifecycle hooks) — as a one-line informational NOTE in `check` output, so the census that is otherwise only enforced by the kit-only meta-test (`tests/test_guard_surface_census.py`) is visible at `check` time. NOTE-form (mirrors `native_gate_note` / `required_unverified_note`), never exit-affecting, off STRICT_SUBCHECKS. Full details land in this card at flip.

- **📊 Model:** opus-4.8 · medium · feature build
- **⚑ Self-initiated:** [[fill: at flip]]
- **💡 Session idea:** [[fill: at flip]]
- **⟲ Previous-session review:** [[fill: at flip]]
