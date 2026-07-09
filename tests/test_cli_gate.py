"""The CI locked-door gate: `check --require-session-log`.

The kit's `check --strict` treats a *missing* session log as advisory (so a
host can lint mid-session). `--require-session-log` flips a missing log to a
hard failure — the gate mode the live CI workflow runs, so a session that never
writes its journal cannot merge. Proves the door locks (red) and opens (green).
"""

from __future__ import annotations

from pathlib import Path

import pytest

pytest.importorskip("engine.hooks.settings")

from engine.adopt import adopt
from engine.cli import cmd_check
from engine.interview.interview import record_answer
from engine.interview.question_bank import QUESTIONS
from engine.lib.config import Config
from engine.lib.state import JsonStateBackend, default_state


def _adopt_scratch(root: Path, kit_root: Path) -> Config:
    """Adopt a scratch repo already in the ENGAGED end state (KL-7 gate green:
    every slot answered pre-adopt → fully rendered docs, enforcement wired,
    session loop counted) — so these tests isolate the session-log gate."""
    config = Config()
    backend = JsonStateBackend(root / config.state_dir / "state.json")
    with backend.transaction():
        for key, value in default_state(config.project_id).items():
            backend.set(key, value)
    for question in QUESTIONS:
        record_answer(
            backend,
            question,
            f"engaged fixture value for {question['slot']} — past every floor",
            source="user",
        )
    adopt(root, config, backend, kit_root=kit_root, wire_enforcement=True)
    backend.set("session_count", 1)
    # KL-8: the control loop is engaged too — a real heartbeat replaces the
    # adopt seed (whose status-no-heartbeat finding would red these checks).
    (root / "control" / "status.md").write_text(
        "# scratch · status\nupdated: 2026-07-09T12:00Z\nphase: fixture\n",
        encoding="utf-8",
    )
    return config


def _write_complete_log(root: Path, config: Config) -> None:
    """A session card that carries every required marker (would pass the gate)."""
    markers = "\n".join(
        f"{m.get('needle', '')} {m.get('label', '')}" for m in config.session_markers
    )
    card = root / config.sessions_dir / "2026-07-07-demo.md"
    card.write_text(
        f"# demo session\n\n> **Status:** `complete`\n\n{markers}\n",
        encoding="utf-8",
    )


def test_missing_log_is_advisory_by_default(tmp_path, capsys):
    root = tmp_path / "repo"
    _adopt_scratch(root, tmp_path / "kit")
    # No session card written; default check does NOT fail on that alone.
    rc = cmd_check(root, strict=True)
    assert rc == 0
    assert "advisory" in capsys.readouterr().out


def test_require_session_log_holds_the_merge_red_when_absent(tmp_path, capsys):
    root = tmp_path / "repo"
    _adopt_scratch(root, tmp_path / "kit")
    # The locked door: same repo, gate mode → a missing journal fails.
    rc = cmd_check(root, strict=True, require_session_log=True)
    assert rc == 1
    assert "MERGE HELD" in capsys.readouterr().out


def test_require_session_log_opens_the_door_once_the_journal_exists(tmp_path):
    root = tmp_path / "repo"
    config = _adopt_scratch(root, tmp_path / "kit")
    # Red before the journal…
    assert cmd_check(root, strict=True, require_session_log=True) == 1
    # …green after writing a complete session card. The door opens.
    _write_complete_log(root, config)
    assert cmd_check(root, strict=True, require_session_log=True) == 0


def test_incomplete_log_fails_the_gate_too(tmp_path):
    root = tmp_path / "repo"
    config = _adopt_scratch(root, tmp_path / "kit")
    # A card missing its required markers is not enough to open the door.
    stub = root / config.sessions_dir / "2026-07-07-stub.md"
    stub.write_text("# stub\n\n> **Status:** `complete`\n", encoding="utf-8")
    assert cmd_check(root, strict=True, require_session_log=True) == 1


# ---------------------------------------------------------------------------
# Explicit card selection — `check --session-log` (groomed-ideas-1)
# ---------------------------------------------------------------------------


def test_explicit_session_log_overrides_the_mtime_guess(tmp_path):
    import os
    import time

    root = tmp_path / "repo"
    config = _adopt_scratch(root, tmp_path / "kit")
    _write_complete_log(root, config)
    # A newer-by-mtime foreign card is incomplete (the CI-checkout trap:
    # mtime order is arbitrary there) — the default selection gates on it…
    other = root / config.sessions_dir / "2026-07-08-other.md"
    other.write_text("# other\n\n> **Status:** `in-progress`\n", encoding="utf-8")
    future = time.time() + 120
    os.utime(other, (future, future))
    assert cmd_check(root, strict=True, require_session_log=True) == 1
    # …but the diff-derived explicit selection names THIS session's card.
    rc = cmd_check(
        root,
        strict=True,
        require_session_log=True,
        session_log=Path(config.sessions_dir) / "2026-07-07-demo.md",
    )
    assert rc == 0


def test_explicit_session_log_missing_never_silently_falls_back(tmp_path, capsys):
    root = tmp_path / "repo"
    config = _adopt_scratch(root, tmp_path / "kit")
    # A complete card exists, but the explicitly named one does not: the gate
    # holds rather than quietly gating on a different card.
    _write_complete_log(root, config)
    rc = cmd_check(
        root,
        strict=True,
        require_session_log=True,
        session_log=Path(config.sessions_dir) / "no-such-card.md",
    )
    assert rc == 1
    out = capsys.readouterr().out
    assert "MERGE HELD" in out
    assert "no-such-card.md" in out


def test_explicit_session_log_missing_is_advisory_without_the_gate(tmp_path, capsys):
    root = tmp_path / "repo"
    config = _adopt_scratch(root, tmp_path / "kit")
    rc = cmd_check(
        root,
        strict=True,
        session_log=Path(config.sessions_dir) / "no-such-card.md",
    )
    assert rc == 0
    assert "advisory" in capsys.readouterr().out


def test_explicit_session_log_accepts_an_incomplete_named_card(tmp_path):
    root = tmp_path / "repo"
    config = _adopt_scratch(root, tmp_path / "kit")
    # The named card is born-red: the gate reports IT, complete siblings or not.
    _write_complete_log(root, config)
    red = root / config.sessions_dir / "2026-07-09-red.md"
    red.write_text("# red\n\n> **Status:** `in-progress`\n", encoding="utf-8")
    rc = cmd_check(
        root,
        strict=True,
        require_session_log=True,
        session_log=Path(config.sessions_dir) / "2026-07-09-red.md",
    )
    assert rc == 1


# ---------------------------------------------------------------------------
# The fast lane's scoped gate — `check --status-only` (fleet review 2026-07-09)
# ---------------------------------------------------------------------------


def test_status_only_reds_on_a_broken_heartbeat(tmp_path, capsys):
    root = tmp_path / "repo"
    _adopt_scratch(root, tmp_path / "kit")
    # The bypass this closes: a control-only PR deletes/corrupts the
    # heartbeat; the fast lane used to skip every checker and report green.
    (root / "control" / "status.md").write_text(
        "# scratch · status\nphase: heartbeat deleted\n", encoding="utf-8"
    )
    rc = cmd_check(root, strict=True, status_only=True)
    assert rc == 1
    assert "status-no-heartbeat" in capsys.readouterr().out


def test_status_only_is_green_on_a_live_heartbeat_without_a_card(tmp_path, capsys):
    root = tmp_path / "repo"
    _adopt_scratch(root, tmp_path / "kit")
    # No session card exists (a heartbeat PR never carries one) and even
    # require_session_log must not deadlock the lane: --status-only never
    # touches the session-log seam.
    rc = cmd_check(root, strict=True, require_session_log=True, status_only=True)
    assert rc == 0
    out = capsys.readouterr().out
    assert "control-status check passed (--status-only)" in out
    assert "MERGE HELD" not in out


def test_status_only_ignores_non_status_findings(tmp_path):
    root = tmp_path / "repo"
    config = _adopt_scratch(root, tmp_path / "kit")
    # A born-red card would red the FULL gate — but it is outside the scoped
    # run: the lane's verdict is about the heartbeat, nothing else.
    red = root / config.sessions_dir / "2026-07-09-red.md"
    red.write_text("# red\n\n> **Status:** `in-progress`\n", encoding="utf-8")
    assert (
        cmd_check(
            root,
            strict=True,
            require_session_log=True,
            session_log=Path(config.sessions_dir) / "2026-07-09-red.md",
            status_only=True,
        )
        == 0
    )
    # Sanity: the same tree fails the full gate (the scoping is real).
    assert (
        cmd_check(
            root,
            strict=True,
            require_session_log=True,
            session_log=Path(config.sessions_dir) / "2026-07-09-red.md",
        )
        == 1
    )
