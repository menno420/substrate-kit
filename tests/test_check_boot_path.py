"""check_boot_path — the boot pointer chain resolves, or it reds.

Covers the three legs (agreement present, boot section present, every listed
path on disk) plus the false-positive discipline that keeps this checker
DETERMINISTIC: backticked prose is not a path, and a bare tree is silent.
"""

from __future__ import annotations

from pathlib import Path

from engine.checks.check_boot_path import check_boot_path
from engine.lib.config import Config


def _write(root: Path, rel: str, text: str) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _agreement(body: str) -> str:
    return f"# proj — constitution\n\n> **Status:** `binding`\n\n{body}\n"


BOOT = """## Boot read path

1. This file — the working agreement.
2. `docs/current-state.md` — the living ledger.
3. `docs/CAPABILITIES.md` — verified capabilities.
"""


def test_bare_tree_is_silent(tmp_path: Path) -> None:
    """Pre-adoption is not broken — `adopt` is what plants an agreement."""
    assert check_boot_path(tmp_path, Config()) == []


def test_missing_agreement_reds(tmp_path: Path) -> None:
    """The original 2026-07-12 class: the router names a file that is absent."""
    _write(tmp_path, "docs/current-state.md", "x")
    findings = check_boot_path(tmp_path, Config())
    assert [f.kind for f in findings] == ["boot-agreement-missing"]


def test_agreement_without_boot_section_reds(tmp_path: Path) -> None:
    """The 2026-08-06 class — 5 of 11 adopters.

    The pointer resolves to a real file and then dead-ends, because the 07-12
    fix repointed the router at the agreement before the agreement had a list.
    """
    _write(tmp_path, "CONSTITUTION.md", _agreement("## Working agreement\n\n- be good\n"))
    findings = check_boot_path(tmp_path, Config())
    assert [f.kind for f in findings] == ["boot-section-missing"]


def test_resolved_boot_path_is_clean(tmp_path: Path) -> None:
    _write(tmp_path, "CONSTITUTION.md", _agreement(BOOT))
    _write(tmp_path, "docs/current-state.md", "x")
    _write(tmp_path, "docs/CAPABILITIES.md", "x")
    assert check_boot_path(tmp_path, Config()) == []


def test_unresolved_entry_reds_and_names_it(tmp_path: Path) -> None:
    _write(tmp_path, "CONSTITUTION.md", _agreement(BOOT))
    _write(tmp_path, "docs/current-state.md", "x")
    # docs/CAPABILITIES.md deliberately absent
    findings = check_boot_path(tmp_path, Config())
    assert [f.kind for f in findings] == ["boot-path-unresolved"]
    assert "docs/CAPABILITIES.md" in findings[0].message


def test_backticked_prose_is_not_a_path(tmp_path: Path) -> None:
    """The false-positive discipline that keeps this deterministic.

    A checker that treats every backticked token as a path is the
    `skill_grounds` failure mode — nine findings naming `READ FIRST` and a
    numpy expression as unresolved commands. That class is what the advisory
    census exists to keep OUT of the agent's channel, so this checker must not
    reproduce it.
    """
    body = """## Boot read path

1. Read this file and flip the card to `complete` when done.
2. Run it with `--strict` and never `$?` after a pipe.
3. `docs/current-state.md` — the living ledger.
"""
    _write(tmp_path, "CONSTITUTION.md", _agreement(body))
    _write(tmp_path, "docs/current-state.md", "x")
    assert check_boot_path(tmp_path, Config()) == []


def test_alternate_heading_phrasings_are_accepted(tmp_path: Path) -> None:
    """A repo calling it "Reading order" is not defective."""
    for heading in ("## Reading order", "## Start every session", "## Boot set"):
        root = tmp_path / heading.replace("#", "").replace(" ", "_").strip("_")
        root.mkdir(parents=True, exist_ok=True)
        _write(root, "CONSTITUTION.md", _agreement(f"{heading}\n\n1. This file.\n"))
        assert check_boot_path(root, Config()) == [], heading


def test_prose_after_the_section_cannot_manufacture_a_finding(tmp_path: Path) -> None:
    """Only list lines inside the section are scanned for paths."""
    body = """## Boot read path

1. This file.

## Autonomy rails

See `docs/does-not-exist.md` for the rider.
"""
    _write(tmp_path, "CONSTITUTION.md", _agreement(body))
    assert check_boot_path(tmp_path, Config()) == []
