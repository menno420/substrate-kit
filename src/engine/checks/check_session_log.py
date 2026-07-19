"""Generic session-log completeness checker (config-driven port).

The session workflow asks every session to end with a
``<sessions_dir>/<date>-<slug>.md`` log that carries a set of required markers
(by default: a Status badge, a session-idea flag, and a previous-session review).
Each marker is a ``{"label", "needle"}`` pair from ``substrate.config.json``, so a
host tunes the ritual without touching engine code.

Unlike the host's version this module does **not** shell out to ``git`` to pick
the "current" log — ``subprocess`` is banned in engine *checker* code (§3.2).
:func:`latest_session_log` (newest ``*.md`` by mtime under ``sessions_dir``) is
only the LAST-RESORT guess: the CLI's fallback lane derives the card set from
the merge-base diff vs ``origin/main`` itself (``engine.cli.
_derive_diff_session_cards``, a documented §3.2 carve-out — the sim-lab V051
false-green showed a post-merge sibling card carries the freshest mtime and the
mtime guess validates the WRONG card), and CI workflows pass ``check
--session-log <file>`` with the card the PR's diff touches (a fresh checkout
flattens every mtime to checkout time). Pure stdlib; returns the missing
markers rather than printing.
"""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from pathlib import Path

from engine.grammar import (
    EXACT_MODEL_ID_RE,
    MODEL_LINE_NEEDLE,
    MODEL_LINE_TAUGHT_FORMAT,
    MODEL_TASK_CLASSES,
    parse_model_payload,
)


def _marker_miss(marker: Mapping[str, str]) -> str:
    """Name one missed marker: its label AND the exact byte-form expected.

    ``Model line (expected `📊 Model:`)`` instead of a bare ``Model line`` —
    the run-1 ON-arm false-red lesson (idea
    model-line-checker-false-red-2026-07-09): a card visibly carrying a
    ``> **Model:**`` line red as "missing: Model line" tells the agent
    nothing about WHICH byte-form the needle scan wanted. A red must name
    the expected form, never contradict what the agent can see on the card.
    """
    label = marker.get("label", "?") or "?"
    needle = marker.get("needle", "")
    return f"{label} (expected `{needle}`)" if needle else label


def missing_markers(text: str, markers: Sequence[Mapping[str, str]]) -> list[str]:
    """Return, for each marker whose needle is absent from ``text``, its
    label plus the expected byte-form (see :func:`_marker_miss`).

    Tolerant of partial host-config entries: a marker without a ``needle`` is
    skipped (nothing to search for) rather than raising, and a missing
    ``label`` reports as ``"?"``.
    """
    lower = text.lower()
    return [
        _marker_miss(m)
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


# The engine's own draft provenance marker (engine.loop.handoff stamps it on
# every auto-drafted card/section). Mirrored here — not imported — because
# checks/ sits below loop/ in the module order and the marker is a stable
# one-line contract; ``tests/test_handoff.py`` pins the two constants equal.
AUTO_DRAFT_MARKER = "<!-- substrate:auto-draft -->"


def is_unadopted_draft(text: str) -> bool:
    """True when a card is an engine-authored auto-draft no session adopted.

    Only the engine's ``draft_card`` writes the ``drafted`` Status value, and
    it stamps :data:`AUTO_DRAFT_MARKER` alongside; the card's own badge text
    instructs the adopting session to flip the badge. Both present = a pure
    machine skeleton — the previous session ended without touching its card
    and the Stop-hook seam drafted one from evidence.

    Why the distinction matters (B1 run-8): the ON arm ended with ``check
    --strict`` exit=1 solely because of a skeleton the ENGINE wrote — the
    next cold session would arrive to a red repo it did not redden and
    cannot honestly close (the judgment slots belong to the departed
    session). The bare mtime-fallback ``check`` lane treats such a card as
    an ADVISORY (adopt it: verify the evidence, resolve the slots, flip the
    badge); the merge-gate lanes (``--require-session-log`` /
    ``--session-log`` / ``--added-card``) still hold RED — a PR shipping a
    drafted card is the born-red discipline working as designed.
    """
    return AUTO_DRAFT_MARKER in text and _status_value_drafted(text)


# The badge VALUE is the backticked span right after ``**Status:**`` (the
# grammar every drafted/documented card writes); a badge that skips
# backticks contributes the bare remainder of its line instead. Trailing
# prose after a backticked value is commentary, never state.
_STATUS_VALUE_RE = re.compile(r"\*\*status:\*\*\s*`([^`]+)`", re.IGNORECASE)
_STATUS_BARE_RE = re.compile(r"\*\*status:\*\*\s*(.+)", re.IGNORECASE)


def _status_badge_value(text: str) -> str | None:
    """Return the Status badge's declared VALUE, or ``None`` without one.

    Prefers the backticked span (`` `complete` ``); falls back to the bare
    remainder of the badge line (leading emphasis markers stripped) for
    badges that don't backtick their value. Only the FIRST badge line is
    read — same single-badge contract the substring scan had.
    """
    for line in text.splitlines():
        if "**status:**" in line.lower():
            match = _STATUS_VALUE_RE.search(line)
            if match:
                return match.group(1).strip()
            match = _STATUS_BARE_RE.search(line)
            if match:
                return match.group(1).strip().strip("*_").strip()
            return None
    return None


def _value_declares(value: str, tokens: tuple[str, ...]) -> bool:
    """True when the badge ``value`` declares one of ``tokens``.

    A token counts only at the START of the value and on a word boundary:
    `` `hold` — waiting`` declares ``hold``; ``holding`` declares nothing.
    """
    lowered = value.lower()
    for token in tokens:
        rest = lowered[len(token) : len(token) + 1]
        if lowered.startswith(token) and (not rest or not rest.isalnum()):
            return True
    return False


def _status_value_drafted(text: str) -> bool:
    """True when the Status badge's VALUE is the auto-draft ``drafted``
    — a substring scan would misread a badge whose trailing prose says
    "*(auto-drafted by substrate-kit …)*" after a session flips the value
    to ``in-progress`` (adoption must end the advisory)."""
    value = _status_badge_value(text)
    return value is not None and value.lower() == "drafted"


def status_in_progress(text: str) -> bool:
    """True when the Status badge's declared VALUE is an in-progress one.

    Judged on the parsed badge VALUE (:func:`_status_badge_value`), never a
    whole-line substring scan: badge prose legitimately contains hold
    tokens — the auto-draft provenance "*(auto-drafted by substrate-kit
    …)*" contains "drafted" — and the old substring scan false-held a
    ``complete`` card over its own commentary (a latent false-hold class on
    the merge-blocking gate; found via the #420 sham fixture).
    """
    value = _status_badge_value(text)
    return value is not None and _value_declares(value, IN_PROGRESS_TOKENS)


def has_status_badge(text: str) -> bool:
    """True when the log carries any Status badge line at all."""
    return any("**status:**" in line.lower() for line in text.splitlines())


# The added-card born-red HOLD message (the superbot-games #40 loophole
# fix). Callers that need to route this finding differently (the CLI gives
# it its own finding kind so the designed-hold banner can recognise it)
# match on this exact string — keep it a single module-level constant.
BORN_RED_HOLD_MESSAGE = (
    "born-red HOLD: this PR ADDS a session card that declares an "
    "in-progress/drafted Status — the gate holds the merge red until the "
    "card flips complete (designed hold, not a defect). Without this hold "
    "a card-only born-red PR with auto-merge pre-armed merges the instant "
    "CI reports (superbot-games #40 merged in 24 s on exactly this)."
)


# The no-badge Status grammar finding (a session card carries a Status badge
# LINE from its first commit — born-red exempts the badge's VALUE, never its
# presence). Shipped for the added-card lane and graduated into ``check_log``
# — the modified-card lane — for full lane parity. Both lanes emit this exact
# string via :func:`_status_grammar_findings`; keep it a single constant.
NO_BADGE_MESSAGE = (
    "a Status badge line (expected `> **Status:**`) — a session card "
    "carries one from its first commit; born-red exempts the badge's "
    "VALUE, never its presence"
)


# The valueless Status-badge grammar finding (the #422 card's filed 💡,
# shipped for the added-card lane in PR #426 and graduated into ``check_log``
# — the modified-card lane — here). Both lanes emit this exact string so a
# valueless badge is named identically wherever it is caught; keep it a
# single module-level constant.
VALUELESS_BADGE_MESSAGE = (
    "a Status badge VALUE (expected a backticked value on the badge "
    "line, e.g. `> **Status:** in-progress` or `> **Status:** "
    "complete`) — the badge line is present but declares no value; "
    "a valueless badge claims nothing, so it can neither hold as "
    "born-red nor be graded as a completed close-out"
)


def _status_grammar_findings(text: str) -> list[str]:
    """Status-badge grammar shared by both card-check lanes.

    A well-formed session card carries a Status badge line, and that badge
    carries a value. Both are grammar rules — about the badge's *presence*,
    not its born-red *value* — so the added-card and modified-card lanes must
    enforce them identically, or a card malformed in one lane slips through
    the other. Returns the first grammar finding (at most one), or [] when clean.
    """
    if not has_status_badge(text):
        return [NO_BADGE_MESSAGE]
    if not _status_badge_value(text):
        return [VALUELESS_BADGE_MESSAGE]
    return []


def _last_model_payload(text: str) -> dict | None:
    """Last-valid ``📊 Model:`` payload on a card, or ``None`` when none parses.

    Mirrors :func:`engine.checks.check_model_line.model_line_findings`'
    last-valid-wins candidate scan — but reused HERE (this module sits below
    ``check_model_line`` in the dist module order, so the reverse edge would be
    circular), sharing only the grammar leaf ``engine.grammar.parse_model_payload``
    + the needle constant. Code spans / fenced blocks and ``[[fill:]]`` stand-in
    lines are not reports (a card whose prose mentions the needle, or a draft's
    stand-in line, is skipped). **Fail-open:** a card with no parseable needle
    line returns ``None`` and the caller stays silent — marker PRESENCE is the
    session-log gate's job (:func:`missing_markers`), never this helper's.
    """
    stripped = _CODE_SPAN_RE.sub("", _FENCE_RE.sub("", text))
    last_valid: dict | None = None
    for line in stripped.splitlines():
        if MODEL_LINE_NEEDLE not in line or DRAFT_FILL_TOKEN in line:
            continue
        parsed = parse_model_payload(line.split(MODEL_LINE_NEEDLE, 1)[1])
        if parsed is not None:
            last_valid = parsed
    return last_valid


def _task_class_findings_for_card(text: str) -> list[str]:
    """The EXIT-AFFECTING PL-004 task-class check for a single ADDED card (R13).

    The fleet-wide payload lint (:func:`engine.checks.check_model_line.
    check_model_line`) enforces the same rule — segment-3 of the ``📊 Model:``
    line must prefix-match one of the 9 :data:`engine.grammar.MODEL_TASK_CLASSES`
    — but it is **advisory-only** and **windowed to the newest cards**, so an
    off-taxonomy class on a NEW card merges green. This helper is the
    exit-affecting half: the born-red added-card lane grades the PR's OWN card,
    so an off-taxonomy PRESENT class reds at CI exactly like an unflipped
    born-red badge. Scope stays the single added card (never a historical/merged
    one), so it can never retroactively redden an existing card.

    **Fail-open on absence:** a card with no parseable ``📊 Model:`` line (or a
    line malformed such that no task-class parses) yields nothing — that case is
    already owned by the marker checks (:func:`check_log` / ``missing_markers``);
    double-reddening it here would be noise. Only an off-taxonomy PRESENT class
    reds. Reuses the shared parser + class tuple; does not duplicate either.
    """
    payload = _last_model_payload(text)
    if payload is None:
        return []
    task_class = payload["task_class"]
    if any(task_class.startswith(known) for known in MODEL_TASK_CLASSES):
        return []
    known = " | ".join(MODEL_TASK_CLASSES)
    return [
        f"an off-taxonomy `{MODEL_LINE_NEEDLE}` task-class {task_class!r} on "
        f"this added card — it does not prefix-match any of the "
        f"{len(MODEL_TASK_CLASSES)} PL-004 classes ({known}); fix this card's "
        f"line to the taught form `{MODEL_LINE_TAUGHT_FORMAT}` (family-level "
        "model \N{MIDDLE DOT} effort \N{MIDDLE DOT} PL-004 task class; see "
        ".sessions/README.md)"
    ]


def _exact_model_id_findings_for_card(text: str) -> list[str]:
    """The EXIT-AFFECTING exact-model-ID check for a single ADDED card (R14).

    The sibling of :func:`_task_class_findings_for_card`, one segment over: the
    fleet-wide payload lint (:func:`engine.checks.check_model_line.
    check_model_line`) enforces the same rule — segment-1 of the ``📊 Model:``
    line is a FAMILY-LEVEL model name (``opus-4.8``, ``fable-5``), never an
    exact model-ID token (``claude-opus-4-8`` and co. — the ORDER 012
    fleet-reporting bar) — but it is **advisory-only** and **windowed to the
    newest cards**, so an exact-ID segment-1 on a NEW card merges green. This
    helper is the exit-affecting half: the born-red added-card lane grades the
    PR's OWN card, so an exact-ID PRESENT model segment reds at CI exactly like
    an unflipped born-red badge. Scope stays the single added card (never a
    historical/merged one), so it can never retroactively redden an existing
    card.

    **Fail-open on absence:** a card with no parseable ``📊 Model:`` line (or a
    ``[[fill:]]`` / code-span / family-level model segment) yields nothing —
    the missing-line case is already owned by the marker checks
    (:func:`check_log` / ``missing_markers``), and a family-level name is
    exactly what the rule wants. Only an exact-model-ID PRESENT segment reds.
    Reuses the shared parser + :data:`engine.grammar.EXACT_MODEL_ID_RE`; does
    not duplicate either.
    """
    payload = _last_model_payload(text)
    if payload is None:
        return []
    model = payload["model"]
    if not EXACT_MODEL_ID_RE.search(model):
        return []
    return [
        f"an exact-model-ID `{MODEL_LINE_NEEDLE}` model segment {model!r} on "
        "this added card — record the family-level model name only (e.g. "
        "`fable-5`, `opus-4.8`), never an exact model ID, dated or not (fleet "
        f"reporting bar, ORDER 012); fix this card's line to the taught form "
        f"`{MODEL_LINE_TAUGHT_FORMAT}` (family-level model \N{MIDDLE DOT} "
        "effort \N{MIDDLE DOT} PL-004 task class; see .sessions/README.md)"
    ]


def check_added_card(path: Path, markers: Sequence[Mapping[str, str]]) -> list[str]:
    """Grade a card newly ADDED by a PR (the gate's added-card lane).

    The venture-lab #15 false-green class: the generated gate exempts an
    ADDED card from the locked door so a born-red heartbeat can merge — but
    the old exemption skipped the card ENTIRELY, so a card that declared
    itself ``complete`` while missing its grammar tokens (💡 / ``📊 Model:``)
    merged green and pre-reddened every later bare ``check --strict`` run
    via the newest-by-mtime fallback (fixed only by the next upgrade wave).

    Judge the added card by what it *declares*, never by mid-flight
    completeness —

    - **no Status badge at all** → a grammar finding: every session card
      carries a parseable ``> **Status:**`` badge from its first commit
      (the born-red convention *requires* the badge; it exempts the VALUE).
    - **badge line present but VALUELESS** (``> **Status:**`` with nothing
      after it — :func:`_status_badge_value` parses ``None``) → a grammar
      finding that HOLDS. Before this branch a valueless badge fell through
      to the completeness check below exactly as if it had declared
      ``complete`` — a card that declares NOTHING must never be graded as a
      claimed close-out and released on its markers (the #422 card's filed
      💡, same value-grammar family as the value-parse fix).
    - **badge declares in-progress/drafted** → the born-red **HOLD**
      (:data:`BORN_RED_HOLD_MESSAGE`): the PR is a mid-flight session and
      must stay red until the card flips complete. This supersedes the
      #168 full exemption — "exempt" meant GREEN, and a green card-only
      diff with auto-merge pre-armed merged 24 seconds after open
      (superbot-games #40, the v1.9.0 wave's premature-merge finding).
      Born-red incompleteness is still never graded (no marker findings) —
      the hold is a single designed-state finding, not a completeness red.
    - **badge declares anything else** (``complete`` & co.) → the card
      claims to be a finished close-out, so it gets the full
      :func:`check_log` completeness check — missing markers and unresolved
      ``[[fill:]]`` slots red exactly as they would on a MODIFIED card — PLUS
      the exit-affecting PL-004 task-class check (R13,
      :func:`_task_class_findings_for_card`) AND the exit-affecting
      exact-model-ID check (R14, :func:`_exact_model_id_findings_for_card`): an
      off-taxonomy ``📊 Model:`` task-class OR an exact-model-ID model segment
      on the PR's OWN card reds here, each scoped to this single added card so
      no historical card is retroactively reddened. (The fleet-wide
      :func:`engine.checks.check_model_line.check_model_line` window stays
      advisory-only and windowed — this is its exit-affecting, own-card half.)
    """
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return ["an unreadable added card (cannot grammar-check)"]
    # The no-badge and valueless-badge grammar findings are shared with the
    # modified-card lane (:func:`_status_grammar_findings`) so a card-grammar
    # finding can never live in one lane and not the other. Either returns at
    # most one finding and HOLDS the added-card lane.
    grammar = _status_grammar_findings(text)
    if grammar:
        return grammar
    value = _status_badge_value(text)
    if _value_declares(value, IN_PROGRESS_TOKENS):
        return [BORN_RED_HOLD_MESSAGE]
    # Complete-branch: the card claims a finished close-out. Full completeness
    # check PLUS the exit-affecting PL-004 task-class check (R13) AND the
    # exit-affecting exact-model-ID check (R14) — all scoped to this single
    # added card. An off-taxonomy `📊 Model:` class OR an exact-model-ID model
    # segment reds here exactly like an unflipped born-red badge; a
    # missing/malformed line stays silent (fail-open — the marker checks own
    # that case).
    findings = check_log(path, markers)
    findings.extend(_task_class_findings_for_card(text))
    findings.extend(_exact_model_id_findings_for_card(text))
    return findings


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
        return [_marker_miss(m) for m in markers]
    missing = missing_markers(text, markers)
    fills = unresolved_fill_count(text)
    if fills:
        missing.append(
            f"{fills} auto-draft [[fill:]] slot(s) unresolved "
            "(the card is drafted, not completed)",
        )
    if status_in_progress(text):
        missing.append("a completed Status (badge still says in-progress)")
    # Shared card-grammar findings (no-badge / valueless), the same the
    # added-card lane blocks — a card whose Status badge line is absent, or
    # present but valueless, makes ``status_in_progress`` False (no value →
    # not in-progress), so without this a card malformed in its badge grammar
    # with all markers present passes ``check_log`` clean. Extracted into
    # :func:`_status_grammar_findings` so the two lanes cannot drift (the
    # no-badge half graduated here; the valueless half is the #426 close).
    missing.extend(_status_grammar_findings(text))
    return missing
