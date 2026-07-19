"""Tests for scripts/measure_pr_latency.py — pure logic, no network.

The GSW-4 latency pass (docs/planning/2026-07-19-grounded-skills-window-run.md;
PR #247 §2 method) computes PR open->merge latency from GitHub-API timestamps.
These tests pin the frozen metric definitions — the bucketing boundaries, the
minutes computation, the numpy-style percentile convention, and the
parse-to-buckets aggregation — so a silent behavior change is a red suite.
No network is touched.
"""

from __future__ import annotations

import importlib.util
import sys
from datetime import date
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPT = _REPO_ROOT / "scripts" / "measure_pr_latency.py"

_spec = importlib.util.spec_from_file_location("measure_pr_latency", _SCRIPT)
mpl = importlib.util.module_from_spec(_spec)
sys.modules.setdefault("measure_pr_latency", mpl)
_spec.loader.exec_module(mpl)

WINDOW = dict(start=date(2026, 7, 1), boundary=date(2026, 7, 12), end=date(2026, 7, 19))


# ── roster ───────────────────────────────────────────────────────────────────


def test_parse_roster_drops_comments_and_lane_tokens():
    text = (
        "# comment\n"
        "\n"
        "menno420/substrate-kit\n"
        "menno420/superbot-games control/status-mining.md control/status-exploration.md\n"
    )
    assert mpl.parse_roster(text) == [
        "menno420/substrate-kit",
        "menno420/superbot-games",
    ]


# ── bucket_of — boundaries ───────────────────────────────────────────────────


def test_bucket_of_at_each_boundary():
    # window edges
    assert mpl.bucket_of(date(2026, 7, 1), **WINDOW) == "before"
    assert mpl.bucket_of(date(2026, 7, 11), **WINDOW) == "before"
    # boundary day excluded from both buckets, reported separately
    assert mpl.bucket_of(date(2026, 7, 12), **WINDOW) == "boundary-day"
    assert mpl.bucket_of(date(2026, 7, 13), **WINDOW) == "after"
    assert mpl.bucket_of(date(2026, 7, 19), **WINDOW) == "after"
    # out of window
    assert mpl.bucket_of(date(2026, 6, 30), **WINDOW) is None
    assert mpl.bucket_of(date(2026, 7, 20), **WINDOW) is None


# ── latency_minutes ──────────────────────────────────────────────────────────


def test_latency_minutes_known_pair():
    # created 12:00:00Z, merged 13:30:00Z → 90.0 minutes
    assert mpl.latency_minutes(
        "2026-07-15T12:00:00Z", "2026-07-15T13:30:00Z"
    ) == 90.0
    # cross-day, with +00:00 offset form
    assert mpl.latency_minutes(
        "2026-07-15T23:00:00+00:00", "2026-07-16T00:15:00+00:00"
    ) == 75.0
    # zero-latency (created == merged)
    assert mpl.latency_minutes(
        "2026-07-15T12:00:00Z", "2026-07-15T12:00:00Z"
    ) == 0.0


# ── summarize — percentile convention + empty case ───────────────────────────


def test_summarize_numpy_linear_convention():
    # 1..10 minutes. numpy.percentile(method='linear'):
    #   p50 → h=(10-1)*0.5=4.5 → between vals[4]=5 and vals[5]=6 → 5.5
    #   p90 → h=(10-1)*0.9=8.1 → between vals[8]=9 and vals[9]=10 → 9.1
    #   p100 → max = 10
    vals = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
    out = mpl.summarize(vals)
    assert out["median_min"] == 5.5
    assert out["p90_min"] == 9.1
    assert out["max_min"] == 10.0


def test_summarize_single_value():
    out = mpl.summarize([42.0])
    assert out == {"median_min": 42.0, "p90_min": 42.0, "max_min": 42.0}


def test_summarize_empty_is_all_null():
    assert mpl.summarize([]) == {
        "median_min": None,
        "p90_min": None,
        "max_min": None,
    }


def test_summarize_rounds_to_one_decimal():
    # median of [1,2] → 1.5; p90 of [1,2] → h=0.9 → 1.9
    out = mpl.summarize([1.0, 2.0])
    assert out["median_min"] == 1.5
    assert out["p90_min"] == 1.9
    assert out["max_min"] == 2.0


# ── buckets_from_prs — parse-to-buckets aggregation ──────────────────────────


def test_buckets_from_prs_synthetic():
    prs = [
        # before: two PRs merged 07-05 and 07-10
        {"created_at": "2026-07-05T10:00:00Z", "merged_at": "2026-07-05T11:00:00Z"},  # 60
        {"created_at": "2026-07-10T09:00:00Z", "merged_at": "2026-07-10T12:00:00Z"},  # 180
        # boundary-day: one PR merged 07-12
        {"created_at": "2026-07-12T08:00:00Z", "merged_at": "2026-07-12T08:30:00Z"},  # 30
        # after: one PR merged 07-15
        {"created_at": "2026-07-15T10:00:00Z", "merged_at": "2026-07-15T14:00:00Z"},  # 240
        # out-of-window: merged 07-20 → dropped
        {"created_at": "2026-07-19T10:00:00Z", "merged_at": "2026-07-20T10:00:00Z"},
        # missing merged_at → dropped
        {"created_at": "2026-07-08T10:00:00Z", "merged_at": None},
    ]
    out = mpl.buckets_from_prs(prs, **WINDOW)

    # before: latencies [60, 180]; median = 120, p90 h=0.9 → 60+(180-60)*0.9=168, max=180
    assert out["before"]["merged"] == 2
    assert out["before"]["latency_n"] == 2
    assert out["before"]["median_min"] == 120.0
    assert out["before"]["p90_min"] == 168.0
    assert out["before"]["max_min"] == 180.0

    # boundary-day: single PR, 30 minutes
    assert out["boundary-day"]["merged"] == 1
    assert out["boundary-day"]["median_min"] == 30.0
    assert out["boundary-day"]["max_min"] == 30.0

    # after: single PR, 240 minutes
    assert out["after"]["merged"] == 1
    assert out["after"]["latency_n"] == 1
    assert out["after"]["median_min"] == 240.0


def test_buckets_from_prs_empty_bucket_is_null():
    prs = [
        {"created_at": "2026-07-15T10:00:00Z", "merged_at": "2026-07-15T11:00:00Z"},
    ]
    out = mpl.buckets_from_prs(prs, **WINDOW)
    # before + boundary-day have no PRs → merged 0, stats null
    assert out["before"] == {
        "merged": 0,
        "latency_n": 0,
        "median_min": None,
        "p90_min": None,
        "max_min": None,
    }
    assert out["boundary-day"]["merged"] == 0
    assert out["boundary-day"]["median_min"] is None
    assert out["after"]["merged"] == 1


def test_latency_n_equals_merged_no_squash_exclusion():
    # every merged PR counts toward the latency stat (flagged method decision 1)
    prs = [
        {"created_at": "2026-07-05T10:00:00Z", "merged_at": "2026-07-05T10:30:00Z"},
        {"created_at": "2026-07-06T10:00:00Z", "merged_at": "2026-07-06T10:45:00Z"},
        {"created_at": "2026-07-07T10:00:00Z", "merged_at": "2026-07-07T12:00:00Z"},
    ]
    out = mpl.buckets_from_prs(prs, **WINDOW)
    assert out["before"]["merged"] == out["before"]["latency_n"] == 3


# ── fleet_aggregate — pooled ─────────────────────────────────────────────────


def test_fleet_aggregate_pools_latencies():
    pooled = {
        "before": [60.0, 180.0],
        "boundary-day": [],
        "after": [30.0, 90.0, 240.0],
    }
    agg = mpl.fleet_aggregate(pooled)
    assert agg["before"]["latency_n"] == 2
    assert agg["before"]["median_min"] == 120.0
    assert agg["boundary-day"]["latency_n"] == 0
    assert agg["boundary-day"]["median_min"] is None
    assert agg["after"]["latency_n"] == 3
    assert agg["after"]["median_min"] == 90.0  # median of [30,90,240]


# ── payload shape ────────────────────────────────────────────────────────────


def test_build_payload_shape():
    repo_results = [
        {
            "name": "menno420/substrate-kit",
            "ok": True,
            "skip_reason": "",
            "api_latency": mpl.buckets_from_prs(
                [
                    {
                        "created_at": "2026-07-05T10:00:00Z",
                        "merged_at": "2026-07-05T11:00:00Z",
                    }
                ],
                **WINDOW,
            ),
            "_latencies": {"before": [60.0], "boundary-day": [], "after": []},
        }
    ]
    payload = mpl.build_payload(
        repo_results, generated="2026-07-19T01:00:00Z", **WINDOW
    )
    assert payload["generated"] == "2026-07-19T01:00:00Z"
    assert payload["window"]["boundary"] == "2026-07-12"
    assert "no squash exclusion" in payload["method"]
    assert payload["repos"][0]["name"] == "menno420/substrate-kit"
    # _latencies is stripped from the serialized repo entry
    assert "_latencies" not in payload["repos"][0]
    # fleet aggregate pooled from the one repo
    assert payload["fleet_aggregate"]["before"]["latency_n"] == 1
    assert payload["fleet_aggregate"]["before"]["median_min"] == 60.0
