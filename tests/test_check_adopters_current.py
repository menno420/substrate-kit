"""The adopter-registry format gate (EAP §6.3 — the CI half).

The execution-home split under test: `bootstrap currency` fetches live fleet
evidence agent-side (CI cannot auth to sibling repos), so CI's only job is
validating the COMMITTED registry's shape with no network. Static format
findings gate strict RED; the staleness nudge stays advisory — a required CI
check never reds on wall-clock time alone (the check_status_current
doctrine).
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

pytest.importorskip("engine.checks.check_adopters_current")

from engine.checks.check_adopters_current import check_adopters_current
from engine.currency import (
    SELF_REPO,
    RepoCurrency,
    SelfReport,
    render_adopters,
)

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


# --- version-home-move advisory (prev-card Q-0089 idea → guard) -------------


def _write_version_home(root: Path, version: str) -> None:
    (root / "substrate.config.json").write_text(
        json.dumps({"kit_version": version}), encoding="utf-8"
    )


def test_version_home_moved_fires_advisory(tmp_path: Path):
    # The #438 class: registry generated against v1.7.0, version home now
    # bumped to v1.8.0 — freshly generated (young stamp), so `adopters-stale`
    # can't catch it. The version-lag advisory must.
    _write_registry(tmp_path, _generated(NOW))  # stamped kit release: v1.7.0
    _write_version_home(tmp_path, "1.8.0")
    gate, advisory = check_adopters_current(tmp_path, now=NOW)
    assert gate == []  # advisory-only, never a gate
    assert [f.kind for f in advisory] == ["adopters-version-lag"]
    assert "v1.7.0" in advisory[0].message and "v1.8.0" in advisory[0].message


def test_version_home_matches_no_advisory(tmp_path: Path):
    _write_registry(tmp_path, _generated(NOW))  # kit release: v1.7.0
    _write_version_home(tmp_path, "1.7.0")
    _, advisory = check_adopters_current(tmp_path, now=NOW)
    assert advisory == []


def test_no_version_home_fails_open(tmp_path: Path):
    # No substrate.config.json (the existing tests' shape) → no version source
    # → the version-lag check must not fire.
    _write_registry(tmp_path, _generated(NOW))
    _, advisory = check_adopters_current(tmp_path, now=NOW)
    assert [f.kind for f in advisory] == []


def test_unparseable_version_home_fails_open(tmp_path: Path):
    _write_registry(tmp_path, _generated(NOW))
    (tmp_path / "substrate.config.json").write_text("{not json", encoding="utf-8")
    _, advisory = check_adopters_current(tmp_path, now=NOW)
    assert "adopters-version-lag" not in [f.kind for f in advisory]


def test_version_lag_rides_alongside_staleness(tmp_path: Path):
    # An old registry generated against a now-superseded version home fires
    # both advisories independently.
    _write_registry(tmp_path, _generated(OLD))  # old stamp, kit release v1.7.0
    _write_version_home(tmp_path, "1.8.0")
    gate, advisory = check_adopters_current(tmp_path, now=NOW)
    assert gate == []
    kinds = sorted(f.kind for f in advisory)
    assert kinds == ["adopters-stale", "adopters-version-lag"]


# --- self-row staleness GATE (B-2) ------------------------------------------


def _self_registry(version: str, now: datetime = NOW) -> str:
    """A registry whose sole row is the substrate-kit self-row at ``version``."""
    scan = RepoCurrency(
        repo=SELF_REPO,
        tree_version=version,
        tree_source="dist/bootstrap.py",
        config_pin=version,
        reports=[
            SelfReport("control/status.md", version, "green", "yes", found=True)
        ],
    )
    return render_adopters([scan], version, now=now)


def test_self_row_stale_fires_gate(tmp_path: Path):
    # The self-row still stamps v1.7.0 but the version home has moved to
    # v1.8.0 — the self-row is stale and the GATE must RED (self-row scoped).
    _write_registry(tmp_path, _self_registry("1.7.0"))
    _write_version_home(tmp_path, "1.8.0")
    gate, _ = check_adopters_current(tmp_path, now=NOW)
    assert "adopters-self-row-stale" in [f.kind for f in gate]
    finding = next(f for f in gate if f.kind == "adopters-self-row-stale")
    assert "v1.7.0" in finding.message and "v1.8.0" in finding.message


def test_self_row_current_no_gate(tmp_path: Path):
    # Self-row stamped at the current home version — the gate must not fire.
    _write_registry(tmp_path, _self_registry("1.8.0"))
    _write_version_home(tmp_path, "1.8.0")
    gate, _ = check_adopters_current(tmp_path, now=NOW)
    assert "adopters-self-row-stale" not in [f.kind for f in gate]


def test_self_row_gate_ignores_sibling_lag(tmp_path: Path):
    # The self-row is current (v1.8.0 == home); a sibling adopter lags at
    # v1.5.0. Sibling lag must NOT red the self-row-scoped gate.
    self_scan = RepoCurrency(
        repo=SELF_REPO,
        tree_version="1.8.0",
        tree_source="dist/bootstrap.py",
        config_pin="1.8.0",
        reports=[
            SelfReport("control/status.md", "1.8.0", "green", "yes", found=True)
        ],
    )
    sibling = RepoCurrency(
        repo="o/sibling", tree_version="1.5.0", tree_source="bootstrap.py",
        config_pin="1.5.0",
    )
    _write_registry(tmp_path, render_adopters([self_scan, sibling], "1.8.0", now=NOW))
    _write_version_home(tmp_path, "1.8.0")
    gate, _ = check_adopters_current(tmp_path, now=NOW)
    assert "adopters-self-row-stale" not in [f.kind for f in gate]


def test_self_row_gate_tolerates_bump_window_tree_lag(tmp_path: Path):
    # The cut_release bump window: config pin already bumped to v1.8.0 but the
    # dist header (tree cell) still reads v1.7.0. The home version (1.8.0)
    # still appears among the self-row cells, so the gate must NOT false-red.
    self_scan = RepoCurrency(
        repo=SELF_REPO,
        tree_version="1.7.0",  # dist not yet rebuilt
        tree_source="dist/bootstrap.py",
        config_pin="1.8.0",  # just bumped
        reports=[
            SelfReport("control/status.md", "1.8.0", "green", "yes", found=True)
        ],
    )
    _write_registry(tmp_path, render_adopters([self_scan], "1.8.0", now=NOW))
    _write_version_home(tmp_path, "1.8.0")
    gate, _ = check_adopters_current(tmp_path, now=NOW)
    assert "adopters-self-row-stale" not in [f.kind for f in gate]


def test_self_row_gate_fails_open_without_version_home(tmp_path: Path):
    # No substrate.config.json version home → no verdict → gate fails open.
    _write_registry(tmp_path, _self_registry("1.7.0"))
    gate, _ = check_adopters_current(tmp_path, now=NOW)
    assert "adopters-self-row-stale" not in [f.kind for f in gate]


def test_self_row_gate_fails_open_without_self_row(tmp_path: Path):
    # A registry with no substrate-kit self-row (only a sibling) → fail open.
    _write_registry(tmp_path, _generated(NOW))  # repo "o/r", no self-row
    _write_version_home(tmp_path, "1.8.0")
    gate, _ = check_adopters_current(tmp_path, now=NOW)
    assert "adopters-self-row-stale" not in [f.kind for f in gate]
