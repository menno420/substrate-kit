"""check_skill_grounds — skill-body command-grounding advisory (slice 2, plan §7.2).

Why + provenance: the grounded-skills program's slice-2 accept criterion is
"each body names only commands that exist" — and the slice-1 session card's
💡 idea (`.sessions/2026-07-12-grounded-skills-slice1-index.md`) rules that
this ships as a CHECKER, not a review habit ("enforce, don't exhort"): a
grammar-level scan that extracts backticked command spans from skill bodies
plus the structured ``grounds`` lists and verifies each names something that
resolves — a whitelisted executable, a file in the target tree, or a path
the kit itself plants/ships. Added 2026-07-12 (grounded-skills slice 2,
§8 Q2=B advisory-first). Reliability (PL-008): UNVERIFIED — confirm its
findings against ground truth a few times across sessions before trusting
it; **delete this if it proves unreliable over multiple sessions.**

Posture is **advisory-only, never exit-affecting** (§8 Q2=B: no CI-red until
proven; graduation is a later, deliberate step) — the same nudge-never-door
contract as ``check_claims`` / ``check_capability_xref``. Detection is
deliberately coarse: backticked spans are prose as often as commands, so a
span is only *judged* when its first token is command- or path-shaped;
everything ambiguous fails open (no verdict). A false nudge costs one
glance; a skill that tells every future session to run a command that does
not exist costs every session an improvisation.

What it scans:

- The kit-truth :data:`engine.skills.skills.SKILLS` list — every body's
  backticked spans, markdown-link targets, and every ``grounds`` entry (the
  self-check that travels with the kit).
- The target's installed/staged skill documents (``.claude/skills/*/
  SKILL.md`` and ``<state_dir>/skills/*/SKILL.md``) when present — the
  RENDERED bodies, so a host-edited or host-added skill gets the same scan.

Skip rules (fail-open classes, in order): a span carrying an unfilled
``${slot}`` (rendered per-project — the raw body cannot know the value);
a span carrying non-ASCII characters (``·``/``→``/``✔`` mark report-format
prose, never commands);
a first token that is not identifier/path-shaped (prose, ``<placeholders>``,
``[brackets]``, flags, globs; a leading ``.`` is path-shaped — dot-led
pointers like ``.claude/skills/x/SKILL.md`` ARE judged); a token ending
``/`` (directory prose); a state-dir token naming a known kit-written
artifact class (:data:`_STATE_DIR_ARTIFACTS` / :data:`_STATE_DIR_PREFIXES`
— runtime artifacts grounded by construction; any OTHER state-dir path is
judged by existence like every pointer); a markdown-link target carrying a
URL scheme, a bare ``#anchor``, or whitespace; a single bare word with no
path shape (``complete``, ``in-progress`` — status tokens, not commands).
Pure stdlib; no ``subprocess`` (§3.2) — resolution is existence checks,
never execution.
"""

from __future__ import annotations

import re
from pathlib import Path

from engine.adopt import ADOPT_PLAN
from engine.checks.check_docs import Finding
from engine.skills.skills import SKILLS

# One backticked inline span (commands never span lines in skill bodies —
# a grounds-matching invariant the skills tests pin).
_SPAN_RE = re.compile(r"`([^`\n]+)`")

# A judgeable first token: identifier/path-shaped, optionally dot-led
# (``.substrate/upgrade-report.md``, ``.claude/skills/x/SKILL.md``, ``.env``).
# The optional leading ``.`` must be followed by an identifier character so
# pure-punctuation prose (``..``, ``...``, ``./``) stays unjudged. Anything
# else (``>``, ``[Unreleased]``, ``<repo>:``, ``<!--``, unicode prose) is
# skipped as prose.
_FIRST_TOKEN_RE = re.compile(r"^\.?[A-Za-z0-9_][A-Za-z0-9_.\-/]*$")

# One markdown link target: ``[text](target)``. Same extraction precedent as
# the kit-side template pointer guard (tests/test_template_pointer_guard.py
# ``_MD_LINK_TARGET_RE``); targets feed the SAME skip ladder as backtick spans.
_MD_LINK_TARGET_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")

# A real file extension (lowercase — ``vX.Y.Z`` version placeholders end in
# uppercase pseudo-extensions and must stay prose).
_EXT_RE = re.compile(r"\.[a-z0-9]{1,5}$")

# Executables a skill body may legitimately invoke without the target repo
# proving anything: VCS/CI/toolchain entry points, plus the MCP tool verbs
# the landing-path doctrine names (gh-mcp). Deliberately generous — this is
# an advisory scan of prose, and an unknown-but-real tool must fail open at
# the "bare word" rule rather than nag every adopter.
_EXECUTABLES = frozenset(
    {
        "git",
        "gh",
        "python",
        "python3",
        "python3.10",
        "python3.11",
        "python3.12",
        "pip",
        "pip3",
        "pytest",
        "ruff",
        "black",
        "isort",
        "mypy",
        "npm",
        "npx",
        "node",
        "yarn",
        "make",
        "cargo",
        "go",
        "sha256sum",
        "shasum",
        "curl",
        "wget",
        "bash",
        "sh",
        "ls",
        "grep",
        "rg",
        "bootstrap",  # the vendored entry point's shorthand spelling
        # gh-mcp / trigger-MCP verbs (tool calls, not shell commands)
        "create_pull_request",
        "update_pull_request",
        "list_pull_requests",
        "merge_pull_request",
        "enable_pr_auto_merge",
        "get_file_contents",
        "create_trigger",
        "delete_trigger",
        "list_triggers",
        "fire_trigger",
        "send_later",
    }
)

# Paths grounded by construction even when absent from the target tree,
# split into explicit classes so each entry states WHY it resolves and the
# kit-side guard (tests/test_skill_pointer_guard.py
# ``test_skill_grounds_kit_path_whitelist_cannot_rot``) can pin each class
# against rot. A raw "must exist in the adopter tree" pin is deliberately
# NOT used: a 4-adopter survey (2026-07-13, kit 1.15.0) measured it at 14–15
# FALSE findings per adopter — these paths never live in adopter trees by
# design. Classes must stay disjoint; the guard test asserts it.

# Kit-repo source/runbook files the ``release`` / ``upgrade-distribution``
# skills name ("the commands below run in the kit repo"). They resolve by
# class in ANY target; the guard test pins each to exist in the KIT tree so
# a kit-side rename cannot leave the whitelist resolving dead pointers.
_KIT_REPO_PATHS = frozenset(
    {
        "dist/bootstrap.py",
        "src/build_bootstrap.py",
        "src/build_release_json.py",
        "src/engine/lib/config.py",
        "pyproject.toml",
        "CHANGELOG.md",
        ".github/workflows/release.yml",
        "docs/adopters.md",
        "docs/operations/release-runbook.md",
    }
)

# Release-wave transients: files that exist only mid-wave or as published
# release assets (release.yml / the consumer flow in release.json) — never
# in any committed tree, kit or adopter. Resolve by class.
_WAVE_TRANSIENT_PATHS = frozenset(
    {
        "bootstrap.py.new",
        "bootstrap.py.sha256",
        "release.json",
    }
)

# Files the kit plants in ADOPTER trees outside ADOPT_PLAN (which joins
# _KNOWN_PATHS below on its own): the vendored single-file dist copied to
# the repo root by adopt (_vendor_bootstrap, skip-if-exists). Class-resolved
# because a not-yet-adopted / empty target legitimately lacks it while the
# shipped skill bodies already name it.
_ADOPTER_PLANTED_PATHS = frozenset({"bootstrap.py"})

# The full grounded-by-construction set — kept as the single derived union
# so resolution behavior is exactly the historical whitelist's.
_KIT_SHIPPED_PATHS = _KIT_REPO_PATHS | _WAVE_TRANSIENT_PATHS | _ADOPTER_PLANTED_PATHS

_KNOWN_PATHS = _KIT_SHIPPED_PATHS | {dest for _tmpl, dest in ADOPT_PLAN}

# State-dir artifacts the kit itself writes/stages, grounded by construction
# even when absent (they appear only after an upgrade / ``skills --build`` /
# a backup): the upgrade report (engine.upgrade.UPGRADE_REPORT_FILENAME),
# the pre-upgrade byte backup dir, and the staged-skills tree. Derived from
# what kit SKILLS bodies + staged skill docs actually reference under the
# state dir. Any OTHER state-dir path is judged by existence like every
# pointer — the pre-2026-07-13 blanket state-dir skip failed dead dot-led
# pointers open.
_STATE_DIR_ARTIFACTS = frozenset({"upgrade-report.md"})
_STATE_DIR_PREFIXES = ("backup/", "skills/")


def _unresolved(span: str, target: Path, state_dir: str) -> bool:
    """True when ``span``'s first token is command/path-shaped and resolves nowhere.

    Every ambiguous shape returns False (fail open — no verdict); see the
    module docstring's skip-rule ladder.
    """
    if "${" in span:
        return False  # slot-bearing — rendered per project, not judgeable raw
    if any(ord(ch) > 127 for ch in span):
        return False  # commands are ASCII; ·/→/✔ mark report-format prose
    tokens = span.split()
    if not tokens:
        return False
    first = tokens[0]
    if not _FIRST_TOKEN_RE.match(first):
        return False  # prose / placeholder / flag / bracket shapes
    if first.endswith("/"):
        return False  # directory prose
    if first.startswith(f"{state_dir}/"):
        rest = first[len(state_dir) + 1 :]
        if rest in _STATE_DIR_ARTIFACTS or rest.startswith(_STATE_DIR_PREFIXES):
            return False  # kit-written runtime artifacts — grounded by class
        # any other state-dir path falls through to the existence lanes
    if first in _EXECUTABLES or first in _KNOWN_PATHS:
        return False
    if (target / first).exists():
        return False
    path_shaped = "/" in first or _EXT_RE.search(first) is not None
    if path_shaped:
        return True  # names a concrete file that is nowhere
    # Bare word: with arguments it reads as a command whose executable is
    # unknown (the fake-command class); alone it is a prose token.
    return len(tokens) > 1


def _spans(body: str) -> list[str]:
    """Return the judgeable spans of ``body``, in order.

    Backticked inline spans first, then markdown-link targets fed through
    the same downstream skip ladder. Link targets carrying a URL scheme, a
    bare ``#anchor``, or whitespace (titles, prose parentheticals) are
    skipped here; fragments are stripped (``docs/x.md#section`` judges
    ``docs/x.md``).
    """
    spans = _SPAN_RE.findall(body)
    for raw in _MD_LINK_TARGET_RE.findall(body):
        candidate = raw.strip()
        if candidate.startswith(("http://", "https://", "mailto:", "#")):
            continue
        candidate = candidate.split("#", 1)[0].strip()
        if not candidate or any(ch.isspace() for ch in candidate):
            continue  # empty after fragment-strip, or title/prose-bearing
        spans.append(candidate)
    return spans


def _skill_doc_paths(target: Path, state_dir: str) -> list[Path]:
    """Return the target's installed + staged skill documents (may be empty)."""
    paths: list[Path] = []
    for root in (target / ".claude" / "skills", target / state_dir / "skills"):
        if root.is_dir():
            paths.extend(sorted(root.glob("*/SKILL.md")))
    return paths


def check_skill_grounds(
    target: Path,
    *,
    skills: list[dict] | None = None,
    state_dir: str = ".substrate",
) -> list[Finding]:
    """Return advisory ``skill-ground-unresolved`` findings for ``target``.

    Scans the kit-truth skill set (``skills`` defaults to :data:`SKILLS`) —
    bodies + ``grounds`` — and any rendered skill documents installed in the
    target. Advisory by contract: callers must NEVER count these findings
    toward an exit code (§8 Q2=B — see module docstring). Fail-open on
    unreadable files and on every ambiguous span shape.
    """
    skill_set = SKILLS if skills is None else skills
    findings: list[Finding] = []
    for skill in skill_set:
        rel = f"skills/{skill['name']}/SKILL.md"
        for span in _spans(skill.get("body", "")):
            if _unresolved(span, target, state_dir):
                findings.append(
                    Finding(
                        rel,
                        "skill-ground-unresolved",
                        f"body names `{span}` but its first token resolves to "
                        "no whitelisted executable, target file, or "
                        "kit-shipped path — a session following this skill "
                        "would improvise; fix the body (or the grounds "
                        "whitelist) this session.",
                    ),
                )
        for ground in skill.get("grounds", []):
            if _unresolved(ground, target, state_dir):
                findings.append(
                    Finding(
                        rel,
                        "skill-ground-unresolved",
                        f"grounds entry `{ground}` resolves to no whitelisted "
                        "executable, target file, or kit-shipped path — "
                        "grounds are the skill's exact-command truth; an "
                        "unresolvable ground is drift.",
                    ),
                )
    for doc in _skill_doc_paths(target, state_dir):
        try:
            text = doc.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue  # fail open — an unreadable file is not a verdict
        rel = str(doc.relative_to(target)) if doc.is_relative_to(target) else str(doc)
        for span in _spans(text):
            if _unresolved(span, target, state_dir):
                findings.append(
                    Finding(
                        rel,
                        "skill-ground-unresolved",
                        f"rendered skill names `{span}` but its first token "
                        "resolves to no whitelisted executable, target file, "
                        "or kit-shipped path — verify the command before a "
                        "session inherits it.",
                    ),
                )
    return findings
