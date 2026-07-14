"""Safe git-ancestry answers for engine code (ORDER 022 push guard).

Engine-shipped port of the repo-tooling helper ``scripts/_git_truth.py``
(PR #358): that module is deliberately repo-level ("lives in scripts/, never
ships in dist/bootstrap.py, adopter repos never receive it"), but the ORDER
022 stop-hook merged-head push guard must ride the dist into every adopter —
so the primitive lives here too, byte-identical in behavior, with a parity
test (``tests/test_git_truth.py``) pinning the two copies against drift.

THE FACT THIS MODULE OWNS: **a shallow (grafted) clone severs real ancestry
paths, so a NEGATIVE git ancestry answer on one proves nothing.** Container
clones are routinely shallow, and on such a clone ``git merge-base
--is-ancestor A B`` returns a FALSE negative for commits that ARE ancestors
on origin (live-hit in kit PRs #355 and #357). The rule: **a positive
ancestry answer is still a proof; a negative one on a shallow clone degrades
to "unprovable" — callers SKIP honestly, never false-FAIL.**

Seam: every function takes a ``GitCommand`` runner —
``run(args) -> (returncode, stdout_text, stderr_text)`` — so callers keep
their own subprocess wrappers / injected test fakes (``make_runner`` is the
default subprocess-backed one). Verdicts:

- ``YES``        — provable: git answered "is an ancestor" (rc 0).
- ``NO``         — provable negative: git said no (rc 1) on a NOT-shallow
                   clone; with ``missing_as_no=True`` an rc-128
                   unknown-commit answer on a NOT-shallow clone also counts
                   (full history + absent commit = genuinely not reachable).
- ``UNPROVABLE`` — a negative on a confirmed-shallow clone, or any git
                   error/other rc: not evidence of anything; degrade (SKIP),
                   never FAIL on it.
"""

from __future__ import annotations

# §3.2 carve-out #2 (ORDER 022, mirroring cli.py's ORDER 018 carve-out):
# subprocess is banned in engine code — but the stop-hook merged-head push
# guard's ONLY evidence source is the local clone's git (is this branch's
# head already in origin/main?), and hooks run locally at session stop where
# no CI bash wrapper exists to do the git work. ``make_runner`` is the one
# subprocess touchpoint; every consumer takes the ``GitCommand`` seam so
# tests inject fakes and never shell out. Fail-open: rc 127 on any failure.
import subprocess  # noqa: TID251
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
