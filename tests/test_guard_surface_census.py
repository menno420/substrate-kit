"""Guard-surface census meta-test — the SET of enforcing surfaces is pinned,
not just each surface's steps.

WHAT THIS GUARDS AGAINST
------------------------
The kit runs three enforcing guard surfaces, and ``tests/test_guard_parity.py``
already pins each one at STEP / SUB-CHECK granularity:

  * ci.yml ``kit-quality`` steps        ⇄ ``guards.REGISTRY``
  * generated adopter ``substrate-gate`` steps ⇄ the ``guards.MIRRORS`` subset
  * ``bootstrap check --strict`` sub-checks    ⇄ ``guards.STRICT_SUBCHECKS``

What none of those pins is the SET OF SURFACES itself. The concrete "fourth
enforcing surface ships unpinned" vector is a new **workflow job**: any job
added under a ``.github/workflows/*.yml`` ``jobs:`` key can gate a PR (or run
automation beside the gate) without appearing in any of the three step-level
registries. Nothing red-flags that.

This census closes the vector. ``guards.WORKFLOW_JOB_CENSUS`` classifies EVERY
job across ALL workflow files as one of three kinds — a parity-pinned gate
(``CENSUS_GATE_PINNED``), a temporary legacy alias (``CENSUS_ALIAS``), or
non-enforcing automation (``CENSUS_AUTOMATION``). This test asserts bidirectional
set-equality between the census and the live workflow ``jobs:`` keys, so a new
job cannot appear un-censused and a census entry cannot linger after its job is
removed. A new enforcing surface therefore cannot ship without either a parity
pin (classified as a gate) or an explicit out-of-scope registration with a
reason.

HOW TO RESPOND WHEN IT GOES RED
-------------------------------
* ``test_every_workflow_job_is_censused`` red — a workflow job was ADDED or
  REMOVED. A NEW job must be classified in ``guards.WORKFLOW_JOB_CENSUS`` as
  ``CENSUS_GATE_PINNED`` (an enforcing gate — and it must be parity-pinned like
  the others), ``CENSUS_ALIAS`` (a temporary legacy required-context alias), or
  ``CENSUS_AUTOMATION`` (non-enforcing automation that never reds a PR). A
  REMOVED job must be dropped from the census.

Parsing is stdlib-only string-splitting — the same convention as
``tests/test_guard_parity.py`` (no YAML parser in the test deps, no subprocess).
Pure test-side code.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from engine.guards import (  # noqa: E402  (after the sys.path insert, like test_guard_parity)
    CENSUS_ALIAS,
    CENSUS_AUTOMATION,
    CENSUS_GATE_PINNED,
    CENSUS_KINDS,
    EXPECTED_CENSUS_GATES,
    PINNING_MECHANISMS,
    REGISTRY,
    STRICT_SUBCHECKS,
    WORKFLOW_JOB_CENSUS,
    census_gate_keys,
    census_kinds,
    mirror_adopter_step_names,
    workflow_job_census,
)

WORKFLOWS_DIR = Path(__file__).resolve().parents[1] / ".github" / "workflows"


# ── stdlib-only parser ───────────────────────────────────────────────────────
def _all_workflow_jobs() -> set[str]:
    """Every workflow job across ``.github/workflows/*.yml`` as
    ``"<filename>::<job_id>"``.

    Stdlib string-splitting only (no yaml): slice each file from its top-level
    ``jobs:`` key, then collect the IMMEDIATE 2-space-indented child keys (the
    job ids), stopping at the next top-level (column-0) key. A 4-space-or-deeper
    step key never matches (the pattern anchors on exactly two leading spaces),
    and comment lines (``  #…``) are not keys. The analogue of
    ``_kit_quality_block`` / ``_named_steps`` in ``tests/test_guard_parity.py``.
    """
    jobs: set[str] = set()
    for wf in sorted(WORKFLOWS_DIR.glob("*.yml")):
        text = wf.read_text(encoding="utf-8")
        match = re.search(r"^jobs:", text, re.MULTILINE)
        if match is None:
            continue
        for line in text[match.end() :].splitlines():
            # A non-indented, non-blank line is a new top-level key — the
            # jobs: block has ended.
            if line and not line[0].isspace():
                break
            job = re.match(r"  ([A-Za-z0-9_-]+):", line)
            if job:
                jobs.add(f"{wf.name}::{job.group(1)}")
    return jobs


# ── tests ────────────────────────────────────────────────────────────────────
def test_every_workflow_job_is_censused():
    """Bidirectional set-equality between the live workflow jobs and the
    census. The primary drift-catch: a new gating (or automation) job cannot be
    added silently, and a removed one cannot linger in the census."""
    discovered = _all_workflow_jobs()
    censused = set(WORKFLOW_JOB_CENSUS)
    unclassified = discovered - censused
    stale = censused - discovered
    assert not unclassified and not stale, (
        "workflow-job ⇄ WORKFLOW_JOB_CENSUS drift in src/engine/guards.py.\n"
        f"  NEW, un-censused workflow job(s): {sorted(unclassified)}\n"
        "    → classify each in WORKFLOW_JOB_CENSUS as CENSUS_GATE_PINNED "
        "(an enforcing gate — and parity-pin it like the others), "
        "CENSUS_ALIAS (a temporary legacy required-context alias), or "
        "CENSUS_AUTOMATION (non-enforcing automation that never reds a PR).\n"
        f"  REMOVED job(s) still in the census: {sorted(stale)}\n"
        "    → drop each from WORKFLOW_JOB_CENSUS."
    )


def test_census_finds_at_least_one_job_per_workflow_file():
    """Sanity floor on the parser: every workflow file contributes at least one
    job. Guards against a silently-broken ``jobs:`` slice (e.g. an empty set
    that would make the equality test vacuously satisfiable in one direction)."""
    files = sorted(WORKFLOWS_DIR.glob("*.yml"))
    assert files, "no workflow files found under .github/workflows/"
    discovered = _all_workflow_jobs()
    for wf in files:
        assert any(key.startswith(f"{wf.name}::") for key in discovered), (
            f"parser found no jobs in {wf.name} — the jobs: slice is broken."
        )


def test_gate_jobs_reference_a_real_pin():
    """Every CENSUS_GATE_PINNED entry carries a descriptive (>15-char) note AND
    its pin resolves to real, non-empty parity registries — a gate can never be
    a bare unbacked claim."""
    gate_keys = census_gate_keys()
    assert gate_keys, "the census must classify at least one enforcing gate."
    for key in gate_keys:
        _kind, note = WORKFLOW_JOB_CENSUS[key]
        assert len(note.strip()) > 15, (
            f"{key}: a GATE_PINNED note must describe WHERE the parity is "
            f"pinned; too-thin: {note!r}"
        )
    # The gate's pin is the three step-level registries — assert they are real
    # and non-empty, so "parity-pinned" is not a hollow label.
    assert REGISTRY, "REGISTRY (the ci.yml step pin) must be non-empty."
    assert mirror_adopter_step_names(), (
        "the MIRRORS subset (adopter substrate-gate step pin) must be non-empty."
    )
    assert STRICT_SUBCHECKS, (
        "STRICT_SUBCHECKS (the check --strict sub-check pin) must be non-empty."
    )


def test_out_of_scope_jobs_carry_a_reason():
    """Every CENSUS_ALIAS / CENSUS_AUTOMATION entry carries a descriptive
    (>15-char) reason — an out-of-scope registration can never be a bare escape
    hatch (the same bar as the KIT_ONLY allowlist in test_guard_parity)."""
    thin = {
        key: note
        for key, (kind, note) in WORKFLOW_JOB_CENSUS.items()
        if kind in (CENSUS_ALIAS, CENSUS_AUTOMATION) and len(note.strip()) <= 15
    }
    assert not thin, (
        "out-of-scope (ALIAS/AUTOMATION) census entries must carry a "
        f"descriptive (>15 char) reason; too-thin: {thin}"
    )


def test_census_kinds_are_known():
    """Every census kind value is one of the three defined constants — the
    classification stays legible instead of degrading to arbitrary strings."""
    for key, (kind, _note) in WORKFLOW_JOB_CENSUS.items():
        assert kind in CENSUS_KINDS, (
            f"{key}: unknown census kind {kind!r}; must be one of {CENSUS_KINDS}"
        )
    # census_kinds() is the accessor the (potential) external reader uses.
    assert set(census_kinds()) <= set(CENSUS_KINDS)


def test_census_gate_count_floor():
    """Anchor floor: at least EXPECTED_CENSUS_GATES enforcing gates today. A
    shrinkage guard (like EXPECTED_MIRRORS / EXPECTED_STRICT_SUBCHECKS) so the
    census can't be gutted to a vacuously-green empty gate set; bump the anchor
    deliberately when a genuinely new enforcing gate is added and pinned."""
    assert len(census_gate_keys()) >= EXPECTED_CENSUS_GATES, (
        f"expected at least {EXPECTED_CENSUS_GATES} CENSUS_GATE_PINNED gate(s), "
        f"found {len(census_gate_keys())} — if the enforcing gate set shrank, "
        "update EXPECTED_CENSUS_GATES deliberately."
    )


def test_enforcing_surface_kinds_are_complete():
    """The enumerated pinning mechanisms are exactly the three real,
    non-empty parity registries — {REGISTRY, MIRRORS, STRICT_SUBCHECKS} — so a
    'fourth pinning mechanism' can't be claimed without a home and none of the
    three can silently empty out."""
    assert set(PINNING_MECHANISMS) == {"REGISTRY", "MIRRORS", "STRICT_SUBCHECKS"}, (
        "the enumerated pinning mechanisms must be exactly the three surfaces "
        f"the census leans on; found {sorted(PINNING_MECHANISMS)}"
    )
    # Each mechanism resolves to a real, non-empty registry in guards.py.
    resolvers = {
        "REGISTRY": REGISTRY,
        "MIRRORS": mirror_adopter_step_names(),
        "STRICT_SUBCHECKS": STRICT_SUBCHECKS,
    }
    for name, registry in resolvers.items():
        assert registry, f"pinning mechanism {name!r} resolves to an empty registry."
        # Every enumerated mechanism carries a descriptive pointer.
        assert len(PINNING_MECHANISMS[name].strip()) > 15, (
            f"pinning mechanism {name!r} needs a descriptive pointer to its registry."
        )


def test_workflow_job_census_accessor_returns_a_copy():
    """``workflow_job_census()`` returns a COPY — a consumer mutating it can't
    corrupt the canonical registry."""
    snapshot = workflow_job_census()
    assert snapshot == WORKFLOW_JOB_CENSUS
    snapshot.clear()
    assert WORKFLOW_JOB_CENSUS, "the canonical census must be unaffected by a mutated copy."
