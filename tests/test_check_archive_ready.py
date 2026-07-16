"""The archive-note completeness advisory (archive-ready close-out plan §5 S4).

Pins the slice's own spec: an `archive-ready-*.md` note carrying unresolved
``[[fill:]]`` slots OR guarded-slot residue (S3's sham-resolution class,
``probe_slot_residue`` reused, not reimplemented) fires a ``check --strict``
advisory that is never exit-affecting (plan §4.3 advisory-first, PL-008
unverified posture). Includes the plan-named **deliberate red fixture**: a
sham-resolved note (markers stripped, templated defaults kept) that must
fire through the full ``cmd_check`` path.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

pytest.importorskip("engine.hooks.settings")

from engine.checks.check_archive_ready import check_archive_ready
from engine.checks.check_session_log import DRAFT_FILL_TOKEN
from engine.cli import cmd_check
from engine.lib.config import Config
from engine.loop.archive import (
    ARCHIVE_TEMPLATE_NAME,
    REQUIRES_PROBE_TOKEN,
)
from engine.render import load_templates

_SLOT_STRIP_RE = re.compile(r"\[\[fill:(.*?)\]\]", re.DOTALL)


def _sham_resolve(text: str) -> str:
    """Strip every [[fill:]] marker pair but keep the templated default text."""
    return _SLOT_STRIP_RE.sub(lambda m: m.group(1), text)


def _wholesale_resolve(text: str) -> str:
    """Replace every [[fill:]] slot wholesale with plausible live output."""

    def replacement(match: re.Match[str]) -> str:
        body = match.group(1)
        if REQUIRES_PROBE_TOKEN in body:
            return (
                "Probed live at 2026-07-16T01:20Z via list_triggers "
                "(paginated, exhaustive): trig_01ABC · cron `0 */2 * * *` · "
                "ENABLED. Nothing else armed."
            )
        if "never drafted as complete" in body:
            return (
                "Attested after resolving every section above. "
                "Nothing remains chat-only."
            )
        return "resolved with live facts this session."

    return _SLOT_STRIP_RE.sub(replacement, text)


def _plant_note(root: Path, text: str, day: str = "2026-07-16") -> Path:
    note = root / "docs" / "retro" / f"archive-ready-{day}.md"
    note.parent.mkdir(parents=True, exist_ok=True)
    note.write_text(text, encoding="utf-8")
    return note


def _template() -> str:
    return load_templates()[ARCHIVE_TEMPLATE_NAME]


def test_unresolved_slots_fire(tmp_path: Path) -> None:
    """A raw draft (all slots live) is unresolved — one finding, counted."""
    template = _template()
    _plant_note(tmp_path, template)
    findings = check_archive_ready(tmp_path, Config())
    assert len(findings) == 1
    finding = findings[0]
    assert finding.kind == "archive-note-unresolved-slots"
    assert finding.path == "docs/retro/archive-ready-2026-07-16.md"
    assert f"{template.count(DRAFT_FILL_TOKEN)} [[fill:]] slot(s)" in finding.message
    assert "wholesale replacement" in finding.message


def test_sham_resolution_fires_residue(tmp_path: Path) -> None:
    """The S3 sham (markers stripped, defaults kept) is residue, not done."""
    _plant_note(tmp_path, _sham_resolve(_template()))
    findings = check_archive_ready(tmp_path, Config())
    assert len(findings) == 1
    finding = findings[0]
    assert finding.kind == "archive-note-slot-residue"
    assert f"routine-state ({REQUIRES_PROBE_TOKEN})" in finding.message
    assert "chat-only confirmation" in finding.message
    assert "NOT complete" in finding.message


def test_unresolved_takes_precedence_over_residue(tmp_path: Path) -> None:
    """A marker-carrying note is 'unresolved', never residue (S3 precedence)."""
    template = _template()
    # Sham-resolve only the guarded slots; leave every other slot live.
    def replacement(match: re.Match[str]) -> str:
        body = match.group(1)
        if REQUIRES_PROBE_TOKEN in body or "never drafted as complete" in body:
            return body  # markers stripped, default kept — residue-shaped
        return match.group(0)  # still a live slot

    _plant_note(tmp_path, _SLOT_STRIP_RE.sub(replacement, template))
    findings = check_archive_ready(tmp_path, Config())
    kinds = {f.kind for f in findings}
    assert kinds == {"archive-note-unresolved-slots"}


def test_wholesale_resolution_is_silent(tmp_path: Path) -> None:
    """A genuinely completed note (template preamble kept) contributes nothing."""
    _plant_note(tmp_path, _wholesale_resolve(_template()))
    assert check_archive_ready(tmp_path, Config()) == []


def test_hand_written_note_without_template_text_is_silent(tmp_path: Path) -> None:
    """The 2026-07-11 evidence-note class: no slots, no defaults — silent."""
    _plant_note(
        tmp_path,
        "# Archive-ready note — 2026-07-11\n\nHand-written close-out, "
        "fully resolved from live probes.\n",
        day="2026-07-11",
    )
    assert check_archive_ready(tmp_path, Config()) == []


def test_every_note_scanned_not_just_newest(tmp_path: Path) -> None:
    """An old half-resolved note is exactly the leak worth surfacing."""
    _plant_note(tmp_path, _template(), day="2026-01-01")
    _plant_note(tmp_path, _wholesale_resolve(_template()), day="2026-07-16")
    findings = check_archive_ready(tmp_path, Config())
    assert [f.path for f in findings] == [
        "docs/retro/archive-ready-2026-01-01.md",
    ]


def test_self_gates_without_notes(tmp_path: Path) -> None:
    """No retro dir / no archive-ready notes → the scan is a no-op."""
    assert check_archive_ready(tmp_path, Config()) == []
    (tmp_path / "docs" / "retro").mkdir(parents=True)
    (tmp_path / "docs" / "retro" / "other-retro.md").write_text(
        "# not an archive note\n", encoding="utf-8"
    )
    assert check_archive_ready(tmp_path, Config()) == []


def test_red_fixture_fires_through_cmd_check_never_exit_affecting(
    tmp_path: Path, capsys
) -> None:
    """The plan-named deliberate red fixture: the advisory fires end-to-end
    through ``cmd_check`` on a sham-resolved note, and the exit code is
    untouched (plan §4.3 advisory-first contract)."""
    _plant_note(tmp_path, _sham_resolve(_template()))
    code = cmd_check(tmp_path, strict=False)
    out = capsys.readouterr().out
    assert code == 0
    assert "archive-note advisory" in out
    assert "archive-note-slot-residue" in out
    assert "never exit-affecting" in out
