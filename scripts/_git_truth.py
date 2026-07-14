#!/usr/bin/env python3
"""_git_truth — shared shallow/graft detection + safe git-ancestry answers.

THE FACT THIS MODULE OWNS: **a shallow (grafted) clone severs real ancestry
paths, so a NEGATIVE git ancestry answer on one proves nothing.** Container
clones here are routinely shallow (``.git/shallow`` present, history grafted),
and on such a clone ``git merge-base --is-ancestor A B`` returns a FALSE
negative for commits that ARE ancestors on origin — live-hit twice:

- PR #355 (``check_idea_index`` merged-reality leg): the session's own
  container clone was shallow at 51 of 441 commits — absence of a commit
  proved nothing about a ship claim.
- PR #357 (``verify_release`` tag leg): ``merge-base --is-ancestor`` returned
  a false negative for v1.15.0's REAL bump commit (``eaf4f23``) because the
  grafted history disconnected it from ``origin/main``.

The degradation rule both consumers had re-implemented independently (and a
third night's session would have re-derived again — the extraction trigger,
PR #357's session-card 💡 ender): **a positive ancestry answer is still a
proof; a negative one on a shallow clone degrades to "unprovable" — SKIP
honestly, never false-FAIL.** This module is the single home of that rule;
new consumers import it instead of writing a fourth variant.

Seam: every function takes a ``GitCommand`` runner —
``run(args) -> (returncode, stdout_text, stderr_text)`` — so callers keep
their own subprocess wrappers / injected test fakes (``make_runner`` is the
default subprocess-backed one). Verdicts:

- ``YES``        — provable: git answered "is an ancestor" (rc 0).
- ``NO``         — provable negative: git said no (rc 1) on a NOT-shallow
                   clone; with ``missing_as_no=True`` an rc-128
                   unknown-commit answer on a NOT-shallow clone also counts
                   (full history + absent commit = genuinely not reachable —
                   the ``check_idea_index`` call-site policy).
- ``UNPROVABLE`` — a negative on a confirmed-shallow clone, or any git
                   error/other rc: not evidence of anything; degrade (SKIP),
                   never FAIL on it.

Repo-level tooling, not engine code: lives in scripts/, never ships in
dist/bootstrap.py, adopter repos never receive it. Stdlib only. Provenance:
extracted 2026-07-14 from the two shipped, test-covered implementations named
above (behavior-preserving refactor, not a new unverified tool).
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Sequence

# run(args) -> (returncode, stdout text, stderr text). rc 127 = git itself
# could not run (the convention check_idea_index._git established).
GitCommand = Callable[[Sequence[str]], tuple[int, str, str]]

YES = "yes"
NO = "no"
UNPROVABLE = "unprovable"


@dataclass(frozen=True)
class AncestryAnswer:
    """One safe ancestry answer: the verdict plus the raw evidence behind it.

    ``verdict``    — YES / NO / UNPROVABLE (module constants).
    ``returncode`` — the raw ``merge-base --is-ancestor`` exit code.
    ``shallow``    — True/False when shallowness was checked and determinable,
                     None when not checked (rc 0) or undeterminable.
    ``detail``     — stderr of the failed git call for UNPROVABLE-on-error,
                     or a one-line reason for the shallow degradation.
    """

    verdict: str
    returncode: int
    shallow: bool | None = None
    detail: str = ""


def make_runner(root: Path, timeout: int = 30) -> GitCommand:
    """Default subprocess-backed runner rooted at ``root`` (rc 127 = no git)."""

    def run(args: Sequence[str]) -> tuple[int, str, str]:
        try:
            proc = subprocess.run(
                ["git", "-C", str(root), *args],
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )
        except (OSError, subprocess.SubprocessError) as exc:
            return 127, "", str(exc)
        return proc.returncode, proc.stdout, proc.stderr

    return run


def is_shallow(run: GitCommand) -> bool | None:
    """True/False per ``rev-parse --is-shallow-repository``; None = unknown.

    None (git errored / unavailable) is deliberately distinct from False:
    "couldn't even ask" must never be read as "provably a full clone".
    """
    rc, out, _err = run(["rev-parse", "--is-shallow-repository"])
    if rc != 0:
        return None
    return out.strip() == "true"


def provable_ancestry(
    run: GitCommand,
    ancestor: str,
    descendant: str,
    *,
    missing_as_no: bool = False,
) -> AncestryAnswer:
    """Answer "is ``ancestor`` an ancestor of ``descendant``?" — safely.

    The one rule this module exists for: a negative answer is only evidence
    on a NOT-shallow clone. On a confirmed-shallow clone it degrades to
    UNPROVABLE (the caller SKIPs, never FAILs). ``missing_as_no`` opts in to
    treating rc 128 (unknown/invalid commit) as a real negative — sound only
    where the caller has already pinned the ref side to exist (the
    ``check_idea_index`` merged-reality policy); the default keeps rc 128
    UNPROVABLE (``verify_release``'s "could not test" policy).
    """
    rc, _out, err = run(["merge-base", "--is-ancestor", ancestor, descendant])
    if rc == 0:
        return AncestryAnswer(YES, rc)
    shallow = is_shallow(run)
    if shallow is True and rc in (1, 128):
        # Both negative shapes are the graft class on a shallow clone: rc 1
        # (paths severed — the #357 live hit) and rc 128 (the commit itself
        # outside the truncated history — the #355 class).
        return AncestryAnswer(
            UNPROVABLE,
            rc,
            shallow=True,
            detail=(
                "negative ancestry answer on a SHALLOW (grafted) clone — "
                "unreliable; re-check on a full clone"
            ),
        )
    if rc == 1 or (rc == 128 and missing_as_no):
        return AncestryAnswer(NO, rc, shallow=shallow)
    return AncestryAnswer(UNPROVABLE, rc, shallow=shallow, detail=err.strip())
