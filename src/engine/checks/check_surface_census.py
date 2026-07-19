"""Guard-surface census NOTE — surface the pinned enforcement surfaces in `check`.

Provenance: docs/planning/2026-07-19-night-run-idea-groom-wave2.md S10 (this PR).
Sibling of the ``native_gate_note`` / ``required_unverified_note`` NOTE emitters
in ``check_engagement.py`` (the "surface information in check output, never a
finding" pattern), not of the posture="advisory" *finding* checkers.

Why this exists: ``src/engine/guards.py`` already pins the kit's whole
enforcement surface — the SET of guard surfaces, not just each surface's steps —
across four registries:

  * ``REGISTRY``            — the ci.yml ``kit-quality`` steps (SETUP / MIRRORS / KIT_ONLY)
  * ``WORKFLOW_JOB_CENSUS`` — every ``.github/workflows/*.yml`` job (gate / alias / automation)
  * ``STRICT_SUBCHECKS``    — the ``bootstrap check --strict`` sub-check set
  * ``HOOK_CENSUS``         — the Claude Code lifecycle hooks (advisory / orientation / enforcing)

Those registries are ENFORCED only by the kit-only meta-test
``tests/test_guard_surface_census.py`` (bidirectional set-equality vs the live
tree), which an adopter never runs and which is invisible at ``check`` time. So
the census that says "this is the full guard surface this bootstrap ships" is
today knowable only by reading source or the kit's CI. S10 makes it VISIBLE:
one concise informational line in ``check`` output, sourced live from the
authoritative ``guards.py`` accessors.

Posture — a NOTE, the extreme fail-open form of "advisory": it is emitted, never
counted toward the exit code, never a ``Finding``, and NOT in ``STRICT_SUBCHECKS``.
The census is always-emitted *information*, not a conditional warning — the drift
DETECTION an advisory *finding* form would add is already the meta-test above, so
reimplementing that here would be redundant and weaker (and, for an adopter whose
own tree differs from these kit-baked registries, meaningless). Hence the
NOTE-emitter shape rather than a ``list[Finding]`` checker. See this rank's card
``⚑ Self-initiated`` line for the deviation flag.

What it reports: the census describes THE GUARD SURFACE THIS BOOTSTRAP SHIPS
(the ``guards.py`` registries baked into the concatenated dist) — accurate as
"the kit's declared surface" in the kit repo (where it also equals the live
tree, per the meta-test) and in any adopter dist (where it is the kit version's
declared surface). Sourced from the pure accessors, never re-parsing the tree,
so it is stdlib-only, allocation-cheap, and can never raise on a malformed tree.

``target`` / ``config`` are accepted for signature parity with the other
NOTE emitters (``native_gate_note(target, config)``); unused today — the census
is static registry data. Public on purpose: ``cmd_check``'s full lane emits it,
like the acceptance / required-ness NOTEs beside it.

Import form mirrors ``adopt.py`` — ``from engine.guards import <names>`` — so the
bare accessor names resolve in the concatenated ``dist/bootstrap.py`` (the
``from engine`` import line is stripped at build time; the names already live in
the single shared namespace). Stdlib only.
"""

from __future__ import annotations

from typing import Any

from engine.guards import (
    CENSUS_ALIAS,
    CENSUS_AUTOMATION,
    HOOK_ADVISORY,
    HOOK_ENFORCING,
    HOOK_ORIENTATION,
    STRICT_SUBCHECKS,
    counts,
    hook_census,
    workflow_job_census,
)


def surface_census_note(target: Any = None, config: Any = None) -> str | None:
    """One-line census of the guard surface this bootstrap ships, or ``None``.

    Returns ``None`` only in the (guard-only) event that every registry is
    empty — a vacuous surface not worth a line; the ``guards.py`` anchor floors
    (``EXPECTED_MIRRORS`` etc.) keep that from happening in practice, so the
    line effectively always prints. Never raises; pure registry reads.

    ``target`` / ``config`` are accepted for signature parity with the other
    NOTE emitters and are unused (the census is static registry data)."""
    guard_counts = counts()  # {"SETUP": n, "MIRRORS": n, "KIT_ONLY": n}
    guard_total = sum(guard_counts.values())

    jobs = workflow_job_census()  # "<wf>::<job>" -> (kind, note)
    job_total = len(jobs)
    job_gate = sum(1 for kind, _n in jobs.values() if kind not in (CENSUS_ALIAS, CENSUS_AUTOMATION))
    job_alias = sum(1 for kind, _n in jobs.values() if kind == CENSUS_ALIAS)
    job_auto = sum(1 for kind, _n in jobs.values() if kind == CENSUS_AUTOMATION)

    subcheck_total = len(STRICT_SUBCHECKS)

    hooks = hook_census()  # "<dispatch>" -> (kind, note)
    hook_total = len(hooks)
    hook_adv = sum(1 for kind, _n in hooks.values() if kind == HOOK_ADVISORY)
    hook_ori = sum(1 for kind, _n in hooks.values() if kind == HOOK_ORIENTATION)
    hook_enf = sum(1 for kind, _n in hooks.values() if kind == HOOK_ENFORCING)

    if not (guard_total or job_total or subcheck_total or hook_total):
        return None  # vacuous surface — no line worth printing

    return (
        "surface census — the guard surface this bootstrap ships (src/engine/"
        f"guards.py, pinned by tests/test_guard_surface_census.py): {guard_total} "
        f"ci.yml kit-quality step(s) (setup {guard_counts['SETUP']} · mirrors "
        f"{guard_counts['MIRRORS']} · kit-only {guard_counts['KIT_ONLY']}), "
        f"{job_total} workflow job(s) (gate {job_gate} · alias {job_alias} · "
        f"automation {job_auto}), {subcheck_total} `check --strict` sub-check(s), "
        f"{hook_total} lifecycle hook(s) (advisory {hook_adv} · orientation "
        f"{hook_ori} · enforcing {hook_enf})."
    )
