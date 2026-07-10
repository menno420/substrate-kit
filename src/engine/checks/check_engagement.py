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
- ``session-loop-idle`` — no session has ever run: ``session_count`` is 0
  AND no real session card exists under the sessions dir.

Scope: the scan covers exactly the **planted** doc paths (the ``ADOPT_PLAN``
destinations, ``project.index.json``, and a live ``.claude/CLAUDE.md``) —
never template sources, so the kit repo's own ``src/engine/templates/``
(legitimately full of ``${...}``) can never red its own gate. Findings ride
the ordinary ``check`` finding loop: strict-only exit-code impact, guard-fire
telemetry, and the reasons-required allowlist all apply unchanged.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from engine.adopt import ADOPT_PLAN, UNRENDERED_BANNER_FIRST_LINE, _adopt_dest
from engine.checks.check_docs import Finding
from engine.render import find_placeholders

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
    relpaths = [_adopt_dest(plan_rel, config) for _, plan_rel in ADOPT_PLAN]
    relpaths.extend(EXTRA_SCAN_RELPATHS)
    return relpaths


def _unrendered_findings(
    target: Path,
    config: Any,
    *,
    evidence: bool,
) -> list[Finding]:
    """Scan the planted docs for the UNRENDERED banner / leftover ``${...}``."""
    findings: list[Finding] = []
    for rel in scan_relpaths(config):
        path = target / rel
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        slots = sorted(find_placeholders(text))
        listed = ", ".join(slots[:5]) + (" …" if len(slots) > 5 else "")
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
        elif evidence and slots:
            findings.append(
                Finding(
                    rel,
                    "unrendered-slot",
                    f"{len(slots)} unfilled ${{...}} slot(s): {listed} — "
                    "answer them, then `bootstrap.py render --live`.",
                ),
            )
    return findings


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


def _enforcement_wired(target: Path) -> bool:
    """True when some workflow under .github/workflows/ runs ``check --strict``.

    Substring match on purpose: it accepts the planted ``substrate-gate.yml``
    verbatim AND a host's hand-rolled gate (the kit repo's own ``ci.yml``) —
    the condition is "a CI door exists", not "our exact file was copied".
    Comment content is stripped first, so a workflow that only *mentions* the
    command inside a ``#`` comment is not a real door and stays unwired.
    """
    workflows = target / ".github" / "workflows"
    if not workflows.is_dir():
        return False
    for path in sorted(workflows.glob("*.yml")) + sorted(workflows.glob("*.yaml")):
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if any("check --strict" in _strip_comment(line) for line in text.splitlines()):
            return True
    return False


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
        findings.append(
            Finding(
                ".github/workflows/",
                "enforcement-unwired",
                "no CI workflow runs `check --strict` — install the staged "
                f"gate: copy {config.state_dir}/ci/substrate-gate.yml to "
                ".github/workflows/ (or `adopt --wire-enforcement`).",
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
