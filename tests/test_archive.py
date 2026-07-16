"""Tests for the archive-ready note drafter (archive-ready close-out plan §5 S2)."""

from datetime import date

import pytest

from engine.checks.check_session_log import DRAFT_FILL_TOKEN
from engine.lib.config import Config, save_config
from engine.lib.state import JsonStateBackend, default_state
from engine.loop.archive import (
    REQUIRES_PROBE_TOKEN,
    archive_note_path,
    draft_archive_note,
    ensure_archive_draft,
)
from engine.loop.handoff import DRAFT_MARKER

TODAY = date.today().isoformat()
_RETRO_DIR_NAME = "retro"


def _init(root):
    config = Config()
    save_config(root, config)
    backend = JsonStateBackend(root / config.state_dir / "state.json")
    with backend.transaction():
        for key, value in default_state(config.project_id).items():
            backend.set(key, value)
    return config, backend


def _seed_evidence(root, config):
    """Plant the tree evidence the drafter harvests (plan §3)."""
    claims = root / config.claims_dir
    claims.mkdir(parents=True)
    (claims / "README.md").write_text("# claims\n", encoding="utf-8")
    (claims / "claude-live-work.md").write_text(
        "- `claude/live-work` · scope · files · 2026-07-16\n",
        encoding="utf-8",
    )
    control = root / "control"
    (control / "status.md").write_text(
        "# seat heartbeat\n"
        "updated: 2026-07-16T00:00Z\n\n"
        "\N{BLACK FLAG} P10 required-check swap\n"
        "WHAT: swap the required checks.\n\n"
        "- \N{BLACK FLAG} FOR OWNER REVIEW: failsafe discrepancy\n",
        encoding="utf-8",
    )
    (root / "CHANGELOG.md").write_text(
        "# Changelog\n\n## [Unreleased]\n\n### Added\n"
        "- archive-prep draft verb (S2).\n\n## [1.17.0] - 2026-07-14\n\n- old.\n",
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# Drafting — evidence fills what the tree proves
# ---------------------------------------------------------------------------


def test_draft_creates_note_with_evidence(tmp_path):
    config, _ = _init(tmp_path)
    _seed_evidence(tmp_path, config)
    lines = ensure_archive_draft(tmp_path, config)
    assert any("drafted" in line for line in lines)
    note = archive_note_path(tmp_path, config)
    assert note.is_file()
    text = note.read_text(encoding="utf-8")
    assert DRAFT_MARKER in text
    # Title slot: date filled from evidence, chat identity stays a slot.
    assert TODAY in text.splitlines()[0]
    # Claims evidence: the live claim is named; README.md is not a claim.
    assert "`claude-live-work.md`" in text
    assert "README.md" not in text.split("Claims:")[1].split("\n")[0]
    # Heartbeat ⚑ extraction: both flag lines carried, names only.
    assert "\N{BLACK FLAG} P10 required-check swap" in text
    assert "\N{BLACK FLAG} FOR OWNER REVIEW: failsafe discrepancy" in text
    # CHANGELOG [Unreleased] park.
    assert "archive-prep draft verb (S2)." in text
    # Judgment stays with the session: unresolved slots remain.
    assert DRAFT_FILL_TOKEN in text


def test_requires_probe_and_confirmation_never_prefilled(tmp_path):
    config, _ = _init(tmp_path)
    _seed_evidence(tmp_path, config)
    ensure_archive_draft(tmp_path, config)
    text = archive_note_path(tmp_path, config).read_text(encoding="utf-8")
    # The routine-state slot survives verbatim as an unresolved REQUIRES-PROBE
    # slot — a record-shaped default is the realized failure (plan §4.2).
    assert f"{DRAFT_FILL_TOKEN} {REQUIRES_PROBE_TOKEN}" in text
    assert "list triggers/routines LIVE" in text
    # The confirmation slot is never drafted as complete.
    assert "never drafted as complete" in text
    assert "writing it IS the final check]]" in text


def test_draft_with_no_evidence_fails_soft(tmp_path):
    config, _ = _init(tmp_path)  # no claims dir, no heartbeat, no CHANGELOG
    lines = ensure_archive_draft(tmp_path, config)
    assert any("drafted" in line for line in lines)
    text = archive_note_path(tmp_path, config).read_text(encoding="utf-8")
    assert "none at draft time" in text  # claims
    assert "none open" in text  # ⚑ items
    assert "nothing parked at draft time" in text  # payload


# ---------------------------------------------------------------------------
# Re-run — report, never redraft; complete notes are never touched
# ---------------------------------------------------------------------------


def test_rerun_reports_unresolved_slots_and_touches_nothing(tmp_path):
    config, _ = _init(tmp_path)
    _seed_evidence(tmp_path, config)
    ensure_archive_draft(tmp_path, config)
    note = archive_note_path(tmp_path, config)
    before = note.read_text(encoding="utf-8")
    lines = ensure_archive_draft(tmp_path, config)
    assert any("still unresolved" in line for line in lines)
    assert note.read_text(encoding="utf-8") == before
    # No second note was drafted.
    assert len(list(note.parent.glob("archive-ready-*.md"))) == 1


def test_complete_note_never_touched(tmp_path):
    config, _ = _init(tmp_path)
    note = archive_note_path(tmp_path, config)
    note.parent.mkdir(parents=True)
    complete = "# Archive-ready note — done\n\nAll slots resolved.\n"
    note.write_text(complete, encoding="utf-8")
    lines = ensure_archive_draft(tmp_path, config)
    assert any("never touched" in line for line in lines)
    assert note.read_text(encoding="utf-8") == complete


def test_prior_complete_note_drafts_todays(tmp_path):
    # A completed note from an earlier archive event does not block a new one.
    config, _ = _init(tmp_path)
    old = archive_note_path(tmp_path, config, day="2026-01-01")
    old.parent.mkdir(parents=True)
    old.write_text("# Archive-ready note — old\n\nResolved.\n", encoding="utf-8")
    lines = ensure_archive_draft(tmp_path, config)
    assert any("drafted" in line for line in lines)
    assert archive_note_path(tmp_path, config).is_file()
    assert old.read_text(encoding="utf-8").endswith("Resolved.\n")


def test_prior_unresolved_note_blocks_new_draft(tmp_path):
    # An unresolved note (any date) is reported, never superseded silently.
    config, _ = _init(tmp_path)
    old = archive_note_path(tmp_path, config, day="2026-01-01")
    old.parent.mkdir(parents=True)
    old.write_text(f"# note\n\n{DRAFT_FILL_TOKEN} pending]]\n", encoding="utf-8")
    lines = ensure_archive_draft(tmp_path, config)
    assert any("1 [[fill:]] slot(s) still unresolved" in line for line in lines)
    assert not archive_note_path(tmp_path, config).is_file()


# ---------------------------------------------------------------------------
# Fail-open + the CLI verb
# ---------------------------------------------------------------------------


def test_fail_open_returns_hand_copy_advisory(tmp_path):
    config, _ = _init(tmp_path)
    # docs/retro exists as a FILE: the draft write must fail, and the verb
    # must fail open with the hand-copy fallback instead of raising.
    (tmp_path / config.docs_root).mkdir(parents=True, exist_ok=True)
    (tmp_path / config.docs_root / "retro").write_text("not a dir", encoding="utf-8")
    lines = ensure_archive_draft(tmp_path, config)
    assert any("failed open" in line for line in lines)
    assert any("archive-ready.md.tmpl" in line for line in lines)


def test_draft_archive_note_composes_from_template(tmp_path):
    config, _ = _init(tmp_path)
    text = draft_archive_note(tmp_path, config, day="2026-02-03")
    assert text.startswith("# Archive-ready note — 2026-02-03")
    assert DRAFT_MARKER in text
    assert REQUIRES_PROBE_TOKEN in text


@pytest.fixture()
def wired(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    config, backend = _init(tmp_path)
    return tmp_path, config, backend


def test_archive_prep_verb(wired, capsys):
    from engine.cli import cmd_archive_prep

    root, config, _ = wired
    assert cmd_archive_prep(root) == 0
    out = capsys.readouterr().out
    assert "archive-prep: drafted" in out
    assert archive_note_path(root, config).is_file()
    # Second run: reports the unresolved slots, exits 0.
    assert cmd_archive_prep(root) == 0
    assert "still unresolved" in capsys.readouterr().out


def test_archive_prep_verb_requires_state(tmp_path, monkeypatch, capsys):
    from engine.cli import cmd_archive_prep

    monkeypatch.chdir(tmp_path)
    assert cmd_archive_prep(tmp_path) == 1
    assert "no state" in capsys.readouterr().out


def test_dist_flat_namespace_does_not_shadow_archive_symbols(tmp_path):
    """The single-file build must substitute evidence exactly like src does.

    Regression: the dist concatenates every module into ONE namespace, so a
    later module's same-named top-level symbol silently replaces an earlier
    one at runtime. First hit: ``check_template_sync._SLOT_RE`` (a ``${}``
    matcher, concatenated after ``loop/archive.py``) shadowed archive's
    ``[[fill:]]`` slot regex — src tests were green while the shipped dist
    drafted a note with ZERO evidence substituted. Drive the dist artifact
    end-to-end and assert the one behavior the shadowing killed.
    """
    import subprocess
    import sys

    import build_bootstrap

    boot = tmp_path / "bootstrap.py"
    boot.write_text(build_bootstrap.build(), encoding="utf-8")
    repo = tmp_path / "repo"
    repo.mkdir()
    init = subprocess.run(
        [sys.executable, str(boot), "init", "--target", str(repo)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert init.returncode == 0, init.stderr
    result = subprocess.run(
        [sys.executable, str(boot), "archive-prep", "--target", str(repo)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert "drafted" in result.stdout
    note = repo / "docs" / _RETRO_DIR_NAME / f"archive-ready-{TODAY}.md"
    text = note.read_text(encoding="utf-8")
    # Evidence substitution happened: the title slot carries today's date...
    assert text.splitlines()[0] == (
        f"# Archive-ready note — {TODAY} \N{MIDDLE DOT} "
        "[[fill: which chat/session is being archived]]"
    )
    # ...and the doctrine-guarded slots survive untouched.
    assert f"{DRAFT_FILL_TOKEN} {REQUIRES_PROBE_TOKEN}" in text
    assert "never drafted as complete" in text
