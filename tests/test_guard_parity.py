"""Guard-parity meta-test — kit CI guards must mirror the adopter CI (or be
explicitly allowlisted as kit-only).

WHAT THIS GUARDS AGAINST
------------------------
The kit runs two CI guard surfaces that must stay in agreement:

  * the kit's OWN CI — ``.github/workflows/ci.yml``, job ``kit-quality``;
  * the GENERATED adopter CI every host receives — the ``substrate-gate`` job
    ``src/engine/adopt.py`` :func:`live_ci_workflow` emits.

They were kept in agreement only BY HAND, and in TWO places at that: the
adopter step names lived inline in :func:`adopt.live_ci_workflow` while this
test carried its own private copy of them. When the claims-only fast-lane
guard shipped to the kit's own ``ci.yml`` (PR #455) but not to the generated
adopter CI, nothing detected the drift — a human had to notice and queue PR
#457 to close the gap (the #455/#457 gap). This meta-test closes that drift
class: every ENFORCING ``kit-quality`` guard must either mirror a live adopter
guard or be listed as legitimately kit-only with a one-line reason.

The classification itself — the ``REGISTRY`` and the ``SETUP`` / ``MIRRORS`` /
``KIT_ONLY`` sentinels — now lives in ONE canonical place,
``src/engine/guards.py``, which :func:`adopt.live_ci_workflow` also reads the
adopter step NAMES from. So a MIRRORS entry and the YAML the generator emits
can no longer disagree by construction, and adding/renaming a guard is a
one-place edit in the manifest, not two. This test imports the manifest and
classifies the live ``ci.yml`` against it.

HOW TO RESPOND WHEN IT GOES RED
-------------------------------
* ``test_every_kit_quality_step_is_classified`` red — a ``kit-quality`` step
  was ADDED or REMOVED. A NEW step must be classified in the ``REGISTRY`` in
  ``src/engine/guards.py`` as ``SETUP`` (non-enforcing setup/detect/echo),
  ``MIRRORS(<adopter step name>)`` (enforcing, with a live counterpart in the
  adopter CI), or ``KIT_ONLY(<why>)`` (enforcing but legitimately kit-only). A
  REMOVED step must be dropped from the registry. This is the primary
  drift-catch: a new kit guard cannot be added silently.
* ``test_mirrored_guards_have_a_live_adopter_counterpart`` red — a ``MIRRORS``
  entry names an adopter step that no longer exists. Someone renamed or removed
  that guard in :func:`live_ci_workflow` while the kit kept it (the reverse of
  the #457-class drift). Restore the adopter counterpart, or — if the guard is
  now legitimately kit-only — reclassify the entry as ``KIT_ONLY`` with a why.

Parsing is stdlib-only string-splitting — the same convention as
``tests/test_ci_control_lane.py`` and ``tests/test_adopt.py`` (no YAML parser
in the test deps, no subprocess). Pure test-side code.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from engine import adopt  # noqa: E402  (after the sys.path insert, like test_adopt)

# The guard mapping is single-sourced in the engine manifest — the SAME module
# adopt.live_ci_workflow() reads the adopter step names from — so the registry
# and the generator can no longer drift (that was the whole two-place hazard
# this file used to embody). Adding/renaming a guard is now a one-place edit in
# src/engine/guards.py; this test just classifies the live ci.yml against it.
from engine.guards import (  # noqa: E402
    EXPECTED_KIT_ONLY,
    EXPECTED_MIRRORS,
    KIT_ONLY,
    MIRRORS,
    REGISTRY,
    SETUP,
)

CI_PATH = Path(__file__).resolve().parents[1] / ".github" / "workflows" / "ci.yml"

# Re-export the sentinels the module docstring/helpers reference so importers
# and readers still see the three-way vocabulary here (SETUP is a bare marker;
# MIRRORS / KIT_ONLY carry a payload — the adopter step name / the kit-only
# reason). The definitions themselves live in the engine manifest.
__all__ = ["SETUP", "MIRRORS", "KIT_ONLY", "REGISTRY", "EXPECTED_MIRRORS", "EXPECTED_KIT_ONLY"]


# ── stdlib-only parsers ──────────────────────────────────────────────────────
def _named_steps(job_block: str) -> list[str]:
    """Ordered list of the ``- name:`` values in a job block (bare ``uses:``
    steps have no name and are excluded by construction)."""
    names: list[str] = []
    for line in job_block.splitlines():
        stripped = line.strip()
        if stripped.startswith("- name:"):
            names.append(stripped[len("- name:") :].strip())
    return names


def _kit_quality_block() -> str:
    """The ``kit-quality`` job block only — from ``  kit-quality:`` to the next
    2-space-indented job key (e.g. ``  legacy-alias-test:``). The two alias
    jobs are ignored entirely."""
    text = CI_PATH.read_text(encoding="utf-8")
    marker = "\n  kit-quality:"
    idx = text.index(marker)
    rest = text[idx + len(marker) :]
    # The next 2-space-indented key ends the block (a following job or a
    # top-level key). Comment lines (`  #`) are not keys.
    nxt = re.search(r"^  [A-Za-z0-9_-]+:", rest, re.MULTILINE)
    return rest[: nxt.start()] if nxt else rest


def _adopter_substrate_gate_block() -> str:
    """The generated adopter ``substrate-gate`` job block, from
    :func:`live_ci_workflow` called with DEFAULTS (no test_command)."""
    wf = adopt.live_ci_workflow()
    return wf.split("  substrate-gate:", 1)[1]


def _kit_quality_steps() -> list[str]:
    return _named_steps(_kit_quality_block())


def _adopter_steps() -> list[str]:
    return _named_steps(_adopter_substrate_gate_block())


# ── tests ────────────────────────────────────────────────────────────────────
def test_every_kit_quality_step_is_classified():
    """Every named kit-quality step is classified in REGISTRY, and REGISTRY has
    no phantom keys. The primary drift-catch: a new kit guard cannot be added
    silently, and a removed one cannot linger in the registry."""
    actual = set(_kit_quality_steps())
    registered = set(REGISTRY)
    unclassified = actual - registered
    stale = registered - actual
    assert not unclassified and not stale, (
        "kit-quality ⇄ REGISTRY drift in tests/test_guard_parity.py.\n"
        f"  NEW, unclassified kit-quality step(s): {sorted(unclassified)}\n"
        "    → classify each in REGISTRY as SETUP, MIRRORS(<adopter step>), "
        "or KIT_ONLY(<why>).\n"
        f"  REMOVED step(s) still in REGISTRY: {sorted(stale)}\n"
        "    → drop each from REGISTRY."
    )


def test_mirrored_guards_have_a_live_adopter_counterpart():
    """Every MIRRORS entry names an adopter step that actually exists in the
    generated substrate-gate job. Catches someone removing/renaming a guard in
    live_ci_workflow() while the kit keeps it (the reverse of #457-class drift)."""
    adopter = set(_adopter_steps())
    missing = {
        kit_step: payload[1]
        for kit_step, payload in REGISTRY.items()
        if payload[0] == "MIRRORS" and payload[1] not in adopter
    }
    assert not missing, (
        "MIRRORS target(s) with no live adopter counterpart in "
        "live_ci_workflow() — a kit guard lost its mirror:\n"
        + "\n".join(
            f"  kit-quality {kit!r} expects adopter step {adopter_name!r} "
            "(not found in substrate-gate)"
            for kit, adopter_name in sorted(missing.items())
        )
        + "\n  → restore the adopter counterpart, or reclassify KIT_ONLY(<why>) "
        "if it is now legitimately kit-only.\n"
        f"  live adopter steps: {sorted(adopter)}"
    )


def test_kit_only_allowlist_entries_carry_a_reason():
    """Every KIT_ONLY entry carries a non-empty, reasonably descriptive reason —
    the allowlist can never be a bare escape hatch."""
    thin = {
        kit_step: payload[1]
        for kit_step, payload in REGISTRY.items()
        if payload[0] == "KIT_ONLY" and len(payload[1].strip()) <= 15
    }
    assert not thin, (
        "KIT_ONLY entries must carry a descriptive (>15 char) reason; "
        f"too-thin: {thin}"
    )


def test_registry_covers_the_known_enforcing_guards():
    """Anchor floor: the enforcing-guard surface is exactly EXPECTED_MIRRORS
    mirrored + EXPECTED_KIT_ONLY kit-only guards as of this PR. A sanity floor
    so the registry can't be gutted to a vacuously-green empty pass; bump the
    anchors deliberately when the guard set legitimately changes."""
    mirrors = sum(1 for p in REGISTRY.values() if p[0] == "MIRRORS")
    kit_only = sum(1 for p in REGISTRY.values() if p[0] == "KIT_ONLY")
    assert mirrors == EXPECTED_MIRRORS, (
        f"expected {EXPECTED_MIRRORS} MIRRORS guards, found {mirrors} — "
        "if the guard set changed, update EXPECTED_MIRRORS deliberately."
    )
    assert kit_only == EXPECTED_KIT_ONLY, (
        f"expected {EXPECTED_KIT_ONLY} KIT_ONLY guards, found {kit_only} — "
        "if the guard set changed, update EXPECTED_KIT_ONLY deliberately."
    )
