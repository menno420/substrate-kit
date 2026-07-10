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
import json
import sys
import tempfile
from datetime import date
from pathlib import Path
from typing import Any

from engine.adopt import (
    adopt,
    record_doc_hash,
    strip_unrendered_banner,
)
from engine.agents.agents import AGENTS, agent_document, agent_relpath
from engine.checks.allowlist import apply_allowlist, load_allowlist
from engine.checks.check_claims import check_claims
from engine.checks.check_docs import Finding, run_doc_checks
from engine.checks.check_engagement import check_engagement, scan_relpaths
from engine.checks.check_inbox_append import check_inbox_append
from engine.checks.check_namespace import check_namespace
from engine.checks.check_owner_actions import check_owner_actions
from engine.checks.check_status_current import check_status_current
from engine.checks.check_orientation_budget import check_orientation_budget
from engine.checks.check_seam_authority import check_seam_authority
from engine.checks.check_session_log import check_log, latest_session_log
from engine.contextpack import generate_packs, load_pack_index
from engine.economy.engine import economy_actuate, economy_check, issue_body
from engine.economy.harvest import harvest_sources, parse_harvest_tables
from engine.economy.simulator import calibration_recipe, default_calibration, run_search
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
    harvest_model_usage,
    reconcile_model_usage,
    record_guard_fires,
)
from engine.loop.triggers import check_triggers, mandatory_questions, trigger_block
from engine.render import build_context, find_placeholders, load_templates, render
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
    must never be blocked by evidence bookkeeping.
    """
    config = load_config(target)
    backend = JsonStateBackend(_state_path(target, config))
    text = compose_orientation(target, config, backend)
    if text:
        sys.stdout.write(text)
    record_session_anchor(target, config, backend)
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


def cmd_check(
    target: Path,
    strict: bool,
    *,
    require_session_log: bool = False,
    session_log: Path | None = None,
    status_only: bool = False,
    inbox_base: Path | None = None,
) -> int:
    """Run every hygiene checker against ``target``.

    ``inbox_base`` (CLI ``--inbox-base``) names the merge-base version of
    ``control/inbox.md`` — extracted by CI in bash, because engine code never
    shells out to git (§3.2). When given, the append-only gate runs on both
    lanes: the change to ``control/inbox.md`` must be pure-append vs that base
    and its appended text must be well-formed ORDER blocks (issue #36 report
    2). It rides the fast lane exactly like the status gate — an inbox append
    is control-lane traffic — and self-skips when there is nothing to judge.

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
    session log counts. A *missing* session log is **advisory by default** (a
    host may run ``check`` mid-session) but becomes a **hard failure** under
    ``require_session_log`` — the gate mode the live CI workflow runs, so a
    session that never writes its journal cannot merge (the "locked door" that
    makes the memory ritual non-optional, not merely advised). Uses config
    defaults if ``target`` has no ``substrate.config.json`` yet, so a project
    can lint before onboarding.

    ``session_log`` (CLI ``--session-log``) names the card to gate on
    *explicitly* — the diff-aware selection a CI workflow derives from which
    ``<sessions_dir>/*.md`` file the PR adds/changes. Without it the gate
    falls back to newest-by-mtime, which a fresh CI checkout silently degrades
    (every mtime flattens to checkout time), the trap that used to require a
    git-mtime-restore shim before this step. A named file that does not exist
    is treated exactly like an absent log (advisory by default, a hard failure
    under ``require_session_log``) — an explicit selection never silently
    falls back to a different card.

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
    # Order-claim hygiene (ORDER 007): advisory-only, like the staleness and
    # owner-action warnings — a duplicate or stale `claimed-by:` is a
    # coordination race the manager reconciles, never a required-check red.
    # Runs on both lanes: claims live on the heartbeat orders line the fast
    # lane already validates.
    claim_advisories = check_claims(
        target,
        status_files=config.heartbeat_files,
    )
    # The inbox append-only gate (issue #36 report 2): a control/inbox.md
    # change must be pure-append vs the merge-base + ORDER-grammar shaped.
    # Rides the finding loop like every checker; engages only when CI handed
    # in a base blob to diff against (no base → no-op, see the checker).
    inbox_findings = (
        check_inbox_append(target, inbox_base) if inbox_base is not None else []
    )
    if status_only:
        # --status-only: the fast lane's scoped gate (see docstring). Only the
        # control-lane checkers run — the heartbeat gate and, when CI passes a
        # base, the inbox append-only gate; everything downstream (allowlist,
        # guard fires, emit loop) is shared with the full run.
        doc_findings = list(status_gate) + inbox_findings
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
        doc_findings += inbox_findings
    entries, allow_findings = load_allowlist(target, config.state_dir)
    doc_findings, suppressed = apply_allowlist(doc_findings, entries)
    doc_findings += allow_findings
    if suppressed:
        _emit(
            f"check: {len(suppressed)} finding(s) suppressed by allowlist "
            "(reason-carrying entries; fires recorded with their verdicts).",
        )
        for finding, entry in suppressed:
            record_guard_fires(
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
        record_guard_fires(
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
        record_guard_fires(
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
        record_guard_fires(
            target,
            config.state_dir,
            cmd="check",
            surface="check",
            posture="advisory",
            findings=owner_ask_advisories,
        )
    if claim_advisories:
        # Same warn-only contract as the advisories above (ORDER 007): the
        # duplicate/stale-claim nudge is surfaced + telemetry-recorded but
        # never counted toward the exit code — the manager adjudicates the
        # tiebreak; the checker only flags the collision.
        _emit(
            f"check: {len(claim_advisories)} order-claim advisory "
            "warning(s) (never exit-affecting):",
        )
        for finding in claim_advisories:
            _emit(f"  [{finding.kind}] {finding.path}: {finding.message}")
        record_guard_fires(
            target,
            config.state_dir,
            cmd="check",
            surface="check",
            posture="advisory",
            findings=claim_advisories,
        )

    log_missing: list[str] = []
    log_absent_fails = False
    if status_only:
        # The fast lane's scoped gate never touches the session-log seam: a
        # control-only heartbeat PR carries no card by design (the lane's
        # whole point), so gating on one here would deadlock every heartbeat.
        if not doc_findings:
            _emit("check: control-status check passed (--status-only).")
            return 0
        return 1 if strict else 0
    if session_log is not None:
        explicit = session_log if session_log.is_absolute() else target / session_log
        log = explicit if explicit.is_file() else None
    else:
        log = latest_session_log(target / config.sessions_dir)
    log_missing = check_log(log, config.session_markers) if log else []
    # In gate mode an absent log is itself a failing condition, so it must feed
    # the exit code exactly like an incomplete one.
    log_absent_fails = log is None and require_session_log
    if log is None:
        if session_log is not None:
            absent = f"--session-log {session_log} does not exist"
        else:
            absent = f"no session log under {config.sessions_dir}/"
        if require_session_log:
            _emit(
                f"check: MERGE HELD — {absent} "
                "(--require-session-log): write one before merging.",
            )
        else:
            _emit(f"check: {absent} (advisory — not a failure).")
    else:
        rel = log.relative_to(target) if log.is_relative_to(target) else log
        if log_missing:
            _emit(f"check: session log {rel} is missing: {', '.join(log_missing)}")
        else:
            _emit(f"check: session log {rel} complete.")
    if log_missing or log_absent_fails:
        # The session gate is a guard too (the kit's flagship one) — its
        # fires feed B3 like any checker's. Never allowlistable, though.
        if log_absent_fails:
            if session_log is not None:
                absent = f"--session-log {session_log} does not exist"
            else:
                absent = f"no session log under {config.sessions_dir}/"
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
        record_guard_fires(
            target,
            config.state_dir,
            cmd="check",
            surface="check",
            posture="blocking" if (strict or require_session_log) else "advisory",
            findings=[gate_finding],
        )

    if not doc_findings and not log_missing and not log_absent_fails:
        _emit("check: all checks passed.")
        return 0
    return 1 if strict else 0


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
    return 0


def cmd_confirm(target: Path, slot: str) -> int:
    """Confirm a provisional (self-answered) slot as user-verified."""
    loaded = _require_state(target, "confirm")
    if loaded is None:
        return 1
    _, backend = loaded
    if confirm_slot(backend, slot, source="user"):
        _emit(f"confirm: {slot} confirmed (provisional -> filled).")
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
) -> int:
    """Adopt the workflow into ``target``: init, plant the docs, stage the packs.

    The one-step flow: ``init`` runs first (idempotent — config + state), so a
    bare directory with nothing but the bootstrap file becomes a fully
    substrate-governed project in this single command. ``wire_enforcement``
    additionally turns on the live nag hook + the CI locked door.
    """
    rc = cmd_init(target)
    if rc != 0:
        return rc
    config = load_config(target)
    backend = JsonStateBackend(_state_path(target, config))
    lines = adopt(
        target,
        config,
        backend,
        kit_root=_kit_root(),
        include_claude=include_claude,
        wire_enforcement=wire_enforcement,
    )
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
    instead of the hook still gets an evidence-backed auto-draft at close.
    """
    loaded = _require_state(target, "session-start")
    if loaded is None:
        return 1
    config, backend = loaded
    _emit(compose_orientation(target, config, backend))
    record_session_anchor(target, config, backend)
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
            "(CI extracts the base blob with git, since engine code never "
            "shells out): the change must be pure-append and its appended "
            "text well-formed ORDER blocks; omit when there is no inbox diff"
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
        if args.command == "check":
            return cmd_check(
                args.target,
                args.strict,
                require_session_log=args.require_session_log,
                session_log=args.session_log,
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
