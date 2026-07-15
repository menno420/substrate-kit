"""Tests for scripts/preflight.py — the kit's own CI-convergence wrapper.

The dogfood half of ORDER 018 (idea-engine ASK 002 / PRs #274/#299, kit
mechanism PR #332): ``_default_preflight_scripts()`` names
``scripts/preflight.py`` and ``_run_preflight_scripts`` runs it on ``check``'s
full lane, so the kit repo planting the file converges the local ritual and
the CI kit-quality job on one leg list. Every test here injects fake legs
(module-level ``CHECKS`` / direct ``run_checks`` calls) — **no test may ever
spawn the real pytest leg from inside pytest** (the recursion the
``SUBSTRATE_KIT_PREFLIGHT`` guard exists to break).
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from engine.cli import _PREFLIGHT_NESTED_ENV

_SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import preflight  # noqa: E402

# The pinned leg set, in run order — mirrors ci.yml's kit-quality job.
PINNED_LEGS = [
    "pytest",
    "dist-byte-pin",
    "ruff",
    "idea-index",
    "retro-index",
    "changelog-structure",
    "program-law",
    "bench-integrity",
]


def _exit(code: int) -> list[str]:
    """A fast, real subprocess command that exits with ``code``."""
    return [sys.executable, "-c", f"raise SystemExit({code})"]


@pytest.fixture(autouse=True)
def _clean_nested_env(monkeypatch):
    """The suite itself may run inside a nested check (env inherited) — every
    test starts from the guard-unset state; the self-skip tests set it back."""
    monkeypatch.delenv(preflight.NESTED_ENV, raising=False)


# --- guard identity -------------------------------------------------------


def test_nested_env_name_matches_cli_guard():
    # The script honors the EXACT marker _run_preflight_scripts stamps on its
    # children — a renamed constant on either side silently unguards the loop.
    assert preflight.NESTED_ENV == _PREFLIGHT_NESTED_ENV == "SUBSTRATE_KIT_PREFLIGHT"


# --- worst-exit aggregation (injected fake legs) --------------------------


def test_all_green_exits_zero(capsys):
    rc = preflight.run_checks([("a", [_exit(0)]), ("b", [_exit(0)])])
    out = capsys.readouterr().out
    assert rc == 0
    assert "PASS — a" in out and "PASS — b" in out
    assert "OK — 2 leg(s) green" in out


def test_one_red_leg_propagates_its_exit(capsys):
    rc = preflight.run_checks([("a", [_exit(0)]), ("b", [_exit(2)])])
    out = capsys.readouterr().out
    assert rc == 2
    assert "FAIL — b (exit 2)" in out
    assert "FAIL — worst exit 2" in out


def test_first_failure_still_runs_the_rest(capsys):
    # Worst-exit, not fail-fast: a red first leg must not shadow later legs.
    rc = preflight.run_checks([("bad", [_exit(1)]), ("good", [_exit(0)])])
    out = capsys.readouterr().out
    assert rc == 1
    assert "FAIL — bad (exit 1)" in out
    assert "PASS — good (exit 0)" in out  # ran despite the earlier failure


def test_multi_command_leg_stops_at_first_nonzero(capsys):
    # A leg is a SEQUENCE (the dist pin is build-then-diff): the first
    # non-zero command is the leg's exit; later commands don't run.
    marker = "never"
    rc = preflight.run_checks(
        [("seq", [_exit(3), [sys.executable, "-c", f"print({marker!r})"]])],
    )
    out = capsys.readouterr().out
    assert rc == 3
    assert marker not in out


def test_uncallable_command_is_exit_two(capsys):
    rc = preflight.run_checks([("ghost", [["/nonexistent-binary-xyz"]])])
    assert rc == 2
    assert "could not run ghost" in capsys.readouterr().err


# --- main(): red-fixture mutation proof through the entry point -----------


def test_main_propagates_failing_leg_exit(monkeypatch, capsys):
    monkeypatch.setattr(preflight, "CHECKS", [("inject-red", [_exit(3)])])
    assert preflight.main([]) == 3
    assert "FAIL — inject-red (exit 3)" in capsys.readouterr().out


def test_main_green_after_fix(monkeypatch, capsys):
    monkeypatch.setattr(preflight, "CHECKS", [("inject-red", [_exit(0)])])
    assert preflight.main([]) == 0
    assert "PASS — inject-red" in capsys.readouterr().out


# --- SUBSTRATE_KIT_PREFLIGHT self-skip -------------------------------------


def test_nested_run_self_skips_exit_zero(monkeypatch, capsys):
    # _run_preflight_scripts invokes the script with the marker SET — a
    # nested run must run NOTHING (the pytest leg would recurse) and pass.
    monkeypatch.setenv(preflight.NESTED_ENV, "1")
    monkeypatch.setattr(preflight, "CHECKS", [("would-red", [_exit(1)])])
    rc = preflight.main([])
    out = capsys.readouterr().out
    assert rc == 0
    assert "nested run" in out and preflight.NESTED_ENV in out
    assert "would-red" not in out  # the failing leg never ran


# --- missing-tool NOTE path (ruff absent) ----------------------------------


def test_ruff_absent_skips_with_note_not_red(monkeypatch, capsys):
    monkeypatch.setattr(preflight, "_ruff_available", lambda: False)
    rc = preflight.run_checks([("ruff", [_exit(1)]), ("other", [_exit(0)])])
    out = capsys.readouterr().out
    assert rc == 0  # the would-red ruff command never ran
    assert "NOTE — ruff skipped" in out
    assert "FAIL" not in out
    assert "OK — 1 leg(s) green" in out  # skipped leg not counted as run


def test_ruff_present_runs_the_leg(monkeypatch, capsys):
    monkeypatch.setattr(preflight, "_ruff_available", lambda: True)
    rc = preflight.run_checks([("ruff", [_exit(0)])])
    out = capsys.readouterr().out
    assert rc == 0
    assert "PASS — ruff" in out and "NOTE" not in out


# --- --list and --only ------------------------------------------------------


def test_list_names_the_pinned_leg_set(capsys):
    assert preflight.main(["--list"]) == 0
    assert capsys.readouterr().out.split() == PINNED_LEGS


def test_list_runs_nothing(monkeypatch):
    monkeypatch.setattr(
        preflight,
        "run_checks",
        lambda *a, **k: pytest.fail("--list must not run legs"),
    )
    assert preflight.main(["--list"]) == 0


def test_only_selects_a_single_leg(monkeypatch, capsys):
    monkeypatch.setattr(
        preflight,
        "CHECKS",
        [("a", [_exit(0)]), ("b", [_exit(4)])],
    )
    assert preflight.main(["--only", "a"]) == 0
    out = capsys.readouterr().out
    assert "PASS — a" in out and "b" not in out


def test_only_unknown_leg_is_exit_two(capsys):
    assert preflight.main(["--only", "nope"]) == 2
    assert "unknown leg" in capsys.readouterr().err


# --- CI-parity pins on the real CHECKS table -------------------------------


def test_checks_table_matches_ci_kit_quality_job():
    names = [name for name, _ in preflight.CHECKS]
    assert names == PINNED_LEGS
    flat = {
        name: [tok for argv in cmds for tok in argv]
        for name, cmds in preflight.CHECKS
    }
    # Exact CI command shapes (ci.yml kit-quality steps):
    assert flat["pytest"][-4:] == ["-m", "pytest", "tests/", "-q"]
    assert flat["dist-byte-pin"] == [
        preflight._PY,
        "src/build_bootstrap.py",
        "git",
        "diff",
        "--exit-code",
        "dist/bootstrap.py",
    ]
    assert flat["ruff"][-4:] == ["-m", "ruff", "check", "src/engine/"]
    # Labels exist only in CI's event context — the local leg must never
    # pass --label-gate (it would false-red every local run).
    assert "--label-gate" not in flat["program-law"]
