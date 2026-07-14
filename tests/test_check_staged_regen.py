"""The staged-artifact regen-lag advisory (ORDER 019 item 6).

Idea authority: ``docs/ideas/staged-artifact-regen-lag-checker-2026-07-12.md``
— staged ``.substrate/`` artifacts (staged CLAUDE.md, skills, agents) can
carry unfilled ``${...}`` slots even though ``slot_values`` are ALL filled
(they were staged pre-slot-fill; nothing re-renders them outside an
``upgrade``), and the engagement gate scans planted docs, never the staged
tree. Proven live on websites @ ``992c045``. These tests pin the idea file's
own fixture ("a repo with all slots answered + one staged artifact carrying
``${project_name}`` must fire; the same artifact with the slot inside a code
span must not"), the mutation arc (stale → fires; regenerate → clean), and
the advisory never-exit-affecting contract.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

pytest.importorskip("engine.hooks.settings")

from engine.adopt import adopt
from engine.checks.check_staged_regen import check_staged_regen
from engine.cli import cmd_check
from engine.interview.interview import record_answer
from engine.interview.question_bank import QUESTIONS
from engine.lib.config import Config
from engine.lib.state import JsonStateBackend, default_state


def _write_state(root: Path, config: Config, slot_values: dict) -> None:
    state = root / config.state_dir / "state.json"
    state.parent.mkdir(parents=True, exist_ok=True)
    state.write_text(json.dumps({"slot_values": slot_values}), encoding="utf-8")


def _filled(slot: str, value: str = "a real answer") -> dict:
    return {slot: {"question_id": "Q-000", "source": "user", "value": value}}


def _stage(root: Path, config: Config, rel: str, text: str) -> Path:
    path = root / config.state_dir / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _init_backend(root: Path, config: Config) -> JsonStateBackend:
    backend = JsonStateBackend(root / config.state_dir / "state.json")
    with backend.transaction():
        for key, value in default_state(config.project_id).items():
            backend.set(key, value)
    return backend


def _answer_everything(backend: JsonStateBackend) -> None:
    for question in QUESTIONS:
        record_answer(
            backend,
            question,
            f"answered value for {question['slot']} — past every floor",
            source="user",
        )


# ---------------------------------------------------------------------------
# The idea file's fixture pair
# ---------------------------------------------------------------------------


def test_filled_slot_in_staged_artifact_fires(tmp_path):
    config = Config()
    _write_state(tmp_path, config, _filled("project_name"))
    _stage(tmp_path, config, "agents/architect.md", "# a\n\n${project_name}\n")
    findings = check_staged_regen(tmp_path, config)
    assert [f.kind for f in findings] == ["staged-regen-lag"]
    assert findings[0].path == f"{config.state_dir}/agents/architect.md"
    assert "project_name" in findings[0].message
    # The message names the recovering command (idea file requirement).
    assert "bootstrap.py upgrade" in findings[0].message


def test_slot_inside_code_span_does_not_fire(tmp_path):
    config = Config()
    _write_state(tmp_path, config, _filled("project_name"))
    _stage(
        tmp_path,
        config,
        "agents/architect.md",
        "# a\n\nmentions `${project_name}` in prose\n",
    )
    assert check_staged_regen(tmp_path, config) == []


def test_slot_inside_fenced_block_does_not_fire(tmp_path):
    config = Config()
    _write_state(tmp_path, config, _filled("project_name"))
    _stage(
        tmp_path,
        config,
        "skills/pack/SKILL.md",
        "# s\n\n```\necho ${project_name}\n```\n",
    )
    assert check_staged_regen(tmp_path, config) == []


# ---------------------------------------------------------------------------
# The filled-slot intersection is the firewall
# ---------------------------------------------------------------------------


def test_unfilled_slot_placeholder_is_not_lag(tmp_path):
    # No answer recorded → nothing to lag behind; the interview owns it.
    config = Config()
    _write_state(tmp_path, config, _filled("other_slot"))
    _stage(tmp_path, config, "claude/CLAUDE.md", "# c\n\n${project_name}\n")
    assert check_staged_regen(tmp_path, config) == []


def test_shell_vars_and_actions_syntax_never_fire(tmp_path):
    # ${GITHUB_ENV} is not a filled slot name; ${{ github.ref }} is not even
    # placeholder-shaped. Staged CI/hook material stays quiet.
    config = Config()
    _write_state(tmp_path, config, _filled("project_name"))
    _stage(
        tmp_path,
        config,
        "ci/substrate-gate.yml",
        'run: echo "${GITHUB_ENV} ${{ github.ref }}"\n',
    )
    assert check_staged_regen(tmp_path, config) == []


def test_empty_value_is_not_filled(tmp_path):
    config = Config()
    _write_state(tmp_path, config, _filled("project_name", value="  "))
    _stage(tmp_path, config, "agents/architect.md", "${project_name}\n")
    assert check_staged_regen(tmp_path, config) == []


# ---------------------------------------------------------------------------
# Scan-surface boundaries
# ---------------------------------------------------------------------------


def test_backup_bank_and_state_root_files_are_never_scanned(tmp_path):
    config = Config()
    _write_state(tmp_path, config, _filled("project_name"))
    _stage(tmp_path, config, "backup/bootstrap-1.0.0.py", "${project_name}\n")
    # Free-text kit state at the state-dir root (a reflection ABOUT a slot)
    # must never fire either.
    _stage(tmp_path, config, "reflections.json", '["note about ${project_name}"]\n')
    assert check_staged_regen(tmp_path, config) == []


def test_no_state_or_no_staged_tree_is_quiet(tmp_path):
    config = Config()
    # No state.json at all.
    assert check_staged_regen(tmp_path, config) == []
    # State with no slot_values.
    _write_state(tmp_path, config, {})
    assert check_staged_regen(tmp_path, config) == []
    # Filled slots but no staged tree.
    _write_state(tmp_path, config, _filled("project_name"))
    assert check_staged_regen(tmp_path, config) == []


def test_unreadable_staged_artifact_fails_open(tmp_path):
    config = Config()
    _write_state(tmp_path, config, _filled("project_name"))
    path = tmp_path / config.state_dir / "agents" / "broken.md"
    path.parent.mkdir(parents=True)
    path.write_bytes(b"\xff\xfe\x00broken ${project_name}")
    assert check_staged_regen(tmp_path, config) == []


# ---------------------------------------------------------------------------
# The mutation arc — stale after answers, clean after regen
# ---------------------------------------------------------------------------


def test_adopt_answer_lag_then_regen_clean(tmp_path):
    root = tmp_path / "repo"
    config = Config()
    backend = _init_backend(root, config)
    # Bare adopt stages the packs with every slot unfilled — no lag yet
    # (nothing answered, nothing to lag behind).
    adopt(root, config, backend, kit_root=tmp_path / "kit")
    assert check_staged_regen(root, config) == []
    # Answer everything AFTER staging — the exact websites @ 992c045 shape:
    # slot_values all filled, staged artifacts still templated.
    _answer_everything(backend)
    findings = check_staged_regen(root, config)
    assert findings, "filled answers + pre-fill staged tree must fire"
    assert {f.kind for f in findings} == {"staged-regen-lag"}
    fired_paths = {f.path for f in findings}
    assert any(p.startswith(f"{config.state_dir}/") for p in fired_paths)
    # Regenerate the staged tree (adopt is idempotent: staged artifacts
    # always regenerate — the same pass `upgrade` runs) → checker clean.
    adopt(root, config, backend, kit_root=tmp_path / "kit")
    assert check_staged_regen(root, config) == []


# ---------------------------------------------------------------------------
# cmd_check integration — advisory NEVER touches the exit code
# ---------------------------------------------------------------------------


def test_cmd_check_strict_stays_green_on_regen_lag(tmp_path, capsys):
    config = Config()
    _write_state(tmp_path, config, _filled("project_name"))
    _stage(tmp_path, config, "agents/architect.md", "# a\n\n${project_name}\n")
    assert cmd_check(tmp_path, strict=True) == 0
    out = capsys.readouterr().out
    assert "staged regen-lag advisory" in out
    assert "staged-regen-lag" in out
    assert "never exit-affecting" in out
    assert "bootstrap.py upgrade" in out


def test_cmd_check_status_only_lane_skips_staged_scan(tmp_path, capsys):
    config = Config()
    _write_state(tmp_path, config, _filled("project_name"))
    _stage(tmp_path, config, "agents/architect.md", "# a\n\n${project_name}\n")
    assert cmd_check(tmp_path, strict=True, status_only=True) == 0
    assert "staged-regen-lag" not in capsys.readouterr().out
