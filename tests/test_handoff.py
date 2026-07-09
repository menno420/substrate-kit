"""Tests for the auto-drafted session handoff (band KL-5, plan §10)."""

import json
import os
import time
from datetime import date

import pytest

from engine.checks.check_session_log import (
    DRAFT_FILL_TOKEN,
    check_log,
    status_in_progress,
    unresolved_fill_count,
)
from engine.lib.config import Config, save_config
from engine.lib.state import JsonStateBackend, default_state
from engine.loop.handoff import (
    DRAFT_MARKER,
    SESSION_ANCHOR_KEY,
    SessionEvidence,
    draft_card,
    draft_close_out,
    ensure_draft,
    gather_evidence,
    read_git_head,
    record_session_anchor,
)
from engine.loop.telemetry import parse_model_line

SHA_A = "a" * 40
SHA_B = "b" * 40


def _init(root, **state_overrides):
    config = Config()
    save_config(root, config)
    backend = JsonStateBackend(root / config.state_dir / "state.json")
    with backend.transaction():
        for key, value in default_state(config.project_id).items():
            backend.set(key, value)
        for key, value in state_overrides.items():
            backend.set(key, value)
    return config, backend


def _fake_git(root, sha=SHA_A, branch="main"):
    git = root / ".git"
    (git / "refs" / "heads").mkdir(parents=True)
    (git / "HEAD").write_text(f"ref: refs/heads/{branch}\n", encoding="utf-8")
    (git / "refs" / "heads" / branch).write_text(sha + "\n", encoding="utf-8")
    return git


def _anchor(backend, epoch=0.0, head=SHA_A, branch="main", ts=None):
    backend.set(
        SESSION_ANCHOR_KEY,
        {
            "ts": ts or f"{date.today().isoformat()}T00:00:00+00:00",
            "epoch": epoch,
            "head": head,
            "branch": branch,
        },
    )


# ---------------------------------------------------------------------------
# Git HEAD reading — pure file parsing
# ---------------------------------------------------------------------------


def test_read_git_head_loose_ref(tmp_path):
    _fake_git(tmp_path)
    assert read_git_head(tmp_path) == ("main", SHA_A)


def test_read_git_head_packed_ref(tmp_path):
    git = tmp_path / ".git"
    git.mkdir()
    (git / "HEAD").write_text("ref: refs/heads/main\n", encoding="utf-8")
    (git / "packed-refs").write_text(
        f"# pack-refs with: peeled\n{SHA_B} refs/heads/main\n",
        encoding="utf-8",
    )
    assert read_git_head(tmp_path) == ("main", SHA_B)


def test_read_git_head_detached(tmp_path):
    git = tmp_path / ".git"
    git.mkdir()
    (git / "HEAD").write_text(SHA_A + "\n", encoding="utf-8")
    assert read_git_head(tmp_path) == (None, SHA_A)


def test_read_git_head_worktree_gitdir_file(tmp_path):
    # A worktree checkout: .git is a FILE pointing at the per-worktree dir,
    # whose commondir points back at the shared .git (where refs live).
    shared = tmp_path / "shared.git"
    (shared / "refs" / "heads").mkdir(parents=True)
    (shared / "refs" / "heads" / "main").write_text(SHA_B + "\n", encoding="utf-8")
    wt_git = tmp_path / "worktrees" / "wt1"
    wt_git.mkdir(parents=True)
    (wt_git / "HEAD").write_text("ref: refs/heads/main\n", encoding="utf-8")
    (wt_git / "commondir").write_text(str(shared) + "\n", encoding="utf-8")
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / ".git").write_text(f"gitdir: {wt_git}\n", encoding="utf-8")
    assert read_git_head(repo) == ("main", SHA_B)


def test_read_git_head_no_git_fails_open(tmp_path):
    assert read_git_head(tmp_path) == (None, None)


# ---------------------------------------------------------------------------
# The session-start anchor
# ---------------------------------------------------------------------------


def test_record_session_anchor_records_head(tmp_path):
    config, backend = _init(tmp_path)
    _fake_git(tmp_path)
    record_session_anchor(tmp_path, config, backend)
    anchor = backend.data[SESSION_ANCHOR_KEY]
    assert anchor["head"] == SHA_A
    assert anchor["branch"] == "main"
    assert anchor["ts"][:10] == date.today().isoformat()
    assert isinstance(anchor["epoch"], float)


def test_record_session_anchor_same_day_keeps_original(tmp_path):
    config, backend = _init(tmp_path)
    _fake_git(tmp_path)
    record_session_anchor(tmp_path, config, backend)
    first = backend.data[SESSION_ANCHOR_KEY]
    record_session_anchor(tmp_path, config, backend)
    assert backend.data[SESSION_ANCHOR_KEY] == first


def test_record_session_anchor_stale_day_overwritten(tmp_path):
    config, backend = _init(tmp_path)
    _fake_git(tmp_path)
    _anchor(backend, ts="2020-01-01T00:00:00+00:00", head=SHA_B)
    record_session_anchor(tmp_path, config, backend)
    anchor = backend.data[SESSION_ANCHOR_KEY]
    assert anchor["ts"][:10] == date.today().isoformat()
    assert anchor["head"] == SHA_A


def test_record_session_anchor_fails_open_on_broken_backend(tmp_path):
    config, _ = _init(tmp_path)

    class Broken:
        @property
        def data(self):
            raise RuntimeError("boom")

    record_session_anchor(tmp_path, config, Broken())  # must not raise


# ---------------------------------------------------------------------------
# Evidence gathering
# ---------------------------------------------------------------------------


def test_gather_evidence_classifies_changed_files(tmp_path):
    config, backend = _init(tmp_path)
    _fake_git(tmp_path)
    _anchor(backend, epoch=time.time() - 60)
    (tmp_path / "app.py").write_text("x = 1\n", encoding="utf-8")
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_app.py").write_text("y = 2\n", encoding="utf-8")
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "note.md").write_text("hi\n", encoding="utf-8")
    (tmp_path / ".sessions").mkdir()
    (tmp_path / ".sessions" / "2026-07-09-x.md").write_text("log\n", encoding="utf-8")
    (tmp_path / "data.csv").write_text("a,b\n", encoding="utf-8")
    evidence = gather_evidence(tmp_path, config, dict(backend.data))
    assert evidence.changed["code"] == ["app.py"]
    assert evidence.changed["tests"] == [os.path.join("tests", "test_app.py")]
    assert evidence.changed["docs"] == [os.path.join("docs", "note.md")]
    assert evidence.changed["sessions"] == [os.path.join(".sessions", "2026-07-09-x.md")]
    # substrate.config.json (written by _init after the anchor) rides along —
    # config edits are legitimate session evidence.
    assert evidence.changed["other"] == ["data.csv", "substrate.config.json"]
    assert evidence.head_start == SHA_A
    assert evidence.head_now == SHA_A
    assert evidence.branch == "main"


def test_gather_evidence_skips_state_dir_and_git(tmp_path):
    config, backend = _init(tmp_path)
    _fake_git(tmp_path)
    _anchor(backend, epoch=0.0)
    evidence = gather_evidence(tmp_path, config, dict(backend.data))
    flat = [p for paths in evidence.changed.values() for p in paths]
    assert not any(p.startswith(config.state_dir) for p in flat)
    assert not any(p.startswith(".git") for p in flat)


def test_gather_evidence_reads_verify_command_slot(tmp_path):
    config, backend = _init(
        tmp_path,
        slot_values={"verify_command": {"value": "python3 -m pytest", "source": "derived"}},
    )
    evidence = gather_evidence(tmp_path, config, dict(backend.data))
    assert evidence.verify_command == "python3 -m pytest"


def test_gather_evidence_no_anchor_scans_nothing(tmp_path):
    config, backend = _init(tmp_path)
    (tmp_path / "app.py").write_text("x = 1\n", encoding="utf-8")
    evidence = gather_evidence(tmp_path, config, dict(backend.data))
    assert evidence.anchor_epoch is None
    assert evidence.changed == {}


# ---------------------------------------------------------------------------
# Draft composition
# ---------------------------------------------------------------------------


def test_draft_close_out_carries_marker_and_slots():
    evidence = SessionEvidence(
        anchor_ts="t",
        anchor_epoch=1.0,
        branch="main",
        head_start=SHA_A,
        head_now=SHA_B,
        verify_command="pytest",
        changed={"code": ["app.py"]},
    )
    text = draft_close_out(evidence)
    assert DRAFT_MARKER in text
    assert "`app.py`" in text
    assert "commits made this session" in text
    assert "run `pytest`" in text
    assert "Decisions made:" in text
    assert "Next session should know:" in text
    assert unresolved_fill_count(text) >= 3


def test_draft_close_out_renders_missing_markers():
    text = draft_close_out(SessionEvidence(), Config().session_markers)
    assert "💡 Session idea" in text
    assert "Previous-session review" in text
    assert "**📊 Model:**" in text
    # The drafted Model stand-in must never harvest into the PL-004 feed.
    assert parse_model_line(text) is None


def test_draft_card_is_drafted_and_holds_the_gate(tmp_path):
    config = Config()
    text = draft_card("2026-07-09 — session", SessionEvidence(), config)
    assert text.startswith("# Session 2026-07-09")
    assert status_in_progress(text)  # `drafted` is an in-progress token
    path = tmp_path / "card.md"
    path.write_text(text, encoding="utf-8")
    missing = check_log(path, config.session_markers)
    assert any("[[fill:]] slot(s) unresolved" in m for m in missing)
    assert any("in-progress" in m for m in missing)
    # Every default marker needle is present (the stand-ins carry them) —
    # only the fill slots + status hold the gate.
    assert not any(m in ("Session idea", "Previous-session review", "Model line") for m in missing)


def test_completed_card_with_no_fills_passes():
    config = Config()
    text = (
        "# card\n> **Status:** `complete`\n💡 idea\nprevious-session review: ok\n"
        "- **📊 Model:** sonnet · medium · test writing\n"
    )
    assert unresolved_fill_count(text) == 0
    assert not status_in_progress(text)
    assert DRAFT_FILL_TOKEN not in text
    del config


# ---------------------------------------------------------------------------
# ensure_draft — the orchestrator
# ---------------------------------------------------------------------------


def test_ensure_draft_creates_skeleton_when_card_missing(tmp_path):
    config, backend = _init(tmp_path)
    _anchor(backend, epoch=time.time() - 60)
    lines = ensure_draft(tmp_path, config, backend)
    assert len(lines) == 1
    assert "auto-drafted" in lines[0]
    cards = list((tmp_path / config.sessions_dir).glob("*.md"))
    assert len(cards) == 1
    text = cards[0].read_text(encoding="utf-8")
    assert DRAFT_MARKER in text
    assert status_in_progress(text)


def test_ensure_draft_appends_close_out_to_in_progress_card(tmp_path):
    config, backend = _init(tmp_path)
    _anchor(backend, epoch=0.0)
    sessions = tmp_path / config.sessions_dir
    sessions.mkdir()
    card = sessions / f"{date.today().isoformat()}-work.md"
    card.write_text("# work\n> **Status:** `in-progress`\nstuff\n", encoding="utf-8")
    lines = ensure_draft(tmp_path, config, backend)
    assert len(lines) == 1
    assert "appended" in lines[0]
    text = card.read_text(encoding="utf-8")
    assert text.startswith("# work\n")  # original content preserved
    assert DRAFT_MARKER in text
    assert "💡 Session idea" in text  # missing markers drafted as stand-ins


def test_ensure_draft_reports_unresolved_slots_without_reappending(tmp_path):
    config, backend = _init(tmp_path)
    _anchor(backend, epoch=0.0)
    ensure_draft(tmp_path, config, backend)  # creates the skeleton
    card = next((tmp_path / config.sessions_dir).glob("*.md"))
    before = card.read_text(encoding="utf-8")
    lines = ensure_draft(tmp_path, config, backend)
    assert len(lines) == 1
    assert "still unresolved" in lines[0]
    assert card.read_text(encoding="utf-8") == before  # never double-drafted


def test_ensure_draft_never_touches_completed_card(tmp_path):
    config, backend = _init(tmp_path)
    _anchor(backend, epoch=0.0)
    sessions = tmp_path / config.sessions_dir
    sessions.mkdir()
    card = sessions / "2026-07-09-done.md"
    complete = (
        "# done\n> **Status:** `complete`\n💡 idea\nprevious-session review: ok\n"
        "- **📊 Model:** sonnet · medium · test writing\n"
    )
    card.write_text(complete, encoding="utf-8")
    assert ensure_draft(tmp_path, config, backend) == []
    assert card.read_text(encoding="utf-8") == complete


def test_ensure_draft_skips_card_when_only_status_flip_remains(tmp_path):
    config, backend = _init(tmp_path)
    _anchor(backend, epoch=0.0)
    sessions = tmp_path / config.sessions_dir
    sessions.mkdir()
    card = sessions / "2026-07-09-ready.md"
    ready = (
        "# ready\n> **Status:** `in-progress`\n💡 idea\nprevious-session review: ok\n"
        "- **📊 Model:** sonnet · medium · test writing\n"
    )
    card.write_text(ready, encoding="utf-8")
    assert ensure_draft(tmp_path, config, backend) == []
    assert card.read_text(encoding="utf-8") == ready


def test_ensure_draft_treats_pre_session_card_as_missing(tmp_path):
    config, backend = _init(tmp_path)
    sessions = tmp_path / config.sessions_dir
    sessions.mkdir()
    old = sessions / "2026-07-01-old.md"
    old.write_text("# old\n> **Status:** `complete`\n", encoding="utf-8")
    past = time.time() - 3600
    os.utime(old, (past, past))
    _anchor(backend, epoch=time.time() - 60)
    lines = ensure_draft(tmp_path, config, backend)
    assert len(lines) == 1
    assert "was missing" in lines[0]
    assert old.read_text(encoding="utf-8").startswith("# old")  # untouched
    assert len(list(sessions.glob("*.md"))) == 2


def test_ensure_draft_fails_open(tmp_path):
    config, _ = _init(tmp_path)

    class Broken:
        @property
        def data(self):
            raise RuntimeError("boom")

    # No sessions dir, broken backend: must return advisories or [] — never raise.
    lines = ensure_draft(tmp_path, config, Broken())
    assert isinstance(lines, list)


# ---------------------------------------------------------------------------
# Telemetry guard — the drafted Model line never harvests
# ---------------------------------------------------------------------------


def test_parse_model_line_skips_drafted_stand_in():
    drafted = "- **📊 Model:** [[fill: model]] · [[fill: effort]] · [[fill: task-class]]\n"
    assert parse_model_line(drafted) is None
    real = drafted + "- **📊 Model:** sonnet · medium · test writing\n"
    parsed = parse_model_line(real)
    assert parsed is not None
    assert parsed["model"] == "sonnet"


# ---------------------------------------------------------------------------
# CLI wiring — hook + session-close + the draft verb
# ---------------------------------------------------------------------------


@pytest.fixture()
def wired(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    config, backend = _init(tmp_path)
    _fake_git(tmp_path)
    _anchor(backend, epoch=time.time() - 60)
    return tmp_path, config, backend


def test_hook_stopcheck_drafts_missing_card(wired, capsys):
    from engine.cli import cmd_hook

    root, config, _ = wired
    assert cmd_hook(root, "stopcheck") == 0
    cards = list((root / config.sessions_dir).glob("*.md"))
    assert len(cards) == 1
    assert DRAFT_MARKER in cards[0].read_text(encoding="utf-8")
    assert "auto-drafted" in capsys.readouterr().err


def test_session_close_drafts_and_reports(wired, capsys):
    from engine.cli import cmd_session_close

    root, config, _ = wired
    assert cmd_session_close(root) == 0
    out = capsys.readouterr().out
    assert "session-close: [draft]" in out
    assert list((root / config.sessions_dir).glob("*.md"))


def test_draft_verb(wired, capsys):
    from engine.cli import cmd_draft

    root, config, _ = wired
    assert cmd_draft(root) == 0
    assert "auto-drafted" in capsys.readouterr().out
    # Second run: reports the unresolved slots, exits 0.
    assert cmd_draft(root) == 0
    assert "still unresolved" in capsys.readouterr().out


def test_sessionstart_hook_records_anchor(tmp_path, monkeypatch):
    from engine.cli import cmd_hook

    monkeypatch.chdir(tmp_path)
    config, backend = _init(tmp_path)
    _fake_git(tmp_path)
    assert cmd_hook(tmp_path, "sessionstart") == 0
    fresh = JsonStateBackend(tmp_path / config.state_dir / "state.json")
    anchor = fresh.data.get(SESSION_ANCHOR_KEY)
    assert isinstance(anchor, dict)
    assert anchor["head"] == SHA_A
    del backend


def test_state_json_round_trips_anchor(tmp_path):
    config, backend = _init(tmp_path)
    _fake_git(tmp_path)
    record_session_anchor(tmp_path, config, backend)
    raw = json.loads(
        (tmp_path / config.state_dir / "state.json").read_text(encoding="utf-8"),
    )
    assert raw[SESSION_ANCHOR_KEY]["branch"] == "main"

def test_unresolved_fill_count_ignores_code_spans_and_fences():
    prose = "the checker counts `[[fill:]]` slots\n```\n[[fill: in a fence]]\n```\n"
    assert unresolved_fill_count(prose) == 0
    assert unresolved_fill_count(prose + "- Decisions made: [[fill: real slot]]\n") == 1
