#!/usr/bin/env python3
"""check_idea_index — the B4 ideas-frontmatter + index checker (KL-6, plan §5.4).

Why + provenance: B4 ("ideas that ship and survive") needs a machine-readable
outcome record per idea; the founding plan §5.4 rules that the convention and
its checker ship in the same PR (the drift-before-next-session failure mode).
Added 2026-07-09 (band KL-6). Reliability (PL-008): UNVERIFIED — confirm its
findings against ground truth a few times across sessions before trusting it;
**delete this if it proves unreliable over multiple sessions.**

The convention (documented in ``docs/ideas/README.md`` + the planted
``ideas-README`` template): every ``docs/ideas/*.md`` entry except README.md
opens with a flat YAML-subset frontmatter block::

    ---
    state: captured | routed | promoted | historical
    origin: lab | owner | consumer:<owner>/<repo>
    shipped_pr: null | <int>
    shipped_repo: null | <owner>/<repo>
    merged_date: null | YYYY-MM-DD
    outcome: open | shipped | survived | reverted | rejected
    ---

What it enforces (exit 1 on any finding, 0 clean):

1. **Frontmatter grammar** — block present at byte one, all six required keys,
   values in their enums/shapes (unknown extra keys are tolerated — the kit's
   forward-compat posture).
2. **Outcome consistency** — ``shipped|survived|reverted`` require all three
   ship fields non-null; ``open|rejected`` require them null; ``survived``
   additionally requires ``merged_date`` ≥ 30 days old (the D-15/KF-8 survive
   window — a younger idea cannot have survived yet).
3. **Cohort key** — the filename ends ``-YYYY-MM-DD.md`` (B4 groups ideas by
   generation-month cohort, derived from the filename date).
4. **Index consistency** — every idea file is linked from
   ``docs/ideas/README.md``, and every relative ``*.md`` link in the README
   resolves to a file on disk.

Repo-level tooling, not engine code: lives in scripts/, uses print, never
ships in dist/bootstrap.py. Stdlib only (no PyYAML — the frontmatter is a
flat ``key: value`` subset by design so consumers never need a dependency).
"""

from __future__ import annotations

import argparse
import datetime as _dt
import re
import sys
from pathlib import Path
from typing import NamedTuple

IDEAS_RELDIR = "docs/ideas"
README_NAME = "README.md"

REQUIRED_KEYS = (
    "state",
    "origin",
    "shipped_pr",
    "shipped_repo",
    "merged_date",
    "outcome",
)
ALLOWED_STATE = ("captured", "routed", "promoted", "historical")
ALLOWED_OUTCOME = ("open", "shipped", "survived", "reverted", "rejected")
# Outcomes that assert a merged PR exists (ship fields required)…
SHIPPED_OUTCOMES = ("shipped", "survived", "reverted")
# …and outcomes that assert none does (ship fields must be null).
UNSHIPPED_OUTCOMES = ("open", "rejected")
SURVIVE_WINDOW_DAYS = 30  # D-15 / KF-8

_REPO_RE = re.compile(r"^[\w.-]+/[\w.-]+$")
_ORIGIN_RE = re.compile(r"^(lab|owner|consumer:[\w.-]+/[\w.-]+)$")
_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_COHORT_FILENAME_RE = re.compile(r"-\d{4}-\d{2}-\d{2}\.md$")
_KV_RE = re.compile(r"^([A-Za-z_][\w-]*):\s*(.*)$")
# Relative markdown links in the README ([text](file.md) — never absolute URLs).
_MD_LINK_RE = re.compile(r"\]\((?!https?://)([^)#]+\.md)\)")


class Finding(NamedTuple):
    path: str
    kind: str
    message: str


def parse_frontmatter(text: str) -> tuple[dict[str, str] | None, str | None]:
    """Return ``(fields, error)`` for the leading frontmatter block.

    ``fields`` is None when the block is missing/unterminated/malformed, with
    ``error`` saying why. Values are raw strings (``null`` stays literal —
    the validators interpret it).
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, "no frontmatter block at the top of the file (line 1 must be `---`)"
    fields: dict[str, str] = {}
    for i, line in enumerate(lines[1:], start=2):
        if line.strip() == "---":
            return fields, None
        if not line.strip():
            continue
        match = _KV_RE.match(line)
        if not match:
            return None, f"line {i}: not a flat `key: value` pair ({line.strip()!r})"
        fields[match.group(1)] = match.group(2).strip()
    return None, "frontmatter block never closed (missing trailing `---`)"


def _is_null(value: str) -> bool:
    return value in ("null", "~", "")


def validate_fields(
    relpath: str,
    fields: dict[str, str],
    today: _dt.date,
) -> list[Finding]:
    findings: list[Finding] = []

    def bad(kind: str, message: str) -> None:
        findings.append(Finding(relpath, kind, message))

    for key in REQUIRED_KEYS:
        if key not in fields:
            bad("missing-key", f"required frontmatter key `{key}` is missing")
    if findings:
        return findings

    state = fields["state"]
    if state not in ALLOWED_STATE:
        bad("bad-state", f"state {state!r} not in {ALLOWED_STATE}")

    if not _ORIGIN_RE.match(fields["origin"]):
        bad(
            "bad-origin",
            f"origin {fields['origin']!r} must be `lab`, `owner`, or `consumer:<owner>/<repo>`",
        )

    outcome = fields["outcome"]
    if outcome not in ALLOWED_OUTCOME:
        bad("bad-outcome", f"outcome {outcome!r} not in {ALLOWED_OUTCOME}")
        return findings

    pr_raw = fields["shipped_pr"]
    repo_raw = fields["shipped_repo"]
    date_raw = fields["merged_date"]

    if not _is_null(pr_raw) and not pr_raw.isdigit():
        bad("bad-shipped-pr", f"shipped_pr {pr_raw!r} must be null or a PR number")
    if not _is_null(repo_raw) and not _REPO_RE.match(repo_raw):
        bad("bad-shipped-repo", f"shipped_repo {repo_raw!r} must be null or `<owner>/<repo>`")
    merged_date: _dt.date | None = None
    if not _is_null(date_raw):
        if not _DATE_RE.match(date_raw):
            bad("bad-merged-date", f"merged_date {date_raw!r} must be null or YYYY-MM-DD")
        else:
            try:
                merged_date = _dt.date.fromisoformat(date_raw)
            except ValueError:
                bad("bad-merged-date", f"merged_date {date_raw!r} is not a real date")

    ship_fields_null = [_is_null(pr_raw), _is_null(repo_raw), _is_null(date_raw)]
    if outcome in SHIPPED_OUTCOMES and any(ship_fields_null):
        bad(
            "outcome-inconsistent",
            f"outcome `{outcome}` requires shipped_pr + shipped_repo + merged_date "
            "all non-null (it asserts a merged PR exists)",
        )
    if outcome in UNSHIPPED_OUTCOMES and not all(ship_fields_null):
        bad(
            "outcome-inconsistent",
            f"outcome `{outcome}` requires the ship fields to be null "
            "(a built-then-reverted idea is `reverted`, not `rejected`)",
        )
    if outcome == "survived" and merged_date is not None:
        age = (today - merged_date).days
        if age < SURVIVE_WINDOW_DAYS:
            bad(
                "survived-too-young",
                f"outcome `survived` needs merged_date ≥ {SURVIVE_WINDOW_DAYS} days old "
                f"(D-15 survive window); {date_raw} is {age} days old",
            )
    return findings


def check_ideas(root: Path, today: _dt.date | None = None) -> list[Finding]:
    today = today or _dt.date.today()
    findings: list[Finding] = []
    ideas_dir = root / IDEAS_RELDIR
    readme = ideas_dir / README_NAME
    if not ideas_dir.is_dir():
        return [Finding(IDEAS_RELDIR, "missing-dir", "docs/ideas/ does not exist")]
    if not readme.is_file():
        findings.append(
            Finding(f"{IDEAS_RELDIR}/{README_NAME}", "missing-readme", "the backlog index is missing"),
        )
        readme_text = ""
    else:
        readme_text = readme.read_text(encoding="utf-8")

    idea_files = sorted(
        p for p in ideas_dir.glob("*.md") if p.name != README_NAME
    )
    for path in idea_files:
        rel = path.relative_to(root).as_posix()
        if not _COHORT_FILENAME_RE.search(path.name):
            findings.append(
                Finding(rel, "bad-filename", "filename must end `-YYYY-MM-DD.md` (the B4 cohort key)"),
            )
        fields, error = parse_frontmatter(path.read_text(encoding="utf-8"))
        if fields is None:
            findings.append(Finding(rel, "no-frontmatter", error or "unparseable frontmatter"))
        else:
            findings.extend(validate_fields(rel, fields, today))
        if readme_text and path.name not in readme_text:
            findings.append(
                Finding(rel, "not-indexed", "idea file is not linked from docs/ideas/README.md"),
            )

    # Every relative .md link in the README must resolve.
    for match in _MD_LINK_RE.finditer(readme_text):
        target = match.group(1).strip()
        if not (ideas_dir / target).is_file():
            findings.append(
                Finding(
                    f"{IDEAS_RELDIR}/{README_NAME}",
                    "dangling-link",
                    f"backlog link `{target}` does not resolve to a file",
                ),
            )
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="repo root (default: this script's repo)",
    )
    args = parser.parse_args(argv)
    findings = check_ideas(args.root.resolve())
    for f in findings:
        print(f"{f.path}: [{f.kind}] {f.message}")
    if findings:
        print(f"check_idea_index: {len(findings)} finding(s).")
        return 1
    print("check_idea_index: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
