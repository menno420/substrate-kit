"""Claim-aware checker — order-claims must be unique and live (ORDER 007).

Why + provenance: the fleet coordination protocol (``control/README.md`` §
"Claiming an order") makes every ``new`` order single-executor. Before
building, a lane appends ``claimed-by: <order-ids> <lane-or-session>
<ISO8601>`` to the ``orders:`` line of its OWN heartbeat (``control/status*.md``)
and lands it on main FIRST — so two readers of the same ``status: new`` order
cannot both execute it. That convention was born from a realized failure, not
a theoretical one (substrate-kit PRs #50/#51: two lanes independently executed
the same ORDER 005 the same day, and a whole session's work had to be
reconciled as twins). But the convention shipped **doc-only** — enforced by
nothing. This checker closes the "enforce, don't exhort" gap for the claim
band, exactly as ``check_inbox_append`` did for the append-only law and
``check_owner_actions`` did for the OWNER-ACTION format.

What it flags (both **advisory** — a nudge, never a locked door, the same
posture as the staleness + owner-action warnings):

- ``claims-duplicate`` — two or more DISTINCT heartbeat files carry a
  ``claimed-by:`` naming the SAME order id. That is the twin-execution race
  itself: the tiebreak (earliest claim merged to main wins) is a human call,
  so the checker surfaces the collision rather than picking a winner.
- ``claims-stale`` — a live ``claimed-by:`` for an order that is (a) already
  reported in some lane's ``done=`` (the executor was meant to DROP the claim
  when moving the id into ``done=`` — a lingering claim on a done order is
  dead), or (b) older than the convention's ~24h abandonment horizon (a claim
  with no fresh activity "may be treated as abandoned and re-claimed"). The
  checker cannot see build activity from the status file alone, so the age
  finding is deliberately a *withdraw-or-refresh* nudge, not a verdict.

Posture is **advisory-only, never exit-affecting** — the deliberate mirror of
``check_owner_actions`` / ``check_status_current``'s staleness warning. Claims
are a coordination hint the manager reconciles; a hard gate would red a
required check on a race the checker can't adjudicate.

Input-gated on the ``control/`` protocol and per heartbeat file, like every
control-band checker. Pure stdlib — no ``subprocess`` (§3.2); it only reads the
heartbeat files the fast lane already validates. Unreadable / claim-less files
fail open (no verdict).
"""

from __future__ import annotations

import re
from collections.abc import Sequence
from datetime import datetime, timezone
from pathlib import Path

from engine.checks.check_docs import Finding
from engine.checks.check_status_current import (
    CONTROL_README_RELPATH,
    INBOX_RELPATH,
    heartbeat_relpaths,
)

# The convention's abandonment horizon (control/README.md § "Claims expire"):
# a claim with no visible activity after ~24h may be re-claimed. Seeded here,
# revisable by data (KF-8 posture), mirroring check_status_current's constant.
CLAIM_STALE_HOURS = 24

# The orders line carries the claim + the done ledger:
#   orders: acked=<ids> done=<ids> [claimed-by: <ids> <lane> <ISO8601>]
_ORDERS_RE = re.compile(r"^orders:\s*(.*)$", re.MULTILINE)
_DONE_RE = re.compile(r"\bdone=(\S*)")
# claimed-by: <ids> <lane-or-session> <ISO8601> — three whitespace tokens.
# The ids token is `+`/`,`-separated (README example: `007+008`); the lane may
# itself carry hyphens (`coordinator-lane`) so it is a whole token, not parsed.
_CLAIMED_RE = re.compile(r"claimed-by:\s*(\S+)\s+(\S+)\s+(\S+)")


def _norm_id(raw: str) -> str | None:
    """Return a 3-digit-normalized order id (``7`` / ``007`` → ``007``), or None."""
    token = raw.strip()
    if not token.isdigit():
        return None
    return f"{int(token):03d}"


def _expand_ids(token: str) -> set[str]:
    """Expand an id list token to a normalized id set.

    Handles the protocol's shapes: comma lists (``001,002``), ``+``-joined
    claim ids (``007+008``), and inclusive ranges (``001-006``). Unparseable
    fragments are skipped rather than crashing the scan.
    """
    ids: set[str] = set()
    for part in re.split(r"[,+]", token):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            lo_raw, _, hi_raw = part.partition("-")
            lo, hi = lo_raw.strip(), hi_raw.strip()
            if lo.isdigit() and hi.isdigit():
                for n in range(int(lo), int(hi) + 1):
                    ids.add(f"{n:03d}")
                continue
        norm = _norm_id(part)
        if norm is not None:
            ids.add(norm)
    return ids


def _parse_iso(raw: str) -> datetime | None:
    """Parse a claim's ISO-8601 timestamp to an aware UTC datetime, or None.

    Mirrors ``check_status_current.parse_heartbeat``'s normalization: a
    trailing ``Z`` is rewritten for ``fromisoformat`` (Python 3.10 floor) and
    a naive stamp is read as UTC (the contract says ISO8601, sessions write
    UTC — treating it otherwise would fabricate staleness).
    """
    token = raw.strip()
    if token.endswith(("Z", "z")):
        token = token[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(token)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _orders_line(text: str) -> str | None:
    """Return the first ``orders:`` line's value, or None when absent."""
    match = _ORDERS_RE.search(text)
    return match.group(1) if match else None


def _done_ids(orders_value: str) -> set[str]:
    """Return the set of order ids reported in ``done=`` on an orders line."""
    match = _DONE_RE.search(orders_value)
    return _expand_ids(match.group(1)) if match else set()


def _claim(orders_value: str) -> tuple[set[str], str, datetime | None] | None:
    """Return ``(ids, lane, ts)`` for the line's ``claimed-by:``, or None.

    ``ids`` is the normalized claimed order-id set, ``lane`` the claimant
    token, ``ts`` the parsed timestamp (None when unparseable — the age check
    then simply skips, never fabricating staleness).
    """
    match = _CLAIMED_RE.search(orders_value)
    if not match:
        return None
    ids = _expand_ids(match.group(1))
    if not ids:
        return None
    return ids, match.group(2), _parse_iso(match.group(3))


def check_claims(
    target: Path,
    *,
    status_files: Sequence[str] | None = None,
    now: datetime | None = None,
) -> list[Finding]:
    """Return advisory findings for duplicate / stale order-claims.

    Scans every configured heartbeat file's ``orders:`` line for
    ``claimed-by:`` annotations (ORDER 007). Emits ``claims-duplicate`` when
    two distinct files claim one order id, and ``claims-stale`` when a live
    claim names an order already in some lane's ``done=`` or is older than
    ``CLAIM_STALE_HOURS``. Advisory by contract — callers must never count
    these toward an exit code (see module docstring). Empty when the
    ``control/`` protocol is absent, and fail-open on unreadable files.
    """
    relpaths = heartbeat_relpaths(status_files)
    control_evidence = [INBOX_RELPATH, CONTROL_README_RELPATH, *relpaths]
    if not any((target / rel).is_file() for rel in control_evidence):
        return []

    now = now or datetime.now(timezone.utc)
    # Per file: its claim (ids, lane, ts). Plus the union of every done= ledger
    # across lanes — an order done anywhere retires its claim everywhere.
    claims: dict[str, tuple[set[str], str, datetime | None]] = {}
    done_union: set[str] = set()
    for rel in relpaths:
        path = target / rel
        if not path.is_file():
            continue  # a missing heartbeat is check_status_current's finding
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue  # fail open — an unreadable file is not a verdict
        orders_value = _orders_line(text)
        if orders_value is None:
            continue
        done_union |= _done_ids(orders_value)
        claim = _claim(orders_value)
        if claim is not None:
            claims[rel] = claim

    findings: list[Finding] = []

    # DUPLICATE — one order id claimed by two or more distinct files.
    holders: dict[str, list[str]] = {}
    for rel, (ids, _lane, _ts) in claims.items():
        for oid in ids:
            holders.setdefault(oid, []).append(rel)
    for oid in sorted(holders):
        rels = sorted(holders[oid])
        if len(rels) < 2:
            continue
        who = ", ".join(f"{r} ({claims[r][1]})" for r in rels)
        for rel in rels:
            findings.append(
                Finding(
                    rel,
                    "claims-duplicate",
                    f"order {oid} is claimed by {len(rels)} lanes ({who}) — "
                    "the twin-execution race (control/README.md § Claiming an "
                    "order). Reconcile by the tiebreak (earliest claim merged "
                    "to main wins); the loser withdraws its claim and stands "
                    "down.",
                ),
            )

    # STALE — a live claim for a done order, or one past the ~24h horizon.
    for rel in sorted(claims):
        ids, _lane, ts = claims[rel]
        done_here = sorted(ids & done_union)
        if done_here:
            findings.append(
                Finding(
                    rel,
                    "claims-stale",
                    f"claim for order(s) {', '.join(done_here)} that already "
                    "appear in a lane's done= — the executor drops the "
                    "claimed-by annotation when moving ids into done= "
                    "(control/README.md § Claiming an order). Withdraw the "
                    "stale claim in your next heartbeat.",
                ),
            )
        if ts is not None:
            age_hours = (now - ts).total_seconds() / 3600
            if age_hours > CLAIM_STALE_HOURS:
                findings.append(
                    Finding(
                        rel,
                        "claims-stale",
                        f"claim for order(s) {', '.join(sorted(ids))} is "
                        f"{age_hours:.0f}h old (> {CLAIM_STALE_HOURS}h "
                        "abandonment horizon, control/README.md § Claims "
                        "expire) — refresh it with a fresh heartbeat / open PR "
                        "reference if still building, or withdraw it so the "
                        "order can be re-claimed.",
                    ),
                )
    return findings
