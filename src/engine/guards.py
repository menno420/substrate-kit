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


# ── Strict sub-check surface (bootstrap check --strict) ──────────────────────
# `bootstrap check --strict` runs a SECOND guard surface: the sub-checks
# assembled inline in ``engine.cli._extra_check_findings``. Unlike the ci.yml
# surface above, NONE of these are kit-only — the whole engine is concatenated
# into every adopter's ``dist/bootstrap.py`` (build_bootstrap.MODULE_ORDER), so
# each sub-check ALSO runs when an adopter runs ``bootstrap check --strict``.
# What varies is *when* each engages: some fire on every rendered adopter, some
# only when that adopter's interview filled the input the check reads.
# STRICT_SUBCHECKS pins the set by name; the parity test asserts set-equality
# against the actual ``check_*(`` calls in the live _extra_check_findings
# source, so a sub-check can't be dropped or renamed silently and a new one
# can't be wired in without a documented reason here.
STRICT_ADOPTER_ALWAYS = "ADOPTER_ALWAYS"  # engages on every rendered adopter
STRICT_ADOPTER_WHEN_CONFIGURED = "ADOPTER_WHEN_CONFIGURED"  # only when configured

STRICT_SUBCHECK_KINDS = (STRICT_ADOPTER_ALWAYS, STRICT_ADOPTER_WHEN_CONFIGURED)

STRICT_SUBCHECKS: dict[str, tuple[str, str]] = {
    "check_ledger": (
        STRICT_ADOPTER_ALWAYS,
        "the decision ledger is planted at adoption; runs whenever the ledger file exists",
    ),
    "check_stamp_discipline": (
        STRICT_ADOPTER_ALWAYS,
        "stamp discipline over docs/, which every rendered adopter ships",
    ),
    "check_namespace": (
        STRICT_ADOPTER_WHEN_CONFIGURED,
        "engages only when the adopter configured namespace.roots that exist on disk (code adopters)",
    ),
    "check_seam_authority": (
        STRICT_ADOPTER_WHEN_CONFIGURED,
        "engages only when the adopter configured audited seams",
    ),
    "check_no_false_walls": (
        STRICT_ADOPTER_ALWAYS,
        "called unconditionally; scans docs, CONSTITUTION.md, CAPABILITIES.md and .claude for false capability walls",
    ),
    "check_orientation_budget": (
        STRICT_ADOPTER_ALWAYS,
        "engages when boot docs exist; every adopter ships CLAUDE.md and current-state.md",
    ),
    "check_engagement": (
        STRICT_ADOPTER_ALWAYS,
        "the post-adopt engagement gate; engages for any repo carrying a kit_version",
    ),
}

# Anchor floor: the strict sub-check surface is exactly these 7 today. A
# shrinkage guard (like EXPECTED_MIRRORS/EXPECTED_KIT_ONLY above) so removing a
# sub-check from BOTH the code and this dict — which keeps set-equality green —
# still trips a red; bump deliberately when the set legitimately changes.
EXPECTED_STRICT_SUBCHECKS = 7


def strict_subcheck_names() -> list[str]:
    """The engine sub-checks ``cli._extra_check_findings`` must call under
    ``bootstrap check --strict`` — sourced from the same manifest the parity
    test asserts set-equality against."""
    return list(STRICT_SUBCHECKS)


def strict_subcheck_reasons() -> list[str]:
    """The one-line reason string of every strict sub-check entry."""
    return [reason for _kind, reason in STRICT_SUBCHECKS.values()]


# ── Fourth-surface guard: the workflow-job census ────────────────────────────
# The three registries above each pin ONE enforcing guard surface at
# STEP / SUB-CHECK granularity: REGISTRY pins the ci.yml ``kit-quality`` steps,
# its MIRRORS subset pins the generated adopter ``substrate-gate`` steps, and
# STRICT_SUBCHECKS pins the ``bootstrap check --strict`` sub-checks. What NONE
# of them pins is the SET OF SURFACES itself — a NEW enforcing surface could
# ship entirely unpinned. The concrete vector is a new WORKFLOW JOB: any job
# added under a ``.github/workflows/*.yml`` ``jobs:`` key can gate a PR (or run
# automation beside the gate) without appearing in any of the three step-level
# registries above.
#
# The census closes that vector. It classifies EVERY job across ALL workflow
# files as one of three kinds — a parity-pinned gate, a temporary legacy alias,
# or non-enforcing automation — so a FOURTH enforcing surface cannot appear
# without either a parity pin or an explicit out-of-scope registration with a
# reason. Pure data + tiny accessors; the meta-test
# (``tests/test_guard_surface_census.py``) parses the live workflow files with
# the same stdlib string-splitting the parity test uses and asserts
# bidirectional set-equality against WORKFLOW_JOB_CENSUS keys — a job added to
# any workflow, or a census entry with no live job, turns it red.

# The three census KINDS.
CENSUS_GATE_PINNED = "GATE_PINNED"  # enforcing gate whose parity is pinned elsewhere
CENSUS_ALIAS = "ALIAS"  # temporary legacy required-context alias (delete after P10)
CENSUS_AUTOMATION = "AUTOMATION"  # non-enforcing automation/dispatch — never reds a PR

CENSUS_KINDS = (CENSUS_GATE_PINNED, CENSUS_ALIAS, CENSUS_AUTOMATION)

# One entry per REAL job across every ``.github/workflows/*.yml``, keyed
# ``"<workflow_filename>::<job_id>"``. Read from ground truth (the live
# ``jobs:`` keys), never guessed. Value is ``(kind, note)``; every note is a
# descriptive (>15-char) reason, exactly like the KIT_ONLY / STRICT_SUBCHECKS
# reasons above.
WORKFLOW_JOB_CENSUS: dict[str, tuple[str, str]] = {
    # ── the one enforcing PR gate — parity-pinned by all three registries ──
    "ci.yml::kit-quality": (
        CENSUS_GATE_PINNED,
        "the one enforcing PR gate; its guard surface is parity-pinned at "
        "step/sub-check granularity by REGISTRY (kit-quality steps), the "
        "MIRRORS subset (adopter substrate-gate steps) and STRICT_SUBCHECKS "
        "(bootstrap check --strict sub-checks)",
    ),
    # ── temporary legacy required-context aliases (delete after the P10 swap) ──
    "ci.yml::legacy-alias-test": (
        CENSUS_ALIAS,
        "temporary legacy required-context alias for the folded-in 'Kit test "
        "suite' job; reports kit-quality's result verbatim. Delete once the "
        "P10 ruleset swap requires `kit-quality` instead (control/status.md "
        "⚡ P10 required-check swap)",
    ),
    "ci.yml::legacy-alias-smoke": (
        CENSUS_ALIAS,
        "temporary legacy required-context alias for the folded-in "
        "'Cold-adoption smoke' job; reports kit-quality's result verbatim. "
        "Delete once the P10 ruleset swap requires `kit-quality` "
        "(control/status.md ⚡ P10 required-check swap)",
    ),
    # ── non-enforcing automation — gates no PR check, never reds a PR ──
    "auto-merge-enabler.yml::enable-auto-merge": (
        CENSUS_AUTOMATION,
        "arms native auto-merge on non-draft claude/*|claim/* PRs; it never "
        "reds a PR and never merges itself — the merge stays gated by the "
        "required kit-quality check, so it enforces nothing",
    ),
    "auto-merge-disarm.yml::disarm": (
        CENSUS_AUTOMATION,
        "disarms native auto-merge when the do-not-automerge label is applied; "
        "a label-triggered convenience action that gates no PR check",
    ),
    "release.yml::release": (
        CENSUS_AUTOMATION,
        "tag-push / workflow_dispatch release publisher; runs off the release "
        "event (tags v*), not pull_request, so it never gates or reds a PR",
    ),
}

# Anchor floor: exactly ONE enforcing gate today (kit-quality). A shrinkage
# guard mirroring EXPECTED_MIRRORS / EXPECTED_STRICT_SUBCHECKS above — so the
# census can't be gutted to a vacuously-green empty set; bump deliberately when
# a genuinely new enforcing gate is added AND parity-pinned.
EXPECTED_CENSUS_GATES = 1

# The three step-level pinning MECHANISMS the census's GATE_PINNED gate leans
# on — each named with a pointer to its registry. The meta-test asserts this
# enumerated set is exactly {REGISTRY, MIRRORS, STRICT_SUBCHECKS} and that each
# resolves to a real, non-empty registry, so a "fourth pinning mechanism" can't
# be claimed without a home and none of the three can silently empty out.
PINNING_MECHANISMS: dict[str, str] = {
    "REGISTRY": (
        "ci.yml kit-quality step-level parity "
        "(and its MIRRORS subset -> adopter substrate-gate steps)"
    ),
    "MIRRORS": (
        "generated adopter substrate-gate step names (adopt.live_ci_workflow)"
    ),
    "STRICT_SUBCHECKS": (
        "bootstrap check --strict sub-check set (cli._extra_check_findings)"
    ),
}


# ── pure accessors (mirroring the REGISTRY / STRICT_SUBCHECKS accessor style) ─
def workflow_job_census() -> dict[str, tuple[str, str]]:
    """The full workflow-job census: ``"<workflow>::<job_id>"`` -> ``(kind, note)``.

    Returns a copy so a consumer can't mutate the canonical registry.
    """
    return dict(WORKFLOW_JOB_CENSUS)


def census_kinds() -> list[str]:
    """The kind value of every census entry, in registry order."""
    return [kind for kind, _note in WORKFLOW_JOB_CENSUS.values()]


def census_gate_keys() -> list[str]:
    """The keys of every ``CENSUS_GATE_PINNED`` entry — the enforcing gates."""
    return [
        key
        for key, (kind, _note) in WORKFLOW_JOB_CENSUS.items()
        if kind == CENSUS_GATE_PINNED
    ]


def census_notes() -> list[str]:
    """The note string of every census entry."""
    return [note for _kind, note in WORKFLOW_JOB_CENSUS.values()]


# ---------------------------------------------------------------------------
# Fast-lane branch-prefix symmetry (B-3)
# ---------------------------------------------------------------------------
# The set of head-branch prefixes that ride the auto-merge fast lane is
# duplicated across surfaces that nothing keeps in agreement:
#   * the auto-merge-enabler arms native auto-merge on these prefixes
#     (.github/workflows/auto-merge-enabler.yml -- startsWith(head_ref, '<p>')),
#   * the claims-only fast-lane guard cards exactly the CARDED ones
#     (.github/workflows/ci.yml -- case "$head_ref" in claude/*),
#   * the engine defaults hand adopters the same set
#     (adopt.DEFAULT_AUTOMERGE_BRANCH_PATTERNS, claim.BRANCH_PREFIX).
# A prefix the enabler arms but the registry/guard doesn't know reopens a
# card-less merge hole; a carded prefix the enabler doesn't arm is the kit#293
# green-and-unarmed stall. This registry pins the canonical set;
# tests/test_fastlane_prefix_symmetry.py asserts every live surface agrees,
# both directions. (The disarm workflow keys on the do-not-automerge LABEL, not
# a prefix, so it is deliberately outside this symmetry.)

FASTLANE_CARDED = "carded"  # work PRs -- the guard requires a session card
FASTLANE_CARDLESS = "card-less"  # ride the fast lane card-free by design

FASTLANE_KINDS = (FASTLANE_CARDED, FASTLANE_CARDLESS)

# prefix (trailing "/") -> kind. The enabler must arm every prefix here; the
# claims-only guard must card exactly the FASTLANE_CARDED ones.
FASTLANE_PREFIX_REGISTRY = {
    "claude/": FASTLANE_CARDED,
    "claim/": FASTLANE_CARDLESS,
}

# Floor: shrinking below this flags a prefix silently dropped from the fast
# lane (mirrors EXPECTED_CENSUS_GATES / EXPECTED_MIRRORS).
EXPECTED_FASTLANE_PREFIXES = 2


def fastlane_prefixes():
    """All fast-lane-eligible head-branch prefixes -> kind (copy)."""
    return dict(FASTLANE_PREFIX_REGISTRY)


def fastlane_carded_prefixes():
    """Prefixes the claims-only guard must require a session card for."""
    return {p for p, kind in FASTLANE_PREFIX_REGISTRY.items() if kind == FASTLANE_CARDED}


def fastlane_cardless_prefixes():
    """Prefixes that ride the fast lane card-free by design."""
    return {p for p, kind in FASTLANE_PREFIX_REGISTRY.items() if kind == FASTLANE_CARDLESS}
