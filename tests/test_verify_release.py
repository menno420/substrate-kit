"""Tests for scripts/verify_release.py — the runbook §5 post-release verifier.

Everything runs on tmp fixture git repos with injected fake fetchers: the
suite never touches the network and never depends on this repo's own tags.
One optional live golden test (against the real v1.15.0 release) is gated
behind ``VERIFY_RELEASE_LIVE=1`` so CI stays hermetic.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "verify_release.py"

_SCRIPTS = REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import verify_release as vr  # noqa: E402

VERSION = "1.2.3"
PREVIOUS = "1.2.2"
_GIT_ENV = {
    **os.environ,
    "GIT_AUTHOR_NAME": "kit-test",
    "GIT_AUTHOR_EMAIL": "kit-test@example.invalid",
    "GIT_COMMITTER_NAME": "kit-test",
    "GIT_COMMITTER_EMAIL": "kit-test@example.invalid",
}


def _git(root: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=root,
        env=_GIT_ENV,
        capture_output=True,
        text=True,
        check=True,
    )
    return proc.stdout.strip()


def _write_tree(root: Path, version: str) -> None:
    (root / "src" / "engine" / "lib").mkdir(parents=True, exist_ok=True)
    (root / "dist").mkdir(exist_ok=True)
    (root / "src" / "engine" / "lib" / "config.py").write_text(
        f'KIT_VERSION = "{version}"\n', encoding="utf-8"
    )
    (root / "pyproject.toml").write_text(
        f'[project]\nname = "kit"\nversion = "{version}"\n', encoding="utf-8"
    )
    (root / "dist" / "bootstrap.py").write_text(
        f'"""substrate-kit bootstrap v{version} — GENERATED, DO NOT EDIT.\n'
        f'"""\nBODY = "payload for {version}"\n',
        encoding="utf-8",
    )


def make_repo(tmp_path: Path, name: str = "repo") -> Path:
    """A fixture history: c1 declares 1.2.2, c2 is the 1.2.3 bump (tagged)."""
    root = tmp_path / name
    root.mkdir()
    _git(root, "init", "-q")
    _write_tree(root, PREVIOUS)
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", f"baseline {PREVIOUS}")
    _write_tree(root, VERSION)
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", f"Release v{VERSION} — version bump")
    _git(root, "tag", "-a", f"v{VERSION}", "-m", f"v{VERSION}")
    _git(root, "update-ref", "refs/remotes/origin/main", "HEAD")
    return root


def dist_sha(root: Path, rev: str = "HEAD") -> str:
    blob = subprocess.run(
        ["git", "show", f"{rev}:dist/bootstrap.py"],
        cwd=root,
        capture_output=True,
        check=True,
    ).stdout
    return hashlib.sha256(blob).hexdigest()


def make_fetch(root: Path, *, sha: str | None = None, asset: bytes | None = None,
               json_version: str = VERSION, runs: list | None = None,
               run_head: str | None = None):
    """A fake fetcher serving the two download URLs + the Actions API."""
    real_asset = subprocess.run(
        ["git", "show", "HEAD:dist/bootstrap.py"],
        cwd=root, capture_output=True, check=True,
    ).stdout
    asset_bytes = asset if asset is not None else real_asset
    sha_field = sha if sha is not None else dist_sha(root)
    if runs is None:
        head = run_head or _git(root, "rev-parse", "HEAD")
        runs = [
            {
                "id": 424242,
                "head_sha": head,
                "status": "completed",
                "conclusion": "success",
            }
        ]

    def fetch(url: str) -> bytes:
        if url.endswith("/release.json"):
            return json.dumps(
                {"version": json_version, "sha256": sha_field}
            ).encode("utf-8")
        if url.endswith("/bootstrap.py"):
            return asset_bytes
        if "api.github.com" in url:
            return json.dumps({"workflow_runs": runs}).encode("utf-8")
        raise vr.FetchError(f"{url} -> unexpected URL in test")

    return fetch


def dead_fetch(url: str) -> bytes:
    raise vr.FetchError(f"{url} -> simulated network unavailability")


def run_verifier(root: Path, fetch, version: str = VERSION, capsys=None,
                 git=None) -> tuple[int, str]:
    code = vr.run(
        version,
        git=git if git is not None else vr.make_git_runner(root),
        fetch=fetch,
    )
    out = capsys.readouterr().out if capsys else ""
    return code, out


# ---------------------------------------------------------------- PASS path


def test_golden_pass_all_three_legs(tmp_path, capsys):
    root = make_repo(tmp_path)
    code, out = run_verifier(root, make_fetch(root), capsys=capsys)
    assert code == 0
    assert "verdict: 3 PASS · 0 FAIL · 0 SKIPPED -> exit 0" in out
    assert "[1/3] tag — PASS" in out
    assert "[2/3] sha256 — PASS" in out
    assert "[3/3] workflow — PASS" in out
    assert "this commit IS the bump" in out
    assert "run 424242" in out
    assert f"sha256 {dist_sha(root)}" in out
    assert "WARNING" not in out


def test_record_line_carries_the_evidence(tmp_path, capsys):
    root = make_repo(tmp_path)
    code, out = run_verifier(root, make_fetch(root), capsys=capsys)
    assert code == 0
    record = out.rsplit("release-record line (paste-ready):", 1)[1]
    commit = _git(root, "rev-parse", "HEAD")
    tag_object = _git(root, "rev-parse", f"refs/tags/v{VERSION}")
    assert f"v{VERSION}" in record
    assert tag_object[:12] in record
    assert commit[:12] in record
    assert dist_sha(root) in record
    assert "release.yml run 424242 green" in record


def test_ls_remote_fallback_resolves_the_tag(tmp_path, capsys):
    origin = make_repo(tmp_path, "origin-repo")
    clone = tmp_path / "clone"
    _git(tmp_path, "clone", "-q", "--no-tags", str(origin), str(clone))
    assert _git(clone, "tag", "-l") == ""  # the fallback is actually exercised
    code, out = run_verifier(clone, make_fetch(origin), capsys=capsys)
    assert code == 0
    assert "via ls-remote origin" in out
    assert "[1/3] tag — PASS" in out


# ---------------------------------------------------------------- FAIL paths


def test_tampered_release_json_sha_fails(tmp_path, capsys):
    root = make_repo(tmp_path)
    fetch = make_fetch(root, sha="0" * 64)
    code, out = run_verifier(root, fetch, capsys=capsys)
    assert code == 1
    assert "[2/3] sha256 — FAIL" in out
    assert "FAIL    release.json==asset" in out
    assert "FAIL    release.json==committed" in out
    assert "PASS    asset==committed" in out
    expected = dist_sha(root)
    assert f"release.json={'0' * 64} != asset={expected}" in out


def test_tampered_asset_fails(tmp_path, capsys):
    root = make_repo(tmp_path)
    fetch = make_fetch(root, asset=b"not the released bytes")
    code, out = run_verifier(root, fetch, capsys=capsys)
    assert code == 1
    assert "FAIL    release.json==asset" in out
    assert "FAIL    asset==committed" in out
    assert "PASS    release.json==committed" in out


def test_release_json_version_mismatch_fails(tmp_path, capsys):
    root = make_repo(tmp_path)
    fetch = make_fetch(root, json_version="9.9.9")
    code, out = run_verifier(root, fetch, capsys=capsys)
    assert code == 1
    assert "release.json declares version '9.9.9', expected '1.2.3'" in out


def test_tag_missing_everywhere_fails(tmp_path, capsys):
    origin = make_repo(tmp_path, "origin-repo")
    _git(origin, "tag", "-d", f"v{VERSION}")
    clone = tmp_path / "clone"
    _git(tmp_path, "clone", "-q", "--no-tags", str(origin), str(clone))
    code, out = run_verifier(clone, make_fetch(origin), capsys=capsys)
    assert code == 1
    assert f"tag v{VERSION} does not exist" in out
    assert "[1/3] tag — FAIL" in out


def test_tag_pointing_past_the_bump_fails(tmp_path, capsys):
    root = make_repo(tmp_path)
    _git(root, "tag", "-d", f"v{VERSION}")
    (root / "extra.txt").write_text("post-bump commit\n", encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "post-bump commit")
    _git(root, "tag", "-a", f"v{VERSION}", "-m", f"v{VERSION}")
    _git(root, "update-ref", "refs/remotes/origin/main", "HEAD")
    code, out = run_verifier(root, make_fetch(root), capsys=capsys)
    assert code == 1
    assert "ALREADY declares 1.2.3 — the tag points past the version-bump" in out


def test_version_homes_mismatch_fails(tmp_path, capsys):
    root = make_repo(tmp_path)
    _git(root, "tag", "-d", f"v{VERSION}")
    _git(root, "tag", "-a", f"v{VERSION}", "-m", "wrong target", "HEAD^")
    code, out = run_verifier(root, make_fetch(root), capsys=capsys)
    assert code == 1
    assert "version-homes" in out
    assert f"KIT_VERSION='{PREVIOUS}'" in out
    assert "dist header not stamped v1.2.3" in out


def test_not_an_ancestor_fails_on_a_full_clone(tmp_path, capsys):
    root = make_repo(tmp_path)
    # origin/main stays at the pre-bump commit: the tagged bump is unmerged.
    _git(root, "update-ref", "refs/remotes/origin/main", "HEAD^")
    code, out = run_verifier(root, make_fetch(root), capsys=capsys)
    assert code == 1
    assert "is NOT an ancestor of origin/main" in out


def test_workflow_run_failure_fails(tmp_path, capsys):
    root = make_repo(tmp_path)
    head = _git(root, "rev-parse", "HEAD")
    runs = [{"id": 7, "head_sha": head, "status": "completed",
             "conclusion": "failure"}]
    code, out = run_verifier(root, make_fetch(root, runs=runs), capsys=capsys)
    assert code == 1
    assert "concluded 'failure' — expected 'success'" in out
    assert "[3/3] workflow — FAIL" in out


# ---------------------------------------------------------------- SKIP paths


def test_network_unavailability_skips_but_exits_zero(tmp_path, capsys):
    root = make_repo(tmp_path)
    code, out = run_verifier(root, dead_fetch, capsys=capsys)
    assert code == 0
    assert "[1/3] tag — PASS" in out  # git-side facts still verified
    assert "[2/3] sha256 — SKIPPED" in out  # no comparison could run
    assert "[3/3] workflow — SKIPPED" in out
    assert "simulated network unavailability" in out
    assert "WARNING" in out
    assert "sha256 UNVERIFIED" in out


def test_all_skipped_prints_nothing_verified_warning(tmp_path, capsys):
    root = tmp_path / "empty"
    root.mkdir()
    _git(root, "init", "-q")
    (root / "README.md").write_text("x\n", encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "no tags, no origin")
    code, out = run_verifier(root, dead_fetch, capsys=capsys)
    assert code == 0
    assert "verdict: 0 PASS · 0 FAIL · 3 SKIPPED -> exit 0" in out
    assert "NOTHING WAS VERIFIED" in out
    assert "tag/commit UNRESOLVED" in out


def test_shallow_clone_negative_ancestry_skips_not_fails(tmp_path, capsys):
    root = make_repo(tmp_path)
    real_git = vr.make_git_runner(root)

    def shallow_git(args):
        if args[:2] == ["merge-base", "--is-ancestor"]:
            return vr.GitResult(1, b"", b"")
        if args == ["rev-parse", "--is-shallow-repository"]:
            return vr.GitResult(0, b"true\n", b"")
        return real_git(args)

    code, out = run_verifier(root, make_fetch(root), capsys=capsys, git=shallow_git)
    assert code == 0
    assert "SKIPPED ancestry" in out
    assert "SHALLOW" in out
    assert "[1/3] tag — PASS" in out  # the other tag facts still passed


def test_workflow_run_not_found_skips(tmp_path, capsys):
    root = make_repo(tmp_path)
    fetch = make_fetch(root, runs=[{"id": 9, "head_sha": "f" * 40,
                                    "status": "completed",
                                    "conclusion": "success"}])
    code, out = run_verifier(root, fetch, capsys=capsys)
    assert code == 0
    assert "[3/3] workflow — SKIPPED" in out
    assert "inconclusive" in out


def test_workflow_run_in_progress_skips(tmp_path, capsys):
    root = make_repo(tmp_path)
    head = _git(root, "rev-parse", "HEAD")
    runs = [{"id": 11, "head_sha": head, "status": "in_progress",
             "conclusion": None}]
    code, out = run_verifier(root, make_fetch(root, runs=runs), capsys=capsys)
    assert code == 0
    assert "still 'in_progress'" in out


def test_offline_flag_skips_every_network_touch(tmp_path, capsys):
    origin = make_repo(tmp_path, "origin-repo")
    clone = tmp_path / "clone"
    _git(tmp_path, "clone", "-q", "--no-tags", str(origin), str(clone))
    code = vr.main([VERSION, "--root", str(clone), "--offline"])
    out = capsys.readouterr().out
    assert code == 0
    assert "not attempted (--offline)" in out
    assert "verdict: 0 PASS · 0 FAIL · 3 SKIPPED -> exit 0" in out


# ------------------------------------------------------------ usage + misc


def test_malformed_version_is_a_usage_error(tmp_path, capsys):
    root = make_repo(tmp_path)
    code, out = run_verifier(root, dead_fetch, version="v1.2.3", capsys=capsys)
    assert code == 2
    assert "malformed version" in out


def test_leg_settle_blocks_setup_only_pass():
    leg = vr.Leg("sha256")
    leg.add("committed-dist", vr.PASS, "hash computed")
    leg.add("release.json==asset", vr.SKIPPED, "unavailable")
    assert leg.settle(vr.SHA_SUBSTANTIVE).verdict == vr.SKIPPED
    leg2 = vr.Leg("sha256")
    leg2.add("committed-dist", vr.PASS, "hash computed")
    leg2.add("release.json==asset", vr.PASS, "both x")
    assert leg2.settle(vr.SHA_SUBSTANTIVE).verdict == vr.PASS


@pytest.mark.skipif(
    not os.environ.get("VERIFY_RELEASE_LIVE"),
    reason="live network golden run — set VERIFY_RELEASE_LIVE=1 to enable",
)
def test_live_golden_v1_15_0():
    proc = subprocess.run(
        [sys.executable, str(SCRIPT_PATH), "1.15.0"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "0 FAIL" in proc.stdout
