#!/usr/bin/env python3
"""check_changelog_structure — the CHANGELOG ``[Unreleased]`` shape checker.

Why + provenance: the 2026-07-09 run close-out's docs-drift audit found the
same defect made twice independently in one run — a ``### Fixed`` block
inserted mid-section, stranding older Added entries under the wrong heading
(KL-4 / PR #14 on main; PR #17's patch re-creating it) — and at every
release cut the KF-5 benchmark prose block accumulated inside the
``[Unreleased]`` body has to be hand-moved so the released-section layout
(prose intro → machine ``<!-- release: … -->`` comment → typed subsections)
comes out right. Design authority:
``docs/ideas/changelog-unreleased-structure-checker-2026-07-09.md``.
Added 2026-07-14 (PR #351). Reliability (PL-008): UNVERIFIED — confirm its
findings against ground truth a few times across sessions before trusting
it; **delete this if it proves unreliable over multiple sessions.**

What it enforces on the ``## [Unreleased]`` section (exit 1 on any finding,
0 clean; only that section is scanned — released sections are history):

1. **unknown-heading** — only the six keep-a-changelog ``###`` headings
   (Added / Changed / Deprecated / Removed / Fixed / Security) may appear.
2. **duplicate-heading** — each typed heading appears at most once (the
   KL-4 failure: a second ``### Fixed`` mid-section strands entries).
3. **heading-order** — the typed headings appear in canonical
   keep-a-changelog order.
4. **early-bullet** — no list item before the first ``###`` heading;
   bullets belong under their typed heading.
5. **tail-prose** — no column-0 prose paragraph after the first ``###``
   heading: free prose (the KF-5 benchmark-outcome blocks) belongs in the
   section PREAMBLE, between ``## [Unreleased]`` and the first ``###``
   heading, so a release cut lifts the preamble verbatim above the machine
   comment with zero hand-reordering.

Fenced code blocks are skipped wholesale; a column-0 line directly under a
non-blank line is treated as a lazy continuation, never flagged (only
paragraph starts fire tail-prose).

Repo-level tooling, not engine code: lives in scripts/, uses print, never
ships in dist/bootstrap.py, runs as a ci.yml kit-quality step next to
check_idea_index.py — adopter repos never receive it. Stdlib only.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import NamedTuple

CHANGELOG_RELPATH = "CHANGELOG.md"

CANONICAL_HEADINGS = (
    "Added",
    "Changed",
    "Deprecated",
    "Removed",
    "Fixed",
    "Security",
)

EXPECTED_LAYOUT = (
    "expected [Unreleased] layout: `## [Unreleased]` -> free prose preamble "
    "(benchmark/KF-5 blocks live HERE) -> typed subsections, each at most "
    "once, in keep-a-changelog order (### Added, ### Changed, "
    "### Deprecated, ### Removed, ### Fixed, ### Security), bullets only "
    "under their typed heading"
)

_UNRELEASED_RE = re.compile(r"^##\s*\[Unreleased\]", re.IGNORECASE)
_SECTION_RE = re.compile(r"^##\s*\[")
_H3_RE = re.compile(r"^###\s+(.*\S)")
_BULLET_RE = re.compile(r"^[-*+]\s")
_FENCE_RE = re.compile(r"^(```|~~~)")


class Finding(NamedTuple):
    path: str
    kind: str
    message: str


def extract_unreleased(text: str) -> tuple[list[str], int] | None:
    """Return ``(lines, start_lineno)`` of the ``[Unreleased]`` body.

    ``lines`` excludes the ``## [Unreleased]`` heading itself and stops
    before the next ``## [`` section heading. ``start_lineno`` is the
    1-based line number of the first body line. ``None`` when the section
    heading is missing entirely.
    """
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if _UNRELEASED_RE.match(line):
            body: list[str] = []
            for nxt in lines[i + 1 :]:
                if _SECTION_RE.match(nxt):
                    break
                body.append(nxt)
            return body, i + 2
    return None


def check_unreleased(text: str, path: str = CHANGELOG_RELPATH) -> list[Finding]:
    """All findings for the ``[Unreleased]`` section of ``text``."""
    findings: list[Finding] = []

    def bad(lineno: int, kind: str, message: str) -> None:
        findings.append(Finding(f"{path}:{lineno}", kind, message))

    extracted = extract_unreleased(text)
    if extracted is None:
        return [
            Finding(
                path,
                "missing-unreleased",
                "no `## [Unreleased]` section found — the release workflow "
                "cuts releases from it; " + EXPECTED_LAYOUT,
            ),
        ]
    body, start = extracted

    seen: dict[str, int] = {}  # canonical heading -> first lineno
    last_rank = -1
    first_h3_seen = False
    in_fence = False
    prev_blank = True

    for offset, line in enumerate(body):
        lineno = start + offset
        if _FENCE_RE.match(line):
            in_fence = not in_fence
            prev_blank = False
            continue
        if in_fence:
            prev_blank = False
            continue

        h3 = _H3_RE.match(line)
        if h3:
            title = h3.group(1).strip()
            if title not in CANONICAL_HEADINGS:
                bad(
                    lineno,
                    "unknown-heading",
                    f"`### {title}` is not a keep-a-changelog heading; "
                    + EXPECTED_LAYOUT,
                )
            else:
                rank = CANONICAL_HEADINGS.index(title)
                if title in seen:
                    bad(
                        lineno,
                        "duplicate-heading",
                        f"`### {title}` already appeared at line "
                        f"{seen[title]} — one heading per type; a second "
                        "block strands the entries between them (the KL-4 "
                        "PR #14 failure); " + EXPECTED_LAYOUT,
                    )
                else:
                    seen[title] = lineno
                    if rank < last_rank:
                        bad(
                            lineno,
                            "heading-order",
                            f"`### {title}` appears after a later-ranked "
                            "heading — canonical order is "
                            f"{' / '.join(CANONICAL_HEADINGS)}; "
                            + EXPECTED_LAYOUT,
                        )
                    last_rank = max(last_rank, rank)
            first_h3_seen = True
            prev_blank = False
            continue

        if not line.strip():
            prev_blank = True
            continue

        if _BULLET_RE.match(line):
            if not first_h3_seen:
                bad(
                    lineno,
                    "early-bullet",
                    "list item before the first `###` heading — bullets "
                    "belong under their typed heading; " + EXPECTED_LAYOUT,
                )
            prev_blank = False
            continue

        # Column-0 prose. Indented lines are entry continuations; a col-0
        # line directly under a non-blank line is a lazy continuation —
        # only a paragraph START (previous line blank) can fire.
        if first_h3_seen and not line[0].isspace() and prev_blank:
            bad(
                lineno,
                "tail-prose",
                "prose paragraph after the first `###` heading — free "
                "prose (KF-5 benchmark blocks) belongs in the [Unreleased] "
                "PREAMBLE, before the first typed heading, so a release "
                "cut lifts it verbatim above the machine comment with no "
                "hand-reordering; " + EXPECTED_LAYOUT,
            )
        prev_blank = False

    return findings


def check_changelog(root: Path) -> list[Finding]:
    changelog = root / CHANGELOG_RELPATH
    if not changelog.is_file():
        return [
            Finding(CHANGELOG_RELPATH, "missing-file", "CHANGELOG.md does not exist"),
        ]
    return check_unreleased(changelog.read_text(encoding="utf-8"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="repo root (default: this script's repo)",
    )
    args = parser.parse_args(argv)
    findings = check_changelog(args.root.resolve())
    for f in findings:
        print(f"{f.path}: [{f.kind}] {f.message}")
    if findings:
        print(f"check_changelog_structure: {len(findings)} finding(s).")
        return 1
    print("check_changelog_structure: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
