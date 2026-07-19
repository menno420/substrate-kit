"""Un-groomed-idea counter advisory (wave-2 groom S3).

Counts 💡 session-idea lines on ``.sessions/`` cards whose filename date is
strictly newer than the newest ``docs/planning/*groom*.md`` doc, so a "backlog
dry" claim can't be made while un-groomed ideas still sit on cards. Advisory
only (warn, never exit-affecting); input-gated + fail-open.
"""

from __future__ import annotations

from pathlib import Path

import pytest

pytest.importorskip("engine.checks.check_ungroomed_ideas")

from engine.checks.check_ungroomed_ideas import (  # noqa: E402
    UNGROOMED_IDEAS_KIND,
    check_ungroomed_ideas,
)

_IDEA = "\N{ELECTRIC LIGHT BULB}"


def _write_groom(root: Path, name: str) -> Path:
    d = root / "docs" / "planning"
    d.mkdir(parents=True, exist_ok=True)
    p = d / name
    p.write_text("# groom pass\n\n> **Status:** `complete`\n", encoding="utf-8")
    return p


def _write_card(root: Path, name: str, text: str) -> Path:
    d = root / ".sessions"
    d.mkdir(parents=True, exist_ok=True)
    p = d / name
    p.write_text(text, encoding="utf-8")
    return p


def test_newer_card_with_idea_fires(tmp_path: Path):
    _write_groom(tmp_path, "2026-07-10-idea-groom.md")
    _write_card(
        tmp_path,
        "2026-07-15-slug.md",
        f"# card\n\n> **Status:** `complete`\n\n## {_IDEA} Session idea\n\nAn idea.\n",
    )
    findings = check_ungroomed_ideas(tmp_path)
    assert len(findings) == 1
    assert findings[0].kind == UNGROOMED_IDEAS_KIND
    assert findings[0].path == ".sessions/"
    assert "1 un-groomed" in findings[0].message
    assert "2026-07-10-idea-groom.md" in findings[0].message


def test_multiple_idea_lines_counted(tmp_path: Path):
    _write_groom(tmp_path, "2026-07-10-idea-groom.md")
    _write_card(
        tmp_path,
        "2026-07-15-a.md",
        f"# a\n\n{_IDEA} one\n{_IDEA} two\n",
    )
    _write_card(tmp_path, "2026-07-16-b.md", f"# b\n\n{_IDEA} three\n")
    findings = check_ungroomed_ideas(tmp_path)
    assert len(findings) == 1
    assert "3 un-groomed" in findings[0].message


def test_no_newer_cards_is_silent(tmp_path: Path):
    # Card dated the SAME day as the groom doc is not strictly newer → silent.
    _write_groom(tmp_path, "2026-07-15-idea-groom.md")
    _write_card(tmp_path, "2026-07-15-slug.md", f"# card\n\n{_IDEA} idea\n")
    _write_card(tmp_path, "2026-07-10-older.md", f"# old\n\n{_IDEA} idea\n")
    assert check_ungroomed_ideas(tmp_path) == []


def test_newer_card_without_idea_is_silent(tmp_path: Path):
    _write_groom(tmp_path, "2026-07-10-idea-groom.md")
    _write_card(
        tmp_path,
        "2026-07-15-slug.md",
        "# card\n\n> **Status:** `complete`\n\nNo bulb here.\n",
    )
    assert check_ungroomed_ideas(tmp_path) == []


def test_readme_is_ignored(tmp_path: Path):
    _write_groom(tmp_path, "2026-07-10-idea-groom.md")
    _write_card(tmp_path, "README.md", f"# readme\n\n{_IDEA} not a session idea\n")
    # README carries no date prefix anyway, but it is skipped by name too.
    assert check_ungroomed_ideas(tmp_path) == []


def test_missing_sessions_dir_fails_open(tmp_path: Path):
    _write_groom(tmp_path, "2026-07-10-idea-groom.md")
    assert check_ungroomed_ideas(tmp_path) == []


def test_missing_groom_doc_fails_open(tmp_path: Path):
    # A newer card with an idea, but NO groom doc to date against → silent.
    _write_card(tmp_path, "2026-07-15-slug.md", f"# card\n\n{_IDEA} idea\n")
    (tmp_path / "docs" / "planning").mkdir(parents=True, exist_ok=True)
    assert check_ungroomed_ideas(tmp_path) == []


def test_missing_planning_dir_fails_open(tmp_path: Path):
    _write_card(tmp_path, "2026-07-15-slug.md", f"# card\n\n{_IDEA} idea\n")
    assert check_ungroomed_ideas(tmp_path) == []


def test_newest_groom_doc_wins(tmp_path: Path):
    # Two groom docs; the NEWER one is the cutoff, so a card between them counts
    # only if newer than the newest.
    _write_groom(tmp_path, "2026-07-01-idea-groom.md")
    _write_groom(tmp_path, "2026-07-14-idea-groom.md")
    _write_card(tmp_path, "2026-07-10-between.md", f"# b\n\n{_IDEA} stale-but-groomed\n")
    _write_card(tmp_path, "2026-07-16-after.md", f"# a\n\n{_IDEA} un-groomed\n")
    findings = check_ungroomed_ideas(tmp_path)
    assert len(findings) == 1
    assert "1 un-groomed" in findings[0].message
    assert "2026-07-14-idea-groom.md" in findings[0].message


def test_undated_card_is_skipped(tmp_path: Path):
    _write_groom(tmp_path, "2026-07-10-idea-groom.md")
    _write_card(tmp_path, "no-date-prefix.md", f"# nd\n\n{_IDEA} idea\n")
    assert check_ungroomed_ideas(tmp_path) == []


def test_not_in_strict_subchecks():
    guards = pytest.importorskip("engine.guards")
    assert UNGROOMED_IDEAS_KIND not in guards.STRICT_SUBCHECKS
    assert "check_ungroomed_ideas" not in guards.STRICT_SUBCHECKS
