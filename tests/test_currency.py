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


def test_parse_kit_line_bullet_embedded_heartbeat():
    # venture-lab's live shape (v1.10.1 wave finding): the heartbeat line
    # embedded as a markdown bullet with a bold label. The old start-of-line
    # anchor read this as "no `kit:` line" and lost the engaged signal.
    text = (
        "# venture-lab · status\nupdated: 2026-07-11T09:00Z\n"
        "- **kit heartbeat:** kit: v1.10.1 · check: green · engaged: yes\n"
    )
    version, check, engaged = parse_kit_line(text)
    assert (version, check, engaged) == ("1.10.1", "green", "yes")


def test_parse_kit_line_plain_bullet_prefix():
    # A bare list-marker prefix (no bold label) parses too.
    version, check, engaged = parse_kit_line(
        "* kit: v1.9.0 · check: red · engaged: no\n",
    )
    assert (version, check, engaged) == ("1.9.0", "red", "no")


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


# ---------------------------------------------------------------------------
# default_fetcher — private-repo blindness fix (kit #230 headline)
#
# raw.githubusercontent.com returns 404 for EVERY path of a private repo, so
# the old fetcher rendered an adopted private repo (pokemon-mod-lab, truly at
# v1.6.0) as "not adopted / unknown". These tests pin the layered contract:
# a 404 only ever becomes "truly absent" once the repo is proven readable
# (API repo probe or branch tarball), and a repo readable by NO transport is
# an *unreadable* row — loudly distinct from "not adopted".
# ---------------------------------------------------------------------------

import io
import tarfile

from engine.currency import (
    CurrencyFetchError,
    RepoUnreadableError,
    default_fetcher,
)

RAW = "https://raw.githubusercontent.com"
API = "https://api.github.com"
CODELOAD = "https://codeload.github.com"


def _http(routes: dict[str, tuple[int, bytes]]):
    """Fake HttpGet seam: url -> (status, body); unlisted urls 404."""

    def get(url: str, headers: dict[str, str]) -> tuple[int, bytes]:
        get.calls.append(url)
        get.headers.append(dict(headers))
        return routes.get(url, (404, b""))

    get.calls = []
    get.headers = []
    return get


def _targz(root: str, files: dict[str, str]) -> bytes:
    """In-memory codeload-shaped tarball (members under `<root>/`)."""
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tf:
        for path, text in files.items():
            data = text.encode("utf-8")
            info = tarfile.TarInfo(f"{root}/{path}")
            info.size = len(data)
            tf.addfile(info, io.BytesIO(data))
    return buf.getvalue()


def test_fetcher_raw_200_needs_no_fallback():
    get = _http({f"{RAW}/o/p/main/f.md": (200, b"body")})
    fetch = default_fetcher(token="t", http_get=get)
    assert fetch("o/p", "f.md") == "body"
    assert get.calls == [f"{RAW}/o/p/main/f.md"]


def test_fetcher_raw_404_api_success_reads_private_repo_as_adopted():
    # The pokemon-mod-lab shape: raw is blind (404 everywhere), the
    # authenticated contents endpoint serves the tree.
    get = _http(
        {
            f"{API}/repos/o/p/contents/substrate.config.json?ref=main": (
                200,
                CONFIG_16.encode(),
            ),
            f"{API}/repos/o/p/contents/bootstrap.py?ref=main": (
                200,
                DIST_HEADER.encode(),
            ),
            f"{API}/repos/o/p/contents/control/status.md?ref=main": (
                200,
                STATUS_OK.encode(),
            ),
        },
    )
    scan = scan_repo("o/p", default_fetcher(token="t", http_get=get))
    assert scan.unreadable is None
    assert scan.adopted
    assert scan.tree_version == "1.6.0"
    assert scan.config_pin == "1.6.0"
    assert scan.verdict("1.7.0") == "stale (v1.6.0 < v1.7.0)"


def test_fetcher_api_404_on_proven_readable_repo_is_truly_absent():
    # Repo probe says readable; contents 404s are then tree truth.
    get = _http({f"{API}/repos/o/empty": (200, b"{}")})
    scan = scan_repo("o/empty", default_fetcher(token="t", http_get=get))
    assert scan.unreadable is None
    assert not scan.adopted
    assert scan.verdict("1.7.0") == "not adopted / unknown"


def test_fetcher_auth_failure_is_unreadable_never_not_adopted():
    # Every transport denied (403): the row must say unreadable — a
    # transport failure must never masquerade as "not adopted".
    get = _http(
        {
            f"{API}/repos/o/dark": (403, b"denied"),
            f"{API}/repos/o/dark/contents/substrate.config.json?ref=main": (
                403,
                b"denied",
            ),
            f"{API}/repos/o/dark/contents/bootstrap.py?ref=main": (403, b"denied"),
            f"{API}/repos/o/dark/contents/dist/bootstrap.py?ref=main": (
                403,
                b"denied",
            ),
            f"{API}/repos/o/dark/contents/control/status.md?ref=main": (
                403,
                b"denied",
            ),
            f"{CODELOAD}/o/dark/tar.gz/refs/heads/main": (403, b"denied"),
        },
    )
    scan = scan_repo("o/dark", default_fetcher(token="t", http_get=get))
    assert scan.unreadable is not None
    assert "403" in scan.unreadable
    verdict = scan.verdict("1.7.0")
    assert "unreadable" in verdict
    assert "not adopted" not in verdict


def test_fetcher_tarball_fallback_reads_tree_and_proves_absence():
    # API REST blocked (the proxy-mediated agent-seat shape) but the branch
    # tarball serves: files read from it, and absence from it is definitive.
    tar = _targz(
        "p-main",
        {
            "substrate.config.json": CONFIG_16,
            "bootstrap.py": DIST_HEADER,
            # no control/status.md in the tree — truly absent
        },
    )
    get = _http(
        {
            f"{API}/repos/o/p": (403, b"blocked"),
            f"{CODELOAD}/o/p/tar.gz/refs/heads/main": (200, tar),
        },
    )
    scan = scan_repo("o/p", default_fetcher(token="t", http_get=get))
    assert scan.unreadable is None
    assert scan.tree_version == "1.6.0"
    assert scan.config_pin == "1.6.0"
    assert scan.reports == [
        SelfReport("control/status.md", None, None, None, found=False),
    ]
    # The tarball is fetched once per repo, not once per path.
    assert get.calls.count(f"{CODELOAD}/o/p/tar.gz/refs/heads/main") == 1


def test_fetcher_raw_non_404_still_aborts_the_run():
    get = _http({f"{RAW}/o/p/main/f.md": (500, b"boom")})
    fetch = default_fetcher(token="t", http_get=get)
    with pytest.raises(CurrencyFetchError):
        fetch("o/p", "f.md")


def test_fetcher_unreadable_error_names_repo_and_reasons():
    get = _http({})  # everything 404s, including probe + tarball
    fetch = default_fetcher(token="", http_get=get)
    with pytest.raises(RepoUnreadableError) as exc_info:
        fetch("o/dark", "bootstrap.py")
    assert exc_info.value.repo == "o/dark"
    assert "unauthenticated" in exc_info.value.reason


def test_fetcher_sends_bearer_token_on_api_calls_only():
    get = _http({f"{API}/repos/o/p/contents/f.md?ref=main": (200, b"x")})
    fetch = default_fetcher(token="sekret", http_get=get)
    assert fetch("o/p", "f.md") == "x"
    raw_headers, api_headers = get.headers
    assert "Authorization" not in raw_headers
    assert api_headers["Authorization"] == "Bearer sekret"


def test_fetcher_reads_token_from_env_when_not_given(monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "env-tok")
    get = _http({f"{API}/repos/o/p/contents/f.md?ref=main": (200, b"x")})
    fetch = default_fetcher(http_get=get)
    assert fetch("o/p", "f.md") == "x"
    assert get.headers[1]["Authorization"] == "Bearer env-tok"


def test_scan_fleet_one_unreadable_repo_does_not_black_out_the_rest():
    tar_dark = f"{CODELOAD}/o/dark/tar.gz/refs/heads/main"
    get = _http(
        {
            f"{RAW}/o/ok/main/bootstrap.py": (200, DIST_HEADER.encode()),
            f"{RAW}/o/ok/main/substrate.config.json": (200, CONFIG_16.encode()),
            f"{RAW}/o/ok/main/control/status.md": (200, STATUS_OK.encode()),
            f"{API}/repos/o/dark": (403, b"denied"),
            tar_dark: (403, b"denied"),
        },
    )
    scans = scan_fleet(
        [("o/ok", []), ("o/dark", [])],
        default_fetcher(token="t", http_get=get),
    )
    ok, dark = scans
    assert ok.adopted and ok.unreadable is None
    assert dark.unreadable is not None
    # The unreadable repo is probed once, then answered from cache.
    assert get.calls.count(tar_dark) == 1


def test_render_unreadable_row_is_loud_and_never_not_adopted():
    scan = RepoCurrency(repo="o/dark", unreadable="API 403; tarball 403")
    text = render_adopters([scan], "1.7.0", now=NOW)
    row = next(line for line in text.splitlines() if line.startswith("| o/dark"))
    assert "unreadable" in row
    assert "not adopted" not in row
    lines = drift_report_lines([scan], "1.7.0")
    assert any("unreadable" in line for line in lines)


def test_partial_evidence_before_unreadable_failure_is_kept():
    scan = RepoCurrency(
        repo="o/flaky",
        config_pin="1.6.0",
        unreadable="tarball HTTP 500",
    )
    verdict = scan.verdict("1.7.0")
    assert "partially unreadable" in verdict
    assert "stale" in verdict


# ---------------------------------------------------------------------------
# registry_delta + `currency --check` — the registry-delta preflight
# (docs/ideas/currency-check-registry-delta-preflight-2026-07-15.md)
# ---------------------------------------------------------------------------

from datetime import timedelta
from pathlib import Path

from engine.cli import KIT_VERSION, cmd_currency
from engine.currency import registry_delta


def _scan(repo: str, version: str) -> RepoCurrency:
    """A clean adopted scan: tree, pin, and self-report all agree."""
    return RepoCurrency(
        repo=repo,
        tree_version=version,
        tree_source="bootstrap.py",
        config_pin=version,
        reports=[
            SelfReport("control/status.md", version, "green", "yes", found=True),
        ],
    )


def test_delta_identical_scan_is_empty_even_across_timestamps():
    """The rows-only contract: a stamp-only difference is NOT a delta."""
    scans = [_scan("o/a", "1.6.0"), _scan("o/b", "1.6.0")]
    committed = render_adopters(scans, "1.7.0", now=NOW)
    later = NOW + timedelta(hours=6)
    assert registry_delta(committed, scans, "1.7.0") == []
    # Re-render at a different time — rows unchanged, still no delta.
    committed_later = render_adopters(scans, "1.7.0", now=later)
    assert committed_later != committed  # the stamp DID move
    assert registry_delta(committed_later, scans, "1.7.0") == []


def test_delta_reports_a_bumped_self_report_row():
    old_scans = [_scan("o/a", "1.6.0"), _scan("o/b", "1.6.0")]
    committed = render_adopters(old_scans, "1.7.0", now=NOW)
    fresh = [_scan("o/a", "1.6.0"), _scan("o/b", "1.7.0")]
    delta = registry_delta(committed, fresh, "1.7.0")
    assert delta, "a bumped row must be a delta"
    assert all(line.split(" ", 1)[1].startswith("o/b") for line in delta)
    assert any(line.startswith("- ") and "v1.6.0" in line for line in delta)
    assert any(line.startswith("+ ") and "v1.7.0" in line for line in delta)


def test_delta_dark_repo_never_counts_in_either_direction():
    """Transport darkness is about THIS run, not the fleet — never a delta."""
    old_scans = [_scan("o/a", "1.6.0"), _scan("o/b", "1.6.0")]
    committed = render_adopters(old_scans, "1.7.0", now=NOW)
    fresh = [
        _scan("o/a", "1.6.0"),
        RepoCurrency(repo="o/b", unreadable="API 403; tarball 403"),
    ]
    assert registry_delta(committed, fresh, "1.7.0") == []
    # Partial darkness (some evidence, then transport failed) is dark too.
    partial = RepoCurrency(
        repo="o/b",
        config_pin="1.7.0",
        unreadable="tarball HTTP 500",
    )
    assert registry_delta(committed, [fresh[0], partial], "1.7.0") == []


def test_delta_roster_add_and_remove_are_deltas():
    scans_ab = [_scan("o/a", "1.6.0"), _scan("o/b", "1.6.0")]
    committed = render_adopters(scans_ab, "1.7.0", now=NOW)
    grown = scans_ab + [_scan("o/c", "1.7.0")]
    delta_add = registry_delta(committed, grown, "1.7.0")
    assert delta_add and all(line.startswith("+ o/c") for line in delta_add)
    shrunk = [scans_ab[0]]
    delta_rm = registry_delta(committed, shrunk, "1.7.0")
    assert delta_rm and all(line.startswith("- o/b") for line in delta_rm)


def _check_target(tmp_path, scans, *, committed_scans=None):
    """A target dir with a roster + a committed registry rendered from scans."""
    (tmp_path / "docs").mkdir()
    roster = "\n".join(scan.repo for scan in scans) + "\n"
    (tmp_path / "docs" / "fleet-repos.txt").write_text(roster, encoding="utf-8")
    committed = render_adopters(committed_scans or scans, KIT_VERSION, now=NOW)
    (tmp_path / "docs" / "adopters.md").write_text(committed, encoding="utf-8")
    files: dict[tuple[str, str], str] = {}
    for scan in scans:
        version = scan.tree_version
        header = DIST_HEADER.replace("v1.6.0", f"v{version}")
        files[(scan.repo, "bootstrap.py")] = header
        files[(scan.repo, "substrate.config.json")] = (
            '{"kit_version": "%s"}' % version
        )
        files[(scan.repo, "control/status.md")] = STATUS_OK.replace(
            "v1.6.0",
            f"v{version}",
        )
    return _fetcher(files)


def test_cmd_currency_check_current_exits_zero_and_writes_nothing(
    tmp_path,
    capsys,
):
    scans = [_scan("o/a", "1.6.0")]
    fetch = _check_target(tmp_path, scans)
    before = (tmp_path / "docs" / "adopters.md").read_bytes()
    code = cmd_currency(tmp_path, check=True, fetcher=fetch)
    out = capsys.readouterr().out
    assert code == 0
    assert "current" in out
    assert (tmp_path / "docs" / "adopters.md").read_bytes() == before


def test_cmd_currency_check_stale_exits_one_prints_rows_writes_nothing(
    tmp_path,
    capsys,
):
    fresh = [_scan("o/a", "1.7.0")]
    committed_scans = [_scan("o/a", "1.6.0")]
    fetch = _check_target(tmp_path, fresh, committed_scans=committed_scans)
    before = (tmp_path / "docs" / "adopters.md").read_bytes()
    code = cmd_currency(tmp_path, check=True, fetcher=fetch)
    out = capsys.readouterr().out
    assert code == 1
    assert "STALE" in out
    assert "o/a" in out
    assert (tmp_path / "docs" / "adopters.md").read_bytes() == before


def test_cmd_currency_check_missing_registry_is_stale():
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp)
        (target / "docs").mkdir()
        (target / "docs" / "fleet-repos.txt").write_text(
            "o/a\n",
            encoding="utf-8",
        )
        fetch = _fetcher(
            {
                ("o/a", "bootstrap.py"): DIST_HEADER,
                ("o/a", "substrate.config.json"): CONFIG_16,
                ("o/a", "control/status.md"): STATUS_OK,
            },
        )
        assert cmd_currency(target, check=True, fetcher=fetch) == 1
