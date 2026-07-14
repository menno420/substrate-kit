"""Tests for scripts/_git_truth.py — the shared shallow/graft ancestry rule.

The module owns ONE rule: a positive git ancestry answer is a proof; a
negative one on a shallow/grafted clone proves nothing and degrades to
``unprovable`` (callers SKIP, never false-FAIL). Full clones give real
answers; every fixture is a tmp git repo (the suite never networks).
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import _git_truth as gt  # noqa: E402

_GIT_ENV = {
    **os.environ,
    "GIT_CONFIG_NOSYSTEM": "1",
    "GIT_AUTHOR_NAME": "kit-test",
    "GIT_AUTHOR_EMAIL": "kit-test@example.invalid",
    "GIT_COMMITTER_NAME": "kit-test",
    "GIT_COMMITTER_EMAIL": "kit-test@example.invalid",
}


def _git(root: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", "-C", str(root), *args],
        env=_GIT_ENV,
        capture_output=True,
        text=True,
        check=True,
    )
    return proc.stdout.strip()


def _make_history(root: Path, subjects: list[str]) -> list[str]:
    """init a repo with one empty commit per subject; return the SHAs oldest-first."""
    root.mkdir(parents=True, exist_ok=True)
    _git(root, "init", "-q", "-b", "main")
    shas = []
    for subject in subjects:
        _git(root, "commit", "-q", "--allow-empty", "-m", subject)
        shas.append(_git(root, "rev-parse", "HEAD"))
    return shas


def _make_shallow_clone(upstream: Path, dest: Path, tmp: Path) -> None:
    subprocess.run(
        ["git", "clone", "-q", "--depth", "1", f"file://{upstream}", str(dest)],
        check=True,
        capture_output=True,
        env=dict(_GIT_ENV, HOME=str(tmp)),
    )


# --------------------------------------------------------------- full clones


class TestFullClone:
    def test_real_ancestor_is_yes(self, tmp_path):
        shas = _make_history(tmp_path / "r", ["one", "two", "three"])
        run = gt.make_runner(tmp_path / "r")
        answer = gt.provable_ancestry(run, shas[0], "HEAD")
        assert answer.verdict == gt.YES
        assert answer.returncode == 0

    def test_real_non_ancestor_is_no(self, tmp_path):
        root = tmp_path / "r"
        _make_history(root, ["base"])
        _git(root, "checkout", "-q", "-b", "side")
        _git(root, "commit", "-q", "--allow-empty", "-m", "off-main")
        side = _git(root, "rev-parse", "HEAD")
        run = gt.make_runner(root)
        answer = gt.provable_ancestry(run, side, "main")
        assert answer.verdict == gt.NO
        assert answer.returncode == 1
        assert answer.shallow is False  # provably a full clone

    def test_unknown_commit_default_is_unprovable(self, tmp_path):
        _make_history(tmp_path / "r", ["one"])
        run = gt.make_runner(tmp_path / "r")
        answer = gt.provable_ancestry(run, "f" * 40, "HEAD")
        assert answer.verdict == gt.UNPROVABLE
        assert answer.returncode == 128
        assert answer.detail  # carries git's verbatim stderr

    def test_unknown_commit_missing_as_no_is_a_real_negative(self, tmp_path):
        # The check_idea_index policy: full history + absent commit = NO.
        _make_history(tmp_path / "r", ["one"])
        run = gt.make_runner(tmp_path / "r")
        answer = gt.provable_ancestry(run, "f" * 40, "HEAD", missing_as_no=True)
        assert answer.verdict == gt.NO
        assert answer.returncode == 128

    def test_is_shallow_false(self, tmp_path):
        _make_history(tmp_path / "r", ["one"])
        assert gt.is_shallow(gt.make_runner(tmp_path / "r")) is False


# ----------------------------------------------------- shallow/grafted clones


class TestShallowClone:
    def test_is_shallow_true(self, tmp_path):
        upstream = tmp_path / "upstream"
        _make_history(upstream, ["old", "new"])
        shallow = tmp_path / "shallow"
        _make_shallow_clone(upstream, shallow, tmp_path)
        assert gt.is_shallow(gt.make_runner(shallow)) is True

    def test_negative_ancestry_degrades_to_unprovable(self, tmp_path):
        # The #355/#357 class: the old commit IS an ancestor upstream, but
        # the grafted clone can't prove it — the answer must degrade, never
        # read as a hard negative.
        upstream = tmp_path / "upstream"
        old_sha = _make_history(upstream, ["old", "mid", "new"])[0]
        shallow = tmp_path / "shallow"
        _make_shallow_clone(upstream, shallow, tmp_path)
        run = gt.make_runner(shallow)
        answer = gt.provable_ancestry(run, old_sha, "HEAD")
        assert answer.verdict == gt.UNPROVABLE
        assert answer.returncode in (1, 128)
        assert answer.shallow is True
        assert "SHALLOW" in answer.detail

    def test_negative_with_missing_as_no_still_degrades(self, tmp_path):
        # missing_as_no widens what counts as negative — it must NOT bypass
        # the shallow degradation.
        upstream = tmp_path / "upstream"
        old_sha = _make_history(upstream, ["old", "mid", "new"])[0]
        shallow = tmp_path / "shallow"
        _make_shallow_clone(upstream, shallow, tmp_path)
        run = gt.make_runner(shallow)
        answer = gt.provable_ancestry(run, old_sha, "HEAD", missing_as_no=True)
        assert answer.verdict == gt.UNPROVABLE
        assert answer.shallow is True

    def test_positive_on_shallow_is_still_a_proof(self, tmp_path):
        upstream = tmp_path / "upstream"
        _make_history(upstream, ["old", "new"])
        shallow = tmp_path / "shallow"
        _make_shallow_clone(upstream, shallow, tmp_path)
        run = gt.make_runner(shallow)
        head = _git(shallow, "rev-parse", "HEAD")
        answer = gt.provable_ancestry(run, head, "HEAD")
        assert answer.verdict == gt.YES


# ------------------------------------------------------------ degraded seams


class TestDegradedSeams:
    def test_git_error_is_unprovable_with_detail(self):
        def broken(args):
            return 255, "", "fatal: something exploded"

        answer = gt.provable_ancestry(broken, "a" * 40, "HEAD")
        assert answer.verdict == gt.UNPROVABLE
        assert answer.detail == "fatal: something exploded"

    def test_negative_with_undeterminable_shallowness_stays_no(self):
        # "Couldn't even ask about shallowness" must not silently upgrade a
        # negative to unprovable — that preserves verify_release's shipped
        # behavior (FAIL when the shallow probe itself errors).
        def runner(args):
            if list(args)[:2] == ["merge-base", "--is-ancestor"]:
                return 1, "", ""
            return 129, "", "rev-parse broke"

        answer = gt.provable_ancestry(runner, "a" * 40, "HEAD")
        assert answer.verdict == gt.NO
        assert answer.shallow is None

    def test_is_shallow_unknown_on_error(self):
        assert gt.is_shallow(lambda args: (127, "", "no git")) is None

    def test_runner_without_git_binary(self, tmp_path):
        run = gt.make_runner(tmp_path)  # a dir that is not a repo
        rc, _out, err = run(["rev-parse", "--is-shallow-repository"])
        assert rc != 0
        assert gt.is_shallow(run) is None


# ---------------------------------------------- engine port parity (ORDER 022)


class TestEngineParity:
    """Pin the engine-shipped port against this scripts/ original.

    ``engine/lib/git_truth.py`` exists because the ORDER 022 stop-hook push
    guard must ride dist/bootstrap.py into adopters, while scripts/ never
    ships. Two copies of one rule invite drift — this test makes any
    behavioral edit to either copy fail until both move together.
    """

    def test_shared_primitives_are_source_identical(self):
        import inspect

        from engine.lib import git_truth as engine_gt

        for name in ("make_runner", "is_shallow", "provable_ancestry"):
            assert inspect.getsource(getattr(gt, name)) == inspect.getsource(
                getattr(engine_gt, name)
            ), f"{name} drifted between scripts/_git_truth.py and engine/lib/git_truth.py"
        assert inspect.getsource(gt.AncestryAnswer) == inspect.getsource(
            engine_gt.AncestryAnswer
        )
        assert (gt.YES, gt.NO, gt.UNPROVABLE) == (
            engine_gt.YES,
            engine_gt.NO,
            engine_gt.UNPROVABLE,
        )
