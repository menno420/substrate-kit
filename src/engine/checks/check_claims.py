"""Claim-aware checker — THE unified claims enforcement (ORDER 007 + EAP §6.4).

Why + provenance: claim conventions had forked across the fleet (EAP program
review 2026-07-10 §6.4 — "4 claim mechanisms + a checker checking a fifth"):
superbot kept one-file-per-claim in ``docs/owner/claims/``, gba-homebrew in a
root ``claims/``, websites had only the orders-line annotation, and this
checker validated only that last convention. This module now enforces the ONE
kit-owned convention, which has two deliberate surfaces:

**ORDER claims** (unchanged — inbox ORDER 007): the fleet coordination
protocol (``control/README.md`` § "Claiming an order") makes every ``new``
order single-executor. Before building, a lane appends ``claimed-by:
<order-ids> <lane-or-session> <ISO8601>`` to the ``orders:`` line of its OWN
heartbeat (``control/status*.md``) and lands it on main FIRST — so two
readers of the same ``status: new`` order cannot both execute it. Born from a
realized failure (substrate-kit PRs #50/#51: twin execution of ORDER 005).

**WORK/lane claims** (EAP §6.4): parallel sessions doing coordinator-assigned
or self-initiated work claim BEFORE a PR exists by creating ONE FILE PER
CLAIM under ``control/claims/`` (``<branch-or-scope>.md``, a single bullet:
`` - `branch-or-scope` · scope — detail · YYYY-MM-DD ``), deleted at session
close. Per-file is the measured winner: superbot's real-``git merge``
simulation (``tools/sim/claim_layout_sim.py``) put a shared-append claim
ledger at ~98% merge-conflict rate under concurrent sessions vs **0% for
one-file-per-claim** at every concurrency level. The planted
``control/claims/README.md`` carries the convention to every adopter.

What it flags (ALL **advisory** — a nudge, never a locked door, the same
posture as the staleness + owner-action warnings):

- ``claims-duplicate`` — (orders) two or more DISTINCT heartbeat files carry
  a ``claimed-by:`` naming the SAME order id; (work) two or more claim files
  name the SAME backticked branch/scope token. The tiebreak (earliest claim
  merged to main wins) is a human call, so the checker surfaces the
  collision rather than picking a winner.
- ``claims-stale`` — (orders) a live ``claimed-by:`` for an order already in
  some lane's ``done=``, or older than the ~24h abandonment horizon; (work)
  a claim file whose bullet date is older than the ~72h work horizon —
  claim files are deleted at session close, so an old one is likely an
  orphan the GC convention says to prune on sight.
- ``claims-format`` — (work) a claim file without a parseable claim bullet
  (a ``- `` bullet carrying a backticked branch/scope token and a
  ``YYYY-MM-DD`` date). Unparseable claims are invisible to the duplicate
  scan, so the format nag protects the collision detection itself.
- ``claims-legacy-location`` — (work, the §6.4 migration/compat window)
  claim files found in a pre-unification location (``docs/owner/claims/`` —
  superbot's home; root ``claims/`` — gba-homebrew's). Legacy dirs are
  AUTO-DETECTED and scanned in place (their claims still get the full
  format/stale/duplicate treatment, and cross-location duplicates are
  caught), with one nudge per legacy dir pointing at the canonical home.
  Because every claims finding is advisory-by-contract, an adopter's
  existing claims can never go born-red on upgrade — migration is by nag,
  not locked door. A host that deliberately keeps a different home pins it
  via ``substrate.config.json`` → ``claims_dir`` (then it IS canonical and
  no nudge fires).

Posture is **advisory-only, never exit-affecting** — the deliberate mirror of
``check_owner_actions`` / ``check_status_current``'s staleness warning. Claims
are a coordination hint the manager reconciles; a hard gate would red a
required check on a race the checker can't adjudicate.

The order-claim half is input-gated on the ``control/`` protocol per
heartbeat file, like every control-band checker; the work-claim half is
input-gated on a claims directory existing (canonical, configured, or
legacy). Pure stdlib — no ``subprocess`` (§3.2). Unreadable / claim-less
files fail open (no verdict). ``README.md`` inside a claims dir is the
planted convention doc, never a claim.
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
from engine.grammar import (
    ORDERS_CLAIMED_BY_RE,
    ORDERS_DONE_RE,
    ORDERS_LINE_RE,
    WORK_CLAIM_BULLET_RE,
    WORK_CLAIM_DATE_RE,
)
from engine.lib.config import DEFAULT_CLAIMS_DIR

# The convention's abandonment horizon (control/README.md § "Claims expire"):
# a claim with no visible activity after ~24h may be re-claimed. Seeded here,
# revisable by data (KF-8 posture), mirroring check_status_current's constant.
CLAIM_STALE_HOURS = 24

# Work-claim horizon (EAP §6.4, decided-and-flagged): claim FILES are deleted
# at session close, so age here means "probably orphaned", not "still
# building" — but long sessions and weekend gaps are real, so the horizon is
# deliberately looser than the order-claim 24h. Seeded at 72h; revisable by
# data like every horizon constant.
WORK_CLAIM_STALE_HOURS = 72

# The §6.4 legacy locations the compat window auto-detects (in priority
# order): superbot's docs/owner/claims/ (Q-0195) and gba-homebrew's root
# claims/ (gen-2 blueprint §1). Scanned in place with a migration nudge —
# see the module docstring's claims-legacy-location entry.
LEGACY_CLAIMS_DIRS = ("docs/owner/claims", "claims")

# The claim grammar — the work-claim bullet and the orders line
# (acked=/done=/claimed-by:) — is kit-owned with ONE home — engine.grammar
# (EAP §6.8): the writer templates and this enforcer consume the same
# constants, so they cannot drift apart. Shape notes live there.


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
    match = ORDERS_LINE_RE.search(text)
    return match.group(1) if match else None


def _done_ids(orders_value: str) -> set[str]:
    """Return the set of order ids reported in ``done=`` on an orders line."""
    match = ORDERS_DONE_RE.search(orders_value)
    return _expand_ids(match.group(1)) if match else set()


def _claim(orders_value: str) -> tuple[set[str], str, datetime | None] | None:
    """Return ``(ids, lane, ts)`` for the line's ``claimed-by:``, or None.

    ``ids`` is the normalized claimed order-id set, ``lane`` the claimant
    token, ``ts`` the parsed timestamp (None when unparseable — the age check
    then simply skips, never fabricating staleness).
    """
    match = ORDERS_CLAIMED_BY_RE.search(orders_value)
    if not match:
        return None
    ids = _expand_ids(match.group(1))
    if not ids:
        return None
    return ids, match.group(2), _parse_iso(match.group(3))


def _claim_dirs(target: Path, claims_dir: str) -> list[tuple[str, bool]]:
    """Return existing claims dirs as ``(relpath, is_legacy)`` pairs.

    The configured/canonical dir first, then every §6.4 legacy location that
    exists — a legacy dir is scanned even when the canonical one exists too
    (claims left behind mid-migration are exactly the drift the nudge names,
    and a cross-location duplicate is still the twin-execution race). A
    legacy path that IS the configured dir is canonical for this host: no
    nudge (the ``claims_dir`` pin is the deliberate-different-home opt-out).
    """
    dirs: list[tuple[str, bool]] = []
    if (target / claims_dir).is_dir():
        dirs.append((claims_dir, False))
    for legacy in LEGACY_CLAIMS_DIRS:
        if legacy != claims_dir and (target / legacy).is_dir():
            dirs.append((legacy, True))
    return dirs


def _work_claim_findings(
    target: Path,
    claims_dir: str,
    now: datetime,
) -> list[Finding]:
    """Return advisory findings for the one-file-per-claim work claims."""
    findings: list[Finding] = []
    # token -> [relpath, ...] across every scanned dir (cross-location
    # duplicates are still one collision).
    holders: dict[str, list[str]] = {}
    for dir_rel, is_legacy in _claim_dirs(target, claims_dir):
        dir_path = target / dir_rel
        claim_files = sorted(
            p for p in dir_path.glob("*.md") if p.name != "README.md"
        )
        if is_legacy and claim_files:
            findings.append(
                Finding(
                    dir_rel,
                    "claims-legacy-location",
                    f"{len(claim_files)} work-claim file(s) in the legacy "
                    f"location {dir_rel}/ — the kit convention is one file "
                    f"per claim under {claims_dir}/ (control/claims/"
                    "README.md). Move open claims there (or pin this "
                    "location via substrate.config.json `claims_dir` if it "
                    "is deliberate). Advisory during the migration window.",
                ),
            )
        for path in claim_files:
            rel = f"{dir_rel}/{path.name}"
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue  # fail open — an unreadable file is not a verdict
            bullet = WORK_CLAIM_BULLET_RE.search(text)
            # The claim's OWN date is the LAST date on the bullet line — the
            # taught grammar ends the bullet with `· YYYY-MM-DD`
            # (work_claim_bullet_example), while scope text legitimately
            # mentions dated filenames (…-2026-07-09.md). Grepping the FIRST
            # date anywhere in the file let such a mention shadow a fresh
            # claim date and fire a false claims-stale (found live on the
            # 2026-07-14 model-line-lint session; guard recipe in that card).
            claim_dates: list[str] = []
            if bullet is not None:
                line_end = text.find("\n", bullet.start())
                if line_end == -1:
                    line_end = len(text)
                claim_dates = WORK_CLAIM_DATE_RE.findall(
                    text[bullet.start() : line_end]
                )
            if bullet is None or not claim_dates:
                findings.append(
                    Finding(
                        rel,
                        "claims-format",
                        "no parseable claim bullet — a claim file carries "
                        "one `- ` bullet with a backticked branch/scope "
                        "token and a YYYY-MM-DD date "
                        f"({claims_dir}/README.md); an unparseable claim is "
                        "invisible to the duplicate scan.",
                    ),
                )
                continue
            holders.setdefault(bullet.group(1).strip(), []).append(rel)
            claim_date = claim_dates[-1]
            claimed = _parse_iso(claim_date)
            if claimed is None:
                continue
            age_hours = (now - claimed).total_seconds() / 3600
            if age_hours > WORK_CLAIM_STALE_HOURS:
                findings.append(
                    Finding(
                        rel,
                        "claims-stale",
                        f"work claim dated {claim_date} is "
                        f"{age_hours / 24:.0f} day(s) old (> "
                        f"{WORK_CLAIM_STALE_HOURS}h work-claim horizon) — "
                        "claim files are deleted at session close, so this "
                        "is likely an orphan; delete it (prune-on-sight) or "
                        "refresh its date if genuinely still building.",
                    ),
                )
    for token in sorted(holders):
        rels = sorted(holders[token])
        if len(rels) < 2:
            continue
        for rel in rels:
            findings.append(
                Finding(
                    rel,
                    "claims-duplicate",
                    f"work claim `{token}` is declared by {len(rels)} files "
                    f"({', '.join(rels)}) — the same-lane collision the "
                    "per-file convention exists to surface. Reconcile by "
                    "the tiebreak (first claim merged to main wins); the "
                    "loser deletes its file and stands down.",
                ),
            )
    return findings


def check_claims(
    target: Path,
    *,
    status_files: Sequence[str] | None = None,
    now: datetime | None = None,
    claims_dir: str | None = None,
) -> list[Finding]:
    """Return advisory findings for order-claims AND work-claims (§6.4).

    Order half (ORDER 007): scans every configured heartbeat file's
    ``orders:`` line for ``claimed-by:`` annotations — ``claims-duplicate``
    when two distinct files claim one order id, ``claims-stale`` when a live
    claim names an order already in some lane's ``done=`` or is older than
    ``CLAIM_STALE_HOURS``. Work half (EAP §6.4): scans the claims
    directory(-ies) — ``claims-format`` / ``claims-stale`` /
    ``claims-duplicate`` per file plus the ``claims-legacy-location``
    migration nudge (see the module docstring). ``claims_dir`` defaults to
    :data:`engine.lib.config.DEFAULT_CLAIMS_DIR`. Advisory by contract —
    callers must never count any of these toward an exit code. Empty when
    neither the ``control/`` protocol nor a claims dir is present, and
    fail-open on unreadable files.
    """
    now = now or datetime.now(timezone.utc)
    resolved_claims_dir = claims_dir or DEFAULT_CLAIMS_DIR
    work_findings = _work_claim_findings(target, resolved_claims_dir, now)

    relpaths = heartbeat_relpaths(status_files)
    control_evidence = [INBOX_RELPATH, CONTROL_README_RELPATH, *relpaths]
    if not any((target / rel).is_file() for rel in control_evidence):
        # No control protocol → no order-claim scan; the work half already
        # self-gated on a claims dir existing.
        return work_findings

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

    findings: list[Finding] = list(work_findings)

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
