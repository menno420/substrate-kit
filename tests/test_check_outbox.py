"""Tests for the friction-outbox pending-count advisory (fm plan A10,
ORDER 020 sub-item d) — the check-time surface of the session-close drain
reminder. Advisory-only: it fires when the outbox holds envelopes and is
silent otherwise, and (proven end-to-end) never affects the ``check`` exit
code."""

from __future__ import annotations

from pathlib import Path

import pytest

pytest.importorskip("engine.hooks.settings")

from engine.checks.check_outbox import OUTBOX_KIND, check_outbox_pending
from engine.cli import main
from engine.lib.config import Config, save_config
from engine.lib.state import JsonStateBackend, default_state
from engine.loop.friction import FRICTION_LABEL, build_envelope, write_outbox


def _install(tmp_path: Path) -> tuple[Path, Config]:
    root = tmp_path / "repo"
    config = Config()
    config.kit_version = "1.0.0"
    root.mkdir()
    save_config(root, config)
    backend = JsonStateBackend(root / config.state_dir / "state.json")
    with backend.transaction():
        for key, value in default_state(config.project_id).items():
            backend.set(key, value)
    return root, config


def _envelope(lesson: str = "x") -> dict:
    return build_envelope(
        repo="o/r",
        project_id="p",
        kit_version="1.0.0",
        reports=[{"lesson": lesson}],
    )


# ── the checker unit ──────────────────────────────────────────────────────────


def test_empty_outbox_is_silent(tmp_path):
    root, config = _install(tmp_path)
    # No outbox directory at all (nothing ever filed).
    assert check_outbox_pending(root, config.state_dir) == []


def test_outbox_dir_present_but_empty_is_silent(tmp_path):
    root, config = _install(tmp_path)
    (root / config.state_dir / "friction-outbox").mkdir(parents=True)
    assert check_outbox_pending(root, config.state_dir) == []


def test_one_envelope_fires_one_advisory(tmp_path):
    root, config = _install(tmp_path)
    path = write_outbox(root, config.state_dir, _envelope())
    findings = check_outbox_pending(root, config.state_dir)
    assert len(findings) == 1
    (finding,) = findings
    assert finding.kind == OUTBOX_KIND
    assert finding.path == f"{config.state_dir}/friction-outbox/"
    # Singular grammar, names the envelope, points at the drain verbs + label.
    assert "1 friction report pending" in finding.message
    assert path.name in finding.message
    assert f"`{FRICTION_LABEL}`-labeled" in finding.message
    assert "friction show" in finding.message


def test_plural_grammar_and_name_preview_elision(tmp_path):
    root, config = _install(tmp_path)
    for i in range(5):
        write_outbox(root, config.state_dir, _envelope(lesson=f"L{i}"))
    (finding,) = check_outbox_pending(root, config.state_dir)
    assert "5 friction reports pending" in finding.message  # plural
    assert ", …" in finding.message  # >3 elides the tail


def test_two_envelopes_no_elision(tmp_path):
    root, config = _install(tmp_path)
    write_outbox(root, config.state_dir, _envelope("a"))
    write_outbox(root, config.state_dir, _envelope("b"))
    (finding,) = check_outbox_pending(root, config.state_dir)
    assert "2 friction reports pending" in finding.message
    assert ", …" not in finding.message


# ── advisory posture end-to-end (never exit-affecting) ────────────────────────


def test_pending_outbox_never_changes_the_check_exit_code(tmp_path, capsys):
    # Differential proof of the advisory contract: whatever a bare
    # `check --strict` decides on this tree, adding a pending outbox envelope
    # must NOT change that verdict — it only adds the surfaced advisory line.
    root, config = _install(tmp_path)
    code_clean = main(["check", "--strict", "--target", str(root)])
    clean_out = capsys.readouterr().out
    assert f"[{OUTBOX_KIND}]" not in clean_out  # empty outbox is silent

    write_outbox(root, config.state_dir, _envelope())
    code_dirty = main(["check", "--strict", "--target", str(root)])
    dirty_out = capsys.readouterr().out
    assert f"[{OUTBOX_KIND}]" in dirty_out  # now surfaced
    assert "never exit-affecting" in dirty_out
    assert code_dirty == code_clean  # the advisory added no exit-code weight
