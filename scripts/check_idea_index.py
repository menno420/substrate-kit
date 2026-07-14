#!/usr/bin/env python3
"""check_idea_index — the B4 ideas-frontmatter + index checker (KL-6, plan §5.4).

Why + provenance: B4 ("ideas that ship and survive") needs a machine-readable
outcome record per idea; the founding plan §5.4 rules that the convention and
its checker ship in the same PR (the drift-before-next-session failure mode).
Added 2026-07-09 (band KL-6). Reliability (PL-008): UNVERIFIED — confirm its
findings against ground truth a few times across sessions before trusting it;
**delete this if it proves unreliable over multiple sessions.**

The convention (documented in ``docs/ideas/README.md`` + the planted
``ideas-README`` template): every ``docs/ideas/*.md`` entry except README.md
opens with a flat YAML-subset frontmatter block::

    ---
    state: captured | routed | promoted | historical
    origin: lab | owner | consumer:<owner>/<repo>
    shipped_pr: null | <int>
    shipped_repo: null | <owner>/<repo>
    merged_date: null | YYYY-MM-DD
    outcome: open | shipped | survived | reverted | rejected
    ---

What it enforces (exit 1 on any finding, 0 clean):

1. **Frontmatter grammar** — block present at byte one, all six required keys,
   values in their enums/shapes (unknown extra keys are tolerated — the kit's
   forward-compat posture).
2. **Outcome consistency** — ``shipped|survived|reverted`` require all three
   ship fields non-null; ``open|rejected`` require them null; ``survived``
   additionally requires ``merged_date`` ≥ 30 days old (the D-15/KF-8 survive
   window — a younger idea cannot have survived yet).
3. **Cohort key** — the filename ends ``-YYYY-MM-DD.md`` (B4 groups ideas by
   generation-month cohort, derived from the filename date).
4. **Index consistency** — every idea file is linked from
   ``docs/ideas/README.md``, and every relative ``*.md`` link in the README
   resolves to a file on disk.
5. **Body-state drift** (friction→guard from PR #311, 2026-07-12: a file's
   frontmatter said ``shipped_pr: 187`` while its body still read
   "captured", misdirecting dispatch into a redundant fix task) — when the
   frontmatter asserts a ship (``outcome`` in shipped/survived/reverted, or
   a non-null ``shipped_pr``) but the body's ``> **State:**`` line still
   opens ``captured``/``routed`` **without** a recognized reconciliation
   marker, that file fails. Recognized markers (designed from the real
   corpus): an arrow-chain State blockquote that reaches ``shipped``
   anywhere in the chain; a ``## Shipped`` section; a ``RULED`` /
   "preserved as written" banner (historical bodies kept verbatim on
   purpose). A body with **no** State line at all predates the convention
   and is skipped — the frontmatter is authoritative there.

6. **Merged reality** (💡 idea from the PR #349 session card, built
   2026-07-14) — shape checks 1–5 accept any *plausible* ship claim; this
   leg verifies the claim against **actual local git history** (no GitHub
   API — the repo is the ground truth for merge reachability):

   - ``shipped_pr`` — main's subject lines are searched for the PR's merge
     marker (squash ``(#N)`` or ``Merge pull request #N``). Found → the
     real merge date is derived from that commit and compared to
     ``merged_date`` (the in-PR flip convention writes an ANTICIPATED
     date; drift > ``DATE_DRIFT_TOLERANCE_DAYS`` is flagged with the real
     date so the fix is mechanical). Not found → flagged only when the
     claim is older than the **grace window** (see below).
   - ``merged_sha`` — an *optional* forward-compat key (unknown keys were
     always tolerated): when present and non-null it must be 7–40 hex
     chars (**enforcing** — a malformed SHA is a typo, never a timing
     issue), and a well-formed SHA must be an ancestor of main
     (``git merge-base --is-ancestor``) once past the grace window.

   **Grace window (``GRACE_WINDOW_DAYS`` = 7, from ``merged_date``, falling
   back to the filename cohort date):** the in-PR flip convention marks an
   idea ``shipped`` while its shipping PR is still open — and this repo's
   PRs can park for days on owner-gated review — so an unreachable claim
   younger than the window is CLEAN, not a finding. 7d over 48h because a
   48h window would flag every owner-gated park (e.g. #317/#345 live now);
   it is also the number the originating idea proposed.

   **Posture — advisory-first, biased against false reds:** every
   reachability/date finding is ADVISORY (printed with an ``[advisory]``
   marker, never exit-affecting). Only ``bad-merged-sha`` (malformed
   syntax) is enforcing, like the other shape findings. The whole leg
   degrades gracefully: when git is unavailable, the tree is not a repo,
   the clone is **shallow** (history truncated — absence of a commit
   proves nothing; this session's own container clone was shallow at 51 of
   441 commits), or no ref resolves, it self-skips with a note and zero
   findings. Ideas whose ``shipped_repo`` names a different repo than the
   local ``origin`` remote are skipped — unverifiable here by design.

Repo-level tooling, not engine code: lives in scripts/, uses print, never
ships in dist/bootstrap.py. Stdlib only (no PyYAML — the frontmatter is a
flat ``key: value`` subset by design so consumers never need a dependency).
"""

from __future__ import annotations

import argparse
import datetime as _dt
import re
import subprocess
import sys
from pathlib import Path
from typing import NamedTuple

IDEAS_RELDIR = "docs/ideas"
README_NAME = "README.md"

REQUIRED_KEYS = (
    "state",
    "origin",
    "shipped_pr",
    "shipped_repo",
    "merged_date",
    "outcome",
)
ALLOWED_STATE = ("captured", "routed", "promoted", "historical")
ALLOWED_OUTCOME = ("open", "shipped", "survived", "reverted", "rejected")
# Outcomes that assert a merged PR exists (ship fields required)…
SHIPPED_OUTCOMES = ("shipped", "survived", "reverted")
# …and outcomes that assert none does (ship fields must be null).
UNSHIPPED_OUTCOMES = ("open", "rejected")
SURVIVE_WINDOW_DAYS = 30  # D-15 / KF-8

_REPO_RE = re.compile(r"^[\w.-]+/[\w.-]+$")
_ORIGIN_RE = re.compile(r"^(lab|owner|consumer:[\w.-]+/[\w.-]+)$")
_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_COHORT_FILENAME_RE = re.compile(r"-\d{4}-\d{2}-\d{2}\.md$")
_KV_RE = re.compile(r"^([A-Za-z_][\w-]*):\s*(.*)$")
# Relative markdown links in the README ([text](file.md) — never absolute URLs).
_MD_LINK_RE = re.compile(r"\]\((?!https?://)([^)#]+\.md)\)")

# --- body-state drift (enforcement item 5) -------------------------------
# The body `> **State:** <word> …` line; the first word is the body's state.
_STATE_LINE_RE = re.compile(r"^>\s*\*\*State:\*\*\s*[*_`\s]*([A-Za-z-]+)")
# Body states that contradict a shipped frontmatter unless reconciled.
DRIFT_BODY_STATES = ("captured", "routed")
# Reconciliation markers (recognized from the real docs/ideas/ corpus):
_SHIPPED_WORD_RE = re.compile(r"\bshipped\b", re.IGNORECASE)  # arrow-chain tail
_SHIPPED_HEADING_RE = re.compile(r"^#{2,}\s+Shipped\b", re.MULTILINE)
_RULED_BANNER_RE = re.compile(r"^>\s*\*\*RULED\b", re.MULTILINE)
_PRESERVED_RE = re.compile(r"preserved[\s-]as[\s-]written", re.IGNORECASE)


# --- merged reality (enforcement item 6) ----------------------------------
GRACE_WINDOW_DAYS = 7  # in-flight/parked shipping PRs never false-red
DATE_DRIFT_TOLERANCE_DAYS = 1  # committer-local vs UTC dates skew ±1 day
_SHA_RE = re.compile(r"^[0-9a-fA-F]{7,40}$")
# owner/repo from any common remote-URL shape (https/ssh/proxy, ± .git).
_REMOTE_REPO_RE = re.compile(r"[:/]([\w.-]+)/([\w.-]+?)(?:\.git)?/?$")


class Finding(NamedTuple):
    path: str
    kind: str
    message: str


class GitReality(NamedTuple):
    """A loaded, trustworthy view of local git history (None when not)."""

    root: Path
    ref: str  # the verification ref: origin/main > main > HEAD
    repo_token: str | None  # lowercased `owner/repo` from the origin URL
    commits: tuple[tuple[str, _dt.date, str], ...]  # (sha, commit-date, subject)


def parse_frontmatter(text: str) -> tuple[dict[str, str] | None, str | None]:
    """Return ``(fields, error)`` for the leading frontmatter block.

    ``fields`` is None when the block is missing/unterminated/malformed, with
    ``error`` saying why. Values are raw strings (``null`` stays literal —
    the validators interpret it).
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, "no frontmatter block at the top of the file (line 1 must be `---`)"
    fields: dict[str, str] = {}
    for i, line in enumerate(lines[1:], start=2):
        if line.strip() == "---":
            return fields, None
        if not line.strip():
            continue
        match = _KV_RE.match(line)
        if not match:
            return None, f"line {i}: not a flat `key: value` pair ({line.strip()!r})"
        fields[match.group(1)] = match.group(2).strip()
    return None, "frontmatter block never closed (missing trailing `---`)"


def _is_null(value: str) -> bool:
    return value in ("null", "~", "")


def validate_fields(
    relpath: str,
    fields: dict[str, str],
    today: _dt.date,
) -> list[Finding]:
    findings: list[Finding] = []

    def bad(kind: str, message: str) -> None:
        findings.append(Finding(relpath, kind, message))

    for key in REQUIRED_KEYS:
        if key not in fields:
            bad("missing-key", f"required frontmatter key `{key}` is missing")
    if findings:
        return findings

    state = fields["state"]
    if state not in ALLOWED_STATE:
        bad("bad-state", f"state {state!r} not in {ALLOWED_STATE}")

    if not _ORIGIN_RE.match(fields["origin"]):
        bad(
            "bad-origin",
            f"origin {fields['origin']!r} must be `lab`, `owner`, or `consumer:<owner>/<repo>`",
        )

    outcome = fields["outcome"]
    if outcome not in ALLOWED_OUTCOME:
        bad("bad-outcome", f"outcome {outcome!r} not in {ALLOWED_OUTCOME}")
        return findings

    pr_raw = fields["shipped_pr"]
    repo_raw = fields["shipped_repo"]
    date_raw = fields["merged_date"]

    if not _is_null(pr_raw) and not pr_raw.isdigit():
        bad("bad-shipped-pr", f"shipped_pr {pr_raw!r} must be null or a PR number")
    if not _is_null(repo_raw) and not _REPO_RE.match(repo_raw):
        bad("bad-shipped-repo", f"shipped_repo {repo_raw!r} must be null or `<owner>/<repo>`")
    merged_date: _dt.date | None = None
    if not _is_null(date_raw):
        if not _DATE_RE.match(date_raw):
            bad("bad-merged-date", f"merged_date {date_raw!r} must be null or YYYY-MM-DD")
        else:
            try:
                merged_date = _dt.date.fromisoformat(date_raw)
            except ValueError:
                bad("bad-merged-date", f"merged_date {date_raw!r} is not a real date")

    ship_fields_null = [_is_null(pr_raw), _is_null(repo_raw), _is_null(date_raw)]
    if outcome in SHIPPED_OUTCOMES and any(ship_fields_null):
        bad(
            "outcome-inconsistent",
            f"outcome `{outcome}` requires shipped_pr + shipped_repo + merged_date "
            "all non-null (it asserts a merged PR exists)",
        )
    if outcome in UNSHIPPED_OUTCOMES and not all(ship_fields_null):
        bad(
            "outcome-inconsistent",
            f"outcome `{outcome}` requires the ship fields to be null "
            "(a built-then-reverted idea is `reverted`, not `rejected`)",
        )
    if outcome == "survived" and merged_date is not None:
        age = (today - merged_date).days
        if age < SURVIVE_WINDOW_DAYS:
            bad(
                "survived-too-young",
                f"outcome `survived` needs merged_date ≥ {SURVIVE_WINDOW_DAYS} days old "
                f"(D-15 survive window); {date_raw} is {age} days old",
            )
    return findings


def _state_blockquote(text: str) -> tuple[str | None, str]:
    """Return ``(first_state_word, blockquote)`` for the body's State line.

    The blockquote is the contiguous run of ``>`` lines starting at the
    ``> **State:**`` line — the arrow-chain lives inside it. ``(None, "")``
    when the body has no State line (pre-convention bodies: frontmatter is
    authoritative, no drift signal).
    """
    lines = text.splitlines()
    for i, line in enumerate(lines):
        match = _STATE_LINE_RE.match(line)
        if not match:
            continue
        block = [line]
        for nxt in lines[i + 1 :]:
            if not nxt.startswith(">"):
                break
            block.append(nxt)
        return match.group(1).lower(), "\n".join(block)
    return None, ""


def check_body_state_drift(relpath: str, fields: dict[str, str], text: str) -> list[Finding]:
    """Enforcement item 5 — shipped frontmatter vs. a stale body State line.

    Fails (hard error, like every other finding) when the frontmatter says
    shipped but the body State line still opens captured/routed and no
    reconciliation marker is present. See the module docstring for the
    marker set and the PR #311 provenance.
    """
    outcome = fields.get("outcome", "")
    pr_raw = fields.get("shipped_pr", "null")
    fm_shipped = outcome in SHIPPED_OUTCOMES or not _is_null(pr_raw)
    if not fm_shipped:
        return []
    state_word, blockquote = _state_blockquote(text)
    if state_word is None or state_word not in DRIFT_BODY_STATES:
        return []
    # Recognized reconciliation markers, cheapest first:
    if _SHIPPED_WORD_RE.search(blockquote):  # arrow-chain reaches `shipped`
        return []
    if _SHIPPED_HEADING_RE.search(text):  # a `## Shipped` section documents it
        return []
    if _RULED_BANNER_RE.search(text) or _PRESERVED_RE.search(text):  # historical
        return []
    return [
        Finding(
            relpath,
            "body-state-drift",
            f"frontmatter says outcome=`{outcome}` / shipped_pr=`{pr_raw}` but the body "
            f"`> **State:**` line still reads `{state_word}` with no reconciliation "
            "marker (arrow-chain → shipped, a `## Shipped` section, or a "
            "RULED/preserved-as-written banner) — reconcile the body citing the "
            "shipping PR (the PR #311 pattern)",
        ),
    ]


def _git(root: Path, *args: str) -> tuple[int, str]:
    """Run git in ``root``; ``(127, "")`` when git can't run at all."""
    try:
        proc = subprocess.run(
            ["git", "-C", str(root), *args],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return 127, ""
    return proc.returncode, proc.stdout


def load_git_reality(root: Path) -> tuple[GitReality | None, str]:
    """Return ``(reality, "")`` or ``(None, why-skipped)``.

    Every None path is a *skip with a note*, never a finding — an absent or
    truncated history proves nothing about a ship claim (graceful-degradation
    rule in the module docstring, item 6).
    """
    rc, out = _git(root, "rev-parse", "--is-inside-work-tree")
    if rc != 0 or out.strip() != "true":
        return None, "not a git work tree (or git unavailable)"
    rc, out = _git(root, "rev-parse", "--is-shallow-repository")
    if rc != 0:
        return None, "git rev-parse failed"
    if out.strip() == "true":
        return None, "shallow clone — history truncated, ship claims unverifiable"
    ref = None
    for candidate in ("origin/main", "main", "HEAD"):
        rc, _ = _git(root, "rev-parse", "--verify", "--quiet", candidate + "^{commit}")
        if rc == 0:
            ref = candidate
            break
    if ref is None:
        return None, "no origin/main, main, or HEAD commit to verify against"
    repo_token = None
    rc, out = _git(root, "remote", "get-url", "origin")
    if rc == 0:
        match = _REMOTE_REPO_RE.search(out.strip())
        if match:
            repo_token = f"{match.group(1)}/{match.group(2)}".lower()
    rc, out = _git(root, "log", ref, "--format=%H%x09%cs%x09%s")
    if rc != 0:
        return None, f"git log {ref} failed"
    commits: list[tuple[str, _dt.date, str]] = []
    for line in out.splitlines():
        parts = line.split("\t", 2)
        if len(parts) != 3:
            continue
        sha, date_str, subject = parts
        try:
            commit_date = _dt.date.fromisoformat(date_str)
        except ValueError:
            continue
        commits.append((sha, commit_date, subject))
    return GitReality(root, ref, repo_token, tuple(commits)), ""


def _find_pr_commit(
    reality: GitReality, pr_number: str
) -> tuple[str, _dt.date, str] | None:
    """The commit on main that merged PR ``pr_number``, or None.

    Strictest marker first so date derivation lands on the true merge
    commit: squash tail ``(#N)`` at end of subject → ``Merge pull request
    #N`` head → ``(#N)`` anywhere in the subject (the multi-PR-subject
    style, e.g. the kit's #106). ``git log`` is newest-first, so the LAST
    hit is the oldest — the first time the marker landed.
    """
    patterns = (
        re.compile(rf"\(#{pr_number}\)\s*$"),
        re.compile(rf"^Merge pull request #{pr_number}(\D|$)"),
        re.compile(rf"\(#{pr_number}\)"),
    )
    for pattern in patterns:
        hits = [entry for entry in reality.commits if pattern.search(entry[2])]
        if hits:
            return hits[-1]
    return None


def check_merged_reality(
    root: Path,
    today: _dt.date | None = None,
    reality: GitReality | None = None,
) -> tuple[list[Finding], list[Finding], str]:
    """Enforcement item 6 — verify ship claims against local git history.

    Returns ``(findings, advisories, note)``: ``findings`` are enforcing
    (only ``bad-merged-sha`` — malformed syntax, checked even without git);
    ``advisories`` are the reachability/date legs (never exit-affecting);
    ``note`` is the non-empty skip reason when history was unavailable.
    Pass ``reality`` explicitly to skip loading (tests) — when omitted it
    is loaded from ``root``.
    """
    today = today or _dt.date.today()
    findings: list[Finding] = []
    advisories: list[Finding] = []
    note = ""
    if reality is None:
        reality, note = load_git_reality(root)

    ideas_dir = root / IDEAS_RELDIR
    if not ideas_dir.is_dir():
        return findings, advisories, note
    for path in sorted(ideas_dir.glob("*.md")):
        if path.name == README_NAME:
            continue
        rel = path.relative_to(root).as_posix()
        fields, error = parse_frontmatter(path.read_text(encoding="utf-8"))
        if fields is None:
            continue  # shape leg already reports unparseable frontmatter

        # Malformed merged_sha is enforcing and needs no git at all.
        sha_raw = fields.get("merged_sha", "null")
        if not _is_null(sha_raw) and not _SHA_RE.match(sha_raw):
            findings.append(
                Finding(
                    rel,
                    "bad-merged-sha",
                    f"merged_sha {sha_raw!r} must be null or 7-40 hex chars "
                    "(a malformed SHA is a typo, not a timing issue)",
                ),
            )
            sha_raw = "null"  # garbage gets no reachability run

        outcome = fields.get("outcome", "")
        pr_raw = fields.get("shipped_pr", "null")
        fm_shipped = outcome in SHIPPED_OUTCOMES or not _is_null(pr_raw)
        if not fm_shipped or reality is None:
            continue

        # Only claims about THIS repo are verifiable against its history.
        repo_raw = fields.get("shipped_repo", "null")
        if (
            _is_null(repo_raw)
            or reality.repo_token is None
            or repo_raw.lower() != reality.repo_token
        ):
            continue

        # Grace reference: merged_date, else the filename cohort date.
        merged_date: _dt.date | None = None
        date_raw = fields.get("merged_date", "null")
        if not _is_null(date_raw) and _DATE_RE.match(date_raw):
            try:
                merged_date = _dt.date.fromisoformat(date_raw)
            except ValueError:
                merged_date = None
        grace_ref = merged_date
        if grace_ref is None:
            cohort = _COHORT_FILENAME_RE.search(path.name)
            if cohort:
                try:
                    grace_ref = _dt.date.fromisoformat(cohort.group(0)[1:-3])
                except ValueError:
                    grace_ref = None
        # No parseable date at all → treat as within grace (the shape leg
        # already flags the missing/invalid date; never double-red).
        in_grace = grace_ref is None or (today - grace_ref).days <= GRACE_WINDOW_DAYS

        if not _is_null(sha_raw):
            rc, _ = _git(reality.root, "merge-base", "--is-ancestor", sha_raw, reality.ref)
            if rc in (1, 128) and not in_grace:
                advisories.append(
                    Finding(
                        rel,
                        "sha-not-on-main",
                        f"merged_sha {sha_raw} is not reachable from {reality.ref} "
                        f"and the claim is past the {GRACE_WINDOW_DAYS}d grace window "
                        "— verify the ship claim against git truth",
                    ),
                )

        if not _is_null(pr_raw) and pr_raw.isdigit():
            hit = _find_pr_commit(reality, pr_raw)
            if hit is None:
                if not in_grace:
                    advisories.append(
                        Finding(
                            rel,
                            "pr-not-on-main",
                            f"shipped_pr {pr_raw} has no merge marker on {reality.ref} "
                            f"(`(#{pr_raw})` / `Merge pull request #{pr_raw}`) and the "
                            f"claim is past the {GRACE_WINDOW_DAYS}d grace window",
                        ),
                    )
            elif merged_date is not None:
                sha, real_date, subject = hit
                drift = abs((real_date - merged_date).days)
                if drift > DATE_DRIFT_TOLERANCE_DAYS:
                    advisories.append(
                        Finding(
                            rel,
                            "merged-date-drift",
                            f"merged_date {date_raw} vs the real merge date {real_date} "
                            f"({sha[:9]} {subject!r}) — {drift}d apart; the in-PR flip "
                            f"writes an anticipated date, reconcile it to {real_date}",
                        ),
                    )
    return findings, advisories, note


def check_ideas(root: Path, today: _dt.date | None = None) -> list[Finding]:
    today = today or _dt.date.today()
    findings: list[Finding] = []
    ideas_dir = root / IDEAS_RELDIR
    readme = ideas_dir / README_NAME
    if not ideas_dir.is_dir():
        return [Finding(IDEAS_RELDIR, "missing-dir", "docs/ideas/ does not exist")]
    if not readme.is_file():
        findings.append(
            Finding(f"{IDEAS_RELDIR}/{README_NAME}", "missing-readme", "the backlog index is missing"),
        )
        readme_text = ""
    else:
        readme_text = readme.read_text(encoding="utf-8")

    idea_files = sorted(
        p for p in ideas_dir.glob("*.md") if p.name != README_NAME
    )
    for path in idea_files:
        rel = path.relative_to(root).as_posix()
        if not _COHORT_FILENAME_RE.search(path.name):
            findings.append(
                Finding(rel, "bad-filename", "filename must end `-YYYY-MM-DD.md` (the B4 cohort key)"),
            )
        text = path.read_text(encoding="utf-8")
        fields, error = parse_frontmatter(text)
        if fields is None:
            findings.append(Finding(rel, "no-frontmatter", error or "unparseable frontmatter"))
        else:
            findings.extend(validate_fields(rel, fields, today))
            findings.extend(check_body_state_drift(rel, fields, text))
        if readme_text and path.name not in readme_text:
            findings.append(
                Finding(rel, "not-indexed", "idea file is not linked from docs/ideas/README.md"),
            )

    # Every relative .md link in the README must resolve.
    for match in _MD_LINK_RE.finditer(readme_text):
        target = match.group(1).strip()
        if not (ideas_dir / target).is_file():
            findings.append(
                Finding(
                    f"{IDEAS_RELDIR}/{README_NAME}",
                    "dangling-link",
                    f"backlog link `{target}` does not resolve to a file",
                ),
            )
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="repo root (default: this script's repo)",
    )
    parser.add_argument(
        "--no-reality",
        action="store_true",
        help="skip the merged-reality git leg entirely (hermetic runs)",
    )
    args = parser.parse_args(argv)
    root = args.root.resolve()
    findings = check_ideas(root)
    advisories: list[Finding] = []
    if args.no_reality:
        print("check_idea_index: merged-reality leg skipped (--no-reality)")
    else:
        reality_findings, advisories, note = check_merged_reality(root)
        findings.extend(reality_findings)
        if note:
            print(f"check_idea_index: merged-reality leg skipped ({note})")
    for f in advisories:
        print(f"{f.path}: [advisory] [{f.kind}] {f.message}")
    for f in findings:
        print(f"{f.path}: [{f.kind}] {f.message}")
    if findings:
        print(f"check_idea_index: {len(findings)} finding(s).")
        return 1
    if advisories:
        print(f"check_idea_index: OK ({len(advisories)} advisory note(s), not exit-affecting)")
    else:
        print("check_idea_index: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
