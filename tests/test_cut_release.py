"""Tests for scripts/cut_release.py — the release-cut preparation mechanizer.

Every test operates on a tmp fixture repo copy; the real tree is never
mutated (the one live-repo test is a dry-run, pinned side-effect-free).
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import check_changelog_structure as ccs  # noqa: E402
import cut_release as cr  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[1]

FIXTURE_CONFIG = """\
# Fixture config.
KIT_VERSION = "0.1.0"
"""

FIXTURE_PYPROJECT = """\
[project]
name = "fixture"
# Kept equal to KIT_VERSION.
version = "0.1.0"
"""

# The kit's own self-pin — kept equal to KIT_VERSION so the kit's own
# `currency` row reads `current` (the tree-internal false-DRIFT fix).
FIXTURE_KIT_CONFIG = """\
{
  "kit_version": "0.1.0"
}
"""

FIXTURE_CHANGELOG = """\
# Changelog

Intro prose.

## [Unreleased]

Preamble prose block (KF-5 lives here).

### Added

- A new capability (PR #1).

### Fixed

- A fix.

## [0.1.0] - 2026-07-01

Old prose.

<!-- release: breaking=false state_migration=false min_upgrade_from=1.0.0 -->

### Added

- Genesis.
"""

# The pinned golden dry-run head for the fixture above (0.1.0 -> 0.2.0,
# --date 2026-07-14): mode line + all three unified diffs + the dry-run
# notice. The checklist tail is asserted by content below, not byte-pinned,
# so a runbook wording tweak doesn't invalidate the diff pin.
GOLDEN_DRY_RUN_HEAD = """\
cut_release 0.1.0 -> 0.2.0 (MINOR) [DRY-RUN]

--- a/src/engine/lib/config.py
+++ b/src/engine/lib/config.py
@@ -1,2 +1,2 @@
 # Fixture config.
-KIT_VERSION = "0.1.0"
+KIT_VERSION = "0.2.0"
--- a/pyproject.toml
+++ b/pyproject.toml
@@ -1,4 +1,4 @@
 [project]
 name = "fixture"
 # Kept equal to KIT_VERSION.
-version = "0.1.0"
+version = "0.2.0"
--- a/substrate.config.json
+++ b/substrate.config.json
@@ -1,3 +1,3 @@
 {
-  "kit_version": "0.1.0"
+  "kit_version": "0.2.0"
 }
--- a/CHANGELOG.md
+++ b/CHANGELOG.md
@@ -4,7 +4,11 @@

 ## [Unreleased]

+## [0.2.0] - 2026-07-14
+
 Preamble prose block (KF-5 lives here).
+
+<!-- release: breaking=false state_migration=false min_upgrade_from=1.0.0 -->

 ### Added


DRY-RUN — no files changed. Re-run with --write to apply.
"""


def make_fixture(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    (root / "src/engine/lib").mkdir(parents=True)
    (root / "src/engine/lib/config.py").write_text(
        FIXTURE_CONFIG, encoding="utf-8"
    )
    (root / "pyproject.toml").write_text(FIXTURE_PYPROJECT, encoding="utf-8")
    (root / "substrate.config.json").write_text(
        FIXTURE_KIT_CONFIG, encoding="utf-8"
    )
    (root / "CHANGELOG.md").write_text(FIXTURE_CHANGELOG, encoding="utf-8")
    return root


def _git(root: Path, *args: str) -> None:
    subprocess.run(
        ["git", "-c", "user.email=t@t", "-c", "user.name=t", *args],
        cwd=root,
        check=True,
        capture_output=True,
    )


def make_git_fixture(tmp_path: Path) -> Path:
    root = make_fixture(tmp_path)
    _git(root, "init", "-q")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "fixture")
    return root


class TestGoldenDryRun:
    def test_golden_output_head(self, tmp_path, capsys):
        root = make_fixture(tmp_path)
        rc = cr.main(["0.2.0", "--root", str(root), "--date", "2026-07-14"])
        out = capsys.readouterr().out
        assert rc == 0
        # Compare rstripped lines: difflib prints context blank lines as a
        # single space, which editors/linters would strip from the pin.
        got = [line.rstrip() for line in out.splitlines()]
        want = [line.rstrip() for line in GOLDEN_DRY_RUN_HEAD.splitlines()]
        assert got[: len(want)] == want

    def test_checklist_names_the_manual_steps(self, tmp_path, capsys):
        root = make_fixture(tmp_path)
        cr.main(["0.2.0", "--root", str(root), "--date", "2026-07-14"])
        out = capsys.readouterr().out
        # Every step the script deliberately does NOT do must be named.
        assert "src/build_bootstrap.py" in out  # dist regen + byte-pin
        assert "born-red session card" in out  # claim + bump PR
        assert "--verify-only" in out  # local verify
        assert "workflow_dispatch with input\n    version=0.2.0" in out
        assert "Three-way verification (never skip)" in out
        assert "release.json\n    sha256 field" in out or "release.json" in out
        assert "dist/bootstrap.py currency" in out  # aftermath

    def test_dry_run_changes_nothing(self, tmp_path):
        root = make_fixture(tmp_path)
        paths = (
            cr.CONFIG_RELPATH,
            cr.PYPROJECT_RELPATH,
            cr.KIT_CONFIG_RELPATH,
            cr.CHANGELOG_RELPATH,
        )
        before = {p: (root / p).read_text(encoding="utf-8") for p in paths}
        cr.main(["0.2.0", "--root", str(root), "--date", "2026-07-14"])
        after = {p: (root / p).read_text(encoding="utf-8") for p in paths}
        assert before == after

    def test_live_repo_dry_run_is_green(self, capsys):
        """The real tree accepts a MINOR dry-run (and is never written).

        Post-cut state is equally golden: immediately after a release cut the
        live ``[Unreleased]`` section is deliberately empty, and the script's
        correct answer is the "nothing to release" refusal (exit 1) — the
        v1.16.0 bump was the first real tree in that state and turned this
        test red until it learned both legs.
        """
        cfg = (REPO_ROOT / cr.CONFIG_RELPATH).read_text(encoding="utf-8")
        current = cr._KIT_VERSION_RE.search(cfg).group(1)
        major, minor, _ = cr.parse_semver(current)
        rc = cr.main(
            [
                f"{major}.{minor + 1}.0",
                "--root",
                str(REPO_ROOT),
                "--date",
                "2026-07-14",
            ]
        )
        out = capsys.readouterr().out + capsys.readouterr().err
        if rc == 0:
            assert "DRY-RUN — no files changed" in out
        else:
            # Freshly-cut tree: empty [Unreleased] must be the ONLY reason.
            assert rc == 1
            assert (
                "[Unreleased] has no typed `###` sections" in out
            ), f"unexpected cut_release failure:\n{out}"


class TestWrite:
    def test_bump_lands_in_all_homes(self, tmp_path, capsys):
        root = make_git_fixture(tmp_path)
        rc = cr.main(
            ["0.2.0", "--root", str(root), "--date", "2026-07-14", "--write"]
        )
        assert rc == 0
        cfg = (root / cr.CONFIG_RELPATH).read_text(encoding="utf-8")
        py = (root / cr.PYPROJECT_RELPATH).read_text(encoding="utf-8")
        kit_cfg = (root / cr.KIT_CONFIG_RELPATH).read_text(encoding="utf-8")
        assert 'KIT_VERSION = "0.2.0"' in cfg
        assert '"0.1.0"' not in cfg
        assert 'version = "0.2.0"' in py
        assert 'version = "0.1.0"' not in py
        # Third home: the kit's own self-pin advances in lockstep.
        assert '"kit_version": "0.2.0"' in kit_cfg
        assert '"0.1.0"' not in kit_cfg

    def test_changelog_passes_structure_checker(self, tmp_path, capsys):
        root = make_git_fixture(tmp_path)
        cr.main(["0.2.0", "--root", str(root), "--date", "2026-07-14", "--write"])
        # The produced file must be clean under the real checker, both via
        # its library API and via the script's own CLI entry point.
        assert ccs.check_changelog(root) == []
        assert ccs.main(["--root", str(root)]) == 0

    def test_changelog_shape(self, tmp_path, capsys):
        root = make_git_fixture(tmp_path)
        cr.main(["0.2.0", "--root", str(root), "--date", "2026-07-14", "--write"])
        text = (root / cr.CHANGELOG_RELPATH).read_text(encoding="utf-8")
        lines = text.splitlines()
        i_unrel = lines.index("## [Unreleased]")
        i_rel = lines.index("## [0.2.0] - 2026-07-14")
        # Fresh empty [Unreleased] directly above the new released section.
        assert i_rel == i_unrel + 2
        assert lines[i_unrel + 1] == ""
        # Preamble kept verbatim; machine comment between it and ### Added.
        i_pre = lines.index("Preamble prose block (KF-5 lives here).")
        i_comment = lines.index(
            "<!-- release: breaking=false state_migration=false "
            "min_upgrade_from=1.0.0 -->"
        )
        i_added = lines.index("### Added")
        assert i_rel < i_pre < i_comment < i_added
        # History untouched: the old released section is still there once.
        assert text.count("## [0.1.0] - 2026-07-01") == 1

    def test_major_bump_sets_breaking_true(self, tmp_path, capsys):
        root = make_git_fixture(tmp_path)
        rc = cr.main(
            ["1.0.0", "--root", str(root), "--date", "2026-07-14", "--write"]
        )
        assert rc == 0
        text = (root / cr.CHANGELOG_RELPATH).read_text(encoding="utf-8")
        assert "<!-- release: breaking=true" in text


class TestRefusals:
    def test_dirty_tree_refused_for_write(self, tmp_path, capsys):
        root = make_git_fixture(tmp_path)
        (root / "CHANGELOG.md").write_text(
            FIXTURE_CHANGELOG + "\n- uncommitted\n", encoding="utf-8"
        )
        rc = cr.main(
            ["0.2.0", "--root", str(root), "--date", "2026-07-14", "--write"]
        )
        out = capsys.readouterr().out
        assert rc == 1
        assert "git tree is dirty" in out

    def test_dirty_tree_ok_for_dry_run(self, tmp_path, capsys):
        root = make_git_fixture(tmp_path)
        (root / "extra.txt").write_text("x", encoding="utf-8")
        rc = cr.main(["0.2.0", "--root", str(root), "--date", "2026-07-14"])
        assert rc == 0

    def test_version_home_disagreement_refused(self, tmp_path, capsys):
        root = make_git_fixture(tmp_path)
        (root / cr.PYPROJECT_RELPATH).write_text(
            FIXTURE_PYPROJECT.replace('"0.1.0"', '"0.0.9"'), encoding="utf-8"
        )
        _git(root, "add", "-A")
        _git(root, "commit", "-q", "-m", "skew")
        rc = cr.main(
            ["0.2.0", "--root", str(root), "--date", "2026-07-14", "--write"]
        )
        out = capsys.readouterr().out
        assert rc == 1
        assert "version homes disagree" in out
        # And nothing was written.
        cfg = (root / cr.CONFIG_RELPATH).read_text(encoding="utf-8")
        assert 'KIT_VERSION = "0.1.0"' in cfg

    def test_malformed_version_refused(self, tmp_path, capsys):
        root = make_fixture(tmp_path)
        for bad in ("v0.2.0", "0.2", "0.2.0.1", "abc", "0.2.x"):
            rc = cr.main([bad, "--root", str(root), "--date", "2026-07-14"])
            out = capsys.readouterr().out
            assert rc == 1, bad
            assert "malformed version" in out, bad

    def test_non_increment_refused(self, tmp_path, capsys):
        root = make_fixture(tmp_path)
        for bad in ("0.3.0", "0.1.2", "2.0.0", "0.1.0", "0.0.9"):
            rc = cr.main([bad, "--root", str(root), "--date", "2026-07-14"])
            out = capsys.readouterr().out
            assert rc == 1, bad
            assert "not a sensible increment" in out, bad

    def test_already_released_refused(self, tmp_path, capsys):
        root = make_fixture(tmp_path)
        # Make 0.2.0 a valid increment that already has a section.
        text = (root / cr.CHANGELOG_RELPATH).read_text(encoding="utf-8")
        (root / cr.CHANGELOG_RELPATH).write_text(
            text + "\n## [0.2.0] - 2026-07-02\n\n### Added\n\n- Ghost.\n",
            encoding="utf-8",
        )
        rc = cr.main(["0.2.0", "--root", str(root), "--date", "2026-07-14"])
        out = capsys.readouterr().out
        assert rc == 1
        assert "already" in out

    def test_empty_unreleased_refused(self, tmp_path, capsys):
        root = make_fixture(tmp_path)
        text = FIXTURE_CHANGELOG.replace(
            """## [Unreleased]

Preamble prose block (KF-5 lives here).

### Added

- A new capability (PR #1).

### Fixed

- A fix.

""",
            "## [Unreleased]\n\n",
        )
        (root / cr.CHANGELOG_RELPATH).write_text(text, encoding="utf-8")
        rc = cr.main(["0.2.0", "--root", str(root), "--date", "2026-07-14"])
        out = capsys.readouterr().out
        assert rc == 1
        assert "nothing to release" in out

    def test_invalid_unreleased_structure_refused(self, tmp_path, capsys):
        root = make_fixture(tmp_path)
        text = FIXTURE_CHANGELOG.replace(
            "### Fixed\n\n- A fix.\n",
            "### Fixed\n\n- A fix.\n\n### Added\n\n- Stranded (duplicate).\n",
        )
        (root / cr.CHANGELOG_RELPATH).write_text(text, encoding="utf-8")
        rc = cr.main(["0.2.0", "--root", str(root), "--date", "2026-07-14"])
        out = capsys.readouterr().out
        assert rc == 1
        assert "structurally invalid" in out
        assert "duplicate-heading" in out

    def test_malformed_date_refused(self, tmp_path, capsys):
        root = make_fixture(tmp_path)
        rc = cr.main(["0.2.0", "--root", str(root), "--date", "14-07-2026"])
        out = capsys.readouterr().out
        assert rc == 1
        assert "malformed --date" in out


class TestHelpers:
    def test_classify_increment(self):
        assert cr.classify_increment("1.15.0", "2.0.0") == "major"
        assert cr.classify_increment("1.15.0", "1.16.0") == "minor"
        assert cr.classify_increment("1.15.0", "1.15.1") == "patch"

    def test_transform_is_idempotent_guarded(self):
        """Transforming twice refuses: the section now exists."""
        once = cr.transform_changelog(
            FIXTURE_CHANGELOG, "0.2.0", "2026-07-14", breaking=False
        )
        try:
            cr.transform_changelog(once, "0.2.0", "2026-07-14", breaking=False)
        except cr.CutError as exc:
            assert "already" in str(exc)
        else:  # pragma: no cover
            raise AssertionError("second transform should refuse")


class TestFollowupChecklistRunbookPin:
    """Drift pin: FOLLOWUP_CHECKLIST embeds runbook prose with no other
    protection — a runbook edit could silently orphan the checklist. Loose
    presence pin (decided-and-flagged): each checklist step's key noun/verb
    phrase must appear in docs/operations/release-runbook.md (and in the
    checklist itself, so the keyword map can't drift either) — NOT byte
    equality, so wording tweaks stay free while concept removals/renames
    fail loudly and force reconciling both homes.
    """

    # step number in FOLLOWUP_CHECKLIST -> the phrases that pin it to the
    # runbook section covering the same step (case-insensitive substrings).
    STEP_KEYWORDS = {
        1: ["machine comment"],
        2: ["src/build_bootstrap.py", "byte count", "wc -c dist/bootstrap.py"],
        3: ["control/claims/release-v", "born-red session card", "auto-merge"],
        4: [
            "pytest tests/ -q",
            "ruff check src/engine/",
            "build_release_json.py",
            "check_idea_index.py",
            "check_program_law.py",
            "check --strict",
        ],
        5: ["flip the card", "auto-merge"],
        6: ["release.yml", "workflow_dispatch", "annotated tag", "release.json"],
        7: ["three-way", "sha256", "never skip"],
        8: ["adopters", "currency", "release record", "upgrade"],
    }

    def test_followup_checklist_keywords_pinned_to_runbook(self):
        runbook = (
            REPO_ROOT / "docs" / "operations" / "release-runbook.md"
        ).read_text(encoding="utf-8").lower()
        checklist = cr.FOLLOWUP_CHECKLIST.format(version="9.9.9").lower()
        # The checklist must name its canonical source.
        assert "docs/operations/release-runbook.md" in checklist
        missing = []
        for step, keywords in self.STEP_KEYWORDS.items():
            for kw in keywords:
                if kw.lower() not in checklist:
                    missing.append(f"step {step}: {kw!r} gone from FOLLOWUP_CHECKLIST")
                if kw.lower() not in runbook:
                    missing.append(f"step {step}: {kw!r} gone from release-runbook.md")
        assert not missing, (
            "checklist/runbook drift — reconcile scripts/cut_release.py "
            "FOLLOWUP_CHECKLIST with docs/operations/release-runbook.md "
            "(or update STEP_KEYWORDS if the concept genuinely moved): "
            + "; ".join(missing)
        )
