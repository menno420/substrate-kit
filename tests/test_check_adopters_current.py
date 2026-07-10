"""The adopter-registry format gate (EAP §6.3 — the CI half).

The execution-home split under test: `bootstrap currency` fetches live fleet
evidence agent-side (CI cannot auth to sibling repos), so CI's only job is
validating the COMMITTED registry's shape with no network. Static format
findings gate strict RED; the staleness nudge stays advisory — a required CI
check never reds on wall-clock time alone (the check_status_current
doctrine).
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest

pytest.importorskip("engine.checks.check_adopters_current")

from engine.checks.check_adopters_current import check_adopters_current
from engine.currency import RepoCurrency, render_adopters

NOW = datetime(2026, 7, 10, 18, 0, tzinfo=timezone.utc)
OLD = datetime(2026, 6, 1, 0, 0, tzinfo=timezone.utc)


def _write_registry(root: Path, text: str) -> Path:
    path = root / "docs" / "adopters.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _generated(now: datetime) -> str:
    scan = RepoCurrency(repo="o/r", tree_version="1.7.0", tree_source="bootstrap.py")
    return render_adopters([scan], "1.7.0", now=now)


def test_absent_registry_is_silent(tmp_path: Path):
    # Adopter repos never carry the registry — the checker must not engage.
    assert check_adopters_current(tmp_path) == ([], [])


def test_generated_registry_passes(tmp_path: Path):
    _write_registry(tmp_path, _generated(NOW))
    gate, advisory = check_adopters_current(tmp_path, now=NOW)
    assert gate == []
    assert advisory == []


def test_missing_marker_is_a_gate_finding(tmp_path: Path):
    # The pre-§6.3 hand-written ledger shape: no GENERATED marker.
    _write_registry(tmp_path, "# Fleet adopter registry\n\n| repo |\n|---|\n| x |\n")
    gate, advisory = check_adopters_current(tmp_path, now=NOW)
    assert [f.kind for f in gate] == ["adopters-not-generated"]
    assert advisory == []


def test_missing_stamp_is_a_gate_finding(tmp_path: Path):
    text = _generated(NOW).replace("> Generated:", "> Was-generated:")
    _write_registry(tmp_path, text)
    gate, _ = check_adopters_current(tmp_path, now=NOW)
    assert "adopters-no-timestamp" in [f.kind for f in gate]


def test_unparseable_table_is_a_gate_finding(tmp_path: Path):
    text = _generated(NOW).replace("## Registry", "## Rows")
    _write_registry(tmp_path, text)
    gate, _ = check_adopters_current(tmp_path, now=NOW)
    assert "adopters-table-unparseable" in [f.kind for f in gate]


def test_stale_stamp_is_advisory_only_never_gate(tmp_path: Path):
    _write_registry(tmp_path, _generated(OLD))
    gate, advisory = check_adopters_current(tmp_path, now=NOW)
    assert gate == []
    assert [f.kind for f in advisory] == ["adopters-stale"]


def test_fresh_stamp_has_no_staleness_advisory(tmp_path: Path):
    _write_registry(tmp_path, _generated(NOW))
    _, advisory = check_adopters_current(tmp_path, now=NOW, max_age_days=14)
    assert advisory == []
