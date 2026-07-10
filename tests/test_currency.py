"""The fleet kit-currency scanner (EAP program review §6.3).

Nothing owned the fleet's version spread before this band: docs/adopters.md
was a hand-written ledger, and a repo's *claim* about its kit version was
never checked against what its tree vendors. These tests pin the module's
contracts: tree truth beats self-report, disagreement is a loud DRIFT (never
silently resolved), a repo with no kit artifact is "not adopted / unknown"
(not an error), and every parse/render path runs with a dict-backed fetcher
— no network.
"""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

pytest.importorskip("engine.currency")

from engine.currency import (
    GENERATED_MARKER,
    GENERATED_STAMP_PREFIX,
    RepoCurrency,
    SelfReport,
    drift_report_lines,
    parse_kit_line,
    parse_roster,
    render_adopters,
    scan_fleet,
    scan_repo,
)

NOW = datetime(2026, 7, 10, 18, 0, tzinfo=timezone.utc)

DIST_HEADER = '"""substrate-kit bootstrap v1.6.0 — GENERATED, DO NOT EDIT.\n\nbody\n"""\n'
STATUS_OK = (
    "# x · status\nupdated: 2026-07-10T12:00Z\n"
    "kit: v1.6.0 · check: green · engaged: yes\n"
)
STATUS_DRIFTED = (
    "# x · status\nupdated: 2026-07-10T12:00Z\n"
    "kit: v1.2.0 · check: green · engaged: yes\n"
)
CONFIG_16 = '{"kit_version": "1.6.0"}'


def _fetcher(files: dict[tuple[str, str], str]):
    """Dict-backed fetcher seam: missing key = 404 = None."""

    def fetch(repo: str, path: str) -> str | None:
        return files.get((repo, path))

    return fetch


# ---------------------------------------------------------------------------
# parse_kit_line — the planted heartbeat convention, leniently
# ---------------------------------------------------------------------------


def test_parse_kit_line_canonical_form():
    version, check, engaged = parse_kit_line(STATUS_OK)
    assert (version, check, engaged) == ("1.6.0", "green", "yes")


def test_parse_kit_line_decorated_line_still_parses():
    # The kit repo's own heartbeat decorates the line with extra prose.
    text = "kit: v1.7.0 released · KIT_VERSION 1.7.0 · tag v1.7.0 live · check: green · engaged: yes\n"
    version, check, engaged = parse_kit_line(text)
    assert (version, check, engaged) == ("1.7.0", "green", "yes")


def test_parse_kit_line_absent_returns_nones():
    assert parse_kit_line("# status\nupdated: 2026-07-10T12:00Z\n") == (
        None,
        None,
        None,
    )


def test_parse_kit_line_unrendered_template_slot_has_no_version():
    # An adopt-seed heartbeat still carries `kit: v${kit_version}` — no
    # numeric version token, so it must parse as version-less, not as junk.
    version, check, engaged = parse_kit_line(
        "kit: v${kit_version} · check: red · engaged: no\n",
    )
    assert version is None
    assert (check, engaged) == ("red", "no")


# ---------------------------------------------------------------------------
# parse_roster — repos + per-lane heartbeat declarations as data
# ---------------------------------------------------------------------------


def test_parse_roster_skips_comments_and_blanks_and_reads_lanes():
    text = (
        "# fleet\n\nmenno420/websites\n"
        "menno420/superbot-games control/status-mining.md control/status-exploration.md\n"
    )
    roster = parse_roster(text)
    assert roster == [
        ("menno420/websites", []),
        (
            "menno420/superbot-games",
            ["control/status-mining.md", "control/status-exploration.md"],
        ),
    ]


# ---------------------------------------------------------------------------
# scan_repo — evidence classes kept distinct
# ---------------------------------------------------------------------------


def test_scan_repo_reads_dist_header_pin_and_self_report():
    fetch = _fetcher(
        {
            ("o/r", "bootstrap.py"): DIST_HEADER,
            ("o/r", "substrate.config.json"): CONFIG_16,
            ("o/r", "control/status.md"): STATUS_OK,
        },
    )
    scan = scan_repo("o/r", fetch)
    assert scan.tree_version == "1.6.0"
    assert scan.tree_source == "bootstrap.py"
    assert scan.config_pin == "1.6.0"
    assert scan.reports == [
        SelfReport("control/status.md", "1.6.0", "green", "yes", found=True),
    ]
    assert scan.adopted
    assert scan.drifts() == []


def test_scan_repo_falls_back_to_dist_bootstrap_path():
    # Consumer #0 (the kit repo itself) vendors at dist/bootstrap.py.
    fetch = _fetcher({("o/r", "dist/bootstrap.py"): DIST_HEADER})
    scan = scan_repo("o/r", fetch)
    assert scan.tree_version == "1.6.0"
    assert scan.tree_source == "dist/bootstrap.py"


def test_scan_repo_no_artifacts_is_not_adopted_not_an_error():
    scan = scan_repo("o/empty", _fetcher({}))
    assert not scan.adopted
    assert scan.verdict("1.7.0") == "not adopted / unknown"
    assert scan.drifts() == []


def test_scan_repo_honours_configured_heartbeat_files():
    fetch = _fetcher(
        {
            ("o/r", "substrate.config.json"): (
                '{"kit_version": "1.6.0",'
                ' "heartbeat_files": ["control/status-a.md"]}'
            ),
            ("o/r", "control/status-a.md"): STATUS_OK,
        },
    )
    scan = scan_repo("o/r", fetch)
    assert [r.heartbeat for r in scan.reports] == ["control/status-a.md"]


def test_scan_repo_extra_heartbeats_add_lanes():
    fetch = _fetcher(
        {
            ("o/r", "substrate.config.json"): CONFIG_16,
            ("o/r", "control/status.md"): STATUS_OK,
            ("o/r", "control/status-mining.md"): STATUS_DRIFTED,
        },
    )
    scan = scan_repo("o/r", fetch, ["control/status-mining.md"])
    assert [r.heartbeat for r in scan.reports] == [
        "control/status.md",
        "control/status-mining.md",
    ]


# ---------------------------------------------------------------------------
# drift — tree is truth; a claim that disagrees is surfaced, never resolved
# ---------------------------------------------------------------------------


def test_drift_self_report_vs_tree_is_loud():
    fetch = _fetcher(
        {
            ("o/r", "bootstrap.py"): DIST_HEADER,
            ("o/r", "control/status.md"): STATUS_DRIFTED,
        },
    )
    scan = scan_repo("o/r", fetch)
    drifts = scan.drifts()
    assert len(drifts) == 1
    assert "claims v1.2.0" in drifts[0]
    assert "tree says v1.6.0" in drifts[0]
    assert "DRIFT" in scan.verdict("1.7.0")


def test_drift_tree_internal_dist_vs_pin():
    fetch = _fetcher(
        {
            ("o/r", "bootstrap.py"): DIST_HEADER,
            ("o/r", "substrate.config.json"): '{"kit_version": "1.0.0"}',
        },
    )
    scan = scan_repo("o/r", fetch)
    drifts = scan.drifts()
    assert len(drifts) == 1
    assert "tree-internal" in drifts[0]
    # Vendored dist stays the primary truth.
    assert scan.effective_tree == "1.6.0"


def test_no_drift_when_report_matches_tree():
    fetch = _fetcher(
        {
            ("o/r", "bootstrap.py"): DIST_HEADER,
            ("o/r", "substrate.config.json"): CONFIG_16,
            ("o/r", "control/status.md"): STATUS_OK,
        },
    )
    assert scan_repo("o/r", fetch).drifts() == []


def test_missing_self_report_is_not_drift():
    # A repo with a tree artifact but no heartbeat is dark, not lying.
    fetch = _fetcher({("o/r", "substrate.config.json"): CONFIG_16})
    scan = scan_repo("o/r", fetch)
    assert scan.drifts() == []
    assert "pin-only" in scan.verdict("1.7.0")


# ---------------------------------------------------------------------------
# verdicts — stale vs current vs pin-only
# ---------------------------------------------------------------------------


def test_verdict_stale_when_behind_kit_release():
    scan = RepoCurrency(repo="o/r", tree_version="1.6.0", tree_source="bootstrap.py")
    assert scan.verdict("1.7.0") == "stale (v1.6.0 < v1.7.0)"


def test_verdict_current_at_kit_release():
    scan = RepoCurrency(repo="o/r", tree_version="1.7.0", tree_source="bootstrap.py")
    assert scan.verdict("1.7.0") == "current"


def test_verdict_self_report_only_has_no_tree_artifact():
    scan = RepoCurrency(repo="o/r")
    scan.reports.append(SelfReport("control/status.md", "1.6.0", "green", "yes", True))
    verdict = scan.verdict("1.7.0")
    assert "no tree artifact" in verdict


# ---------------------------------------------------------------------------
# render_adopters — the generated registry's contract
# ---------------------------------------------------------------------------


def _two_repo_scans() -> list[RepoCurrency]:
    fetch = _fetcher(
        {
            ("o/ok", "bootstrap.py"): DIST_HEADER,
            ("o/ok", "substrate.config.json"): CONFIG_16,
            ("o/ok", "control/status.md"): STATUS_OK,
            ("o/drift", "bootstrap.py"): DIST_HEADER,
            ("o/drift", "control/status.md"): STATUS_DRIFTED,
        },
    )
    return scan_fleet([("o/ok", []), ("o/drift", []), ("o/none", [])], fetch)


def test_render_carries_marker_stamp_badge_and_rows():
    text = render_adopters(_two_repo_scans(), "1.7.0", now=NOW)
    assert GENERATED_MARKER in text
    assert f"{GENERATED_STAMP_PREFIX} 2026-07-10T18:00:00Z" in text
    assert "> **Status:** `living-ledger`" in text  # badge kept for check_docs
    assert "## Registry" in text
    assert "| o/ok |" in text
    assert "| o/none |" in text
    assert "not adopted / unknown" in text


def test_render_drift_section_names_the_drifting_repo():
    text = render_adopters(_two_repo_scans(), "1.7.0", now=NOW)
    assert "## Drift report" in text
    assert "**o/drift**" in text
    assert "claims v1.2.0" in text


def test_render_no_drift_says_so():
    fetch = _fetcher(
        {
            ("o/ok", "bootstrap.py"): DIST_HEADER,
            ("o/ok", "control/status.md"): STATUS_OK,
        },
    )
    text = render_adopters(scan_fleet([("o/ok", [])], fetch), "1.7.0", now=NOW)
    assert "No drift" in text


def test_render_multi_lane_reports_name_their_lane_files():
    fetch = _fetcher(
        {
            ("o/shared", "control/status-mining.md"): STATUS_OK,
            ("o/shared", "control/status-exploration.md"): STATUS_DRIFTED,
        },
    )
    scans = scan_fleet(
        [
            (
                "o/shared",
                ["control/status-mining.md", "control/status-exploration.md"],
            ),
        ],
        fetch,
    )
    text = render_adopters(scans, "1.7.0", now=NOW)
    assert "status-mining.md: v1.6.0" in text
    assert "status-exploration.md: v1.2.0" in text


def test_drift_report_lines_cover_every_repo():
    lines = drift_report_lines(_two_repo_scans(), "1.7.0")
    assert any(line.startswith("o/ok:") for line in lines)
    assert any(line.startswith("o/none:") for line in lines)
    assert any("DRIFT" in line for line in lines)
