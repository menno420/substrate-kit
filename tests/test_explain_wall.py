"""R6 — `bootstrap.py check --explain-wall <phrase>` / `--why` lookup.

Mirrors the false-wall checker's explain surface: the phrase->rule->correction
mapping, the per-rule correction coverage guard, and the cmd_check CLI branch.
"""
from __future__ import annotations

from pathlib import Path

import pytest

mod = pytest.importorskip("engine.checks.check_no_false_walls")
cli = pytest.importorskip("engine.cli")

_FALSE_WALL = "agents cannot merge their own PRs"


def test_explain_wall_matches_a_false_wall():
    result = mod.explain_wall(_FALSE_WALL)
    assert result is not None
    rule, matched, correction = result
    assert rule
    assert matched
    assert correction


def test_explain_wall_returns_none_for_benign_text():
    assert mod.explain_wall("agents merge their own green PRs directly") is None
    assert mod.explain_wall("the weather is nice today") is None


def test_every_rule_has_a_correction():
    assert set(mod.WALL_CORRECTIONS) == set(mod.all_rule_names())


def test_cmd_check_explain_wall_prints_and_exits_zero(capsys, tmp_path: Path):
    rc = cli.cmd_check(tmp_path, False, explain_wall=_FALSE_WALL)
    assert rc == 0
    out = capsys.readouterr().out
    assert "explain-wall" in out
    assert "false-wall:" in out
    assert "CAPABILITIES.md" in out


def test_cmd_check_explain_wall_benign_exits_zero(capsys, tmp_path: Path):
    rc = cli.cmd_check(tmp_path, False, explain_wall="the weather is nice today")
    assert rc == 0
    out = capsys.readouterr().out
    assert "no false-wall rule matched" in out


def test_parser_accepts_explain_wall_and_why_alias():
    parser = cli.build_parser()
    ns = parser.parse_args(["check", "--explain-wall", "foo"])
    assert ns.explain_wall == "foo"
    ns2 = parser.parse_args(["check", "--why", "bar"])
    assert ns2.explain_wall == "bar"
