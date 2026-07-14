#!/usr/bin/env python3
"""verify_release — mechanize the POST-release verification as one command.

Why + provenance: the runbook's §5 three-way verification is marked "never
skip", yet it was the one release step still reassembled by hand from
memory-file lore every cut — 19 cuts and counting. With the PREPARATION half
mechanized (``scripts/cut_release.py``, PR #356), this script mechanizes the
verification half, leaving only judgment steps (semver class, prose summary,
the dispatch click) manual. Design authority: the PR #356 session card's 💡
ender (``.sessions/2026-07-14-cut-release-mechanization.md``) +
``docs/operations/release-runbook.md`` §5 (canonical recipe — this script
mechanizes §5, nothing else). Added 2026-07-14. Reliability (PL-008):
UNVERIFIED — confirm its verdicts against ground truth at the next real cuts
before trusting it; **delete this if it proves unreliable over multiple
sessions.**

What ``python3 scripts/verify_release.py X.Y.Z`` verifies (three legs):

1. **tag** — annotated tag ``vX.Y.Z`` exists (local tag, else a read-only
   ``git ls-remote origin``); its dereferenced commit ``vX.Y.Z^{}`` is an
   ancestor of ``origin/main``; the tree at that commit declares the version
   in all three homes (``KIT_VERSION``, ``pyproject.toml``, the dist header
   stamp); and the commit itself IS the version bump (its parent declares a
   different ``KIT_VERSION`` — degrades honestly on a shallow-clone graft).
2. **sha256** — the runbook's three-way: the ``release.json`` ``sha256``
   field == sha256 of the downloaded release asset ``bootstrap.py`` ==
   sha256 of the committed ``dist/bootstrap.py`` at the tag commit. Assets
   are downloaded from the ``github.com/<slug>/releases/download/`` path —
   the URL family that works through the environment's proxy;
   ``api.github.com`` is a documented wall (``docs/CAPABILITIES.md``) and is
   never needed for this leg.
3. **workflow** — the ``release.yml`` run that published the release
   (matched by ``head_sha`` == the tag commit, via the Actions API)
   concluded ``success``. In proxy-walled environments this leg SKIPs with
   the verbatim error instead of guessing.

Every check prints PASS / FAIL / SKIPPED with expected-vs-actual values; the
tail is a paste-ready release-record line (tag object · commit SHA · the
hash · run id) per runbook §5's "record …" instruction.

Degradation policy (decide-and-flag): a wall is not a verification failure —
SKIPPED legs never fail the run, but they are never silently upgraded to a
pass either. Exit 1 iff any check FAILs; exit 0 otherwise — including the
all-SKIPPED case, which additionally prints a loud ``NOTHING WAS VERIFIED``
warning (an honest "could not verify" is a different fact from "verified
bad", and a different fact from "verified good"). Exit 2 = usage error.

What it NEVER does: push, commit, dispatch a workflow, or write anything.
Network use is read-only downloads (plus an optional read-only
``git ls-remote``); ``--offline`` forces every network touch to SKIP.

Repo-level tooling, not engine code: lives in scripts/, uses print, never
ships in dist/bootstrap.py, adopter repos never receive it. Stdlib only.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

import _git_truth  # noqa: E402

REPO_SLUG = "menno420/substrate-kit"
DOWNLOAD_URL = "https://github.com/{slug}/releases/download/v{version}/{name}"
RUNS_API_URL = (
    "https://api.github.com/repos/{slug}/actions/workflows/release.yml/"
    "runs?per_page=100"
)

CONFIG_RELPATH = "src/engine/lib/config.py"
PYPROJECT_RELPATH = "pyproject.toml"
DIST_RELPATH = "dist/bootstrap.py"

_SEMVER_RE = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")
_KIT_VERSION_RE = re.compile(r'^KIT_VERSION = "(\d+\.\d+\.\d+)"$', re.MULTILINE)
_PYPROJECT_VERSION_RE = re.compile(r'^version = "(\d+\.\d+\.\d+)"$', re.MULTILINE)

PASS = "PASS"
FAIL = "FAIL"
SKIPPED = "SKIPPED"

# The purpose-checks of each leg (Leg.settle): a leg whose only passes are
# setup facts (tag resolved, one hash computed) must not read as green.
TAG_SUBSTANTIVE = frozenset(
    {"ancestry", "version-homes", "dist-stamp", "is-the-bump"}
)
SHA_SUBSTANTIVE = frozenset(
    {"release.json==asset", "asset==committed", "release.json==committed"}
)
WORKFLOW_SUBSTANTIVE = frozenset({"release-run"})

# Seam types — tests inject fakes for both (the suite never touches the
# network and never depends on this repo's own tags).
GitRunner = Callable[[list[str]], "GitResult"]
Fetcher = Callable[[str], bytes]


class FetchError(Exception):
    """A download that could not be made — carries the verbatim reason."""


@dataclass
class GitResult:
    returncode: int
    stdout: bytes
    stderr: bytes

    @property
    def text(self) -> str:
        return self.stdout.decode("utf-8", errors="replace").strip()


@dataclass
class Check:
    """One verified fact: a name, a verdict, and the evidence line."""

    name: str
    status: str
    detail: str


@dataclass
class Leg:
    name: str
    checks: list[Check] = field(default_factory=list)
    _settled_skip: bool = False

    def add(self, name: str, status: str, detail: str) -> None:
        self.checks.append(Check(name, status, detail))

    def settle(self, substantive: frozenset[str]) -> "Leg":
        """A leg may only claim PASS when a SUBSTANTIVE check passed.

        Setup facts (tag resolution, a hash computed but compared to
        nothing) are not the leg's purpose; if every purpose-check skipped,
        the leg is SKIPPED, never silently green.
        """
        if not any(c.status == FAIL for c in self.checks) and not any(
            c.status == PASS and c.name in substantive for c in self.checks
        ):
            self._settled_skip = True
        return self

    @property
    def verdict(self) -> str:
        statuses = {c.status for c in self.checks}
        if FAIL in statuses:
            return FAIL
        if self._settled_skip or statuses == {SKIPPED} or not statuses:
            return SKIPPED
        return PASS


def make_git_runner(root: Path) -> GitRunner:
    def run(args: list[str]) -> GitResult:
        try:
            proc = subprocess.run(
                ["git", *args],
                cwd=root,
                capture_output=True,
                timeout=120,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            return GitResult(returncode=255, stdout=b"", stderr=str(exc).encode())
        return GitResult(proc.returncode, proc.stdout, proc.stderr)

    return run


def make_fetcher(timeout: float) -> Fetcher:
    def fetch(url: str) -> bytes:
        headers = {"User-Agent": "substrate-kit-verify-release"}
        if "api.github.com" in url:
            headers["Accept"] = "application/vnd.github+json"
            token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
            if token:
                headers["Authorization"] = f"Bearer {token}"
        request = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return response.read()
        except (urllib.error.URLError, OSError, ValueError) as exc:
            raise FetchError(f"{url} -> {exc}") from exc

    return fetch


def _truth_runner(git: GitRunner) -> "_git_truth.GitCommand":
    """Adapt this module's injectable ``GitRunner`` to the shared seam."""

    def run(args):
        result = git(list(args))
        return (
            result.returncode,
            result.text,
            result.stderr.decode("utf-8", errors="replace").strip(),
        )

    return run


def offline_fetcher(url: str) -> bytes:
    raise FetchError(f"{url} -> not attempted (--offline)")


def offline_git_runner(inner: GitRunner) -> GitRunner:
    """Wrap a git runner so `ls-remote` (the one networked git op) SKIPs."""

    def run(args: list[str]) -> GitResult:
        if args and args[0] == "ls-remote":
            return GitResult(255, b"", b"not attempted (--offline)")
        return inner(args)

    return run


def _short(sha: str) -> str:
    return sha[:12] if sha else sha


def _kit_version_of(blob: str) -> str | None:
    match = _KIT_VERSION_RE.search(blob)
    return match.group(1) if match else None


def resolve_tag(
    version: str, git: GitRunner, leg: Leg
) -> tuple[str | None, str | None]:
    """Resolve ``vX.Y.Z`` -> (tag object sha, dereferenced commit sha)."""
    tag = f"v{version}"
    obj = git(["rev-parse", "--verify", "--quiet", f"refs/tags/{tag}"])
    if obj.returncode == 0:
        commit = git(["rev-parse", "--verify", "--quiet", f"{tag}^{{commit}}"])
        if commit.returncode == 0:
            leg.add(
                "resolve",
                PASS,
                f"tag {tag} (object {_short(obj.text)}) -> commit "
                f"{_short(commit.text)} (local tag)",
            )
            return obj.text, commit.text
    # Local clone has no tag (routine here: container clones fetch no tags) —
    # fall back to a read-only ls-remote against origin.
    remote = git(["ls-remote", "origin", f"refs/tags/{tag}", f"refs/tags/{tag}^{{}}"])
    if remote.returncode != 0:
        leg.add(
            "resolve",
            SKIPPED,
            f"tag {tag} not in the local clone and `git ls-remote origin` "
            f"failed: {remote.stderr.decode('utf-8', errors='replace').strip()}",
        )
        return None, None
    tag_object = commit_sha = None
    for line in remote.text.splitlines():
        parts = line.split(None, 1)
        if len(parts) != 2:
            continue
        sha, ref = parts
        if ref == f"refs/tags/{tag}^{{}}":
            commit_sha = sha
        elif ref == f"refs/tags/{tag}":
            tag_object = sha
    if tag_object is None:
        leg.add(
            "resolve",
            FAIL,
            f"tag {tag} does not exist — not in the local clone and not on "
            "origin (expected an annotated tag created by release.yml)",
        )
        return None, None
    if commit_sha is None:
        # A lightweight tag has no ^{} line — the tag IS the commit.
        commit_sha = tag_object
        leg.add(
            "resolve",
            FAIL,
            f"tag {tag} on origin is LIGHTWEIGHT ({_short(tag_object)}) — "
            "release.yml creates annotated tags; expected a tag object with "
            "a dereferenced commit",
        )
        return tag_object, commit_sha
    leg.add(
        "resolve",
        PASS,
        f"tag {tag} (object {_short(tag_object)}) -> commit "
        f"{_short(commit_sha)} (via ls-remote origin)",
    )
    return tag_object, commit_sha


def leg_tag(version: str, git: GitRunner) -> tuple[Leg, str | None]:
    """Leg 1: the tag points at the version-bump commit on main."""
    leg = Leg("tag")
    _tag_object, commit = resolve_tag(version, git, leg)
    if commit is None:
        return leg, None
    present = git(["cat-file", "-e", f"{commit}^{{commit}}"])
    if present.returncode != 0:
        leg.add(
            "commit-present",
            SKIPPED,
            f"commit {_short(commit)} is not in the local clone (shallow "
            "history?) — ancestry / tree / bump checks cannot run here",
        )
        return leg, commit

    # Shallow/graft degradation is the shared rule (scripts/_git_truth.py):
    # a negative answer on a grafted clone proves nothing (live-hit:
    # v1.15.0's bump commit reachable but disconnected from origin/main in
    # this container's shallow clone); a positive answer is still a proof.
    answer = _git_truth.provable_ancestry(
        _truth_runner(git), commit, "origin/main"
    )
    if answer.verdict == _git_truth.YES:
        leg.add("ancestry", PASS, f"{_short(commit)} is an ancestor of origin/main")
    elif answer.verdict == _git_truth.NO:
        leg.add(
            "ancestry",
            FAIL,
            f"{_short(commit)} is NOT an ancestor of origin/main",
        )
    elif answer.shallow:
        leg.add(
            "ancestry",
            SKIPPED,
            f"{_short(commit)} not provably an ancestor of origin/main — "
            "the local clone is SHALLOW (grafted history), so a negative "
            "answer is unreliable; re-check on a full clone",
        )
    else:
        leg.add(
            "ancestry",
            SKIPPED,
            "could not test ancestry: " + answer.detail,
        )

    config_blob = git(["show", f"{commit}:{CONFIG_RELPATH}"])
    if config_blob.returncode != 0:
        leg.add("version-homes", FAIL, f"{CONFIG_RELPATH} missing at {_short(commit)}")
    else:
        declared = _kit_version_of(config_blob.text)
        pyproject_blob = git(["show", f"{commit}:{PYPROJECT_RELPATH}"])
        py_match = _PYPROJECT_VERSION_RE.search(
            pyproject_blob.text if pyproject_blob.returncode == 0 else ""
        )
        py_declared = py_match.group(1) if py_match else None
        if declared == version and py_declared == version:
            leg.add(
                "version-homes",
                PASS,
                f"KIT_VERSION and pyproject both declare {version} at "
                f"{_short(commit)}",
            )
        else:
            leg.add(
                "version-homes",
                FAIL,
                f"expected {version} in both homes at {_short(commit)} — "
                f"KIT_VERSION={declared!r}, pyproject={py_declared!r}",
            )

    dist_blob = git(["show", f"{commit}:{DIST_RELPATH}"])
    if dist_blob.returncode != 0:
        leg.add("dist-stamp", FAIL, f"{DIST_RELPATH} missing at {_short(commit)}")
    else:
        header = dist_blob.stdout.split(b"\n", 1)[0].decode("utf-8", errors="replace")
        if f"bootstrap v{version} " in header:
            leg.add("dist-stamp", PASS, f"dist header stamped v{version}")
        else:
            leg.add(
                "dist-stamp",
                FAIL,
                f"dist header not stamped v{version} — first line: {header!r}",
            )

    parent_blob = git(["show", f"{commit}^:{CONFIG_RELPATH}"])
    if parent_blob.returncode != 0:
        leg.add(
            "is-the-bump",
            SKIPPED,
            f"parent of {_short(commit)} unavailable (shallow-clone graft?) — "
            "bump-commit identity unverifiable here",
        )
    else:
        parent_version = _kit_version_of(parent_blob.text)
        if parent_version == version:
            leg.add(
                "is-the-bump",
                FAIL,
                f"parent of {_short(commit)} ALREADY declares {version} — the "
                "tag points past the version-bump commit",
            )
        else:
            leg.add(
                "is-the-bump",
                PASS,
                f"parent declares {parent_version}, tag commit declares "
                f"{version} — this commit IS the bump",
            )
    return leg, commit


def leg_sha256(
    version: str,
    commit: str | None,
    git: GitRunner,
    fetch: Fetcher,
    slug: str,
) -> tuple[Leg, str | None]:
    """Leg 2: runbook §5's three-way sha256 equality."""
    leg = Leg("sha256")
    voices: dict[str, str | None] = {
        "release.json": None,
        "asset": None,
        "committed": None,
    }
    reasons: dict[str, str] = {}

    if commit is None:
        reasons["committed"] = "tag commit unknown (leg 1)"
        leg.add("committed-dist", SKIPPED, "tag commit unknown — cannot read the blob")
    else:
        blob = git(["show", f"{commit}:{DIST_RELPATH}"])
        if blob.returncode != 0:
            reasons["committed"] = f"{DIST_RELPATH} unreadable at {_short(commit)}"
            leg.add(
                "committed-dist",
                SKIPPED,
                f"could not read {DIST_RELPATH} at {_short(commit)}: "
                + blob.stderr.decode("utf-8", errors="replace").strip(),
            )
        else:
            voices["committed"] = hashlib.sha256(blob.stdout).hexdigest()
            leg.add(
                "committed-dist",
                PASS,
                f"dist@{_short(commit)} sha256 {voices['committed']}",
            )

    url = DOWNLOAD_URL.format(slug=slug, version=version, name="release.json")
    try:
        payload = json.loads(fetch(url).decode("utf-8"))
    except FetchError as exc:
        reasons["release.json"] = str(exc)
        leg.add("release-json", SKIPPED, f"download failed: {exc}")
    except (ValueError, UnicodeDecodeError) as exc:
        leg.add("release-json", FAIL, f"downloaded release.json unparseable: {exc}")
        reasons["release.json"] = "unparseable"
    else:
        declared_version = payload.get("version")
        voices["release.json"] = payload.get("sha256")
        if declared_version != version:
            leg.add(
                "release-json",
                FAIL,
                f"release.json declares version {declared_version!r}, "
                f"expected {version!r}",
            )
        elif not voices["release.json"]:
            leg.add("release-json", FAIL, "release.json has no sha256 field")
        else:
            leg.add(
                "release-json",
                PASS,
                f"release.json sha256 {voices['release.json']}",
            )

    url = DOWNLOAD_URL.format(slug=slug, version=version, name="bootstrap.py")
    try:
        asset = fetch(url)
    except FetchError as exc:
        reasons["asset"] = str(exc)
        leg.add("released-asset", SKIPPED, f"download failed: {exc}")
    else:
        voices["asset"] = hashlib.sha256(asset).hexdigest()
        leg.add(
            "released-asset",
            PASS,
            f"downloaded bootstrap.py ({len(asset)} bytes) sha256 "
            f"{voices['asset']}",
        )

    for left, right in (
        ("release.json", "asset"),
        ("asset", "committed"),
        ("release.json", "committed"),
    ):
        a, b = voices[left], voices[right]
        if a is None or b is None:
            missing = left if a is None else right
            leg.add(
                f"{left}=={right}",
                SKIPPED,
                f"{missing} hash unavailable"
                + (f" ({reasons[missing]})" if missing in reasons else ""),
            )
        elif a == b:
            leg.add(f"{left}=={right}", PASS, f"both {a}")
        else:
            leg.add(f"{left}=={right}", FAIL, f"{left}={a} != {right}={b}")

    # The record-line hash needs corroboration: at least two voices, all in
    # agreement. A single uncompared hash is a fact, not a verification.
    present = [v for v in voices.values() if v is not None]
    the_hash = (
        present[0] if len(present) >= 2 and len(set(present)) == 1 else None
    )
    return leg, the_hash


def leg_workflow(
    version: str, commit: str | None, fetch: Fetcher, slug: str
) -> tuple[Leg, str | None]:
    """Leg 3: the release.yml run for this release concluded success."""
    leg = Leg("workflow")
    if commit is None:
        leg.add(
            "release-run",
            SKIPPED,
            "tag commit unknown (leg 1) — cannot match a run by head_sha",
        )
        return leg, None
    url = RUNS_API_URL.format(slug=slug)
    try:
        payload = json.loads(fetch(url).decode("utf-8"))
    except FetchError as exc:
        leg.add("release-run", SKIPPED, f"Actions API unreachable: {exc}")
        return leg, None
    except (ValueError, UnicodeDecodeError) as exc:
        leg.add("release-run", SKIPPED, f"Actions API response unparseable: {exc}")
        return leg, None
    runs = payload.get("workflow_runs") or []
    matches = [run for run in runs if run.get("head_sha") == commit]
    if not matches:
        leg.add(
            "release-run",
            SKIPPED,
            f"no release.yml run with head_sha {_short(commit)} among the "
            f"{len(runs)} most recent runs — inconclusive (older than the "
            "window, or the run rode a different head)",
        )
        return leg, None
    run = matches[0]  # the API returns newest-first
    run_id = str(run.get("id"))
    status = run.get("status")
    conclusion = run.get("conclusion")
    if status != "completed":
        leg.add(
            "release-run",
            SKIPPED,
            f"run {run_id} at {_short(commit)} is still {status!r} — "
            "re-verify once it completes",
        )
    elif conclusion == "success":
        leg.add(
            "release-run",
            PASS,
            f"run {run_id} at {_short(commit)} concluded success",
        )
    else:
        leg.add(
            "release-run",
            FAIL,
            f"run {run_id} at {_short(commit)} concluded {conclusion!r} — "
            "expected 'success'",
        )
    return leg, run_id


def record_line(
    version: str,
    tag_object: str | None,
    commit: str | None,
    the_hash: str | None,
    run_id: str | None,
    run_verified: bool,
) -> str:
    """The paste-ready release-record line runbook §5 asks to record."""
    parts = [f"v{version}"]
    if tag_object and commit:
        parts.append(f"tag object {_short(tag_object)} -> commit {_short(commit)}")
    elif commit:
        parts.append(f"commit {_short(commit)}")
    else:
        parts.append("tag/commit UNRESOLVED")
    parts.append(f"sha256 {the_hash}" if the_hash else "sha256 UNVERIFIED")
    if run_id and run_verified:
        parts.append(f"release.yml run {run_id} green")
    elif run_id:
        parts.append(f"release.yml run {run_id} (see leg 3)")
    else:
        parts.append("release.yml run UNVERIFIED")
    return " · ".join(parts)


def run(
    version: str,
    *,
    git: GitRunner,
    fetch: Fetcher,
    slug: str = REPO_SLUG,
) -> int:
    if not _SEMVER_RE.match(version):
        print(
            f"verify_release: error: malformed version {version!r} — "
            "expected X.Y.Z (digits only, no v prefix)"
        )
        return 2

    print(f"verify_release: v{version} — post-release verification (runbook §5)")
    print()

    tag_leg, commit = leg_tag(version, git)
    tag_leg.settle(TAG_SUBSTANTIVE)
    # resolve_tag recorded the tag object inside the leg; recover it for the
    # record line (first check's detail carries it) without re-running git.
    tag_object = None
    obj = git(["rev-parse", "--verify", "--quiet", f"refs/tags/v{version}"])
    if obj.returncode == 0:
        tag_object = obj.text
    elif tag_leg.checks and "object " in tag_leg.checks[0].detail:
        tag_object = tag_leg.checks[0].detail.split("object ", 1)[1].split(")")[0]

    sha_leg, the_hash = leg_sha256(version, commit, git, fetch, slug)
    sha_leg.settle(SHA_SUBSTANTIVE)
    wf_leg, run_id = leg_workflow(version, commit, fetch, slug)
    wf_leg.settle(WORKFLOW_SUBSTANTIVE)

    legs = [tag_leg, sha_leg, wf_leg]
    for index, leg in enumerate(legs, start=1):
        print(f"[{index}/{len(legs)}] {leg.name} — {leg.verdict}")
        for check in leg.checks:
            print(f"    {check.status:<7} {check.name}: {check.detail}")
        print()

    counts = {PASS: 0, FAIL: 0, SKIPPED: 0}
    for leg in legs:
        counts[leg.verdict] += 1
    failed = counts[FAIL] > 0
    print(
        f"verdict: {counts[PASS]} PASS · {counts[FAIL]} FAIL · "
        f"{counts[SKIPPED]} SKIPPED -> exit {1 if failed else 0}"
    )
    skipped_checks = [
        (leg.name, c) for leg in legs for c in leg.checks if c.status == SKIPPED
    ]
    if not failed and skipped_checks:
        print(
            f"WARNING: {len(skipped_checks)} check(s) SKIPPED — the skipped "
            "facts are UNVERIFIED, not verified-good:"
        )
        for leg_name, check in skipped_checks:
            print(f"    {leg_name}/{check.name}: {check.detail}")
    if counts[PASS] == 0 and not failed:
        print(
            "WARNING: NOTHING WAS VERIFIED — every leg skipped. Exit 0 means "
            "'no verified failure', NOT a green release; re-run where the "
            "walls are down (runbook §5: never skip)."
        )
    print()
    print("release-record line (paste-ready):")
    print(
        "  "
        + record_line(
            version,
            tag_object,
            commit,
            the_hash,
            run_id,
            run_verified=(wf_leg.verdict == PASS),
        )
    )
    return 1 if failed else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("version", help="the released version to verify, X.Y.Z")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="repo root (default: this script's repo)",
    )
    parser.add_argument(
        "--repo-slug",
        default=REPO_SLUG,
        help=f"owner/repo for release downloads (default: {REPO_SLUG})",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="per-download timeout in seconds (default: 30)",
    )
    parser.add_argument(
        "--offline",
        action="store_true",
        help="skip every network download (legs degrade to SKIPPED)",
    )
    args = parser.parse_args(argv)
    git = make_git_runner(args.root.resolve())
    if args.offline:
        return run(
            args.version,
            git=offline_git_runner(git),
            fetch=offline_fetcher,
            slug=args.repo_slug,
        )
    return run(args.version, git=git, fetch=make_fetcher(args.timeout), slug=args.repo_slug)


if __name__ == "__main__":
    sys.exit(main())
