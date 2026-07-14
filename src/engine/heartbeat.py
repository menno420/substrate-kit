"""Mechanical heartbeat writer — the ``bootstrap heartbeat`` verb's logic.

Why + provenance: the control protocol's LAST step — overwriting
``control/status.md`` with a fresh heartbeat — was hand-assembled markdown,
and the hand-written ``updated:`` timestamp is the failure surface the idea
file names (``docs/ideas/heartbeat-verb-2026-07-09.md``, ORDER 019 item 7):
a session that writes ``updated: 2026-7-9 13:00`` (unparseable) goes red for
formatting, not for darkness, and a routine wake has to template the whole
file by hand in its prompt. The engine already owns atomic writes, UTC time,
and the contract text — this module closes the gap with two lanes:

- **Restamp lane** (:func:`restamp_status`, the default) — non-destructive
  preserve-and-restamp: ONLY the ``updated:`` timestamp token (always a
  parseable UTC now) plus the heartbeat fields the caller explicitly passes
  are rewritten; ⚑ blocks, ORDER ledger lines, ``claimed-by`` annotations,
  and every human-authored section survive **byte-identical**. This is the
  mechanical fix for the fleet-wide heartbeat-staleness class.
- **Full-write lane** (:func:`full_status`, behind an explicit ``--full``) —
  the idea file's contract-shape whole-file writer ("overwrite-own semantics
  preserved — whole-file write, never append") for the first real heartbeat
  over the adopt seed; missing flags default honestly (``blockers: none``,
  ``⚑ needs-owner: none``).

Grammar is kit-owned with ONE home — ``engine.grammar`` (EAP §6.8): the
``updated:`` and ``kit:`` lines are located via the SAME ``UPDATED_LINE_RE``
/ ``KIT_LINE_RE`` / ``KIT_VERSION_TOKEN_RE`` constants the ``check``
enforcers consume, and every write is round-tripped through
``check_status_current.parse_heartbeat`` before it leaves this module (the
idea file's write → parse → equal recipe), so the writer can never emit a
heartbeat the enforcer rejects. Stdlib only; sits below ``cli.py`` (which
owns the file I/O via ``atomic_write_text``) and imports only grammar +
``check_status_current``'s parser.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone

from engine.checks.check_status_current import parse_heartbeat
from engine.grammar import KIT_LINE_RE, KIT_VERSION_TOKEN_RE, UPDATED_LINE_RE

# The heartbeat's field lines, exactly as control/README.md § "status.md
# format" teaches them (flag name → line label). Order matters: it is the
# contract shape full_status renders.
HEARTBEAT_FIELD_LABELS = {
    "phase": "phase:",
    "health": "health:",
    "last_shipped": "last-shipped:",
    "blockers": "blockers:",
    "orders": "orders:",
    "needs_owner": "⚑ needs-owner:",
    "notes": "notes:",
}


class HeartbeatError(ValueError):
    """A heartbeat write that cannot proceed non-destructively.

    Raised instead of guessing: a missing field line, an unparseable
    ``updated:`` stamp (the adopt seed), or a ``kit:`` line without a
    version token each name their fix in the message — never a silent
    whole-file clobber.
    """


def utc_stamp(now: datetime | None = None) -> str:
    """Render the canonical ``updated:`` timestamp (UTC, seconds precision).

    The exact shape ``grammar.updated_line_example`` teaches
    (``2026-07-10T12:00:00Z``) — always parseable by ``parse_heartbeat``.
    """
    moment = now or datetime.now(timezone.utc)
    return moment.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _verify_roundtrip(text: str, stamp: str) -> str:
    """Assert ``text``'s heartbeat parses back to ``stamp``; return ``text``.

    The idea file's write → parse → equal recipe, run on every write (not
    just in tests): the writer half and the enforcer half
    (``check_status_current.parse_heartbeat``) can never disagree silently.
    """
    parsed = parse_heartbeat(text)
    expected = datetime.strptime(stamp, "%Y-%m-%dT%H:%M:%SZ").replace(
        tzinfo=timezone.utc
    )
    if parsed != expected:
        msg = (
            "internal round-trip failure: the written heartbeat did not "
            f"parse back to {stamp} — refusing to emit an unparseable file."
        )
        raise HeartbeatError(msg)
    return text


def _replace_field_line(text: str, label: str, value: str) -> str:
    """Replace the first ``<label> …`` line's value; the rest stays put."""
    pattern = re.compile(rf"^({re.escape(label)}\s*).*$", re.MULTILINE)
    match = pattern.search(text)
    if match is None:
        msg = (
            f"no `{label}` line found — the restamp lane only rewrites "
            "existing field lines (non-destructive); add the line by hand "
            "or write a fresh contract-shape heartbeat with --full."
        )
        raise HeartbeatError(msg)
    return text[: match.start()] + match.group(1) + value + text[match.end() :]


def _replace_kit_version(text: str, version: str) -> str:
    """Rewrite the ``kit:`` line's ``v<X.Y.Z>`` token, decorations intact."""
    line = KIT_LINE_RE.search(text)
    if line is None:
        msg = (
            "no parseable `kit:` line found (grammar: KIT_LINE_RE — keep "
            "the token PLAIN, never bold) — add one, or write a fresh "
            "contract-shape heartbeat with --full."
        )
        raise HeartbeatError(msg)
    token = KIT_VERSION_TOKEN_RE.search(text, line.start(), line.end())
    if token is None:
        msg = (
            "the `kit:` line carries no `v<X.Y.Z>` version token to "
            "rewrite — fix the line by hand (format: control/README.md "
            '§ "status.md format").'
        )
        raise HeartbeatError(msg)
    return text[: token.start()] + f"v{version}" + text[token.end() :]


def restamp_status(
    text: str,
    *,
    now: datetime | None = None,
    fields: dict[str, str] | None = None,
    kit_version: str | None = None,
) -> str:
    """Return ``text`` with ONLY the mechanical heartbeat fields rewritten.

    - The ``updated:`` line's timestamp token becomes a fresh UTC now;
      everything after the token (live heartbeats decorate the line) is
      preserved byte-for-byte.
    - Each entry in ``fields`` (flag name → new value, labels per
      :data:`HEARTBEAT_FIELD_LABELS`) replaces that field line's value.
    - ``kit_version`` rewrites the ``kit:`` line's version token only.

    Everything not named is preserved **byte-identical** — ⚑ blocks, ORDER
    ledger lines, ``claimed-by`` annotations, prose sections. Raises
    :class:`HeartbeatError` (never guesses) when the existing heartbeat
    doesn't parse — an adopt seed or a hand-mangled stamp is a case for
    ``--full`` or a hand fix, not for a silent rewrite of unknown content.
    """
    match = UPDATED_LINE_RE.search(text)
    if match is None or parse_heartbeat(text) is None:
        msg = (
            "no parseable `updated:` ISO-8601 heartbeat in the existing "
            "file — still the adopt seed? Write the first real heartbeat "
            "with --full (whole-file contract shape), which is the seed's "
            "own documented overwrite path."
        )
        raise HeartbeatError(msg)
    stamp = utc_stamp(now)
    result = text[: match.start(1)] + stamp + text[match.end(1) :]
    for name, value in (fields or {}).items():
        result = _replace_field_line(result, HEARTBEAT_FIELD_LABELS[name], value)
    if kit_version is not None:
        result = _replace_kit_version(result, kit_version)
    return _verify_roundtrip(result, stamp)


def full_status(
    project_name: str,
    kit_version: str,
    *,
    phase: str,
    now: datetime | None = None,
    health: str = "green",
    orders: str = "acked= done=",
    last_shipped: str = "none",
    blockers: str = "none",
    needs_owner: str = "none",
    notes: str = "none",
    kit_check: str = "green",
    kit_engaged: str = "yes",
) -> str:
    """Render the exact contract-shape heartbeat (the idea file's lane).

    The taught block from control/README.md § "status.md format", field for
    field; missing flags default honestly (``blockers: none``,
    ``⚑ needs-owner: none`` — the idea file's named defaults). ``phase`` has
    no honest default — what the seat is doing is the one thing only the
    caller knows — so it is required. The render is round-tripped through
    the enforcer's parser before it leaves.
    """
    stamp = utc_stamp(now)
    text = (
        f"# {project_name} · status\n"
        f"updated: {stamp}\n"
        f"phase: {phase}\n"
        f"health: {health}\n"
        f"kit: v{kit_version} · check: {kit_check} · engaged: {kit_engaged}\n"
        f"last-shipped: {last_shipped}\n"
        f"blockers: {blockers}\n"
        f"orders: {orders}\n"
        f"⚑ needs-owner: {needs_owner}\n"
        f"notes: {notes}\n"
    )
    return _verify_roundtrip(text, stamp)
