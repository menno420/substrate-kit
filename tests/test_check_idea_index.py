"""Tests for scripts/check_idea_index.py — the B4 ideas-frontmatter checker."""

from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import check_idea_index as cii  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[1]
TODAY = dt.date(2026, 7, 9)

GOOD_FM = """---
state: captured
origin: lab
shipped_pr: null
shipped_repo: null
merged_date: null
outcome: open
---

# An idea (2026-07-01)

Body.
"""


def _make_repo(tmp_path, files, readme=None):
    ideas = tmp_path / "docs" / "ideas"
    ideas.mkdir(parents=True)
    names = []
    for name, text in files.items():
        (ideas / name).write_text(text, encoding="utf-8")
        names.append(name)
    if readme is None:
        links = "\n".join(f"- [x]({n})" for n in names)
        readme = f"# ideas\n\n## Backlog\n\n{links}\n"
    (ideas / "README.md").write_text(readme, encoding="utf-8")
    return tmp_path


def _kinds(findings):
    return sorted({f.kind for f in findings})


class TestParseFrontmatter:
    def test_good_block(self):
        fields, err = cii.parse_frontmatter(GOOD_FM)
        assert err is None
        assert fields["state"] == "captured"
        assert fields["outcome"] == "open"

    def test_missing_block(self):
        fields, err = cii.parse_frontmatter("# Title\n")
        assert fields is None
        assert "no frontmatter" in err

    def test_unterminated_block(self):
        fields, err = cii.parse_frontmatter("---\nstate: captured\n")
        assert fields is None
        assert "never closed" in err

    def test_non_kv_line(self):
        fields, err = cii.parse_frontmatter("---\n- a list item\n---\n")
        assert fields is None
        assert "key: value" in err


class TestValidateFields:
    def _fields(self, **over):
        base = {
            "state": "captured",
            "origin": "lab",
            "shipped_pr": "null",
            "shipped_repo": "null",
            "merged_date": "null",
            "outcome": "open",
        }
        base.update(over)
        return base

    def test_clean(self):
        assert cii.validate_fields("x.md", self._fields(), TODAY) == []

    def test_missing_key(self):
        fields = self._fields()
        del fields["outcome"]
        assert _kinds(cii.validate_fields("x.md", fields, TODAY)) == ["missing-key"]

    def test_bad_enums(self):
        assert _kinds(cii.validate_fields("x.md", self._fields(state="wip"), TODAY)) == ["bad-state"]
        assert _kinds(cii.validate_fields("x.md", self._fields(outcome="done"), TODAY)) == ["bad-outcome"]
        assert _kinds(cii.validate_fields("x.md", self._fields(origin="me"), TODAY)) == ["bad-origin"]

    def test_consumer_origin_ok(self):
        fields = self._fields(origin="consumer:menno420/superbot")
        assert cii.validate_fields("x.md", fields, TODAY) == []

    def test_shipped_requires_ship_fields(self):
        fields = self._fields(outcome="shipped")
        assert "outcome-inconsistent" in _kinds(cii.validate_fields("x.md", fields, TODAY))

    def test_shipped_complete_ok(self):
        fields = self._fields(
            outcome="shipped",
            shipped_pr="16",
            shipped_repo="menno420/substrate-kit",
            merged_date="2026-07-09",
        )
        assert cii.validate_fields("x.md", fields, TODAY) == []

    def test_open_with_ship_fields_is_inconsistent(self):
        fields = self._fields(shipped_pr="16")
        assert "outcome-inconsistent" in _kinds(cii.validate_fields("x.md", fields, TODAY))

    def test_survived_too_young(self):
        fields = self._fields(
            outcome="survived",
            shipped_pr="16",
            shipped_repo="menno420/substrate-kit",
            merged_date="2026-07-01",
        )
        assert "survived-too-young" in _kinds(cii.validate_fields("x.md", fields, TODAY))

    def test_survived_old_enough(self):
        fields = self._fields(
            outcome="survived",
            shipped_pr="16",
            shipped_repo="menno420/substrate-kit",
            merged_date="2026-06-01",
        )
        assert cii.validate_fields("x.md", fields, TODAY) == []

    def test_bad_shapes(self):
        fields = self._fields(
            outcome="shipped",
            shipped_pr="sixteen",
            shipped_repo="not a repo",
            merged_date="July 9",
        )
        kinds = _kinds(cii.validate_fields("x.md", fields, TODAY))
        assert "bad-shipped-pr" in kinds
        assert "bad-shipped-repo" in kinds
        assert "bad-merged-date" in kinds


SHIPPED_FM = """---
state: promoted
origin: lab
shipped_pr: 92
shipped_repo: menno420/substrate-kit
merged_date: 2026-07-01
outcome: shipped
---
"""


def _shipped_idea(body: str) -> str:
    return SHIPPED_FM + "\n# An idea (2026-07-01)\n\n" + body


class TestBodyStateDrift:
    """Enforcement item 5 — shipped frontmatter vs. a stale body State line
    (friction→guard from PR #311)."""

    def _drift(self, text):
        fields, err = cii.parse_frontmatter(text)
        assert err is None
        return cii.check_body_state_drift("x-2026-07-01.md", fields, text)

    def test_stale_captured_body_fails(self):
        text = _shipped_idea("> **State:** captured (a session).\n\n## The finding\n\nBody.\n")
        findings = self._drift(text)
        assert _kinds(findings) == ["body-state-drift"]
        # The message names the two disagreeing values.
        assert "outcome=`shipped`" in findings[0].message
        assert "shipped_pr=`92`" in findings[0].message
        assert "`captured`" in findings[0].message

    def test_stale_routed_body_fails(self):
        text = _shipped_idea("> **State:** routed (discuss-first).\n\nBody.\n")
        assert _kinds(self._drift(text)) == ["body-state-drift"]

    def test_arrow_chain_reaching_shipped_passes(self):
        text = _shipped_idea(
            "> **State:** captured (a session) → promoted →\n"
            "> **shipped** same day (kit PR #92).\n\nBody.\n"
        )
        assert self._drift(text) == []

    def test_plain_shipped_state_line_passes(self):
        text = _shipped_idea("> **State:** shipped — kit PR #92 (2026-07-01).\n\nBody.\n")
        assert self._drift(text) == []

    def test_shipped_section_marker_passes(self):
        text = _shipped_idea(
            "> **State:** captured (a session).\n\nBody.\n\n## Shipped\n\nPR #92 built it.\n"
        )
        assert self._drift(text) == []

    def test_ruled_banner_passes(self):
        text = _shipped_idea(
            "> **State:** captured (a session).\n\n"
            "> **RULED 2026-07-10 — Reading A.** Body above\n"
            "> preserved as written (historical).\n"
        )
        assert self._drift(text) == []

    def test_no_state_line_passes(self):
        # Pre-convention bodies have no State line; frontmatter is authoritative.
        text = _shipped_idea("Just prose, no State blockquote.\n")
        assert self._drift(text) == []

    def test_unshipped_frontmatter_with_captured_body_passes(self):
        text = GOOD_FM  # outcome: open, shipped_pr: null, body says nothing shipped
        fields, err = cii.parse_frontmatter(text)
        assert err is None
        assert cii.check_body_state_drift("x.md", fields, text + "> **State:** captured.\n") == []

    def test_shipped_word_outside_state_blockquote_still_fails(self):
        # `shipped` in ordinary prose is not a reconciliation marker — only the
        # State blockquote's arrow-chain counts.
        text = _shipped_idea(
            "> **State:** captured (a session).\n\nSomeday this could be shipped.\n"
        )
        assert _kinds(self._drift(text)) == ["body-state-drift"]

    def test_check_ideas_integration_flags_drift(self, tmp_path):
        drifted = _shipped_idea("> **State:** captured (a session).\n\nBody.\n")
        root = _make_repo(tmp_path, {"an-idea-2026-07-01.md": drifted})
        assert "body-state-drift" in _kinds(cii.check_ideas(root, today=TODAY))


class TestCheckIdeas:
    def test_clean_repo(self, tmp_path):
        root = _make_repo(tmp_path, {"an-idea-2026-07-01.md": GOOD_FM})
        assert cii.check_ideas(root, today=TODAY) == []

    def test_missing_frontmatter(self, tmp_path):
        root = _make_repo(tmp_path, {"an-idea-2026-07-01.md": "# Title\n"})
        assert "no-frontmatter" in _kinds(cii.check_ideas(root, today=TODAY))

    def test_bad_filename(self, tmp_path):
        root = _make_repo(tmp_path, {"an-idea.md": GOOD_FM})
        assert "bad-filename" in _kinds(cii.check_ideas(root, today=TODAY))

    def test_unindexed_file(self, tmp_path):
        root = _make_repo(
            tmp_path,
            {"an-idea-2026-07-01.md": GOOD_FM},
            readme="# ideas\n\n## Backlog\n\n(none)\n",
        )
        assert "not-indexed" in _kinds(cii.check_ideas(root, today=TODAY))

    def test_dangling_link(self, tmp_path):
        root = _make_repo(
            tmp_path,
            {"an-idea-2026-07-01.md": GOOD_FM},
            readme="# ideas\n\n- [a](an-idea-2026-07-01.md)\n- [gone](missing-2026-01-01.md)\n",
        )
        assert "dangling-link" in _kinds(cii.check_ideas(root, today=TODAY))

    def test_absolute_links_ignored(self, tmp_path):
        root = _make_repo(
            tmp_path,
            {"an-idea-2026-07-01.md": GOOD_FM},
            readme=(
                "# ideas\n\n- [a](an-idea-2026-07-01.md)\n"
                "- [ext](https://github.com/menno420/superbot/blob/main/docs/x.md)\n"
            ),
        )
        assert cii.check_ideas(root, today=TODAY) == []

    def test_missing_dir(self, tmp_path):
        assert _kinds(cii.check_ideas(tmp_path, today=TODAY)) == ["missing-dir"]


class TestLiveRepo:
    def test_this_repo_is_clean(self):
        assert cii.check_ideas(REPO_ROOT) == []

    def test_main_exit_code(self, capsys):
        assert cii.main(["--root", str(REPO_ROOT)]) == 0
        assert "OK" in capsys.readouterr().out
