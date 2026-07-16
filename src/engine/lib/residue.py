"""Shared wholesale-replacement residue guard for KL-5 drafted surfaces.

Why + provenance: the KL-5 generalization of S3's archive-note residue probe
(idea filed on the archive-probe-s3 session card, PR #414). Every KL-5
drafted surface — the auto-drafted session card (``loop/handoff.py``), the
archive-ready note (``loop/archive.py``), and any future ``ensure_draft``
sibling — shares the same sham corridor: completeness is counted by
``[[fill:]]`` tokens, so a surface whose slots were "resolved" by stripping
the markers while keeping the drafted default/hint text in place *looks*
done while carrying no session knowledge at all. S3 built the fingerprint
answer for archive notes; this module lifts the mechanism into a shared,
surface-agnostic seam so every drafted surface points at ONE implementation
(the S4 rule — "reused verbatim; no second fingerprint implementation" —
applied at lib level).

The mechanism (unchanged from S3): a guarded body is fingerprinted as
whitespace-normalized word shingles (:data:`RESIDUE_SHINGLE_WORDS`
consecutive words — long enough that genuine session text cannot collide
with drafted instruction text by accident, short enough that keeping even
one full default line still trips the guard); any shingle surviving in the
probed text means the slot was NOT wholesale-replaced. A body still wrapped
in its intact ``[[fill: …]]`` markers is *unresolved*, not residue — the
fill-token count owns that report.

This module also owns the canonical session-card judgment-slot hints
(:data:`CARD_GUARDED_HINTS`): ``loop/handoff.py`` draws its ``_fill()``
hints from these constants, so the drafted text and the fingerprints can
never drift apart (one source, the same no-second-copy rule the archive
probe applies by extracting bodies from the shipped template).

Layering: pure stdlib, no engine imports — ``lib/`` sits below ``checks/``
and ``loop/``, so both the checkers and the drafters may import from here.
:data:`RESIDUE_FILL_TOKEN` mirrors ``checks.check_session_log.
DRAFT_FILL_TOKEN`` (which this module must not import — checks/ sits above
lib/); ``tests/test_residue.py`` pins the two constants equal, the same
mirror-pin contract ``AUTO_DRAFT_MARKER`` already uses.
"""

from __future__ import annotations

import re
from collections.abc import Sequence

# Mirror of ``checks.check_session_log.DRAFT_FILL_TOKEN`` — pinned equal by
# tests/test_residue.py (lib/ must not import checks/).
RESIDUE_FILL_TOKEN = "[[fill:"

# Shingle window: runs of this many whitespace-normalized words fingerprint
# a guarded body (the S3 calibration, unchanged — see module docstring).
RESIDUE_SHINGLE_WORDS = 8

# Inline code spans + fenced blocks are stripped before probing a prose
# surface: text that *quotes* a drafted hint (session cards about the draft
# mechanism legitimately do, in backticks or fences) is not residue. Mirrors
# of ``checks.check_session_log._CODE_SPAN_RE`` / ``_FENCE_RE`` — pinned
# pattern-equal by tests/test_residue.py, same reason as the token above.
_RESIDUE_CODE_SPAN_RE = re.compile(r"`[^`\n]*`")
_RESIDUE_FENCE_RE = re.compile(r"^```.*?^```", re.MULTILINE | re.DOTALL)


def strip_code_regions(text: str) -> str:
    """Return ``text`` with fenced blocks and inline code spans removed."""
    return _RESIDUE_CODE_SPAN_RE.sub("", _RESIDUE_FENCE_RE.sub("", text))


def residue_normalize_ws(text: str) -> str:
    """Collapse all whitespace runs to single spaces (re-wrap-proof)."""
    return " ".join(text.split())


def residue_shingles(body: str, words: int = RESIDUE_SHINGLE_WORDS) -> set[str]:
    """Word-run fingerprints of a guarded body, whitespace-normalized.

    A body shorter than the window fingerprints as one whole-body shingle;
    an empty/whitespace-only body fingerprints as nothing (never matches).
    """
    tokens = residue_normalize_ws(body).split(" ")
    if tokens == [""]:
        return set()
    if len(tokens) <= words:
        return {" ".join(tokens)}
    return {" ".join(tokens[i : i + words]) for i in range(len(tokens) - words + 1)}


def probe_residue(
    text: str,
    guarded: Sequence[tuple[str, str]],
    *,
    fill_token: str = RESIDUE_FILL_TOKEN,
    shingle_words: int = RESIDUE_SHINGLE_WORDS,
) -> list[str]:
    """Return the names of guarded bodies whose default text survives in ``text``.

    ``guarded`` is ``(name, body)`` pairs — the body is the drafted default /
    hint text between the ``[[fill:`` and ``]]`` markers. Empty list = every
    guarded body was wholesale-replaced (or still sits inside its intact
    markers, which the fill-token count already reports as *unresolved* — a
    marker-carrying slot is never residue). Callers own the finding message;
    this core reports guilty names only, in ``guarded`` order.
    """
    normalized = residue_normalize_ws(text)
    guilty: list[str] = []
    for name, body in guarded:
        # Intact-slot skip: the slot may have been drafted with or without a
        # space after the token — both normalize distinctly, so check both.
        intact_forms = {
            residue_normalize_ws(f"{fill_token}{body}]]"),
            residue_normalize_ws(f"{fill_token} {body}]]"),
        }
        if any(form and form in normalized for form in intact_forms):
            continue
        if any(s in normalized for s in residue_shingles(body, shingle_words)):
            guilty.append(name)
    return guilty


# ---------------------------------------------------------------------------
# The session-card surface — canonical judgment-slot hints
# ---------------------------------------------------------------------------

# The drafted judgment hints ``loop/handoff.py`` writes into every card
# draft, named. Handoff imports these constants for its ``_fill()`` calls,
# so the fingerprints track the drafted text without a second copy to
# drift (tests/test_residue.py additionally pins each hint into a real
# ``draft_card`` render). The generic host-marker fallback hint
# ("resolve this marker") is deliberately NOT guarded: it is three common
# words — too short to fingerprint without false positives.
CARD_HINT_VERIFY_RESULT = "verify result — the engine cannot execute commands"
CARD_HINT_VERIFY_HOW = "how this session was verified (command + result)"
CARD_HINT_DECISIONS = "decisions taken this session, or none"
CARD_HINT_POINTER = "the handoff pointer — where to pick up"
CARD_HINT_IDEA = "one idea you genuinely believe in — never filler"
CARD_HINT_REVIEW = (
    "one genuine remark on the previous session + one workflow improvement"
)
CARD_HINT_MODEL = "model \N{MIDDLE DOT} effort \N{MIDDLE DOT} task-class (Q-0248 taxonomy)"

CARD_GUARDED_HINTS: tuple[tuple[str, str], ...] = (
    ("verify result", CARD_HINT_VERIFY_RESULT),
    ("verify command+result", CARD_HINT_VERIFY_HOW),
    ("decisions", CARD_HINT_DECISIONS),
    ("handoff pointer", CARD_HINT_POINTER),
    ("session idea", CARD_HINT_IDEA),
    ("previous-session review", CARD_HINT_REVIEW),
    ("model line", CARD_HINT_MODEL),
)


def probe_card_residue(text: str) -> list[str]:
    """Return guilty judgment-slot names for one session card's text.

    Code spans and fenced blocks are stripped first (cards that *discuss*
    the draft mechanism quote hints in backticks — prose mentions are not
    residue), then the card is probed against every canonical drafted hint.
    """
    return probe_residue(strip_code_regions(text), CARD_GUARDED_HINTS)
