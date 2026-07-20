"""Next-2 baton deliverable-freshness advisory — warn-only, NEVER exit-affecting.

Provenance: the S17 session card's ``⟲ Previous-session review`` note
(``.sessions/2026-07-20-s17-recipe-discovery.md``) proposed this as the natural
next rung after S4's ``check_baton_resolves``. Sibling of the S3/S4/R5/R7/R8/R11
advisories on the same posture="advisory" seam.

Why this exists — the INVERSE of S4. ``check_baton_resolves`` (S4) verifies the
``## Next-2 baton`` names a *path* that still RESOLVES on disk (a dead pointer =
a renamed/deleted file). This advisory catches the opposite failure the S16
incident exposed: the baton names a *deliverable* — a ``check_<name>`` checker or
a ``--<flag>`` CLI option — as work still to build, but that deliverable ALREADY
EXISTS in the tree. That is exactly what stranded a real worker: the baton pointed
the next wake at S16 (``--api-latency`` harness mode) as buildable-now work, but
``--api-latency`` had already shipped (PR #479, GSW-5) — the session hard-synced,
built its orientation, and only the collision-guard grep caught the duplication,
after real tokens were spent. This advisory greps the tree for the baton's named
deliverable and warns when a "build X" baton points at already-shipped work, so a
stale baton surfaces at check time instead of burning a successor's session.

What it does, per ``control/status*.md`` file:
  (a) locate the ``## Next-2 baton`` section (heading -> next ``## `` H2 or EOF);
  (b) extract deliverable-shaped tokens from the section PROSE — not only from
      code spans: real batons name deliverables in running text
      (``S16 (--api-latency harness ...)``), so a code-span-only scan (S4's
      grammar) would miss every real case. A token is deliverable-shaped when it
      matches ``check_[a-z0-9_]+`` (a checker fn/file name) or ``--[a-z][a-z0-9-]*``
      (a long CLI flag);
  (c) SHIPPED-SUPPRESSION: any deliverable token that appears in the baton on a
      line ALSO carrying a completion marker (``shipped`` / ``merged`` / ``landed``
      / ``done`` / ``complete`` / ``already`` / ``exists`` / a ``#<digits>`` PR
      reference) is a deliverable the baton REPORTS as done — never a stale
      to-build target — and is suppressed everywhere in that file. This is the
      tree-analogue of S17's "already-known" guard and is what keeps the advisory
      silent on a healthy heartbeat (where every landed rank carries its PR
      number), while still firing on the S16 shape (a to-build line with no
      completion marker naming a deliverable the heartbeat never acknowledged);
  (d) for each remaining candidate token (on a non-marked line, not shipped-
      suppressed), RESOLVE it precisely against the tree and emit ONE advisory
      finding per already-built deliverable.

Resolution is deliberately PRECISE (this is the real backstop against loose prose
extraction — a token that does not resolve as a genuine deliverable can never
fire, so even a spurious ``--known``-from-``well--known`` token is harmless):
  * ``check_<name>``  -> a ``def <name>(`` definition exists in scanned source,
                        OR a file named ``<name>.py`` exists in the tree.
  * ``--<flag>``      -> an ``add_argument("--<flag>"`` / ``'--<flag>'`` argparse
                        registration exists in scanned source (flag-first form —
                        the codebase's dominant style, e.g. ``--api-latency``).
                        A short-alias-first registration is a deliberate
                        false-negative (fail-open): a missed stale baton is a
                        cheap nudge lost; a false-positive on a shipped item
                        erodes trust, so the bias is toward silence.
A ``def <name>(`` / ``add_argument(...)`` predicate is immune to a docstring
MENTION of the token (this module names ``check_baton_resolves`` / ``--api-latency``
in prose but defines neither), so the checker never self-satisfies.

Scan scope: ``.py`` files under the target, pruning VCS/kit-machinery noise
(``.git`` / ``__pycache__`` / ``node_modules`` / ``.venv`` / ``venv`` /
``.substrate``) and ``tests/`` (a test fixture must not count as a deliverable's
home); ``bootstrap.py`` skipped; files > 512 KiB or non-UTF-8 skipped (fail-open).

Posture — ADVISORY only, wired on the posture="advisory" seam in cli.py exactly
like check_baton_resolves / check_recipe_discovery / check_ungroomed_ideas. NOT in
STRICT_SUBCHECKS — a stale baton is a handoff nudge, not a defect to fail an
adopter on. Input-gated + fail-open: no control/ dir, no status file, no baton
section, or an unreadable file yields nothing. Never raises. Stdlib only.
"""

from __future__ import annotations

import re
from pathlib import Path

from engine.checks.check_docs import Finding

# Reuse S4's section-boundary grammar + control-plane locators as the single
# source of truth, so the two baton advisories can never drift on where the
# ``## Next-2 baton`` section starts/ends or which heartbeat files they cover.
from engine.checks.check_baton_resolves import (
    _CONTROL_RELDIR,
    _RE_BATON_HEADING,
    _RE_H2,
    _STATUS_GLOB,
)

# Named BATON_STALE_DELIVERABLE_KIND (not a bare FINDING_KIND) — the dist
# concatenates every engine module into one namespace, so a second top-level
# FINDING_KIND would collide. The value is the finding kind.
BATON_STALE_DELIVERABLE_KIND = "baton-stale-deliverable"

# Deliverable-shaped tokens, matched anywhere in the baton PROSE (not only code
# spans). A checker fn/file name, or a long CLI flag. Both are anchored to a
# word/flag boundary so a substring of a longer identifier is not clipped out.
_RE_CHECKER_TOKEN = re.compile(r"(?<![\w-])(check_[a-z0-9_]+)")
_RE_FLAG_TOKEN = re.compile(r"(?<![\w-])(--[a-z][a-z0-9-]*)")

# A baton line carrying any of these (case-insensitive) REPORTS its deliverable
# as done — a shipped-and-acknowledged rank, never a stale to-build target — so
# every deliverable token on such a line is suppressed everywhere in that file.
# ``#<digits>`` (a PR/issue reference) is the strongest signal a healthy
# heartbeat attaches to a landed rank; the words cover prose acknowledgements.
_RE_COMPLETION_MARKER = re.compile(
    r"(?i)(?:\bshipped\b|\bmerged\b|\blanded\b|\bdone\b|\bcomplete\b"
    r"|\balready\b|\bexists\b|#\d+|✓)",
)

# Directories never scanned for a deliverable's home (VCS / kit machinery / test
# fixtures — a test that registers a ``--flag`` or defines a ``check_`` helper
# must not count as the deliverable actually existing).
_BATON_FRESH_PRUNE_DIRS = frozenset(
    {".git", "__pycache__", "node_modules", ".venv", "venv", ".substrate", "tests"},
)
_BATON_FRESH_MAX_BYTES = 512 * 1024


def _iter_py_files(root: Path):
    """Yield ``.py`` files under ``root``, pruning VCS/kit/test noise + bootstrap.

    A generator so a huge tree short-circuits the moment every token resolves."""
    stack = [root]
    while stack:
        current = stack.pop()
        try:
            entries = list(current.iterdir())
        except OSError:
            continue  # fail open on an unreadable dir
        for entry in entries:
            try:
                if entry.is_dir():
                    if entry.name not in _BATON_FRESH_PRUNE_DIRS:
                        stack.append(entry)
                    continue
            except OSError:
                continue
            if entry.suffix == ".py" and entry.name != "bootstrap.py":
                yield entry


def _baton_section_lines(text: str) -> list[str]:
    """The raw lines inside the ``## Next-2 baton`` section (heading excluded)."""
    lines = text.splitlines()
    in_section = False
    out: list[str] = []
    for line in lines:
        stripped = line.strip()
        if not in_section:
            if _RE_BATON_HEADING.match(stripped):
                in_section = True
            continue
        if _RE_H2.match(stripped):  # any other H2 closes the section
            break
        out.append(line)
    return out


def _deliverable_tokens(line: str) -> list[str]:
    """The deliverable-shaped tokens (``check_*`` / ``--flag``) on ``line``."""
    tokens: list[str] = []
    tokens += _RE_CHECKER_TOKEN.findall(line)
    tokens += _RE_FLAG_TOKEN.findall(line)
    return tokens


def _partition_baton_tokens(section_lines: list[str]) -> tuple[list[str], set[str]]:
    """Return (candidate to-build tokens in order, shipped-suppressed token set).

    A token on a completion-marked line is SHIPPED-suppressed (added to the set);
    a token on an unmarked line is a candidate. The set suppresses a token file-
    wide, so a deliverable acknowledged done anywhere in the baton is never later
    flagged from a bare context-mention on an unmarked line."""
    candidates: list[str] = []
    shipped: set[str] = set()
    for line in section_lines:
        marked = _RE_COMPLETION_MARKER.search(line) is not None
        for token in _deliverable_tokens(line):
            if marked:
                shipped.add(token)
            else:
                candidates.append(token)
    return candidates, shipped


def _resolves(token: str, files: list[tuple[str, str]]) -> bool:
    """Whether ``token`` resolves as a genuine, already-built deliverable.

    ``files`` is a list of (basename, text) for the scanned ``.py`` sources.
    Precise by construction: a ``def <name>(`` / ``add_argument("<flag>"`` match,
    or (for a checker) a ``<name>.py`` file present — never a mere prose mention."""
    if token.startswith("--"):
        pattern = re.compile(
            r"add_argument\(\s*['\"]" + re.escape(token) + r"['\"]",
        )
        return any(pattern.search(text) for _, text in files)
    # checker token: check_<name>
    def_pattern = re.compile(r"\bdef\s+" + re.escape(token) + r"\s*\(")
    filename = f"{token}.py"
    return any(name == filename or def_pattern.search(text) for name, text in files)


def check_baton_freshness(target: Path, config=None) -> list[Finding]:
    """Advisory: warn when a ``## Next-2 baton`` entry names a ``check_*`` /
    ``--flag`` deliverable as to-build that ALREADY resolves in the tree.

    The inverse of ``check_baton_resolves`` (S4, which flags a path that does NOT
    resolve). Advisory only — the caller wires this on posture="advisory" and
    never counts it toward the exit code. Input-gated + fail-open. ``config``
    accepted for signature parity with the sibling advisories; unused today."""
    control_dir = target / _CONTROL_RELDIR
    if not control_dir.is_dir():
        return []  # input-gated: no control plane here

    # First pass over the heartbeats: collect every distinct candidate token so
    # the (potentially large) tree scan runs at most once, and only when there is
    # a genuine to-build candidate to resolve.
    per_file: list[tuple[str, list[str], set[str]]] = []
    all_candidates: set[str] = set()
    for status_path in sorted(control_dir.glob(_STATUS_GLOB)):
        try:
            text = status_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue  # fail open — an unreadable heartbeat is not a verdict
        candidates, shipped = _partition_baton_tokens(_baton_section_lines(text))
        live = [t for t in candidates if t not in shipped]
        if not live:
            continue
        rel = f"{_CONTROL_RELDIR}/{status_path.name}"
        per_file.append((rel, live, shipped))
        all_candidates.update(live)

    if not all_candidates:
        return []  # nothing to resolve -> silent, no tree walk

    # Load the scanned source corpus once, short-circuiting as soon as every
    # candidate token has resolved (a healthy tree resolves most of them fast).
    resolved: dict[str, bool] = {}
    unresolved = set(all_candidates)
    files: list[tuple[str, str]] = []
    for path in _iter_py_files(target):
        if not unresolved:
            break
        try:
            if path.stat().st_size > _BATON_FRESH_MAX_BYTES:
                continue
            body = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue  # fail open on an unreadable / binary-ish file
        files.append((path.name, body))
        for token in list(unresolved):
            if _resolves(token, [(path.name, body)]):
                resolved[token] = True
                unresolved.discard(token)
    for token in unresolved:
        resolved[token] = False

    findings: list[Finding] = []
    for rel, live, _shipped in per_file:
        seen: set[str] = set()
        for token in live:
            if token in seen or not resolved.get(token):
                continue  # one advisory per distinct already-built token per file
            seen.add(token)
            findings.append(
                Finding(
                    rel,
                    BATON_STALE_DELIVERABLE_KIND,
                    f"the `## Next-2 baton` names `{token}` as work still to "
                    "build, but that deliverable already resolves in the tree — "
                    "a stale baton pointing at already-shipped work strands the "
                    "next wake (the S16 `--api-latency` incident). Verify it is "
                    "shipped and advance the baton to the next real slice (or "
                    "mark the rank done with its PR).",
                ),
            )
    return findings
