"""S7 — `bootstrap.py check --remediate <finding-kind>` paste-ready lookup.

Mirrors the R6 `--explain-wall` test surface: the kind->block registry, the CLI
branch (always exits 0, prints), the unknown-kind listing, and — the S7 guard
rail — a test that the command is print-only and modifies nothing.
"""
from __future__ import annotations

from pathlib import Path

import pytest

mod = pytest.importorskip("engine.checks.check_remediate")
folded = pytest.importorskip("engine.checks.check_folded_gate")
cli = pytest.importorskip("engine.cli")


def test_remediate_returns_block_for_known_kind():
    block = mod.remediate("folded-gate-mtime-picker")
    assert block is not None
    assert block.strip()


def test_remediate_returns_none_for_unknown_kind():
    assert mod.remediate("no-such-finding-kind") is None
    assert mod.remediate("") is None


def test_folded_gate_block_is_the_checker_source_of_truth():
    # single source of truth — imported from check_folded_gate, never duplicated
    assert (
        mod.remediate(folded.FINDING_KIND) == folded.REMEDIATION_SNIPPET
    )


def test_available_kinds_are_sorted_and_all_resolve():
    kinds = mod.available_remediation_kinds()
    assert kinds == tuple(sorted(kinds))
    assert kinds  # non-empty seed set
    for kind in kinds:
        assert mod.remediate(kind) is not None


def test_cmd_check_remediate_prints_and_exits_zero(capsys, tmp_path: Path):
    rc = cli.cmd_check(tmp_path, False, remediate="folded-gate-mtime-picker")
    assert rc == 0
    out = capsys.readouterr().out
    assert "remediate: folded-gate-mtime-picker" in out
    assert "paste-ready" in out


def test_cmd_check_remediate_unknown_lists_kinds_and_exits_zero(
    capsys, tmp_path: Path
):
    rc = cli.cmd_check(tmp_path, False, remediate="bogus-kind")
    assert rc == 0
    out = capsys.readouterr().out
    assert "no remediation registered" in out
    # lists every covered kind so the vocabulary is discoverable
    for kind in mod.available_remediation_kinds():
        assert kind in out


def test_cmd_check_remediate_is_print_only_modifies_nothing(
    capsys, tmp_path: Path
):
    """The S7 guard rail: --remediate is a lookup, never a file-rewriting path.
    Running it against a populated tree must leave every file byte-identical."""
    (tmp_path / "a.md").write_text("original a\n", encoding="utf-8")
    sub = tmp_path / "docs"
    sub.mkdir()
    (sub / "b.md").write_text("original b\n", encoding="utf-8")
    before = {
        p: p.read_bytes() for p in tmp_path.rglob("*") if p.is_file()
    }

    rc = cli.cmd_check(tmp_path, True, remediate="stale-wall")
    assert rc == 0  # a lookup never reds, even under --strict

    after = {
        p: p.read_bytes() for p in tmp_path.rglob("*") if p.is_file()
    }
    assert after == before  # zero files created, deleted, or changed


def test_parser_accepts_remediate():
    parser = cli.build_parser()
    ns = parser.parse_args(["check", "--remediate", "stale-wall"])
    assert ns.remediate == "stale-wall"
