#!/usr/bin/env python3
"""measure_pr_latency — GSW-4 open->merge latency pass (GitHub-API).

Why + provenance: the grounded-skills measurement harness
(``scripts/measure_grounded_skills.py``) deliberately does NOT measure PR
open->merge latency — its M4 metric is a git-log throughput *proxy* (merged
``(#N)`` subjects per day), and open->merge latency needs the GitHub API to
get exact ``created_at``/``merged_at`` timestamps. The window-run plan
(``docs/planning/2026-07-19-grounded-skills-window-run.md``) names this the
optional **GSW-4** API pass, per the PR #247 §2 methodology
(``docs/reports/2026-07-11-adopter-outcomes-measurement.md``). This script is
that pass: a standalone, reproducible measurement, read-only over the GitHub
API.

**Metric.** PR open->merge latency = ``merged_at - created_at`` in minutes.
Per (repo x bucket) it reports ``merged`` (count of merged PRs), ``latency_n``
(count used in the latency stat), ``median_min``, ``p90_min``, ``max_min``.
Only actually-merged PRs count (closed-unmerged excluded).

**Two flagged method decisions (authored deviations, stated in the report):**

1. **All merged PRs are included in the latency stat with their exact API
   timestamps (so ``latency_n == merged``); squash-merges are NOT excluded.**
   #247 §2 excluded squash PRs only because its git-derived open-time *proxy*
   could not time them. The GitHub API returns exact ``created_at`` /
   ``merged_at`` for every merged PR regardless of merge method, so the
   exclusion is unnecessary and inclusion is strictly more complete. This is
   the one authored method deviation from #247 §2.
2. **Each PR is bucketed by its ``merged_at`` calendar DATE (day resolution,
   UTC),** parallel to the harness M4 which buckets by merge-commit author
   date. The boundary DAY (default 2026-07-12) is reported separately and
   excluded from before/after.

**Percentile convention.** The harness has no percentile/quantile helper (M4
is counts only), so this script uses the **numpy-style linear-interpolation**
percentile: for a sorted list of n values, percentile p maps to fractional
rank ``h = (n-1) * p/100`` and interpolates linearly between the two nearest
ranks. ``median_min`` = p50, ``p90_min`` = p90, ``max_min`` = p100 (the max).
This convention is stated in the report so the latency numbers are
interpretable alongside M1-M4.

Auth: DIRECT egress with the fleet PAT (the proxied GitHub REST path 403s).
``$GITHUB_PAT`` (fallbacks ``$GH_TOKEN`` / ``$GITHUB_TOKEN``).

Read-only everywhere: this script only issues GitHub read requests.

Usage (reproduces the frozen 2026-07-19 run)::

    python3 scripts/measure_pr_latency.py \\
        --start 2026-07-01 --boundary 2026-07-12 --end 2026-07-19 \\
        --repos docs/fleet-repos.txt \\
        --json docs/reports/data/2026-07-19-grounded-skills-latency.json \\
        --generated 2026-07-19T01:00:00Z

Tests: ``tests/test_measure_pr_latency.py`` (pure logic, no network).
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parent.parent

_API_ROOT = "https://api.github.com"
_CA_BUNDLE = "/root/.ccr/ca-bundle.crt"
_TOKEN_ENV_VARS = ("GITHUB_PAT", "GH_TOKEN", "GITHUB_TOKEN")


# ── roster ───────────────────────────────────────────────────────────────────


def parse_roster(text: str) -> list[str]:
    """``docs/fleet-repos.txt`` → ``owner/repo`` list (extra lane tokens dropped)."""
    repos: list[str] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        repos.append(line.split()[0])
    return repos


# ── pure logic (no network) ──────────────────────────────────────────────────


def bucket_of(day: date, start: date, boundary: date, end: date) -> str | None:
    """``before`` / ``boundary-day`` / ``after``, or None outside the window.

    before = start .. (boundary - 1)  [start <= day < boundary]
    boundary-day = boundary           [day == boundary]
    after = (boundary + 1) .. end      [boundary < day <= end]
    """
    if day < start or day > end:
        return None
    if day < boundary:
        return "before"
    if day == boundary:
        return "boundary-day"
    return "after"


def _parse_iso(ts: str) -> datetime:
    """Parse a GitHub ISO-8601 timestamp (``...Z`` or ``...+00:00``) as aware UTC."""
    s = ts.strip()
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    dt = datetime.fromisoformat(s)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def latency_minutes(created_iso: str, merged_iso: str) -> float:
    """Open->merge latency in minutes: ``merged_at - created_at``."""
    created = _parse_iso(created_iso)
    merged = _parse_iso(merged_iso)
    return (merged - created).total_seconds() / 60.0


def _percentile(sorted_vals: list[float], p: float) -> float:
    """numpy-style linear-interpolation percentile (p in [0, 100]).

    For n sorted values, fractional rank ``h = (n-1) * p/100``; interpolate
    linearly between ``floor(h)`` and ``ceil(h)``. Matches ``numpy.percentile``
    default (``method='linear'``).
    """
    n = len(sorted_vals)
    if n == 1:
        return sorted_vals[0]
    h = (n - 1) * (p / 100.0)
    lo = int(h)  # floor
    hi = min(lo + 1, n - 1)
    frac = h - lo
    return sorted_vals[lo] + (sorted_vals[hi] - sorted_vals[lo]) * frac


def summarize(latencies: list[float]) -> dict[str, float | None]:
    """{median_min, p90_min, max_min} (1-decimal), or nulls for an empty list."""
    if not latencies:
        return {"median_min": None, "p90_min": None, "max_min": None}
    s = sorted(latencies)
    return {
        "median_min": round(_percentile(s, 50.0), 1),
        "p90_min": round(_percentile(s, 90.0), 1),
        "max_min": round(_percentile(s, 100.0), 1),
    }


def _empty_bucket() -> dict[str, Any]:
    return {
        "merged": 0,
        "latency_n": 0,
        "median_min": None,
        "p90_min": None,
        "max_min": None,
    }


def buckets_from_prs(
    prs: list[dict[str, str]], *, start: date, boundary: date, end: date
) -> dict[str, dict[str, Any]]:
    """Turn ``[{created_at, merged_at}, ...]`` into per-bucket latency summaries.

    Each PR is bucketed by its ``merged_at`` calendar date (UTC, day
    resolution). PRs whose ``merged_at`` falls outside the window are dropped.
    All merged PRs in a bucket contribute to that bucket's latency stat
    (``latency_n == merged``; no squash exclusion).
    """
    per_bucket: dict[str, list[float]] = {"before": [], "boundary-day": [], "after": []}
    counts: dict[str, int] = {"before": 0, "boundary-day": 0, "after": 0}
    for pr in prs:
        merged_at = pr.get("merged_at")
        created_at = pr.get("created_at")
        if not merged_at or not created_at:
            continue
        merged_day = _parse_iso(merged_at).date()
        b = bucket_of(merged_day, start, boundary, end)
        if b is None:
            continue
        counts[b] += 1
        per_bucket[b].append(latency_minutes(created_at, merged_at))
    out: dict[str, dict[str, Any]] = {}
    for b in ("before", "boundary-day", "after"):
        lat = per_bucket[b]
        summary = summarize(lat)
        out[b] = {
            "merged": counts[b],
            "latency_n": len(lat),
            "median_min": summary["median_min"],
            "p90_min": summary["p90_min"],
            "max_min": summary["max_min"],
        }
    return out


# ── network (isolated) ───────────────────────────────────────────────────────


def _resolve_token() -> str | None:
    for var in _TOKEN_ENV_VARS:
        val = os.environ.get(var)
        if val:
            return val
    return None


def make_session() -> "Any":
    """A direct-egress requests.Session with the fleet PAT (proxied path 403s)."""
    import requests

    token = _resolve_token()
    if not token:
        raise RuntimeError(
            "no GitHub token in env (tried " + ", ".join(_TOKEN_ENV_VARS) + ")"
        )
    s = requests.Session()
    s.trust_env = False  # bypass the proxy — direct egress
    verify = _CA_BUNDLE if Path(_CA_BUNDLE).exists() else True
    s.verify = verify
    s.headers.update(
        {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
    )
    return s


def _respect_rate_limit(resp: "Any") -> None:
    """Sleep until reset+1 if the search rate budget is nearly spent."""
    try:
        remaining = int(resp.headers.get("X-RateLimit-Remaining", "99"))
    except (TypeError, ValueError):
        return
    if remaining > 2:
        return
    try:
        reset = int(resp.headers.get("X-RateLimit-Reset", "0"))
    except (TypeError, ValueError):
        reset = 0
    now = int(time.time())
    sleep_for = max(reset - now + 1, 1)
    sleep_for = min(sleep_for, 90)  # never wedge the run
    print(f"    [rate-limit] remaining={remaining}, sleeping {sleep_for}s", flush=True)
    time.sleep(sleep_for)


def fetch_merged_prs(
    repo: str,
    session: "Any",
    *,
    start: date,
    end: date,
    verbose: bool = False,
) -> list[dict[str, str]]:
    """Fetch ``{created_at, merged_at}`` for every merged PR of ``repo`` in
    [start, end] (merged-date inclusive), via the search-issues endpoint.

    Raises RuntimeError on a non-recoverable HTTP error so the caller can
    record an honest per-repo null; rate-limit 403s are backed off + retried.
    """
    owner_name = repo
    q = (
        f"repo:{owner_name} is:pr is:merged "
        f"merged:{start.isoformat()}..{end.isoformat()}"
    )
    prs: list[dict[str, str]] = []
    page = 1
    total_count: int | None = None
    while True:
        params = {"q": q, "per_page": 100, "page": page}
        resp = None
        for attempt in range(4):
            resp = session.get(
                f"{_API_ROOT}/search/issues", params=params, timeout=60
            )
            if resp.status_code == 200:
                break
            # rate-limit 403 / 429 → back off on the reset header and retry
            if resp.status_code in (403, 429):
                _respect_rate_limit(resp)
                # if the header said we still have budget, this is a hard 403
                try:
                    remaining = int(resp.headers.get("X-RateLimit-Remaining", "0"))
                except (TypeError, ValueError):
                    remaining = 0
                if remaining > 2 and attempt == 0:
                    # not a rate-limit 403 — surface the real error
                    break
                time.sleep(2)
                continue
            break
        if resp is None or resp.status_code != 200:
            code = "no-response" if resp is None else resp.status_code
            msg = ""
            if resp is not None:
                try:
                    msg = resp.json().get("message", "")
                except Exception:  # noqa: BLE001
                    msg = (resp.text or "")[:200]
            raise RuntimeError(f"HTTP {code}: {msg}".strip())
        payload = resp.json()
        if total_count is None:
            total_count = int(payload.get("total_count", 0))
        items = payload.get("items", [])
        if not items:
            break
        for item in items:
            pr_obj = item.get("pull_request") or {}
            merged_at = pr_obj.get("merged_at") or item.get("closed_at")
            created_at = item.get("created_at")
            if merged_at and created_at:
                prs.append({"created_at": created_at, "merged_at": merged_at})
        if verbose and page == 1 and items:
            sample = items[0].get("pull_request") or {}
            print(
                f"    [validate] {repo} page1: total={total_count}, "
                f"sample merged_at={sample.get('merged_at')!r} "
                f"created_at={items[0].get('created_at')!r}",
                flush=True,
            )
        if page * 100 >= (total_count or 0):
            break
        page += 1
        time.sleep(2)  # courtesy pace under the 30 req/min search budget
    return prs


# ── per-repo measurement ─────────────────────────────────────────────────────


def measure_repo(
    repo: str,
    session: "Any",
    *,
    start: date,
    boundary: date,
    end: date,
    verbose: bool = False,
) -> dict[str, Any]:
    """One repo → the per-repo result dict (ok / skip_reason / api_latency)."""
    try:
        prs = fetch_merged_prs(
            repo, session, start=start, end=end, verbose=verbose
        )
    except Exception as exc:  # noqa: BLE001
        return {
            "name": repo,
            "ok": False,
            "skip_reason": str(exc),
            "api_latency": {
                "before": _empty_bucket(),
                "boundary-day": _empty_bucket(),
                "after": _empty_bucket(),
            },
        }
    api_latency = buckets_from_prs(prs, start=start, boundary=boundary, end=end)
    return {
        "name": repo,
        "ok": True,
        "skip_reason": "",
        "api_latency": api_latency,
        "_latencies": _bucket_latencies(prs, start=start, boundary=boundary, end=end),
    }


def _bucket_latencies(
    prs: list[dict[str, str]], *, start: date, boundary: date, end: date
) -> dict[str, list[float]]:
    """The raw per-bucket latency lists (used only to pool the fleet aggregate)."""
    out: dict[str, list[float]] = {"before": [], "boundary-day": [], "after": []}
    for pr in prs:
        merged_at = pr.get("merged_at")
        created_at = pr.get("created_at")
        if not merged_at or not created_at:
            continue
        b = bucket_of(_parse_iso(merged_at).date(), start, boundary, end)
        if b is None:
            continue
        out[b].append(latency_minutes(created_at, merged_at))
    return out


def fleet_aggregate(pooled: dict[str, list[float]]) -> dict[str, dict[str, Any]]:
    """Pool ALL repos' latencies per bucket into the fleet-aggregate summaries."""
    out: dict[str, dict[str, Any]] = {}
    for b in ("before", "boundary-day", "after"):
        lat = pooled[b]
        summary = summarize(lat)
        out[b] = {
            "merged": len(lat),
            "latency_n": len(lat),
            "median_min": summary["median_min"],
            "p90_min": summary["p90_min"],
            "max_min": summary["max_min"],
        }
    return out


# ── output ───────────────────────────────────────────────────────────────────

_METHOD = (
    "GitHub API open->merge latency; latency = merged_at - created_at; "
    "all merged PRs included (no squash exclusion); bucket by merged_at date"
)


def _now_iso() -> str:
    """Best-effort current UTC ISO-Z; falls back to `date -u` then a placeholder."""
    try:
        return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    except Exception:  # noqa: BLE001
        pass
    try:
        out = subprocess.run(
            ["date", "-u", "+%Y-%m-%dT%H:%M:%SZ"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if out.returncode == 0 and out.stdout.strip():
            return out.stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        pass
    return "1970-01-01T00:00:00Z"


def build_payload(
    repo_results: list[dict[str, Any]],
    *,
    start: date,
    boundary: date,
    end: date,
    generated: str,
) -> dict[str, Any]:
    pooled: dict[str, list[float]] = {"before": [], "boundary-day": [], "after": []}
    clean_repos: list[dict[str, Any]] = []
    for r in repo_results:
        lat = r.pop("_latencies", None)
        if r["ok"] and lat:
            for b in ("before", "boundary-day", "after"):
                pooled[b].extend(lat[b])
        clean_repos.append(r)
    return {
        "generated": generated,
        "window": {
            "start": start.isoformat(),
            "boundary": boundary.isoformat(),
            "end": end.isoformat(),
        },
        "method": _METHOD,
        "repos": clean_repos,
        "fleet_aggregate": fleet_aggregate(pooled),
    }


# ── CLI ──────────────────────────────────────────────────────────────────────


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--start", type=date.fromisoformat, default=date(2026, 7, 1))
    ap.add_argument("--boundary", type=date.fromisoformat, default=date(2026, 7, 12))
    ap.add_argument("--end", type=date.fromisoformat, default=date(2026, 7, 19))
    ap.add_argument(
        "--repos", type=Path, default=_REPO_ROOT / "docs" / "fleet-repos.txt"
    )
    ap.add_argument("--json", type=Path, help="write machine-readable results here")
    ap.add_argument(
        "--generated",
        default=None,
        help="ISO-Z stamp for the output (default: real UTC now)",
    )
    args = ap.parse_args(argv)

    repos = parse_roster(args.repos.read_text(encoding="utf-8"))
    generated = args.generated or _now_iso()

    try:
        session = make_session()
    except RuntimeError as exc:
        print(f"BLOCKER: {exc}", file=sys.stderr)
        return 2

    repo_results: list[dict[str, Any]] = []
    for i, repo in enumerate(repos):
        verbose = i == 0  # validate merged_at is populated on the first repo
        print(f"[{i + 1}/{len(repos)}] {repo} ...", flush=True)
        r = measure_repo(
            repo,
            session,
            start=args.start,
            boundary=args.boundary,
            end=args.end,
            verbose=verbose,
        )
        if r["ok"]:
            a = r["api_latency"]
            print(
                f"    before: merged={a['before']['merged']} "
                f"median={a['before']['median_min']} | "
                f"boundary-day: merged={a['boundary-day']['merged']} | "
                f"after: merged={a['after']['merged']} "
                f"median={a['after']['median_min']}",
                flush=True,
            )
        else:
            print(f"    ERROR (honest null): {r['skip_reason']}", flush=True)
        repo_results.append(r)

    payload = build_payload(
        repo_results,
        start=args.start,
        boundary=args.boundary,
        end=args.end,
        generated=generated,
    )

    agg = payload["fleet_aggregate"]
    print("\n=== FLEET AGGREGATE (pooled) ===", flush=True)
    for b in ("before", "boundary-day", "after"):
        c = agg[b]
        print(
            f"  {b}: n={c['latency_n']} median={c['median_min']} "
            f"p90={c['p90_min']} max={c['max_min']}",
            flush=True,
        )

    if args.json:
        args.json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(f"\nwrote {args.json}", flush=True)
    else:
        print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
