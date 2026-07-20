"""The capability dateless-wall advisory (wave-2 groom S14).

The exact NEGATIVE complement of R5's ``check_stale_walls``: R5 flags a *dated*
wall whose date has aged past the re-verify window and DELIBERATELY skips a wall
row with no parseable date; this checker IS that skipped concern. A wall with no
date can never trip the staleness re-verify rule, so it escapes THE DISCOVERY
RULE's cadence forever and hardens into an un-auditable claim. This surfaces
those undated wall rows so a date can be stamped. Advisory-only (warn, never
exit-affecting), so it returns a single ``list[Finding]`` with no gate tier.

The load-bearing negatives mirror R5's: a capability row is never flagged (walls
only) and a *dated* wall row is never flagged (that is R5's domain). Together the
two checkers cover every wall row exactly once — the ``test_stale_and_dateless_*``
partition test pins that complementarity.
"""

from __future__ import annotations

from pathlib import Path

import pytest

pytest.importorskip("engine.checks.check_dateless_walls")

from engine.checks.check_dateless_walls import (
    DATELESS_WALL_KIND,
    check_dateless_walls,
)

# A ledger with, in the `## Walls` section: one DATELESS seed wall (no
# LAST-VERIFIED) and one DATED seed wall (LAST-VERIFIED 2026-07-15); plus a
# DATELESS capability seed row that must NOT flag. In the `## Append log`: a DATED
# wall row (has a leading date — R5's job, silent here), a DATELESS wall row (no
# leading date — the flag), and a DATELESS capability row that must NOT flag.
_LEDGER = """\
# demo — session capabilities & walls

> **Status:** `living-ledger`

## Capabilities — verified working

- `any` · **Media is readable**: extract frames before reporting a format wall.

## Walls — verified blocked

- `any` · **Undated seed wall**: 403 on every path, no date recorded.
- `any` · **Dated seed wall**: HTTP 403 from the git proxy. — LAST-VERIFIED: 2026-07-15

## Append log — newest first

Format: `- YYYY-MM-DD · capability|wall · finding · evidence · workaround`.

- 2026-07-18 · wall · **Dated append wall** · evidence · workaround
- wall · **Dateless append wall** with no leading date · evidence · workaround
- capability · **Dateless capability row**, not a wall · evidence · none
"""


def _write_ledger(root: Path, text: str = _LEDGER) -> Path:
    docs = root / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    path = docs / "CAPABILITIES.md"
    path.write_text(text, encoding="utf-8")
    return path


def test_dateless_seed_wall_fires(tmp_path: Path):
    # A `## Walls` seed row (classed a wall by its section) with no LAST-VERIFIED
    # stamp carries no parseable date -> flagged.
    _write_ledger(
        tmp_path,
        "## Walls — verified blocked\n\n"
        "- `any` · **Undated seed wall**: 403 on every path.\n",
    )
    findings = check_dateless_walls(tmp_path)
    assert len(findings) == 1
    finding = findings[0]
    assert finding.kind == DATELESS_WALL_KIND
    assert finding.path == "docs/CAPABILITIES.md"
    assert "Undated seed wall" in finding.message


def test_dated_seed_wall_is_silent(tmp_path: Path):
    # A `## Walls` seed row carrying a well-formed LAST-VERIFIED stamp IS dated ->
    # R5's domain, silent here.
    _write_ledger(
        tmp_path,
        "## Walls — verified blocked\n\n"
        "- `any` · **Dated seed wall**: 403 from the proxy. — LAST-VERIFIED: 2026-07-15\n",
    )
    assert check_dateless_walls(tmp_path) == []


def test_dateless_append_wall_fires(tmp_path: Path):
    # An append-log wall row with no leading date is our concern.
    _write_ledger(
        tmp_path,
        "## Append log\n\n- wall · **No leading date** · e · w\n",
    )
    findings = check_dateless_walls(tmp_path)
    assert len(findings) == 1
    assert "No leading date" in findings[0].message


def test_dated_append_wall_is_silent(tmp_path: Path):
    # A well-formed append-log wall row carries its leading date -> R5's domain.
    _write_ledger(
        tmp_path,
        "## Append log\n\n- 2026-07-18 · wall · **Has a date** · e · w\n",
    )
    assert check_dateless_walls(tmp_path) == []


def test_dateless_capability_seed_row_never_flags(tmp_path: Path):
    # A `## Capabilities` seed row without a date is NOT a wall — walls only.
    _write_ledger(
        tmp_path,
        "## Capabilities — verified working\n\n"
        "- `any` · **Media is readable** before reporting a format wall.\n",
    )
    assert check_dateless_walls(tmp_path) == []


def test_dateless_capability_appendlog_row_never_flags(tmp_path: Path):
    # A dateless append-log `capability` row is not a wall -> not flagged.
    _write_ledger(
        tmp_path,
        "## Append log\n\n- capability · **A dateless capability** · e · none\n",
    )
    assert check_dateless_walls(tmp_path) == []


def test_append_wall_with_last_verified_but_no_leading_date_is_silent(tmp_path: Path):
    # A dateless-leading append-log wall row that nonetheless carries a
    # well-formed LAST-VERIFIED stamp IS dated -> silent (R5 can fire on it).
    _write_ledger(
        tmp_path,
        "## Append log\n\n- wall · **Stamped** · e · w — LAST-VERIFIED: 2026-07-01\n",
    )
    assert check_dateless_walls(tmp_path) == []


def test_malformed_last_verified_still_flags(tmp_path: Path):
    # A LAST-VERIFIED stamp whose date is malformed is NOT a parseable date, so
    # the wall is still un-checkable and must flag.
    _write_ledger(
        tmp_path,
        "## Walls — verified blocked\n\n"
        "- `any` · **Bad date wall**: 403. — LAST-VERIFIED: 2026-13-99\n",
    )
    findings = check_dateless_walls(tmp_path)
    assert len(findings) == 1
    assert "Bad date wall" in findings[0].message


def test_missing_file_fails_open(tmp_path: Path):
    # No docs/CAPABILITIES.md (input-gated) -> [], no exception.
    assert check_dateless_walls(tmp_path) == []


def test_mixed_ledger_flags_only_the_dateless_walls(tmp_path: Path):
    # The full fixture: exactly the two DATELESS walls fire (one seed, one
    # append-log); the dated walls and both capability rows are silent.
    _write_ledger(tmp_path)
    findings = check_dateless_walls(tmp_path)
    messages = " || ".join(f.message for f in findings)
    assert len(findings) == 2, messages
    assert "Undated seed wall" in messages
    assert "Dateless append wall" in messages
    assert "Dated seed wall" not in messages
    assert "Dated append wall" not in messages
    assert "Media is readable" not in messages
    assert "Dateless capability row" not in messages


def test_stale_and_dateless_partition_every_wall_row_once(tmp_path: Path):
    # Complementarity guard: over the full fixture, check_stale_walls (dated,
    # aged-out) and check_dateless_walls (undated) must never both fire on the
    # SAME wall row, and every real wall row is owned by exactly one of them.
    from datetime import date

    from engine.checks.check_stale_walls import check_stale_walls

    _write_ledger(tmp_path)
    today = date(2026, 8, 1)  # window 14d -> the 2026-07-15 dated seed is fresh
    stale = check_stale_walls(tmp_path, today=today)
    dateless = check_dateless_walls(tmp_path)
    # No wall row title appears in BOTH result sets.
    stale_titles = {f.message for f in stale}
    dateless_titles = {f.message for f in dateless}
    assert stale_titles.isdisjoint(dateless_titles)
    # The two DATELESS walls are owned by check_dateless_walls, never R5.
    assert len(dateless) == 2
    for f in stale:
        assert "Undated seed wall" not in f.message
        assert "Dateless append wall" not in f.message


def test_not_in_strict_subchecks():
    # This checker is advisory-only and must stay OFF the exit-affecting strict
    # surface. A regression that classified it strict would red every adopter
    # whose ledger legitimately carries an as-yet-undated wall.
    guards = pytest.importorskip("engine.guards")
    assert "dateless-wall" not in guards.STRICT_SUBCHECKS
    assert "check_dateless_walls" not in guards.STRICT_SUBCHECKS


def test_dateless_wall_kind_has_remediation():
    # S8 coverage lesson: every emittable advisory Finding kind carries a
    # paste-ready remediation block.
    remediate = pytest.importorskip("engine.checks.check_remediate")
    block = remediate.remediate(DATELESS_WALL_KIND)
    assert block is not None
    assert "LAST-VERIFIED" in block
