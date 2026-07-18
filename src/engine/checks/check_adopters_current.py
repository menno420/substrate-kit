"""Adopter-registry format gate — the CI half of the currency scanner.

Why + provenance: EAP program review §6.3 (menno420/superbot
``docs/eap/eap-program-review-2026-07-10.md``) made ``docs/adopters.md`` a
GENERATED artifact (``engine/currency.py``), but kit CI cannot authenticate
to sibling repos, so the network-fetching half can never run in CI. This
checker is the half that CAN: it validates the *committed* registry's shape
— generated marker present, parseable ``Generated:`` stamp, parseable
registry table — with **no network**, so a hand-edit that breaks the
generated contract (or a stray hand-written registry masquerading as one)
reds the gate deterministically.

Postures, split exactly like ``check_status_current`` (a required CI check
never reds on wall-clock time alone):

- **Gate findings** (strict loop, RED under ``check --strict``): static,
  deterministic format states — ``adopters-not-generated`` (the file exists
  but carries no GENERATED marker: hand-edited or pre-§6.3),
  ``adopters-no-timestamp`` (no parseable ``> Generated:`` ISO-8601 stamp),
  ``adopters-table-unparseable`` (no ``## Registry`` table with at least one
  data row).
- **Advisory findings** (warn-only, never exit-affecting):
  ``adopters-stale`` — the stamp parses but is older than ``max_age_days``
  (default 14, the config staleness horizon): rerun ``bootstrap currency``.
  ``adopters-version-lag`` — the ``kit release: v<X>`` the registry was
  generated against differs from the tree's current version home
  (``substrate.config.json`` ``kit_version``): a version home moved *after*
  the last regen, so the registry is stale even when the calendar age is
  young (the #438 class the age nag misses). Both read purely — no
  subprocess/git, so a checker stays deterministic (§3.2).

Input-gated like every checker: engages only when ``docs/adopters.md``
exists — adopter repos (which don't carry the registry; it is kit-lab's
sole-writer surface) add nothing here. Unreadable files fail open. Stdlib
only; imports its marker constants from ``engine/currency.py`` so the
generator and the gate can never drift apart.
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

from engine.checks.check_docs import Finding
from engine.currency import (
    ADOPTERS_RELPATH,
    GENERATED_MARKER,
    GENERATED_STAMP_PREFIX,
    REGEN_COMMAND,
    SELF_REPO,
    _registry_rows,
)

DEFAULT_MAX_AGE_DAYS = 14

_STAMP_FORMATS = ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%MZ", "%Y-%m-%d")

# The version home the generator syncs to (cut_release.py keeps it equal to
# ``config.py``'s ``KIT_VERSION``; #438 made it the self-pin). Read purely
# (JSON, no subprocess/git — §3.2 keeps checkers deterministic) to answer
# "did a version home move after the registry was last generated?".
_KIT_CONFIG_RELPATH = "substrate.config.json"

# ``render_adopters`` stamps ``> Generated: <stamp> · kit release: v<X.Y.Z>``
# (engine/currency.py) — the kit version the registry was generated against.
_EMBEDDED_KIT_VERSION_RE = re.compile(r"kit release:\s*v(\d+\.\d+\.\d+)")

# Any ``vX.Y.Z`` token in a registry cell — used to read the self-row's
# version-bearing cells (tree / config-pin / self-report) for the self-row
# staleness gate.
_CELL_VERSION_RE = re.compile(r"v(\d+\.\d+\.\d+)")


def _parse_stamp(text: str) -> datetime | None:
    """Parse the ``> Generated: <stamp> …`` line's timestamp, if any."""
    for line in text.splitlines():
        if not line.startswith(GENERATED_STAMP_PREFIX):
            continue
        token = line[len(GENERATED_STAMP_PREFIX) :].strip().split()
        if not token:
            return None
        for fmt in _STAMP_FORMATS:
            try:
                return datetime.strptime(token[0], fmt).replace(tzinfo=timezone.utc)
            except ValueError:
                continue
        return None
    return None


def _embedded_kit_version(text: str) -> str | None:
    """Return the ``kit release: vX.Y.Z`` version the registry was generated
    against, if the Generated line carries one (files rendered before version
    stamping have none — fail open)."""
    for line in text.splitlines():
        if not line.startswith(GENERATED_STAMP_PREFIX):
            continue
        match = _EMBEDDED_KIT_VERSION_RE.search(line)
        return match.group(1) if match else None
    return None


def _current_version_home(target: Path) -> str | None:
    """Return the target tree's current kit version from its
    ``substrate.config.json`` ``kit_version`` self-pin — None if the file is
    absent / unparseable / has no string pin (fail open: no version source =
    no verdict)."""
    path = target / _KIT_CONFIG_RELPATH
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, ValueError):
        return None
    pin = data.get("kit_version") if isinstance(data, dict) else None
    return pin if isinstance(pin, str) and pin else None


def _self_row_versions(text: str) -> set[str] | None:
    """Return the ``vX.Y.Z`` tokens in the substrate-kit self-row's
    version-bearing cells (tree / config-pin / self-report), or None when the
    registry carries no self-row (fail open — nothing to gate).

    An empty set (a self-row present but with no parseable version token in
    those cells — e.g. all ``—``) reads as "no stamped version", also fail
    open: the gate only fires when the row *does* stamp a version and that
    version no longer includes the current home.
    """
    rows = _registry_rows(text)
    row = rows.get(SELF_REPO)
    if row is None:
        return None
    # ``_registry_rows`` joins cells with " | ":
    # repo | tree | config-pin | self-report | engaged | verdict.
    cells = [cell.strip() for cell in row.split(" | ")]
    version_cells = cells[1:4]  # tree, config-pin, self-report
    return {
        match.group(1)
        for cell in version_cells
        for match in _CELL_VERSION_RE.finditer(cell)
    }


def _has_registry_table(text: str) -> bool:
    """True when a ``## Registry`` table with >= 1 data row exists."""
    lines = text.splitlines()
    try:
        start = next(
            i for i, line in enumerate(lines) if line.strip() == "## Registry"
        )
    except StopIteration:
        return False
    rows = [
        line
        for line in lines[start:]
        if line.startswith("|") and "---" not in line
    ]
    # Header row + at least one data row.
    return len(rows) >= 2


def check_adopters_current(
    target: Path,
    *,
    now: datetime | None = None,
    max_age_days: int = DEFAULT_MAX_AGE_DAYS,
) -> tuple[list[Finding], list[Finding]]:
    """Return ``(gate, advisory)`` findings for the adopter registry."""
    path = target / ADOPTERS_RELPATH
    if not path.is_file():
        return [], []
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return [], []  # fail open — an unreadable file is not a verdict
    gate: list[Finding] = []
    advisory: list[Finding] = []
    if GENERATED_MARKER not in text:
        gate.append(
            Finding(
                ADOPTERS_RELPATH,
                "adopters-not-generated",
                "the adopter registry exists but carries no GENERATED "
                "marker — it is generated output since EAP §6.3; regenerate "
                "with `bootstrap currency` instead of hand-editing.",
            ),
        )
        return gate, advisory
    stamp = _parse_stamp(text)
    if stamp is None:
        gate.append(
            Finding(
                ADOPTERS_RELPATH,
                "adopters-no-timestamp",
                "no parseable `> Generated:` ISO-8601 stamp — the staleness "
                "contract needs the evidence date; regenerate with "
                "`bootstrap currency`.",
            ),
        )
    if not _has_registry_table(text):
        gate.append(
            Finding(
                ADOPTERS_RELPATH,
                "adopters-table-unparseable",
                "no `## Registry` table with at least one data row — the "
                "registry's whole payload; regenerate with "
                "`bootstrap currency`.",
            ),
        )
    # Self-row staleness GATE (B-2): the substrate-kit self-row is the ONE
    # registry row the lab can regenerate from local evidence alone (its own
    # version homes), so it need not wait for a network `currency` aftermath
    # run — cut_release.py stamps it into the bump PR (`restamp_self_row`).
    # This gate RED-holds when the self-row still stamps a version that no
    # longer includes the current version home (the #438-class stale window
    # scoped to the self-row). Robust to the bump window where the tree cell
    # lags the just-bumped config pin: the gate passes as long as the home
    # version appears among the self-row's version cells, so a transient
    # tree-vs-pin spread does not false-red the bump PR. Fail open when: the
    # registry has no self-row, the self-row stamps no parseable version, or
    # the version home is unreadable (mirrors `adopters-version-lag`). Scoped
    # to the SELF row only — sibling adopter lag never reds this gate.
    self_versions = _self_row_versions(text)
    self_home = _current_version_home(target)
    if self_versions and self_home is not None and self_home not in self_versions:
        stamped = ", ".join(f"v{v}" for v in sorted(self_versions))
        gate.append(
            Finding(
                ADOPTERS_RELPATH,
                "adopters-self-row-stale",
                f"the substrate-kit self-row in {ADOPTERS_RELPATH} is stamped "
                f"{stamped} but the kit version home (`{_KIT_CONFIG_RELPATH}`) "
                f"is now v{self_home}; run `{REGEN_COMMAND}` or the release "
                "self-stamp so the self-row (and the bump PR) carry the "
                "current version.",
            ),
        )
    if stamp is not None:
        current = now or datetime.now(timezone.utc)
        if current - stamp > timedelta(days=max_age_days):
            advisory.append(
                Finding(
                    ADOPTERS_RELPATH,
                    "adopters-stale",
                    f"generated {stamp.date().isoformat()} — older than "
                    f"{max_age_days} days; the fleet's version spread may "
                    "have moved. Rerun `bootstrap currency` (agent-side; "
                    "CI cannot refetch).",
                ),
            )
    # Version-home-move advisory (prev-card Q-0089 idea → guard): the
    # calendar-age nag above misses the #438 class — a version home bumped at
    # the source leaves the freshly-generated registry (<14d, so age never
    # fires) silently stale. The registry records the kit version it was
    # generated against; when the version home now reads a different version,
    # a home moved after the last regen. Warn-only, same never-exit-affecting
    # contract as `adopters-stale`.
    embedded = _embedded_kit_version(text)
    home = _current_version_home(target)
    if embedded is not None and home is not None and embedded != home:
        advisory.append(
            Finding(
                ADOPTERS_RELPATH,
                "adopters-version-lag",
                f"generated against kit v{embedded}, but the version home "
                f"(`{_KIT_CONFIG_RELPATH}`) now reads v{home} — a version "
                "home moved after the last regen; the registry's verdicts are "
                "stale. Rerun `bootstrap currency` (agent-side; CI cannot "
                "refetch).",
            ),
        )
    return gate, advisory
