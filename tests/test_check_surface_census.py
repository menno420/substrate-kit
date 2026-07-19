"""S10 — the guard-surface census NOTE (``surface_census_note``).

Pins the wave-2 groom S10 contract: the census ``guards.py`` already carries —
``REGISTRY`` (ci.yml kit-quality steps), ``WORKFLOW_JOB_CENSUS`` (workflow jobs),
``STRICT_SUBCHECKS`` (``check --strict`` sub-checks), ``HOOK_CENSUS`` (lifecycle
hooks) — is surfaced as ONE informational NOTE in ``check`` output, sourced live
from the authoritative accessors, never a ``Finding`` and never exit-affecting.

These are the visibility (NOTE) counterpart to the ENFORCEMENT meta-test
``tests/test_guard_surface_census.py`` (which pins the census-vs-live-tree
set-equality). Together: the meta-test keeps the registries honest; S10 makes
them visible.
"""

from __future__ import annotations

from pathlib import Path

from engine import guards
from engine.checks.check_surface_census import surface_census_note


def test_note_is_a_string_with_all_four_surfaces():
    """The NOTE prints and names all four pinned surfaces (guards, jobs,
    sub-checks, hooks) so the census is legible at a glance."""
    note = surface_census_note()
    assert isinstance(note, str)
    lowered = note.lower()
    assert "surface census" in lowered
    assert "kit-quality step" in lowered
    assert "workflow job" in lowered
    assert "check --strict` sub-check" in note  # keep the backtick literal
    assert "lifecycle hook" in lowered


def test_note_counts_match_the_live_registries():
    """Every number in the NOTE is sourced from the guards.py accessors — a
    registry change flows straight into the surfaced line (no hardcoded count)."""
    guard_counts = guards.counts()
    guard_total = sum(guard_counts.values())
    jobs = guards.workflow_job_census()
    subchecks = len(guards.STRICT_SUBCHECKS)
    hooks = guards.hook_census()

    note = surface_census_note()
    assert f"{guard_total} ci.yml kit-quality step(s)" in note
    assert f"setup {guard_counts['SETUP']}" in note
    assert f"mirrors {guard_counts['MIRRORS']}" in note
    assert f"kit-only {guard_counts['KIT_ONLY']}" in note
    assert f"{len(jobs)} workflow job(s)" in note
    assert f"{subchecks} `check --strict` sub-check(s)" in note
    assert f"{len(hooks)} lifecycle hook(s)" in note


def test_job_and_hook_breakdowns_sum_to_the_totals():
    """The gate/alias/automation split sums to the job total, and the
    advisory/orientation/enforcing split sums to the hook total — the census
    partitions each surface, it does not double-count or drop entries."""
    jobs = guards.workflow_job_census()
    hooks = guards.hook_census()
    gate = sum(
        1
        for kind, _n in jobs.values()
        if kind not in (guards.CENSUS_ALIAS, guards.CENSUS_AUTOMATION)
    )
    alias = sum(1 for kind, _n in jobs.values() if kind == guards.CENSUS_ALIAS)
    auto = sum(1 for kind, _n in jobs.values() if kind == guards.CENSUS_AUTOMATION)
    assert gate + alias + auto == len(jobs)

    adv = sum(1 for kind, _n in hooks.values() if kind == guards.HOOK_ADVISORY)
    ori = sum(1 for kind, _n in hooks.values() if kind == guards.HOOK_ORIENTATION)
    enf = sum(1 for kind, _n in hooks.values() if kind == guards.HOOK_ENFORCING)
    assert adv + ori + enf == len(hooks)

    note = surface_census_note()
    assert f"gate {gate} · alias {alias} · automation {auto}" in note
    assert f"advisory {adv} · orientation {ori} · enforcing {enf}" in note


def test_accepts_target_and_config_for_signature_parity(tmp_path: Path):
    """Signature parity with the other NOTE emitters (native_gate_note): it takes
    ``(target, config)`` and ignores them — the census is static registry data,
    so an arbitrary tree / config never changes or breaks the note."""
    a = surface_census_note()
    b = surface_census_note(tmp_path, object())
    assert a == b


def test_returns_none_only_on_a_vacuous_surface(monkeypatch):
    """The guard-only escape: if EVERY registry were empty the note is None (no
    line worth printing). The guards.py anchor floors keep that from happening in
    practice, so the line effectively always prints — this pins the branch."""
    monkeypatch.setattr(
        "engine.checks.check_surface_census.counts",
        lambda: {"SETUP": 0, "MIRRORS": 0, "KIT_ONLY": 0},
    )
    monkeypatch.setattr(
        "engine.checks.check_surface_census.workflow_job_census", lambda: {}
    )
    monkeypatch.setattr(
        "engine.checks.check_surface_census.hook_census", lambda: {}
    )
    monkeypatch.setattr(
        "engine.checks.check_surface_census.STRICT_SUBCHECKS", {}
    )
    assert surface_census_note() is None


def test_wired_into_cli_note_seam():
    """The NOTE is actually reachable from cmd_check — cli imports the emitter,
    so the surfaced line is not dead code."""
    from engine import cli

    assert cli.surface_census_note is surface_census_note


def test_never_raises():
    """A NOTE emitter on a green path must never raise — pure registry reads."""
    # Called every possible way the cli seam could call it.
    surface_census_note()
    surface_census_note(None, None)
    surface_census_note(Path("."), None)
