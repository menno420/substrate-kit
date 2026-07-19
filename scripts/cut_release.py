#!/usr/bin/env python3
"""cut_release — mechanize the release cut's PREPARATION as one command.

Why + provenance: every release cut (19 so far, v1.0.0 → v1.15.0) hand-made
the same three edits — bump ``KIT_VERSION`` in ``src/engine/lib/config.py``
and ``version`` in ``pyproject.toml`` in the SAME commit, and restructure
``CHANGELOG.md`` (``[Unreleased]`` → ``[X.Y.Z] - <date>``, machine comment
inserted, fresh empty ``[Unreleased]`` opened above). The hand-move of the
KF-5 preamble block was recorded release-cut friction; the structure checker
(``scripts/check_changelog_structure.py``, PR #351) pinned the input shape,
which makes the transform a deterministic text operation. Design authority:
the PR #351 session card's 💡 ender (``.sessions/2026-07-14-changelog-
structure-check.md``) + ``docs/operations/release-runbook.md`` (canonical
recipe — this script mechanizes §2's file edits, nothing else).
Added 2026-07-14. Reliability (PL-008): UNVERIFIED — confirm its output
against ground truth at the next real cuts before trusting it; **delete
this if it proves unreliable over multiple sessions.**

What it does (``--write``) or previews as a diff (default, DRY-RUN):

1. Bumps BOTH version homes in one coherent edit: ``src/engine/lib/config.py``
   ``KIT_VERSION`` and ``pyproject.toml`` ``[project] version``.
2. Transforms ``CHANGELOG.md``: retitles ``## [Unreleased]`` to
   ``## [X.Y.Z] - <date>``, keeps the preamble prose (KF-5 blocks) exactly
   where it is, inserts the ``<!-- release: … -->`` machine comment between
   the preamble and the first typed heading, and opens a fresh empty
   ``## [Unreleased]`` above — the layout every released section carries.
   The result is verified against ``check_changelog_structure``'s own rules
   before anything is written.
3. Prints the follow-up checklist of steps it deliberately does NOT do:
   dist regen + byte-pin, commit/branch/PR, merge on green, ``release.yml``
   ``workflow_dispatch``, and the three-way sha256 post-release verification
   (all copied from the runbook — the runbook stays canonical).

What it NEVER does: dispatch a workflow, push, commit, or touch the
network. It only edits the working tree, and only with ``--write``.

Refusals (exit non-zero, clear message): malformed version string; target
not exactly one semver increment (major/minor/patch) of the current
version; target already released (a ``## [X.Y.Z]`` section exists); the
two version homes currently disagree; ``[Unreleased]`` empty (nothing to
release) or structurally invalid; and, for ``--write`` only, a dirty git
tree.

Repo-level tooling, not engine code: lives in scripts/, uses print, never
ships in dist/bootstrap.py, adopter repos never receive it. Stdlib only.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import difflib
import re
import subprocess
import sys
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))
_SRC_DIR = _SCRIPTS_DIR.parent / "src"
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

import check_changelog_structure as _ccs  # noqa: E402
from engine.currency import (  # noqa: E402
    ADOPTERS_RELPATH,
    local_self_scan,
    restamp_self_row,
)

CONFIG_RELPATH = "src/engine/lib/config.py"
PYPROJECT_RELPATH = "pyproject.toml"
KIT_CONFIG_RELPATH = "substrate.config.json"
CHANGELOG_RELPATH = "CHANGELOG.md"

_SEMVER_RE = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")
_KIT_VERSION_RE = re.compile(r'^KIT_VERSION = "(\d+\.\d+\.\d+)"$', re.MULTILINE)
_PYPROJECT_VERSION_RE = re.compile(r'^version = "(\d+\.\d+\.\d+)"$', re.MULTILINE)
# The kit's own substrate.config.json self-pin — kept equal to KIT_VERSION so
# the kit's own `currency` row reads `current` (the tree-internal false-DRIFT
# fix). Matches the pretty-printed `"kit_version": "X.Y.Z"` line.
_KIT_CONFIG_VERSION_RE = re.compile(
    r'^(?P<indent>\s*)"kit_version": "(\d+\.\d+\.\d+)"', re.MULTILINE
)
_H3_RE = re.compile(r"^###\s")

# The machine comment every released section carries; release.yml refuses a
# version whose CHANGELOG section lacks it. state_migration / min_upgrade_from
# have been constant across all cuts to date; breaking follows the semver
# class (MAJOR = breaking per the CHANGELOG header contract). The checklist
# tells the operator to verify all three before committing.
_MACHINE_COMMENT = (
    "<!-- release: breaking={breaking} state_migration=false "
    "min_upgrade_from=1.0.0 -->"
)

FOLLOWUP_CHECKLIST = """\
Follow-up checklist — steps cut_release.py deliberately does NOT do
(canonical recipe: docs/operations/release-runbook.md):

 1. Review the new [{version}] section: verify the machine comment flags
    (breaking= / state_migration= / min_upgrade_from=) and add the
    release-class prose summary to the section preamble if desired (the
    [Unreleased] preamble was kept verbatim).
 2. Dist regen + byte-pin: python3 src/build_bootstrap.py, then confirm the
    builder's printed byte count equals `wc -c dist/bootstrap.py`.
 3. Claim, then bump PR (born-red): work-claim
    control/claims/release-v{version}.md on main first (control fast-lane
    PR); cut the bump branch from post-claim main; born-red session card is
    the first commit; open the PR ready + arm auto-merge at open.
 4. Verify locally (runbook §3):
      python3.10 -m pytest tests/ -q
      python3.10 -m ruff check src/engine/
      python3 src/build_release_json.py --version {version} --verify-only
      python3 scripts/check_idea_index.py
      python3 scripts/check_program_law.py
      python3 dist/bootstrap.py check --strict
    (the only acceptable pre-flip red is the designed born-red hold naming
    this session's own card).
 5. Flip the card `complete` as the last commit; auto-merge lands it on
    green.
 6. Publish: dispatch release.yml via workflow_dispatch with input
    version={version} on main at the bump merge SHA. The run creates
    annotated tag v{version} and the GitHub Release with three assets:
    bootstrap.py, bootstrap.py.sha256, release.json.
 7. Three-way verification (never skip): independently download the
    released bootstrap.py; its sha256 must equal BOTH the release.json
    sha256 field AND the committed dist/bootstrap.py at the bump SHA.
    Record run id, tag object, commit SHA, and the hash in the release
    record.
 8. Aftermath: the substrate-kit self-row was already stamped into this bump
    (network-free, at --write time), so the adopters regen (python3
    dist/bootstrap.py currency → docs/adopters.md) now only has to refresh
    SIBLING rows; control/status.md release record + claim delete; then the
    distribution wave (upgrade each adopter, merged on green, then registry
    regen).\
"""


class CutError(Exception):
    """A refusal — printed as the error message, exit 1."""


def parse_semver(version: str) -> tuple[int, int, int]:
    m = _SEMVER_RE.match(version)
    if not m:
        raise CutError(
            f"malformed version {version!r} — expected X.Y.Z (digits only, "
            "no v prefix)"
        )
    return int(m.group(1)), int(m.group(2)), int(m.group(3))


def classify_increment(current: str, target: str) -> str:
    """Return 'major'/'minor'/'patch', or refuse."""
    cur = parse_semver(current)
    tgt = parse_semver(target)
    if tgt == (cur[0] + 1, 0, 0):
        return "major"
    if tgt == (cur[0], cur[1] + 1, 0):
        return "minor"
    if tgt == (cur[0], cur[1], cur[2] + 1):
        return "patch"
    raise CutError(
        f"target {target} is not a sensible increment of current {current} — "
        f"expected one of {cur[0] + 1}.0.0 (MAJOR), "
        f"{cur[0]}.{cur[1] + 1}.0 (MINOR), or "
        f"{cur[0]}.{cur[1]}.{cur[2] + 1} (PATCH)"
    )


def read_version_homes(root: Path) -> tuple[str, str, str, str, str, str]:
    """Return the three version homes' text + parsed version.

    Order: (config_text, config_version, pyproject_text, pyproject_version,
    kit_config_text, kit_config_version). The kit's own
    ``substrate.config.json`` ``kit_version`` self-pin is the third home — it
    is kept equal to ``KIT_VERSION`` so the kit's own ``currency`` row reads
    ``current`` instead of a permanent tree-internal false-DRIFT.
    """
    config_path = root / CONFIG_RELPATH
    pyproject_path = root / PYPROJECT_RELPATH
    kit_config_path = root / KIT_CONFIG_RELPATH
    if not config_path.is_file():
        raise CutError(f"{CONFIG_RELPATH} not found under {root}")
    if not pyproject_path.is_file():
        raise CutError(f"{PYPROJECT_RELPATH} not found under {root}")
    if not kit_config_path.is_file():
        raise CutError(f"{KIT_CONFIG_RELPATH} not found under {root}")
    config_text = config_path.read_text(encoding="utf-8")
    pyproject_text = pyproject_path.read_text(encoding="utf-8")
    kit_config_text = kit_config_path.read_text(encoding="utf-8")
    cfg_matches = _KIT_VERSION_RE.findall(config_text)
    if len(cfg_matches) != 1:
        raise CutError(
            f"expected exactly one KIT_VERSION line in {CONFIG_RELPATH}, "
            f"found {len(cfg_matches)}"
        )
    py_matches = _PYPROJECT_VERSION_RE.findall(pyproject_text)
    if len(py_matches) != 1:
        raise CutError(
            f'expected exactly one `version = "X.Y.Z"` line in '
            f"{PYPROJECT_RELPATH}, found {len(py_matches)}"
        )
    kit_matches = _KIT_CONFIG_VERSION_RE.findall(kit_config_text)
    if len(kit_matches) != 1:
        raise CutError(
            f'expected exactly one `"kit_version": "X.Y.Z"` line in '
            f"{KIT_CONFIG_RELPATH}, found {len(kit_matches)}"
        )
    return (
        config_text,
        cfg_matches[0],
        pyproject_text,
        py_matches[0],
        kit_config_text,
        kit_matches[0][1],
    )


def bump_version_texts(
    config_text: str, pyproject_text: str, kit_config_text: str, target: str
) -> tuple[str, str, str]:
    new_config = _KIT_VERSION_RE.sub(f'KIT_VERSION = "{target}"', config_text)
    new_pyproject = _PYPROJECT_VERSION_RE.sub(
        f'version = "{target}"', pyproject_text
    )
    new_kit_config = _KIT_CONFIG_VERSION_RE.sub(
        rf'\g<indent>"kit_version": "{target}"', kit_config_text
    )
    return new_config, new_pyproject, new_kit_config


def transform_changelog(text: str, target: str, date: str, breaking: bool) -> str:
    """[Unreleased] → [target] - date, per the runbook + checker shape."""
    if f"## [{target}]" in text:
        raise CutError(
            f"version {target} already has a `## [{target}]` section in "
            f"{CHANGELOG_RELPATH} — already released?"
        )
    findings = _ccs.check_unreleased(text)
    if findings:
        details = "\n".join(f"  {f.path}: [{f.kind}] {f.message}" for f in findings)
        raise CutError(
            "[Unreleased] is structurally invalid — fix it first (run "
            "scripts/check_changelog_structure.py):\n" + details
        )

    lines = text.splitlines()
    unreleased_idx = None
    for i, line in enumerate(lines):
        if _ccs._UNRELEASED_RE.match(line):
            unreleased_idx = i
            break
    if unreleased_idx is None:
        raise CutError(f"no `## [Unreleased]` section in {CHANGELOG_RELPATH}")

    body_start = unreleased_idx + 1
    body_end = body_start
    while body_end < len(lines) and not _ccs._SECTION_RE.match(lines[body_end]):
        body_end += 1
    body = lines[body_start:body_end]

    first_h3_offset = None
    for offset, line in enumerate(body):
        if _H3_RE.match(line):
            first_h3_offset = offset
            break
    if first_h3_offset is None:
        raise CutError(
            "[Unreleased] has no typed `###` sections — nothing to release"
        )

    comment = _MACHINE_COMMENT.format(breaking=str(breaking).lower())
    new_body = (
        body[:first_h3_offset] + [comment, ""] + body[first_h3_offset:]
    )
    new_lines = (
        lines[:unreleased_idx]
        + ["## [Unreleased]", "", f"## [{target}] - {date}"]
        + new_body
        + lines[body_end:]
    )
    new_text = "\n".join(new_lines)
    if text.endswith("\n"):
        new_text += "\n"

    # Self-check: the fresh [Unreleased] must be clean under the checker,
    # and the new released section must satisfy the same shape rules the
    # checker enforces on [Unreleased] (verified by retitling it).
    if _ccs.check_unreleased(new_text):
        raise CutError(
            "internal error: transformed [Unreleased] fails "
            "check_changelog_structure — refusing to proceed"
        )
    released_as_unreleased = new_text.replace(
        f"## [{target}] - {date}", "## [Unreleased]", 1
    )
    # Drop the (now empty) fresh [Unreleased] above so the checker sees the
    # retitled released section as the one [Unreleased] it scans.
    first = released_as_unreleased.index("## [Unreleased]")
    second = released_as_unreleased.index("## [Unreleased]", first + 1)
    section = released_as_unreleased[second:]
    if _ccs.check_unreleased(section):
        raise CutError(
            f"internal error: new [{target}] section fails the structure "
            "rules — refusing to proceed"
        )
    return new_text


def ensure_clean_tree(root: Path) -> None:
    try:
        proc = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=root,
            capture_output=True,
            text=True,
            timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CutError(f"cannot verify git tree cleanliness: {exc}") from exc
    if proc.returncode != 0:
        raise CutError(
            "cannot verify git tree cleanliness: "
            + (proc.stderr.strip() or f"git exited {proc.returncode}")
        )
    if proc.stdout.strip():
        raise CutError(
            "git tree is dirty — commit or stash before --write:\n"
            + proc.stdout.rstrip()
        )


def _diff(old: str, new: str, relpath: str) -> str:
    return "".join(
        difflib.unified_diff(
            old.splitlines(keepends=True),
            new.splitlines(keepends=True),
            fromfile=f"a/{relpath}",
            tofile=f"b/{relpath}",
        )
    )


def run(root: Path, target: str, write: bool, date: str) -> int:
    parse_semver(target)
    (
        config_text,
        cfg_version,
        pyproject_text,
        py_version,
        kit_config_text,
        kit_config_version,
    ) = read_version_homes(root)
    if not (cfg_version == py_version == kit_config_version):
        raise CutError(
            f"version homes disagree — {CONFIG_RELPATH} says {cfg_version}, "
            f"{PYPROJECT_RELPATH} says {py_version}, {KIT_CONFIG_RELPATH} says "
            f"{kit_config_version}; reconcile them first (they are bumped in "
            "the same commit by contract)"
        )
    increment = classify_increment(cfg_version, target)
    changelog_path = root / CHANGELOG_RELPATH
    if not changelog_path.is_file():
        raise CutError(f"{CHANGELOG_RELPATH} not found under {root}")
    changelog_text = changelog_path.read_text(encoding="utf-8")
    new_changelog = transform_changelog(
        changelog_text, target, date, breaking=(increment == "major")
    )
    new_config, new_pyproject, new_kit_config = bump_version_texts(
        config_text, pyproject_text, kit_config_text, target
    )

    if write:
        ensure_clean_tree(root)

    mode = "WRITE" if write else "DRY-RUN"
    print(f"cut_release {cfg_version} -> {target} ({increment.upper()}) [{mode}]")
    print()
    for relpath, old, new in (
        (CONFIG_RELPATH, config_text, new_config),
        (PYPROJECT_RELPATH, pyproject_text, new_pyproject),
        (KIT_CONFIG_RELPATH, kit_config_text, new_kit_config),
        (CHANGELOG_RELPATH, changelog_text, new_changelog),
    ):
        print(_diff(old, new, relpath), end="")
    print()

    if write:
        (root / CONFIG_RELPATH).write_text(new_config, encoding="utf-8")
        (root / PYPROJECT_RELPATH).write_text(new_pyproject, encoding="utf-8")
        (root / KIT_CONFIG_RELPATH).write_text(new_kit_config, encoding="utf-8")
        changelog_path.write_text(new_changelog, encoding="utf-8")
        # Self-row registry stamp (B-2): substrate.config.json now reads the
        # target version, so a network-free local scan renders a current
        # self-row. Restamp only docs/adopters.md's substrate-kit row (+ the
        # `kit release:` token) so the bump PR carries a current self-row and
        # the aftermath `currency` regen only has to refresh sibling rows.
        # Never touches the network or any sibling row (KF-2).
        adopters_path = root / ADOPTERS_RELPATH
        if adopters_path.is_file():
            old_adopters = adopters_path.read_text(encoding="utf-8")
            # local_self_scan reads config_pin from the just-bumped
            # substrate.config.json (= target) BUT tree_version from
            # dist/bootstrap.py's header, which is still the OLD version here:
            # the dist rebuild is FOLLOWUP step 2, not done by --write. Left as
            # is, the scan renders tree(old) != pin(target) -> a false
            # tree-internal DRIFT in the committed self-row (kit #472). Stamp
            # the self-row from the release's tree truth (target) instead: the
            # bump PR can only merge once dist/bootstrap.py is rebuilt to target
            # (test_committed_bootstrap_is_current byte-pins committed dist ==
            # build(src)), so every mergeable PR carries dist == target and the
            # `current` self-row is honest for the committed state — restoring
            # the B-2 intent ("renders a current self-row").
            self_scan = local_self_scan(root)
            if self_scan.tree_version is not None:
                self_scan.tree_version = target
            new_adopters = restamp_self_row(old_adopters, target, self_scan)
            if new_adopters != old_adopters:
                adopters_path.write_text(new_adopters, encoding="utf-8")
                print(
                    f"self-row stamped: {ADOPTERS_RELPATH} substrate-kit row "
                    f"-> v{target} (network-free; sibling rows untouched)"
                )
        print(
            f"applied: all three version homes {cfg_version} -> {target}; "
            f"{CHANGELOG_RELPATH} [Unreleased] -> [{target}] - {date}"
        )
    else:
        print("DRY-RUN — no files changed. Re-run with --write to apply.")
    print()
    print(FOLLOWUP_CHECKLIST.format(version=target))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("version", help="the new version to cut, X.Y.Z")
    parser.add_argument(
        "--write",
        action="store_true",
        help="apply the edits to the working tree (default: dry-run diff)",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="repo root (default: this script's repo)",
    )
    parser.add_argument(
        "--date",
        default=None,
        help="release date YYYY-MM-DD (default: today, UTC)",
    )
    args = parser.parse_args(argv)
    date = args.date or _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d")
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", date):
        print(f"cut_release: error: malformed --date {date!r} (want YYYY-MM-DD)")
        return 1
    try:
        return run(args.root.resolve(), args.version, args.write, date)
    except CutError as exc:
        print(f"cut_release: error: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
