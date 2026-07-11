"""Tests for the SessionStart orientation composer (plan §5.B, Lane B7)."""

from engine.hooks.session_start import compose_orientation
from engine.lib.config import Config, save_config
from engine.lib.state import JsonStateBackend, default_state
from engine.loop.reflections import REFLECTIONS_FILENAME, add_reflection


def _init(root, *, mode="guided", config=None, **overrides):
    config = config or Config()
    save_config(root, config)
    backend = JsonStateBackend(root / config.state_dir / "state.json")
    with backend.transaction():
        for key, value in default_state(config.project_id).items():
            backend.set(key, value)
        backend.set("mode", mode)
        for key, value in overrides.items():
            backend.set(key, value)
    return config, backend


def _add_lessons(root, config, count):
    path = root / config.state_dir / REFLECTIONS_FILENAME
    for n in range(count):
        add_reflection(
            path,
            lesson=f"lesson {n}",
            evidence=f"log:{n}",
            tags=["test"],
            buffer_size=10,
        )


# ---------------------------------------------------------------------------
# Depth: guided → standard
# ---------------------------------------------------------------------------


def test_guided_standard_renders_core_sections(tmp_path):
    config, backend = _init(tmp_path)
    text = compose_orientation(tmp_path, config, backend)
    assert "# Session orientation" in text
    assert "mode: guided" in text
    assert "In-scope actions" in text  # stance briefing
    assert "Active practices:" in text
    assert "Questions this session" in text


def test_guided_quota_suffix_counts_hidden_pending(tmp_path):
    # 13 bank questions pending, guided quota 3 → "(+10 more later)".
    config, backend = _init(tmp_path)
    text = compose_orientation(tmp_path, config, backend)
    assert "(+10 more later)" in text


def test_guided_trigger_block_mandates(tmp_path):
    config, backend = _init(tmp_path, open_questions=["q-verify-command"])
    text = compose_orientation(tmp_path, config, backend)
    assert "MANDATORY" in text
    assert "blocking question(s) open" in text


def test_standard_caps_lessons_at_three(tmp_path):
    config, backend = _init(tmp_path)
    _add_lessons(tmp_path, config, 5)
    text = compose_orientation(tmp_path, config, backend)
    assert "Learned lessons" in text
    assert text.count("- [R-") == 3


# ---------------------------------------------------------------------------
# Depth: active → full
# ---------------------------------------------------------------------------


def test_active_full_uncaps_lessons(tmp_path):
    config, backend = _init(tmp_path, mode="active")
    _add_lessons(tmp_path, config, 5)
    text = compose_orientation(tmp_path, config, backend)
    assert text.count("- [R-") == 5


def test_active_full_asks_everything_no_suffix(tmp_path):
    config, backend = _init(tmp_path, mode="active")
    text = compose_orientation(tmp_path, config, backend)
    assert "Questions this session" in text
    assert "more later" not in text


def test_full_gauges_advisory_lists_only_over_cap(tmp_path):
    config = Config()
    config.economy["gauges"] = [
        {"name": "pile", "kind": "count_cap", "glob": "docs/*.md", "cap": 0},
        {"name": "calm", "kind": "count_cap", "glob": "notes/*.md", "cap": 99},
    ]
    config, backend = _init(tmp_path, mode="active", config=config)
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "a.md").write_text("# hi\n", encoding="utf-8")
    text = compose_orientation(tmp_path, config, backend)
    assert "Economy advisory" in text
    assert "pile" in text
    assert "calm" not in text


def test_gauges_section_skipped_when_none_over(tmp_path):
    config, backend = _init(tmp_path, mode="active")
    text = compose_orientation(tmp_path, config, backend)
    assert "Economy advisory" not in text


# ---------------------------------------------------------------------------
# Depth: observe → minimal (observe imposes nothing)
# ---------------------------------------------------------------------------


def test_observe_minimal_omits_imposing_sections(tmp_path):
    config, backend = _init(
        tmp_path,
        mode="observe",
        slot_values={"owner_profile": {"value": "short bullets"}},
    )
    _add_lessons(tmp_path, config, 2)
    text = compose_orientation(tmp_path, config, backend)
    assert "mode: observe" in text
    assert "In-scope actions" not in text  # no stance briefing
    assert "How the owner works" not in text
    assert "Learned lessons" not in text
    assert "Active practices" not in text
    assert "Questions this session" not in text


def test_observe_minimal_trigger_block_is_advisory(tmp_path):
    config, backend = _init(tmp_path, mode="observe", open_questions=["q-x"])
    text = compose_orientation(tmp_path, config, backend)
    assert "Trigger advisory (non-mandatory)" in text
    assert "MANDATORY" not in text


def test_observe_workflow_proposal_when_due(tmp_path):
    config, backend = _init(tmp_path, mode="observe", session_count=5)
    text = compose_orientation(tmp_path, config, backend)
    assert "Proposed workflow" in text
    assert "guided" in text
    assert "active" in text


def test_observe_no_proposal_before_due(tmp_path):
    config, backend = _init(tmp_path, mode="observe", session_count=2)
    text = compose_orientation(tmp_path, config, backend)
    assert "Proposed workflow" not in text


# ---------------------------------------------------------------------------
# Handoff push (the B1 run-4/run-5 continuity-null fix)
# ---------------------------------------------------------------------------


def _write_card(root, config, name, text):
    sessions = root / config.sessions_dir
    sessions.mkdir(parents=True, exist_ok=True)
    (sessions / name).write_text(text, encoding="utf-8")


def test_handoff_pushes_newest_card_with_status_and_slots(tmp_path):
    config, backend = _init(tmp_path)
    _write_card(
        tmp_path,
        config,
        "2026-07-10-session.md",
        "# Session\n\n> **Status:** `drafted`\n\n"
        "- Decisions made: [[fill: decisions taken this session, or none]]\n"
        "- Next session should know: [[fill: the handoff pointer]]\n",
    )
    text = compose_orientation(tmp_path, config, backend)
    assert "## Handoff" in text
    assert "`.sessions/2026-07-10-session.md`" in text
    assert "status: in-progress/drafted" in text
    assert "2 unresolved [[fill:]] slot(s)" in text
    # The unresolved pointer slot is NOT pushed — a template slot is noise.
    assert "Next session should know: [[fill:" not in text
    assert "Open that card FIRST" in text


def test_handoff_extracts_resolved_pointer_from_complete_card(tmp_path):
    config, backend = _init(tmp_path)
    _write_card(
        tmp_path,
        config,
        "2026-07-10-session.md",
        "# Session\n\n> **Status:** `complete`\n\n"
        "- Next session should know: the budgets read-hook lives in store.py\n",
    )
    text = compose_orientation(tmp_path, config, backend)
    assert "status: complete" in text
    assert "unresolved [[fill:]]" not in text
    assert "Next session should know: the budgets read-hook lives in store.py" in text


def test_handoff_takes_last_resolved_pointer(tmp_path):
    config, backend = _init(tmp_path)
    _write_card(
        tmp_path,
        config,
        "2026-07-10-session.md",
        "# Session\n\n> **Status:** `complete`\n\n"
        "- Next session should know: older pointer\n\n"
        "- Next session should know: newest pointer wins\n",
    )
    text = compose_orientation(tmp_path, config, backend)
    assert "Next session should know: newest pointer wins" in text
    assert "older pointer" not in text


def test_handoff_pointer_excerpt_is_capped(tmp_path):
    config, backend = _init(tmp_path)
    _write_card(
        tmp_path,
        config,
        "2026-07-10-session.md",
        "# Session\n\n> **Status:** `complete`\n\n"
        f"- Next session should know: {'x' * 600}\n",
    )
    text = compose_orientation(tmp_path, config, backend)
    line = next(l for l in text.splitlines() if "Next session should know:" in l)
    assert len(line) < 350
    assert line.endswith("…")


def test_handoff_skipped_when_no_cards(tmp_path):
    config, backend = _init(tmp_path)
    text = compose_orientation(tmp_path, config, backend)
    assert "## Handoff" not in text


def test_handoff_skips_sessions_readme(tmp_path):
    config, backend = _init(tmp_path)
    _write_card(tmp_path, config, "README.md", "# how cards work\n")
    text = compose_orientation(tmp_path, config, backend)
    assert "## Handoff" not in text


def test_handoff_renders_at_observe_minimal_depth(tmp_path):
    config, backend = _init(tmp_path, mode="observe")
    _write_card(
        tmp_path,
        config,
        "2026-07-10-session.md",
        "# Session\n\n> **Status:** `complete`\n",
    )
    text = compose_orientation(tmp_path, config, backend)
    assert "## Handoff" in text
    assert "In-scope actions" not in text  # minimal still omits imposing sections


def test_handoff_renders_right_after_status_header(tmp_path):
    config, backend = _init(tmp_path)
    _write_card(
        tmp_path,
        config,
        "2026-07-10-session.md",
        "# Session\n\n> **Status:** `complete`\n",
    )
    text = compose_orientation(tmp_path, config, backend)
    assert text.index("# Session orientation") < text.index("## Handoff")
    assert text.index("## Handoff") < text.index("In-scope actions")


def test_unreadable_card_drops_handoff_not_composition(tmp_path):
    config, backend = _init(tmp_path)
    _write_card(
        tmp_path,
        config,
        "2026-07-10-session.md",
        "# Session\n\n> **Status:** `complete`\n",
    )
    (tmp_path / config.sessions_dir / "2026-07-10-session.md").chmod(0o000)
    try:
        text = compose_orientation(tmp_path, config, backend)
    finally:
        (tmp_path / config.sessions_dir / "2026-07-10-session.md").chmod(0o644)
    assert "# Session orientation" in text  # composition survives


# ---------------------------------------------------------------------------
# Section order + resilience
# ---------------------------------------------------------------------------


def test_user_style_renders_before_lessons(tmp_path):
    config, backend = _init(
        tmp_path,
        slot_values={"owner_profile": {"value": "Short bullets, no fluff."}},
    )
    _add_lessons(tmp_path, config, 1)
    text = compose_orientation(tmp_path, config, backend)
    assert "How the owner works" in text
    assert "Short bullets, no fluff." in text
    assert text.index("How the owner works") < text.index("Learned lessons")


def test_user_style_skipped_when_unfilled(tmp_path):
    config, backend = _init(tmp_path)
    text = compose_orientation(tmp_path, config, backend)
    assert "How the owner works" not in text


def test_corrupt_reflections_file_does_not_break_composition(tmp_path):
    config, backend = _init(tmp_path)
    state_dir = tmp_path / config.state_dir
    (state_dir / REFLECTIONS_FILENAME).write_text("{not json", encoding="utf-8")
    text = compose_orientation(tmp_path, config, backend)
    assert "# Session orientation" in text
    assert "Learned lessons" not in text


def test_raising_section_is_dropped_not_fatal(tmp_path, monkeypatch):
    def _boom(*_args, **_kwargs):
        raise RuntimeError("gauge meltdown")

    monkeypatch.setattr("engine.hooks.session_start.economy_gauges", _boom)
    config, backend = _init(tmp_path, mode="active")
    text = compose_orientation(tmp_path, config, backend)
    assert "# Session orientation" in text
    assert "Questions this session" in text  # later sections still render


def test_empty_backend_fails_open(tmp_path):
    config = Config()
    save_config(tmp_path, config)
    backend = JsonStateBackend(tmp_path / config.state_dir / "state.json")
    text = compose_orientation(tmp_path, config, backend)
    assert "# Session orientation" in text
