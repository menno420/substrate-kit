"""Generic session-log completeness checker (config-driven port).

The session workflow asks every session to end with a
``<sessions_dir>/<date>-<slug>.md`` log that carries a set of required markers
(by default: a Status badge, a session-idea flag, and a previous-session review).
Each marker is a ``{"label", "needle"}`` pair from ``substrate.config.json``, so a
host tunes the ritual without touching engine code.

Unlike the host's version this port does **not** shell out to ``git`` to pick the
"current" log — ``subprocess`` is banned in engine code and is host-CI sugar
anyway. The current log is the newest ``*.md`` by mtime under ``sessions_dir``
(the CLI also accepts an explicit ``--file``). Pure stdlib; returns the missing
markers rather than printing.
"""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from pathlib import Path


def missing_markers(text: str, markers: Sequence[Mapping[str, str]]) -> list[str]:
    """Return the labels of markers whose needle is absent from ``text``.

    Tolerant of partial host-config entries: a marker without a ``needle`` is
    skipped (nothing to search for) rather than raising, and a missing
    ``label`` reports as ``"?"``.
    """
    lower = text.lower()
    return [
        m.get("label", "?")
        for m in markers
        if m.get("needle") and m.get("needle", "").lower() not in lower
    ]


def latest_session_log(sessions_dir: Path) -> Path | None:
    """Best guess at this session's log: newest ``*.md`` by mtime (skip README)."""
    if not sessions_dir.is_dir():
        return None
    candidates = [p for p in sessions_dir.glob("*.md") if p.name != "README.md"]
    if not candidates:
        return None
    return max(candidates, key=lambda p: p.stat().st_mtime)


# Status-badge values that mean "this session is not finished yet". A card
# carrying one is INCOMPLETE even when every marker needle is present — the
# born-red discipline checks the status VALUE, not just the badge's presence.
# (KL-1 lesson, kit repo PR #9: a reopened card kept its idea/review markers
# from the previous PR, so a presence-only check read born-red as green and
# auto-merge landed the PR without its close-out.) ``drafted`` is the
# auto-draft state (KL-5): an auto-drafted skeleton is real write-back but
# not a finished session — drafted holds the gate exactly like born-red.
IN_PROGRESS_TOKENS = ("in-progress", "in progress", "wip", "hold", "drafted")

# The auto-draft judgment-slot opener (KL-5). Drafted text marks every field
# only the session can fill with ``[[fill: <hint>]]``; a card still carrying
# one is DRAFTED, not completed — a distinct, mechanically countable state
# between "nothing written" (the twice-measured Phase-2.5 baseline) and a
# genuine close-out. The needle-based markers may all be present in a draft
# (the stand-ins carry them on purpose), so this token is what keeps an
# unedited draft from counting complete.
DRAFT_FILL_TOKEN = "[[fill:"

# Inline code spans + fenced blocks are stripped before counting: a card
# whose prose *mentions* the token (`[[fill:]]` in backticks — session cards
# about the draft mechanism legitimately do) is not an unresolved slot; the
# draft always writes real slots bare.
_CODE_SPAN_RE = re.compile(r"`[^`\n]*`")
_FENCE_RE = re.compile(r"^```.*?^```", re.MULTILINE | re.DOTALL)


def unresolved_fill_count(text: str) -> int:
    """Return how many auto-draft ``[[fill:]]`` slots remain in ``text``.

    Counts only slots outside inline code spans and fenced code blocks —
    prose that *talks about* the token doesn't hold the gate.
    """
    stripped = _CODE_SPAN_RE.sub("", _FENCE_RE.sub("", text))
    return stripped.count(DRAFT_FILL_TOKEN)


def status_in_progress(text: str) -> bool:
    """True when the log's Status badge line carries an in-progress value."""
    for line in text.splitlines():
        if "**status:**" in line.lower():
            lowered = line.lower()
            return any(token in lowered for token in IN_PROGRESS_TOKENS)
    return False


def check_log(path: Path, markers: Sequence[Mapping[str, str]]) -> list[str]:
    """Return what keeps one log file from counting complete (all if unreadable).

    Three conditions feed the list: marker needles that are absent, a Status
    badge still carrying an in-progress value, and unresolved auto-draft
    ``[[fill:]]`` slots (the drafted-vs-completed distinction, KL-5 — a
    drafted card is named as drafted, never mistaken for a finished one).
    """
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return [m["label"] for m in markers]
    missing = missing_markers(text, markers)
    fills = unresolved_fill_count(text)
    if fills:
        missing.append(
            f"{fills} auto-draft [[fill:]] slot(s) unresolved "
            "(the card is drafted, not completed)",
        )
    if status_in_progress(text):
        missing.append("a completed Status (badge still says in-progress)")
    return missing
