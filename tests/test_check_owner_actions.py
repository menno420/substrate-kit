"""The owner-action quality checker (inbox ORDER 008).

Agents' ⚑ needs-owner asks must be actionable by a non-technical owner:
every ask carries the six OWNER-ACTION fields (WHAT / WHERE / HOW /
WHY-IT-MATTERS / UNBLOCKS / VERIFIED-NEEDED — attempted-or-exact-wall).
These tests pin the checker's posture: advisory-only (a nag toward the
format, never exit-affecting — existing adopters carry free-text asks
today), input-gated on the control/ protocol, per-heartbeat-file, and
fail-open on unreadable files.
"""

from __future__ import annotations

from pathlib import Path

import pytest

pytest.importorskip("engine.checks.check_owner_actions")

from engine.checks.check_owner_actions import (
    OWNER_ACTION_FIELDS,
    check_owner_actions,
)
from engine.checks.check_status_current import STATUS_RELPATH
from engine.cli import cmd_check


def _write(root: Path, rel: str, text: str) -> Path:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _status(needs_owner: str, extra: str = "") -> str:
    return (
        "# x · status\nupdated: 2026-07-09T12:00Z\nphase: testing\n"
        "health: green\nlast-shipped: none\nblockers: none\n"
        f"orders: acked= done=\n⚑ needs-owner: {needs_owner}\nnotes: none\n"
        f"{extra}"
    )


STRUCTURED_BLOCK = (
    "\n⚑ OWNER-ACTION\nWHAT: merge PR 7.\n"
    "WHERE: https://example.test/pr/7\nHOW: click Merge.\n"
    "WHY-IT-MATTERS: unblocks the release.\nUNBLOCKS: the v2 cut.\n"
    "VERIFIED-NEEDED: I attempted the merge and got 403 (exact error).\n"
)


# ---------------------------------------------------------------------------
# Input gating + the none fast-path
# ---------------------------------------------------------------------------


def test_no_control_protocol_no_findings(tmp_path):
    assert check_owner_actions(tmp_path) == []


def test_needs_owner_none_is_clean(tmp_path):
    _write(tmp_path, STATUS_RELPATH, _status("none"))
    assert check_owner_actions(tmp_path) == []


def test_missing_needs_owner_line_is_clean(tmp_path):
    # No ⚑ line at all: nothing was routed to the owner — nothing to grade.
    _write(tmp_path, STATUS_RELPATH, "# x · status\nupdated: 2026-07-09T12:00Z\n")
    assert check_owner_actions(tmp_path) == []


def test_missing_heartbeat_file_is_not_this_checkers_finding(tmp_path):
    # check_status_current owns status-missing; this checker stays silent.
    _write(tmp_path, "control/inbox.md", "# inbox\n")
    assert check_owner_actions(tmp_path) == []


# ---------------------------------------------------------------------------
# The advisory — unstructured asks name their missing fields
# ---------------------------------------------------------------------------


def test_unstructured_ask_names_every_missing_field(tmp_path):
    _write(tmp_path, STATUS_RELPATH, _status("please merge PR 7 (one click)"))
    findings = check_owner_actions(tmp_path)
    assert [f.kind for f in findings] == ["owner-action-fields"]
    assert findings[0].path == STATUS_RELPATH
    for alts in OWNER_ACTION_FIELDS:
        assert alts[0].rstrip(":") in findings[0].message
    assert "assumption-based asks are banned" in findings[0].message


def test_partially_structured_ask_names_only_the_absent_fields(tmp_path):
    extra = "\nWHAT: merge PR 7.\nWHERE: https://example.test/pr/7\n"
    _write(tmp_path, STATUS_RELPATH, _status("merge PR 7", extra))
    findings = check_owner_actions(tmp_path)
    assert len(findings) == 1
    message = findings[0].message
    assert "WHAT," not in message and "WHERE," not in message
    for field in ("HOW", "WHY-IT-MATTERS", "UNBLOCKS", "VERIFIED-NEEDED"):
        assert field in message


def test_fully_structured_ask_is_clean(tmp_path):
    _write(tmp_path, STATUS_RELPATH, _status("merge PR 7 — see block below", STRUCTURED_BLOCK))
    assert check_owner_actions(tmp_path) == []


# ---------------------------------------------------------------------------
# Token agreement — checker labels match the shipped templates, and the
# shorthand spellings adopters write inline are accepted too (ITEM 1).
# ---------------------------------------------------------------------------

SHORTHAND_BLOCK = (
    "\n⚑ OWNER-ACTION\nWHAT: merge PR 7.\n"
    "WHERE: https://example.test/pr/7\nHOW: click Merge.\n"
    "WHY: unblocks the release.\nUNBLOCKS: the v2 cut.\n"
    "VERIFIED-WHEN: I attempted the merge and got 403 (exact error).\n"
)


def test_shorthand_why_verified_spellings_are_accepted(tmp_path):
    # Adopters sometimes write the shorthand WHY / VERIFIED-WHEN inline; the
    # checker accepts both those and the canonical WHY-IT-MATTERS /
    # VERIFIED-NEEDED, so a complete ask never trips the advisory.
    _write(tmp_path, STATUS_RELPATH, _status("merge PR 7", SHORTHAND_BLOCK))
    assert check_owner_actions(tmp_path) == []


def test_checker_canonical_labels_match_the_shipped_template():
    # The checker's canonical labels and the OWNER-ACTION format block in the
    # shipped control-README template MUST be the same tokens — checker and
    # templates agree.
    tmpl = (
        Path(__file__).resolve().parents[1]
        / "src"
        / "engine"
        / "templates"
        / "control-README.md.tmpl"
    ).read_text(encoding="utf-8")
    for alts in OWNER_ACTION_FIELDS:
        canonical = alts[0]
        assert canonical in tmpl, f"{canonical} missing from control-README template"


# ---------------------------------------------------------------------------
# Multi-lane heartbeats (the ORDER 004 configurable path set)
# ---------------------------------------------------------------------------

LANES = ["control/status-mining.md", "control/status-exploration.md"]


def test_multi_lane_only_the_unstructured_lane_fires(tmp_path):
    _write(tmp_path, LANES[0], _status("merge PR 7"))
    _write(tmp_path, LANES[1], _status("do X", STRUCTURED_BLOCK))
    findings = check_owner_actions(tmp_path, status_files=LANES)
    assert [(f.kind, f.path) for f in findings] == [
        ("owner-action-fields", LANES[0]),
    ]


# ---------------------------------------------------------------------------
# Fail-open
# ---------------------------------------------------------------------------


def test_unreadable_heartbeat_fails_open(tmp_path):
    # A directory at the status path raises OSError on read_text — the
    # checker must treat it as no-verdict, not crash or fire.
    (tmp_path / STATUS_RELPATH).mkdir(parents=True)
    assert check_owner_actions(tmp_path) == []


# ---------------------------------------------------------------------------
# cmd_check integration — advisory NEVER touches the exit code
# ---------------------------------------------------------------------------


def test_cmd_check_strict_stays_green_on_unstructured_ask(tmp_path, capsys):
    _write(tmp_path, STATUS_RELPATH, _status("merge PR 7 (one click)"))
    assert cmd_check(tmp_path, strict=True) == 0
    out = capsys.readouterr().out
    assert "owner-action-fields" in out
    assert "never exit-affecting" in out


def test_cmd_check_status_only_lane_also_warns(tmp_path, capsys):
    # The asks live in the heartbeat files the control fast lane validates,
    # so the nag rides both lanes.
    _write(tmp_path, STATUS_RELPATH, _status("merge PR 7 (one click)"))
    assert cmd_check(tmp_path, strict=True, status_only=True) == 0
    assert "owner-action-fields" in capsys.readouterr().out


def test_cmd_check_quiet_when_asks_are_structured(tmp_path, capsys):
    _write(tmp_path, STATUS_RELPATH, _status("merge PR 7", STRUCTURED_BLOCK))
    assert cmd_check(tmp_path, strict=True) == 0
    assert "owner-action-fields" not in capsys.readouterr().out
