---
state: promoted
origin: lab
shipped_pr: 354
shipped_repo: menno420/substrate-kit
merged_date: 2026-07-14
outcome: shipped
---

# Kit-side `scripts/preflight.py` — CI-convergence dogfood (2026-07-14)

> **Status:** `ideas`
>
> **State:** captured (SELECT phase 2026-07-14 — friction observable live at
> HEAD a67ccda: the standing "preflight script scripts/preflight.py not
> found" NOTE on every full `check`) → **shipped** same session (kit PR
> #354: the wrapper + 16 tests + CHANGELOG; merged_date is the anticipated
> date per the #349/#351/#352 in-PR flip convention).

## The idea

`config.py::_default_preflight_scripts()` has defaulted to
`["scripts/preflight.py"]` since PR #332 shipped the consumption mechanism
(`cmd_check` → `_run_preflight_scripts`), but the kit repo itself never
planted the file. Consequences, both live at HEAD: every full `check` prints
a standing self-skip NOTE, and a local `check --strict` runs **none** of the
seven CI kit-quality legs — the exact local-green→CI-red class the mechanism
was built to close (idea-engine ASK 002 / PRs #274/#299). Plant the
conventional wrapper in the kit itself: a stdlib-only `CHECKS` table of the
seven ci.yml kit-quality legs + a worst-exit runner (the idea-engine
pattern), honoring the `SUBSTRATE_KIT_PREFLIGHT` nested-run marker by
self-skipping exit-0 so the pytest leg's check-invoking tests can never
recurse.

## Why it is worth having

The kit ships a convergence mechanism it does not use — the one repo where
the "plant one to converge the local ritual and the CI gate on one check
list" NOTE fires on every run is the repo that wrote the NOTE. Dogfooding it
(a) retires the standing NOTE, (b) gives kit sessions a one-command local
mirror of the CI kit-quality job before push, and (c) exercises the #332
mechanism end-to-end in-repo, where a semantics regression (env-marker
rename, arg-splitting change) would surface immediately.

## Shipped

Kit PR #354 (2026-07-14): `scripts/preflight.py` (seven legs — pytest ·
dist byte-pin · ruff with a skip-NOTE when not importable · idea index ·
changelog structure · program law WITHOUT `--label-gate`, labels being
CI-only · bench integrity; `--list` / `--only`; nested-run self-skip) +
`tests/test_kit_preflight.py` (16 tests: worst-exit aggregation with
injected fake legs, first-fails-still-runs-rest, the self-skip path, the
ruff-absent NOTE path, `--list`/`--only`, guard-name identity with
`cli._PREFLIGHT_NESTED_ENV`, and CI-command-shape pins). The CI
cold-adoption smoke leg is deliberately excluded (shell-heavy/slow; CI
keeps it). No engine change, no dist regen, no adopter surface.
