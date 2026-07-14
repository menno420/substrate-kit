"""Tests for scripts/check_changelog_structure.py — the [Unreleased] shape checker."""

from __future__ import annotations

import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import check_changelog_structure as ccs  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[1]

GOOD = """# Changelog

Header prose about the format.

## [Unreleased]

**Benchmark outcome (KF-5 — travels into the next release's notes):** prose
block in the preamble, spanning lines at column zero, which is exactly
where it belongs.

### Added

- **A new capability (PR #1).** Wrapped continuation lines are
  indented in the house style.

### Fixed

- A fix entry.

## [1.0.0] - 2026-07-01

Anything down here is history and is never scanned — even a
stray paragraph.

### Fixed
### Fixed
"""


def _kinds(findings):
    return sorted({f.kind for f in findings})


class TestExtract:
    def test_finds_section_and_stops_at_next(self):
        body, start = ccs.extract_unreleased(GOOD)
        text = "\n".join(body)
        assert "Benchmark outcome" in text
        assert "history" not in text
        assert start == 6  # first body line after `## [Unreleased]` (line 5)

    def test_missing_section(self):
        assert ccs.extract_unreleased("# Changelog\n\n## [1.0.0] - x\n") is None


class TestCleanShapes:
    def test_good_document_is_clean(self):
        assert ccs.check_unreleased(GOOD) == []

    def test_real_repo_changelog_is_born_green(self):
        findings = ccs.check_changelog(REPO_ROOT)
        assert findings == [], findings

    def test_empty_unreleased_is_clean(self):
        assert ccs.check_unreleased("## [Unreleased]\n\n## [1.0.0] - x\n") == []

    def test_preamble_only_is_clean(self):
        text = "## [Unreleased]\n\nJust a prose preamble, no entries yet.\n"
        assert ccs.check_unreleased(text) == []


class TestFindings:
    def test_missing_unreleased(self):
        findings = ccs.check_unreleased("# Changelog\n\n## [1.0.0] - x\n")
        assert _kinds(findings) == ["missing-unreleased"]

    def test_unknown_heading(self):
        text = "## [Unreleased]\n\n### Notes\n\n- entry\n"
        findings = ccs.check_unreleased(text)
        assert _kinds(findings) == ["unknown-heading"]

    def test_duplicate_heading(self):
        text = "## [Unreleased]\n\n### Added\n\n- a\n\n### Fixed\n\n- f\n\n### Added\n\n- b\n"
        findings = ccs.check_unreleased(text)
        assert "duplicate-heading" in _kinds(findings)

    def test_heading_order(self):
        text = "## [Unreleased]\n\n### Fixed\n\n- f\n\n### Added\n\n- a\n"
        findings = ccs.check_unreleased(text)
        assert _kinds(findings) == ["heading-order"]

    def test_early_bullet(self):
        text = "## [Unreleased]\n\n- an entry above any heading\n\n### Added\n\n- a\n"
        findings = ccs.check_unreleased(text)
        assert _kinds(findings) == ["early-bullet"]

    def test_finding_names_expected_layout(self):
        text = "## [Unreleased]\n\n### Fixed\n\n- f\n\n### Added\n\n- a\n"
        (finding,) = ccs.check_unreleased(text)
        assert "keep-a-changelog order" in finding.message
        assert "### Added" in finding.message

    def test_missing_file(self, tmp_path):
        findings = ccs.check_changelog(tmp_path)
        assert _kinds(findings) == ["missing-file"]


class TestMutationArc:
    """The release-cut friction end to end: malformed fires, corrected is clean."""

    MALFORMED = """## [Unreleased]

### Added

- an entry.

**Benchmark outcome (KF-5):** block accumulated at the section TAIL, the
shape that gets hand-moved at every release cut.

## [1.0.0] - x
"""

    CORRECTED = """## [Unreleased]

**Benchmark outcome (KF-5):** block moved to the preamble, where the cut
lifts it verbatim.

### Added

- an entry.

## [1.0.0] - x
"""

    def test_malformed_fires_tail_prose(self):
        findings = ccs.check_unreleased(self.MALFORMED)
        assert _kinds(findings) == ["tail-prose"]
        (finding,) = findings
        assert "PREAMBLE" in finding.message

    def test_corrected_is_clean(self):
        assert ccs.check_unreleased(self.CORRECTED) == []

    def test_duplicate_arc(self):
        malformed = "## [Unreleased]\n\n### Added\n\n- new\n\n### Fixed\n\n- f\n\n### Added\n\n- old\n"
        assert "duplicate-heading" in _kinds(ccs.check_unreleased(malformed))
        corrected = "## [Unreleased]\n\n### Added\n\n- new\n- old\n\n### Fixed\n\n- f\n"
        assert ccs.check_unreleased(corrected) == []


class TestFalsePositiveGuards:
    def test_code_fence_contents_are_skipped(self):
        text = (
            "## [Unreleased]\n\n### Added\n\n- entry:\n\n"
            "```\n### Fixed\nprose in a fence\n- bullet in a fence\n```\n"
        )
        assert ccs.check_unreleased(text) == []

    def test_lazy_continuation_not_flagged(self):
        # A col-0 line directly under a non-blank bullet line is a lazy
        # markdown continuation, not a new paragraph — never fires.
        text = "## [Unreleased]\n\n### Added\n\n- a long entry that wraps\nlazily at column zero.\n"
        assert ccs.check_unreleased(text) == []

    def test_indented_continuation_not_flagged(self):
        text = "## [Unreleased]\n\n### Added\n\n- entry\n\n  indented continuation paragraph.\n"
        assert ccs.check_unreleased(text) == []

    def test_released_sections_never_scanned(self):
        text = "## [Unreleased]\n\n### Added\n\n- a\n\n## [1.0.0] - x\n\n### Fixed\n### Fixed\n\nstray prose\n"
        assert ccs.check_unreleased(text) == []


class TestMain:
    def test_main_green_on_repo(self, capsys):
        assert ccs.main(["--root", str(REPO_ROOT)]) == 0
        assert "OK" in capsys.readouterr().out

    def test_main_red_on_bad_tree(self, tmp_path, capsys):
        (tmp_path / "CHANGELOG.md").write_text(
            "## [Unreleased]\n\n### Fixed\n\n- f\n\n### Added\n\n- a\n",
            encoding="utf-8",
        )
        assert ccs.main(["--root", str(tmp_path)]) == 1
        out = capsys.readouterr().out
        assert "heading-order" in out
        assert "1 finding(s)" in out
