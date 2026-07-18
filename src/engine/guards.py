"""Guard manifest — the SINGLE SOURCE OF TRUTH for the kit-CI ⇄ adopter-CI
guard mapping.

Two CI guard surfaces must stay in agreement:

  * the kit's OWN CI — ``.github/workflows/ci.yml``, job ``kit-quality``;
  * the GENERATED adopter CI every host receives — the ``substrate-gate`` job
    :func:`engine.adopt.live_ci_workflow` emits.

Historically the mapping was maintained in TWO hand-kept places: the adopter
step-name literals lived inline in :func:`adopt.live_ci_workflow`, and the
parity meta-test (:mod:`tests.test_guard_parity`) carried its own private
``REGISTRY`` copy of the same names. Adding or renaming a guard meant editing
both, and nothing detected the drift when only one moved (the #455/#457 gap
this whole surface exists to close). This module collapses the two into one
declarative manifest that BOTH consumers read:

  * :func:`adopt.live_ci_workflow` sources the five MIRRORS adopter step
    NAMES from the constants here, so the YAML it emits and the parity
    registry can no longer disagree by construction; and
  * :mod:`tests.test_guard_parity` imports :data:`REGISTRY` (plus the
    :data:`SETUP` / :func:`MIRRORS` / :func:`KIT_ONLY` sentinels and the
    :data:`EXPECTED_MIRRORS` / :data:`EXPECTED_KIT_ONLY` anchor floors) from
    here instead of re-declaring them.

Adding, renaming, or removing a guard is now a ONE-PLACE edit: this file.

Pure data + tiny pure accessors. Stdlib-only, no subprocess, no I/O at import
(the same discipline every engine module keeps, §3.2).
"""

from __future__ import annotations

# ── the five adopter (substrate-gate) step NAMES that mirror a kit guard ─────
# These are the EXACT ``- name:`` strings live_ci_workflow() emits for the
# enforcing steps that have a kit-quality counterpart. adopt.py references
# these constants so the emitted YAML name and the MIRRORS payload below are
# the same object — never two hand-kept copies. Match by exact string
# equality; do not paraphrase a character.
ADOPTER_CONTROL_STATUS_GATE = (
    "control-status gate (fast lane — a control diff must still prove its heartbeat)"
)
ADOPTER_INBOX_APPEND_GATE = (
    "inbox append-only gate (control/inbox.md pure-append + ORDER grammar)"
)
ADOPTER_CLAIMS_FASTLANE_GUARD = (
    "claims-only fast-lane guard (claude/* work PRs must carry a session card)"
)
ADOPTER_PYTEST_SUITE = (
    "pytest suite (a test suite ships with its CI runner; "
    "self-skips when tests/ is absent)"
)
ADOPTER_SUBSTRATE_GATE = "substrate gate (docs + session-log required)"


# ── sentinels ────────────────────────────────────────────────────────────────
# A tiny three-way classification. SETUP is a bare marker; MIRRORS / KIT_ONLY
# carry a payload (the adopter step name / the kit-only reason).
SETUP = ("SETUP",)


def MIRRORS(adopter_step_name: str) -> tuple[str, str]:
    """An enforcing guard with a live counterpart in the adopter ``substrate-gate`` job."""
    return ("MIRRORS", adopter_step_name)


def KIT_ONLY(why: str) -> tuple[str, str]:
    """An enforcing guard that is legitimately kit-only, with a one-line reason."""
    return ("KIT_ONLY", why)


# ── the maintained registry ─────────────────────────────────────────────────
# One entry per NAMED kit-quality step (bare `uses:` steps — checkout,
# setup-python — have no name and are excluded by construction). Keys are the
# EXACT step-name strings read from ci.yml; MIRRORS targets are the EXACT
# adopter step-name strings emitted by live_ci_workflow() (sourced from the
# ADOPTER_* constants above, so this registry and the generator cannot drift).
REGISTRY: dict[str, tuple[str, ...]] = {
    # ── non-enforcing setup / detect / echo — no parity needed ──
    "Control fast lane detect (KL-8 — control/**-only diff)": SETUP,
    "Control fast lane (green by design)": SETUP,
    "Install dev tools": SETUP,
    # ── enforcing guards mirrored in the generated adopter CI ──
    "Control-status gate (fast lane — the one check a control diff must still pass)": MIRRORS(
        ADOPTER_CONTROL_STATUS_GATE
    ),
    "Inbox append-only gate (control/inbox.md pure-append + ORDER grammar)": MIRRORS(
        ADOPTER_INBOX_APPEND_GATE
    ),
    "Claims-only fast-lane guard (claude/* work PRs must carry a session card)": MIRRORS(
        ADOPTER_CLAIMS_FASTLANE_GUARD
    ),
    "Kit test suite (§3.2 item 1)": MIRRORS(ADOPTER_PYTEST_SUITE),
    "Session gate (§3.2 item 5 — dogfood, the born-red discipline)": MIRRORS(
        ADOPTER_SUBSTRATE_GATE
    ),
    # ── enforcing guards that are legitimately kit-only ──
    "Dist byte-equality pin (§3.2 item 2)": KIT_ONLY(
        "adopters ship no dist/bootstrap.py, so there is no built artifact to byte-pin"
    ),
    "Engine lint bans (§3.2 item 3 — no print/assert/subprocess)": KIT_ONLY(
        "adopters carry no src/engine/ tree; the ruff bans target kit engine source only"
    ),
    "Idea index (§5.4 — B4 frontmatter + backlog consistency)": KIT_ONLY(
        "validates the kit repo's own docs/ideas index; not part of the adopter deliverable"
    ),
    "Retro index (docs/retro reachability — no unindexed retro file)": KIT_ONLY(
        "validates the kit repo's own retro index; not part of the adopter deliverable"
    ),
    "CHANGELOG structure ([Unreleased] keep-a-changelog shape)": KIT_ONLY(
        "validates the kit's own CHANGELOG; adopters carry no kit CHANGELOG"
    ),
    'No false merge-walls (forward-binding surfaces don\'t re-seed "agents cannot merge")': KIT_ONLY(
        "propagated into adopters via `bootstrap check --strict` (PR #450), "
        "not as a separate generated-CI step"
    ),
    "Taxonomy sync (PL-004 — TASK_CLASSES ⇄ ladder ⇄ telemetry README)": KIT_ONLY(
        "validates the kit's own program/taxonomy docs; kit-internal"
    ),
    "Program law (§8.3 — PL register grammar + planted pointers + owner-gate label)": KIT_ONLY(
        "validates the kit's own program-law label gate; kit-internal governance"
    ),
    "Bench integrity (§5.0 — pin-path label gate + append-only results)": KIT_ONLY(
        "validates the kit's own bench harness; kit-internal"
    ),
    "Cold-adoption smoke (§3.2 item 4 — the KL-7 RED→ENGAGED→GREEN arc)": KIT_ONLY(
        "exercises the adopt→render→session arc on the kit itself; an adopter "
        "does not re-adopt, so it has no adopter-CI analogue"
    ),
}

# Anchor floors: the guard surface today is exactly 5 MIRRORS and 10 KIT_ONLY
# enforcing guards. These track the surface as a shrinkage guard so the
# registry can't be silently gutted to an empty (vacuously green) pass; bump
# them deliberately when the guard set legitimately changes.
EXPECTED_MIRRORS = 5
EXPECTED_KIT_ONLY = 10


# ── pure accessors the two consumers read ────────────────────────────────────
def manifest() -> dict[str, tuple[str, ...]]:
    """The full ordered guard manifest: kit-quality step name -> classification."""
    return REGISTRY


def classification_by_kit_step() -> dict[str, tuple[str, ...]]:
    """Alias of :data:`REGISTRY` — kit step name -> ``(kind, *payload)`` tuple."""
    return REGISTRY


def mirror_adopter_step_names() -> list[str]:
    """The adopter ``substrate-gate`` step names every MIRRORS entry points at.

    These are exactly the names :func:`adopt.live_ci_workflow` must emit for the
    parity test's mirror check to pass — sourced from the same constants the
    generator uses.
    """
    return [p[1] for p in REGISTRY.values() if p[0] == "MIRRORS"]


def kit_only_reasons() -> list[str]:
    """The one-line reason string of every KIT_ONLY entry."""
    return [p[1] for p in REGISTRY.values() if p[0] == "KIT_ONLY"]


def counts() -> dict[str, int]:
    """Count of guards by kind — ``{"SETUP": n, "MIRRORS": n, "KIT_ONLY": n}``."""
    tally = {"SETUP": 0, "MIRRORS": 0, "KIT_ONLY": 0}
    for payload in REGISTRY.values():
        tally[payload[0]] += 1
    return tally
