"""The control-protocol status-freshness checker (band KL-8, ORDER 002).

The fleet coordination protocol's heartbeat rule: `control/status.md` is how
the manager knows a Project is alive — stale = dark. These tests pin the two
postures: static protocol states (missing / heartbeat-less status) gate
strict RED like every checker, while wall-clock staleness stays advisory —
surfaced and telemetry-recorded but never exit-affecting, so a required CI
check can never red on time alone.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest

pytest.importorskip("engine.checks.check_status_current")

from engine.checks.check_status_current import (
    STATUS_RELPATH,
    check_status_current,
    heartbeat_relpaths,
    parse_heartbeat,
)
from engine.cli import cmd_check

NOW = datetime(2026, 7, 9, 12, 0, tzinfo=timezone.utc)


def _write(root: Path, rel: str, text: str) -> Path:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _status(updated: str) -> str:
    return (
        f"# x · status\nupdated: {updated}\nphase: testing\nhealth: green\n"
        "last-shipped: none\nblockers: none\norders: acked= done=\n"
        "⚑ needs-owner: none\nnotes: none\n"
    )


# ---------------------------------------------------------------------------
# parse_heartbeat — the contract's ISO-8601 shapes
# ---------------------------------------------------------------------------


def test_parse_heartbeat_accepts_z_suffix_and_minutes_precision():
    ts = parse_heartbeat("updated: 2026-07-09T12:07Z\n")
    assert ts == datetime(2026, 7, 9, 12, 7, tzinfo=timezone.utc)


def test_parse_heartbeat_accepts_offset_and_seconds():
    ts = parse_heartbeat("# head\nupdated: 2026-07-09T14:07:30+02:00\n")
    assert ts == datetime(2026, 7, 9, 12, 7, 30, tzinfo=timezone.utc)


def test_parse_heartbeat_naive_is_taken_as_utc():
    ts = parse_heartbeat("updated: 2026-07-09T12:07:00\n")
    assert ts is not None and ts.tzinfo is not None
    assert ts == datetime(2026, 7, 9, 12, 7, tzinfo=timezone.utc)


def test_parse_heartbeat_accepts_case_variant_prefix():
    # kit #326: a live heartbeat wrote `Updated:` and went red on
    # [status-no-heartbeat] — a casing slip is a writer spelling variant,
    # not a dead heartbeat. The prefix match is case-insensitive; the
    # canonical writer form stays lowercase (pinned in test_grammar.py).
    ts = parse_heartbeat("Updated: 2026-07-09T12:07Z\n")
    assert ts == datetime(2026, 7, 9, 12, 7, tzinfo=timezone.utc)
    ts = parse_heartbeat("UPDATED: 2026-07-09T12:07:00+00:00\n")
    assert ts == datetime(2026, 7, 9, 12, 7, tzinfo=timezone.utc)


def test_parse_heartbeat_rejects_seed_prose_and_garbage():
    assert parse_heartbeat("updated: (seeded at adopt — overwrite me)\n") is None
    assert parse_heartbeat("updated: not-a-date\n") is None
    assert parse_heartbeat("phase: no updated line at all\n") is None
    # `updated:` must start the line — prose mentions never count.
    assert parse_heartbeat("the field updated: 2026-07-09T12:07Z inline\n") is None


# ---------------------------------------------------------------------------
# check_status_current — gate vs advisory split
# ---------------------------------------------------------------------------


def test_no_control_dir_yields_nothing(tmp_path):
    gate, advisory = check_status_current(tmp_path, now=NOW)
    assert gate == [] and advisory == []


def test_inbox_without_status_is_a_gate_finding(tmp_path):
    _write(tmp_path, "control/inbox.md", "# inbox\n")
    gate, advisory = check_status_current(tmp_path, now=NOW)
    assert [f.kind for f in gate] == ["status-missing"]
    assert advisory == []


def test_seed_status_has_no_heartbeat_and_gates_red(tmp_path):
    _write(
        tmp_path,
        STATUS_RELPATH,
        _status("(seeded at adopt — no real heartbeat yet)"),
    )
    gate, advisory = check_status_current(tmp_path, now=NOW)
    assert [f.kind for f in gate] == ["status-no-heartbeat"]
    assert advisory == []


def test_fresh_heartbeat_is_clean(tmp_path):
    _write(tmp_path, STATUS_RELPATH, _status("2026-07-09T10:00Z"))
    gate, advisory = check_status_current(tmp_path, now=NOW)
    assert gate == [] and advisory == []


def test_fresh_capitalized_heartbeat_is_clean_too(tmp_path):
    # The gate-level twin of the parse_heartbeat casing pin: a heartbeat
    # differing only in prefix casing must not red [status-no-heartbeat]
    # (kit #326's exact failure).
    _write(
        tmp_path,
        STATUS_RELPATH,
        _status("2026-07-09T10:00Z").replace("updated:", "Updated:", 1),
    )
    gate, advisory = check_status_current(tmp_path, now=NOW)
    assert gate == [] and advisory == []


def test_stale_heartbeat_is_advisory_only(tmp_path):
    _write(tmp_path, STATUS_RELPATH, _status("2026-07-01T10:00Z"))
    gate, advisory = check_status_current(tmp_path, now=NOW)
    assert gate == []
    assert [f.kind for f in advisory] == ["status-stale"]
    assert "DARK" in advisory[0].message


def test_max_age_boundary_is_inclusive(tmp_path):
    # Exactly max_age old is NOT yet stale (> not >=).
    _write(tmp_path, STATUS_RELPATH, _status("2026-07-06T12:00Z"))
    gate, advisory = check_status_current(tmp_path, now=NOW, max_age_hours=72)
    assert gate == [] and advisory == []


# ---------------------------------------------------------------------------
# cmd_check integration — gate reds strict; advisory never touches the exit
# ---------------------------------------------------------------------------


def test_cmd_check_strict_reds_on_seed_status(tmp_path, capsys):
    _write(tmp_path, STATUS_RELPATH, _status("(seeded at adopt)"))
    assert cmd_check(tmp_path, strict=True) == 1
    assert "status-no-heartbeat" in capsys.readouterr().out


def test_cmd_check_strict_stays_green_on_stale_heartbeat(tmp_path, capsys):
    # Wall-clock staleness warns loudly but never exit-affects: a required CI
    # check must not red just because time passed (the time-bomb this split
    # exists to prevent).
    _write(tmp_path, STATUS_RELPATH, _status("2020-01-01T00:00Z"))
    assert cmd_check(tmp_path, strict=True) == 0
    out = capsys.readouterr().out
    assert "status-stale" in out
    assert "never exit-affecting" in out


def test_cmd_check_strict_green_on_fresh_heartbeat(tmp_path):
    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    _write(tmp_path, STATUS_RELPATH, _status(now_iso))
    assert cmd_check(tmp_path, strict=True) == 0
# ---------------------------------------------------------------------------
# Configurable heartbeat paths (ORDER 004 — multi-Project / per-lane repos)
# ---------------------------------------------------------------------------

LANES = ["control/status-mining.md", "control/status-exploration.md"]


def test_heartbeat_relpaths_unset_or_empty_falls_back_to_default():
    # A stray `"heartbeat_files": []` must never silently disable the gate.
    assert heartbeat_relpaths(None) == [STATUS_RELPATH]
    assert heartbeat_relpaths([]) == [STATUS_RELPATH]
    assert heartbeat_relpaths(["", "  "]) == [STATUS_RELPATH]
    assert heartbeat_relpaths(LANES) == LANES


def test_multi_lane_missing_file_gates_per_lane(tmp_path):
    # One lane wrote its heartbeat; the other lane's file doesn't exist yet —
    # exactly one status-missing finding, naming the missing lane's path.
    _write(tmp_path, LANES[0], _status("2026-07-09T10:00Z"))
    gate, advisory = check_status_current(tmp_path, now=NOW, status_files=LANES)
    assert [(f.kind, f.path) for f in gate] == [("status-missing", LANES[1])]
    assert advisory == []


def test_multi_lane_all_fresh_is_clean_and_default_file_not_required(tmp_path):
    # Both lanes beat; the classic control/status.md is absent and NOT
    # demanded — the configured list replaces the default, not adds to it.
    for lane in LANES:
        _write(tmp_path, lane, _status("2026-07-09T10:00Z"))
    gate, advisory = check_status_current(tmp_path, now=NOW, status_files=LANES)
    assert gate == [] and advisory == []


def test_multi_lane_stale_advisory_names_its_lane(tmp_path):
    _write(tmp_path, LANES[0], _status("2026-07-01T10:00Z"))  # stale
    _write(tmp_path, LANES[1], _status("2026-07-09T10:00Z"))  # fresh
    gate, advisory = check_status_current(tmp_path, now=NOW, status_files=LANES)
    assert gate == []
    assert [(f.kind, f.path) for f in advisory] == [("status-stale", LANES[0])]
    assert LANES[0] in advisory[0].message


def test_multi_lane_seed_lane_gates_red_with_its_own_path(tmp_path):
    _write(tmp_path, LANES[0], _status("2026-07-09T10:00Z"))
    _write(tmp_path, LANES[1], _status("(seeded at adopt)"))
    gate, advisory = check_status_current(tmp_path, now=NOW, status_files=LANES)
    assert [(f.kind, f.path) for f in gate] == [("status-no-heartbeat", LANES[1])]
    assert advisory == []


def test_cmd_check_reads_heartbeat_files_from_config(tmp_path, capsys):
    # The host's substrate.config.json heartbeat_files list is what cmd_check
    # gates on: a seed-prose lane reds strict even though control/status.md
    # doesn't exist, and the finding names the lane file.
    from engine.lib.config import Config, save_config

    config = Config(heartbeat_files=list(LANES))
    save_config(tmp_path, config)
    _write(tmp_path, LANES[0], _status("2026-07-09T10:00Z"))
    _write(tmp_path, LANES[1], _status("(seeded at adopt)"))
    assert cmd_check(tmp_path, strict=True) == 1
    out = capsys.readouterr().out
    assert "status-no-heartbeat" in out
    assert LANES[1] in out
