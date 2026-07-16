# Session — model-line card conformance (clear standing self-advisory)

> **Status:** `complete`

- **📊 Model:** opus-4.8 · medium · docs-only

⚑ Self-initiated: relabelled the prior session card's `📊 Model:` task-class to a conforming PL-004 class, clearing the sole live `model-line-class` advisory on the kit's own `check --strict`. Proposed as a DRAFT PR for human review (auto-merge intentionally not armed).

## What shipped
Relabelled the `📊 Model:` task-class on `.sessions/2026-07-16-valueless-badge-check-log.md` from `gate-integrity build …` to `feature build (gate-integrity: kit-quality gate source, check_log lane)`, so it prefix-matches the PL-004 `feature build` class (PL-010: building a new checker is a feature build). Model + effort + descriptive detail preserved; only the class label conformed. Docs-only; no engine/dist change.

Not built this session — the coordinator-relayed slice (an adopters-staleness `check --strict` advisory) is a verified DUPLICATE: `src/engine/checks/check_adopters_current.py:45` already emits an advisory-only `adopters-stale` finding (`DEFAULT_MAX_AGE_DAYS = 14`, never exit-affecting, 7 passing tests). The only delta wanted (a ~26h threshold) is coupled to the parked kit-lab daily-cron A/B (recreate vs retire) — building it now would bake in the "daily cadence" branch and emit a standing nag. Flagged, not shipped.

## Verify
- `python3 dist/bootstrap.py check --strict` → passes; `model-line-class` advisory gone (staged-regen-lag + enforcement-required NOTE remain, pre-existing/advisory-only)
- `python3 -m pytest -q` → full suite green

## 💡 Session idea
The kit's OWN staged `.substrate/` tree can silently lag: `.substrate/state.json` slots (`architecture_layers`, `mutation_seam`, `ownership_model`, `owner_profile`) are filled but their staged renders still carry `${…}` tokens (unrendered since #381) — the doctrine-shipping repo ships a lagging staged tree, relying on a session remembering to run `bootstrap upgrade`. Idea: a CI/`check` guard that a fresh render of `.substrate/` matches the committed staged tree (byte-diff, like dist byte-pinning), so consumer #0 can never ship a stale staged pack. "Enforce, don't exhort" (PL-007). (dedup-grep docs/ideas/ before filing.)

## ⟲ Previous-session review
#430 cleanly regenerated `docs/adopters.md` from live discovery. One miss it inherited from #429: the valueless-badge check_log session shipped its own card with a `📊 Model:` task-class the kit's own grammar rejects — a gate-authoring session tripping an adjacent gate. System improvement it surfaces: the `model-line-class` advisory only scans the 10 newest completed cards, so this drift would have aged out unfixed in ~10 sessions (124/178 historical cards already drifted per the checker's own docstring) — the guard catches recent drift but silently forgives the tail. Worth considering a born-conforming card template (task-class picked from the 9-class enum at authoring time) over post-hoc lint.
