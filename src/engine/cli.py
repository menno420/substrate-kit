"""The substrate-kit bootstrap command line.

Surface: ``init`` (idempotent), ``status``, ``mode <name>``, ``stance [name]``
(show or set the task stance), ``ask`` (list the pending interview questions),
``answer`` / ``confirm`` (fill / confirm a slot), ``render`` (write content
docs), ``skills`` / ``agents`` / ``hooks`` (list / ``--build`` the packs),
``hook <event>`` (the runtime hook entry points), ``check`` (every hygiene
checker), ``triggers``, ``reflect``, ``episodes``, ``metrics``, ``maintain``,
``review`` (the independent-review seam), ``economy`` (the context-economy
engine), ``ledger`` (the [D-NNNN] decisions ledger), ``friction`` (export/list/show
the §9.1 friction-report outbox), ``draft`` (auto-draft the session card's
close-out from evidence — KL-5), and ``--simulate N
[--mode m]`` (the CI / proving smoke that drives the staged interview and
asserts per-mode behavior). Output goes through ``_emit`` (``sys.stdout.write``)
rather than ``print`` to keep the engine lint-clean.
"""

from __future__ import annotations

import argparse
import difflib
import json
import os
import shlex

# THE §3.2 carve-out (ORDER 018 / idea-engine ASK 002): subprocess is banned
# in engine code — checkers never shell out; CI does the git work in bash.
# The ONE exception is `check`'s LOCAL-RITUAL parity legs below
# (_derive_inbox_base + _derive_diff_session_cards + _run_preflight_scripts):
# local `check --strict` must run the SAME legs as the CI substrate-gate, and
# locally there is no bash wrapper to extract the merge-base blob, derive the
# PR-diff card set, or launch the repo's preflight scripts. All helpers
# self-skip (fail open, NOTE line) on any failure and are never on the CI
# gate path, which still hands in --inbox-base / --session-log explicitly.
import subprocess  # noqa: TID251
import sys
import tempfile
from datetime import date
from pathlib import Path
from typing import Any

from engine.adopt import (
    adopt,
    gate_test_command_advisory,
    record_doc_hash,
    strip_unrendered_banner,
)
from engine.agents.agents import AGENTS, agent_document, agent_relpath
from engine.checks.allowlist import apply_allowlist, load_allowlist
from engine.checks.check_adopters_current import check_adopters_current
from engine.checks.check_capability_xref import check_capability_xref
from engine.checks.check_claims import check_claims, claim_scan_dirs
from engine.checks.check_docs import Finding, run_doc_checks
from engine.checks.check_folded_gate import check_folded_gate
from engine.checks.check_stale_walls import check_stale_walls
from engine.checks.check_engagement import (
    check_engagement,
    check_engagement_control,
    check_enforcement_strength,
    native_gate_note,
    required_unverified_note,
    scan_relpaths,
)
from engine.checks.check_inbox_append import INBOX_RELPATH, check_inbox_append
from engine.checks.check_model_line import check_model_line
from engine.checks.check_namespace import check_namespace
from engine.checks.check_no_false_walls import check_no_false_walls
from engine.checks.check_owner_actions import check_owner_actions
from engine.checks.check_status_current import (
    CONTROL_README_RELPATH,
    check_status_current,
    heartbeat_relpaths,
)
from engine.checks.check_orientation_budget import (
    check_orientation_budget,
    check_orientation_headroom,
)
from engine.checks.check_seam_authority import check_seam_authority
from engine.checks.check_session_log import (
    BORN_RED_HOLD_MESSAGE,
    check_added_card,
    check_log,
    is_unadopted_draft,
    latest_session_log,
    status_in_progress,
)
from engine.checks.check_automerge_preflight import check_automerge_preflight
from engine.claim import (
    ClaimError,
    branch_for,
    claim_filename,
    claim_order_ids,
    normalize_order,
    owner_token,
    render_claim,
)
from engine.checks.check_seat_digest import check_seat_digest
from engine.checks.check_setup_script import check_setup_script
from engine.checks.check_skill_grounds import check_skill_grounds
from engine.checks.check_archive_ready import check_archive_ready
from engine.checks.check_card_residue import check_card_residue
from engine.checks.check_staged_regen import check_staged_regen
from engine.checks.check_template_sync import check_template_sync
from engine.contextpack import generate_packs, load_pack_index
from engine.currency import (
    ADOPTERS_RELPATH,
    REGEN_COMMAND,
    ROSTER_RELPATH,
    default_fetcher,
    drift_report_lines,
    parse_roster,
    registry_delta,
    render_adopters,
    scan_fleet,
)
from engine.economy.engine import economy_actuate, economy_check, issue_body
from engine.economy.harvest import harvest_sources, parse_harvest_tables
from engine.economy.simulator import calibration_recipe, default_calibration, run_search
from engine.grammar import CAPABILITY_VENUE_TOKENS, SEAT_DIGEST_DEFAULT_VENUES
from engine.heartbeat import (
    HeartbeatError,
    full_status,
    restamp_status,
)
from engine.hooks.post_edit import evaluate_edit
from engine.hooks.session_start import compose_orientation
from engine.hooks.settings import full_settings_template, hooks_fill_table
from engine.hooks.stance_guard import evaluate_tool, settings_snippet, tool_from_payload
from engine.hooks.stop_check import evaluate_stop
from engine.interview.interview import (
    confirm_slot,
    critical_slots,
    pending_questions,
    record_answer,
    run_session,
    session_questions,
)
from engine.interview.question_bank import QUESTIONS
from engine.ledger import (
    LEDGER_FILENAME,
    append_decision,
    check_ledger,
    check_stamp_discipline,
)
from engine.lib.atomicio import atomic_write_text
from engine.lib.config import (
    KIT_VERSION,
    Config,
    config_path,
    load_config,
    save_config,
)
from engine.lib.guardrail import UnsafeTargetError, assert_safe_target
from engine.lib.modes import actuators_may_apply, triggers_mandate
from engine.lib.state import JsonStateBackend, default_state
from engine.loop.archive import ensure_archive_draft
from engine.loop.episodes import (
    EPISODIC_INDEX_FILENAME,
    rebuild_episodic_index,
    search_episodes,
)
from engine.loop.friction import (
    FRICTION_LABEL,
    build_envelope,
    detect_repo,
    friction_issue_body,
    friction_issue_title,
    friction_reports,
    list_outbox,
    load_envelope,
    write_outbox,
)
from engine.loop.handoff import (
    ensure_draft,
    record_session_anchor,
)
from engine.loop.handoff_pointer import write_handoff_pointer
from engine.loop.kpis import kpi_footer, workflow_kpis
from engine.loop.maintenance import compaction_due, maintenance_report, run_compaction
from engine.loop.reflections import (
    REFLECTIONS_FILENAME,
    add_reflection,
    lessons_block,
    load_reflections,
    mine_reflections,
)
from engine.loop.review_seam import (
    apply_review_verdict,
    build_review_payload,
    clear_review_payload,
    seam_wiring_doc,
    write_review_payload,
)
from engine.loop.telemetry import (
    GUARD_FIRES_FILENAME,
    harvest_model_usage,
    reconcile_model_usage,
    record_guard_fires,
)
from engine.loop.triggers import check_triggers, mandatory_questions, trigger_block
from engine.render import (
    agreement_home,
    build_context,
    find_placeholders,
    load_templates,
    render,
)
from engine.seatdigest import (
    seat_digest_relpath,
    seat_digest_text,
    walls_digest_venues,
)
from engine.skills.skills import (
    SKILLS,
    skill_capabilities,
    skill_document,
    skill_relpath,
)
from engine.stances.stances import DEFAULT_STANCE, stance_briefing, stance_names
from engine.upgrade import UpgradeRefused, run_rollback, run_upgrade


def _emit(line: str = "") -> None:
    """Write a line to stdout (avoids the print() lint ban in engine code)."""
    sys.stdout.write(line + "\n")


def _kit_root() -> Path:
    """Return the tree the guardrail protects (the kit's own checkout).

    Only the source layout (``.../src/engine/cli.py``) has a kit tree to
    protect: there, the checkout root is ``parents[2]``. Running as the
    copied single-file bootstrap or a pip install, this returns the module
    file itself — a *file* matches no target directory, so the guardrail
    never engages (there is no kit tree). The old unconditional
    ``parents[2]`` made the dist's guardrail root the grandparent of the
    user's repo, refusing EVERY real ``adopt``/``init`` outside the temp
    tree — the documented primary flow.
    """
    here = Path(__file__).resolve()
    if here.parent.name == "engine" and here.parent.parent.name == "src":
        return here.parents[2]
    return here


def _state_path(root: Path, config: Config) -> Path:
    """Return the state-file path under a project ``root``."""
    return root / config.state_dir / "state.json"


def cmd_init(target: Path) -> int:
    """Create config + state under ``target`` if absent; never clobber."""
    assert_safe_target(target, _kit_root())
    target.mkdir(parents=True, exist_ok=True)
    if config_path(target).exists():
        config = load_config(target)
    else:
        config = Config()
        save_config(target, config)
    state_path = _state_path(target, config)
    if state_path.exists():
        _emit(f"init: already initialised at {target} (idempotent no-op).")
        return 0
    backend = JsonStateBackend(state_path)
    with backend.transaction():
        for key, value in default_state(config.project_id).items():
            backend.set(key, value)
    _emit(f"init: created {state_path} (project_id={config.project_id}).")
    return 0


def cmd_status(target: Path) -> int:
    """Print a one-screen summary of the install's state."""
    config = load_config(target)
    backend = JsonStateBackend(_state_path(target, config))
    data = backend.data
    if not data:
        _emit(f"status: no state at {target} (run init first).")
        return 1
    _emit(f"project_id : {data.get('project_id')}")
    _emit(f"stage      : {data.get('stage')}")
    _emit(f"mode       : {data.get('mode')}")
    _emit(f"stance     : {data.get('stance')}")
    _emit(f"sessions   : {data.get('session_count')}")
    return 0


def cmd_mode(target: Path, name: str) -> int:
    """Set the integration mode (observe | guided | active)."""
    valid = ("observe", "guided", "active")
    if name not in valid:
        _emit(f"mode: invalid mode {name!r} (choose from {list(valid)}).")
        return 2
    config = load_config(target)
    backend = JsonStateBackend(_state_path(target, config))
    if not backend.data:
        _emit(f"mode: no state at {target} (run init first).")
        return 1
    history = list(backend.get("mode_history", []))
    history.append(
        {
            "mode": name,
            "session": int(backend.get("session_count", 0)),
            "date": date.today().isoformat(),
        },
    )
    with backend.transaction():
        backend.set("mode", name)
        backend.set("mode_history", history)
    _emit(f"mode: set to {name} (audit trail: {len(history)} switch(es)).")
    return 0


def cmd_stance(target: Path, name: str | None) -> int:
    """Show or set the active task stance (question|analysis|debug|review|plan).

    With no ``name``, prints the active stance's briefing (reading-route +
    tool-scope + output contract) and the available set. With a ``name``, switches
    the active stance in state. The stance is advisory — it scopes orientation, it
    does not block actions.
    """
    config = load_config(target)
    backend = JsonStateBackend(_state_path(target, config))
    if not backend.data:
        _emit(f"stance: no state at {target} (run init first).")
        return 1
    if name is None:
        active = backend.data.get("stance", DEFAULT_STANCE)
        _emit(stance_briefing(active))
        _emit(f"  available: {', '.join(stance_names())}")
        return 0
    if name not in stance_names():
        _emit(f"stance: invalid stance {name!r} (choose from {stance_names()}).")
        return 2
    backend.set("stance", name)
    _emit(f"stance: set to {name}.")
    _emit(stance_briefing(name))
    return 0


def cmd_ask(target: Path) -> int:
    """List the interview's currently pending questions."""
    config = load_config(target)
    backend = JsonStateBackend(_state_path(target, config))
    if not backend.data:
        _emit(f"ask: no state at {target} (run init first).")
        return 1
    pending = pending_questions(backend.data)
    if not pending:
        _emit("ask: no pending questions — all slots filled.")
        return 0
    asked = session_questions(backend.data)
    _emit(f"ask: {len(asked)} question(s) this session (mode quota):")
    for question in asked:
        _emit(
            f"  [{question['id']}] "
            f"({question['audience']}/{question['priority']}) {question['prompt']}",
        )
    remaining = len(pending) - len(asked)
    if remaining > 0:
        _emit(f"  (+{remaining} more later — the mode paces the interview)")
    return 0


def _render_live(target: Path, context: dict[str, str], backend: Any) -> int:
    """Fill remaining ``${slot}`` placeholders in the PLANTED docs, in place.

    Placeholders survive verbatim in a planted file until their slot fills, so
    substituting over the live text updates exactly the newly-answered slots
    while preserving every hand edit around them. Returns the leftover count.
    Every rewrite re-records the doc's sha256 (the §4.3 "kit last wrote this"
    provenance the upgrade diff keys on).

    The render set is :func:`engine.checks.check_engagement.scan_relpaths` —
    the SAME list the engagement gate scans — so the two surfaces can never
    disagree about whose job a planted file is. They used to: ``render
    --live`` iterated only the ``ADOPT_PLAN`` docs while the gate also
    counted ``.claude/CLAUDE.md``, so an ``--include-claude`` adopter's
    checklist could not reach GREEN by its own named commands (run-2 finding,
    idea render-live-claude-md-gap-2026-07-09).
    """
    leftover_total = 0
    for rel in scan_relpaths(load_config(target)):
        path = target / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        filled = render(text, context)
        leftover = find_placeholders(filled)
        leftover_total += len(leftover)
        if not leftover:
            # Fully rendered — the adopt-time UNRENDERED banner has done its job.
            filled = strip_unrendered_banner(filled)
        if filled != text:
            atomic_write_text(path, filled)
            record_doc_hash(backend, rel, filled)
            suffix = f" ({len(leftover)} slot(s) still unfilled)" if leftover else ""
            _emit(f"render: filled {rel}{suffix}")
    _emit(f"render: {leftover_total} unfilled placeholder(s) across planted docs.")
    return 0


def cmd_render(target: Path, live: bool = False) -> int:
    """Render the content docs from the current filled slots.

    Default: stage fresh renders of every template into
    ``<state_dir>/rendered/``. With ``live``: fill remaining placeholders in
    the *planted* docs in place (hand edits preserved) — the post-interview
    "make the live docs catch up" pass.
    """
    assert_safe_target(target, _kit_root())
    config = load_config(target)
    backend = JsonStateBackend(_state_path(target, config))
    if not backend.data:
        _emit(f"render: no state at {target} (run init first).")
        return 1
    context = build_context(backend.data)
    # Engine-computed boot pointer (ORDER 015): same rule as adopt, so a
    # staged/live render never strands ${agreement_home} as an unfilled slot.
    context.setdefault("agreement_home", agreement_home(target))
    if live:
        return _render_live(target, context, backend)
    out_dir = target / config.state_dir / "rendered"
    leftover_total = 0
    for name, text in load_templates().items():
        rendered = render(text, context)
        leftover = find_placeholders(rendered)
        leftover_total += len(leftover)
        out_name = name[:-5] if name.endswith(".tmpl") else name
        atomic_write_text(out_dir / out_name, rendered)
        suffix = f" ({len(leftover)} slot(s) unfilled)" if leftover else ""
        _emit(f"render: wrote {out_name}{suffix}")
    _emit(f"render: {leftover_total} unfilled placeholder(s) total.")
    return 0


def cmd_skills(target: Path, build: bool) -> int:
    """List the skill pack, or ``--build`` it into ``<state_dir>/skills/``.

    Listing shows each skill + its declared capabilities (what it may do beyond
    read, overriding the ambient stance). Building emits a native ``SKILL.md`` per
    skill into the staging area, body slot-filled from the interview — the host
    then installs them under ``.claude/skills/``. Like ``render``, the kit stages;
    it never writes a live ``.claude/`` tree.
    """
    config = load_config(target)
    if build:
        assert_safe_target(target, _kit_root())
    if not build:
        _emit("skills:")
        for skill in SKILLS:
            caps = ", ".join(skill_capabilities(skill["name"]))
            _emit(f"  {skill['name']} — {skill['description']}")
            _emit(f"    capabilities: {caps}")
        return 0
    backend = JsonStateBackend(_state_path(target, config))
    context = build_context(backend.data) if backend.data else {}
    out_base = target / config.state_dir
    leftover_total = 0
    for skill in SKILLS:
        body = render(skill["body"], context)
        leftover = find_placeholders(body)
        leftover_total += len(leftover)
        atomic_write_text(out_base / skill_relpath(skill), skill_document(skill, body))
        suffix = f" ({len(leftover)} slot(s) unfilled)" if leftover else ""
        _emit(f"skills: wrote {skill_relpath(skill)}{suffix}")
    _emit(f"skills: {len(SKILLS)} skill(s), {leftover_total} unfilled placeholder(s).")
    return 0


def cmd_agents(target: Path, build: bool) -> int:
    """List the persona pack, or ``--build`` it into ``<state_dir>/agents/``.

    Listing shows each persona + its description. Building emits a native
    ``.claude/agents``-style ``<name>.md`` per persona into the staging area, body
    slot-filled from the project's contract slots — the host then installs them
    under ``.claude/agents/``. Like ``render``/``skills``, the kit stages; it never
    writes a live ``.claude/`` tree.
    """
    config = load_config(target)
    if build:
        assert_safe_target(target, _kit_root())
    if not build:
        _emit("agents:")
        for agent in AGENTS:
            _emit(f"  {agent['name']} — {agent['description']}")
        return 0
    backend = JsonStateBackend(_state_path(target, config))
    context = build_context(backend.data) if backend.data else {}
    out_base = target / config.state_dir
    leftover_total = 0
    for agent in AGENTS:
        body = render(agent["body"], context)
        leftover = find_placeholders(body)
        leftover_total += len(leftover)
        atomic_write_text(out_base / agent_relpath(agent), agent_document(agent, body))
        suffix = f" ({len(leftover)} slot(s) unfilled)" if leftover else ""
        _emit(f"agents: wrote {agent_relpath(agent)}{suffix}")
    count = len(AGENTS)
    _emit(f"agents: {count} persona(s), {leftover_total} unfilled placeholder(s).")
    return 0


def _hook_command(config: Config) -> str:
    """Return the shell command Claude Code runs for the PreToolUse guard."""
    return f"{config.interpreter} bootstrap.py hook pretooluse"


def cmd_hooks(target: Path, build: bool) -> int:
    """Show the hook wiring, or ``--build`` the settings files into staging.

    Four hooks: the **PreToolUse stance guard**, **SessionStart orientation**,
    the **PostToolUse edit advisor**, and the **Stop-check advisor**. Building
    stages the PreToolUse snippet, the full four-event
    ``settings.template.json``, and the fill-table README into
    ``<state_dir>/hooks/`` — the host merges them into their own settings
    (adjusting the bootstrap path). Like the other emitters, the kit stages;
    it never writes a live ``.claude/`` tree.
    """
    config = load_config(target)
    if build:
        assert_safe_target(target, _kit_root())
    command = _hook_command(config)
    if not build:
        _emit("hooks:")
        _emit("  pretooluse   — stance guard: warns on an out-of-stance tool.")
        _emit("  sessionstart — prints the mode-aware orientation injection.")
        _emit("  postedit     — warns on generated-artifact / unbadged-doc edits.")
        _emit("  stopcheck    — session-close advisories (log, questions, cadence).")
        _emit(f"  wiring command: {command}")
        return 0
    out = target / config.state_dir / "hooks" / "settings.snippet.json"
    atomic_write_text(out, settings_snippet(command))
    tmpl = target / config.state_dir / "hooks" / "settings.template.json"
    atomic_write_text(tmpl, full_settings_template(config))
    atomic_write_text(
        target / config.state_dir / "hooks" / "README.md",
        hooks_fill_table(),
    )
    _emit(f"hooks: wrote {out.relative_to(target)}")
    _emit(f"hooks: wrote {tmpl.relative_to(target)} (all four events) + README.md")
    _emit("hooks: merge the hook blocks into .claude/settings.json yourself.")
    return 0


def _hook_pretooluse(target: Path) -> list[str]:
    """PreToolUse stance guard: warn on stderr for an out-of-stance tool."""
    tool_name = tool_from_payload(sys.stdin.read())
    if not tool_name:
        return []
    config = load_config(target)
    backend = JsonStateBackend(_state_path(target, config))
    stance = backend.data.get("stance") if backend.data else None
    if not stance:
        return []
    warning = evaluate_tool(stance, tool_name)
    if warning:
        sys.stderr.write(warning + "\n")
        return [warning]
    return []


def _hook_sessionstart(target: Path) -> list[str]:
    """SessionStart: print the orientation composition + record the anchor.

    The anchor (timestamp + git HEAD/branch, ``state["session_anchor"]``) is
    the evidence baseline the KL-5 auto-draft diffs against at session close.
    Recording is fail-open inside ``record_session_anchor`` — orientation
    must never be blocked by evidence bookkeeping. The boot also regenerates
    the repo-root ``HANDOFF.md`` pointer (the B1 run-6 delivery-gap fix: the
    orchestrator→worker seam does not forward this hook's stdout, so the same
    handoff content rides the working tree, where delegated workers look).
    """
    config = load_config(target)
    backend = JsonStateBackend(_state_path(target, config))
    text = compose_orientation(target, config, backend)
    if text:
        sys.stdout.write(text)
    record_session_anchor(target, config, backend)
    write_handoff_pointer(target, config)
    return []


def _hook_postedit(target: Path) -> list[str]:
    """PostToolUse: warn on stderr for a generated-artifact / unbadged-doc edit.

    Handles Edit/Write (``tool_input.file_path``) and NotebookEdit
    (``tool_input.notebook_path``) — the three tools the settings matcher wires.
    A NotebookEdit carries ``notebook_path``, not ``file_path``, so keying only
    on the latter matched notebook edits but never advised them (the matcher
    over-advertised its coverage).
    """
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        return []
    tool_input = payload.get("tool_input") if isinstance(payload, dict) else None
    if not isinstance(tool_input, dict):
        return []
    file_path = tool_input.get("file_path") or tool_input.get("notebook_path")
    if not isinstance(file_path, str) or not file_path:
        return []
    warning = evaluate_edit(target, load_config(target), file_path)
    if warning:
        sys.stderr.write(warning + "\n")
        return [warning]
    return []


def _hook_stopcheck(target: Path) -> list[str]:
    """Stop: auto-draft the session card, then print the advisories to stderr.

    Drafting runs FIRST (KL-5 — the mechanized write-back the Phase-2.5 A/B
    proved doesn't happen by discipline): a missing card gets a drafted
    skeleton, an in-progress card missing its close-out gets the drafted
    section appended, and the advisories that follow see the drafted state.
    Both halves fail open; the hook always exits 0.
    """
    config = load_config(target)
    backend = JsonStateBackend(_state_path(target, config))
    lines = ensure_draft(target, config, backend)
    lines += evaluate_stop(target, config, backend)
    for line in lines:
        sys.stderr.write(line + "\n")
    return lines


_HOOK_EVENTS = {
    "pretooluse": _hook_pretooluse,
    "sessionstart": _hook_sessionstart,
    "postedit": _hook_postedit,
    "stopcheck": _hook_stopcheck,
}

# Guard kind per hook event, for the §5.3 guard-fire feed. ``sessionstart``
# is orientation, not a guard — it never records a fire.
_HOOK_GUARD_KINDS = {
    "pretooluse": "stance",
    "postedit": "edit-advisor",
    "stopcheck": "stop-advisory",
}


def cmd_hook(target: Path, event: str) -> int:
    """Run a Claude Code hook entry point (all advisory — always exit 0).

    ``pretooluse`` warns on an out-of-stance tool; ``sessionstart`` prints the
    orientation injection to stdout; ``postedit`` reads the PostToolUse stdin
    payload (``tool_input.file_path``) and warns on stderr; ``stopcheck``
    prints session-close advisories to stderr. Every event fails open on a
    missing / malformed payload, config, or state.

    This dispatch is one of the two guard-fire choke points (KL-3, plan
    §5.3): each warning a guard hook surfaces is appended to
    ``<state_dir>/guard-fires.jsonl`` (surface ``hook``, posture ``advisory``
    — hooks never block). The write is fail-open and never alters the exit
    code: telemetry must never crash a hook.
    """
    handler = _HOOK_EVENTS.get(event)
    if handler is None:
        return 0
    try:
        warnings = handler(target)
        kind = _HOOK_GUARD_KINDS.get(event)
        if warnings and kind:
            record_guard_fires(
                target,
                load_config(target).state_dir,
                cmd=f"hook {event}",
                surface="hook",
                posture="advisory",
                findings=[Finding("", kind, warning) for warning in warnings],
            )
        return 0
    except Exception:  # noqa: BLE001 — hooks fail open by contract, always 0
        return 0


def _extra_check_findings(target: Path, config: Config) -> list:
    """Run the configured non-doc checkers (ledger, namespace, seams, budget).

    Each checker engages only when its inputs exist — an un-adopted project
    with no ledger, no namespace roots, no seams, and no boot docs runs none of
    them, so ``check`` stays meaningful before onboarding.
    """
    findings: list = []
    ledger_path = target / config.docs_root / LEDGER_FILENAME
    if ledger_path.exists():
        findings += check_ledger(ledger_path)
        findings += check_stamp_discipline(target / config.docs_root, ledger_path)
    roots = [target / r for r in config.namespace.get("roots", [])]
    roots = [r for r in roots if r.exists()]
    if roots:
        findings += check_namespace(
            roots,
            reserved=config.namespace.get("reserved") or None,
        )
    if config.seams:
        findings += check_seam_authority(target, config.seams)
    # No-false-walls leg (propagated from tools/check_no_false_walls.py so EVERY
    # adopter enforces it via its own `check --strict`, not just substrate-kit's
    # own CI): a forward-binding surface (live docs / CONSTITUTION / CAPABILITIES
    # / .claude) that documents a FALSE agent-capability limitation ("agents
    # cannot merge", "classifier-denied", "owner is the merge authority") reds
    # the gate. Additive — a new finding class only; dated/repudiated/historical
    # lines and CODE rules pass (see the checker's false-positive discipline).
    # Self-quiet on a bare tree (no docs / constitution / .claude to scan).
    findings += check_no_false_walls(target, config)
    boot_docs = config.orientation.get("boot_docs") or config.readpath_docs
    docs_root = target / config.docs_root
    if any((docs_root / doc).exists() or (target / doc).exists() for doc in boot_docs):
        findings += check_orientation_budget(target, config)
    # The post-adopt ENGAGEMENT gate (KL-7): red in an adopted host until the
    # planted docs are rendered, a CI workflow runs the check, and the session
    # loop has engaged. Self-gating on adoption evidence — a bare tree adds
    # nothing here.
    findings += check_engagement(target, config)
    return findings


# Recursion guard for the preflight-scripts leg (ORDER 018): a repo's
# preflight wrapper conventionally invokes `bootstrap.py check` itself
# (idea-engine's runs `check --strict --status-only`), so the leg marks its
# children with this env var and skips itself inside one — otherwise a
# wrapper entry that runs plain `check --strict` would recurse forever.
_PREFLIGHT_NESTED_ENV = "SUBSTRATE_KIT_PREFLIGHT"

# Git subprocess budget for the inbox merge-base derivation: local plumbing
# reads are milliseconds; a hung git (dead network FS) must not wedge check.
_GIT_TIMEOUT_SECONDS = 30


def _derive_inbox_base(target: Path) -> tuple[bytes | None, str | None]:
    """Derive the merge-base blob of ``control/inbox.md`` from ``origin/main``.

    The LOCAL-RITUAL half of the inbox append-only gate (ORDER 018 /
    idea-engine ASK 002): CI extracts the merge-base blob in bash and hands
    it in via ``--inbox-base``, but a plain local ``check --strict`` had no
    base to diff against, so the gate silently no-opped and the tree learned
    about an inbox violation only from red CI (idea-engine PR #274). This
    helper is the documented §3.2 subprocess carve-out (see the import-site
    note): it runs only when ``--inbox-base`` was NOT given, and mirrors the
    generated gate's bash exactly — ``git merge-base HEAD origin/main`` then
    ``git show <base>:control/inbox.md`` (absent-at-base → empty blob, the
    gate's ``|| : > basefile`` posture).

    Returns ``(blob_bytes, note)``. ``blob_bytes`` is None when there is
    nothing to judge or derivation failed; ``note`` carries the one-line
    self-skip reason worth surfacing (None for the silent skips: no inbox
    file, or not a git checkout at all — a bare tree must stay quiet).
    """
    if not (target / INBOX_RELPATH).is_file():
        return None, None  # no inbox — nothing to judge, silently
    if not (target / ".git").exists():  # dir, or file for worktrees
        return None, None  # not a git checkout — a bare tree stays quiet
    git = ["git", "-C", str(target)]
    try:
        merge_base = subprocess.run(  # noqa: TID251 — §3.2 carve-out (import-site note)
            [*git, "merge-base", "HEAD", "origin/main"],
            capture_output=True,
            timeout=_GIT_TIMEOUT_SECONDS,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return None, (
            f"inbox merge-base leg skipped — could not run git "
            f"({exc.__class__.__name__}); CI still gates with --inbox-base."
        )
    if merge_base.returncode != 0:
        return None, (
            "inbox merge-base leg skipped — origin/main not resolvable "
            "(no remote-tracking ref / unborn HEAD); CI still gates with "
            "--inbox-base."
        )
    base = merge_base.stdout.decode("utf-8", "replace").strip()
    try:
        show = subprocess.run(  # noqa: TID251 — §3.2 carve-out (import-site note)
            [*git, "show", f"{base}:{INBOX_RELPATH}"],
            capture_output=True,
            timeout=_GIT_TIMEOUT_SECONDS,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return None, (
            f"inbox merge-base leg skipped — could not run git "
            f"({exc.__class__.__name__}); CI still gates with --inbox-base."
        )
    # Path absent at the base (a fresh inbox) → empty base blob, exactly the
    # generated gate's `git show ... || : > "$basefile"` behavior.
    return (show.stdout if show.returncode == 0 else b""), None


_MTIME_FALLBACK_NOTE = "falling back to newest-by-mtime; CI still gates diff-derived."


def _derive_diff_session_cards(
    target: Path,
    sessions_dir: str,
) -> tuple[list[Path] | None, str | None]:
    """Derive the session cards this branch touches from the merge-base diff.

    The session-gate half of the ORDER 018 local↔CI parity posture
    (idea-engine ASK 003): ``cmd_check``'s fallback lane used to pick the
    card to gate on by newest mtime, and after merging ``origin/main`` into
    a working branch a sibling's COMPLETED card carries the freshest mtime —
    so a plain local ``check --strict`` validated the WRONG card and went
    green while the session's own card was still in-progress (reproduced
    live, sim-lab V051). The CI substrate-gate never had this hole because
    it derives the card set from the PR diff in bash; this helper — a
    documented §3.2 subprocess carve-out like :func:`_derive_inbox_base`,
    same mechanism, same self-skip posture — brings the local ritual onto
    the same selection: ``git merge-base HEAD origin/main``, then the
    base-vs-worktree diff under ``sessions_dir`` (``--diff-filter=d``,
    deletions excluded, exactly the CI pathspec) plus untracked cards
    (``git ls-files --others``) so a mid-session run still sees its own
    card before the first commit.

    Returns ``(cards, note)``:

    - ``(None, note-or-None)`` — no git context to derive from (bare tree,
      no ``origin/main``, git unavailable, or HEAD *is* origin/main with no
      card changes — a clean post-merge checkout, not a PR context): the
      caller keeps the historical newest-by-mtime fallback, so non-git
      adopters are unchanged.
    - ``(cards, None)`` — derivation succeeded; the list may be EMPTY
      (branch ahead of origin/main but no card in the diff), which the
      caller treats as an absent card rather than silently mtime-greening —
      the fail-closed-on-ambiguity direction.
    """
    if not (target / ".git").exists():  # dir, or file for worktrees
        return None, None  # not a git checkout — a bare tree stays quiet
    git = ["git", "-C", str(target)]
    pathspecs = [f"{sessions_dir}/*.md", f":!{sessions_dir}/README.md"]
    try:
        merge_base = subprocess.run(  # noqa: TID251 — §3.2 carve-out (import-site note)
            [*git, "merge-base", "HEAD", "origin/main"],
            capture_output=True,
            timeout=_GIT_TIMEOUT_SECONDS,
        )
        head = subprocess.run(  # noqa: TID251 — §3.2 carve-out (import-site note)
            [*git, "rev-parse", "HEAD"],
            capture_output=True,
            timeout=_GIT_TIMEOUT_SECONDS,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return None, (
            f"session-card diff selection skipped — could not run git "
            f"({exc.__class__.__name__}); {_MTIME_FALLBACK_NOTE}"
        )
    if merge_base.returncode != 0 or head.returncode != 0:
        return None, (
            "session-card diff selection skipped — origin/main not "
            f"resolvable (no remote-tracking ref / unborn HEAD); "
            f"{_MTIME_FALLBACK_NOTE}"
        )
    base = merge_base.stdout.decode("utf-8", "replace").strip()
    try:
        diff = subprocess.run(  # noqa: TID251 — §3.2 carve-out (import-site note)
            [*git, "diff", "--name-only", "--diff-filter=d", base, "--", *pathspecs],
            capture_output=True,
            timeout=_GIT_TIMEOUT_SECONDS,
        )
        untracked = subprocess.run(  # noqa: TID251 — §3.2 carve-out (import-site note)
            [*git, "ls-files", "--others", "--exclude-standard", "--", *pathspecs],
            capture_output=True,
            timeout=_GIT_TIMEOUT_SECONDS,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return None, (
            f"session-card diff selection skipped — could not run git "
            f"({exc.__class__.__name__}); {_MTIME_FALLBACK_NOTE}"
        )
    if diff.returncode != 0 or untracked.returncode != 0:
        return None, (
            f"session-card diff selection skipped — git diff failed; "
            f"{_MTIME_FALLBACK_NOTE}"
        )
    names: set[str] = set()
    for stream in (diff.stdout, untracked.stdout):
        for line in stream.decode("utf-8", "replace").splitlines():
            name = line.strip()
            if not name or not name.endswith(".md"):
                continue
            if Path(name).name == "README.md":
                continue
            if (target / name).is_file():
                names.add(name)
    cards = sorted(target / name for name in names)
    if not cards and base == head.stdout.decode("utf-8", "replace").strip():
        # Sitting exactly on origin/main with no card changes: there is no
        # PR context to be ambiguous about — keep the historical fallback
        # (every merged card is complete on a healthy main) with a NOTE.
        return None, (
            "session-card diff selection — HEAD is origin/main and no card "
            "differs (not a PR context); using newest-by-mtime."
        )
    return cards, None


def _select_gate_card(
    cards: list[Path],
    markers: list[dict[str, str]],
) -> Path:
    """Pick the card to gate on from the diff-derived set — fail-closed.

    Every card in the set is graded and a red card outranks a green one, so
    downstream's single-log machinery reds iff ANY card in the diff is red —
    the same every-card-never-one-picked posture as the CI gate (the
    venture-lab #33 tail-1 shadowing lesson). Among red cards a
    session-owned one outranks an unadopted engine draft (the B1 run-8
    advisory lane must never mask a genuinely red sibling), and an
    in-progress card outranks other reds (the born-red hold is the gate's
    subject); name order breaks the remaining ties deterministically.
    """

    def _rank(card: Path) -> tuple[bool, bool, bool, str]:
        try:
            text = card.read_text(encoding="utf-8")
        except OSError:
            text = ""
        return (
            not check_log(card, markers),  # red cards first
            is_unadopted_draft(text),  # session-owned reds before drafts
            not status_in_progress(text),  # in-progress holds first
            str(card),
        )

    return min(cards, key=_rank)


def _run_preflight_scripts(
    target: Path,
    config: Config,
) -> tuple[list, list[str]]:
    """Run the config-declared repo-local preflight scripts; return findings.

    The other LOCAL-RITUAL parity leg (ORDER 018 / idea-engine ASK 002):
    ``substrate.config.json::preflight_scripts`` is the ONE check list —
    ``check``'s full lane runs it here, and the CI substrate-gate's full lane
    runs it too *through this very code* (its gate step invokes
    ``bootstrap.py check --strict``), so a checker added to the repo's
    preflight wrapper red-flags in both venues (idea-engine PR #299's
    local-green→CI-red class). Returns ``(findings, notes)``: a non-zero
    exit is an exit-affecting ``preflight-script`` finding riding the strict
    loop; an absent script is a NOTE (self-skip — the default entry names a
    conventional path many adopters won't have); a nested run (see
    ``_PREFLIGHT_NESTED_ENV``) skips the whole leg.
    """
    scripts = [s for s in (config.preflight_scripts or []) if str(s).strip()]
    if not scripts:
        return [], []
    if os.environ.get(_PREFLIGHT_NESTED_ENV):
        return [], [
            "preflight scripts skipped — nested check run "
            f"({_PREFLIGHT_NESTED_ENV} set; the outer run owns the leg).",
        ]
    findings: list = []
    notes: list[str] = []
    child_env = dict(os.environ)
    child_env[_PREFLIGHT_NESTED_ENV] = "1"
    for entry in scripts:
        tokens = shlex.split(str(entry))
        if not tokens:
            continue
        script_rel = tokens[0]
        script = target / script_rel
        if not script.is_file():
            notes.append(
                f"preflight script {script_rel} not found — skipped "
                "(config preflight_scripts; plant one to converge the local "
                "ritual and the CI gate on one check list).",
            )
            continue
        if script_rel.endswith(".py"):
            # The interpreter already running check exists in BOTH venues by
            # construction (the recorded config interpreter may not exist in
            # CI) — the same choice the conventional wrapper itself makes.
            argv = [sys.executable or "python3", str(script), *tokens[1:]]
        else:
            argv = [str(script), *tokens[1:]]
        try:
            proc = subprocess.run(  # noqa: TID251 — §3.2 carve-out (import-site note)
                argv,
                cwd=target,
                env=child_env,
                capture_output=True,
                timeout=900,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            findings.append(
                Finding(
                    script_rel,
                    "preflight-script",
                    f"could not run ({exc.__class__.__name__}) — the CI gate "
                    "runs this same preflight, so a local crash is a red.",
                ),
            )
            continue
        if proc.returncode != 0:
            tail = ""
            for stream in (proc.stderr, proc.stdout):
                text = stream.decode("utf-8", "replace")
                lines = [ln for ln in text.splitlines() if ln.strip()]
                if lines:
                    tail = lines[-1][:200]
                    break
            findings.append(
                Finding(
                    script_rel,
                    "preflight-script",
                    f"exit {proc.returncode}"
                    + (f": {tail}" if tail else "")
                    + " — the CI substrate-gate runs this same preflight; "
                    "fix it before pushing.",
                ),
            )
    return findings, notes


def cmd_check(
    target: Path,
    strict: bool,
    *,
    require_session_log: bool = False,
    session_log: Path | None = None,
    added_card: Path | None = None,
    simulate_added_card: Path | None = None,
    status_only: bool = False,
    inbox_base: Path | None = None,
) -> int:
    """Run every hygiene checker against ``target``.

    ``added_card`` (CLI ``--added-card``) names a session card the PR's diff
    ADDS — the generated gate's added-card lane passes it so a born-red
    heartbeat is graded by what it *declares* (see
    :func:`engine.checks.check_session_log.check_added_card` for the
    declared-status tiering): an in-progress/drafted card yields the
    born-red HOLD (the superbot-games #40 card-only loophole fix — an
    added mid-flight card holds the merge red until it flips complete,
    never advisory-green); grammar misses red as before (the venture-lab
    #15 false-green class). Findings ride the strict loop like any doc
    finding and are never allowlistable (they are the session-gate seam);
    a named file that does not exist is advisory-only — the gate derives
    the path from the diff, so absence means nothing to judge.

    ``simulate_added_card`` (CLI ``--simulate-added-card``) is the lane's
    ADVISORY self-test: it prints exactly what the added-card lane WOULD
    conclude for the named card (hold / findings / pass) without ever
    touching the exit code. It exists because the lane is unobservable on
    the very PR that ships gate changes — a PR touching the gate workflow
    takes the full locked door, superseding ``--added-card`` — so gate
    work needs an in-run way to verify the lane's grading.

    ``inbox_base`` (CLI ``--inbox-base``) names the merge-base version of
    ``control/inbox.md`` — extracted by CI in bash, because engine *checker*
    code never shells out to git (§3.2). When given, the append-only gate
    runs on both lanes: the change to ``control/inbox.md`` must be
    pure-append vs that base and its appended text must be well-formed ORDER
    blocks (issue #36 report 2). It rides the fast lane exactly like the
    status gate — an inbox append is control-lane traffic — and self-skips
    when there is nothing to judge. When ``inbox_base`` is ABSENT (the local
    ritual), the gate no longer no-ops: :func:`_derive_inbox_base` — the
    documented §3.2 carve-out — derives the base blob from ``origin/main``
    so plain local ``check --strict`` reds where CI would red (ORDER 018),
    and self-skips with a NOTE when no git context is derivable.

    ``status_only`` (CLI ``--status-only``) scopes the run to the control/
    status heartbeat checker alone — the CI control fast lane's gate. A
    control-only diff edits exactly the files ``check_status_current``
    validates, so the lane must not skip that one checker (a
    heartbeat-deleting control PR would merge green and pre-redden the NEXT
    unrelated full-suite PR — the fleet-review 2026-07-09 finding), but it
    must not pay the heavy suite either. Stdlib-only and session-log-free by
    construction: heartbeat PRs carry no session card. The allowlist and
    guard-fire telemetry apply exactly as in a full run, so a suppressed
    status finding behaves identically on both lanes.

    Docs (badge/link/reachable), the decisions ledger + stamp discipline, the
    namespace/shadowing guard, the seam-authority fences, and the orientation
    word budget — each engaging only when its inputs exist. Findings always
    count toward the exit code (under ``--strict``); an *incomplete* existing
    session log counts — EXCEPT an **unadopted auto-draft** in the
    mtime-fallback lane (no explicit ``--session-log``, no
    ``require_session_log``): a card the engine itself drafted and no session
    adopted reports as an advisory instead of a failure, so a departed
    session's untouched skeleton cannot leave the repo red for the next cold
    session (B1 run-8; see ``check_session_log.is_unadopted_draft``). Gate
    mode is unaffected. A *missing* session log is **advisory by default** (a
    host may run ``check`` mid-session) but becomes a **hard failure** under
    ``require_session_log`` — the gate mode the live CI workflow runs, so a
    session that never writes its journal cannot merge (the "locked door" that
    makes the memory ritual non-optional, not merely advised). Uses config
    defaults if ``target`` has no ``substrate.config.json`` yet, so a project
    can lint before onboarding.

    ``session_log`` (CLI ``--session-log``) names the card to gate on
    *explicitly* — the diff-aware selection a CI workflow derives from which
    ``<sessions_dir>/*.md`` file the PR adds/changes. Without it the gate
    derives the card set itself from the merge-base diff vs ``origin/main``
    (:func:`_derive_diff_session_cards`, idea-engine ASK 003 — the sim-lab
    V051 false-green: after merging origin/main a sibling's COMPLETED card
    carries the freshest mtime, so the old newest-by-mtime guess validated
    the WRONG card), grading fail-closed via :func:`_select_gate_card`.
    Only when no git context is derivable (bare tree, no origin/main) does
    it fall back to newest-by-mtime with a NOTE — the non-git-adopter
    posture; with git context but no card in the diff, the gate treats the
    card as absent rather than silently mtime-greening. A named file that
    does not exist is treated exactly like an absent log (advisory by
    default, a hard failure under ``require_session_log``) — an explicit
    selection never silently falls back to a different card.

    Two KL-3 mechanisms ride the finding loop (plan §5.3):

    - **Reasons-required allowlist**: ``<state_dir>/check-exceptions.yml``
      entries suppress exact path+kind matches — but only entries carrying a
      ``reason``; a reason-less entry is refused and reported as its own
      finding. The session-log gate is never allowlistable.
    - **Guard-fire telemetry** (the ``check`` choke point): every surfaced
      finding — and every allowlist suppression, recorded with the entry's
      verdict + reason (creating the entry IS the verdict event) — appends a
      record to ``<state_dir>/guard-fires.jsonl``. Fail-open, written only
      into an existing install; the ``ci`` surface + ``did_not_run`` rows are
      derived by readers from the Checks API, never written in CI.
    """
    config = load_config(target)
    posture = "blocking" if strict else "advisory"
    # The control-protocol heartbeat (KL-8): static gate findings (missing /
    # heartbeat-less status.md) ride the strict loop like every checker;
    # wall-clock staleness is advisory-only and handled below — a required CI
    # check must never red on time alone (see check_status_current's docstring).
    # The validated path set is the host's configured heartbeat list (ORDER
    # 004: multi-Project repos gate one status file per lane).
    status_gate, status_advisories = check_status_current(
        target,
        status_files=config.heartbeat_files,
    )
    # Owner-action quality (ORDER 008): advisory-only by contract, like the
    # staleness warning — an unstructured ⚑ needs-owner ask nags on every run
    # (both lanes: the asks live in the heartbeat files the fast lane already
    # validates) but never reds a required check (see the checker docstring).
    owner_ask_advisories = check_owner_actions(
        target,
        status_files=config.heartbeat_files,
    )
    # Claims hygiene — orders AND work claims (ORDER 007 + EAP §6.4):
    # advisory-only, like the staleness and owner-action warnings — a
    # duplicate/stale `claimed-by:`, an orphaned/unparseable work-claim file,
    # or a legacy claims location is a coordination nudge the manager/session
    # reconciles, never a required-check red (the §6.4 compat guarantee: no
    # adopter's existing claims can go born-red on upgrade). Runs on both
    # lanes: order claims live on the heartbeat orders line and work claims
    # under control/claims/ — both control-lane surfaces.
    claim_advisories = check_claims(
        target,
        status_files=config.heartbeat_files,
        claims_dir=config.claims_dir,
    )
    # OWNER-ACTION ↔ CAPABILITIES cross-reference (kit-lab queue item 8, the
    # #68 card idea): advisory-only, like the ORDER 008 format nag it
    # extends — a wall-shaped ask whose wall the capability ledger doesn't
    # record (or records only as a working capability) nudges the session to
    # close the discovery-rule loop, never reds a required check (see the
    # checker docstring). Runs on both lanes: the asks live in the heartbeat
    # files the fast lane already validates.
    # Slice-5 extensions ride the same call (grounded-skills §4.2d): the
    # config hands the checker its staleness window (cadence.staleness_days,
    # default-on-missing) + sessions_dir for the newest-card citation scan.
    xref_advisories = check_capability_xref(
        target,
        status_files=config.heartbeat_files,
        config=config,
    )
    # Setup-script contract (EAP §6.5): advisory-only, like every nudge
    # above — the planted scripts/env-setup.sh is host-owned after adopt,
    # so contract drift (fatal posture / missing exit 0 / secret literal)
    # migrates by nag, never a required-check red. Full lane only: the hook
    # is not control-lane traffic (emitted below with the adopters block).
    setup_advisories = check_setup_script(target)
    # Skill command-grounding scan (grounded-skills slice 2, §8 Q2=B):
    # advisory-only by contract, like every nudge above — a skill body /
    # grounds entry / rendered SKILL.md naming a command that resolves
    # nowhere is a drift nudge for the session, never a required-check red
    # (UNVERIFIED per its provenance header; graduation is a later,
    # deliberate step). Full lane only: skills are not control-lane traffic.
    grounds_advisories = check_skill_grounds(target, state_dir=config.state_dir)
    # Staged-artifact regen-lag scan (ORDER 019 item 6, idea
    # staged-artifact-regen-lag-checker-2026-07-12): advisory-only by
    # contract, like every nudge above — a staged artifact still carrying a
    # ``${slot}`` whose answer is ALREADY filled in state is a one-command
    # regen nudge (`upgrade` / pack `--build`), never a required-check red
    # (UNVERIFIED per its PL-008 provenance header; a strict red would bomb
    # every green adopter whose staged tree predates its answers). Full lane
    # only: the staged tree is not control-lane traffic.
    staged_regen_advisories = check_staged_regen(target, config)
    # Template↔local-copy heading-set sync scan (idea
    # template-local-copy-sync-advisory-2026-07-15): advisory-only by
    # contract, like every nudge above — an ADOPT_PLAN doctrine section
    # existing on only one side of a template/local-copy pair is a
    # hand-sync nudge (the twice-in-one-day paid class: #395 observed,
    # #397 paid), never a required-check red (UNVERIFIED per its PL-008
    # provenance header). Self-gates everywhere but the kit's own repo —
    # only that tree carries src/engine/templates/, so adopters pay
    # nothing. Full lane only: template sources are not control-lane
    # traffic.
    template_sync_advisories = check_template_sync(target, config)
    # Archive-note completeness scan (archive-ready close-out plan §5 S4):
    # advisory-only by contract, like every nudge above — an
    # `archive-ready-*.md` note still carrying `[[fill:]]` slots, or a
    # zero-slot note whose guarded default text survives marker-stripping
    # (the S3 sham-resolution class, `probe_slot_residue` reused verbatim),
    # is a resolve-with-live-facts nudge, never a required-check red
    # (UNVERIFIED per its PL-008 provenance header; graduation to a
    # preflight/gate leg is a later, deliberate decision — plan §4.3).
    # Self-gates on repos with no archive notes. Full lane only: retro
    # notes are not control-lane traffic.
    archive_ready_advisories = check_archive_ready(target, config)
    # Session-card sham-resolution scan (KL-5 residue generalization, idea
    # filed on the archive-probe-s3 card): advisory-only by contract, like
    # every nudge above — a card that declares itself finished while a
    # drafted judgment-slot hint survives marker-stripping (the S3
    # sham-resolution class, shared fingerprint core in engine.lib.residue)
    # is a replace-wholesale nudge, never a required-check red (UNVERIFIED
    # per its PL-008 provenance header; graduation into the merge-blocking
    # session-gate lanes is a later, deliberate decision). Self-gates on
    # repos with no sessions dir. Full lane only: cards are not control-lane
    # traffic.
    card_residue_advisories = check_card_residue(target, config)
    # Seat-digest drift guard (grounded-skills slice 6, §8 Q2=B):
    # advisory-only by contract, like every nudge above — a planted
    # docs/seat-digest.md whose bytes differ from a fresh render of its
    # sources (skill index + capability ledger) is a regenerate nudge,
    # never a required-check red (UNVERIFIED per its PL-008 provenance
    # header; graduation is a later, deliberate step). Full lane only: the
    # digest is not control-lane traffic. The render context is rebuilt
    # from state so the fresh render matches what adopt/upgrade/regen
    # would write (only project_name matters to the render).
    digest_backend = JsonStateBackend(_state_path(target, config))
    digest_advisories = check_seat_digest(
        target,
        config,
        context=build_context(digest_backend.data) if digest_backend.data else {},
    )
    # K0 headroom gauge (PR #308, the nightcap-card 💡 spec): advisory-only
    # by contract, like every nudge above — the boot set nearing (but not
    # over) the orientation budget warns with the exact headroom + per-doc
    # split, so a docs session sees the pressure BEFORE the cliff reds
    # `check --strict` (UNVERIFIED per its PL-008 provenance header;
    # graduation is a later, deliberate step). Full lane only: boot docs are
    # not control-lane traffic. Over-budget stays the gate's verdict — the
    # advisory self-silences there (see the checker docstring).
    headroom_advisories = check_orientation_headroom(target, config)
    # Auto-merge-enabler branch-allowlist preflight (enabler-install-preflight
    # idea, 2026-07-13 night-run finding): advisory-only by contract, like
    # every nudge above — a planted auto-merge-enabler.yml whose branch
    # allowlist drifts from `automerge.branch_patterns` (a hand-edit that
    # `upgrade` clobbers, or a stale allowlist that never arms the branches
    # sessions push) is a regenerate/config nudge, never a required-check red
    # (the offline engine cannot verify the required-context half — that stays
    # owner-UI, surfaced by the enabler's own PR-time ::warning::). Full lane
    # only: workflows are not control-lane traffic; self-silences when the
    # live branch expr matches config.
    automerge_advisories = check_automerge_preflight(target, config)
    # Enforcement wiring-STRENGTH scan (idea engagement-wiring-strength-
    # verification-2026-07-12, sibling of the native_gate class): advisory-
    # only by contract, like every nudge above — a wired `check --strict`
    # door running the PLAIN form while the staged substrate-gate carries
    # the stronger legs (`--require-session-log`, diff-aware `--session-log`
    # selection, `--inbox-base`) is a copy-the-staged-gate nudge, never a
    # required-check red (the idea's letter: "a hand-rolled gate is
    # legitimate" — the kit's own ci.yml folds differently and carries all
    # three legs, so it self-silences). Full lane only: workflows are not
    # control-lane traffic.
    strength_advisories = check_enforcement_strength(target, config)
    # 📊 Model-line payload lint (idea model-line-payload-lint-advisory-
    # 2026-07-11, Night-8 triage #3): advisory-only by contract, like every
    # nudge above — a completed card whose Model line breaks the three-field
    # `·` shape, carries an exact model-ID token instead of a family-level
    # name, or files off-taxonomy effort/task-class segments is a copy-edit
    # nudge quoting the taught form verbatim, never a required-check red
    # (UNVERIFIED per its PL-008 provenance header; adopters carry drifted
    # historical cards today, so a gate would pre-redden them all on
    # upgrade). Scans the newest completed cards only (the checker's bounded
    # window — historical drift is measured, not nagged). Full lane only:
    # session cards are not control-lane traffic.
    model_line_advisories = check_model_line(
        target,
        sessions_dir=config.sessions_dir,
    )
    # Friction-outbox pending-count advisory (ORDER 020 item d, fm plan A10):
    # advisory-only by contract, like every nudge above — pending friction
    # envelopes previously surfaced only at session-close (the
    # cmd_session_close list_outbox advisory), so a session that never ran
    # the ritual sat on undrained reports through every `check --strict`.
    # Surfaced + telemetry-recorded, never counted toward the exit code —
    # the engine cannot file the issue itself (stdlib-only, no credentials);
    # the nudge is the mechanism. Full lane only: friction envelopes are not
    # control-lane traffic.
    outbox_pending = (
        [] if status_only else list_outbox(target, config.state_dir)
    )
    outbox_advisories = (
        [
            Finding(
                f"{config.state_dir}/friction-outbox/",
                "friction-outbox-pending",
                f"{len(outbox_pending)} friction report(s) pending — file "
                f"each as a `{FRICTION_LABEL}`-labeled issue on the kit "
                "repo (`friction show <name>` prints the issue title+body), "
                "then delete the drained file.",
            )
        ]
        if outbox_pending
        else []
    )
    # The inbox append-only gate (issue #36 report 2): a control/inbox.md
    # change must be pure-append vs the merge-base + ORDER-grammar shaped.
    # Rides the finding loop like every checker. CI hands in the base blob
    # via --inbox-base; a LOCAL run without one derives it from origin/main
    # itself (ORDER 018 — local `check --strict` must red where CI reds) and
    # self-skips, NOTE'd, when there is no git context to derive from.
    inbox_note: str | None = None
    if inbox_base is not None:
        inbox_findings = check_inbox_append(target, inbox_base)
    else:
        derived_blob, inbox_note = _derive_inbox_base(target)
        if derived_blob is None:
            inbox_findings = []
        else:
            base_fd, base_name = tempfile.mkstemp(prefix="inbox-base-")
            try:
                with os.fdopen(base_fd, "wb") as handle:
                    handle.write(derived_blob)
                inbox_findings = check_inbox_append(target, Path(base_name))
            finally:
                try:
                    os.unlink(base_name)
                except OSError:
                    pass
    if inbox_note:
        _emit(f"check: NOTE — {inbox_note}")
    # The adopter-registry format gate (EAP §6.3): docs/adopters.md is
    # generated output (`bootstrap currency`, agent-side because CI cannot
    # auth to sibling repos); CI validates only the committed file's shape.
    # Static format findings ride the strict loop; the staleness nag is
    # advisory-only, exactly like the heartbeat checker (a required check
    # never reds on wall-clock time alone). Engages only when the registry
    # exists — adopter repos add nothing here.
    adopters_gate, adopters_advisories = check_adopters_current(target)
    # Folded-gate diff-aware advisory (needs-planning §2 / folded-gate idea
    # 2026-07-11): a host that hand-FOLDED the session gate into its own CI
    # (superbot-next's `gate` job, websites' `quality.yml`) can freeze at the
    # pre-#19 newest-by-mtime card picker, misgrading a sibling's `complete`
    # card in a flat-mtime CI checkout. The kit never regenerates host-authored
    # workflows, so `check` is the only kit surface that runs in adopter repos.
    # Advisory-only, never exit-affecting (a hard red would break every adopter
    # that legitimately folds its gate before they can react) — and matched
    # precisely on "require-session-log present AND session-log absent" so the
    # kit's own diff-aware ci.yml and the planted gate stay silent.
    folded_gate_advisories = check_folded_gate(target)
    # Capability stale-wall advisory (night-run groom R5): surfaces any `wall`
    # row in docs/CAPABILITIES.md whose verification date has aged past the
    # staleness window (cadence.staleness_days, default 14) — the enforcement
    # analogue of the DISCOVERY RULE. Advisory-only, NEVER exit-affecting: a
    # wall aging out is a re-verify nudge, not a defect, so it is wired on the
    # posture="advisory" seam below (NOT _extra_check_findings, which counts
    # toward the exit code) and stays off STRICT_SUBCHECKS.
    stale_walls_advisories = check_stale_walls(target, config)
    if status_only:
        # --status-only: the fast lane's scoped gate (see docstring). Only the
        # control-lane checkers run — the heartbeat gate, the control-scoped
        # unrendered scan (queued fix 4: a control-only PR that writes a slot
        # regression into a control-plane planted doc must red HERE, not
        # poison the next full-lane PR — the #148/#150 incident), and, when
        # CI passes a base, the inbox append-only gate; everything downstream
        # (allowlist, guard fires, emit loop) is shared with the full run.
        doc_findings = (
            list(status_gate)
            + inbox_findings
            + check_engagement_control(target, config)
        )
    else:
        docs_root = target / config.docs_root
        doc_findings = list(
            run_doc_checks(
                docs_root,
                config.badge_tokens,
                config.readpath_docs,
            )
        )
        doc_findings += _extra_check_findings(target, config) + status_gate
        # Native-gate acceptance visibility (idea engagement-native-consumer-
        # state-2026-07-12): when a declared `native_gate` workflow is the
        # evidence keeping `enforcement-unwired` quiet, say so — accepted,
        # never silent. NOTE-only by contract: acceptance is a green path,
        # and the dead-declaration case reds via the finding itself.
        native_note = native_gate_note(target, config)
        if native_note:
            _emit(f"check: NOTE — {native_note}")
        # Required-ness honesty (the wiring-strength idea's layer 2, issue
        # #36 report 3): whether the CI door is a REQUIRED status check is
        # owner-UI state the stdlib engine cannot read — say so, once,
        # whenever a door exists. NOTE-only by contract, like the
        # acceptance NOTE above: honesty on a green path, never a finding.
        required_note = required_unverified_note(target, config)
        if required_note:
            _emit(f"check: NOTE — {required_note}")
        doc_findings += inbox_findings
        doc_findings += adopters_gate
        # Local preflight scripts (ORDER 018): the config-declared check
        # list both venues run — locally right here, and in CI because the
        # substrate-gate's full lane invokes `check --strict` (this code).
        # Full lane only: preflights are not control-lane traffic, and the
        # conventional wrapper itself calls `check --status-only` (the
        # nested-run guard in _run_preflight_scripts breaks any deeper
        # recursion). Findings ride the strict loop like every checker;
        # an absent script is a NOTE'd self-skip, never a red.
        preflight_findings, preflight_notes = _run_preflight_scripts(
            target,
            config,
        )
        for note in preflight_notes:
            _emit(f"check: NOTE — {note}")
        doc_findings += preflight_findings
    entries, allow_findings = load_allowlist(target, config.state_dir)
    doc_findings, suppressed = apply_allowlist(doc_findings, entries)
    doc_findings += allow_findings
    # Added-card grading (queued kit fix 1, the venture-lab #15 false-green
    # class + the superbot-games #40 born-red loophole): appended AFTER the
    # allowlist pass on purpose — like the session-log gate it extends, it
    # is never allowlistable. An in-progress ADDED card yields the born-red
    # HOLD finding (kind `session-card-hold`, so the designed-hold banner
    # below can recognise it); grammar misses keep `session-card-grammar`.
    if added_card is not None and not status_only:
        card_path = (
            added_card if added_card.is_absolute() else target / added_card
        )
        if card_path.is_file():
            card_rel = (
                str(card_path.relative_to(target))
                if card_path.is_relative_to(target)
                else str(card_path)
            )
            doc_findings += [
                Finding(
                    card_rel,
                    (
                        "session-card-hold"
                        if miss == BORN_RED_HOLD_MESSAGE
                        else "session-card-grammar"
                    ),
                    miss,
                )
                for miss in check_added_card(card_path, config.session_markers)
            ]
        else:
            _emit(
                f"check: --added-card {added_card} does not exist "
                "(advisory — nothing to grammar-check).",
            )
    # --simulate-added-card: the lane's advisory self-test (v1.9.0 wave
    # finding — the --added-card grading is unobservable on the very PR
    # that ships gate changes, because touching the gate workflow routes
    # the PR through the full locked door instead). Prints the lane's
    # would-be verdict; NEVER feeds doc_findings or the exit code.
    if simulate_added_card is not None and not status_only:
        sim_path = (
            simulate_added_card
            if simulate_added_card.is_absolute()
            else target / simulate_added_card
        )
        if not sim_path.is_file():
            _emit(
                f"check: simulate-added-card {simulate_added_card} does not "
                "exist — nothing to simulate (advisory).",
            )
        else:
            sim_misses = check_added_card(sim_path, config.session_markers)
            if not sim_misses:
                _emit(
                    f"check: simulate-added-card {simulate_added_card} — the "
                    "added-card lane would PASS (card declares a completed "
                    "Status and carries every marker).",
                )
            elif sim_misses == [BORN_RED_HOLD_MESSAGE]:
                _emit(
                    f"check: simulate-added-card {simulate_added_card} — the "
                    "added-card lane would HOLD (born-red: the card declares "
                    "an in-progress/drafted Status; the gate would stay red "
                    "until it flips complete).",
                )
            else:
                _emit(
                    f"check: simulate-added-card {simulate_added_card} — the "
                    f"added-card lane would RED with {len(sim_misses)} "
                    "finding(s):",
                )
                for miss in sim_misses:
                    _emit(f"  [simulated session-card-grammar] {miss}")
            _emit(
                "check: simulation is advisory-only — it never affects this "
                "run's exit code.",
            )
    # Guard-fire write announcement (PR #328 card's ⟲ finding): the ledger is
    # a TRACKED file by design (founding plan KF-11 — committed, never
    # gitignored), so a silent append leaves a "mystery" dirty tree that
    # sessions were reverting. Aggregate every call site's written count and
    # say so once, at the end of the run, on every return path.
    fires_written = 0

    def _announce_fires() -> None:
        if fires_written:
            _emit(
                f"check: {fires_written} guard-fire record(s) appended to "
                f"{config.state_dir}/{GUARD_FIRES_FILENAME} — telemetry "
                "ledger; commit the delta with your session (do not revert).",
            )

    if suppressed:
        _emit(
            f"check: {len(suppressed)} finding(s) suppressed by allowlist "
            "(reason-carrying entries; fires recorded with their verdicts).",
        )
        for finding, entry in suppressed:
            fires_written += record_guard_fires(
                target,
                config.state_dir,
                cmd="check",
                surface="check",
                posture=posture,
                findings=[finding],
                verdict=entry.get("verdict"),
                reason=entry.get("reason"),
            )
    if doc_findings:
        _emit(f"check: {len(doc_findings)} finding(s):")
        for finding in doc_findings:
            _emit(f"  [{finding.kind}] {finding.path}: {finding.message}")
        fires_written += record_guard_fires(
            target,
            config.state_dir,
            cmd="check",
            surface="check",
            posture=posture,
            findings=doc_findings,
        )
    if status_advisories:
        # Warn-only by contract: surfaced + telemetry-recorded, never counted
        # toward the exit code (a stale heartbeat must not red a required CI
        # check on wall-clock time alone — the Stop hook and this warning are
        # the nag; the manager's dark-Project read is the consequence).
        _emit(
            f"check: {len(status_advisories)} control-status advisory "
            "warning(s) (never exit-affecting):",
        )
        for finding in status_advisories:
            _emit(f"  [{finding.kind}] {finding.path}: {finding.message}")
        fires_written += record_guard_fires(
            target,
            config.state_dir,
            cmd="check",
            surface="check",
            posture="advisory",
            findings=status_advisories,
        )
    if owner_ask_advisories:
        # Same warn-only contract as the staleness advisory above: surfaced +
        # telemetry-recorded, never counted toward the exit code — the owner-
        # action format migrates by nag, not by locked door (ORDER 008).
        _emit(
            f"check: {len(owner_ask_advisories)} owner-action advisory "
            "warning(s) (never exit-affecting):",
        )
        for finding in owner_ask_advisories:
            _emit(f"  [{finding.kind}] {finding.path}: {finding.message}")
        fires_written += record_guard_fires(
            target,
            config.state_dir,
            cmd="check",
            surface="check",
            posture="advisory",
            findings=owner_ask_advisories,
        )
    if claim_advisories:
        # Same warn-only contract as the advisories above (ORDER 007 +
        # EAP §6.4): the duplicate/stale/format/legacy-location claim nudge
        # is surfaced + telemetry-recorded but never counted toward the exit
        # code — the manager adjudicates the tiebreak; the checker only
        # flags the collision/drift.
        _emit(
            f"check: {len(claim_advisories)} claims advisory "
            "warning(s) (never exit-affecting):",
        )
        for finding in claim_advisories:
            _emit(f"  [{finding.kind}] {finding.path}: {finding.message}")
        fires_written += record_guard_fires(
            target,
            config.state_dir,
            cmd="check",
            surface="check",
            posture="advisory",
            findings=claim_advisories,
        )
    if xref_advisories:
        # Same warn-only contract as the advisories above (queue item 8):
        # the ledger cross-reference is a coarse token-overlap nudge —
        # surfaced + telemetry-recorded, never counted toward the exit code;
        # a heuristic match can never be a verdict.
        _emit(
            f"check: {len(xref_advisories)} capability cross-reference "
            "advisory warning(s) (never exit-affecting):",
        )
        for finding in xref_advisories:
            _emit(f"  [{finding.kind}] {finding.path}: {finding.message}")
        fires_written += record_guard_fires(
            target,
            config.state_dir,
            cmd="check",
            surface="check",
            posture="advisory",
            findings=xref_advisories,
        )
    if setup_advisories and not status_only:
        # Same warn-only contract as the advisories above (EAP §6.5): the
        # setup-script hook is host-owned after planting — a contract nudge
        # (fatal posture, missing exit 0, secret-shaped literal) is surfaced
        # + telemetry-recorded, never counted toward the exit code, so no
        # adopter's hand-rolled script can red a required check on upgrade.
        _emit(
            f"check: {len(setup_advisories)} setup-script contract advisory "
            "warning(s) (never exit-affecting):",
        )
        for finding in setup_advisories:
            _emit(f"  [{finding.kind}] {finding.path}: {finding.message}")
        fires_written += record_guard_fires(
            target,
            config.state_dir,
            cmd="check",
            surface="check",
            posture="advisory",
            findings=setup_advisories,
        )
    if grounds_advisories and not status_only:
        # Same warn-only contract as the advisories above (grounded-skills
        # slice 2, §8 Q2=B advisory-first): an unresolvable skill command is
        # surfaced + telemetry-recorded, never counted toward the exit code
        # — the checker is UNVERIFIED (PL-008 header) and a coarse prose
        # scan can never be a verdict.
        _emit(
            f"check: {len(grounds_advisories)} skill-grounds advisory "
            "warning(s) (never exit-affecting):",
        )
        for finding in grounds_advisories:
            _emit(f"  [{finding.kind}] {finding.path}: {finding.message}")
        fires_written += record_guard_fires(
            target,
            config.state_dir,
            cmd="check",
            surface="check",
            posture="advisory",
            findings=grounds_advisories,
        )
    if staged_regen_advisories and not status_only:
        # Same warn-only contract as the advisories above (ORDER 019 item 6,
        # advisory-first per the idea file's adopt-freely posture): a staged
        # artifact lagging its own filled answers is surfaced + telemetry-
        # recorded, never counted toward the exit code — the fix is one
        # regen command, not a locked door.
        _emit(
            f"check: {len(staged_regen_advisories)} staged regen-lag advisory "
            "warning(s) (never exit-affecting):",
        )
        for finding in staged_regen_advisories:
            _emit(f"  [{finding.kind}] {finding.path}: {finding.message}")
        fires_written += record_guard_fires(
            target,
            config.state_dir,
            cmd="check",
            surface="check",
            posture="advisory",
            findings=staged_regen_advisories,
        )
    if template_sync_advisories and not status_only:
        # Same warn-only contract as the advisories above (idea
        # template-local-copy-sync-advisory-2026-07-15, advisory-first per
        # its guard recipe): a doctrine heading existing on only one side
        # of a template/local-copy pair is surfaced + telemetry-recorded,
        # never counted toward the exit code — the fix is one hand-sync
        # edit, and a deliberate local divergence is a judgment call no
        # locked door can adjudicate.
        _emit(
            f"check: {len(template_sync_advisories)} template-sync advisory "
            "warning(s) (never exit-affecting):",
        )
        for finding in template_sync_advisories:
            _emit(f"  [{finding.kind}] {finding.path}: {finding.message}")
        fires_written += record_guard_fires(
            target,
            config.state_dir,
            cmd="check",
            surface="check",
            posture="advisory",
            findings=template_sync_advisories,
        )
    if archive_ready_advisories and not status_only:
        # Same warn-only contract as the advisories above (archive-ready
        # close-out plan §5 S4, advisory-first per plan §4.3): an incomplete
        # archive note — unresolved slots, or guarded-slot residue from a
        # sham resolution — is surfaced + telemetry-recorded, never counted
        # toward the exit code — the checker is UNVERIFIED (PL-008 header)
        # and the fix is resolving the note with live facts, not a locked
        # door.
        _emit(
            f"check: {len(archive_ready_advisories)} archive-note advisory "
            "warning(s) (never exit-affecting):",
        )
        for finding in archive_ready_advisories:
            _emit(f"  [{finding.kind}] {finding.path}: {finding.message}")
        fires_written += record_guard_fires(
            target,
            config.state_dir,
            cmd="check",
            surface="check",
            posture="advisory",
            findings=archive_ready_advisories,
        )
    if card_residue_advisories and not status_only:
        # Same warn-only contract as the advisories above (KL-5 residue
        # generalization, advisory-first mirroring the S4 introduction): a
        # sham-resolved session card — drafted hint text surviving with its
        # [[fill:]] markers stripped — is surfaced + telemetry-recorded,
        # never counted toward the exit code — the checker is UNVERIFIED
        # (PL-008 header) and the fix is replacing each surviving hint
        # wholesale with genuine session text, not a locked door.
        _emit(
            f"check: {len(card_residue_advisories)} session-card residue "
            "advisory warning(s) (never exit-affecting):",
        )
        for finding in card_residue_advisories:
            _emit(f"  [{finding.kind}] {finding.path}: {finding.message}")
        fires_written += record_guard_fires(
            target,
            config.state_dir,
            cmd="check",
            surface="check",
            posture="advisory",
            findings=card_residue_advisories,
        )
    if digest_advisories and not status_only:
        # Same warn-only contract as the advisories above (grounded-skills
        # slice 6, §8 Q2=B advisory-first): a stale/over-budget seat digest
        # is surfaced + telemetry-recorded, never counted toward the exit
        # code — the checker is UNVERIFIED (PL-008 header); the fix is one
        # `bootstrap.py seat-digest` regen, not a locked door.
        _emit(
            f"check: {len(digest_advisories)} seat-digest advisory "
            "warning(s) (never exit-affecting):",
        )
        for finding in digest_advisories:
            _emit(f"  [{finding.kind}] {finding.path}: {finding.message}")
        fires_written += record_guard_fires(
            target,
            config.state_dir,
            cmd="check",
            surface="check",
            posture="advisory",
            findings=digest_advisories,
        )
    if headroom_advisories and not status_only:
        # Same warn-only contract as the advisories above (PR #308): the
        # near-budget boot set is a trim-early nudge — surfaced + telemetry-
        # recorded, never counted toward the exit code; the cliff itself
        # (over budget) stays the exit-affecting orientation-budget gate.
        _emit(
            f"check: {len(headroom_advisories)} orientation-headroom advisory "
            "warning(s) (never exit-affecting):",
        )
        for finding in headroom_advisories:
            _emit(f"  [{finding.kind}] {finding.path}: {finding.message}")
        fires_written += record_guard_fires(
            target,
            config.state_dir,
            cmd="check",
            surface="check",
            posture="advisory",
            findings=headroom_advisories,
        )
    if automerge_advisories and not status_only:
        # Same warn-only contract as the advisories above
        # (enabler-install-preflight): a drifted enabler branch allowlist is a
        # regenerate/config nudge — surfaced + telemetry-recorded, never
        # counted toward the exit code. The offline engine cannot see whether
        # the base branch requires a status context (the INERT-on-zero half),
        # so a required-check red here would be a fleet bomb during version
        # skew; that half stays owner-UI.
        _emit(
            f"check: {len(automerge_advisories)} auto-merge-enabler advisory "
            "warning(s) (never exit-affecting):",
        )
        for finding in automerge_advisories:
            _emit(f"  [{finding.kind}] {finding.path}: {finding.message}")
        fires_written += record_guard_fires(
            target,
            config.state_dir,
            cmd="check",
            surface="check",
            posture="advisory",
            findings=automerge_advisories,
        )
    if strength_advisories and not status_only:
        # Same warn-only contract as the advisories above (idea engagement-
        # wiring-strength-verification-2026-07-12, advisory-first per its
        # guard recipe): a plain-form wired gate is a copy-the-staged-file
        # nudge — surfaced + telemetry-recorded, never counted toward the
        # exit code; a hand-rolled gate is a legitimate door, and a strict
        # red here would bomb every weak-form adopter on upgrade.
        _emit(
            f"check: {len(strength_advisories)} enforcement-strength advisory "
            "warning(s) (never exit-affecting):",
        )
        for finding in strength_advisories:
            _emit(f"  [{finding.kind}] {finding.path}: {finding.message}")
        fires_written += record_guard_fires(
            target,
            config.state_dir,
            cmd="check",
            surface="check",
            posture="advisory",
            findings=strength_advisories,
        )
    if model_line_advisories and not status_only:
        # Same warn-only contract as the advisories above (the model-line
        # payload lint, idea 2026-07-11): a drifted 📊 Model payload on a
        # completed card is a one-line copy-edit nudge — surfaced +
        # telemetry-recorded, never counted toward the exit code; the PL-004
        # dataset records drift verbatim either way, the lint just makes it
        # visible at check time instead of a later hand sweep.
        _emit(
            f"check: {len(model_line_advisories)} model-line payload advisory "
            "warning(s) (never exit-affecting):",
        )
        for finding in model_line_advisories:
            _emit(f"  [{finding.kind}] {finding.path}: {finding.message}")
        fires_written += record_guard_fires(
            target,
            config.state_dir,
            cmd="check",
            surface="check",
            posture="advisory",
            findings=model_line_advisories,
        )
    if outbox_advisories and not status_only:
        # Same warn-only contract as the advisories above (ORDER 020 item d,
        # fm plan A10): a pending friction envelope is a drain-me nudge —
        # surfaced + telemetry-recorded, never counted toward the exit code;
        # the session-close ritual keeps its own copy of this advisory, this
        # one just makes the backlog visible at check time too.
        _emit(
            f"check: {len(outbox_advisories)} friction-outbox advisory "
            "warning(s) (never exit-affecting):",
        )
        for finding in outbox_advisories:
            _emit(f"  [{finding.kind}] {finding.path}: {finding.message}")
        fires_written += record_guard_fires(
            target,
            config.state_dir,
            cmd="check",
            surface="check",
            posture="advisory",
            findings=outbox_advisories,
        )
    if adopters_advisories and not status_only:
        # Same warn-only contract as the advisories above (EAP §6.3): a
        # stale `Generated:` stamp is a rerun-the-scan nudge — CI cannot
        # refetch (no auth to sibling repos), so time-based red here would
        # be a bomb; surfaced + telemetry-recorded, never exit-affecting.
        _emit(
            f"check: {len(adopters_advisories)} adopter-registry advisory "
            "warning(s) (never exit-affecting):",
        )
        for finding in adopters_advisories:
            _emit(f"  [{finding.kind}] {finding.path}: {finding.message}")
        fires_written += record_guard_fires(
            target,
            config.state_dir,
            cmd="check",
            surface="check",
            posture="advisory",
            findings=adopters_advisories,
        )
    if folded_gate_advisories and not status_only:
        # Same warn-only contract as the advisories above (needs-planning §2):
        # a host-folded session gate that froze at the pre-#19 mtime picker is
        # a port-the-diff-aware-block nudge — the kit cannot regenerate a
        # host-authored workflow, so this is surfaced + telemetry-recorded but
        # NEVER counted toward the exit code (a hard red would break adopters
        # that legitimately fold their gate). Deliberately off STRICT_SUBCHECKS.
        _emit(
            f"check: {len(folded_gate_advisories)} folded-gate advisory "
            "warning(s) (never exit-affecting):",
        )
        for finding in folded_gate_advisories:
            _emit(f"  [{finding.kind}] {finding.path}: {finding.message}")
        fires_written += record_guard_fires(
            target,
            config.state_dir,
            cmd="check",
            surface="check",
            posture="advisory",
            findings=folded_gate_advisories,
        )
    if stale_walls_advisories and not status_only:
        # Same warn-only contract as the advisories above (night-run groom R5):
        # a documented wall whose LAST-VERIFIED date has aged past the window is
        # a re-verify-per-the-DISCOVERY-RULE nudge — a platform classifier can
        # loosen and a stale wall may already be false, but a still-real wall
        # aging out is not a defect. Surfaced + telemetry-recorded, NEVER
        # counted toward the exit code (deliberately off STRICT_SUBCHECKS).
        _emit(
            f"check: {len(stale_walls_advisories)} stale-wall advisory "
            "warning(s) (never exit-affecting):",
        )
        for finding in stale_walls_advisories:
            _emit(f"  [{finding.kind}] {finding.path}: {finding.message}")
        fires_written += record_guard_fires(
            target,
            config.state_dir,
            cmd="check",
            surface="check",
            posture="advisory",
            findings=stale_walls_advisories,
        )

    log_missing: list[str] = []
    log_absent_fails = False
    if status_only:
        # The fast lane's scoped gate never touches the session-log seam: a
        # control-only heartbeat PR carries no card by design (the lane's
        # whole point), so gating on one here would deadlock every heartbeat.
        if not doc_findings:
            _emit("check: control-status check passed (--status-only).")
            _announce_fires()
            return 0
        _announce_fires()
        return 1 if strict else 0
    diff_no_card = False
    if session_log is not None:
        explicit = session_log if session_log.is_absolute() else target / session_log
        log = explicit if explicit.is_file() else None
    else:
        # Diff-derived selection (idea-engine ASK 003, the sim-lab V051
        # false-green): with git context the card set comes from the
        # merge-base diff vs origin/main — the CI gate's selection — never
        # from mtime (a post-merge sibling card carries the freshest mtime
        # and the mtime guess validated the WRONG card, green while the
        # session's own card was still in-progress). No git context →
        # the historical newest-by-mtime fallback (non-git adopters are
        # unchanged); git context but no card in the diff → absent-card
        # semantics, never a silent mtime-green (fail-closed on ambiguity).
        diff_cards, diff_note = _derive_diff_session_cards(
            target,
            config.sessions_dir,
        )
        if diff_note:
            _emit(f"check: NOTE — {diff_note}")
        if diff_cards is None:
            log = latest_session_log(target / config.sessions_dir)
        elif diff_cards:
            log = _select_gate_card(diff_cards, config.session_markers)
            gate_rel = (
                log.relative_to(target) if log.is_relative_to(target) else log
            )
            _emit(
                f"check: session-card selection — {len(diff_cards)} card(s) "
                f"in the merge-base diff vs origin/main; gating on {gate_rel}.",
            )
        else:
            log = None
            diff_no_card = True
    if session_log is not None:
        absent = f"--session-log {session_log} does not exist"
    elif diff_no_card:
        absent = (
            f"no session card in the merge-base diff vs origin/main (under "
            f"{config.sessions_dir}/; diff-derived selection never falls "
            "back to the mtime guess when git context exists)"
        )
    else:
        absent = f"no session log under {config.sessions_dir}/"
    log_missing = check_log(log, config.session_markers) if log else []
    # In gate mode an absent log is itself a failing condition, so it must feed
    # the exit code exactly like an incomplete one.
    log_absent_fails = log is None and require_session_log
    # Unadopted-auto-draft advisory lane (B1 run-8): a card the ENGINE wrote
    # (Stop-hook draft) that no session ever adopted must not leave the repo
    # red for the NEXT session's bare `check --strict` — run-8's ON arm ended
    # exit=1 solely on its own untouched skeleton, and the next cold session
    # would inherit that red without owning the judgment slots. Applies ONLY
    # to the local fallback lane (no explicit --session-log — whether the
    # card came from the diff derivation or the mtime guess): an explicit
    # --session-log selection or --require-session-log gate mode keeps the
    # locked door (a PR shipping a drafted card is the born-red discipline,
    # not this class).
    draft_advisory = False
    if (
        log is not None
        and log_missing
        and session_log is None
        and not require_session_log
    ):
        try:
            draft_advisory = is_unadopted_draft(log.read_text(encoding="utf-8"))
        except OSError:
            draft_advisory = False
    if log is None:
        if require_session_log:
            _emit(
                f"check: MERGE HELD — {absent} "
                "(--require-session-log): write one before merging.",
            )
        else:
            _emit(f"check: {absent} (advisory — not a failure).")
    else:
        rel = log.relative_to(target) if log.is_relative_to(target) else log
        if log_missing and draft_advisory:
            _emit(
                f"check: session log {rel} is an unadopted auto-draft "
                f"({', '.join(log_missing)}) — advisory in the mtime-fallback "
                "lane, not exit-affecting: adopt it (verify the evidence, "
                "resolve the [[fill:]] slots, flip the Status badge) or it "
                "holds the merge in gate mode (--require-session-log / "
                "--session-log / --added-card).",
            )
            fires_written += record_guard_fires(
                target,
                config.state_dir,
                cmd="check",
                surface="check",
                posture="advisory",
                findings=[
                    Finding(
                        str(rel),
                        "session-log-draft",
                        f"unadopted auto-draft: {', '.join(log_missing)}",
                    ),
                ],
            )
            log_missing = []
        elif log_missing:
            _emit(f"check: session log {rel} is missing: {', '.join(log_missing)}")
        else:
            _emit(f"check: session log {rel} complete.")
    if log_missing or log_absent_fails:
        # The session gate is a guard too (the kit's flagship one) — its
        # fires feed B3 like any checker's. Never allowlistable, though.
        if log_absent_fails:
            gate_finding = Finding(
                "",
                "session-log",
                f"{absent} (--require-session-log)",
            )
        else:
            log_rel = str(log.relative_to(target)) if log.is_relative_to(target) else str(log)
            gate_finding = Finding(
                log_rel,
                "session-log",
                f"missing: {', '.join(log_missing)}",
            )
        fires_written += record_guard_fires(
            target,
            config.state_dir,
            cmd="check",
            surface="check",
            posture="blocking" if (strict or require_session_log) else "advisory",
            findings=[gate_finding],
        )

    # Designed-hold signal (queued kit fix 4, the PL-006 observer-noise
    # class): with parallel sessions, every born-red PR's mid-flight red CI
    # draws "investigate this failure" pings from coordinators/observers —
    # three live occurrences (#140/#144/#147 class, again on #153). When the
    # ONLY thing holding the run red is a session card that itself DECLARES
    # an in-progress/drafted Status, the red is the born-red discipline
    # working as designed — say so, unmissably, in the failing output (and
    # as a GitHub annotation when running in Actions) so an observer can
    # tell a designed hold from a real defect without opening the job log's
    # fine print. Any other finding alongside suppresses the banner: a
    # partially-real failure must never be labelled "by design".
    added_card_holds = [f for f in doc_findings if f.kind == "session-card-hold"]
    hold_is_designed = (
        strict
        and not doc_findings
        and not log_absent_fails
        and log is not None
        and bool(log_missing)
        and _card_declares_in_progress(log)
    )
    # Same banner for the added-card lane's born-red HOLD (the
    # superbot-games #40 loophole fix): when the ONLY thing holding the run
    # red is the ADDED card's in-progress declaration, that red is the
    # designed hold too — an observer must be able to tell it from a defect
    # without opening the fine print. Any other finding alongside (a grammar
    # miss, a doc finding, an incomplete --session-log card) suppresses it.
    added_hold_is_designed = (
        strict
        and bool(added_card_holds)
        and len(doc_findings) == len(added_card_holds)
        and not log_missing
        and not log_absent_fails
    )
    if added_hold_is_designed:
        hold_rel = added_card_holds[0].path
    elif hold_is_designed:
        hold_rel = log.relative_to(target) if log.is_relative_to(target) else log
    if hold_is_designed or added_hold_is_designed:
        _emit(
            f"check: HOLD (by design): session card {hold_rel} declares an "
            "in-progress Status — the born-red session gate holds the merge "
            "red until the card flips complete. This red is the designed "
            "hold, not a defect; nothing to investigate.",
        )
        if os.environ.get("GITHUB_ACTIONS"):
            _emit(
                "::notice title=HOLD: session card in-progress (by design)::"
                f"The born-red session gate is holding this red until {hold_rel} "
                "flips complete. Designed hold — not a CI failure to "
                "investigate.",
            )
    if not doc_findings and not log_missing and not log_absent_fails:
        _emit("check: all checks passed.")
        _announce_fires()
        return 0
    _announce_fires()
    return 1 if strict else 0


def _card_declares_in_progress(log: Path) -> bool:
    """True when ``log``'s own Status badge carries an in-progress value.

    The designed-hold banner's honesty condition (fix 4): the card must SAY
    it is mid-flight — a card that claims ``complete`` but still reds is a
    real defect and never gets the "by design" label. Unreadable → False
    (never claim design intent on evidence that cannot be read).
    """
    try:
        return status_in_progress(log.read_text(encoding="utf-8"))
    except OSError:
        return False


def _require_state(
    target: Path,
    command: str,
) -> tuple[Config, JsonStateBackend] | None:
    """Load config + state; None (with a message) when the install is missing.

    Also runs the live-loop guardrail: state-backed commands read AND write
    the install, and only ``init``/``adopt`` were guarded before — ``ledger``,
    the ``--build`` emitters, and ``episodes --rebuild`` wrote into a target
    the guardrail would have refused.
    """
    assert_safe_target(target, _kit_root())
    config = load_config(target)
    backend = JsonStateBackend(_state_path(target, config))
    if not backend.data:
        _emit(f"{command}: no state at {target} (run init first).")
        return None
    return config, backend


def _question_for_slot(slot: str) -> dict | None:
    """Return the bank question that fills ``slot`` (None when unknown)."""
    for question in QUESTIONS:
        if question["slot"] == slot:
            return question
    return None


def cmd_answer(target: Path, slot: str, answer: str) -> int:
    """Record a user answer for ``slot`` (fills it, resolves its escalation)."""
    loaded = _require_state(target, "answer")
    if loaded is None:
        return 1
    _, backend = loaded
    question = _question_for_slot(slot)
    if question is None:
        known = ", ".join(q["slot"] for q in QUESTIONS)
        _emit(f"answer: unknown slot {slot!r} (known: {known}).")
        return 2
    record_answer(backend, question, answer, source="user")
    status = backend.get("slots", {}).get(slot)
    _emit(f"answer: {slot} -> {status}.")
    if status == "partial":
        floor = int(question.get("min_len", 1))
        _emit(f"answer: too thin to count (needs >= {floor} chars of substance).")
    if status == "filled":
        _emit_gate_safety_advisory(backend, slot)
    return 0


def _emit_gate_safety_advisory(backend: JsonStateBackend, slot: str) -> None:
    """Surface verify_command gate-unsafety at the moment the slot fills.

    The answer-time half of the #405 honored-lane contract (the #405
    card's 💡): only a filled + gate-safe + non-default ``verify_command``
    drives the generated substrate-gate's test step, and a prose-y value
    otherwise fails that bar SILENTLY — the divergence surfaces only at
    the next adopt/upgrade. Advisory prose only; never changes state or
    exit codes. No-op for every other slot.
    """
    if slot != "verify_command":
        return
    entry = backend.get("slot_values", {}).get(slot)
    value = entry.get("value") if isinstance(entry, dict) else None
    if not isinstance(value, str):
        return
    advisory = gate_test_command_advisory(value)
    if advisory:
        _emit(advisory)


def cmd_confirm(target: Path, slot: str) -> int:
    """Confirm a provisional (self-answered) slot as user-verified."""
    loaded = _require_state(target, "confirm")
    if loaded is None:
        return 1
    _, backend = loaded
    if confirm_slot(backend, slot, source="user"):
        _emit(f"confirm: {slot} confirmed (provisional -> filled).")
        _emit_gate_safety_advisory(backend, slot)
        return 0
    _emit(f"confirm: {slot} is not provisional (nothing to confirm).")
    return 1


def cmd_triggers(target: Path) -> int:
    """Scan for fired triggers and show the mandated / advisory questions."""
    loaded = _require_state(target, "triggers")
    if loaded is None:
        return 1
    config, backend = loaded
    triggers = check_triggers(target, config, backend.data)
    if not triggers:
        _emit("triggers: none fired.")
        return 0
    questions = mandatory_questions(triggers)
    block = trigger_block(
        triggers,
        questions,
        mandate=triggers_mandate(backend.data),
    )
    _emit(block)
    return 0


def cmd_reflect(
    target: Path,
    *,
    add: str | None,
    evidence: str,
    tags: str,
    mine: bool,
) -> int:
    """List, add to, or mine the forward reflection buffer."""
    loaded = _require_state(target, "reflect")
    if loaded is None:
        return 1
    config, backend = loaded
    path = target / config.state_dir / REFLECTIONS_FILENAME
    buffer_size = int(config.reflection.get("buffer_size", 5))
    if add is not None:
        entry = add_reflection(
            path,
            lesson=add,
            evidence=evidence,
            tags=[t for t in tags.split(",") if t],
            buffer_size=buffer_size,
        )
        _emit(f"reflect: added {entry['id']}.")
    if mine:
        known = {e.get("lesson", "") for e in load_reflections(path)}
        candidates = [
            c
            for c in mine_reflections(target / config.sessions_dir)
            if c["lesson"] not in known
        ]
        for cand in candidates:
            entry = add_reflection(
                path,
                lesson=cand["lesson"],
                evidence=cand.get("evidence", ""),
                tags=list(cand.get("tags", [])),
                buffer_size=buffer_size,
            )
            known.add(cand["lesson"])
            _emit(f"reflect: mined {entry['id']} — {cand['lesson'][:60]}")
        if not candidates:
            _emit("reflect: mined nothing new.")
    entries = load_reflections(path)
    backend.set(
        "reflection_buffer",
        {
            "active_count": len(entries),
            "last_mined": (
                date.today().isoformat()
                if mine
                else (backend.get("reflection_buffer", {}) or {}).get("last_mined")
            ),
        },
    )
    block = lessons_block(entries)
    _emit(block if block else "reflect: buffer empty.")
    return 0


def cmd_episodes(target: Path, *, rebuild: bool, search: str | None) -> int:
    """Rebuild or search the episodic index over the session logs."""
    config = load_config(target)
    if rebuild:
        assert_safe_target(target, _kit_root())
    index_path = target / config.state_dir / EPISODIC_INDEX_FILENAME
    if rebuild:
        entries = rebuild_episodic_index(target / config.sessions_dir, index_path)
        _emit(f"episodes: indexed {len(entries)} session(s).")
    if search is not None:
        hits = search_episodes(index_path, search)
        for hit in hits:
            _emit(
                f"  {hit.get('date', '?')} {hit.get('slug', '?')} — "
                f"{hit.get('summary', '')}",
            )
        _emit(f"episodes: {len(hits)} hit(s) for {search!r}.")
    if not rebuild and search is None:
        _emit("episodes: pass --rebuild and/or --search TAG.")
    return 0


def cmd_metrics(target: Path) -> int:
    """Emit the router / workflow KPIs (JSON + the one-line footer)."""
    loaded = _require_state(target, "metrics")
    if loaded is None:
        return 1
    config, backend = loaded
    kpis = workflow_kpis(backend.data, target / config.sessions_dir)
    _emit(json.dumps(kpis, indent=2, sort_keys=True))
    _emit(kpi_footer(kpis))
    return 0


def cmd_maintain(target: Path, *, compact: bool) -> int:
    """Run the self-maintenance loop's report (and compaction when asked)."""
    loaded = _require_state(target, "maintain")
    if loaded is None:
        return 1
    config, backend = loaded
    if compact:
        if compaction_due(backend.data, dict(config.cadence or {})):
            path = run_compaction(target, config, backend)
            rel = path.relative_to(target) if path.is_relative_to(target) else path
            _emit(f"maintain: compaction written -> {rel}")
        else:
            _emit("maintain: compaction not due.")
    triggers = check_triggers(target, config, backend.data)
    economy = economy_check(target, config)
    ledger_path = target / config.docs_root / LEDGER_FILENAME
    ledger_findings = check_ledger(ledger_path) if ledger_path.exists() else []
    kpis = workflow_kpis(backend.data, target / config.sessions_dir)
    _emit(
        maintenance_report(
            target,
            config,
            backend,
            triggers=triggers,
            economy_findings=list(economy.get("findings", [])),
            ledger_findings=ledger_findings,
            kpis=kpis,
        ),
    )
    return 0


def cmd_review(
    target: Path,
    action: str,
    slot: str | None,
    *,
    verdict: str,
    reviewer: str,
) -> int:
    """Drive the independent-review seam: build payloads, record verdicts."""
    if action == "doc":
        _emit(seam_wiring_doc())
        return 0
    if slot is None:
        _emit("review: a slot is required for build/confirm.")
        return 2
    loaded = _require_state(target, "review")
    if loaded is None:
        return 1
    config, backend = loaded
    if action == "build":
        payload = build_review_payload(backend, slot)
        if not payload:
            _emit(f"review: slot {slot!r} is not provisional — nothing to review.")
            return 1
        path = write_review_payload(target, config, payload)
        rel = path.relative_to(target) if path.is_relative_to(target) else path
        _emit(f"review: payload written -> {rel}")
        return 0
    if action == "confirm":
        if verdict not in ("pass", "fail"):
            _emit("review: --verdict must be pass or fail.")
            return 2
        outcome = apply_review_verdict(
            backend,
            slot,
            verdict=verdict,
            reviewer=reviewer,
        )
        _emit(f"review: {slot} -> {outcome}.")
        if outcome == "not-provisional":
            _emit(
                "review: nothing recorded — the slot is not provisional "
                "(typo, already confirmed, or never answered).",
            )
            return 1
        # The verdict is recorded → the payload is consumed. Remove it so the
        # maintenance "awaiting a reviewer" count reflects reality.
        if clear_review_payload(target, config, slot):
            _emit(f"review: cleared consumed payload for {slot}.")
        return 0
    _emit(f"review: unknown action {action!r} (build | confirm | doc).")
    return 2


def cmd_economy(
    target: Path,
    action: str,
    *,
    strict: bool,
    apply: bool,
    reviewed: bool,
    bands: int,
) -> int:
    """Drive the context-economy engine: check, apply, simulate, recipe."""
    config = load_config(target)
    if action == "recipe":
        _emit(calibration_recipe())
        return 0
    if action == "simulate":
        result = run_search(default_calibration(), bands=bands)
        _emit(str(result.get("why_it_won", "")))
        winner = result.get("winner", {})
        name = winner.get("name") if isinstance(winner, dict) else winner
        _emit(f"economy: winner {name} (feasible: {result.get('feasible_count')}).")
        return 0
    pass_records = (
        target / config.docs_root / config.economy.get("pass_records_dir", "planning")
    )
    harvested = parse_harvest_tables(pass_records)
    report = economy_check(
        target,
        config,
        harvested=harvested,
        harvest_exclude=harvest_sources(pass_records),
    )
    if action == "issue-body":
        _emit(issue_body(report))
        return 0
    if action == "check":
        census = report.get("census", {})
        for name in sorted(census):
            row = census[name]
            _emit(
                f"  class {name}: {row.get('files', 0)} file(s), "
                f"{row.get('words', 0)} word(s)",
            )
        for gauge in report.get("gauges", []):
            flag = "OVER" if gauge.get("over") else "ok"
            _emit(f"  gauge {gauge['name']}: {gauge['value']}/{gauge['cap']} [{flag}]")
        findings = report.get("findings", [])
        for finding in findings:
            _emit(f"  [{finding.kind}] {finding.path}: {finding.message}")
        for line in economy_actuate(target, config, report, apply=False):
            _emit(f"  would-act: {line}")
        debt = report.get("debt", 0)
        threshold = int(config.economy.get("debt_threshold", 10))
        _emit(f"economy: debt {debt} (threshold {threshold}).")
        over = bool(findings) or debt >= threshold
        return 1 if strict and over else 0
    if action == "apply":
        if apply:
            backend = JsonStateBackend(_state_path(target, config))
            if backend.data and not actuators_may_apply(backend.data):
                _emit(
                    "economy: refused — the mode/promotion policy does not "
                    "permit actuators to apply (promotion_rights must be "
                    "'promote'); dry-run only.",
                )
                return 1
        lines = economy_actuate(
            target,
            config,
            report,
            apply=apply,
            acknowledged=reviewed,
        )
        for line in lines:
            _emit(f"  {line}")
        if not apply:
            _emit("economy: dry-run (pass --yes to act; maturity gates apply).")
        return 0
    _emit(
        f"economy: unknown action {action!r} "
        "(check | apply | simulate | recipe | issue-body).",
    )
    return 2


def cmd_adopt(
    target: Path,
    include_claude: bool,
    wire_enforcement: bool = False,
    lane: str | None = None,
) -> int:
    """Adopt the workflow into ``target``: init, plant the docs, stage the packs.

    The one-step flow: ``init`` runs first (idempotent — config + state), so a
    bare directory with nothing but the bootstrap file becomes a fully
    substrate-governed project in this single command. ``wire_enforcement``
    additionally turns on the live nag hook + the CI locked door. ``lane``
    is the SHARED-repo shape (multi-Project cohabitation): this Project's
    heartbeat plants as ``control/status-<lane>.md`` and is declared in
    ``heartbeat_files``; the rest of the bus is shared, never re-planted.
    """
    rc = cmd_init(target)
    if rc != 0:
        return rc
    config = load_config(target)
    backend = JsonStateBackend(_state_path(target, config))
    try:
        lines = adopt(
            target,
            config,
            backend,
            kit_root=_kit_root(),
            include_claude=include_claude,
            wire_enforcement=wire_enforcement,
            lane=lane,
        )
    except ValueError as exc:
        _emit(f"adopt: REFUSED — {exc}")
        return 2
    for line in lines:
        _emit(f"adopt: {line}")
    # KL-7 — the adopter is told, in the adopt output itself, exactly what the
    # born-red engagement gate needs: the gate's findings ARE the checklist.
    # KL-8 rider: the control-protocol gate findings (the just-planted seed
    # status.md has no heartbeat yet) join the same checklist — "write your
    # first real heartbeat" is part of engaging, same shape as the first card.
    status_gate, _ = check_status_current(
        target,
        status_files=config.heartbeat_files,
    )
    engage = check_engagement(target, config) + status_gate
    if engage:
        _emit(
            f"adopt: NOT ENGAGED — `check --strict` holds RED until these "
            f"{len(engage)} item(s) are done:",
        )
        for finding in engage:
            where = f"{finding.path}: " if finding.path else ""
            _emit(f"adopt:   [{finding.kind}] {where}{finding.message}")
    else:
        _emit("adopt: ENGAGED — the post-adopt gate is green.")
    return 0


def cmd_upgrade(
    target: Path,
    *,
    apply_docs: bool,
    rollback: bool,
    release_json: Path | None,
    keep_inputs: bool = False,
) -> int:
    """Run the §4.3 upgrade flow (or ``--rollback``) against ``target``.

    The consumer flow: download the new release's file as ``bootstrap.py.new``
    (plus its ``release.json`` for sha256 verification) and run
    ``python3 bootstrap.py.new upgrade``. Archives before it overwrites;
    planted docs are only ever touched under ``--apply-docs`` and only when
    the recorded hash proves the consumer never edited them. On completion
    the consumed inputs (the ``.new`` file + its adjacent ``release.json``)
    are removed unless ``--keep-inputs``.
    """
    loaded = _require_state(target, "upgrade")
    if loaded is None:
        return 1
    config, backend = loaded
    if rollback:
        for line in run_rollback(target, config):
            _emit(f"upgrade: {line}")
        return 0
    running = (
        Path(sys.argv[0]).resolve()
        if sys.argv and sys.argv[0]
        else Path(__file__).resolve()
    )
    try:
        lines = run_upgrade(
            target,
            config,
            backend,
            kit_root=_kit_root(),
            running=running,
            apply_docs=apply_docs,
            release_json=release_json,
            cleanup_inputs=not keep_inputs,
        )
    except UpgradeRefused as exc:
        _emit(f"upgrade: REFUSED — {exc}")
        return 2
    for line in lines:
        _emit(f"upgrade: {line}")
    return 0


def cmd_contextpack(target: Path, index: Path | None) -> int:
    """Generate agent context packs from the project index (or a manifest)."""
    assert_safe_target(target, _kit_root())
    config = load_config(target)
    index_path = index if index is not None else target / "project.index.json"
    if not index_path.exists():
        _emit(f"contextpack: no index at {index_path} (run adopt first).")
        return 1
    try:
        areas = load_pack_index(index_path)
    except ValueError as exc:
        _emit(f"contextpack: {exc}")
        return 2
    if not areas:
        _emit("contextpack: index has no areas — nothing to generate.")
        return 0
    for path in generate_packs(target, config, areas):
        rel = path.relative_to(target) if path.is_relative_to(target) else path
        _emit(f"contextpack: wrote {rel}")
    return 0


def cmd_session_start(target: Path) -> int:
    """Print this session's orientation injection (the SessionStart composition).

    Also records the session-start evidence anchor (fail-open) — the same
    baseline the SessionStart hook records, so a session driven by the CLI
    instead of the hook still gets an evidence-backed auto-draft at close —
    and regenerates the repo-root ``HANDOFF.md`` pointer (the B1 run-6
    delivery-gap fix), exactly as the hook does.
    """
    loaded = _require_state(target, "session-start")
    if loaded is None:
        return 1
    config, backend = loaded
    _emit(compose_orientation(target, config, backend))
    record_session_anchor(target, config, backend)
    note = write_handoff_pointer(target, config)
    if note:
        _emit(f"session-start: {note}")
    return 0


def cmd_session_close(target: Path) -> int:
    """Run the session-close ritual: draft, mine, index, advise, report KPIs.

    First auto-drafts the session card's close-out from evidence (KL-5 —
    ``ensure_draft``; fail-open), then mines the session logs into the
    reflection buffer, rebuilds the episodic index, harvests the
    ``📊 Model:`` line into the PL-004 model-usage feed
    (``telemetry/model-usage.jsonl`` — one row per session, KL-3; a drafted
    ``[[fill:]]`` stand-in line is never harvested), prints the stop-check
    advisories, and ends with the KPI footer — the engine analog of the
    one-idea / previous-session-review enders.
    """
    loaded = _require_state(target, "session-close")
    if loaded is None:
        return 1
    config, backend0 = loaded
    # KL-5 mechanized write-back: draft the card/close-out from evidence
    # BEFORE the ritual runs, so mining/advisories see the drafted state and
    # a session that wrote nothing still leaves an evidence-backed draft.
    for line in ensure_draft(target, config, backend0):
        _emit(f"session-close: [draft] {line}")
    rc = cmd_reflect(target, add=None, evidence="", tags="", mine=True)
    if rc != 0:
        return rc
    index_path = target / config.state_dir / EPISODIC_INDEX_FILENAME
    entries = rebuild_episodic_index(target / config.sessions_dir, index_path)
    _emit(f"session-close: indexed {len(entries)} session(s).")
    log = latest_session_log(target / config.sessions_dir)
    for line in harvest_model_usage(target, log):
        _emit(f"session-close: {line}")
    # Whole-tree reconcile (KL-3 write-at-commit, gen-2 queue item 6): the
    # single-latest harvest above only ever wrote the newest card's row, so a
    # card committed under a newer one was never harvested (10 rows vs 42
    # eligible cards). Sweep every complete card so no eligible card is left
    # behind — idempotent + fail-open, so it costs a re-scan and nothing else.
    for line in reconcile_model_usage(target, target / config.sessions_dir):
        _emit(f"session-close: {line}")
    # Re-read state: the mine above stamped reflection_buffer.last_mined, and
    # a pre-mine snapshot would re-advise the mine it just ran.
    backend = JsonStateBackend(_state_path(target, config))
    for line in evaluate_stop(target, config, backend):
        _emit(f"session-close: [advisory] {line}")
    # §9.1: filing friction issues rides session-close, best-effort — the
    # engine cannot reach GitHub, so it advises the session/agent instead.
    pending = list_outbox(target, config.state_dir)
    if pending:
        _emit(
            f"session-close: [advisory] {len(pending)} friction report(s) "
            f"pending in {config.state_dir}/friction-outbox/ — file each as "
            f"a `{FRICTION_LABEL}`-labeled issue on the kit repo "
            "(`friction show <name>` prints the issue title+body), then "
            "delete the drained file.",
        )
    kpis = workflow_kpis(backend.data, target / config.sessions_dir)
    _emit(kpi_footer(kpis))
    return 0


def cmd_draft(target: Path) -> int:
    """Auto-draft the session card / close-out from evidence, on demand.

    The same seam ``session-close`` and the Stop hook run (KL-5): a missing
    card gets a drafted skeleton, an in-progress card missing its close-out
    gets the drafted section appended, a drafted card reports its unresolved
    ``[[fill:]]`` slots, and a completed card is never touched.
    """
    loaded = _require_state(target, "draft")
    if loaded is None:
        return 1
    config, backend = loaded
    lines = ensure_draft(target, config, backend)
    if not lines:
        _emit("draft: nothing to do (card complete, or close-out already present).")
        return 0
    for line in lines:
        _emit(f"draft: {line}")
    return 0


def cmd_archive_prep(target: Path) -> int:
    """Draft / report the archive-ready close-out note (plan §5 S2).

    The KL-5 evidence-draft seam pointed at the archive ritual
    (``docs/operations/archive-ready-close-out.md``): a missing note gets a
    drafted ``docs/retro/archive-ready-<date>.md`` with evidence pre-fills, a
    drafted note reports its unresolved ``[[fill:]]`` slots, and a completed
    note is never touched. Separate verb by design (plan §4.1): the archive
    ritual is rare and produces a ``docs/retro/`` note, not a card close-out —
    a ``session-close --archive`` flag would fork that function's contract.
    """
    loaded = _require_state(target, "archive-prep")
    if loaded is None:
        return 1
    config, _ = loaded
    for line in ensure_archive_draft(target, config):
        _emit(f"archive-prep: {line}")
    return 0


def cmd_friction(
    target: Path,
    action: str,
    *,
    repo: str | None,
    name: str | None,
) -> int:
    """Drive the §9.1 friction-report protocol's consumer half.

    ``export`` collects the ⚑ friction records (reflection buffer + a full
    session-log scan), wraps them in the wire envelope, writes it to
    ``<state_dir>/friction-outbox/``, and prints the issue-ready title +
    body — **the engine never files the issue itself** (stdlib-only, no
    credentials): the session/agent files it on the kit repo with the
    ``friction`` label and deletes the drained outbox file. ``list`` shows
    pending outbox envelopes; ``show <name>`` re-prints one's issue text
    (how a later session drains an outbox held by a network/credential
    failure).
    """
    loaded = _require_state(target, "friction")
    if loaded is None:
        return 1
    config, _ = loaded
    if action == "list":
        pending = list_outbox(target, config.state_dir)
        for path in pending:
            envelope = load_envelope(path) or {}
            count = len(envelope.get("reports") or [])
            _emit(f"  {path.name} — {count} report(s), repo {envelope.get('repo')!r}")
        _emit(f"friction: {len(pending)} pending outbox envelope(s).")
        return 0
    if action == "show":
        if not name:
            _emit("friction: show needs the outbox file name (see `friction list`).")
            return 2
        path = target / config.state_dir / "friction-outbox" / name
        envelope = load_envelope(path)
        if envelope is None:
            _emit(f"friction: no readable envelope at {path}.")
            return 1
        _emit(f"title: {friction_issue_title(envelope)}")
        _emit("")
        _emit(friction_issue_body(envelope))
        return 0
    if action != "export":
        _emit(f"friction: unknown action {action!r} (export | list | show).")
        return 2
    reports = friction_reports(target, config)
    if not reports:
        _emit("friction: no \N{BLACK FLAG} friction records found — nothing to export.")
        return 0
    repo_name = repo or detect_repo(target)
    if not repo_name:
        _emit(
            "friction: could not detect the GitHub repo from .git/config — "
            "pass --repo <owner/name>.",
        )
        return 2
    envelope = build_envelope(
        repo=repo_name,
        project_id=str(config.project_id),
        # The honest install record — "" (rendered "unrecorded") when the
        # install predates version recording; never guessed from KIT_VERSION.
        kit_version=config.kit_version or "",
        reports=reports,
    )
    path = write_outbox(target, config.state_dir, envelope)
    rel = path.relative_to(target) if path.is_relative_to(target) else path
    _emit(f"friction: wrote {rel} ({len(reports)} report(s)).")
    _emit(
        f"friction: now file it — open a `{FRICTION_LABEL}`-labeled issue on "
        "the kit repo with the title+body below, then delete the outbox file.",
    )
    _emit("")
    _emit(f"title: {friction_issue_title(envelope)}")
    _emit("")
    _emit(friction_issue_body(envelope))
    return 0


def cmd_ledger(
    target: Path,
    *,
    title: str,
    verdict: str,
    why: str,
    provenance: str,
    supersedes: str | None,
) -> int:
    """Append a decision to the [D-NNNN] ledger (created on first use)."""
    assert_safe_target(target, _kit_root())
    config = load_config(target)
    path = target / config.docs_root / LEDGER_FILENAME
    entry = append_decision(
        path,
        title=title,
        verdict=verdict,
        why=why,
        provenance=provenance,
        supersedes=supersedes,
    )
    _emit(f"ledger: recorded {entry['id']} — {title}")
    if supersedes:
        _emit(f"ledger: {supersedes} stamped superseded-by {entry['id']}.")
    return 0


def _simulate_mode_asserts(
    mode: str,
    data: dict,
    graduated: bool,
    n: int,
) -> str | None:
    """Return the per-mode behavior violation, or None when behavior held.

    The behavior-assert half of the simulation: observe must never
    auto-graduate (it proposes), guided/active must graduate once the quiet
    streak is long enough.
    """
    quiet_needed = 3
    if mode == "observe":
        if graduated or data.get("stage") != "integration":
            return "observe mode auto-graduated (must only propose)"
        if n > quiet_needed and not data.get("graduation_proposed"):
            return "observe mode never proposed graduation"
        return None
    if n > quiet_needed and not graduated:
        return f"{mode} mode failed to graduate after the quiet streak"
    return None


def cmd_simulate(n: int, mode: str = "guided") -> int:
    """Init into a temp dir and drive ``n`` interview sessions; verify behavior.

    Session 1 supplies confirmed answers for every critical slot; later sessions
    supply none. Asserts the critical slots fill and that the run behaves
    per ``mode``: guided/active graduate integration -> steady once quiet;
    observe only ever *proposes* graduation.
    """
    with tempfile.TemporaryDirectory(prefix="substrate-sim-") as tmp:
        target = Path(tmp)
        rc = cmd_init(target)
        if rc != 0:
            return rc
        state_path = _state_path(target, load_config(target))
        if mode != "guided":
            rc = cmd_mode(target, mode)
            if rc != 0:
                return rc
        crit = critical_slots()
        answers = {slot: f"value-for-{slot}" for slot in crit}
        graduated = False
        for index in range(n):
            backend = JsonStateBackend(state_path)
            result = run_session(backend, answers if index == 0 else {})
            graduated = graduated or result["graduated"]
        data = JsonStateBackend(state_path).data
        missing = [s for s in crit if data.get("slots", {}).get(s) != "filled"]
        if missing:
            _emit(f"simulate: FAILED — critical slots unfilled: {missing}")
            return 1
        violation = _simulate_mode_asserts(mode, data, graduated, n)
        if violation:
            _emit(f"simulate: FAILED — {violation}")
            return 1
        _emit(
            f"simulate: OK — {n} session(s), {len(crit)} critical slots filled, "
            f"mode={mode}, stage={data.get('stage')} (graduated={graduated}).",
        )
    return 0


def cmd_currency(
    target: Path,
    *,
    roster_file: Path | None = None,
    dry_run: bool = False,
    check: bool = False,
    fetcher: Any = None,
) -> int:
    """Regenerate ``docs/adopters.md`` from live fleet evidence (EAP §6.3).

    Agent-side by design (the execution-home split): this command fetches
    each rostered repo's committed tree read-only (vendored bootstrap header
    + config pin + heartbeat ``kit:`` line) over raw content, rewrites the
    generated registry, and prints the version-spread + drift report. Kit CI
    never runs this — it cannot auth to sibling repos; CI only validates the
    committed file's format (``check_adopters_current``). ``fetcher`` is the
    injectable seam the tests use; drift is surfaced, never resolved.

    ``check=True`` is the registry-delta preflight (idea
    ``docs/ideas/currency-check-registry-delta-preflight-2026-07-15.md``):
    same read-only scan, but instead of writing it compares the would-be
    registry against the committed one **rows only** (the ``Generated:``
    stamp never counts; network-dark repos never count) and exits 0 (current)
    / 1 (a regen would change rows — the changed rows are printed). Any
    session or wrapper can now answer "is a currency slice due?" from a
    plain exit code instead of hand-eyeballing adopter ``kit:`` lines.
    """
    roster_path = roster_file or (target / ROSTER_RELPATH)
    if not roster_path.is_file():
        _emit(f"currency: no roster at {roster_path} — nothing to scan.")
        return 1
    roster = parse_roster(roster_path.read_text(encoding="utf-8"))
    if not roster:
        _emit(f"currency: roster {roster_path} lists no repos.")
        return 1
    fetch = fetcher or default_fetcher()
    scans = scan_fleet(roster, fetch)
    text = render_adopters(scans, KIT_VERSION)
    out_path = target / ADOPTERS_RELPATH
    if check:
        return _currency_check(out_path, scans)
    if dry_run:
        _emit(f"currency: dry run — would write {out_path}.")
    else:
        atomic_write_text(out_path, text)
        _emit(f"currency: wrote {out_path} ({len(scans)} repo(s) scanned).")
    for line in drift_report_lines(scans, KIT_VERSION):
        _emit(f"  {line}")
    unreadable = [scan.repo for scan in scans if scan.unreadable]
    if unreadable:
        _emit(
            f"currency: UNREADABLE {len(unreadable)} repo(s): "
            + ", ".join(unreadable)
            + " — no transport could read their trees; their rows say"
            " 'unreadable' (adoption UNKNOWN, never 'not adopted')."
            " Fix transport/auth (GITHUB_TOKEN/GH_TOKEN?) and rerun.",
        )
    drifting = [scan.repo for scan in scans if scan.drifts()]
    if drifting:
        _emit(
            f"currency: DRIFT in {len(drifting)} repo(s): "
            + ", ".join(drifting)
            + " — tree vs self-report disagree; reconcile at the source.",
        )
    else:
        _emit("currency: no drift — every self-report matches its tree.")
    return 0


def _currency_check(out_path: Path, scans: list[Any]) -> int:
    """The ``currency --check`` lane: rows-only delta, exit code, no write."""
    if not out_path.is_file():
        _emit(
            f"currency --check: STALE — no committed registry at {out_path};"
            f" run `{REGEN_COMMAND}` to generate it.",
        )
        return 1
    dark = [scan.repo for scan in scans if scan.unreadable]
    if dark:
        _emit(
            f"currency --check: {len(dark)} repo(s) dark this run"
            " (excluded from the compare — transport darkness is never"
            " delta): " + ", ".join(dark),
        )
    delta = registry_delta(
        out_path.read_text(encoding="utf-8"),
        scans,
        KIT_VERSION,
    )
    if delta:
        repos = {line[2:].split(" | ", 1)[0] for line in delta}
        _emit(
            f"currency --check: STALE — a regen would change"
            f" {len(repos)} row(s):",
        )
        for line in delta:
            _emit(f"  {line}")
        _emit(f"currency --check: run `{REGEN_COMMAND}` to regenerate.")
        return 1
    _emit(
        f"currency --check: current — committed registry matches the fresh"
        f" scan ({len(scans)} repo(s), rows-only compare;"
        " Generated: stamp ignored).",
    )
    return 0


def cmd_seat_digest(target: Path, *, venues: list[str] | None = None) -> int:
    """Regenerate the planted ``docs/seat-digest.md`` (grounded-skills slice 6).

    The on-demand arm of the derived-render contract (adopt plants it,
    upgrade refreshes it, this regenerates it whenever the sources moved —
    the fix ``check_seat_digest``'s stale advisory names). ``venues``
    overrides the walls-digest venue filter; without it, the committed
    doc's own ``venues=`` marker is preserved (a regen never silently
    resets a seat's venue choice), falling back to the Project-seat
    default. The write re-records the planted-doc hash when an install
    exists (so upgrade keeps recognizing the file as kit-written); like the
    guard-fire log, it never CREATES state in an uninitialized tree.
    """
    config = load_config(target)
    rel = seat_digest_relpath(config)
    path = target / rel
    if venues:
        venue_tuple = tuple(venues)
    elif path.is_file():
        venue_tuple = walls_digest_venues(path.read_text(encoding="utf-8"))
    else:
        venue_tuple = SEAT_DIGEST_DEFAULT_VENUES
    backend = JsonStateBackend(_state_path(target, config))
    context = build_context(backend.data) if backend.data else {}
    text = seat_digest_text(target, config, context, venues=venue_tuple)
    atomic_write_text(path, text)
    if backend.data:
        record_doc_hash(backend, rel, text)
    _emit(
        f"seat-digest: wrote {rel} "
        f"(walls venues: {', '.join(venue_tuple)}; derived render — the "
        "sources stay the skill index + the capability ledger).",
    )
    return 0


def cmd_heartbeat(
    target: Path,
    *,
    full: bool = False,
    dry_run: bool = False,
    status_file: str | None = None,
    fields: dict[str, str] | None = None,
    kit_version: str | None = None,
    kit_check: str | None = None,
    kit_engaged: str | None = None,
) -> int:
    """Write/refresh the control heartbeat mechanically (ORDER 019 item 7).

    The ``bootstrap heartbeat`` verb — the idea file's mechanical LAST step
    (``docs/ideas/heartbeat-verb-2026-07-09.md``). Default lane: a
    non-destructive **restamp** of the existing heartbeat file — a fresh,
    always-parseable UTC ``updated:`` stamp plus only the field lines the
    caller passed; everything else survives byte-identical
    (:func:`engine.heartbeat.restamp_status`). ``--full``: the whole-file
    contract-shape write for the first real heartbeat over the adopt seed.
    ``--dry-run`` prints the would-be diff (or full text for a new file)
    and writes nothing. Refuses outside a control-carrying host, and on a
    missing/unparseable heartbeat names the fix instead of guessing.
    """
    config = load_config(target)
    relpaths = heartbeat_relpaths(config.heartbeat_files)
    bus_files = [INBOX_RELPATH, CONTROL_README_RELPATH, *relpaths]
    if not any((target / rel).is_file() for rel in bus_files):
        _emit(
            "heartbeat: refused — no control/ bus here (no inbox, README, "
            "or heartbeat file); this verb writes a control-protocol "
            "heartbeat only."
        )
        return 2
    rel = status_file or relpaths[0]
    path = target / rel
    fields = dict(fields or {})
    old_text: str | None = None
    if path.is_file():
        try:
            old_text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            _emit(f"heartbeat: cannot read {rel} ({exc}) — fix the file first.")
            return 2
    if full:
        phase = fields.pop("phase", None)
        if not phase:
            _emit(
                "heartbeat: --full needs --phase — what the seat is doing "
                "is the one field with no honest default."
            )
            return 2
        backend = JsonStateBackend(_state_path(target, config))
        context = build_context(backend.data) if backend.data else {}
        project_name = context.get("project_name") or target.resolve().name
        new_text = full_status(
            project_name,
            kit_version or KIT_VERSION,
            phase=phase,
            kit_check=kit_check or "green",
            kit_engaged=kit_engaged or "yes",
            **fields,
        )
        touched = "whole contract shape (--full)"
    else:
        if kit_check is not None or kit_engaged is not None:
            _emit(
                "heartbeat: --kit-check/--kit-engaged shape the --full "
                "contract render only — the restamp lane preserves the "
                "existing kit: line (version token via --kit-version)."
            )
            return 2
        if old_text is None:
            _emit(
                f"heartbeat: {rel} not found — write the first heartbeat "
                "with --full (or point --status-file at your lane's file)."
            )
            return 2
        try:
            new_text = restamp_status(
                old_text,
                fields=fields,
                kit_version=kit_version,
            )
        except HeartbeatError as exc:
            _emit(f"heartbeat: refused — {exc}")
            return 2
        parts = ["updated:", *sorted(fields)]
        if kit_version is not None:
            parts.append(f"kit: v{kit_version}")
        touched = ", ".join(parts)
    if dry_run:
        if old_text is not None:
            diff = difflib.unified_diff(
                old_text.splitlines(keepends=True),
                new_text.splitlines(keepends=True),
                fromfile=f"a/{rel}",
                tofile=f"b/{rel}",
            )
            _emit("".join(diff).rstrip("\n"))
        else:
            _emit(new_text.rstrip("\n"))
        _emit(f"heartbeat: DRY RUN — {rel} not written.")
        return 0
    atomic_write_text(path, new_text)
    _emit(
        f"heartbeat: wrote {rel} ({touched}) — stamp parseable by "
        "check_status_current (round-trip verified)."
    )
    return 0


def cmd_claim(
    target: Path,
    slug: str,
    *,
    scope: str | None = None,
    area: str | None = None,
    order: str | None = None,
    force: bool = False,
    delete: bool = False,
    dry_run: bool = False,
) -> int:
    """Write/delete a grammar-valid work claim mechanically (#358 💡 ender).

    The ``bootstrap claim`` verb — the one-file-per-claim convention's
    mechanical writer (``control/claims/README.md``, EAP §6.4). Default
    lane: render + write ``<claims_dir>/claude-<slug>.md`` with ONE bullet
    the ``check_claims`` enforcer is guaranteed to parse
    (:func:`engine.claim.render_claim` — same grammar constants, round-trip
    verified, current UTC date last on the line). ``--order NNN`` renders
    the structured inbox-ORDER segment AND refuses to write when another
    live claim on a DIFFERENT branch already names that order — the
    #362/#363 twin-build guard; ``--force`` overrides for a deliberate
    one-order-two-branch split. ``--delete`` removes YOUR OWN claim at
    session close. Both lanes refuse a FOREIGN claim at the target path —
    an existing file whose bullet token is not this slug's
    ``claude/<slug>`` branch (or that the grammar cannot parse, so ownership
    is unprovable) — leaving the file intact. ``--dry-run`` prints the
    would-be content (or the would-be deletion) and touches nothing.
    Refuses outside a control-carrying host, like the heartbeat verb.
    """
    config = load_config(target)
    relpaths = heartbeat_relpaths(config.heartbeat_files)
    bus_files = [INBOX_RELPATH, CONTROL_README_RELPATH, *relpaths]
    has_bus = any((target / rel).is_file() for rel in bus_files)
    if not has_bus and not (target / config.claims_dir).is_dir():
        _emit(
            "claim: refused — no control/ bus here (no inbox, README, "
            "heartbeat file, or claims dir); this verb writes the control "
            "protocol's work claims only."
        )
        return 2
    try:
        branch = branch_for(slug)
        rel = f"{config.claims_dir}/{claim_filename(slug)}"
    except ClaimError as exc:
        _emit(f"claim: refused — {exc}")
        return 2
    path = target / rel
    old_text: str | None = None
    if path.is_file():
        try:
            old_text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            _emit(f"claim: cannot read {rel} ({exc}) — fix the file first.")
            return 2
    if old_text is not None:
        token = owner_token(old_text)
        if token != branch:
            whose = f"`{token}`" if token else "an unparseable bullet (ownership unprovable)"
            _emit(
                f"claim: refused — {rel} exists and belongs to {whose}, not "
                f"`{branch}`; a session only "
                f"{'deletes' if delete else 'overwrites'} its OWN claim "
                "(control/claims/README.md — the loser of a collision "
                "stands down; reconcile by hand). File left intact."
            )
            return 2
    if delete:
        if old_text is None:
            _emit(f"claim: {rel} not found — nothing to delete.")
            return 2
        if dry_run:
            _emit(f"claim: DRY RUN — would delete {rel} (own claim, `{branch}`).")
            return 0
        path.unlink()
        _emit(f"claim: deleted {rel} (own claim, `{branch}` — session close).")
        return 0
    if scope is None:
        _emit(
            "claim: --scope is required to write a claim (one line: what "
            "this session is building) — or use --delete at session close."
        )
        return 2
    try:
        new_text = render_claim(slug, scope, area=area, order=order)
        norm_order = normalize_order(order) if order is not None else None
    except ClaimError as exc:
        _emit(f"claim: refused — {exc}")
        return 2
    if norm_order is not None:
        # The cross-branch ORDER-collision guard (the #362/#363 twin-build):
        # scan every dir check_claims scans for a LIVE claim on a DIFFERENT
        # branch naming this order. Same parsing home (engine.claim /
        # engine.grammar) as the enforcer, so verb and checker cannot
        # disagree about what "names this order" means.
        holders: list[str] = []
        for dir_rel, _is_legacy in claim_scan_dirs(target, config.claims_dir):
            for other in sorted((target / dir_rel).glob("*.md")):
                other_rel = f"{dir_rel}/{other.name}"
                if other.name == "README.md" or other_rel == rel:
                    continue
                try:
                    other_text = other.read_text(encoding="utf-8")
                except (OSError, UnicodeDecodeError):
                    continue  # fail open — unreadable is not a verdict
                other_token = owner_token(other_text)
                if other_token is None or other_token == branch:
                    continue
                if norm_order in claim_order_ids(other_text):
                    holders.append(f"{other_rel} (`{other_token}`)")
        if holders and not force:
            _emit(
                f"claim: refused — order {norm_order} already has a live "
                f"claim on a different branch: {', '.join(holders)}. Two "
                "branches serving one ORDER is the #362/#363 twin-build; "
                "coordinate with the claim holder (or pass --force for a "
                "deliberate split of the order across branches). "
                "Nothing written."
            )
            return 2
        if holders:
            _emit(
                f"claim: --force override — order {norm_order} is also "
                f"claimed by {', '.join(holders)}; proceeding as a "
                "deliberate cross-branch split (check_claims will keep "
                "flagging the overlap as claims-order-collision)."
            )
    if dry_run:
        _emit(new_text.rstrip("\n"))
        _emit(f"claim: DRY RUN — {rel} not written.")
        return 0
    path.parent.mkdir(parents=True, exist_ok=True)
    atomic_write_text(path, new_text)
    refreshed = " (refreshed own claim)" if old_text is not None else ""
    _emit(
        f"claim: wrote {rel}{refreshed} — bullet parseable by check_claims "
        "(round-trip verified). Delete it at session close: "
        f"bootstrap claim {slug} --delete."
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    """Construct the bootstrap argument parser."""
    parser = argparse.ArgumentParser(prog="bootstrap", description="substrate-kit")
    parser.add_argument(
        "--version",
        action="version",
        version=f"substrate-kit {KIT_VERSION}",
        help="print the kit version and exit",
    )
    parser.add_argument(
        "--simulate",
        type=int,
        metavar="N",
        help="run N synthetic sessions in a temp dir, then exit",
    )
    parser.add_argument(
        "--mode",
        default="guided",
        choices=("observe", "guided", "active"),
        help="integration mode for --simulate (behavior asserts differ per mode)",
    )
    sub = parser.add_subparsers(dest="command")
    for name, helptext in (
        ("init", "initialise a project"),
        ("status", "show install state"),
        ("ask", "list pending interview questions"),
        ("triggers", "scan for fired triggers / mandatory questions"),
        ("metrics", "emit the router + workflow KPIs"),
        ("session-start", "print this session's orientation injection"),
        ("session-close", "draft the close-out, mine reflections, report KPIs"),
        ("draft", "auto-draft the session card / close-out from evidence"),
        ("archive-prep", "draft the archive-ready close-out note from evidence"),
    ):
        child = sub.add_parser(name, help=helptext)
        child.add_argument("--target", type=Path, default=Path.cwd())
    adopt_p = sub.add_parser("adopt", help="plant the workflow docs + stage the packs")
    adopt_p.add_argument(
        "--include-claude",
        action="store_true",
        help="also write .claude/CLAUDE.md + .claude/settings.json (skip-if-exists)",
    )
    adopt_p.add_argument(
        "--wire-enforcement",
        action="store_true",
        help=(
            "turn on the forcing functions: the live nag hook (implies "
            "--include-claude) + a live CI gate that holds the merge red until "
            "the session journal is written"
        ),
    )
    adopt_p.add_argument(
        "--lane",
        metavar="NAME",
        default=None,
        help=(
            "adopt as a named lane in a SHARED multi-Project repo: plant "
            "control/status-NAME.md as this Project's heartbeat (declared in "
            "heartbeat_files) and share the rest of the control/ bus"
        ),
    )
    adopt_p.add_argument("--target", type=Path, default=Path.cwd())
    upgrade_p = sub.add_parser(
        "upgrade",
        help="upgrade the install to this bootstrap's version (archives first)",
    )
    upgrade_p.add_argument(
        "--apply-docs",
        action="store_true",
        help="re-render template-improved docs the consumer never edited",
    )
    upgrade_p.add_argument(
        "--rollback",
        action="store_true",
        help="restore the state + dist banked by the last upgrade",
    )
    upgrade_p.add_argument(
        "--release-json",
        type=Path,
        default=None,
        help="release.json to verify this file's sha256 against "
        "(default: one next to the running file, when present)",
    )
    upgrade_p.add_argument(
        "--keep-inputs",
        action="store_true",
        help="keep bootstrap.py.new + its release.json after a completed "
        "upgrade (default: the consumed inputs are removed)",
    )
    upgrade_p.add_argument("--target", type=Path, default=Path.cwd())
    contextpack = sub.add_parser(
        "contextpack",
        help="generate agent context packs from the index",
    )
    contextpack.add_argument(
        "--index",
        type=Path,
        default=None,
        help="index or manifest path (default: <target>/project.index.json)",
    )
    contextpack.add_argument("--target", type=Path, default=Path.cwd())
    render_p = sub.add_parser("render", help="render content docs from filled slots")
    render_p.add_argument(
        "--live",
        action="store_true",
        help="fill remaining placeholders in the PLANTED docs in place",
    )
    render_p.add_argument("--target", type=Path, default=Path.cwd())
    answer = sub.add_parser("answer", help="record a user answer for a slot")
    answer.add_argument("slot")
    answer.add_argument("value", nargs="+", help="the answer text")
    answer.add_argument("--target", type=Path, default=Path.cwd())
    confirm = sub.add_parser("confirm", help="confirm a provisional slot")
    confirm.add_argument("slot")
    confirm.add_argument("--target", type=Path, default=Path.cwd())
    reflect = sub.add_parser("reflect", help="list/add/mine the reflection buffer")
    reflect.add_argument("--add", metavar="LESSON", default=None)
    reflect.add_argument("--evidence", default="")
    reflect.add_argument("--tags", default="", help="comma-separated tags")
    reflect.add_argument("--mine", action="store_true")
    reflect.add_argument("--target", type=Path, default=Path.cwd())
    episodes = sub.add_parser("episodes", help="rebuild/search the episodic index")
    episodes.add_argument("--rebuild", action="store_true")
    episodes.add_argument("--search", metavar="TAG", default=None)
    episodes.add_argument("--target", type=Path, default=Path.cwd())
    maintain = sub.add_parser("maintain", help="run the self-maintenance report")
    maintain.add_argument("--compact", action="store_true")
    maintain.add_argument("--target", type=Path, default=Path.cwd())
    review = sub.add_parser("review", help="drive the independent-review seam")
    review.add_argument("action", choices=("build", "confirm", "doc"))
    review.add_argument("slot", nargs="?", default=None)
    review.add_argument("--verdict", default="", help="pass | fail (for confirm)")
    review.add_argument("--reviewer", default="external")
    review.add_argument("--target", type=Path, default=Path.cwd())
    economy = sub.add_parser("economy", help="run the context-economy engine")
    economy.add_argument(
        "action",
        choices=("check", "apply", "simulate", "recipe", "issue-body"),
    )
    economy.add_argument("--strict", action="store_true")
    economy.add_argument("--yes", action="store_true", help="really act (apply)")
    economy.add_argument(
        "--reviewed",
        action="store_true",
        help="acknowledge the human review a 'gated' maturity first prune needs",
    )
    economy.add_argument("--bands", type=int, default=24)
    economy.add_argument("--target", type=Path, default=Path.cwd())
    friction = sub.add_parser(
        "friction",
        help="export/list/show §9.1 friction-report envelopes (outbox)",
    )
    friction.add_argument("action", choices=("export", "list", "show"))
    friction.add_argument(
        "name",
        nargs="?",
        default=None,
        help="outbox file name (for show)",
    )
    friction.add_argument(
        "--repo",
        default=None,
        help="this consumer's GitHub owner/name (default: parsed from .git/config)",
    )
    friction.add_argument("--target", type=Path, default=Path.cwd())
    ledger = sub.add_parser("ledger", help="append a [D-NNNN] decision")
    ledger.add_argument("--title", required=True)
    ledger.add_argument("--verdict", required=True)
    ledger.add_argument("--why", required=True)
    ledger.add_argument("--provenance", required=True)
    ledger.add_argument("--supersedes", default=None)
    ledger.add_argument("--target", type=Path, default=Path.cwd())
    mode = sub.add_parser("mode", help="set the integration mode")
    mode.add_argument("name")
    mode.add_argument("--target", type=Path, default=Path.cwd())
    stance = sub.add_parser("stance", help="show or set the task stance")
    stance.add_argument("name", nargs="?", default=None)
    stance.add_argument("--target", type=Path, default=Path.cwd())
    skills = sub.add_parser("skills", help="list or --build the skill pack")
    skills.add_argument(
        "--build",
        action="store_true",
        help="emit SKILL.md files into <state_dir>/skills/",
    )
    skills.add_argument("--target", type=Path, default=Path.cwd())
    agents = sub.add_parser("agents", help="list or --build the persona pack")
    agents.add_argument(
        "--build",
        action="store_true",
        help="emit agent .md files into <state_dir>/agents/",
    )
    agents.add_argument("--target", type=Path, default=Path.cwd())
    hooks = sub.add_parser("hooks", help="show or --build the hook wiring")
    hooks.add_argument(
        "--build",
        action="store_true",
        help="emit the PreToolUse settings snippet into <state_dir>/hooks/",
    )
    hooks.add_argument("--target", type=Path, default=Path.cwd())
    hook = sub.add_parser("hook", help="run a hook check (e.g. `hook pretooluse`)")
    hook.add_argument("event")
    hook.add_argument("--target", type=Path, default=Path.cwd())
    currency = sub.add_parser(
        "currency",
        help=(
            "regenerate docs/adopters.md from live fleet evidence "
            "(agent-side: fetches sibling repos read-only; CI only "
            "format-checks the committed output)"
        ),
    )
    currency.add_argument("--target", type=Path, default=Path.cwd())
    currency.add_argument(
        "--roster",
        type=Path,
        default=None,
        help=f"fleet roster file (default: <target>/{ROSTER_RELPATH})",
    )
    currency.add_argument(
        "--dry-run",
        action="store_true",
        help="scan + print the drift report without writing docs/adopters.md",
    )
    currency.add_argument(
        "--check",
        action="store_true",
        help=(
            "registry-delta preflight: same read-only scan, no write — "
            "compare against the committed docs/adopters.md rows-only "
            "(Generated: stamp ignored; dark repos never delta) and exit "
            "0 (current) / 1 (a regen would change rows)"
        ),
    )

    seat_digest = sub.add_parser(
        "seat-digest",
        help=(
            "regenerate docs/seat-digest.md — the fence-marked skills + "
            "walls digest blocks fleet-manager's seat-prompt regen "
            "extracts (derived render; never hand-edit)"
        ),
    )
    seat_digest.add_argument("--target", type=Path, default=Path.cwd())
    seat_digest.add_argument(
        "--venue",
        action="append",
        choices=CAPABILITY_VENUE_TOKENS,
        default=None,
        help=(
            "walls-digest venue filter (repeatable). Default: the committed "
            "doc's own venues= marker, else the Project-seat default "
            f"({', '.join(SEAT_DIGEST_DEFAULT_VENUES)})"
        ),
    )

    heartbeat_p = sub.add_parser(
        "heartbeat",
        help=(
            "restamp the control/ status heartbeat mechanically — a fresh "
            "parseable UTC updated: stamp plus only the fields you pass "
            "(everything else preserved byte-identical); --full writes the "
            "whole contract shape (the first real heartbeat)"
        ),
    )
    heartbeat_p.add_argument("--target", type=Path, default=Path.cwd())
    heartbeat_p.add_argument(
        "--status-file",
        default=None,
        help=(
            "heartbeat file to write (default: the first configured "
            "heartbeat_files entry — control/status.md unless a lane "
            "configured otherwise)"
        ),
    )
    heartbeat_p.add_argument(
        "--full",
        action="store_true",
        help=(
            "write the whole contract-shape heartbeat (the adopt seed's "
            "documented overwrite path); requires --phase, other fields "
            "default honestly (blockers/⚑ needs-owner: none)"
        ),
    )
    heartbeat_p.add_argument(
        "--dry-run",
        action="store_true",
        help="print the would-be diff (or full text for a new file) without writing",
    )
    heartbeat_p.add_argument("--phase", default=None, help="phase: line value")
    heartbeat_p.add_argument("--health", default=None, help="health: line value")
    heartbeat_p.add_argument(
        "--orders",
        default=None,
        help='orders: line value (e.g. "acked=001-003 done=001,002")',
    )
    heartbeat_p.add_argument(
        "--last-shipped",
        dest="last_shipped",
        default=None,
        help="last-shipped: line value",
    )
    heartbeat_p.add_argument("--blockers", default=None, help="blockers: line value")
    heartbeat_p.add_argument(
        "--needs-owner",
        dest="needs_owner",
        default=None,
        help="⚑ needs-owner: line value",
    )
    heartbeat_p.add_argument("--notes", default=None, help="notes: line value")
    heartbeat_p.add_argument(
        "--kit-version",
        dest="kit_version",
        default=None,
        help=(
            "rewrite the kit: line's v<X.Y.Z> token (restamp lane keeps "
            "the line's decorations; --full default: this dist's version)"
        ),
    )
    heartbeat_p.add_argument(
        "--kit-check",
        dest="kit_check",
        choices=("green", "red"),
        default=None,
        help="kit: line check: field (--full lane only)",
    )
    heartbeat_p.add_argument(
        "--kit-engaged",
        dest="kit_engaged",
        choices=("yes", "no"),
        default=None,
        help="kit: line engaged: field (--full lane only)",
    )

    claim_p = sub.add_parser(
        "claim",
        help=(
            "write a grammar-valid work claim file (control/claims/"
            "claude-<slug>.md, one bullet check_claims is guaranteed to "
            "parse — branch token · scope · UTC date); --delete removes "
            "your OWN claim at session close, refusing foreign claims"
        ),
    )
    claim_p.add_argument(
        "slug",
        help=(
            "branch slug — the claim's branch is claude/<slug>, its file "
            "claude-<slug>.md under the configured claims_dir"
        ),
    )
    claim_p.add_argument("--target", type=Path, default=Path.cwd())
    claim_p.add_argument(
        "--scope",
        default=None,
        help=(
            "one-line scope (rendered bold) — required to write; dated "
            "filenames in it are safe (the claim's own date is appended "
            "LAST on the bullet, the post-#353 rule)"
        ),
    )
    claim_p.add_argument(
        "--area",
        default=None,
        help='optional expected files/area segment (e.g. "src/ + tests/")',
    )
    claim_p.add_argument(
        "--order",
        default=None,
        metavar="NNN",
        help=(
            "the inbox ORDER this claim serves (e.g. 020) — renders the "
            "structured `order NNN` segment the cross-branch overlap scan "
            "keys on, and refuses to write when another live claim on a "
            "different branch already names that order (the #362/#363 "
            "twin-build guard)"
        ),
    )
    claim_p.add_argument(
        "--force",
        action="store_true",
        help=(
            "override the --order collision refusal for a deliberate split "
            "of one order across branches (check_claims keeps flagging the "
            "overlap as claims-order-collision)"
        ),
    )
    claim_p.add_argument(
        "--delete",
        action="store_true",
        help=(
            "delete your OWN claim file (session close); a foreign claim — "
            "different branch token, or unparseable — is refused intact"
        ),
    )
    claim_p.add_argument(
        "--dry-run",
        action="store_true",
        help="print the would-be claim content (or deletion) without touching disk",
    )

    check = sub.add_parser("check", help="run the doc + session-log hygiene checks")
    check.add_argument("--target", type=Path, default=Path.cwd())
    check.add_argument("--strict", action="store_true", help="exit 1 if any violation")
    check.add_argument(
        "--require-session-log",
        action="store_true",
        help="fail (not just advise) when the session log is missing — the CI gate mode",
    )
    check.add_argument(
        "--session-log",
        type=Path,
        default=None,
        help=(
            "gate on this session card explicitly (e.g. the card the PR's diff "
            "touches) instead of newest-by-mtime; a missing file counts as an "
            "absent log, never a silent fallback"
        ),
    )
    check.add_argument(
        "--added-card",
        type=Path,
        default=None,
        help=(
            "grade this session card as one newly ADDED by the PR (the "
            "gate's added-card lane): an in-progress/drafted card is the "
            "born-red HOLD (red until it flips complete — the "
            "superbot-games #40 loophole fix); a missing Status badge — or "
            "a card that declares itself complete while missing its "
            "markers — reds (the venture-lab #15 false-green class)"
        ),
    )
    check.add_argument(
        "--simulate-added-card",
        type=Path,
        default=None,
        help=(
            "ADVISORY self-test: print what the gate's added-card lane "
            "WOULD do for this card (hold / grammar findings / pass) "
            "without affecting the exit code — makes the lane observable "
            "on the very PR that ships gate changes, where the locked "
            "door supersedes the --added-card path"
        ),
    )
    check.add_argument(
        "--status-only",
        action="store_true",
        help=(
            "run ONLY the control/ status heartbeat checker — the CI control "
            "fast lane's scoped gate: a control-only diff edits exactly the "
            "files this checker validates, so the lane must still prove the "
            "heartbeat parses (stdlib-only, session-log-free)"
        ),
    )
    check.add_argument(
        "--inbox-base",
        type=Path,
        default=None,
        help=(
            "gate control/inbox.md against this merge-base copy of the file "
            "(CI extracts the base blob with git): the change must be "
            "pure-append and its appended text well-formed ORDER blocks; "
            "when omitted, a local run derives the base from origin/main "
            "itself (ORDER 018 local↔CI parity) and self-skips with a NOTE "
            "when no git context is derivable"
        ),
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the bootstrap CLI; return a process exit code."""
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.simulate is not None:
            return cmd_simulate(args.simulate, args.mode)
        if args.command == "init":
            return cmd_init(args.target)
        if args.command == "status":
            return cmd_status(args.target)
        if args.command == "ask":
            return cmd_ask(args.target)
        if args.command == "render":
            return cmd_render(args.target, live=args.live)
        if args.command == "mode":
            return cmd_mode(args.target, args.name)
        if args.command == "stance":
            return cmd_stance(args.target, args.name)
        if args.command == "skills":
            return cmd_skills(args.target, args.build)
        if args.command == "agents":
            return cmd_agents(args.target, args.build)
        if args.command == "hooks":
            return cmd_hooks(args.target, args.build)
        if args.command == "hook":
            return cmd_hook(args.target, args.event)
        if args.command == "currency":
            return cmd_currency(
                args.target,
                roster_file=args.roster,
                dry_run=args.dry_run,
                check=args.check,
            )
        if args.command == "seat-digest":
            return cmd_seat_digest(args.target, venues=args.venue)
        if args.command == "heartbeat":
            fields = {
                name: value
                for name, value in (
                    ("phase", args.phase),
                    ("health", args.health),
                    ("orders", args.orders),
                    ("last_shipped", args.last_shipped),
                    ("blockers", args.blockers),
                    ("needs_owner", args.needs_owner),
                    ("notes", args.notes),
                )
                if value is not None
            }
            return cmd_heartbeat(
                args.target,
                full=args.full,
                dry_run=args.dry_run,
                status_file=args.status_file,
                fields=fields,
                kit_version=args.kit_version,
                kit_check=args.kit_check,
                kit_engaged=args.kit_engaged,
            )
        if args.command == "claim":
            return cmd_claim(
                args.target,
                args.slug,
                scope=args.scope,
                area=args.area,
                order=args.order,
                force=args.force,
                delete=args.delete,
                dry_run=args.dry_run,
            )
        if args.command == "check":
            return cmd_check(
                args.target,
                args.strict,
                require_session_log=args.require_session_log,
                session_log=args.session_log,
                added_card=args.added_card,
                simulate_added_card=args.simulate_added_card,
                status_only=args.status_only,
                inbox_base=args.inbox_base,
            )
        if args.command == "answer":
            return cmd_answer(args.target, args.slot, " ".join(args.value))
        if args.command == "confirm":
            return cmd_confirm(args.target, args.slot)
        if args.command == "triggers":
            return cmd_triggers(args.target)
        if args.command == "reflect":
            return cmd_reflect(
                args.target,
                add=args.add,
                evidence=args.evidence,
                tags=args.tags,
                mine=args.mine,
            )
        if args.command == "episodes":
            return cmd_episodes(args.target, rebuild=args.rebuild, search=args.search)
        if args.command == "metrics":
            return cmd_metrics(args.target)
        if args.command == "maintain":
            return cmd_maintain(args.target, compact=args.compact)
        if args.command == "review":
            return cmd_review(
                args.target,
                args.action,
                args.slot,
                verdict=args.verdict,
                reviewer=args.reviewer,
            )
        if args.command == "economy":
            return cmd_economy(
                args.target,
                args.action,
                strict=args.strict,
                apply=args.yes,
                reviewed=args.reviewed,
                bands=args.bands,
            )
        if args.command == "adopt":
            return cmd_adopt(
                args.target,
                args.include_claude,
                wire_enforcement=args.wire_enforcement,
                lane=args.lane,
            )
        if args.command == "upgrade":
            return cmd_upgrade(
                args.target,
                apply_docs=args.apply_docs,
                rollback=args.rollback,
                release_json=args.release_json,
                keep_inputs=args.keep_inputs,
            )
        if args.command == "contextpack":
            return cmd_contextpack(args.target, args.index)
        if args.command == "session-start":
            return cmd_session_start(args.target)
        if args.command == "session-close":
            return cmd_session_close(args.target)
        if args.command == "draft":
            return cmd_draft(args.target)
        if args.command == "archive-prep":
            return cmd_archive_prep(args.target)
        if args.command == "friction":
            return cmd_friction(
                args.target,
                args.action,
                repo=args.repo,
                name=args.name,
            )
        if args.command == "ledger":
            return cmd_ledger(
                args.target,
                title=args.title,
                verdict=args.verdict,
                why=args.why,
                provenance=args.provenance,
                supersedes=args.supersedes,
            )
    except UnsafeTargetError as exc:
        _emit(f"refused: {exc}")
        return 2
    parser.print_help()
    return 0
