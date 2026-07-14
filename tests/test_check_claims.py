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

from engine.checks.check_claims import (
    CLAIM_STALE_HOURS,
    LEGACY_CLAIMS_DIRS,
    WORK_CLAIM_STALE_HOURS,
    check_claims,
)
from engine.checks.check_status_current import STATUS_RELPATH
from engine.cli import cmd_check
from engine.lib.config import DEFAULT_CLAIMS_DIR

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
# WORK claims (EAP §6.4) — one file per claim under control/claims/
# ---------------------------------------------------------------------------


def _claim_bullet(token: str, day: str = "2026-07-10") -> str:
    return f"- `{token}` · **scope** — a slice under way · src/x · {day}\n"


def test_no_claims_dir_no_work_findings(tmp_path):
    # No control protocol, no claims dir anywhere → completely silent.
    assert check_claims(tmp_path, now=NOW) == []
    assert DEFAULT_CLAIMS_DIR == "control/claims"


def test_valid_fresh_work_claim_is_clean(tmp_path):
    _write(tmp_path, f"{DEFAULT_CLAIMS_DIR}/claude__lane-a.md", _claim_bullet("claude/lane-a"))
    assert check_claims(tmp_path, now=NOW) == []


def test_claims_readme_is_never_a_claim(tmp_path):
    _write(tmp_path, f"{DEFAULT_CLAIMS_DIR}/README.md", "# convention doc, no bullet\n")
    assert check_claims(tmp_path, now=NOW) == []


def test_unparseable_claim_flags_format(tmp_path):
    _write(tmp_path, f"{DEFAULT_CLAIMS_DIR}/mystery.md", "working on stuff\n")
    findings = check_claims(tmp_path, now=NOW)
    assert [f.kind for f in findings] == ["claims-format"]
    assert findings[0].path == f"{DEFAULT_CLAIMS_DIR}/mystery.md"


def test_bullet_without_date_flags_format(tmp_path):
    _write(tmp_path, f"{DEFAULT_CLAIMS_DIR}/no-date.md", "- `lane-x` · scope only\n")
    assert [f.kind for f in check_claims(tmp_path, now=NOW)] == ["claims-format"]


def test_old_work_claim_flags_stale(tmp_path):
    # Dated 5 days before NOW — past the 72h work horizon.
    _write(
        tmp_path,
        f"{DEFAULT_CLAIMS_DIR}/old.md",
        _claim_bullet("claude/old-lane", day="2026-07-05"),
    )
    findings = check_claims(tmp_path, now=NOW)
    assert [f.kind for f in findings] == ["claims-stale"]
    assert "orphan" in findings[0].message
    assert WORK_CLAIM_STALE_HOURS == 72


def test_dated_filename_in_scope_text_is_not_stale(tmp_path):
    # Regression (found live, 2026-07-14 model-line-lint session): the
    # checker dated a claim by the FIRST date-string anywhere in the file,
    # so a dated idea-filename in the scope text shadowed the fresh claim
    # date and fired a false claims-stale. The claim's own date is the LAST
    # date on the bullet line (the taught grammar ends `· YYYY-MM-DD`).
    _write(
        tmp_path,
        f"{DEFAULT_CLAIMS_DIR}/fresh-with-dated-ref.md",
        "- `claude/lane-a` · **scope** — build the checker per "
        "docs/ideas/foo-2026-07-05.md · src/engine/checks · 2026-07-10\n",
    )
    assert check_claims(tmp_path, now=NOW) == []


def test_old_claim_date_fires_despite_fresh_filename_mention(tmp_path):
    # The inverse guard: a genuinely old claim date (last on the bullet)
    # still fires even when the scope text mentions a fresher dated file.
    _write(
        tmp_path,
        f"{DEFAULT_CLAIMS_DIR}/old-with-fresh-ref.md",
        "- `claude/lane-b` · **scope** — port docs/ideas/bar-2026-07-10.md "
        "· src/x · 2026-07-05\n",
    )
    findings = check_claims(tmp_path, now=NOW)
    assert [f.kind for f in findings] == ["claims-stale"]
    assert "dated 2026-07-05" in findings[0].message


def test_date_outside_bullet_line_flags_format(tmp_path):
    # A date somewhere else in the file is not the claim's date field —
    # a bullet without its own date is unparseable (claims-format), not
    # dated by unrelated prose.
    _write(
        tmp_path,
        f"{DEFAULT_CLAIMS_DIR}/date-elsewhere.md",
        "- `claude/lane-c` · scope only\n\nopened 2026-07-01 by a session\n",
    )
    assert [f.kind for f in check_claims(tmp_path, now=NOW)] == ["claims-format"]


def test_two_files_same_token_flag_duplicate(tmp_path):
    _write(tmp_path, f"{DEFAULT_CLAIMS_DIR}/a.md", _claim_bullet("claude/same"))
    _write(tmp_path, f"{DEFAULT_CLAIMS_DIR}/b.md", _claim_bullet("claude/same"))
    findings = check_claims(tmp_path, now=NOW)
    assert [f.kind for f in findings] == ["claims-duplicate", "claims-duplicate"]
    assert {f.path for f in findings} == {
        f"{DEFAULT_CLAIMS_DIR}/a.md",
        f"{DEFAULT_CLAIMS_DIR}/b.md",
    }
    for f in findings:
        assert "claude/same" in f.message


def test_distinct_tokens_are_clean(tmp_path):
    _write(tmp_path, f"{DEFAULT_CLAIMS_DIR}/a.md", _claim_bullet("claude/one"))
    _write(tmp_path, f"{DEFAULT_CLAIMS_DIR}/b.md", _claim_bullet("claude/two"))
    assert check_claims(tmp_path, now=NOW) == []


# ---------------------------------------------------------------------------
# Cross-branch ORDER collision (the #362/#363 twin-build fix)
# ---------------------------------------------------------------------------


def _order_bullet(token: str, order: str, day: str = "2026-07-10") -> str:
    return f"- `{token}` · **scope** — a slice under way · order {order} · {day}\n"


def test_cross_branch_same_order_flags_collision(tmp_path):
    # The realized #362/#363 shape: two live claims, DIFFERENT branches,
    # both serving ORDER 020 — branch-keyed dedupe is silent; the order
    # scan must not be.
    _write(
        tmp_path,
        f"{DEFAULT_CLAIMS_DIR}/a.md",
        _order_bullet("claude/lane-a", "020"),
    )
    _write(
        tmp_path,
        f"{DEFAULT_CLAIMS_DIR}/b.md",
        _order_bullet("claude/lane-b", "020"),
    )
    findings = check_claims(tmp_path, now=NOW)
    assert [f.kind for f in findings] == [
        "claims-order-collision",
        "claims-order-collision",
    ]
    assert {f.path for f in findings} == {
        f"{DEFAULT_CLAIMS_DIR}/a.md",
        f"{DEFAULT_CLAIMS_DIR}/b.md",
    }
    for f in findings:
        assert "order 020" in f.message
        assert "claude/lane-a" in f.message
        assert "claude/lane-b" in f.message


def test_free_text_order_mention_also_keys_the_scan(tmp_path):
    # A hand-written claim naming its order in prose (`ORDER 20`) collides
    # with a verb-written structured `order 020` segment — same normalized
    # id, one grammar home.
    _write(
        tmp_path,
        f"{DEFAULT_CLAIMS_DIR}/a.md",
        _order_bullet("claude/lane-a", "020"),
    )
    _write(
        tmp_path,
        f"{DEFAULT_CLAIMS_DIR}/b.md",
        "- `claude/lane-b` · **ORDER 20 sub-items (d)+(e)** · src/x · 2026-07-10\n",
    )
    findings = check_claims(tmp_path, now=NOW)
    assert [f.kind for f in findings] == [
        "claims-order-collision",
        "claims-order-collision",
    ]


def test_distinct_orders_across_branches_are_clean(tmp_path):
    _write(
        tmp_path,
        f"{DEFAULT_CLAIMS_DIR}/a.md",
        _order_bullet("claude/lane-a", "019"),
    )
    _write(
        tmp_path,
        f"{DEFAULT_CLAIMS_DIR}/b.md",
        _order_bullet("claude/lane-b", "020"),
    )
    assert check_claims(tmp_path, now=NOW) == []


def test_order_less_claims_never_collide(tmp_path):
    # Order-less claims stay valid and invisible to the order scan — no
    # false positive against an order-carrying sibling.
    _write(tmp_path, f"{DEFAULT_CLAIMS_DIR}/a.md", _claim_bullet("claude/lane-a"))
    _write(
        tmp_path,
        f"{DEFAULT_CLAIMS_DIR}/b.md",
        _order_bullet("claude/lane-b", "020"),
    )
    assert check_claims(tmp_path, now=NOW) == []


def test_same_branch_same_order_is_duplicate_not_collision(tmp_path):
    # One branch, two files, one order: that is the existing same-token
    # claims-duplicate — the collision kind needs DISTINCT branches.
    _write(tmp_path, f"{DEFAULT_CLAIMS_DIR}/a.md", _order_bullet("claude/same", "020"))
    _write(tmp_path, f"{DEFAULT_CLAIMS_DIR}/b.md", _order_bullet("claude/same", "020"))
    kinds = [f.kind for f in check_claims(tmp_path, now=NOW)]
    assert kinds == ["claims-duplicate", "claims-duplicate"]


def test_order_word_inside_prose_is_not_an_order_id(tmp_path):
    # `reorder 020` / `orders 001` must not parse as order references —
    # the regex requires the standalone word `order` before the digits.
    _write(
        tmp_path,
        f"{DEFAULT_CLAIMS_DIR}/a.md",
        "- `claude/lane-a` · **reorder 020 rows in the panel** · 2026-07-10\n",
    )
    _write(
        tmp_path,
        f"{DEFAULT_CLAIMS_DIR}/b.md",
        _order_bullet("claude/lane-b", "020"),
    )
    assert check_claims(tmp_path, now=NOW) == []


def test_cross_location_order_collision_is_caught(tmp_path):
    # A canonical-dir claim and a legacy-dir claim serving one order still
    # collide (plus the legacy-location nudge, which is its own finding).
    _write(
        tmp_path,
        f"{DEFAULT_CLAIMS_DIR}/a.md",
        _order_bullet("claude/lane-a", "020"),
    )
    _write(
        tmp_path,
        "docs/owner/claims/b.md",
        _order_bullet("claude/lane-b", "020"),
    )
    kinds = sorted(f.kind for f in check_claims(tmp_path, now=NOW))
    assert kinds == [
        "claims-legacy-location",
        "claims-order-collision",
        "claims-order-collision",
    ]


def test_cmd_check_strict_stays_green_on_order_collision(tmp_path, capsys):
    # Advisory posture preserved end-to-end: the collision warns, the exit
    # code never moves.
    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    _write(tmp_path, STATUS_RELPATH, _status("acked=020 done=020"))
    _write(
        tmp_path,
        f"{DEFAULT_CLAIMS_DIR}/a.md",
        _order_bullet("claude/lane-a", "020", day=day),
    )
    _write(
        tmp_path,
        f"{DEFAULT_CLAIMS_DIR}/b.md",
        _order_bullet("claude/lane-b", "020", day=day),
    )
    assert cmd_check(tmp_path, strict=True) == 0
    out = capsys.readouterr().out
    assert "claims-order-collision" in out
    assert "never exit-affecting" in out


def test_legacy_superbot_location_nudges_and_still_scans(tmp_path):
    # docs/owner/claims/ (superbot's Q-0195 home): one nudge per legacy dir,
    # and the claims inside still get the full treatment (here: stale).
    _write(
        tmp_path,
        "docs/owner/claims/claude__x.md",
        _claim_bullet("claude/x", day="2026-07-01"),
    )
    findings = check_claims(tmp_path, now=NOW)
    kinds = sorted(f.kind for f in findings)
    assert kinds == ["claims-legacy-location", "claims-stale"]
    legacy = next(f for f in findings if f.kind == "claims-legacy-location")
    assert legacy.path == "docs/owner/claims"
    assert DEFAULT_CLAIMS_DIR in legacy.message
    assert "claims_dir" in legacy.message


def test_legacy_root_claims_location_nudges(tmp_path):
    # Root claims/ (gba-homebrew's home).
    _write(tmp_path, "claims/lane.md", _claim_bullet("games/lane"))
    findings = check_claims(tmp_path, now=NOW)
    assert [f.kind for f in findings] == ["claims-legacy-location"]
    assert LEGACY_CLAIMS_DIRS == ("docs/owner/claims", "claims")


def test_empty_legacy_dir_is_silent(tmp_path):
    # A legacy dir holding only its README (or nothing) has nothing to move.
    _write(tmp_path, "claims/README.md", "# convention doc\n")
    assert check_claims(tmp_path, now=NOW) == []


def test_cross_location_duplicate_is_caught(tmp_path):
    # The same token claimed canonically AND in a legacy home is still the
    # collision — the compat window must not blind the duplicate scan.
    _write(tmp_path, f"{DEFAULT_CLAIMS_DIR}/a.md", _claim_bullet("claude/same"))
    _write(tmp_path, "claims/b.md", _claim_bullet("claude/same"))
    kinds = sorted(f.kind for f in check_claims(tmp_path, now=NOW))
    assert kinds == [
        "claims-duplicate",
        "claims-duplicate",
        "claims-legacy-location",
    ]


def test_configured_claims_dir_is_canonical_no_nudge(tmp_path):
    # A host that pins a legacy path via claims_dir made it canonical —
    # no legacy nudge, full scanning.
    _write(
        tmp_path,
        "docs/owner/claims/fresh.md",
        _claim_bullet("claude/fresh"),
    )
    findings = check_claims(tmp_path, now=NOW, claims_dir="docs/owner/claims")
    assert findings == []


def test_work_claims_scan_without_control_protocol(tmp_path):
    # The work half self-gates on the dir, not on control/ evidence.
    _write(tmp_path, f"{DEFAULT_CLAIMS_DIR}/x.md", "no bullet here\n")
    assert [f.kind for f in check_claims(tmp_path, now=NOW)] == ["claims-format"]


def test_work_and_order_findings_combine(tmp_path):
    _write(
        tmp_path,
        STATUS_RELPATH,
        _status(f"acked=001-005 done=005 claimed-by: 005 lane-a {FRESH}"),
    )
    _write(tmp_path, f"{DEFAULT_CLAIMS_DIR}/y.md", "unparseable\n")
    kinds = sorted(f.kind for f in check_claims(tmp_path, now=NOW))
    assert kinds == ["claims-format", "claims-stale"]


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


def test_cmd_check_strict_stays_green_on_work_claim_findings(tmp_path, capsys):
    # The §6.4 compat guarantee: format + legacy-location nudges (the exact
    # shape an adopter's pre-unification claims produce on upgrade) never
    # touch the exit code. Uses the root claims/ legacy home — a docs_root
    # legacy home additionally meets the ORDINARY docs-hygiene checkers
    # (badge/reachability), which is check_docs' finding, not a claims one.
    _write(tmp_path, STATUS_RELPATH, _status("acked=001 done=001"))
    _write(tmp_path, "claims/legacy-lane.md", "prose, no bullet\n")
    assert cmd_check(tmp_path, strict=True) == 0
    out = capsys.readouterr().out
    assert "claims-legacy-location" in out
    assert "claims-format" in out
    assert "never exit-affecting" in out


def test_cmd_check_honours_configured_claims_dir(tmp_path, capsys):
    # A pinned claims_dir is canonical: scanned (the stale nag fires) but
    # never nudged as legacy (pinning the root claims/ home end-to-end).
    _write(tmp_path, STATUS_RELPATH, _status("acked=001 done=001"))
    _write(
        tmp_path,
        "claims/old.md",
        "- `claude/old` · scope — detail · 2026-01-01\n",
    )
    (tmp_path / "substrate.config.json").write_text(
        '{"claims_dir": "claims"}',
        encoding="utf-8",
    )
    assert cmd_check(tmp_path, strict=True) == 0
    out = capsys.readouterr().out
    assert "claims-stale" in out
    assert "claims-legacy-location" not in out


def test_cmd_check_quiet_when_claims_clean(tmp_path, capsys):
    _write(
        tmp_path,
        STATUS_RELPATH,
        _status(f"acked=001-006 done=001-006 claimed-by: 007 lane-a {_recent()}"),
    )
    assert cmd_check(tmp_path, strict=True) == 0
    out = capsys.readouterr().out
    assert "claims-duplicate" not in out and "claims-stale" not in out
