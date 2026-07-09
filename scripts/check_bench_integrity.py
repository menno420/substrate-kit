#!/usr/bin/env python3
"""check_bench_integrity — the §5.0 bench pin, layer 1 (CI-enforced from birth).

Why + provenance: the founding plan §5.0/D-9/D-24 — `parity/`'s
oracle-outside-the-measured-system's-write-reach principle, implemented with
in-repo mechanisms because the kit repo has no second repo to hide the oracle
in, and CODEOWNERS alone binds nothing without a ruleset (P10, owner-gated).
Added 2026-07-09 (band KL-5). Reliability (PL-008): UNVERIFIED — confirm its
findings against ground truth a few times across sessions before trusting it;
**delete this if it proves unreliable over multiple sessions.**

Two rules, exit 1 on any finding:

1. **Pin-path label gate** (pull-request context only): a diff that touches
   ``bench/rubric/``, ``bench/tasks/``, or ``bench/seeds/`` must carry the
   ``do-not-automerge`` label — forcing every rubric/tasks/seeds change to
   sit for review instead of auto-merging (the lab loop never merges its own
   change to the oracle). Labels come from ``$PR_LABELS`` (comma-separated —
   the workflow injects ``join(github.event.pull_request.labels.*.name)``);
   the gate is skipped with a note when ``$GITHUB_EVENT_NAME`` is not
   ``pull_request`` (a push to main has no label context and was already
   gated as a PR).
2. **Append-aware results immutability** (every context): under
   ``bench/results/``, deleting any file or modifying an existing non-index
   artifact is a violation; an ``index.json`` may only be modified by
   APPEND — the old rows must be exactly a prefix of the new rows. Adding
   new files/run dirs is what a benchmark run does and is always allowed.

Diff base: ``--base`` (default ``origin/main``; for push events ``HEAD^``),
compared via ``git diff --name-status <merge-base>``.

Repo-level tooling, not engine code: lives in scripts/, uses
print/subprocess, never ships in dist/bootstrap.py.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

PIN_PREFIXES = ("bench/rubric/", "bench/tasks/", "bench/seeds/")
RESULTS_PREFIX = "bench/results/"
REQUIRED_LABEL = "do-not-automerge"


def _git(args: list[str], cwd: Path) -> str:
    result = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        raise SystemExit(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout


def changed_files(root: Path, base: str) -> list[tuple[str, str]]:
    """Return ``(status, path)`` pairs for the merge-base diff vs ``base``."""
    merge_base = _git(["merge-base", base, "HEAD"], root).strip()
    out = _git(["diff", "--name-status", "--no-renames", merge_base, "HEAD"], root)
    pairs = []
    for line in out.splitlines():
        parts = line.split("\t")
        if len(parts) >= 2:
            pairs.append((parts[0][:1], parts[-1]))
    return pairs


def old_content(root: Path, base: str, path: str) -> str | None:
    """Return ``path``'s content at the merge-base (None when absent)."""
    merge_base = _git(["merge-base", base, "HEAD"], root).strip()
    result = subprocess.run(
        ["git", "show", f"{merge_base}:{path}"],
        cwd=root,
        capture_output=True,
        text=True,
    )
    return result.stdout if result.returncode == 0 else None


def check_label_gate(changed: list[tuple[str, str]], labels: list[str], event: str) -> list[str]:
    """Rule 1 — pin-path changes must ride a labeled PR."""
    pinned = [p for _, p in changed if p.startswith(PIN_PREFIXES)]
    if not pinned:
        return []
    if event != "pull_request":
        print(
            f"bench-integrity: {len(pinned)} pin-path change(s) outside a PR "
            f"context (event={event or 'none'}) — label gate not applicable here.",
        )
        return []
    if REQUIRED_LABEL in labels:
        print(
            f"bench-integrity: {len(pinned)} pin-path change(s) under the "
            f"`{REQUIRED_LABEL}` label — riding review, as the law requires.",
        )
        return []
    return [
        f"{path}: changes bench/rubric|tasks|seeds but the PR lacks the "
        f"`{REQUIRED_LABEL}` label — the §5.0 pin: label the PR (then re-run "
        "CI); rubric/tasks/seeds changes sit for review, never auto-merge"
        for path in pinned
    ]


def _index_append_only(root: Path, base: str, path: str) -> str | None:
    """Return a finding when an index.json modification is not a pure append."""
    old_text = old_content(root, base, path)
    if old_text is None:
        return None  # newly added — fine
    try:
        old_rows = json.loads(old_text)
        new_rows = json.loads((root / path).read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        return f"{path}: unreadable as JSON while verifying append-only ({exc})"
    if not isinstance(old_rows, list) or not isinstance(new_rows, list):
        return f"{path}: results index must be a JSON array"
    if new_rows[: len(old_rows)] != old_rows:
        return (
            f"{path}: existing rows were edited or removed — bench/results is "
            "append-only (new rows go at the end; recorded history is immutable)"
        )
    return None


def check_results_integrity(root: Path, base: str, changed: list[tuple[str, str]]) -> list[str]:
    """Rule 2 — results are append-aware immutable."""
    findings = []
    for status, path in changed:
        if not path.startswith(RESULTS_PREFIX):
            continue
        if status == "D":
            findings.append(
                f"{path}: deleted — bench/results history is never deleted "
                "(archive via a tombstone if retention demands it)",
            )
        elif status == "M":
            if Path(path).name == "index.json":
                finding = _index_append_only(root, base, path)
                if finding:
                    findings.append(finding)
            else:
                findings.append(
                    f"{path}: modified — an existing results artifact is "
                    "immutable (append new files; never rewrite recorded runs)",
                )
    return findings


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    default_base = "HEAD^" if os.environ.get("GITHUB_EVENT_NAME") == "push" else "origin/main"
    parser.add_argument("--base", default=default_base, help=f"diff base (default: {default_base})")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument(
        "--labels",
        default=os.environ.get("PR_LABELS", ""),
        help="comma-separated PR labels (default: $PR_LABELS)",
    )
    parser.add_argument(
        "--event",
        default=os.environ.get("GITHUB_EVENT_NAME", ""),
        help="CI event name (default: $GITHUB_EVENT_NAME)",
    )
    args = parser.parse_args(argv)

    changed = changed_files(args.root, args.base)
    bench_changed = [(s, p) for s, p in changed if p.startswith("bench/")]
    if not bench_changed:
        print("bench-integrity: no bench/ changes — OK")
        return 0
    labels = [label.strip() for label in args.labels.split(",") if label.strip()]
    findings = check_label_gate(bench_changed, labels, args.event)
    findings += check_results_integrity(args.root, args.base, bench_changed)
    if findings:
        print(f"bench-integrity: {len(findings)} finding(s):")
        for finding in findings:
            print(f"  {finding}")
        return 1
    print(f"bench-integrity: {len(bench_changed)} bench/ change(s) — OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
