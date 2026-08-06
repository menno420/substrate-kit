"""Advisory-census parity — a checker cannot ship unclassified.

``guards.ADVISORY_CENSUS`` is the fifth pinned surface (see the module header
there for the measurement that motivated it). The four censuses beside it pin
the ENFORCING surfaces — which steps, jobs, sub-checks and hooks can red a PR.
This one pins the surface an agent READS: every ``check --strict`` advisory
block, classified DETERMINISTIC (stays in the agent's channel) or HEURISTIC
(routed to ``--advisories``, off the channel).

The pin is bidirectional set-equality against the live ``_advisory_out(`` call
sites in ``cli.cmd_check``, parsed with the same stdlib string-splitting the
guard-parity and surface-census tests use:

  * an advisory block added without a census entry turns this red, so a new
    checker cannot silently rejoin the noise field; and
  * a census entry whose block is gone turns this red, so the registry cannot
    outlive the code it describes.

Plus the anchor floors, mirroring EXPECTED_MIRRORS / EXPECTED_CENSUS_GATES —
so the census cannot be gutted to a vacuously-green empty set.
"""

from __future__ import annotations

import re
from pathlib import Path

from engine.guards import (
    ADVISORY_CENSUS,
    ADVISORY_DETERMINISTIC,
    ADVISORY_HEURISTIC,
    ADVISORY_KINDS,
    EXPECTED_ADVISORY_DETERMINISTIC,
    EXPECTED_ADVISORY_HEURISTIC,
    advisory_census,
    advisory_checkers,
    advisory_kind,
    advisory_reasons,
    deterministic_advisories,
    heuristic_advisories,
)

CLI_SOURCE = Path(__file__).resolve().parents[1] / "src" / "engine" / "cli.py"

# `_advisory_out(\n    <report>,\n    "<site>",` — the site name is the second
# argument, always a bare string literal on its own line.
_CALL = re.compile(
    r'_advisory_out\(\s*\n\s*\w+,\s*\n\s*"([a-z_]+)",',
)


def _live_sites() -> set[str]:
    """Every advisory emit site the live cli.py routes through the census."""
    return set(_CALL.findall(CLI_SOURCE.read_text(encoding="utf-8")))


def test_every_live_site_is_censused() -> None:
    """An advisory block cannot ship without a classification."""
    missing = _live_sites() - set(ADVISORY_CENSUS)
    assert not missing, (
        "advisory emit site(s) with no ADVISORY_CENSUS entry — classify them "
        f"DETERMINISTIC or HEURISTIC in guards.py: {sorted(missing)}"
    )


def test_every_census_entry_has_a_live_site() -> None:
    """A census entry cannot outlive the block it describes."""
    stale = set(ADVISORY_CENSUS) - _live_sites()
    assert not stale, (
        "ADVISORY_CENSUS entr(ies) with no live _advisory_out call — the block "
        f"was removed or renamed; drop the entry too: {sorted(stale)}"
    )


def test_kinds_are_from_the_enumerated_set() -> None:
    for site, (kind, _checker, _why) in ADVISORY_CENSUS.items():
        assert kind in ADVISORY_KINDS, f"{site} carries unknown kind {kind!r}"


def test_every_entry_carries_a_checker_and_a_reason() -> None:
    """The reason is the point — an unexplained classification is a guess."""
    for site, (_kind, checker, why) in ADVISORY_CENSUS.items():
        assert checker, f"{site} names no producing checker"
        assert len(why) > 15, f"{site} carries no descriptive reason: {why!r}"


def test_anchor_floors_hold() -> None:
    """Shrinkage guard — the census cannot be gutted to a vacuous pass."""
    assert len(deterministic_advisories()) == EXPECTED_ADVISORY_DETERMINISTIC
    assert len(heuristic_advisories()) == EXPECTED_ADVISORY_HEURISTIC
    assert len(ADVISORY_CENSUS) == (
        EXPECTED_ADVISORY_DETERMINISTIC + EXPECTED_ADVISORY_HEURISTIC
    )


def test_accessors_agree_with_the_registry() -> None:
    assert advisory_census() == ADVISORY_CENSUS
    assert advisory_census() is not ADVISORY_CENSUS  # a copy, not the original
    assert len(advisory_checkers()) == len(ADVISORY_CENSUS)
    assert len(advisory_reasons()) == len(ADVISORY_CENSUS)
    for site in deterministic_advisories():
        assert advisory_kind(site) == ADVISORY_DETERMINISTIC
    for site in heuristic_advisories():
        assert advisory_kind(site) == ADVISORY_HEURISTIC


def test_unknown_site_fails_loud_not_silent() -> None:
    """Forgetting a census entry must produce noise, never silence.

    An unclassified site defaults to DETERMINISTIC, so it keeps printing in the
    agent's channel and the parity test above catches it. The opposite default
    would suppress an unclassified block silently — a checker could go dark
    with nothing to notice it.
    """
    assert advisory_kind("no_such_site_xyz") == ADVISORY_DETERMINISTIC


def test_the_measured_noise_classes_are_all_heuristic() -> None:
    """The eight tags observed firing on real trees (2026-08-06) route away.

    Measured on substrate-kit @ 61278b3 and fleet-manager @ c19ae90: these are
    the only advisory sites that actually fired, and they accounted for 87% and
    90% of gate output respectively. If any of them were to be reclassified
    DETERMINISTIC, the noise field returns — so the classification is pinned
    against the observation that motivated it.
    """
    observed = {
        "status_advisories",
        "xref_advisories",
        "model_line_advisories",
        "adopters_advisories",
        "stale_walls_advisories",
        "dateless_walls_advisories",
        "ungroomed_ideas_advisories",
        "grounds_advisories",
    }
    assert observed <= set(heuristic_advisories()), (
        "a measured noise class was reclassified as deterministic: "
        f"{sorted(observed - set(heuristic_advisories()))}"
    )
