"""Tests for the session-card sham-resolution advisory (KL-5 generalization).

The checker (``engine.checks.check_card_residue``) puts the S3 residue
verdict on the session-card surface via the shared ``engine.lib.residue``
core — advisory-only, never exit-affecting (PL-008 posture, mirroring how
S4 introduced the archive advisory). The deliberate red fixture drives a
sham-resolved card through ``cmd_check`` end-to-end; the ``ensure_draft``
test covers the same verdict at the Stop-hook/session-close seam.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

pytest.importorskip("engine.hooks.settings")

from engine.checks.check_card_residue import check_card_residue
from engine.cli import cmd_check
from engine.lib.config import Config, save_config
from engine.lib.state import JsonStateBackend, default_state
from engine.loop.handoff import SessionEvidence, draft_card, ensure_draft

_SLOT_STRIP_RE = re.compile(r"\[\[fill:\s*(.*?)\]\]", re.DOTALL)


# The drafted badge block (three lines, with the flip instruction) — the
# sham replaces it wholesale with a clean complete badge, exactly what an
# agent gaming the gate would write.
_DRAFT_BADGE_BLOCK = (
    "> **Status:** `drafted` *(auto-drafted by substrate-kit — edit the\n"
    "> close-out, resolve every `[[fill:]]` slot, then flip this badge to\n"
    "> `complete`.)*"
)


def _sham_card() -> str:
    """A drafted card with every marker stripped, hints kept, badge flipped —
    the exact card that passes the token-counting gate today."""
    text = draft_card("2026-07-16 — sham", SessionEvidence(), Config())
    assert _DRAFT_BADGE_BLOCK in text  # fixture tracks the real draft badge
    text = text.replace(_DRAFT_BADGE_BLOCK, "> **Status:** `complete`")
    return _SLOT_STRIP_RE.sub(r"\1", text)


_GENUINE_CARD = (
    "# Session 2026-07-16 — real\n\n> **Status:** `complete`\n\n"
    "- **📊 Model:** fable-5 · medium · test writing\n"
    "- verify: ran the suite, green.\n\n"
    "## 💡 Session idea\n\nA real idea.\n\n"
    "## ⟲ Previous-session review\n\nA real remark, previous-session review.\n"
)


def _plant_card(root: Path, text: str, name: str = "2026-07-16-card.md") -> Path:
    sessions = root / Config().sessions_dir
    sessions.mkdir(parents=True, exist_ok=True)
    path = sessions / name
    path.write_text(text, encoding="utf-8")
    return path


def test_sham_card_passes_the_token_counting_gate(tmp_path: Path) -> None:
    """The corridor this advisory exists for: the merge-blocking session gate
    counts ``[[fill:]]`` tokens only, so the sham card reads COMPLETE to it —
    zero findings. If this ever starts failing, the gate learned to see
    residue and the advisory has graduated (update the checker docstring)."""
    from engine.checks.check_session_log import check_log

    card = _plant_card(tmp_path, _sham_card())
    assert check_log(card, Config().session_markers) == []


def test_sham_card_fires_naming_guilty_slots(tmp_path: Path) -> None:
    _plant_card(tmp_path, _sham_card())
    findings = check_card_residue(tmp_path, Config())
    assert len(findings) == 1
    assert findings[0].kind == "session-card-slot-residue"
    assert findings[0].path == ".sessions/2026-07-16-card.md"
    assert "session idea" in findings[0].message
    assert "previous-session review" in findings[0].message
    assert "wholesale" in findings[0].message


def test_drafted_card_with_intact_slots_is_skipped(tmp_path: Path) -> None:
    """Unresolved slots are the gate's drafted-vs-completed report, not residue."""
    _plant_card(tmp_path, draft_card("2026-07-16 — draft", SessionEvidence(), Config()))
    assert check_card_residue(tmp_path, Config()) == []


def test_in_progress_card_is_skipped(tmp_path: Path) -> None:
    """A mid-flight card is judged only once it declares itself finished."""
    sham = _sham_card().replace("`complete`", "`in-progress`")
    _plant_card(tmp_path, sham)
    assert check_card_residue(tmp_path, Config()) == []


def test_readme_and_genuine_cards_are_silent(tmp_path: Path) -> None:
    _plant_card(tmp_path, _GENUINE_CARD)
    _plant_card(tmp_path, _sham_card(), name="README.md")
    assert check_card_residue(tmp_path, Config()) == []


def test_self_gates_without_sessions_dir(tmp_path: Path) -> None:
    assert check_card_residue(tmp_path, Config()) == []


def test_every_card_scanned_not_just_newest(tmp_path: Path) -> None:
    """An old sham card is exactly the leak worth surfacing."""
    _plant_card(tmp_path, _sham_card(), name="2026-01-01-old-sham.md")
    _plant_card(tmp_path, _GENUINE_CARD, name="2026-07-16-new-real.md")
    findings = check_card_residue(tmp_path, Config())
    assert [f.path for f in findings] == [".sessions/2026-01-01-old-sham.md"]


def test_red_fixture_fires_through_cmd_check_never_exit_affecting(
    tmp_path: Path, capsys
) -> None:
    """The deliberate red fixture for the card surface: the advisory fires
    end-to-end through ``cmd_check`` on a sham-resolved card, and the exit
    code is untouched (advisory-first contract, S4 pattern)."""
    _plant_card(tmp_path, _sham_card())
    code = cmd_check(tmp_path, strict=False)
    out = capsys.readouterr().out
    assert code == 0
    assert "session-card residue advisory" in out
    assert "session-card-slot-residue" in out
    assert "never exit-affecting" in out


def test_ensure_draft_reports_sham_card_and_touches_nothing(tmp_path: Path) -> None:
    """The Stop-hook/session-close seam gives the same verdict the archive
    verb gives a sham note (S3 semantics on the card surface)."""
    config = Config()
    save_config(tmp_path, config)
    backend = JsonStateBackend(tmp_path / config.state_dir / "state.json")
    with backend.transaction():
        for key, value in default_state(config.project_id).items():
            backend.set(key, value)
    card = _plant_card(tmp_path, _sham_card())
    before = card.read_text(encoding="utf-8")
    lines = ensure_draft(tmp_path, config, backend)
    assert len(lines) == 1
    assert "hint text survives" in lines[0]
    assert "wholesale" in lines[0]
    assert card.read_text(encoding="utf-8") == before  # report, never touch
