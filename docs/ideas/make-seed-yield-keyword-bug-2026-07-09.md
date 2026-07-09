---
state: captured
origin: lab
shipped_pr: null
shipped_repo: null
merged_date: null
outcome: open
---

# make_seed: keyword domain nouns generate SyntaxError seeds + prepare should smoke the seed suite (2026-07-09)

> **Status:** `ideas`
>
> **State:** captured (B1 record session, run `2026-07-09-run02`). ⚑ Pin
> path: `bench/seeds/make_seed.py` is under `bench/seeds/` — **the fix
> MUST ride a `do-not-automerge` owner-review PR**
> (`check_bench_integrity.py` rule 1). Do not auto-merge this one.

## The bug (found live, run-2 prepare)

Run-2's ordered seed **424242** generates the harvest/**yield** domain —
and `yield` is a Python keyword — so the generated seed project is a
**SyntaxError**: the arms cannot even import it. The runner deviated by
rule to the first keyword-safe seed above it, **424243** (cedarvisit),
recording the deviation in the manifest (`runner_notes` item 1;
`bench/results/cold-start/2026-07-09-run02/manifest.json`). 424245 was
also skipped-by-rule for a different reason (it reproduces run-1's exact
galereading surface — cross-run contamination).

Root cause: `make_seed.py`'s domain-noun vocabulary is not screened
against Python keywords (`keyword.iskeyword()`) or builtins before the
nouns become identifiers (module/function/argument names).

## The guard half: `run_ab.py prepare` should run the seed's tests

The bug reached the runner because nothing between "seed generated" and
"session started" executes the seed project. `prepare`'s smoke step
checks kit-surface presence + `check --strict`, but never runs the seed
suite. Recipe: after generating each arm, run the seed's own pytest
(both arms) and abort the prepare on red — a SyntaxError seed then dies
at prepare time with a named error instead of surfacing mid-run.
`run_ab.py` is **NOT** pin-path, so the smoke half can ship on the
ordinary lane — but shipping it together with the `make_seed.py` screen
in one `do-not-automerge` PR keeps the fix+guard pair reviewable as a
unit (preferred).

## Done-when

- `make_seed.py` rejects/reskins keyword+builtin collisions for every
  generated identifier (seed 424242 generates a valid project), with a
  regression test pinning 424242.
- `run_ab.py prepare` fails fast (before any session) when a generated
  arm's seed suite is red.
- Shipped via a `do-not-automerge` PR (pin-path law).
