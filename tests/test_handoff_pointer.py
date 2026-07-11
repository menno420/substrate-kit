"""Tests for the pull-visible handoff pointer (the B1 run-6 delivery-gap fix).

Run-6 (PR #201) proved the SessionStart handoff-push stops at the
orchestrator — delegated workers saw it in 0/3. The pointer file delivers the
same trail through the working-tree surfaces workers actually touch
(``git status`` / ``ls``): a kit-regenerated, marker-guarded ``HANDOFF.md``
at repo root, untracked by design.
"""

from engine.hooks.session_start import compose_orientation
from engine.lib.config import Config, save_config
from engine.lib.state import JsonStateBackend, default_state
from engine.loop.handoff import ensure_draft
from engine.loop.handoff_pointer import (
    HANDOFF_POINTER_FILENAME,
    HANDOFF_POINTER_MARKER,
    handoff_lines,
    write_handoff_pointer,
)


def _init(root, *, mode="guided", **overrides):
    config = Config()
    save_config(root, config)
    backend = JsonStateBackend(root / config.state_dir / "state.json")
    with backend.transaction():
        for key, value in default_state(config.project_id).items():
            backend.set(key, value)
        backend.set("mode", mode)
        for key, value in overrides.items():
            backend.set(key, value)
    return config, backend


def _write_card(root, config, name, text):
    sessions = root / config.sessions_dir
    sessions.mkdir(parents=True, exist_ok=True)
    (sessions / name).write_text(text, encoding="utf-8")


_CARD = (
    "# Session\n\n> **Status:** `drafted`\n\n"
    "- Decisions made: [[fill: decisions taken this session, or none]]\n"
    "- Next session should know: the budgets read-hook lives in store.py\n"
)


# ---------------------------------------------------------------------------
# write_handoff_pointer — the file surface
# ---------------------------------------------------------------------------


def test_pointer_file_written_with_marker_card_and_trail(tmp_path):
    config, _ = _init(tmp_path)
    _write_card(tmp_path, config, "2026-07-10-session.md", _CARD)
    note = write_handoff_pointer(tmp_path, config)
    assert note is not None
    path = tmp_path / HANDOFF_POINTER_FILENAME
    text = path.read_text(encoding="utf-8")
    assert HANDOFF_POINTER_MARKER in text
    assert "# HANDOFF — the previous session's trail" in text
    assert "`.sessions/2026-07-10-session.md`" in text
    assert "status: in-progress/drafted, 1 unresolved [[fill:]] slot(s)" in text
    assert "Next session should know: the budgets read-hook lives in store.py" in text
    assert "Open that card FIRST" in text
    assert "never commit or edit it" in text


def test_pointer_file_stays_lean(tmp_path):
    # The push's orchestrator-side footprint is ~113 words; the file must be
    # comparable or smaller (the B1 M1 lesson — a fat artifact makes the
    # regression worse).
    config, _ = _init(tmp_path)
    _write_card(tmp_path, config, "2026-07-10-session.md", _CARD)
    write_handoff_pointer(tmp_path, config)
    text = (tmp_path / HANDOFF_POINTER_FILENAME).read_text(encoding="utf-8")
    assert len(text.split()) <= 113


def test_pointer_matches_orientation_push_lines(tmp_path):
    # One composer, two surfaces: every pushed handoff bullet appears
    # byte-identically in the pointer file — the surfaces can never drift.
    config, backend = _init(tmp_path)
    _write_card(tmp_path, config, "2026-07-10-session.md", _CARD)
    write_handoff_pointer(tmp_path, config)
    pushed = compose_orientation(tmp_path, config, backend)
    pulled = (tmp_path / HANDOFF_POINTER_FILENAME).read_text(encoding="utf-8")
    for line in handoff_lines(tmp_path, config):
        assert line in pushed
        assert line in pulled


def test_pointer_refreshes_when_newer_card_lands(tmp_path):
    config, _ = _init(tmp_path)
    _write_card(tmp_path, config, "2026-07-10-session.md", _CARD)
    write_handoff_pointer(tmp_path, config)
    _write_card(
        tmp_path,
        config,
        "2026-07-11-session.md",
        "# Session\n\n> **Status:** `complete`\n",
    )
    note = write_handoff_pointer(tmp_path, config)
    assert note is not None
    text = (tmp_path / HANDOFF_POINTER_FILENAME).read_text(encoding="utf-8")
    assert "2026-07-11-session.md" in text
    assert "2026-07-10-session.md" not in text


def test_pointer_unchanged_content_is_a_silent_noop(tmp_path):
    config, _ = _init(tmp_path)
    _write_card(tmp_path, config, "2026-07-10-session.md", _CARD)
    assert write_handoff_pointer(tmp_path, config) is not None
    assert write_handoff_pointer(tmp_path, config) is None  # no rewrite churn


def test_no_session_card_writes_nothing(tmp_path):
    config, _ = _init(tmp_path)
    assert write_handoff_pointer(tmp_path, config) is None
    assert not (tmp_path / HANDOFF_POINTER_FILENAME).exists()


def test_stale_kit_pointer_removed_when_cards_vanish(tmp_path):
    config, _ = _init(tmp_path)
    _write_card(tmp_path, config, "2026-07-10-session.md", _CARD)
    write_handoff_pointer(tmp_path, config)
    (tmp_path / config.sessions_dir / "2026-07-10-session.md").unlink()
    note = write_handoff_pointer(tmp_path, config)
    assert note is not None and "removed" in note
    assert not (tmp_path / HANDOFF_POINTER_FILENAME).exists()


def test_host_owned_handoff_md_is_never_touched(tmp_path):
    config, _ = _init(tmp_path)
    host = "# My own handoff notes\n\nhands off\n"
    (tmp_path / HANDOFF_POINTER_FILENAME).write_text(host, encoding="utf-8")
    _write_card(tmp_path, config, "2026-07-10-session.md", _CARD)
    assert write_handoff_pointer(tmp_path, config) is None
    assert (tmp_path / HANDOFF_POINTER_FILENAME).read_text(encoding="utf-8") == host


def test_host_owned_handoff_md_is_never_deleted(tmp_path):
    config, _ = _init(tmp_path)  # no session cards at all
    host = "# My own handoff notes\n"
    (tmp_path / HANDOFF_POINTER_FILENAME).write_text(host, encoding="utf-8")
    assert write_handoff_pointer(tmp_path, config) is None
    assert (tmp_path / HANDOFF_POINTER_FILENAME).read_text(encoding="utf-8") == host


def test_pointer_fails_open_on_unreadable_card(tmp_path, monkeypatch):
    # chmod tricks are unreliable under a root test runner — force the read
    # failure at the seam instead. Fail-open contract: no raise, no file.
    config, _ = _init(tmp_path)
    _write_card(tmp_path, config, "2026-07-10-session.md", _CARD)

    def _boom(_):
        raise OSError("unreadable card")

    monkeypatch.setattr("engine.loop.handoff_pointer.latest_session_log", _boom)
    assert write_handoff_pointer(tmp_path, config) is None
    assert not (tmp_path / HANDOFF_POINTER_FILENAME).exists()


# ---------------------------------------------------------------------------
# Seam wiring — the pointer rides every boot and every draft
# ---------------------------------------------------------------------------


def test_ensure_draft_refreshes_pointer_after_drafting(tmp_path):
    # The Stop-hook seam: a session that wrote nothing still leaves both the
    # drafted card AND a pointer naming it for the next cold session.
    config, backend = _init(tmp_path)
    (tmp_path / config.sessions_dir).mkdir(parents=True, exist_ok=True)
    ensure_draft(tmp_path, config, backend)
    text = (tmp_path / HANDOFF_POINTER_FILENAME).read_text(encoding="utf-8")
    assert HANDOFF_POINTER_MARKER in text
    assert "-session.md" in text  # the just-drafted skeleton card


def test_ensure_draft_advisory_contract_unchanged(tmp_path):
    # The silent-refresh rule: the pointer write never adds advisory lines.
    config, backend = _init(tmp_path)
    _write_card(
        tmp_path,
        config,
        "2026-07-10-session.md",
        "# Session\n\n> **Status:** `complete`\n\n- **📊 Model:** x · y · z\n",
    )
    assert ensure_draft(tmp_path, config, backend) == []
    assert (tmp_path / HANDOFF_POINTER_FILENAME).exists()


# ---------------------------------------------------------------------------
# The auto-derived evidence trail (B1 run-8 content-gap fix)
# ---------------------------------------------------------------------------
# Run-8 report §2: ON-T4 "`cat .sessions/2026-07-11-session.md`" returned an
# unfilled draft, so ON's real context came from reading `cli.py` — the
# pointer converted into a skeleton. When the card's own pointer is still an
# unresolved slot, the pointer file carries the draft's auto-collected
# EVIDENCE (files touched, HEAD movement, commit subjects) itself.

_DRAFT_CARD = (
    "# Session\n\n> **Status:** `drafted`\n\n"
    "<!-- substrate:auto-draft -->\n\n"
    "- code touched (2): `deltareading/cli.py`, `deltareading/ops.py`\n"
    "- tests touched (1): `tests/test_deltareading.py`\n"
    "- git: branch `master`, HEAD unchanged at 70408b0d6 (nothing committed yet).\n"
    '- commits this session (1): "add report command"\n'
    "- verify: run `python3 -m pytest tests/ -q` and record the result → "
    "[[fill: verify result]]\n"
    "- Decisions made: [[fill: decisions taken this session, or none]]\n"
    "- Next session should know: [[fill: the handoff pointer — where to pick up]]\n"
)


def test_trail_surfaces_draft_evidence_when_pointer_unresolved(tmp_path):
    config, _ = _init(tmp_path)
    _write_card(tmp_path, config, "2026-07-11-session.md", _DRAFT_CARD)
    write_handoff_pointer(tmp_path, config)
    text = (tmp_path / HANDOFF_POINTER_FILENAME).read_text(encoding="utf-8")
    assert "- code touched (2): `deltareading/cli.py`" in text
    assert "- git: branch `master`, HEAD unchanged" in text
    assert '"add report command"' in text
    # Unresolved-slot lines never ride the trail (noise, not handoff) — the
    # header's "N unresolved [[fill:]] slot(s)" count note is the one
    # legitimate mention; no real slot (`[[fill: hint]]`) may appear.
    assert "[[fill: " not in text
    assert "Next session should know" not in text


def test_trail_absent_when_pointer_resolved(tmp_path):
    config, _ = _init(tmp_path)
    _write_card(tmp_path, config, "2026-07-11-session.md", _CARD)
    write_handoff_pointer(tmp_path, config)
    text = (tmp_path / HANDOFF_POINTER_FILENAME).read_text(encoding="utf-8")
    # The resolved human pointer wins; no evidence trail alongside.
    assert "Next session should know: the budgets read-hook lives in store.py" in text
    assert "code touched" not in text


def test_trail_pointer_file_stays_lean(tmp_path):
    # Even carrying the trail, the pointer must hold the ~113-word budget
    # (the push footprint the bench pins — a fat artifact worsens M1).
    config, _ = _init(tmp_path)
    _write_card(tmp_path, config, "2026-07-11-session.md", _DRAFT_CARD)
    write_handoff_pointer(tmp_path, config)
    text = (tmp_path / HANDOFF_POINTER_FILENAME).read_text(encoding="utf-8")
    assert len(text.split()) <= 113


def test_trail_caps_lines_and_length(tmp_path):
    from engine.loop.handoff_pointer import (
        _TRAIL_CHAR_CAP,
        _TRAIL_LINE_CAP,
        evidence_trail,
    )

    text = (
        "- code touched (1): `" + "x" * 300 + "`\n"
        "- tests touched (1): `t`\n"
        "- docs touched (1): `d`\n"
        "- other touched (1): `o`\n"
        "- sessions touched (1): `s`\n"
        "- git: branch `main`, HEAD moved.\n"
    )
    trail = evidence_trail(text)
    assert len(trail) == _TRAIL_LINE_CAP
    assert all(len(line) <= _TRAIL_CHAR_CAP for line in trail)
    assert trail[0].endswith("…")
