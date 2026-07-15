#!/usr/bin/env python3
"""check_retro_index — docs/retro reachability checker (no unindexed retro file).

Why + provenance: the 2026-07-09 wind-down addendum (PR #76) merged into
``docs/retro/`` WITHOUT a README index line and stayed invisible to every
orientation route that starts at the index — despite self-flagging the
follow-up — until a gen-2-boot reconcile pass (#78) added the line. Parallel
wind-down lanes collide on the shared index file and defer the line "until
after X merges"; that deferral is exactly what got lost. This checker converts
the index convention into enforcement (friction→guard), mirroring
``check_idea_index.py``'s index-consistency leg (its enforcement item 4) over
``docs/retro/``. Idea: ``docs/ideas/retro-docs-reachability-checker-2026-07-10.md``.
Added 2026-07-15. Reliability (PL-008): UNVERIFIED — confirm its findings
against ground truth a few times across sessions before trusting it;
**delete this if it proves unreliable over multiple sessions.**

What it enforces (exit 1 on any finding, 0 clean):

1. **Index consistency** — every ``docs/retro/*.md`` except ``README.md`` is
   linked from ``docs/retro/README.md`` (substring match on the filename, the
   same rule ``check_idea_index.py`` applies to the ideas backlog).
2. **Link integrity** — every relative ``*.md`` link in the README resolves to
   a file on disk. Links may leave the directory (the real corpus points at
   ``../succession/README.md`` and ``../gen2/next-boot.md``); they are resolved
   against ``docs/retro/``.

Unlike the ideas checker there is no frontmatter/cohort grammar here — retro
files are free-form review prose; reachability is the whole convention.

Repo-level tooling, not engine code: lives in scripts/, uses print, never
ships in dist/bootstrap.py. Stdlib only.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import NamedTuple

RETRO_RELDIR = "docs/retro"
README_NAME = "README.md"

# Relative markdown links in the README ([text](file.md) — never absolute
# URLs). Same shape as check_idea_index._MD_LINK_RE.
_MD_LINK_RE = re.compile(r"\]\((?!https?://)([^)#]+\.md)\)")


class Finding(NamedTuple):
    path: str
    kind: str
    message: str


def check_retro(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    retro_dir = root / RETRO_RELDIR
    readme = retro_dir / README_NAME
    if not retro_dir.is_dir():
        return [Finding(RETRO_RELDIR, "missing-dir", "docs/retro/ does not exist")]
    if not readme.is_file():
        findings.append(
            Finding(
                f"{RETRO_RELDIR}/{README_NAME}",
                "missing-readme",
                "the retro index is missing",
            ),
        )
        readme_text = ""
    else:
        readme_text = readme.read_text(encoding="utf-8")

    for path in sorted(p for p in retro_dir.glob("*.md") if p.name != README_NAME):
        rel = path.relative_to(root).as_posix()
        if readme_text and path.name not in readme_text:
            findings.append(
                Finding(
                    rel,
                    "not-indexed",
                    "retro file is not linked from docs/retro/README.md — an "
                    "unindexed retro doc is invisible to every orientation "
                    "route that starts at the index (the PR #76 class)",
                ),
            )

    # Every relative .md link in the README must resolve (../ allowed —
    # the corpus points at sibling docs/ directories).
    for match in _MD_LINK_RE.finditer(readme_text):
        target = match.group(1).strip()
        if not (retro_dir / target).is_file():
            findings.append(
                Finding(
                    f"{RETRO_RELDIR}/{README_NAME}",
                    "dangling-link",
                    f"index link `{target}` does not resolve to a file",
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
    findings = check_retro(args.root.resolve())
    for f in findings:
        print(f"{f.path}: [{f.kind}] {f.message}")
    if findings:
        print(f"check_retro_index: {len(findings)} finding(s).")
        return 1
    print("check_retro_index: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
