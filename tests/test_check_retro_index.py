"""Tests for scripts/check_retro_index.py — the docs/retro reachability checker."""

from __future__ import annotations

import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import check_retro_index as cri  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[1]


def _kinds(findings):
    return sorted({f.kind for f in findings})


def _make_repo(tmp_path: Path, readme: str | None, files: dict[str, str]) -> Path:
    retro = tmp_path / "docs" / "retro"
    retro.mkdir(parents=True)
    if readme is not None:
        (retro / "README.md").write_text(readme, encoding="utf-8")
    for name, text in files.items():
        (retro / name).write_text(text, encoding="utf-8")
    return tmp_path


class TestIndexConsistency:
    def test_clean_tree_passes(self, tmp_path):
        root = _make_repo(
            tmp_path,
            "# retro\n\n- [a](retro-a-2026-07-01.md)\n- [q](QUESTIONS.md)\n",
            {"retro-a-2026-07-01.md": "body", "QUESTIONS.md": "questions"},
        )
        assert cri.check_retro(root) == []

    def test_unindexed_file_fails(self, tmp_path):
        # The PR #76 class: a retro file on disk with no README line.
        root = _make_repo(
            tmp_path,
            "# retro\n\n- [a](retro-a-2026-07-01.md)\n",
            {"retro-a-2026-07-01.md": "body", "addendum-2026-07-09.md": "orphan"},
        )
        findings = cri.check_retro(root)
        assert _kinds(findings) == ["not-indexed"]
        assert findings[0].path == "docs/retro/addendum-2026-07-09.md"

    def test_dangling_link_fails(self, tmp_path):
        root = _make_repo(
            tmp_path,
            "# retro\n\n- [gone](never-existed.md)\n",
            {},
        )
        assert _kinds(cri.check_retro(root)) == ["dangling-link"]

    def test_parent_relative_link_resolves(self, tmp_path):
        # The real corpus links ../succession/README.md etc. — out-of-dir
        # relative links resolve against docs/retro/ and must count.
        root = _make_repo(tmp_path, "# retro\n\n- [pack](../succession/pack.md)\n", {})
        (tmp_path / "docs" / "succession").mkdir()
        (tmp_path / "docs" / "succession" / "pack.md").write_text("x", encoding="utf-8")
        assert cri.check_retro(root) == []

    def test_absolute_urls_ignored(self, tmp_path):
        root = _make_repo(
            tmp_path,
            "# retro\n\nSee [docs](https://example.com/page.md).\n",
            {},
        )
        assert cri.check_retro(root) == []

    def test_missing_readme_fails(self, tmp_path):
        root = _make_repo(tmp_path, None, {"retro-a-2026-07-01.md": "body"})
        assert "missing-readme" in _kinds(cri.check_retro(root))

    def test_missing_dir_fails(self, tmp_path):
        assert _kinds(cri.check_retro(tmp_path)) == ["missing-dir"]


class TestLiveRepo:
    def test_this_repo_is_clean(self):
        # The kit's own docs/retro/ must satisfy its own checker — the same
        # dogfood rule every other scripts/check_*.py holds itself to.
        findings = cri.check_retro(REPO_ROOT)
        assert findings == [], findings

    def test_main_exit_codes(self, tmp_path, capsys):
        root = _make_repo(
            tmp_path,
            "# retro\n",
            {"orphan-2026-07-01.md": "body"},
        )
        assert cri.main(["--root", str(root)]) == 1
        assert "not-indexed" in capsys.readouterr().out
        (root / "docs" / "retro" / "README.md").write_text(
            "- [o](orphan-2026-07-01.md)\n", encoding="utf-8"
        )
        assert cri.main(["--root", str(root)]) == 0
        assert "OK" in capsys.readouterr().out
