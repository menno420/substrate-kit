#!/usr/bin/env python3
"""preflight — the kit's own local↔CI convergence wrapper (ORDER 018 dogfood).

Why + provenance: ``config.py::_default_preflight_scripts()`` has defaulted to
``["scripts/preflight.py"]`` since PR #332 shipped the consumption mechanism
(``cmd_check`` → ``_run_preflight_scripts``), but the kit repo itself never
planted the file — so every full ``check`` printed a standing self-skip NOTE
and a local ``check --strict`` ran none of the seven CI kit-quality legs (the
local-green→CI-red class from idea-engine ASK 002 / PRs #274/#299). Added
2026-07-14 (session ``kit-preflight-dogfood``), following idea-engine's
``scripts/preflight.py`` convergence pattern: a ``CHECKS`` list + a worst-exit
runner, one PASS/FAIL line per leg. Reliability (PL-008): UNVERIFIED — confirm
its verdicts against real CI runs a few times across sessions before trusting
it; **delete this if it proves unreliable over multiple sessions.**

The legs mirror ``.github/workflows/ci.yml``'s kit-quality job byte-for-byte
where possible:

1. ``python3 -m pytest tests/ -q``                (§3.2 item 1)
2. ``python3 src/build_bootstrap.py`` then
   ``git diff --exit-code dist/bootstrap.py``     (§3.2 item 2 — dist byte pin)
3. ``python3 -m ruff check src/engine/``          (§3.2 item 3 — skipped with a
   NOTE when ruff is not importable locally; CI always runs it)
4. ``python3 scripts/check_idea_index.py``        (§5.4)
5. ``python3 scripts/check_retro_index.py``       (docs/retro reachability)
6. ``python3 scripts/check_changelog_structure.py``
7. ``python3 scripts/check_taxonomy_sync.py``     (PL-004 three-surface sync)
8. ``python3 scripts/check_program_law.py``       (§8.3 — WITHOUT
   ``--label-gate``: PR labels exist only in CI's event context)
9. ``python3 scripts/check_bench_integrity.py``   (§5.0)

Deliberately excluded: the CI cold-adoption smoke (§3.2 item 4) — shell-heavy
and slow (a scratch adopt + the full RED→ENGAGED→GREEN arc); CI keeps it.

Recursion guard: ``_run_preflight_scripts`` (src/engine/cli.py) invokes this
script with ``SUBSTRATE_KIT_PREFLIGHT=1`` in its environment — the marker it
stamps on its children so a wrapper that re-enters ``check`` cannot loop.
When that variable is set this script exits 0 immediately with a one-line
note: the pytest leg contains tests that invoke ``check``, so a nested run
must never spawn the suite again. The entry point for the legs is a
DIRECT run — ``python3 scripts/preflight.py`` — exactly the idea-engine
convention the config default names.

Usage:
    python3 scripts/preflight.py            # run all legs, worst exit wins
    python3 scripts/preflight.py --list     # print leg names, run nothing
    python3 scripts/preflight.py --only pytest   # run a single leg by name

Exit codes: worst child exit — 0 = all green · non-zero = a leg failed ·
2 = a leg could not run at all (crashed child / unknown ``--only`` name).

Repo-level tooling, not engine code: lives in scripts/, uses print, never
ships in dist/bootstrap.py. Stdlib only.
"""

from __future__ import annotations

import argparse
import importlib.util
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

# The cli-side nested-run marker (src/engine/cli.py::_PREFLIGHT_NESTED_ENV):
# _run_preflight_scripts sets it in THIS script's environment when `check`
# runs the leg, and this script honors it by self-skipping (see docstring).
NESTED_ENV = "SUBSTRATE_KIT_PREFLIGHT"

# The interpreter already running this wrapper — the same both-venues choice
# _run_preflight_scripts makes for *.py entries.
_PY = sys.executable or "python3"

# One entry per CI kit-quality leg: (name, [argv, argv, ...]). A leg is a
# SEQUENCE of commands run in order; its exit is the first non-zero (the
# dist byte pin is build-then-diff, like the workflow step). Module-level on
# purpose: tests inject fake legs here (or call run_checks directly) so the
# suite never spawns the real pytest leg from inside pytest.
CHECKS: list[tuple[str, list[list[str]]]] = [
    ("pytest", [[_PY, "-m", "pytest", "tests/", "-q"]]),
    (
        "dist-byte-pin",
        [
            [_PY, "src/build_bootstrap.py"],
            ["git", "diff", "--exit-code", "dist/bootstrap.py"],
        ],
    ),
    ("ruff", [[_PY, "-m", "ruff", "check", "src/engine/"]]),
    ("idea-index", [[_PY, "scripts/check_idea_index.py"]]),
    ("retro-index", [[_PY, "scripts/check_retro_index.py"]]),
    ("changelog-structure", [[_PY, "scripts/check_changelog_structure.py"]]),
    ("taxonomy-sync", [[_PY, "scripts/check_taxonomy_sync.py"]]),
    ("program-law", [[_PY, "scripts/check_program_law.py"]]),
    ("bench-integrity", [[_PY, "scripts/check_bench_integrity.py"]]),
]


def _ruff_available() -> bool:
    """True when ruff is importable by the interpreter running this wrapper."""
    try:
        return importlib.util.find_spec("ruff") is not None
    except (ImportError, ValueError):
        return False


def run_leg(name: str, commands: list[list[str]], cwd: Path = REPO_ROOT) -> int:
    """Run one leg's command sequence; return its exit (first non-zero wins)."""
    for argv in commands:
        try:
            code = subprocess.run(argv, cwd=cwd).returncode
        except OSError as exc:  # fail loud: a leg that cannot run is not a pass
            print(f"preflight: could not run {name}: {exc}", file=sys.stderr)
            return 2
        if code != 0:
            return code
    return 0


def run_checks(
    checks: list[tuple[str, list[list[str]]]],
    cwd: Path = REPO_ROOT,
) -> int:
    """Run every leg (a failure never stops the rest); return the worst exit."""
    worst = 0
    ran = 0
    for name, commands in checks:
        if name == "ruff" and not _ruff_available():
            print(
                "preflight: NOTE — ruff skipped "
                "(not importable locally; CI always runs this leg)",
            )
            continue
        code = run_leg(name, commands, cwd=cwd)
        verdict = "PASS" if code == 0 else "FAIL"
        print(f"preflight: {verdict} — {name} (exit {code})")
        worst = max(worst, code)
        ran += 1
    if worst == 0:
        print(f"preflight: OK — {ran} leg(s) green")
    else:
        print(f"preflight: FAIL — worst exit {worst}")
    return worst


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--list",
        action="store_true",
        help="print the leg names in run order and exit (runs nothing)",
    )
    parser.add_argument(
        "--only",
        metavar="NAME",
        help="run a single leg by name (see --list)",
    )
    args = parser.parse_args(argv)
    if args.list:
        for name, _ in CHECKS:
            print(name)
        return 0
    if os.environ.get(NESTED_ENV):
        print(
            f"preflight: skipped — nested run ({NESTED_ENV} set; "
            "the outer run owns the legs).",
        )
        return 0
    checks = CHECKS
    if args.only:
        checks = [(n, c) for n, c in CHECKS if n == args.only]
        if not checks:
            known = ", ".join(n for n, _ in CHECKS)
            print(f"preflight: unknown leg {args.only!r} (known: {known})", file=sys.stderr)
            return 2
    return run_checks(checks)


if __name__ == "__main__":
    sys.exit(main())
