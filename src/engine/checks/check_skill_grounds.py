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
  backticked spans and every ``grounds`` entry (the self-check that travels
  with the kit).
- The target's installed/staged skill documents (``.claude/skills/*/
  SKILL.md`` and ``<state_dir>/skills/*/SKILL.md``) when present — the
  RENDERED bodies, so a host-edited or host-added skill gets the same scan.

Skip rules (fail-open classes, in order): a span carrying an unfilled
``${slot}`` (rendered per-project — the raw body cannot know the value);
a span carrying non-ASCII characters (``·``/``→``/``✔`` mark report-format
prose, never commands);
a first token that is not identifier/path-shaped (prose, ``<placeholders>``,
``[brackets]``, flags, globs); a token ending ``/`` (directory prose); a
token under the state dir (runtime artifacts, not committed files); a single
bare word with no path shape (``complete``, ``in-progress`` — status tokens,
not commands). Pure stdlib; no ``subprocess`` (§3.2) — resolution is
existence checks, never execution.
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

# A judgeable first token: identifier/path-shaped. Anything else (``>``,
# ``[Unreleased]``, ``<repo>:``, ``<!--``, unicode prose) is skipped as prose.
_FIRST_TOKEN_RE = re.compile(r"^[A-Za-z0-9_][A-Za-z0-9_.\-/]*$")

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

# Paths that are grounded by construction even when absent from the target
# tree: the kit's own release/distribution artifacts (the ``release`` and
# ``upgrade-distribution`` runbooks name kit-repo files and transient wave
# files that no adopter tree carries) plus the vendored-dist names the
# consumer flow uses. ADOPT_PLAN destinations join this set below — a path
# the kit plants is grounded wherever the kit is adopted.
_KIT_SHIPPED_PATHS = frozenset(
    {
        "bootstrap.py",
        "bootstrap.py.new",
        "bootstrap.py.sha256",
        "release.json",
        "dist/bootstrap.py",
        "src/build_bootstrap.py",
        "src/build_release_json.py",
        "src/engine/lib/config.py",
        "pyproject.toml",
        "CHANGELOG.md",
        ".github/workflows/release.yml",
        "docs/adopters.md",
        "docs/operations/release-runbook.md",
        "docs/SKILLS.md",
    }
)

_KNOWN_PATHS = _KIT_SHIPPED_PATHS | {dest for _tmpl, dest in ADOPT_PLAN}


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
    if first.endswith("/") or first.startswith(f"{state_dir}/"):
        return False  # directory prose; runtime state artifacts
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
    """Return the backticked inline spans of ``body``, in order."""
    return _SPAN_RE.findall(body)


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
