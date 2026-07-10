"""Tests for src/build_release_json.py — the release workflow's guard + assets."""

from __future__ import annotations

import hashlib
import json

import build_release_json
from build_release_json import (
    build_release_json as build_json,
)
from build_release_json import (
    changelog_section,
    heading_anchor,
    kit_version,
    section_metadata,
    verify,
)

_CHANGELOG = """# Changelog

## [1.1.0] - 2026-08-01

### Added
- a thing

## [1.0.0] - 2026-07-09

First release.

### Added
- everything
"""


def test_kit_version_parses():
    assert len(kit_version().split(".")) == 3


def test_changelog_section_extracts_the_right_block():
    heading, body = changelog_section("1.0.0", _CHANGELOG)
    assert heading.startswith("## [1.0.0]")
    assert "everything" in body
    assert "a thing" not in body


def test_changelog_section_missing_returns_none():
    assert changelog_section("9.9.9", _CHANGELOG) is None


def test_heading_anchor_matches_github_style():
    assert heading_anchor("## [1.0.0] - 2026-07-09") == "100---2026-07-09"


def test_section_metadata_defaults():
    meta = section_metadata("no comment here", "1.2.0")
    assert meta == {
        "breaking": False,
        "requires_state_migration": False,
        "min_upgrade_from": "1.0.0",
    }


def test_section_metadata_comment_overrides():
    body = "<!-- release: breaking=true state_migration=true min_upgrade_from=1.1.0 -->"
    meta = section_metadata(body, "2.0.0")
    assert meta["breaking"] is True
    assert meta["requires_state_migration"] is True
    assert meta["min_upgrade_from"] == "1.1.0"


def test_verify_refuses_a_version_without_changelog_section():
    problems = verify("9.9.9")
    assert problems
    assert any("KIT_VERSION" in p for p in problems)
    assert any("CHANGELOG" in p for p in problems)


def test_verify_is_green_for_the_current_version():
    # The repo must always be releasable at its declared version: stamp,
    # CHANGELOG section, and dist all agree (this is the workflow's guard).
    assert verify(kit_version()) == []


def test_main_writes_the_three_assets_plus_notes(tmp_path, capsys):
    out = tmp_path / "assets"
    rc = build_release_json.main(
        ["--version", kit_version(), "--out", str(out)],
    )
    assert rc == 0
    dist_bytes = (out / "bootstrap.py").read_bytes()
    digest = hashlib.sha256(dist_bytes).hexdigest()
    sha_line = (out / "bootstrap.py.sha256").read_text(encoding="utf-8")
    assert sha_line == f"{digest}  bootstrap.py\n"
    payload = json.loads((out / "release.json").read_text(encoding="utf-8"))
    assert payload["version"] == kit_version()
    assert payload["sha256"] == digest
    assert payload["upgrade_steps"]
    assert payload["changelog_anchor"].startswith("https://github.com/")
    notes = (out / "notes.md").read_text(encoding="utf-8")
    assert notes.strip()
    # ORDER 003 (adopter-visibility band): every release's notes carry the
    # adopter upgrade checklist, version-stamped for THIS release, ending in
    # the `kit:` status-line self-report step (enforce, don't exhort — the
    # appender lives in main(), so an author cannot forget it).
    assert "## Adopter upgrade checklist" in notes
    assert f"kit: v{kit_version()}" in notes
    assert "{version}" not in notes
    # The checklist must name release.json next to bootstrap.py.new (idea
    # upgrade-checklist-release-json-placement): an operator following it to
    # the letter otherwise omits the file and the sha256 self-verification
    # silently skips — no tamper/corruption check, no signal it never ran.
    assert "release.json" in notes
    assert "silently skips" in notes


def test_main_refuses_on_version_mismatch(capsys):
    rc = build_release_json.main(["--version", "9.9.9", "--verify-only"])
    assert rc == 1
    assert "REFUSED" in capsys.readouterr().err
