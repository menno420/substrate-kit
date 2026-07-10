"""The post-adopt ENGAGEMENT gate (band KL-7) — the fleet-review §4 fix.

Both fresh adopters stranded identically: planted docs still under UNRENDERED
banners with raw ``${...}`` slots, no CI running the check, ``session_count``
0. These tests pin the fix: `check --strict` is BORN RED after a bare adopt
and turns GREEN exactly when the install is rendered + enforcing + looping —
the permanent regression guard for the stranding (enforce-don't-exhort,
PL-007, applied to onboarding itself).
"""

from __future__ import annotations

from pathlib import Path

import pytest

pytest.importorskip("engine.hooks.settings")

from engine.adopt import adopt
from engine.checks.check_engagement import check_engagement
from engine.cli import cmd_adopt, cmd_check, cmd_render
from engine.interview.interview import record_answer
from engine.interview.question_bank import QUESTIONS
from engine.lib.config import Config, save_config
from engine.lib.state import JsonStateBackend, default_state

ENGAGEMENT_KINDS = {
    "unrendered-banner",
    "unrendered-slot",
    "enforcement-unwired",
    "session-loop-idle",
}


def _init_backend(root: Path, config: Config) -> JsonStateBackend:
    backend = JsonStateBackend(root / config.state_dir / "state.json")
    with backend.transaction():
        for key, value in default_state(config.project_id).items():
            backend.set(key, value)
    return backend


def _adopt_bare(root: Path, kit_root: Path) -> tuple[Config, JsonStateBackend]:
    """A default adopt with no interview answers — today's stranding shape."""
    config = Config()
    backend = _init_backend(root, config)
    adopt(root, config, backend, kit_root=kit_root)
    return config, backend


def _answer_everything(backend: JsonStateBackend) -> None:
    for question in QUESTIONS:
        record_answer(
            backend,
            question,
            f"engaged value for {question['slot']} — past every substance floor",
            source="user",
        )


def _install_staged_gate(root: Path, config: Config) -> None:
    staged = root / config.state_dir / "ci" / "substrate-gate.yml"
    dest = root / ".github" / "workflows" / "substrate-gate.yml"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(staged.read_text(encoding="utf-8"), encoding="utf-8")


def _write_complete_card(root: Path, config: Config) -> Path:
    markers = "\n".join(
        f"{m.get('needle', '')} {m.get('label', '')}" for m in config.session_markers
    )
    card = root / config.sessions_dir / "2026-07-09-first.md"
    card.parent.mkdir(parents=True, exist_ok=True)
    card.write_text(
        f"# first session\n\n> **Status:** `complete`\n\n{markers}\n",
        encoding="utf-8",
    )
    return card


# ---------------------------------------------------------------------------
# The checker itself
# ---------------------------------------------------------------------------


def test_bare_adopt_raises_all_four_blocker_kinds(tmp_path):
    root = tmp_path / "repo"
    config, _ = _adopt_bare(root, tmp_path / "kit")
    kinds = {f.kind for f in check_engagement(root, config)}
    assert "unrendered-banner" in kinds  # unanswered slots → bannered docs
    assert "enforcement-unwired" in kinds  # no CI installed by default
    assert "session-loop-idle" in kinds  # no session has run
    assert kinds <= ENGAGEMENT_KINDS


def test_banner_finding_fires_even_without_version_evidence(tmp_path):
    # A doc still carrying the UNRENDERED banner is kit output by
    # construction — flagged even on an install that never recorded a
    # kit_version (pre-v1.0.0 installs).
    root = tmp_path / "repo"
    config = Config()
    save_config(root, config)
    doc = root / "docs" / "architecture.md"
    doc.parent.mkdir(parents=True)
    doc.write_text(
        "> ⚠️ **UNRENDERED SLOTS BELOW — run `python3 bootstrap.py ask`.**\n"
        "> …\n\n# arch\n\n${architecture_layers}\n",
        encoding="utf-8",
    )
    findings = check_engagement(root, config)
    assert [f.kind for f in findings] == ["unrendered-banner"]
    assert "architecture_layers" in findings[0].message


def test_bare_placeholder_prose_needs_adoption_evidence(tmp_path):
    # ${name}-form prose in a never-adopted repo is host content, not a kit
    # slot — no evidence, no finding; with a recorded kit_version it counts.
    root = tmp_path / "repo"
    config = Config()
    save_config(root, config)
    doc = root / "docs" / "helper-policy.md"
    doc.parent.mkdir(parents=True)
    doc.write_text("# doc\n\nshell example: ${some_var}\n", encoding="utf-8")
    assert check_engagement(root, config) == []
    config.kit_version = "1.0.0"
    kinds = [f.kind for f in check_engagement(root, config)]
    assert "unrendered-slot" in kinds


def test_template_sources_are_never_scanned(tmp_path):
    # The kit repo's own templates legitimately contain ${...} — the scan
    # covers planted destinations only, so template sources can never red
    # the gate.
    root = tmp_path / "repo"
    config = Config()
    config.kit_version = "1.0.0"
    save_config(root, config)
    tmpl = root / "src" / "engine" / "templates" / "x.md.tmpl"
    tmpl.parent.mkdir(parents=True)
    tmpl.write_text("${project_name}\n", encoding="utf-8")
    kinds = {f.kind for f in check_engagement(root, config)}
    assert "unrendered-slot" not in kinds
    assert "unrendered-banner" not in kinds


def test_enforcement_accepts_any_workflow_running_strict_check(tmp_path):
    # A hand-rolled gate (the kit repo's own ci.yml shape) counts — the
    # condition is "a CI door exists", not "our exact file was copied".
    root = tmp_path / "repo"
    config, backend = _adopt_bare(root, tmp_path / "kit")
    wf = root / ".github" / "workflows" / "ci.yml"
    wf.parent.mkdir(parents=True)
    wf.write_text("run: python3 bootstrap.py check --strict\n", encoding="utf-8")
    kinds = {f.kind for f in check_engagement(root, config)}
    assert "enforcement-unwired" not in kinds


def test_enforcement_ignores_comment_only_mentions(tmp_path):
    # A workflow whose ONLY mention of the command is inside a `#` comment is
    # a dead door — it must RED as enforcement-unwired, not clear the gate
    # (fleet-review §c1 comment-leniency: issue #36 report 1).
    root = tmp_path / "repo"
    config, backend = _adopt_bare(root, tmp_path / "kit")
    wf = root / ".github" / "workflows" / "ci.yml"
    wf.parent.mkdir(parents=True)
    wf.write_text(
        "# TODO someday run check --strict here\n"
        "jobs:\n  build:\n    steps:\n      - run: echo hi  # not check --strict\n",
        encoding="utf-8",
    )
    kinds = {f.kind for f in check_engagement(root, config)}
    assert "enforcement-unwired" in kinds
    # Uncommenting the command wires a real door — no false-negative regression.
    wf.write_text(
        "jobs:\n  build:\n    steps:\n      - run: python3 bootstrap.py check --strict\n",
        encoding="utf-8",
    )
    kinds = {f.kind for f in check_engagement(root, config)}
    assert "enforcement-unwired" not in kinds


def test_session_loop_engages_via_count_or_card(tmp_path):
    root = tmp_path / "repo"
    config, backend = _adopt_bare(root, tmp_path / "kit")
    assert "session-loop-idle" in {f.kind for f in check_engagement(root, config)}
    # A real card (even born-red) proves the loop is running…
    card = root / config.sessions_dir / "2026-07-09-x.md"
    card.write_text("# x\n\n> **Status:** `in-progress`\n", encoding="utf-8")
    assert "session-loop-idle" not in {f.kind for f in check_engagement(root, config)}
    card.unlink()
    # …and so does a session_count ≥ 1 with no card on disk.
    backend.set("session_count", 1)
    assert "session-loop-idle" not in {f.kind for f in check_engagement(root, config)}


def test_unadopted_tree_yields_nothing(tmp_path):
    root = tmp_path / "bare"
    (root / "docs").mkdir(parents=True)
    (root / "docs" / "architecture.md").write_text("# fine\n", encoding="utf-8")
    assert check_engagement(root, Config()) == []


# ---------------------------------------------------------------------------
# The cold-adopt ENGAGED-state arc — the fleet-review §4 regression guard
# ---------------------------------------------------------------------------


def test_cold_adopt_is_born_red_then_green_once_engaged(tmp_path, capsys):
    root = tmp_path / "repo"
    config, backend = _adopt_bare(root, tmp_path / "kit")

    # RED: a bare adopt LOOKS onboarded but is neither rendered nor
    # enforcing — exactly today's stranding; the gate holds.
    assert cmd_check(root, strict=True) == 1
    out = capsys.readouterr().out
    assert "unrendered-banner" in out
    assert "enforcement-unwired" in out
    assert "session-loop-idle" in out

    # ENGAGE: (1) render — answer every slot, fill the planted docs live…
    _answer_everything(backend)
    assert cmd_render(root, live=True) == 0
    # …(2) enforcement — install the staged gate workflow…
    _install_staged_gate(root, config)
    # …(3) session loop — the first real session card.
    card = _write_complete_card(root, config)

    # Still RED: the KL-8 control loop hasn't engaged — the planted
    # control/status.md is the heartbeat-less adopt seed.
    capsys.readouterr()
    assert cmd_check(root, strict=True) == 1
    assert "status-no-heartbeat" in capsys.readouterr().out
    # …(4) control loop — the first real heartbeat overwrites the seed.
    (root / "control" / "status.md").write_text(
        "# repo · status\nupdated: 2026-07-09T12:00Z\nphase: engaged\n"
        "health: green\nlast-shipped: none\nblockers: none\n"
        "orders: acked= done=\n⚑ needs-owner: none\nnotes: first heartbeat\n",
        encoding="utf-8",
    )

    # GREEN: engaged — and the gate-mode CI invocation agrees.
    capsys.readouterr()
    assert cmd_check(root, strict=True) == 0
    assert (
        cmd_check(
            root,
            strict=True,
            require_session_log=True,
            session_log=card.relative_to(root),
        )
        == 0
    )


def test_wire_enforcement_alone_is_still_red(tmp_path):
    # --wire-enforcement wires the door but render + session loop are still
    # pending — a wired-but-unrendered install must not read as engaged.
    root = tmp_path / "repo"
    config = Config()
    backend = _init_backend(root, config)
    adopt(root, config, backend, kit_root=tmp_path / "kit", wire_enforcement=True)
    kinds = {f.kind for f in check_engagement(root, config)}
    assert "enforcement-unwired" not in kinds
    assert "unrendered-banner" in kinds
    assert "session-loop-idle" in kinds
    assert cmd_check(root, strict=True) == 1


# ---------------------------------------------------------------------------
# Adopt UX — the output IS the checklist; the gate workflow is staged
# ---------------------------------------------------------------------------


def test_adopt_stages_the_live_gate_workflow(tmp_path):
    root = tmp_path / "repo"
    config, _ = _adopt_bare(root, tmp_path / "kit")
    staged = root / config.state_dir / "ci" / "substrate-gate.yml"
    assert staged.is_file()
    text = staged.read_text(encoding="utf-8")
    assert "check --strict --require-session-log" in text
    # Staged, not installed: a default adopt still never writes live CI.
    assert not (root / ".github").exists()


def test_cmd_adopt_prints_the_engagement_checklist(tmp_path, capsys):
    root = tmp_path / "repo"
    assert cmd_adopt(root, include_claude=False) == 0
    out = capsys.readouterr().out
    assert "NOT ENGAGED" in out
    assert "check --strict" in out
    assert "[enforcement-unwired]" in out
    assert "[session-loop-idle]" in out
    assert "[unrendered-banner]" in out
    # KL-8 rider: the just-planted seed status.md joins the checklist —
    # writing the first real heartbeat is part of engaging.
    assert "[status-no-heartbeat]" in out
