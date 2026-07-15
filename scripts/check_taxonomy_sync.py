#!/usr/bin/env python3
"""check_taxonomy_sync — the task-class taxonomy's three surfaces must agree.

Why + provenance: the PL-004 task-class taxonomy lives on three surfaces that
must agree — the canonical ``MODEL_TASK_CLASSES`` tuple in
``src/engine/grammar.py`` (re-exported as ``TASK_CLASSES`` by
``src/engine/loop/telemetry.py``), the first column of the ladder table in
``telemetry/allocation-ladder.md`` (the surface agents actually read when
picking a model), and the class list in ``telemetry/README.md``. Nothing
enforced the agreement: the PL-010 amendment session (PR #22) updated all
three by hand and also found the class *count* hardcoded in four places. The
next amendment, or a ladder edit that drops/typos a row, can silently desync
them. This converts the convention into enforcement (friction→guard, PL-007).
Idea: ``docs/ideas/taxonomy-surface-sync-checker-2026-07-09.md``.
Added 2026-07-15. Reliability (PL-008): UNVERIFIED — confirm its findings
against ground truth a few times across sessions before trusting it;
**delete this if it proves unreliable over multiple sessions.**

What it enforces (exit 1 on any finding, 0 clean):

1. **Ladder ⇄ canonical set-equality** — the first-column cells of the
   "## The ladder" table (emphasis/flags stripped) equal the canonical
   tuple's class set: no missing row, no extra/typoed row.
2. **README ⇄ canonical set-equality** — the ``·``-separated class list in
   the README's ``task_class ∈`` bullet equals the canonical set.
3. **README count honesty** — the "the N PL-004 classes" number in that
   bullet equals ``len(MODEL_TASK_CLASSES)`` (the hardcoded-count class the
   PL-010 session fixed elsewhere by deriving from the tuple).

The canonical tuple is regex-parsed from ``src/engine/grammar.py`` — the
script stays import-free (repo-level tooling, not engine code: lives in
scripts/, uses print, never ships in dist/bootstrap.py; a parse failure on
any surface is itself a finding, never a silent pass). Stdlib only.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import NamedTuple

GRAMMAR_RELPATH = "src/engine/grammar.py"
LADDER_RELPATH = "telemetry/allocation-ladder.md"
README_RELPATH = "telemetry/README.md"

# The canonical tuple block in grammar.py: `MODEL_TASK_CLASSES = ( ... )`.
_TUPLE_RE = re.compile(
    r"^MODEL_TASK_CLASSES\s*=\s*\((?P<body>.*?)^\)",
    re.MULTILINE | re.DOTALL,
)
_STRING_RE = re.compile(r"\"([^\"]+)\"|'([^']+)'")

# The ladder section: from `## The ladder` to the next `## ` heading (or EOF).
_LADDER_SECTION_RE = re.compile(
    r"^## The ladder[^\n]*\n(?P<body>.*?)(?=^## |\Z)",
    re.MULTILINE | re.DOTALL,
)

# The README class-list bullet: `- `task_class` ∈ the N PL-004 classes …:
# a · b · c.` — a bullet line plus its indented continuations.
_README_BULLET_RE = re.compile(
    r"^- `task_class` ∈ (?P<body>.*?)(?=^\S|^- |\Z)",
    re.MULTILINE | re.DOTALL,
)
_README_COUNT_RE = re.compile(r"the (\d+) PL-004 classes")


class Finding(NamedTuple):
    path: str
    kind: str
    message: str


def _strip_cell(cell: str) -> str:
    """Normalize a ladder cell: drop emphasis marks and trailing flag glyphs."""
    cell = cell.strip()
    cell = cell.strip("`*_").strip()
    # Trailing flag glyphs (e.g. ` ⚑`) are annotations, not class-name bytes.
    cell = cell.rstrip("⚑⚠️ ").strip()
    return cell


def parse_canonical(text: str) -> list[str]:
    """The MODEL_TASK_CLASSES entries, in tuple order ([] when unparseable)."""
    match = _TUPLE_RE.search(text)
    if not match:
        return []
    return [a or b for a, b in _STRING_RE.findall(match.group("body"))]


def parse_ladder(text: str) -> list[str] | None:
    """First-column cells of the ladder table's body rows (None = unparseable)."""
    section = _LADDER_SECTION_RE.search(text)
    if not section:
        return None
    rows: list[str] = []
    table_lines = [
        line.strip()
        for line in section.group("body").splitlines()
        if line.strip().startswith("|")
    ]
    if len(table_lines) < 2:
        return None
    for line in table_lines[1:]:  # skip the header row
        first_cell = line.strip("|").split("|", 1)[0]
        cell = _strip_cell(first_cell)
        if not cell or set(cell) <= {"-", ":"}:  # the |---| separator row
            continue
        rows.append(cell)
    return rows


def parse_readme(text: str) -> tuple[list[str] | None, int | None]:
    """(class list, declared count) from the task_class bullet (None = unparseable)."""
    match = _README_BULLET_RE.search(text)
    if not match:
        return None, None
    bullet = " ".join(match.group("body").split())
    count_match = _README_COUNT_RE.search(bullet)
    count = int(count_match.group(1)) if count_match else None
    # The class list follows the bullet's final colon; the classes themselves
    # never contain one. Trailing period is prose, not class bytes.
    if ":" not in bullet:
        return None, count
    tail = bullet.rsplit(":", 1)[1].strip().rstrip(".")
    classes = [c.strip() for c in tail.split("·") if c.strip()]
    return (classes or None), count


def _set_findings(
    path: str, surface: str, got: list[str], canonical: list[str]
) -> list[Finding]:
    findings: list[Finding] = []
    got_set, canon_set = set(got), set(canonical)
    for missing in sorted(canon_set - got_set):
        findings.append(
            Finding(
                path,
                f"{surface}-missing-class",
                f"canonical class `{missing}` (MODEL_TASK_CLASSES, "
                f"{GRAMMAR_RELPATH}) is absent from this surface",
            ),
        )
    for extra in sorted(got_set - canon_set):
        findings.append(
            Finding(
                path,
                f"{surface}-extra-class",
                f"`{extra}` is not a canonical class — extra or typoed "
                f"entry (canonical tuple: {GRAMMAR_RELPATH})",
            ),
        )
    return findings


def check_taxonomy(root: Path) -> list[Finding]:
    findings: list[Finding] = []

    grammar_path = root / GRAMMAR_RELPATH
    if not grammar_path.is_file():
        return [Finding(GRAMMAR_RELPATH, "missing-file", "grammar module not found")]
    canonical = parse_canonical(grammar_path.read_text(encoding="utf-8"))
    if not canonical:
        return [
            Finding(
                GRAMMAR_RELPATH,
                "grammar-unparsed",
                "could not parse the MODEL_TASK_CLASSES tuple",
            ),
        ]

    ladder_path = root / LADDER_RELPATH
    if not ladder_path.is_file():
        findings.append(Finding(LADDER_RELPATH, "missing-file", "ladder not found"))
    else:
        ladder = parse_ladder(ladder_path.read_text(encoding="utf-8"))
        if ladder is None:
            findings.append(
                Finding(
                    LADDER_RELPATH,
                    "ladder-unparsed",
                    "could not parse the `## The ladder` table",
                ),
            )
        else:
            findings.extend(
                _set_findings(LADDER_RELPATH, "ladder", ladder, canonical),
            )

    readme_path = root / README_RELPATH
    if not readme_path.is_file():
        findings.append(Finding(README_RELPATH, "missing-file", "README not found"))
    else:
        classes, count = parse_readme(readme_path.read_text(encoding="utf-8"))
        if classes is None:
            findings.append(
                Finding(
                    README_RELPATH,
                    "readme-unparsed",
                    "could not parse the `task_class ∈` class-list bullet",
                ),
            )
        else:
            findings.extend(
                _set_findings(README_RELPATH, "readme", classes, canonical),
            )
        if count is not None and count != len(canonical):
            findings.append(
                Finding(
                    README_RELPATH,
                    "readme-count-drift",
                    f"bullet says `the {count} PL-004 classes` but "
                    f"MODEL_TASK_CLASSES has {len(canonical)} entries",
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
    findings = check_taxonomy(args.root.resolve())
    for f in findings:
        print(f"{f.path}: [{f.kind}] {f.message}")
    if findings:
        print(f"check_taxonomy_sync: {len(findings)} finding(s).")
        return 1
    print("check_taxonomy_sync: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
