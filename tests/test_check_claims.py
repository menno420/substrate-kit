"""The claim-aware checker (inbox ORDER 007).

Order-claims live as ``claimed-by: <ids> <lane> <ISO8601>`` on the
``orders:`` line of a lane's heartbeat (``control/status*.md``); the
convention (control/README.md § Claiming an order) makes every ``new``
order single-executor. These tests pin the checker's posture: advisory-only
(a nudge toward reconciliation, never exit-affecting — the manager
adjudicates the tiebreak), input-gated on the control/ protocol,
per-heartbeat-file, and fail-open on unreadable / claim-less files. They
cover the two findings — ``claims-duplicate`` (two lanes, one order) and
``claims-stale`` (order already done / claim past the ~24h horizon) — plus
the clean and empty paths.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

pytest.importorskip("engine.checks.check_claims")

from engine.checks.check_claims import CLAIM_STALE_HOURS, check_claims
from engine.checks.check_status_current import STATUS_RELPATH
from engine.cli import cmd_check

NOW = datetime(2026, 7, 10, 12, 0, tzinfo=timezone.utc)
FRESH = "2026-07-10T11:00Z"  # 1h before NOW — inside the horizon
STALE = "2026-07-08T00:00Z"  # ~60h before NOW — past the 24h horizon


def _write(root: Path, rel: str, text: str) -> Path:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _status(orders: str) -> str:
    return (
        "# x · status\nupdated: 2026-07-10T11:00Z\nphase: testing\n"
        "health: green\nlast-shipped: none\nblockers: none\n"
        f"orders: {orders}\n⚑ needs-owner: none\nnotes: none\n"
    )


LANES = ["control/status-mining.md", "control/status-exploration.md"]


def _recent() -> str:
    """A claim timestamp ~1h ago in real wall-clock — always inside the
    horizon, so cmd_check integration tests (which use the real ``now``) stay
    green whatever day CI runs them.
    """
    return (datetime.now(timezone.utc) - timedelta(hours=1)).strftime("%Y-%m-%dT%H:%MZ")


# ---------------------------------------------------------------------------
# Input gating + fail-open
# ---------------------------------------------------------------------------


def test_no_control_protocol_no_findings(tmp_path):
    assert check_claims(tmp_path, now=NOW) == []


def test_empty_claims_fail_open_clean(tmp_path):
    # Control protocol present but no claimed-by anywhere → clean.
    _write(tmp_path, STATUS_RELPATH, _status("acked=001,002 done=001"))
    assert check_claims(tmp_path, now=NOW) == []


def test_missing_heartbeat_file_is_not_this_checkers_finding(tmp_path):
    # check_status_current owns status-missing; this checker stays silent.
    _write(tmp_path, "control/inbox.md", "# inbox\n")
    assert check_claims(tmp_path, now=NOW) == []


def test_unreadable_heartbeat_fails_open(tmp_path):
    (tmp_path / STATUS_RELPATH).mkdir(parents=True)
    assert check_claims(tmp_path, now=NOW) == []


def test_no_orders_line_is_clean(tmp_path):
    _write(tmp_path, STATUS_RELPATH, "# x · status\nupdated: 2026-07-10T11:00Z\n")
    assert check_claims(tmp_path, now=NOW) == []


# ---------------------------------------------------------------------------
# The happy path — a single live claim is clean
# ---------------------------------------------------------------------------


def test_single_valid_claim_is_clean(tmp_path):
    _write(
        tmp_path,
        STATUS_RELPATH,
        _status(f"acked=001-008 done=001-006 claimed-by: 007+008 lane-a {FRESH}"),
    )
    assert check_claims(tmp_path, now=NOW) == []


# ---------------------------------------------------------------------------
# DUPLICATE — two distinct lanes claim the same order
# ---------------------------------------------------------------------------


def test_two_lanes_one_order_flags_duplicate(tmp_path):
    _write(tmp_path, LANES[0], _status(f"acked=007 done= claimed-by: 007 lane-a {FRESH}"))
    _write(tmp_path, LANES[1], _status(f"acked=007 done= claimed-by: 007 lane-b {FRESH}"))
    findings = check_claims(tmp_path, status_files=LANES, now=NOW)
    kinds = [f.kind for f in findings]
    assert kinds == ["claims-duplicate", "claims-duplicate"]
    # One finding on each colliding lane, both naming order 007.
    assert {f.path for f in findings} == set(LANES)
    for f in findings:
        assert "order 007" in f.message
        assert "lane-a" in f.message and "lane-b" in f.message


def test_distinct_orders_across_lanes_are_clean(tmp_path):
    _write(tmp_path, LANES[0], _status(f"acked=007 done= claimed-by: 007 lane-a {FRESH}"))
    _write(tmp_path, LANES[1], _status(f"acked=008 done= claimed-by: 008 lane-b {FRESH}"))
    assert check_claims(tmp_path, status_files=LANES, now=NOW) == []


# ---------------------------------------------------------------------------
# STALE — claim on a done order, or one past the ~24h horizon
# ---------------------------------------------------------------------------


def test_claim_on_done_order_flags_stale(tmp_path):
    # Order 005 is claimed here but already reported done → dead claim.
    _write(
        tmp_path,
        STATUS_RELPATH,
        _status(f"acked=001-005 done=005 claimed-by: 005 lane-a {FRESH}"),
    )
    findings = check_claims(tmp_path, now=NOW)
    assert [f.kind for f in findings] == ["claims-stale"]
    assert "005" in findings[0].message and "done=" in findings[0].message


def test_claim_done_in_a_sibling_lane_flags_stale(tmp_path):
    # A claim retires the moment ANY lane reports the order done.
    _write(tmp_path, LANES[0], _status(f"acked=009 done= claimed-by: 009 lane-a {FRESH}"))
    _write(tmp_path, LANES[1], _status("acked=009 done=009"))
    findings = check_claims(tmp_path, status_files=LANES, now=NOW)
    assert [f.kind for f in findings] == ["claims-stale"]
    assert findings[0].path == LANES[0]


def test_claim_past_horizon_flags_stale(tmp_path):
    _write(
        tmp_path,
        STATUS_RELPATH,
        _status(f"acked=001-007 done=001-006 claimed-by: 007 lane-a {STALE}"),
    )
    findings = check_claims(tmp_path, now=NOW)
    assert [f.kind for f in findings] == ["claims-stale"]
    assert "abandonment horizon" in findings[0].message


def test_claim_inside_horizon_is_clean(tmp_path):
    _write(
        tmp_path,
        STATUS_RELPATH,
        _status(f"acked=001-007 done=001-006 claimed-by: 007 lane-a {FRESH}"),
    )
    assert check_claims(tmp_path, now=NOW) == []


def test_unparseable_timestamp_skips_age_check(tmp_path):
    # A malformed ts must not fabricate staleness (no age finding); the claim
    # is otherwise fine (not done, not duplicate) → clean.
    _write(
        tmp_path,
        STATUS_RELPATH,
        _status("acked=001-007 done=001-006 claimed-by: 007 lane-a not-a-date"),
    )
    assert check_claims(tmp_path, now=NOW) == []


def test_default_now_uses_wall_clock(tmp_path):
    # No `now` passed → a fresh claim (moments ago) is inside the horizon.
    recent = (datetime.now(timezone.utc) - timedelta(hours=1)).strftime(
        "%Y-%m-%dT%H:%MZ"
    )
    _write(tmp_path, STATUS_RELPATH, _status(f"acked=007 done= claimed-by: 007 lane-a {recent}"))
    assert check_claims(tmp_path) == []
    assert CLAIM_STALE_HOURS == 24


# ---------------------------------------------------------------------------
# cmd_check integration — advisory NEVER touches the exit code
# ---------------------------------------------------------------------------


def test_cmd_check_strict_stays_green_on_duplicate(tmp_path, capsys):
    recent = _recent()
    _write(tmp_path, LANES[0], _status(f"acked=007 done= claimed-by: 007 lane-a {recent}"))
    _write(tmp_path, LANES[1], _status(f"acked=007 done= claimed-by: 007 lane-b {recent}"))
    # Point the config at both heartbeat files (ORDER 004 configurable set).
    (tmp_path / "substrate.config.json").write_text(
        '{"heartbeat_files": ["control/status-mining.md", '
        '"control/status-exploration.md"]}',
        encoding="utf-8",
    )
    assert cmd_check(tmp_path, strict=True) == 0
    out = capsys.readouterr().out
    assert "claims-duplicate" in out
    assert "never exit-affecting" in out


def test_cmd_check_status_only_lane_also_warns(tmp_path, capsys):
    # Claims live in the heartbeat files the control fast lane validates, so
    # the nag rides both lanes.
    _write(
        tmp_path,
        STATUS_RELPATH,
        _status("acked=001-005 done=005 claimed-by: 005 lane-a 2026-07-10T11:00Z"),
    )
    assert cmd_check(tmp_path, strict=True, status_only=True) == 0
    assert "claims-stale" in capsys.readouterr().out


def test_cmd_check_quiet_when_claims_clean(tmp_path, capsys):
    _write(
        tmp_path,
        STATUS_RELPATH,
        _status(f"acked=001-006 done=001-006 claimed-by: 007 lane-a {_recent()}"),
    )
    assert cmd_check(tmp_path, strict=True) == 0
    out = capsys.readouterr().out
    assert "claims-duplicate" not in out and "claims-stale" not in out
