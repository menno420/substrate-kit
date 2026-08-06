"""check_boot_path — the boot pointer chain must RESOLVE.

The kit already ships a reachability checker, and it points the wrong way.
``check_docs``'s ``[reachable]`` finding asserts that every live doc is
reachable FROM the read path — it catches an orphan. Nothing asserted the
inverse: that the read path's own targets EXIST. A boot pointer into a missing
file is invisible to every guard the kit has.

That gap has a measured cost. ``render.agreement_home`` records that on
2026-07-12 a dead ``.claude/CLAUDE.md`` boot pointer was "verified live in 3/3
adopters" and fixed: the rendered router stopped naming a file the default
adopt only STAGES, and instead said *"the boot set lives in the working
agreement"*. On 2026-08-06 that fix was checked against 11 adopter trees:

  * **5** carried the new router text pointing at an agreement with **no boot
    section at all** (gba-homebrew, pokemon-mod-lab, superbot-mineverse,
    superbot-next, venture-lab);
  * **6** still carried the old numbered list naming ``.claude/CLAUDE.md``;
  * **0 of 11** had a boot pointer that resolved end to end.

The fix moved the deadness rather than removing it, and the second form is
harder to see than the first — which is exactly why it survived 25 days. A
pointer nobody checks decays silently, and a boot pointer is the first thing a
cold session reads.

So this checker walks the chain a booting session actually walks:

  1. the **agreement** the router names (``render.agreement_home``) exists;
  2. that agreement carries a **boot section** — the list, in one home;
  3. every **path** the boot section names resolves on disk.

DETERMINISTIC by the ``guards.ADVISORY_CENSUS`` definition: each leg is a file
that is present or absent, and a heading that is there or not. No prose
inference, no aging, no judgement — so its findings belong in the agent's
channel rather than the routed heuristic tail.

**Not gate-wired yet, deliberately.** 11 of 11 adopters would red, and the fix
is a hand-edit per repo (planted docs are skip-if-exists, so ``upgrade`` will
not add the section to an existing agreement). Ship it visible, let the fleet
converge, and promote it when ``check --gate-preview`` says the sweep is clean
— the ``gate_ready`` distinction the census already carries.

Stdlib-only, no subprocess, no I/O at import (§3.2).
"""

from __future__ import annotations

import re
from pathlib import Path

from engine.checks.check_docs import Finding
from engine.render import agreement_home

# NOTE on the import above: it MUST be module-level, not lazy inside the
# function. build_bootstrap strips lines beginning `from engine` when it
# concatenates the engine into the single-file dist (_INTRA_PKG_PREFIXES) —
# the names already live in the same file by then. A lazy `from engine.render
# import ...` inside a function body is NOT at the start of a line, so the
# stripper never sees it, and the dist raises ModuleNotFoundError at runtime
# the first time the checker runs. Caught by the bench's cold-adoption arc
# (tests/test_bench.py) on 2026-08-06, which exercises the built dist rather
# than the source layout — the only place this class of bug is visible.

# The boot section's heading, matched case-insensitively on the `##` line. Kept
# deliberately loose across the phrasings already live in the fleet rather than
# pinned to one string — a repo that calls it "Reading order" is not defective.
_BOOT_HEADING = re.compile(
    r"^##\s+.*\b(boot\s+read\s+path|boot\s+set|reading\s+order|read\s+path|"
    r"start\s+every\s+session)\b",
    re.IGNORECASE,
)

# A repo-relative path named in the boot list: a backticked token that looks
# like a path (has a slash or a known doc extension). Bare prose in backticks
# (`complete`, `--strict`) is deliberately NOT a path and must not be checked —
# a false positive here would be exactly the noise this estate just spent a
# session removing.
_PATH_TOKEN = re.compile(r"`([^`\s]+\.(?:md|py|json|ya?ml)|[^`\s]*/[^`\s]+)`")

# Ordered-list lines inside the boot section — the numbered steps a session
# reads. Only these are scanned for paths, so a later paragraph mentioning some
# other file cannot manufacture a finding.
_LIST_LINE = re.compile(r"^\s*(?:\d+[.)]|[-*])\s+")


def _boot_section(text: str) -> list[str] | None:
    """The lines of the agreement's boot section, or None when it has none."""
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if _BOOT_HEADING.match(line):
            start = index + 1
            break
    if start is None:
        return None
    body: list[str] = []
    for line in lines[start:]:
        if line.startswith("## "):
            break
        body.append(line)
    return body


def check_boot_path(target: Path, config) -> list[Finding]:
    """Walk the boot pointer chain; report every leg that does not resolve.

    Self-quiet on a bare tree: a repo with no agreement at all is pre-adoption,
    not broken, and `adopt` is what plants one.
    """
    findings: list[Finding] = []
    relpath = agreement_home(target)
    agreement = target / relpath

    # Self-gate on adoption evidence, like check_engagement. A tree with no
    # rendered doc set has no boot path to be wrong about — it is
    # pre-adoption, and `adopt` is what plants one. Without this, `check` on a
    # bare tree reds before the repo has onboarded, and the cold-adoption smoke
    # arc reds on its own first step.
    docs_root = target / getattr(config, "docs_root", "docs")
    if not docs_root.is_dir() and not agreement.is_file():
        return []

    if not agreement.is_file():
        # The router names it and a cold session opens it first. Absent is the
        # 3/3-adopter class from 2026-07-12 — the original dead pointer.
        return [
            Finding(
                relpath,
                "boot-agreement-missing",
                f"the orientation router names `{relpath}` as the working "
                "agreement holding the boot set, but no such file exists — a "
                "cold session's first read resolves to nothing. Plant it "
                "(`adopt`) or point the router at the agreement this repo "
                "actually has.",
            )
        ]

    text = agreement.read_text(encoding="utf-8", errors="replace")
    body = _boot_section(text)
    if body is None:
        # The 2026-08-06 class: the router was repointed here, but here has no
        # list. The pointer resolves to a file and then stops.
        return [
            Finding(
                relpath,
                "boot-section-missing",
                f"`{relpath}` exists but carries no boot-read-path section, "
                "while docs/AGENT_ORIENTATION.md points here for the boot set "
                "— so the pointer resolves to a file and then dead-ends. Add a "
                "`## Boot read path` section listing what to read at session "
                "start (one list, one home).",
            )
        ]

    seen: set[str] = set()
    for line in body:
        if not _LIST_LINE.match(line):
            continue
        for token in _PATH_TOKEN.findall(line):
            candidate = token.strip("/")
            if candidate in seen:
                continue
            seen.add(candidate)
            if (target / candidate).exists():
                continue
            findings.append(
                Finding(
                    relpath,
                    "boot-path-unresolved",
                    f"the boot read path names `{candidate}`, which does not "
                    "exist in this repo — every session is told to read it "
                    "first. Fix the path, or drop the entry if the doc is gone.",
                )
            )
    return findings
