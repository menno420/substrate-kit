"""Capability stale-wall advisory — warn-only, NEVER exit-affecting.

Provenance: ``docs/planning/2026-07-19-night-run-idea-groom.md`` R5 (from the
``generalize-wall-guard`` card). This is the enforcement analogue of the
DISCOVERY RULE's staleness step — the rule says a wall must be *re-verified*, not
merely once-recorded, or it decays from a fact into a stale claim; this checker
surfaces any documented wall whose verification date has aged past the window.

Why this exists: ``docs/CAPABILITIES.md`` is the durable "what agent sessions
CAN and CANNOT do here" ledger. A recorded *wall* (a blocked capability) is only
as good as its last verification — a platform classifier can loosen, a proxy
quirk can clear, an env token can be provisioned — so a wall that has not been
re-checked in a while may already be false. Nothing warns when that happens. The
DISCOVERY RULE tells a session to re-verify before trusting an old wall, but a
rule is exhortation; this checker is the enforcing readout (surfaced at the kit's
own ``check`` layer, the only kit surface that runs in adopter repos).

What it does: parse the ``## Walls`` seed rows and the ``## Append log`` rows of
``docs/CAPABILITIES.md`` under ``target``; for any *wall* row (never a
capability row) whose verification date is strictly older than
``today - staleness_days`` (config ``cadence.staleness_days``, default 14), emit
ONE advisory naming the wall, its last-verified date, and its age vs the window.
Rows with no parseable date are NOT flagged (they are simply not stale-checkable
— a separate concern), and capability rows are never flagged (R5 is walls only).

Two ledger row formats are handled (both live in the real file):
  * Append-log rows — ``- YYYY-MM-DD · wall · finding · evidence · workaround``
    (older five-field lines without a venue token, and ``wall+recipe`` type
    tokens, are valid too). The leading date is the verification date.
  * Seed / prose rows — a ``## Walls`` bullet carrying a trailing
    ``LAST-VERIFIED: YYYY-MM-DD`` token. The seed row is classed a wall by its
    enclosing ``## Walls`` section, and its date is the ``LAST-VERIFIED`` value
    (preferred over any leading date).

Posture — ADVISORY only (warn-only, never exit-affecting): this returns a single
``list[Finding]`` with no gate tier, so it is wired on the advisory path in
``cli.py`` (``posture="advisory"``) exactly like the folded-gate / claims-format
/ capability-xref nags. It is deliberately NOT in ``STRICT_SUBCHECKS`` — a hard
red would break every repo the moment a wall aged out, which is the opposite of
the "re-verify, don't panic" nudge intended (and a stale-but-still-real wall is a
nudge to re-check, not a defect to fail on). Input-gated + fail-open like every
checker: no ``docs/CAPABILITIES.md``, or an unreadable file, yields nothing (an
absent/unreadable ledger is not a verdict). Stdlib only.

``today`` is injectable so tests are deterministic; it defaults to
``date.today()`` when ``None``.
"""

from __future__ import annotations

import re
from datetime import date, timedelta
from pathlib import Path

from engine.checks.check_docs import Finding

# The capability ledger this checker reads (same relpath as check_capability_xref).
_CAPABILITIES_RELPATH = "docs/CAPABILITIES.md"

# Default staleness window when no config (or no cadence key) is supplied — the
# triggers.py / check_capability_xref default-on-missing pattern.
_DEFAULT_STALENESS_DAYS = 14

# Named STALE_WALL_KIND, not FINDING_KIND: the dist concatenates every engine
# module into one file, and check_folded_gate.py already owns a module-level
# ``FINDING_KIND`` — a second top-level ``FINDING_KIND`` would collide (the last
# wins) and reds ``test_check_namespace``. The value is the finding kind.
STALE_WALL_KIND = "stale-wall"

# An append-log row: ``- YYYY-MM-DD · <type> · ...``. The type token (group 2)
# decides wall vs capability; ``wall`` and ``wall+recipe`` both start with "wall".
_RE_APPENDLOG = re.compile(r"^-\s+(\d{4}-\d{2}-\d{2})\s+·\s+(\S+)")

# A trailing verification stamp on a seed / prose row.
_RE_LAST_VERIFIED = re.compile(r"LAST-VERIFIED:\s*(\d{4}-\d{2}-\d{2})")

# A markdown section header (``## Walls — verified blocked``).
_RE_SECTION = re.compile(r"^##\s+(.*)$")

# The bold title carried by seed rows / emphasized append-log findings.
_RE_BOLD = re.compile(r"\*\*(.+?)\*\*")


def _parse_date(text: str) -> date | None:
    """Parse an ISO ``YYYY-MM-DD`` string, or return ``None`` if malformed."""
    try:
        return date.fromisoformat(text)
    except ValueError:
        return None  # fail open — an unparseable date is not stale-checkable


def _is_wall_section(header: str | None) -> bool:
    """True when a ``## `` section header denotes walls (not capabilities).

    ``## Walls — verified blocked`` -> True; ``## Capabilities — verified
    working`` and ``## Append log`` -> False. Seed rows carry no type token, so
    the enclosing section is what classes them.
    """
    if header is None:
        return False
    low = header.lower()
    return "wall" in low and "capabilit" not in low


def _title(bullet_text: str, first_line: str, appendlog_finding: str | None) -> str:
    """A short human title for the wall row, for the advisory message.

    Prefer the first ``**bold**`` span (seed rows and emphasized findings carry
    one); else the append-log *finding* field (3rd ``·``-delimited field); else
    a trimmed slice of the bullet's first line.
    """
    bold = _RE_BOLD.search(bullet_text)
    if bold:
        return bold.group(1).strip().strip("`").strip()
    if appendlog_finding:
        return appendlog_finding.strip()[:60].strip()
    trimmed = first_line.lstrip("-").strip()
    return trimmed[:60].strip()


def _iter_bullets(text: str):
    """Yield ``(section, first_line, bullet_text)`` for every top-level ``- ``
    bullet, tracking the enclosing ``## `` section.

    A bullet begins at a column-0 ``- `` line and absorbs subsequent indented /
    non-bullet continuation lines until the next bullet, blank line, or header —
    so a wall row whose ``LAST-VERIFIED`` stamp sits on a continuation line is
    still parsed as one logical row.
    """
    section: str | None = None
    first_line: str | None = None
    buf: list[str] = []
    for raw in text.splitlines():
        header = _RE_SECTION.match(raw)
        if header is not None:
            if first_line is not None:
                yield section, first_line, "\n".join(buf)
                first_line = None
                buf = []
            section = header.group(1)
            continue
        if raw.startswith("- "):
            if first_line is not None:
                yield section, first_line, "\n".join(buf)
            first_line = raw
            buf = [raw]
            continue
        if first_line is not None:
            if raw.strip() == "" or raw.startswith("#"):
                yield section, first_line, "\n".join(buf)
                first_line = None
                buf = []
            else:
                buf.append(raw)
    if first_line is not None:
        yield section, first_line, "\n".join(buf)


def _wall_row_date(section, first_line, bullet_text) -> tuple[str, date] | None:
    """Return ``(title, verification_date)`` if the bullet is a dated *wall*
    row, else ``None`` (capability rows, non-wall seed rows, and dateless rows
    are all skipped)."""
    last_verified = _RE_LAST_VERIFIED.search(bullet_text)
    appendlog = _RE_APPENDLOG.match(first_line)

    if appendlog is not None:
        # Append-log row: the type token classes it. Only ``wall`` (and
        # ``wall+recipe`` etc.) rows are our concern.
        row_type = appendlog.group(2).lower()
        if not row_type.startswith("wall"):
            return None  # capability (or other) append-log row — skip
        # Prefer an explicit LAST-VERIFIED stamp; else the leading log date.
        raw_date = last_verified.group(1) if last_verified else appendlog.group(1)
        fields = first_line.split(" · ")
        finding = fields[2] if len(fields) >= 3 else None
    elif last_verified is not None and _is_wall_section(section):
        # Seed / prose wall row: no type token — classed a wall by its section.
        raw_date = last_verified.group(1)
        finding = None
    else:
        return None  # not a stale-checkable wall row

    parsed = _parse_date(raw_date)
    if parsed is None:
        return None  # unparseable date -> not stale-checkable (do not flag)
    return _title(bullet_text, first_line, finding), parsed


def check_stale_walls(
    target: Path,
    config=None,
    *,
    today: date | None = None,
) -> list[Finding]:
    """Return advisory findings for ``wall`` ledger rows whose verification date
    has aged past the staleness window.

    Advisory only — the caller wires this on the ``posture="advisory"`` path and
    NEVER counts it toward the exit code. Input-gated + fail-open: an absent or
    unreadable ``docs/CAPABILITIES.md`` yields no finding. ``today`` is
    injectable for deterministic tests (defaults to ``date.today()``).
    """
    ledger = target / _CAPABILITIES_RELPATH
    if not ledger.is_file():
        return []  # input-gated: no ledger to scan
    try:
        text = ledger.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return []  # fail open — an unreadable ledger is not a verdict

    staleness_days = _DEFAULT_STALENESS_DAYS
    if config is not None:
        cadence = getattr(config, "cadence", None) or {}
        try:
            staleness_days = int(cadence.get("staleness_days", _DEFAULT_STALENESS_DAYS))
        except (TypeError, ValueError):
            staleness_days = _DEFAULT_STALENESS_DAYS

    now = today if today is not None else date.today()
    cutoff = now - timedelta(days=staleness_days)

    findings: list[Finding] = []
    for section, first_line, bullet_text in _iter_bullets(text):
        row = _wall_row_date(section, first_line, bullet_text)
        if row is None:
            continue
        title, verified = row
        if verified >= cutoff:
            continue  # within the window — fresh enough
        age = (now - verified).days
        findings.append(
            Finding(
                _CAPABILITIES_RELPATH,
                STALE_WALL_KIND,
                f"stale wall '{title}' last-verified {verified.isoformat()} "
                f"({age} days old > {staleness_days}-day window) — re-verify "
                "per the DISCOVERY RULE or it is a claim, not a fact.",
            ),
        )
    return findings
