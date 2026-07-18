#!/usr/bin/env python3
"""check_no_false_walls — CI guard against writing ANY false agent-capability
limitation into a forward-binding surface.

THIN WRAPPER (2026-07-18): the grammar, blocklist, and clearing logic moved into
the engine (``src/engine/checks/check_no_false_walls.py``) so that
``bootstrap.py check --strict`` runs it as a finding leg on EVERY adopter with
zero per-repo wiring (an adopter authoring a false wall into its own local docs
is now caught by its generated CI, not only substrate-kit's own tree). This tool
keeps working for substrate-kit's own CI and **delegates to that engine module —
no duplicate logic.** It scans the KIT-only forward surfaces adopters do not
have (``src/engine/templates/*.tmpl``, ``skills/skills.py``) *plus* the adopter
surfaces (live ``docs/``, root ``CONSTITUTION.md`` / ``CAPABILITIES.md``, live
``.claude/**``) via the shared scanner.

OWNER'S PRINCIPLE (the reason this check exists — bake it in, do not soften it):
**agents have NO owner-imposed limitations.** A capability refusal, when it
happens at all, is a TRANSIENT auto-mode-classifier state — so any wall written
down is stale on the very next platform update AND it makes the next session not
even try. The docs must record **capabilities, never limitations.** The genuine,
momentary refusals still get recorded — but as DATED ledger rows / ``LAST-VERIFIED``
walls that carry their own expiry, never as forward-binding standing doctrine.

GROUND TRUTH (owner-confirmed, proven ~20× live on 2026-07-18): merging is
NORMAL agent work; so is deploying / pushing / arming.

Full grammar + false-positive discipline (CODE rules, dated walls, missing-input
requests, and repudiations all PASS) live in the engine module's docstring.

Repo-level tooling: stdlib only (the engine module it imports is stdlib-only
too — no third-party/pytest dep), uses print, never ships in dist/bootstrap.py.
Reliability (PL-008): UNVERIFIED at birth — confirm its findings against ground
truth a few times across sessions before trusting it; **delete this if it proves
unreliable over multiple sessions.** Added 2026-07-18; generalized past merge
2026-07-18; grammar ported to the engine (single home) 2026-07-18.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import NamedTuple

_REPO_ROOT = Path(__file__).resolve().parents[1]
_SRC = _REPO_ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

# The single home for the grammar/blocklist/clearing + line scanner + the
# adopter-surface collector (no duplicate logic — this wrapper only adds the
# kit-only surfaces adopters lack).
from engine.checks.check_no_false_walls import (  # noqa: E402
    iter_adopter_files,
    scan_text,
)


class Finding(NamedTuple):
    path: str
    line: int
    phrase: str
    rule: str


def _iter_kit_files(root: Path) -> list[Path]:
    """The KIT-only forward-binding surfaces adopters do not have.

    ``src/engine/templates/*.tmpl`` (the doctrine sources that render into every
    adopter's docs) and ``src/engine/skills/skills.py`` (the skill bodies). The
    adopter-shared surfaces (docs, constitution, capabilities, .claude) come
    from :func:`iter_adopter_files`.
    """
    targets: list[Path] = []
    tdir = root / "src" / "engine" / "templates"
    if tdir.is_dir():
        targets.extend(sorted(tdir.rglob("*.tmpl")))
    skills = root / "src" / "engine" / "skills" / "skills.py"
    if skills.is_file():
        targets.append(skills)
    return targets


def _iter_target_files(root: Path) -> list[Path]:
    """Every forward-binding surface: kit-only sources + adopter surfaces."""
    seen: set[Path] = set()
    out: list[Path] = []
    for path in [*_iter_kit_files(root), *iter_adopter_files(root, "docs")]:
        if path in seen:
            continue
        seen.add(path)
        out.append(path)
    return out


def check_file(path: Path, root: Path) -> list[Finding]:
    rel = path.relative_to(root).as_posix()
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return []
    return [Finding(rel, hit.line, hit.phrase, hit.rule) for hit in scan_text(text)]


def check_tree(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in _iter_target_files(root):
        findings.extend(check_file(path, root))
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--root",
        type=Path,
        default=_REPO_ROOT,
        help="repo root (default: this script's repo)",
    )
    args = parser.parse_args(argv)
    findings = check_tree(args.root.resolve())
    for f in findings:
        print(f"{f.path}:{f.line}: [{f.rule}] false merge-wall phrasing: {f.phrase!r}")
    if findings:
        print(
            f"check_no_false_walls: {len(findings)} finding(s) — a forward-binding "
            "surface asserts a FALSE 'agents cannot merge' wall. Merging is normal "
            "agent work; correct or date-stamp/repudiate the line."
        )
        return 1
    print("check_no_false_walls: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
