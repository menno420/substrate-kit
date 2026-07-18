"""B-3 -- fast-lane branch-prefix symmetry.

The set of head-branch prefixes that ride the auto-merge fast lane is
duplicated across surfaces (the auto-merge-enabler workflow, the claims-only
fast-lane guard in ci.yml, and the engine defaults). Nothing keeps them in
agreement, so a new seat prefix added to one surface but not another silently
reopens a card-less merge hole or the kit#293 green-and-unarmed stall. This
meta-test pins the canonical set in engine.guards.FASTLANE_PREFIX_REGISTRY and
asserts every live surface agrees, both directions.

Stdlib-only, no subprocess (matches tests/test_guard_surface_census.py).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
_SRC = _ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from engine import adopt, claim, guards  # noqa: E402  (after the sys.path insert, like test_guard_surface_census)

_ENABLER = _ROOT / ".github" / "workflows" / "auto-merge-enabler.yml"
_CI = _ROOT / ".github" / "workflows" / "ci.yml"

_REGISTRY_PREFIXES = set(guards.FASTLANE_PREFIX_REGISTRY)
_STARTSWITH = re.compile(r"startsWith\(\s*github\.head_ref\s*,\s*'([^']+)'\s*\)")


def _enabler_armed_prefixes() -> set[str]:
    """Prefixes the auto-merge-enabler arms -- startsWith(github.head_ref, 'X')."""
    return set(_STARTSWITH.findall(_ENABLER.read_text(encoding="utf-8")))


def _guard_carded_prefixes() -> set[str]:
    """Prefixes the claims-only fast-lane guard requires a session card for.

    The guard is a bash `case "$head_ref" in` block: a `<prefix>*)` arm cards
    that prefix; the bare `*)` fallback rides card-free.
    """
    text = _CI.read_text(encoding="utf-8")
    prefixes: set[str] = set()
    for block in re.findall(r'case\s+"\$head_ref"\s+in(.*?)esac', text, re.DOTALL):
        for label in re.findall(r"([A-Za-z][\w./-]*)\*\)", block):
            prefixes.add(label)
    return prefixes


def _engine_default_prefixes() -> set[str]:
    """adopt.DEFAULT_AUTOMERGE_BRANCH_PATTERNS -> prefixes (strip trailing '*')."""
    return {
        p[:-1] if p.endswith("*") else p
        for p in adopt.DEFAULT_AUTOMERGE_BRANCH_PATTERNS
    }


def test_enabler_arms_exactly_the_registry_prefixes():
    armed = _enabler_armed_prefixes()
    missing = _REGISTRY_PREFIXES - armed
    extra = armed - _REGISTRY_PREFIXES
    assert not missing and not extra, (
        "auto-merge-enabler branch prefixes drifted from "
        "guards.FASTLANE_PREFIX_REGISTRY: un-armed registry prefixes "
        f"{sorted(missing)} would sit green+unarmed (kit#293); un-registered "
        f"armed prefixes {sorted(extra)} would merge card-less. Update "
        ".github/workflows/auto-merge-enabler.yml and "
        "guards.FASTLANE_PREFIX_REGISTRY together."
    )


def test_guard_cards_exactly_the_carded_prefixes():
    carded = _guard_carded_prefixes()
    expected = guards.fastlane_carded_prefixes()
    assert carded == expected, (
        "claims-only fast-lane guard carded prefixes "
        f"{sorted(carded)} drifted from the FASTLANE_CARDED registry entries "
        f"{sorted(expected)}. Update the ci.yml guard `case` arm and "
        "guards.FASTLANE_PREFIX_REGISTRY together."
    )


def test_engine_defaults_match_registry():
    assert _engine_default_prefixes() == _REGISTRY_PREFIXES, (
        "adopt.DEFAULT_AUTOMERGE_BRANCH_PATTERNS "
        f"{sorted(_engine_default_prefixes())} drifted from "
        f"FASTLANE_PREFIX_REGISTRY {sorted(_REGISTRY_PREFIXES)}."
    )


def test_adopter_enabler_generator_arms_the_registry_prefixes():
    expr = adopt._automerge_branch_expr(list(adopt.DEFAULT_AUTOMERGE_BRANCH_PATTERNS))
    rendered = set(_STARTSWITH.findall(expr))
    assert rendered == _REGISTRY_PREFIXES, (
        "the adopter enabler generator renders startsWith terms "
        f"{sorted(rendered)} that drift from FASTLANE_PREFIX_REGISTRY "
        f"{sorted(_REGISTRY_PREFIXES)}."
    )


def test_claim_branch_prefix_is_a_carded_fastlane_prefix():
    assert claim.BRANCH_PREFIX in guards.FASTLANE_PREFIX_REGISTRY, (
        f"claim.BRANCH_PREFIX {claim.BRANCH_PREFIX!r} is not a registered "
        "fast-lane prefix."
    )
    assert (
        guards.FASTLANE_PREFIX_REGISTRY[claim.BRANCH_PREFIX] == guards.FASTLANE_CARDED
    ), "the claim work-branch prefix must be a CARDED fast-lane prefix."


def test_registry_kinds_are_known():
    for prefix, kind in guards.FASTLANE_PREFIX_REGISTRY.items():
        assert kind in guards.FASTLANE_KINDS, f"{prefix!r} has unknown kind {kind!r}"


def test_registry_prefixes_end_with_slash():
    for prefix in guards.FASTLANE_PREFIX_REGISTRY:
        assert prefix.endswith("/"), (
            f"fast-lane prefix {prefix!r} must end with '/' or it matches "
            "sibling names (e.g. 'claude' would match 'claudex/...')."
        )


def test_registry_floor():
    assert len(guards.FASTLANE_PREFIX_REGISTRY) >= guards.EXPECTED_FASTLANE_PREFIXES


def test_at_least_one_carded_prefix():
    assert guards.fastlane_carded_prefixes(), (
        "at least one fast-lane prefix must be CARDED, or the claims-only "
        "guard cards nothing."
    )


def test_accessor_returns_a_copy():
    guards.fastlane_prefixes()["bogus/"] = "x"
    assert "bogus/" not in guards.FASTLANE_PREFIX_REGISTRY
