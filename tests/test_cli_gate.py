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


# ---------------------------------------------------------------------------
# Added-card grammar lint — `check --added-card` (queued kit fix 1,
# the venture-lab #15 false-green class)
# ---------------------------------------------------------------------------


_SENTINEL = Path(".sessions") / "__born-red-card-added__.md"


def test_added_card_born_red_heartbeat_stays_green(tmp_path):
    root = tmp_path / "repo"
    config = _adopt_scratch(root, tmp_path / "kit")
    # The generated gate's advisory lane: absent sentinel as --session-log,
    # the ADDED card via --added-card. A well-badged in-progress card is the
    # designed born-red state — no red.
    card = root / config.sessions_dir / "2026-07-11-born.md"
    card.write_text(
        "# born\n\n> **Status:** `in-progress`\n\nabout to do X\n",
        encoding="utf-8",
    )
    assert (
        cmd_check(
            root,
            strict=True,
            session_log=_SENTINEL,
            added_card=Path(config.sessions_dir) / "2026-07-11-born.md",
        )
        == 0
    )


def test_added_card_claiming_complete_but_malformed_reds(tmp_path, capsys):
    root = tmp_path / "repo"
    config = _adopt_scratch(root, tmp_path / "kit")
    # The exact #15 shape: ADDED card declares `complete` but misses its
    # grammar needles — under the old full exemption this merged green.
    card = root / config.sessions_dir / "2026-07-11-bad.md"
    card.write_text(
        "# bad\n\n> **Status:** `complete`\n\n## Session idea\nno needle\n"
        "\n## Model\nCoordinator seat: opus-x\n",
        encoding="utf-8",
    )
    rc = cmd_check(
        root,
        strict=True,
        session_log=_SENTINEL,
        added_card=Path(config.sessions_dir) / "2026-07-11-bad.md",
    )
    assert rc == 1
    assert "session-card-grammar" in capsys.readouterr().out


def test_added_card_without_badge_reds(tmp_path, capsys):
    root = tmp_path / "repo"
    config = _adopt_scratch(root, tmp_path / "kit")
    card = root / config.sessions_dir / "2026-07-11-nobadge.md"
    card.write_text("# nobadge\n\nfree-form text, no Status\n", encoding="utf-8")
    rc = cmd_check(
        root,
        strict=True,
        session_log=_SENTINEL,
        added_card=Path(config.sessions_dir) / "2026-07-11-nobadge.md",
    )
    assert rc == 1
    assert "Status badge" in capsys.readouterr().out


def test_added_card_absent_is_advisory(tmp_path, capsys):
    root = tmp_path / "repo"
    config = _adopt_scratch(root, tmp_path / "kit")
    rc = cmd_check(
        root,
        strict=True,
        session_log=_SENTINEL,
        added_card=Path(config.sessions_dir) / "never-written.md",
    )
    assert rc == 0
    assert "nothing to grammar-check" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# Designed-hold signal (queued kit fix 4, the PL-006 observer-noise class)
# ---------------------------------------------------------------------------


def _write_born_red_card(root: Path, config) -> Path:
    card = root / config.sessions_dir / "2026-07-11-hold.md"
    card.write_text(
        "# hold\n\n> **Status:** `in-progress`\n\nmid-flight\n",
        encoding="utf-8",
    )
    return Path(config.sessions_dir) / "2026-07-11-hold.md"


def test_designed_hold_banner_when_only_the_card_holds(tmp_path, capsys):
    root = tmp_path / "repo"
    config = _adopt_scratch(root, tmp_path / "kit")
    rel = _write_born_red_card(root, config)
    rc = cmd_check(root, strict=True, require_session_log=True, session_log=rel)
    assert rc == 1  # the hold is real — only its LABELLING changes
    out = capsys.readouterr().out
    assert "HOLD (by design)" in out
    assert "not a defect" in out


def test_designed_hold_banner_emits_actions_annotation(tmp_path, capsys, monkeypatch):
    root = tmp_path / "repo"
    config = _adopt_scratch(root, tmp_path / "kit")
    rel = _write_born_red_card(root, config)
    monkeypatch.setenv("GITHUB_ACTIONS", "true")
    assert cmd_check(root, strict=True, require_session_log=True, session_log=rel) == 1
    out = capsys.readouterr().out
    assert "::notice title=HOLD: session card in-progress (by design)::" in out


def test_no_hold_banner_outside_actions(tmp_path, capsys, monkeypatch):
    root = tmp_path / "repo"
    config = _adopt_scratch(root, tmp_path / "kit")
    rel = _write_born_red_card(root, config)
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
    assert cmd_check(root, strict=True, require_session_log=True, session_log=rel) == 1
    out = capsys.readouterr().out
    assert "HOLD (by design)" in out
    assert "::notice" not in out


def test_no_hold_banner_when_other_findings_exist(tmp_path, capsys):
    root = tmp_path / "repo"
    config = _adopt_scratch(root, tmp_path / "kit")
    rel = _write_born_red_card(root, config)
    # A REAL defect alongside the hold (heartbeat corrupted): the red is now
    # partially genuine and must never be labelled "by design".
    (root / "control" / "status.md").write_text(
        "# scratch · status\nphase: heartbeat deleted\n", encoding="utf-8"
    )
    assert cmd_check(root, strict=True, require_session_log=True, session_log=rel) == 1
    assert "HOLD (by design)" not in capsys.readouterr().out


def test_no_hold_banner_when_card_claims_complete(tmp_path, capsys):
    root = tmp_path / "repo"
    config = _adopt_scratch(root, tmp_path / "kit")
    # An incomplete card that CLAIMS complete is a real defect, not a
    # designed hold — the honesty condition is the card's own declaration.
    card = root / config.sessions_dir / "2026-07-11-liar.md"
    card.write_text("# liar\n\n> **Status:** `complete`\n", encoding="utf-8")
    rc = cmd_check(
        root,
        strict=True,
        require_session_log=True,
        session_log=Path(config.sessions_dir) / "2026-07-11-liar.md",
    )
    assert rc == 1
    assert "HOLD (by design)" not in capsys.readouterr().out
