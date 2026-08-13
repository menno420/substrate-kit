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
# Adopter-only extension point (v1.21.0) — no kit-quality mirror by design:
# the step's CONTENT is host-owned (scripts/repo_checks.sh), so there is no
# kit guard for it to mirror. It exists because host checkers hand-added into
# the kit-owned gate were silently dropped at every regen (fm #833).
ADOPTER_REPO_CHECKERS = (
    "repo checkers (host-owned scripts/repo_checks.sh; self-skips when absent)"
)


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


# ── Fourth-surface guard #2: the lifecycle-hook census ───────────────────────
# WORKFLOW_JOB_CENSUS above pins the SET of workflow-job surfaces. The SECOND
# fourth-surface vector is the kit's Claude Code LIFECYCLE HOOKS: the four hook
# entry points the kit plants into a host ``.claude/settings.json`` and
# dispatches through ``cli.cmd_hook`` (``cli._HOOK_EVENTS`` keys
# ``pretooluse`` / ``sessionstart`` / ``postedit`` / ``stopcheck``, wired by
# ``src/engine/hooks/settings.py`` ``_SET_EVENTS``). A NEW hook can be added to
# that dispatch — and even wired into the settings template — WITHOUT appearing
# in any parity registry: it can ship unregistered (no census entry) or
# unclassified (guard-shaped but never confirmed fail-open). Nothing red-flags
# that.
#
# NOTE ON THE NAME: the groom recipe called this "enumerate repo git-hooks",
# but the kit ships ZERO git-hooks (no ``.git/hooks`` planting, no
# pre-commit/pre-push shell). Its real fourth hook surface is these four
# CLAUDE CODE lifecycle hooks, so the census pins THOSE — faithful to the
# baton's intent ("a new hook can't ship unregistered/unclassified"), just
# corrected for the misnomer.
#
# The census closes the vector by classifying EVERY dispatched hook as one of
# three kinds — a fail-open ADVISORY guard, a non-guard ORIENTATION context
# injector, or a would-be ENFORCING hook (none today; a hook that can
# block/deny must reference a pin, exactly like a GATE_PINNED workflow job).
# Pure data + tiny accessors; the meta-test
# (``tests/test_guard_surface_census.py``) asserts bidirectional set-equality
# against ``cli._HOOK_EVENTS`` and pins the ADVISORY set to
# ``cli._HOOK_GUARD_KINDS`` — a hook added to dispatch, or a census entry with
# no live hook, turns it red.

# The three hook KINDS.
HOOK_ENFORCING = "ENFORCING"  # a hook that can block/deny — must reference a pin
HOOK_ADVISORY = "ADVISORY"  # fail-open guard: always exits 0, surfaces guidance only
HOOK_ORIENTATION = "ORIENTATION"  # non-guard context injector (SessionStart), never gates

HOOK_KINDS = (HOOK_ENFORCING, HOOK_ADVISORY, HOOK_ORIENTATION)

# One entry per REAL lifecycle hook, keyed by its ``cli._HOOK_EVENTS`` dispatch
# name. Read from ground truth (the live dispatch + guard-kind maps), never
# guessed. Value is ``(kind, note)``; every note is a descriptive (>15-char)
# reason, exactly like the WORKFLOW_JOB_CENSUS / STRICT_SUBCHECKS reasons above.
# The three ADVISORY entries are exactly ``cli._HOOK_GUARD_KINDS``; the lone
# ORIENTATION entry (``sessionstart``) is deliberately absent from that map — it
# injects context and records no guard fire.
HOOK_CENSUS: dict[str, tuple[str, str]] = {
    # ── fail-open advisory guards (exactly cli._HOOK_GUARD_KINDS) ──
    "pretooluse": (
        HOOK_ADVISORY,
        "PreToolUse stance guard (cli._hook_pretooluse, guard-kind 'stance'); "
        "warns on an out-of-stance tool but is fail-open — always exits 0, "
        "never blocks the tool call",
    ),
    "postedit": (
        HOOK_ADVISORY,
        "PostToolUse edit advisor (cli._hook_postedit, guard-kind "
        "'edit-advisor'); surfaces generated-artifact / unbadged-doc warnings "
        "on stderr, fail-open — always exits 0",
    ),
    "stopcheck": (
        HOOK_ADVISORY,
        "Stop-check advisor (cli._hook_stopcheck, guard-kind 'stop-advisory'); "
        "surfaces session-close hygiene on stderr, fail-open — always exits 0",
    ),
    # ── non-guard orientation injector (absent from cli._HOOK_GUARD_KINDS) ──
    "sessionstart": (
        HOOK_ORIENTATION,
        "SessionStart orientation (cli._hook_sessionstart); prints the "
        "mode-aware orientation composition to stdout, injecting context — it "
        "is not a guard and records no guard fire",
    ),
}

# Anchor floor: exactly THREE fail-open advisory guards today (stance, edit,
# stop). A shrinkage guard mirroring EXPECTED_CENSUS_GATES / EXPECTED_MIRRORS
# above — so the census can't be gutted to a vacuously-green empty advisory set;
# bump deliberately when a genuinely new advisory hook is added.
EXPECTED_HOOK_ADVISORY = 3


# ── pure accessors (mirroring the WORKFLOW_JOB_CENSUS accessor style) ─────────
def hook_census() -> dict[str, tuple[str, str]]:
    """The full lifecycle-hook census: ``"<dispatch_name>"`` -> ``(kind, note)``.

    Returns a copy so a consumer can't mutate the canonical registry.
    """
    return dict(HOOK_CENSUS)


def hook_census_kinds() -> list[str]:
    """The kind value of every hook census entry, in registry order."""
    return [kind for kind, _note in HOOK_CENSUS.values()]


def hook_advisory_keys() -> list[str]:
    """The keys of every ``HOOK_ADVISORY`` entry — the fail-open guard hooks."""
    return [
        key for key, (kind, _note) in HOOK_CENSUS.items() if kind == HOOK_ADVISORY
    ]


def hook_orientation_keys() -> list[str]:
    """The keys of every ``HOOK_ORIENTATION`` entry — the non-guard injectors."""
    return [
        key for key, (kind, _note) in HOOK_CENSUS.items() if kind == HOOK_ORIENTATION
    ]


def hook_enforcing_keys() -> list[str]:
    """The keys of every ``HOOK_ENFORCING`` entry — hooks that can block/deny.

    Empty today (every planted hook is fail-open); the accessor exists so the
    meta-test can assert a future enforcing hook references a pin.
    """
    return [
        key for key, (kind, _note) in HOOK_CENSUS.items() if kind == HOOK_ENFORCING
    ]


def hook_census_notes() -> list[str]:
    """The note string of every hook census entry."""
    return [note for _kind, note in HOOK_CENSUS.values()]


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

# ── Fifth surface: the ADVISORY census (deterministic vs heuristic) ──────────
# The four censuses above pin the ENFORCING surfaces: which steps, jobs,
# sub-checks and hooks can red a PR. None of them says anything about the
# surface an agent actually READS. `check --strict` emits, beside its
# exit-affecting findings, a long tail of blocks each labelled "(never
# exit-affecting)". Measured 2026-08-06 at HEAD: that tail is 41 of 47 output
# lines on substrate-kit (87%) and 80 of 89 on fleet-manager (90%) -- with BOTH
# trees exiting 0. Every tag that fired was an aging nag or a false positive
# (13 stale-wall rows titled 'any'; nine skill-grounds rows naming `READ FIRST`
# and a numpy expression as unresolved "commands"). No deterministic structural
# checker fired on either tree.
#
# So the channel an agent consults to decide whether it is done runs at roughly
# 1:9 signal to noise, and the noise is wrong. That is Goodhart pointed at a
# feedback loop: an agent's default response to a warning is to try to fix it,
# so a large permanent field of false warnings is not neutral -- it actively
# recruits effort toward hallucinated repairs.
#
# The fix is NOT to gate the tail (a noisy heuristic wired hard produces an
# agent inventing changes to satisfy a false positive, then a deadlocked PR).
# It is to CLASSIFY it, and route by class:
#
#   * DETERMINISTIC -- the finding is a structural disagreement between two
#     surfaces, or an unresolved reference. Binary, no judgement, no prose
#     matching. A finding is a defect. These stay in the agent's channel.
#   * HEURISTIC -- the finding is an aging nag, a count, or an inference over
#     prose. It may be a false positive by construction. These leave the
#     agent's channel entirely and land in the advisory report, where they are
#     an owner-facing periodic read rather than a gate line.
#
# Both classes keep recording guard fires exactly as before: only stdout moves,
# so routing is exit-neutral by construction.
#
# Keys are the advisory VARIABLE names in `cli.cmd_check` -- the emit sites the
# routing governs. `tests/test_advisory_census.py` asserts bidirectional
# set-equality against the live `_advisory_out(` call sites, so an advisory
# block cannot ship unclassified and a census entry cannot outlive its block.
ADVISORY_DETERMINISTIC = "DETERMINISTIC"
ADVISORY_HEURISTIC = "HEURISTIC"

ADVISORY_KINDS = (ADVISORY_DETERMINISTIC, ADVISORY_HEURISTIC)

# name -> (kind, producing checker, why it is classified that way)
ADVISORY_CENSUS: dict[str, tuple[str, str, str]] = {
    # ── DETERMINISTIC: two surfaces disagree, or a reference does not resolve ──
    "staged_regen_advisories": (
        ADVISORY_DETERMINISTIC,
        "check_staged_regen",
        "a staged artifact still carries a literal ${slot} whose answer is "
        "already filled in state -- a string-presence test against a recorded "
        "value, with no judgement in it",
    ),
    "template_sync_advisories": (
        ADVISORY_DETERMINISTIC,
        "check_template_sync",
        "set difference between a template's heading set and its local copy's; "
        "a heading is present on one side or it is not",
    ),
    "automerge_advisories": (
        ADVISORY_DETERMINISTIC,
        "check_automerge_preflight",
        "set comparison between the planted enabler's branch allowlist and "
        "automerge.branch_patterns -- two committed surfaces that either agree "
        "or do not",
    ),
    "strength_advisories": (
        ADVISORY_DETERMINISTIC,
        "check_enforcement_strength",
        "flag comparison between the wired `check --strict` door and the "
        "staged gate's stronger legs; both flag sets are read from committed "
        "YAML",
    ),
    "folded_gate_advisories": (
        ADVISORY_DETERMINISTIC,
        "check_folded_gate",
        "detects one specific structural shape in a host-folded gate (the "
        "pre-#19 newest-by-mtime card picker); the shape is present or absent",
    ),
    "fastlane_symmetry_advisories": (
        ADVISORY_DETERMINISTIC,
        "check_fastlane_symmetry",
        "set comparison between the prefixes the claims-only guard cards and "
        "the prefixes the enabler arms -- the FASTLANE_PREFIX_REGISTRY "
        "symmetry above, evaluated against a host tree",
    ),
    "recipe_applies_when_advisories": (
        ADVISORY_DETERMINISTIC,
        "check_recipe_applies_when",
        "parses an `applies-when:` badge and reports absent/empty/malformed; "
        "well-formedness is a grammar question, not a judgement (its HONESTY "
        "sibling, which reads the recipe's prose, is heuristic below)",
    ),
    "baton_resolves_advisories": (
        ADVISORY_DETERMINISTIC,
        "check_baton_resolves",
        "resolves a repo-relative path/anchor cited by a Next-2 baton against "
        "the filesystem -- the file and anchor exist or they do not",
    ),
    "boot_path_advisories": (
        ADVISORY_DETERMINISTIC,
        "check_boot_path",
        "walks the boot pointer chain -- agreement exists, carries a boot "
        "section, every path it names is on disk. Three file-presence tests "
        "and one heading match; no prose inference anywhere in it",
    ),
    # ── HEURISTIC: aging, counting, or inference over prose ──
    "status_advisories": (
        ADVISORY_HEURISTIC,
        "check_status_current",
        "the wall-clock STALENESS half of the heartbeat checker (its static "
        "gate half is exit-affecting and stays there); a heartbeat aging past "
        "a window is a clock reading, not a defect",
    ),
    "adopters_advisories": (
        ADVISORY_HEURISTIC,
        "check_adopters_current",
        "the staleness half of the adopter registry, exactly like the "
        "heartbeat above; the format half is exit-affecting and stays there",
    ),
    "owner_ask_advisories": (
        ADVISORY_HEURISTIC,
        "check_owner_actions",
        "judges whether a prose owner-ask is 'actionable'; the checker's own "
        "docstring calls the match coarse",
    ),
    "claim_advisories": (
        ADVISORY_HEURISTIC,
        "check_claims",
        "flags a claim collision the manager adjudicates -- the checker "
        "surfaces the tiebreak, it cannot decide it",
    ),
    "xref_advisories": (
        ADVISORY_HEURISTIC,
        "check_capability_xref",
        "coarse token overlap between an owner-ask and a ledger row; the call "
        "site already says a heuristic match can never be a verdict. Measured "
        "22 fires on fleet-manager, many byte-identical repeats",
    ),
    "setup_advisories": (
        ADVISORY_HEURISTIC,
        "check_setup_script",
        "detects a 'secret-shaped literal' in a host-owned script -- shape "
        "matching over arbitrary text",
    ),
    "grounds_advisories": (
        ADVISORY_HEURISTIC,
        "check_skill_grounds",
        "tokenizes skill prose and asks whether the first token names a "
        "command. Measured nine fires on fleet-manager, all false: `READ "
        "FIRST`, `verify <out.json>`, and a numpy expression",
    ),
    "archive_ready_advisories": (
        ADVISORY_HEURISTIC,
        "check_archive_ready",
        "infers a sham resolution from guarded default text surviving "
        "marker-stripping; UNVERIFIED per its own provenance header",
    ),
    "card_residue_advisories": (
        ADVISORY_HEURISTIC,
        "check_card_residue",
        "the same marker-stripping inference applied to session cards; the "
        "module docstring calls itself heuristic and UNVERIFIED",
    ),
    "digest_advisories": (
        ADVISORY_HEURISTIC,
        "check_seat_digest",
        "seat-digest drift nudge, UNVERIFIED per its provenance header; the "
        "fix is one regen command, not a defect to gate",
    ),
    "headroom_advisories": (
        ADVISORY_HEURISTIC,
        "check_orientation_headroom",
        "a GAUGE -- it fires when the boot set is NEAR the budget, not over "
        "it. The over-budget case is check_orientation_budget, which is "
        "exit-affecting and stays there",
    ),
    "model_line_advisories": (
        ADVISORY_HEURISTIC,
        "check_model_line",
        "classifies a prose Model line against a taxonomy; UNVERIFIED per its "
        "provenance header",
    ),
    "outbox_advisories": (
        ADVISORY_HEURISTIC,
        "list_outbox",
        "a pending-count nudge; a count is never a defect",
    ),
    "stale_walls_advisories": (
        ADVISORY_HEURISTIC,
        "check_stale_walls",
        "wall-clock aging of capability rows. Measured 33 fires on "
        "fleet-manager, 13 of them titled 'any' and four 'autonomous-project' "
        "-- the row extractor mis-parses, so even the subject is unreliable",
    ),
    "dateless_walls_advisories": (
        ADVISORY_HEURISTIC,
        "check_dateless_walls",
        "the complement of the ager above -- rows carrying no parseable date. "
        "Measured 12 fires on fleet-manager, largely on section headers rather "
        "than wall rows",
    ),
    "claim_provenance_advisories": (
        ADVISORY_HEURISTIC,
        "check_claim_provenance",
        "infers from prose whether a numeric table states its instrument; "
        "PL-014 itself scopes this as a nudge, noting a hard red would flag "
        "every existing measurement document at once",
    ),
    "wall_ledger_advisories": (
        ADVISORY_HEURISTIC,
        "check_wall_ledger_agreement",
        "infers disagreement between an append-log entry and a corrections "
        "section -- two prose surfaces, compared by meaning",
    ),
    "recipe_signature_honesty_advisories": (
        ADVISORY_HEURISTIC,
        "check_recipe_signature_honesty",
        "cross-checks a signature token against the recipe's PROSE BODY; "
        "whether the body 'mentions' a marker is not a binary question",
    ),
    "recipe_discovery_advisories": (
        ADVISORY_HEURISTIC,
        "check_recipe_discovery",
        "pattern-matches an adopter tree against a recipe signature and "
        "suggests a read; its own docstring says discovery, not enforcement",
    ),
    "ungroomed_ideas_advisories": (
        ADVISORY_HEURISTIC,
        "check_ungroomed_ideas",
        "counts idea lines newer than the last groom pass; a backlog count is "
        "a prompt to schedule work, not a defect in the tree",
    ),
    "baton_freshness_advisories": (
        ADVISORY_HEURISTIC,
        "check_baton_freshness",
        "infers that a baton names as still-to-build something that already "
        "resolves -- an inference about INTENT, unlike its S4 sibling above "
        "which only resolves a path",
    ),
}

# Anchor floors: 9 deterministic + 21 heuristic advisory sites today. Shrinkage
# guards in the style of EXPECTED_MIRRORS / EXPECTED_CENSUS_GATES above, so the
# census cannot be gutted to a vacuously-green empty set; bump deliberately
# when an advisory site is legitimately added or removed.
EXPECTED_ADVISORY_DETERMINISTIC = 9
EXPECTED_ADVISORY_HEURISTIC = 21


# ── Which deterministic sites are GATE-WIRED (exit-affecting) ────────────────
# Being DETERMINISTIC says a checker is SAFE to gate — binary, no judgement, no
# false-positive surface. It does not say the fleet is READY for it to gate. A
# checker whose finding is real everywhere still cannot be promoted until the
# trees it ships to are clean, or the promotion is just a fleet-wide red with a
# hand-edit at the end of it.
#
# So promotion is evidence-gated, and `check --gate-preview` is the instrument
# that produces the evidence. Measured 2026-08-06 across all 12 adopter trees
# in docs/adopters.md — 3 findings total:
#
#   * six sites fired NOWHERE (staged_regen, enforcement_strength, folded_gate,
#     fastlane_symmetry, recipe_applies_when, baton_resolves);
#
# ...and then the TEST SUITE corrected the sweep, which is worth recording
# because it is a flaw in the method and not in the data. `staged_regen` fires
# on ZERO of the 12 trees and still cannot be promoted: it fires THREE times on
# the COLD-ADOPTION ARC itself (`tests/test_check_engagement.py` — a fresh
# `adopt` + `render --live` leaves .substrate/agents/*.md and
# .substrate/claude/CLAUDE.md carrying filled-but-unrendered slots). Promoting
# it would make every NEW adoption born-red on a defect the adopt flow creates.
# The sweep swept MATURE trees and had no way to see that. A clean sweep across
# adopters is necessary evidence for promotion, not sufficient — the arc a new
# adopter walks is part of the fleet too.
#   * template_sync fired once, on substrate-kit itself, self-inflicted by #577
#     and fixed in the same PR that promotes it;
#   * automerge_preflight fired on superbot and superbot-next — both REAL
#     latent defects (an enabler whose allowlist disagrees with the config it
#     regenerates from, so an upgrade silently stops arming prefixes sessions
#     push).
#
# automerge_preflight is therefore NOT promoted, and the REASON IS THE RULE
# rather than the finding: promotion waits on a CLEAN sweep, and two live
# findings is not a clean sweep. The defects are real and worth fixing in those
# two repos — at which point the next sweep returns clean and the promotion is
# free. Promoting it now would also spend a compat guarantee the kit states out
# loud (EAP §6.4: no adopter's existing tree goes born-red on upgrade), which is
# not a thing to trade for two findings already recorded in a PR body.
#
# `boot_path` is absent for the same reason at larger scale: 11 of 11 would red,
# and the fix
# is a hand-edit per repo (planted docs are skip-if-exists, so `upgrade` will
# not add the section to an existing agreement). It ships DETERMINISTIC — in the
# agent's channel, visible, never hidden in the routed tail — and gets promoted
# when a later sweep says the fleet has converged. Add it here then; do not add
# it on the argument that it is "obviously right", which is what promotion
# without a sweep always feels like.
ADVISORY_GATE_READY: frozenset[str] = frozenset({
    "template_sync_advisories",
    "strength_advisories",
    "folded_gate_advisories",
    "fastlane_symmetry_advisories",
    "recipe_applies_when_advisories",
    "baton_resolves_advisories",
})

# Anchor floor: 6 of the 9 deterministic sites gate today. Bump deliberately,
# and only behind a clean --gate-preview sweep across docs/adopters.md.
EXPECTED_ADVISORY_GATE_READY = 6


def gate_ready_advisories() -> frozenset[str]:
    """Deterministic sites whose findings COUNT TOWARD THE EXIT CODE."""
    return ADVISORY_GATE_READY


def gate_pending_advisories() -> list[str]:
    """Deterministic sites that are visible but not yet exit-affecting.

    The waiting room: safe to gate by construction, held back until a
    ``--gate-preview`` sweep shows the fleet would survive the promotion.
    """
    return [s for s in deterministic_advisories() if s not in ADVISORY_GATE_READY]


def advisory_census() -> dict[str, tuple[str, str, str]]:
    """The full advisory census: emit-site name -> ``(kind, checker, why)``.

    Returns a copy so a consumer cannot mutate the canonical registry.
    """
    return dict(ADVISORY_CENSUS)


def advisory_kind(name: str) -> str:
    """The classification of one advisory emit site.

    Unknown names classify as :data:`ADVISORY_DETERMINISTIC` — the fail-LOUD
    default. An unclassified block keeps printing in the agent's channel, so
    the failure mode of forgetting a census entry is noise (which the meta-test
    catches) and never silence (which nothing would catch).
    """
    entry = ADVISORY_CENSUS.get(name)
    return entry[0] if entry else ADVISORY_DETERMINISTIC


def deterministic_advisories() -> list[str]:
    """Emit sites that stay in the agent's feedback channel."""
    return [k for k, v in ADVISORY_CENSUS.items() if v[0] == ADVISORY_DETERMINISTIC]


def heuristic_advisories() -> list[str]:
    """Emit sites routed to the advisory report, off the agent's channel."""
    return [k for k, v in ADVISORY_CENSUS.items() if v[0] == ADVISORY_HEURISTIC]


def advisory_checkers() -> list[str]:
    """The producing checker of every census entry, in registry order."""
    return [checker for _kind, checker, _why in ADVISORY_CENSUS.values()]


def advisory_reasons() -> list[str]:
    """The classification reason of every census entry."""
    return [why for _kind, _checker, why in ADVISORY_CENSUS.values()]


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
