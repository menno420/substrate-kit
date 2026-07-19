"""The capability stale-wall advisory (night-run groom R5).

``docs/CAPABILITIES.md`` records what agent sessions CAN and CANNOT do here. A
recorded *wall* (a blocked capability) is only as good as its last verification
— a platform classifier can loosen, so a wall not re-checked in a while may
already be false. This checker surfaces any `wall` row whose verification date
has aged past ``cadence.staleness_days`` (default 14) — the enforcement analogue
of the DISCOVERY RULE. It is advisory-only (warn, never exit-affecting), so it
returns a single ``list[Finding]`` with no gate tier.

Two ledger row formats are pinned below: append-log rows
(``- YYYY-MM-DD · wall · ...``) and ``## Walls`` seed rows carrying a trailing
``LAST-VERIFIED: YYYY-MM-DD`` stamp. The load-bearing negatives are that a
capability row is never flagged (R5 is walls only) and a wall row with no
parseable date is never flagged (not stale-checkable). ``today`` is injected for
determinism.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest

pytest.importorskip("engine.checks.check_stale_walls")

from engine.checks.check_stale_walls import STALE_WALL_KIND, check_stale_walls

_TODAY = date(2026, 7, 19)  # window = 14 days -> cutoff 2026-07-05

# A ledger whose append log carries one STALE wall (2026-06-01, ~48d old) and one
# FRESH wall (2026-07-18, 1d old), plus a capability row that must NOT flag, plus
# a dateless wall row that must NOT flag. The `## Walls` section carries one
# STALE seed wall (LAST-VERIFIED 2026-06-10) and one FRESH seed wall
# (LAST-VERIFIED 2026-07-15), plus a capability seed row that must NOT flag.
_LEDGER = """\
# demo — session capabilities & walls

> **Status:** `living-ledger`

## Capabilities — verified working

- `any` · **Media is readable**: extract frames before reporting a format
  wall. — LAST-VERIFIED: 2026-06-01

## Walls — verified blocked

- `any` · **Old branch deletion**: 403 on every path. — LAST-VERIFIED: 2026-06-10
- `any` · **Fresh tag push**: HTTP 403 from the git proxy → workflow_dispatch.
  — LAST-VERIFIED: 2026-07-15

## Append log — newest first

Format: `- YYYY-MM-DD · capability|wall · finding · evidence · workaround`.

- 2026-07-18 · wall · **Fresh append wall** · evidence · workaround
- 2026-06-01 · wall · **Stale append wall** · evidence · workaround
- 2026-07-01 · capability · **A recent capability**, not a wall · evidence · none
- wall · **Dateless wall row** with no leading date · evidence · workaround
"""


def _write_ledger(root: Path, text: str = _LEDGER) -> Path:
    docs = root / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    path = docs / "CAPABILITIES.md"
    path.write_text(text, encoding="utf-8")
    return path


def test_stale_append_wall_fires(tmp_path: Path):
    # The 2026-06-01 append-log wall is well past the 14-day cutoff (2026-07-05).
    _write_ledger(tmp_path, "## Append log\n\n- 2026-06-01 · wall · **Stale one** · e · w\n")
    findings = check_stale_walls(tmp_path, today=_TODAY)
    assert len(findings) == 1
    finding = findings[0]
    assert finding.kind == STALE_WALL_KIND
    assert finding.path == "docs/CAPABILITIES.md"
    assert "Stale one" in finding.message
    assert "2026-06-01" in finding.message


def test_fresh_append_wall_is_silent(tmp_path: Path):
    # A wall verified yesterday is within the window -> no advisory.
    _write_ledger(tmp_path, "## Append log\n\n- 2026-07-18 · wall · **Fresh one** · e · w\n")
    assert check_stale_walls(tmp_path, today=_TODAY) == []


def test_capability_row_never_flags(tmp_path: Path):
    # An OLD capability row is not our concern — R5 is walls only.
    _write_ledger(
        tmp_path,
        "## Append log\n\n- 2026-01-01 · capability · **Ancient capability** · e · none\n",
    )
    assert check_stale_walls(tmp_path, today=_TODAY) == []


def test_dateless_wall_row_never_flags(tmp_path: Path):
    # A wall row with no parseable date is not stale-checkable -> not flagged.
    _write_ledger(
        tmp_path,
        "## Append log\n\n- wall · **No date here** · e · w\n",
    )
    assert check_stale_walls(tmp_path, today=_TODAY) == []


def test_stale_seed_wall_fires_by_last_verified(tmp_path: Path):
    # A `## Walls` seed row (no type token, classed a wall by its section) whose
    # trailing LAST-VERIFIED stamp is stale fires; the LAST-VERIFIED date is used.
    _write_ledger(
        tmp_path,
        "## Walls — verified blocked\n\n"
        "- `any` · **Old branch deletion**: 403 everywhere. — LAST-VERIFIED: 2026-06-10\n",
    )
    findings = check_stale_walls(tmp_path, today=_TODAY)
    assert len(findings) == 1
    assert "Old branch deletion" in findings[0].message
    assert "2026-06-10" in findings[0].message


def test_fresh_seed_wall_is_silent(tmp_path: Path):
    # A `## Walls` seed row verified inside the window stays silent.
    _write_ledger(
        tmp_path,
        "## Walls — verified blocked\n\n"
        "- `any` · **Fresh tag push**: 403 from the proxy. — LAST-VERIFIED: 2026-07-15\n",
    )
    assert check_stale_walls(tmp_path, today=_TODAY) == []


def test_capability_seed_row_never_flags(tmp_path: Path):
    # A `## Capabilities` seed row with an old LAST-VERIFIED is NOT a wall — the
    # enclosing section (not the word "wall" in the prose) classes the row.
    _write_ledger(
        tmp_path,
        "## Capabilities — verified working\n\n"
        "- `any` · **Media is readable** before reporting a format wall. "
        "— LAST-VERIFIED: 2026-01-01\n",
    )
    assert check_stale_walls(tmp_path, today=_TODAY) == []


def test_missing_file_fails_open(tmp_path: Path):
    # No docs/CAPABILITIES.md (input-gated) -> [], no exception.
    assert check_stale_walls(tmp_path, today=_TODAY) == []


def test_mixed_ledger_flags_only_the_stale_walls(tmp_path: Path):
    # The full fixture: exactly the two STALE walls fire (one append-log, one
    # seed); the fresh walls, the capability rows, and the dateless wall are silent.
    _write_ledger(tmp_path)
    findings = check_stale_walls(tmp_path, today=_TODAY)
    messages = " || ".join(f.message for f in findings)
    assert len(findings) == 2, messages
    assert "Stale append wall" in messages
    assert "Old branch deletion" in messages
    assert "Fresh append wall" not in messages
    assert "Fresh tag push" not in messages
    assert "Media is readable" not in messages
    assert "Dateless wall row" not in messages


def test_staleness_window_from_config(tmp_path: Path):
    # A config with a larger cadence.staleness_days widens the window: a wall
    # that fires at the 14-day default stays silent at a 90-day window.
    _write_ledger(
        tmp_path,
        "## Append log\n\n- 2026-06-01 · wall · **48 days old** · e · w\n",
    )

    class _Cfg:
        cadence = {"staleness_days": 90}

    assert check_stale_walls(tmp_path, _Cfg(), today=_TODAY) == []
    # And with the default (no config) it fires.
    assert len(check_stale_walls(tmp_path, today=_TODAY)) == 1


def test_not_in_strict_subchecks():
    # This checker is advisory-only and must stay OFF the exit-affecting strict
    # surface (guards.STRICT_SUBCHECKS is pinned to the =7 floor by the parity
    # meta-test). A regression that classified it strict would red every adopter
    # the moment one of its documented walls aged out of the window.
    guards = pytest.importorskip("engine.guards")
    assert "stale-wall" not in guards.STRICT_SUBCHECKS
    assert "check_stale_walls" not in guards.STRICT_SUBCHECKS
