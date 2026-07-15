"""Tests for scripts/check_taxonomy_sync.py — the taxonomy three-surface checker."""

from __future__ import annotations

import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import check_taxonomy_sync as cts  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[1]

_CLASSES = ("alpha work", "beta work", "gamma work")

_GRAMMAR = """\
SOMETHING_ELSE = ("x",)
MODEL_TASK_CLASSES = (
    "alpha work",
    "beta work",
    "gamma work",
)
MODEL_EFFORT_VALUES = ("low", "medium", "high")
"""

_LADDER = """\
# Model-for-task allocation ladder

## The ladder (seeded defaults)

| Task class (verbatim) | Default tier | Notes |
|---|---|---|
| alpha work | top tier | |
| beta work | workhorse ⚑ | flagged note |
| gamma work | *(observe-first)* | |

## Revision log

| Date | Row changed | Cited rows | By |
|---|---|---|---|
| 2026-07-09 | (seed) | — | band |
"""

_README = """\
# telemetry/

- `task_class` ∈ the 3 PL-004 classes verbatim (the founding
  set + amendments): alpha work · beta work ·
  gamma work.
- `tokens_out` is null until a meter exists.
"""


def _kinds(findings):
    return sorted({f.kind for f in findings})


def _make_repo(
    tmp_path: Path,
    grammar: str = _GRAMMAR,
    ladder: str = _LADDER,
    readme: str = _README,
) -> Path:
    engine = tmp_path / "src" / "engine"
    engine.mkdir(parents=True)
    (engine / "grammar.py").write_text(grammar, encoding="utf-8")
    telemetry = tmp_path / "telemetry"
    telemetry.mkdir()
    (telemetry / "allocation-ladder.md").write_text(ladder, encoding="utf-8")
    (telemetry / "README.md").write_text(readme, encoding="utf-8")
    return tmp_path


class TestParsers:
    def test_canonical_tuple_parses_in_order(self):
        assert cts.parse_canonical(_GRAMMAR) == list(_CLASSES)

    def test_ladder_first_column_strips_emphasis_and_flags(self):
        assert cts.parse_ladder(_LADDER) == list(_CLASSES)

    def test_ladder_ignores_the_revision_log_table(self):
        rows = cts.parse_ladder(_LADDER)
        assert "2026-07-09" not in rows

    def test_readme_bullet_yields_classes_and_count(self):
        classes, count = cts.parse_readme(_README)
        assert classes == list(_CLASSES)
        assert count == 3


class TestSetEquality:
    def test_clean_fixture_passes(self, tmp_path):
        assert cts.check_taxonomy(_make_repo(tmp_path)) == []

    def test_missing_ladder_row_fails(self, tmp_path):
        ladder = _LADDER.replace("| beta work | workhorse ⚑ | flagged note |\n", "")
        findings = cts.check_taxonomy(_make_repo(tmp_path, ladder=ladder))
        assert _kinds(findings) == ["ladder-missing-class"]
        assert "beta work" in findings[0].message

    def test_extra_or_typoed_ladder_row_fails(self, tmp_path):
        # A typo is both a missing canonical row and an extra unknown row.
        ladder = _LADDER.replace("| beta work |", "| beta wrok |")
        findings = cts.check_taxonomy(_make_repo(tmp_path, ladder=ladder))
        assert _kinds(findings) == ["ladder-extra-class", "ladder-missing-class"]

    def test_readme_class_drift_fails(self, tmp_path):
        readme = _README.replace("beta work ·\n  gamma work.", "gamma work.")
        findings = cts.check_taxonomy(_make_repo(tmp_path, readme=readme))
        assert "readme-missing-class" in _kinds(findings)

    def test_readme_count_drift_fails(self, tmp_path):
        readme = _README.replace("the 3 PL-004 classes", "the 9 PL-004 classes")
        findings = cts.check_taxonomy(_make_repo(tmp_path, readme=readme))
        assert _kinds(findings) == ["readme-count-drift"]


class TestParseFailuresAreFindings:
    def test_unparseable_grammar_is_a_finding(self, tmp_path):
        findings = cts.check_taxonomy(_make_repo(tmp_path, grammar="X = 1\n"))
        assert _kinds(findings) == ["grammar-unparsed"]

    def test_missing_ladder_section_is_a_finding(self, tmp_path):
        findings = cts.check_taxonomy(
            _make_repo(tmp_path, ladder="# ladder\n\nno table here\n"),
        )
        assert "ladder-unparsed" in _kinds(findings)

    def test_missing_readme_bullet_is_a_finding(self, tmp_path):
        findings = cts.check_taxonomy(
            _make_repo(tmp_path, readme="# telemetry\n\nno bullet\n"),
        )
        assert "readme-unparsed" in _kinds(findings)

    def test_missing_files_are_findings(self, tmp_path):
        engine = tmp_path / "src" / "engine"
        engine.mkdir(parents=True)
        (engine / "grammar.py").write_text(_GRAMMAR, encoding="utf-8")
        findings = cts.check_taxonomy(tmp_path)
        assert _kinds(findings) == ["missing-file"]
        assert len(findings) == 2


class TestRealRepo:
    def test_the_kit_repo_is_in_sync(self):
        # The whole point: the three live surfaces agree right now.
        assert cts.check_taxonomy(REPO_ROOT) == []

    def test_main_exit_codes(self, tmp_path, capsys):
        assert cts.main(["--root", str(_make_repo(tmp_path))]) == 0
        assert "OK" in capsys.readouterr().out
