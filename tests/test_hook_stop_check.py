"""Tests for the Stop-hook session-close advisor (plan §5.B, Lane B7)."""

from datetime import date

from engine.hooks.stop_check import evaluate_stop
from engine.lib.config import Config, save_config
from engine.lib.state import JsonStateBackend, default_state

COMPLETE_LOG = (
    "# 2026-07-02-test session\n"
    "> **Status:** `complete`\n"
    "💡 Session idea: one genuine idea.\n"
    "⟲ Previous-session review: looked fine.\n"
    "- **📊 Model:** sonnet · medium · test writing\n"
)


def _init(root, **overrides):
    config = Config()
    save_config(root, config)
    backend = JsonStateBackend(root / config.state_dir / "state.json")
    with backend.transaction():
        for key, value in default_state(config.project_id).items():
            backend.set(key, value)
        for key, value in overrides.items():
            backend.set(key, value)
    return config, backend


def _mined_today():
    return {"active_count": 0, "last_mined": date.today().isoformat()}


def _write_log(root, config, text=COMPLETE_LOG):
    sessions = root / config.sessions_dir
    sessions.mkdir(parents=True, exist_ok=True)
    (sessions / "2026-07-02-test.md").write_text(text, encoding="utf-8")


# ---------------------------------------------------------------------------
# All clean
# ---------------------------------------------------------------------------


def test_all_clean_returns_empty(tmp_path):
    config, backend = _init(tmp_path, reflection_buffer=_mined_today())
    _write_log(tmp_path, config)
    assert evaluate_stop(tmp_path, config, backend) == []


# ---------------------------------------------------------------------------
# Each advisory fires on its own
# ---------------------------------------------------------------------------


def test_missing_session_log_advises(tmp_path):
    config, backend = _init(tmp_path, reflection_buffer=_mined_today())
    lines = evaluate_stop(tmp_path, config, backend)
    assert len(lines) == 1
    assert "no session log" in lines[0]


def test_incomplete_session_log_names_missing_markers(tmp_path):
    config, backend = _init(tmp_path, reflection_buffer=_mined_today())
    _write_log(tmp_path, config, "> **Status:** `in-progress`\n")
    lines = evaluate_stop(tmp_path, config, backend)
    assert len(lines) == 1
    assert "is missing" in lines[0]
    assert "Session idea" in lines[0]
    assert "Previous-session review" in lines[0]


def test_open_blocking_questions_advise(tmp_path):
    config, backend = _init(
        tmp_path,
        reflection_buffer=_mined_today(),
        open_questions=["q-verify-command"],
    )
    _write_log(tmp_path, config)
    lines = evaluate_stop(tmp_path, config, backend)
    assert len(lines) == 1
    assert "blocking question(s) open" in lines[0]
    assert "q-verify-command" in lines[0]


def test_compaction_due_advises(tmp_path):
    config, backend = _init(
        tmp_path,
        reflection_buffer=_mined_today(),
        session_count=20,
    )
    _write_log(tmp_path, config)
    lines = evaluate_stop(tmp_path, config, backend)
    assert len(lines) == 1
    assert "compaction due" in lines[0]


def test_unmined_reflections_advise(tmp_path):
    config, backend = _init(tmp_path)  # default buffer: last_mined None
    _write_log(tmp_path, config)
    lines = evaluate_stop(tmp_path, config, backend)
    assert lines == [
        "reflections unmined this session — run bootstrap reflect --mine",
    ]


# ---------------------------------------------------------------------------
# Combination + fail open
# ---------------------------------------------------------------------------


def test_multiple_advisories_stack(tmp_path):
    config, backend = _init(tmp_path, open_questions=["q-x"], session_count=20)
    lines = evaluate_stop(tmp_path, config, backend)
    assert len(lines) == 4  # log missing, open q, compaction, unmined
    assert any("no session log" in line for line in lines)
    assert any("blocking question" in line for line in lines)
    assert any("compaction due" in line for line in lines)
    assert any("reflections unmined" in line for line in lines)


def test_broken_backend_fails_open(tmp_path):
    class _NoData:
        pass

    config = Config()
    save_config(tmp_path, config)
    _write_log(tmp_path, config)
    lines = evaluate_stop(tmp_path, config, _NoData())
    # State-based checks degrade to empty state; the run never raises.
    assert isinstance(lines, list)
    assert any("reflections unmined" in line for line in lines)


# ---------------------------------------------------------------------------
# The control-status heartbeat advisory (band KL-8)
# ---------------------------------------------------------------------------


def _write_status(root, mtime=None):
    control = root / "control"
    control.mkdir(parents=True, exist_ok=True)
    status = control / "status.md"
    status.write_text("# x · status\nupdated: 2026-07-09T12:00Z\n", encoding="utf-8")
    if mtime is not None:
        import os

        os.utime(status, (mtime, mtime))
    return status


def test_status_not_overwritten_this_session_advises(tmp_path):
    config, backend = _init(
        tmp_path,
        reflection_buffer=_mined_today(),
        session_anchor={"ts": "2026-07-09T12:00:00", "epoch": 2_000_000_000.0},
    )
    _write_log(tmp_path, config)
    _write_status(tmp_path, mtime=1_000_000_000)  # older than the anchor
    lines = evaluate_stop(tmp_path, config, backend)
    assert len(lines) == 1
    assert "control/status.md not overwritten this session" in lines[0]


def test_status_touched_after_anchor_is_clean(tmp_path):
    config, backend = _init(
        tmp_path,
        reflection_buffer=_mined_today(),
        session_anchor={"ts": "2026-07-09T12:00:00", "epoch": 1_000_000_000.0},
    )
    _write_log(tmp_path, config)
    _write_status(tmp_path, mtime=2_000_000_000)  # newer than the anchor
    assert evaluate_stop(tmp_path, config, backend) == []


def test_status_advisory_skips_without_anchor_or_protocol(tmp_path):
    # No anchor -> no basis for the claim -> no advisory (fail-open)…
    config, backend = _init(tmp_path, reflection_buffer=_mined_today())
    _write_log(tmp_path, config)
    _write_status(tmp_path, mtime=1_000_000_000)
    assert evaluate_stop(tmp_path, config, backend) == []
    # …and no control/status.md -> nothing either, even with an anchor.
    config2, backend2 = _init(
        tmp_path / "bare",
        reflection_buffer=_mined_today(),
        session_anchor={"epoch": 1_000_000_000.0},
    )
    _write_log(tmp_path / "bare", config2)
    assert evaluate_stop(tmp_path / "bare", config2, backend2) == []


def test_status_multi_lane_any_fresh_lane_clears_the_advisory(tmp_path):
    # ORDER 004: a shared repo lists one heartbeat per lane; the hook cannot
    # know which lane this session is, so ANY fresh lane clears the nag.
    lanes = ["control/status-mining.md", "control/status-exploration.md"]
    config, backend = _init(
        tmp_path,
        reflection_buffer=_mined_today(),
        session_anchor={"ts": "2026-07-09T12:00:00", "epoch": 1_500_000_000.0},
    )
    config.heartbeat_files = list(lanes)
    save_config(tmp_path, config)
    _write_log(tmp_path, config)
    import os

    control = tmp_path / "control"
    control.mkdir(parents=True, exist_ok=True)
    for lane, mtime in zip(lanes, (1_000_000_000, 2_000_000_000)):
        f = tmp_path / lane
        f.write_text("# lane · status\nupdated: 2026-07-09T12:00Z\n", encoding="utf-8")
        os.utime(f, (mtime, mtime))
    assert evaluate_stop(tmp_path, config, backend) == []


def test_status_multi_lane_all_stale_advises_naming_every_lane(tmp_path):
    lanes = ["control/status-mining.md", "control/status-exploration.md"]
    config, backend = _init(
        tmp_path,
        reflection_buffer=_mined_today(),
        session_anchor={"ts": "2026-07-09T12:00:00", "epoch": 2_500_000_000.0},
    )
    config.heartbeat_files = list(lanes)
    save_config(tmp_path, config)
    _write_log(tmp_path, config)
    import os

    control = tmp_path / "control"
    control.mkdir(parents=True, exist_ok=True)
    for lane in lanes:
        f = tmp_path / lane
        f.write_text("# lane · status\nupdated: 2026-07-09T12:00Z\n", encoding="utf-8")
        os.utime(f, (1_000_000_000, 1_000_000_000))
    lines = evaluate_stop(tmp_path, config, backend)
    assert len(lines) == 1
    for lane in lanes:
        assert lane in lines[0]
