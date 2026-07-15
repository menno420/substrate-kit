"""Post-adopt ENGAGEMENT gate — RED until the install is rendered + enforcing + looping.

Why + provenance: the independent fleet review (2026-07-09, superbot
``docs/eap/fleet-review-2026-07-09.md`` §4) found both fresh adopters stranded
identically — planted docs still under the UNRENDERED banner with raw
``${...}`` slots, ``session_count`` 0, no CI running the check. ``adopt``
plants-and-banners by design, but render/enforcement were separate opt-in
steps nothing forced, so a default adopt LOOKED onboarded while being neither
rendered nor enforcing. This checker is the owner-directed fix (band KL-7):
"enforce, don't exhort" (PL-007) applied to onboarding itself — the same
``check --strict`` an adopter's CI runs holds the gate red until the last
mile is walked. Ships with its regression tests (the cold-adopt RED→GREEN
arc), so it is load-bearing from birth, not a PL-008 unverified convenience.

The gate engages only on **adoption evidence** — a recorded ``kit_version``
in config or state (``adopt``/``upgrade`` write it) — so ``check`` stays
meaningful on an un-adopted tree, exactly like the other input-gated
checkers. One exception: a file that still *carries the UNRENDERED banner*
is kit output by construction and is flagged even without version evidence
(pre-v1.0.0 installs never recorded one).

What turns it red (one finding per condition, each message an actionable
checklist line — ``adopt`` prints these same findings as its next steps):

- ``unrendered-banner`` — a planted doc still opens with the adopt-time
  UNRENDERED banner.
- ``unrendered-slot`` — a planted doc still contains ``${...}`` interview
  slots (adoption-evidence-gated: bare ``${name}`` prose in a never-adopted
  repo is host content, not a kit slot).
- ``enforcement-unwired`` — no workflow under ``.github/workflows/`` runs
  ``check --strict`` (the staged ``substrate-gate.yml`` is the one-copy fix).
  A host whose CI door is real but not kit-shaped (the superbot shape —
  friction #37: required code-quality check, born-red merge gate, zero
  ``check --strict`` workflows) opts out of this false positive by declaring
  the door: ``substrate.config.json`` → ``native_gate.workflow`` names the
  workflow file that constitutes it. The declaration counts only while that
  file exists in-tree (PL-011's letter: a door must exist and be visible);
  acceptance is surfaced as an ``enforcement-native`` NOTE by ``check``'s
  full lane (:func:`native_gate_note`) — visible, never silent.
- ``session-loop-idle`` — no session has ever run: ``session_count`` is 0
  AND no real session card exists under the sessions dir.

Beyond the strict gate, two honesty surfaces cover what "wired" alone can't
see (idea engagement-wiring-strength-verification-2026-07-12 — the #38
weak-form class + #36 report 3): :func:`check_enforcement_strength` fires an
**advisory-only** ``enforcement-weak-form`` finding when the wired door runs
the plain form while the staged gate carries the stronger legs, and
:func:`required_unverified_note` NOTEs that required-check status is
owner-UI state the engine cannot read. Neither ever affects the exit code.

Scope: the scan covers exactly the **planted** doc paths (the ``ADOPT_PLAN``
destinations, ``project.index.json``, and a live ``.claude/CLAUDE.md``) —
never template sources, so the kit repo's own ``src/engine/templates/``
(legitimately full of ``${...}``) can never red its own gate. Findings ride
the ordinary ``check`` finding loop: strict-only exit-code impact, guard-fire
telemetry, and the reasons-required allowlist all apply unchanged.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from engine.adopt import ADOPT_PLAN, UNRENDERED_BANNER_FIRST_LINE, _adopt_dest
from engine.checks.check_docs import Finding
from engine.render import find_placeholders, find_placeholders_outside_code

# Planted paths beyond the ADOPT_PLAN doc set that the unrendered scan covers.
# project.index.json is planted by adopt; .claude/CLAUDE.md exists only after
# the include_claude opt-in (scanned when present — a live-but-unrendered
# working agreement is exactly the "looks onboarded, isn't" failure).
EXTRA_SCAN_RELPATHS = ("project.index.json", ".claude/CLAUDE.md")


def _load_state(target: Path, config: Any) -> dict:
    """Read the install's state.json (empty dict when absent/unreadable)."""
    path = target / config.state_dir / "state.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def _adoption_evidence(config: Any, state: dict) -> bool:
    """True when this tree is a known kit install (adopt/upgrade recorded it)."""
    return bool(config.kit_version) or bool(state.get("kit_version"))


def scan_relpaths(config: Any) -> list[str]:
    """Return the planted relpaths the unrendered scan covers.

    Public on purpose: ``render --live`` iterates this SAME list, so the
    render verb and the engagement gate can never disagree about whose job a
    planted file is. The run-2 gap (idea render-live-claude-md-gap-2026-07-09)
    was exactly that disagreement — the gate counted ``.claude/CLAUDE.md``'s
    unrendered banner/slots as strict-RED while the render path skipped the
    file, stranding every fresh adopter mid-checklist.
    """
    relpaths = [
        _adopt_dest(plan_rel, config)
        for _, plan_rel in ADOPT_PLAN
        # Shell plants are excluded from the unrendered/render-live surface
        # (EAP §6.5): shell `${VAR}` syntax is not an interview slot — a
        # host's hand-rolled scripts/env-setup.sh would false-red as
        # `unrendered-slot`, and `render --live` must never rewrite an
        # executable hook. The kit's own env-setup.sh.tmpl is slot-free by
        # contract (a test pins it), so nothing real is skipped.
        if not plan_rel.endswith(".sh")
    ]
    relpaths.extend(EXTRA_SCAN_RELPATHS)
    return relpaths


def _unrendered_findings(
    target: Path,
    config: Any,
    *,
    evidence: bool,
    relpaths: list[str] | None = None,
) -> list[Finding]:
    """Scan the planted docs for the UNRENDERED banner / leftover ``${...}``.

    The ``unrendered-slot`` finding is **code-span-aware** (queued fix 4, the
    #148/#150 incident): planted docs the host maintains — the
    ``control/status.md`` heartbeat above all — legitimately *mention*
    ``${VAR}`` literals inside backticks or fenced blocks, and those are
    prose about a token, never an unfilled interview slot. The banner branch
    keeps the full-text slot listing: a doc still under the UNRENDERED banner
    is kit output by construction, so a backticked slot there (e.g. the
    ai-project-workflow template's `` `${verify_command}` ``) is a real slot
    — and the banner itself (placed on full-text evidence) keeps holding the
    gate until it renders away.
    """
    findings: list[Finding] = []
    for rel in relpaths if relpaths is not None else scan_relpaths(config):
        path = target / rel
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        slots = sorted(find_placeholders(text))
        listed = ", ".join(slots[:5]) + (" …" if len(slots) > 5 else "")
        live_slots = sorted(find_placeholders_outside_code(text))
        live_listed = ", ".join(live_slots[:5]) + (
            " …" if len(live_slots) > 5 else ""
        )
        if text.startswith(UNRENDERED_BANNER_FIRST_LINE):
            detail = f" (unfilled: {listed})" if slots else ""
            findings.append(
                Finding(
                    rel,
                    "unrendered-banner",
                    "still under the adopt-time UNRENDERED banner"
                    f"{detail} — answer the slots (`bootstrap.py answer "
                    "<slot> <value>`), then `bootstrap.py render --live`.",
                ),
            )
        elif evidence and live_slots:
            findings.append(
                Finding(
                    rel,
                    "unrendered-slot",
                    f"{len(live_slots)} unfilled ${{...}} slot(s): "
                    f"{live_listed} — "
                    "answer them, then `bootstrap.py render --live`.",
                ),
            )
    return findings


def check_engagement_control(target: Path, config: Any) -> list[Finding]:
    """The unrendered scan scoped to control-plane planted docs (fast lane).

    Queued fix 4's deeper-bug half (#148 root cause): the CI control fast
    lane runs only ``check --strict --status-only``, so a control-only PR
    that wrote a slot regression into ``control/status.md`` merged GREEN and
    poisoned main — every SUBSEQUENT full-lane PR went red until a hand-fix
    (#150). A control-only diff can only regress ``control/**`` files, so
    the fast lane runs exactly this scoped scan: the same banner/slot logic,
    restricted to the planted docs under ``control/``. Cheap by construction
    (a handful of file reads, stdlib-only) — the lane stays fast.
    """
    state = _load_state(target, config)
    evidence = _adoption_evidence(config, state)
    control = [rel for rel in scan_relpaths(config) if rel.startswith("control/")]
    return _unrendered_findings(target, config, evidence=evidence, relpaths=control)


def _strip_comment(line: str) -> str:
    """Drop a YAML/shell ``#`` comment, keeping the code before it.

    A whole-line comment (leading ``#``) yields ``""``; an inline `` #``
    comment keeps the code up to it. A bare ``#`` with no leading space
    (inside a URL or token) is left alone — kept simple, not a YAML parser.
    """
    if line.lstrip().startswith("#"):
        return ""
    idx = line.find(" #")
    return line[:idx] if idx != -1 else line


def _wired_workflows(target: Path) -> list[tuple[str, str]]:
    """Return ``(relpath, comment-stripped text)`` per workflow running the gate.

    A workflow counts when some non-comment line contains ``check --strict``
    (the same needle :func:`_enforcement_wired` has always used). The stripped
    text rides along so the strength scan (:func:`check_enforcement_strength`)
    can look for the stronger legs in exactly the content that counted —
    comment mentions of a leg must not read as wired strength any more than a
    commented command reads as a door.
    """
    workflows = target / ".github" / "workflows"
    if not workflows.is_dir():
        return []
    wired: list[tuple[str, str]] = []
    for path in sorted(workflows.glob("*.yml")) + sorted(workflows.glob("*.yaml")):
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        stripped_lines = [_strip_comment(line) for line in text.splitlines()]
        if any("check --strict" in line for line in stripped_lines):
            rel = path.relative_to(target).as_posix()
            wired.append((rel, "\n".join(stripped_lines)))
    return wired


def _enforcement_wired(target: Path) -> bool:
    """True when some workflow under .github/workflows/ runs ``check --strict``.

    Substring match on purpose: it accepts the planted ``substrate-gate.yml``
    verbatim AND a host's hand-rolled gate (the kit repo's own ``ci.yml``) —
    the condition is "a CI door exists", not "our exact file was copied".
    Comment content is stripped first, so a workflow that only *mentions* the
    command inside a ``#`` comment is not a real door and stays unwired.
    """
    return bool(_wired_workflows(target))


# The staged gate's stronger legs the plain form silently skips (idea
# engagement-wiring-strength-verification-2026-07-12, layer 1 — the #38
# weak-form class, re-verified at superbot-next c03df80): flag → what the
# missing leg costs, quoted verbatim in the advisory so the nudge teaches.
STRONG_GATE_LEGS: tuple[tuple[str, str], ...] = (
    (
        "--require-session-log",
        "the session-log locked door (a missing card is advisory, not red)",
    ),
    (
        "--session-log",
        "diff-aware card selection (mtime fallback grades the wrong card "
        "on multi-card diffs)",
    ),
    (
        "--inbox-base",
        "the inbox append-only gate (latent without a base blob — the "
        "v1.7.0-wave finding)",
    ),
)


def _has_leg(text: str, leg: str) -> bool:
    """Token-boundary test for a CLI flag in comment-stripped workflow text.

    Boundary-guarded on purpose: ``--session-log`` is a substring of
    ``--require-session-log``, so a plain ``in`` test would read the locked
    door's flag as also satisfying the diff-aware-selection leg. A flag
    counts only when not embedded in a longer flag/word (space- and
    ``=``-joined argument forms both pass).
    """
    return re.search(rf"(?<![\w-]){re.escape(leg)}(?![\w-])", text) is not None


def check_enforcement_strength(target: Path, config: Any) -> list[Finding]:
    """Advisory-only wiring-STRENGTH scan of the wired ``check --strict`` door.

    Why + provenance: idea engagement-wiring-strength-verification-2026-07-12
    (origin: fleet-review friction residuals, issues #36 report 3 + #38).
    ``_enforcement_wired`` answers only "does a workflow run the command?" —
    superbot-next's ``ci.yml`` (re-verified 2026-07-12 at ``c03df80``) runs
    the PLAIN form and read as fully wired while skipping the session-log
    locked door, diff-aware card selection, and the inbox append-only gate.
    Reliability (PL-008): UNVERIFIED — confirm its findings against ground
    truth a few times across sessions before trusting it; **delete this if it
    proves unreliable over multiple sessions.**

    Posture is **advisory-only, never exit-affecting** (the idea's contract:
    "Never strict-red — a hand-rolled gate is legitimate"): fires ONE
    ``enforcement-weak-form`` finding when the wired door lacks
    :data:`STRONG_GATE_LEGS` legs that the staged
    ``<state_dir>/ci/substrate-gate.yml`` demonstrably carries — the staged
    file is both the evidence the stronger form exists and the one-copy fix
    the message names. Silent when: no adoption evidence, nothing wired (the
    strict ``enforcement-unwired``/native path owns that), every leg present
    across the wired workflows (the kit's own ``ci.yml`` shape), or the
    staged gate is absent/doesn't carry the missing legs (nothing to copy).
    Leg presence is token-boundary matched (:func:`_has_leg`) on
    comment-stripped text only.
    """
    state = _load_state(target, config)
    if not _adoption_evidence(config, state):
        return []
    wired = _wired_workflows(target)
    if not wired:
        return []
    combined = "\n".join(text for _, text in wired)
    missing = [
        (leg, why) for leg, why in STRONG_GATE_LEGS if not _has_leg(combined, leg)
    ]
    if not missing:
        return []
    staged_rel = f"{config.state_dir}/ci/substrate-gate.yml"
    staged = target / staged_rel
    try:
        staged_text = "\n".join(
            _strip_comment(line)
            for line in staged.read_text(encoding="utf-8").splitlines()
        )
    except (OSError, UnicodeDecodeError):
        return []  # no staged stronger form to point at — nothing to copy
    staged_missing = [
        (leg, why) for leg, why in missing if _has_leg(staged_text, leg)
    ]
    if not staged_missing:
        return []
    doors = ", ".join(rel for rel, _ in wired)
    legs = "; ".join(f"`{leg}` — {why}" for leg, why in staged_missing)
    return [
        Finding(
            ".github/workflows/",
            "enforcement-weak-form",
            f"the wired `check --strict` door ({doors}) runs the plain form "
            f"and skips the staged gate's stronger leg(s): {legs}. Copy "
            f"{staged_rel} to .github/workflows/ (or `adopt "
            "--wire-enforcement`) for the full-strength gate — advisory "
            "only: a hand-rolled gate is legitimate.",
        ),
    ]


def required_unverified_note(target: Path, config: Any) -> str | None:
    """The ``enforcement-required-unverified`` honesty NOTE (idea layer 2).

    Whether the wired check is a REQUIRED status check is owner-UI state —
    invisible in-tree and 403-walled to agents (issue #36 report 3; proven:
    superbot-next #51/#68 merged with red non-required legs). The checker
    cannot confirm it today (no rules-API probe in a stdlib-only engine), so
    it says so honestly: one NOTE line whenever a CI door exists — either a
    workflow running ``check --strict`` or an accepted ``native_gate``
    declaration — naming the context expected to be required
    (``native_gate.required_context`` on the native path, else
    ``automerge.required_context``). NOTE-only by the idea's contract, like
    the ``enforcement-native`` acceptance NOTE it rides beside: honesty
    output on a green path, never telemetry, never exit-affecting. ``None``
    when no door exists (the unwired finding owns that conversation).
    """
    wired = _enforcement_wired(target)
    workflow, exists = _native_gate_declared(target, config)
    native_active = bool(workflow and exists) and not wired
    if not (wired or native_active):
        return None
    if native_active:
        gate = getattr(config, "native_gate", {})
        context = gate.get("required_context") if isinstance(gate, dict) else None
    else:
        automerge = getattr(config, "automerge", {})
        context = (
            automerge.get("required_context")
            if isinstance(automerge, dict)
            else None
        )
    named = (
        f"`{context}`" if isinstance(context, str) and context.strip() else "the wired check"
    )
    return (
        f"enforcement-required-unverified — whether {named} is a REQUIRED "
        "status check on the base branch is owner-UI state this gate cannot "
        "read (rules API; 403-walled to agents) — owner glance: Settings → "
        "Rules → required status checks; inference recipes: "
        "docs/CAPABILITIES.md."
    )


def _native_gate_declared(target: Path, config: Any) -> tuple[str | None, bool]:
    """Return ``(declared workflow relpath | None, exists-on-disk)``.

    The native-substrate-consumer evidence class (idea
    engagement-native-consumer-state-2026-07-12): ``substrate.config.json`` →
    ``native_gate.workflow`` names the workflow file the host declares as its
    real-but-not-kit-shaped CI door. Malformed declarations (non-dict field,
    non-string path) read as undeclared — a misconfiguration must not
    silently widen the gate (the ``heartbeat_files`` doctrine).
    """
    gate = getattr(config, "native_gate", None)
    if not isinstance(gate, dict):
        return None, False
    workflow = gate.get("workflow")
    if not isinstance(workflow, str) or not workflow.strip():
        return None, False
    workflow = workflow.strip()
    return workflow, (target / workflow).is_file()


def native_gate_note(target: Path, config: Any) -> str | None:
    """One-line ``enforcement-native`` NOTE when the declaration does the work.

    Returns the note exactly when the declared native gate is the evidence
    keeping ``enforcement-unwired`` quiet — declared, existing on disk, and
    no workflow runs ``check --strict`` (a kit-shaped door makes the
    declaration moot). ``None`` otherwise. Public on purpose: ``cmd_check``'s
    full lane emits it so acceptance is visible, never silent — the idea's
    contract, and the same "a quiet pass must say why" instinct as the
    inbox/preflight self-skip NOTEs.
    """
    workflow, exists = _native_gate_declared(target, config)
    if not (workflow and exists):
        return None
    if _enforcement_wired(target):
        return None
    context = getattr(config, "native_gate", {}).get("required_context")
    ctx = f" (required check: {context})" if context else ""
    return (
        f"enforcement-native — declared native gate `{workflow}`{ctx} "
        "accepted as the CI door (substrate.config.json `native_gate`); "
        "no workflow runs `check --strict`."
    )


def _session_loop_engaged(target: Path, config: Any, state: dict) -> bool:
    """True when at least one session has run (count or a real card)."""
    try:
        if int(state.get("session_count", 0) or 0) >= 1:
            return True
    except (TypeError, ValueError):
        pass
    sessions = target / config.sessions_dir
    if not sessions.is_dir():
        return False
    return any(p.name != "README.md" for p in sessions.glob("*.md"))


def check_engagement(target: Path, config: Any) -> list[Finding]:
    """Return the engagement-gate findings for ``target`` (empty = ENGAGED)."""
    state = _load_state(target, config)
    evidence = _adoption_evidence(config, state)
    findings = _unrendered_findings(target, config, evidence=evidence)
    if not evidence:
        return findings
    if not _enforcement_wired(target):
        declared, declared_exists = _native_gate_declared(target, config)
        if not (declared and declared_exists):
            dead = (
                f" (declared native_gate workflow `{declared}` does not "
                "exist — fix the declaration or wire the kit gate)"
                if declared
                else ""
            )
            findings.append(
                Finding(
                    ".github/workflows/",
                    "enforcement-unwired",
                    "no CI workflow runs `check --strict` — install the "
                    f"staged gate: copy {config.state_dir}/ci/"
                    "substrate-gate.yml to .github/workflows/ (or `adopt "
                    f"--wire-enforcement`).{dead}",
                ),
            )
    if not _session_loop_engaged(target, config, state):
        findings.append(
            Finding(
                config.sessions_dir,
                "session-loop-idle",
                "no session has ever run (session_count 0, no session card) "
                f"— write the first born-red card under {config.sessions_dir}/ "
                "and run `bootstrap.py session-close` at close.",
            ),
        )
    return findings
