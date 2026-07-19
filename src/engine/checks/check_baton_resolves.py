"""Next-2 baton path/anchor resolver advisory — warn-only, NEVER exit-affecting.

Provenance: docs/planning/2026-07-19-night-run-idea-groom-wave2.md S4 (this PR).
Sibling of the S3/R5/R7/R8/R11 advisories on the same posture="advisory" seam.

Why this exists: the coordination heartbeat (``control/status.md``, and per-lane
``control/status-*.md`` in multi-Project repos) ends with a ``## Next-2 baton``
section that hands the next wake its buildable work — and it does so by CITING
repo-relative paths (``docs/planning/...groom....md``, a recipe, a checker file)
that the next session is expected to open and act on. When a cited path is
renamed, moved, or deleted and the baton is not updated, the handoff points a
fresh wake at a file that no longer exists — a silent dead-pointer that costs the
successor a wasted orientation loop. This advisory verifies every path/anchor the
baton names still resolves on disk, so a dangling baton pointer surfaces instead
of stranding the next session.

What it does, per ``control/status*.md`` file: (a) locate the ``## Next-2 baton``
section (from the heading line to the next ``## `` heading or EOF); (b) extract
the inline-code spans inside it that LOOK LIKE a repo-relative path — a token
with no whitespace, at least one ``/`` separator, and a ``.<ext>`` file suffix,
optionally followed by a ``#anchor``; (c) for each, resolve the path part against
the target tree and, when an ``#anchor`` is present and the file is a readable
markdown file, resolve the anchor against the file's GitHub-slugified headings;
(d) return ONE advisory finding per unresolved reference, naming the token and
which status file cited it. Path-only tokens that resolve are silent; a resolved
path with an unresolvable anchor is flagged as an anchor miss (only when the file
was readable and carried headings — otherwise the anchor check fails open).

Deliberately conservative token filter (fail-open by construction): a code span
is treated as a path ONLY when it contains a ``/`` AND ends in ``.<ext>`` (before
any ``#``) AND has no whitespace. That excludes the baton's non-path code spans
by design — ``## Next-2 baton`` (no ``/`` before a ``.``, has whitespace),
``check --strict`` (whitespace), ``kit: v1.19.0`` (whitespace / no ``/``),
``trig_...`` (no ``/``), ``2 */2 * * *`` (whitespace) — so a version string or a
cron token is never mistaken for a missing file. Only an unambiguous
repo-relative path that fails to resolve fires.

Posture — ADVISORY only, wired on the posture="advisory" seam in cli.py exactly
like check_ungroomed_ideas / check_recipe_applies_when / check_fastlane_symmetry.
NOT in STRICT_SUBCHECKS — a stale baton pointer is a handoff nudge, not a defect
to fail an adopter on. Input-gated + fail-open: no control/ dir, no
status file, no baton section, or an unreadable file yields nothing. Never
raises. Stdlib only.
"""

from __future__ import annotations

import re
from pathlib import Path

from engine.checks.check_docs import Finding

_CONTROL_RELDIR = "control"
# Multi-Project repos carry per-lane heartbeats (control/status-mining.md,
# control/status-exploration.md) alongside control/status.md — glob them all so
# the advisory covers every lane's baton, not just the default single-lane file.
_STATUS_GLOB = "status*.md"

# The baton section heading. Matched at the start of a stripped line so a
# deeper-nested ``### `` heading elsewhere is not mistaken for it.
_RE_BATON_HEADING = re.compile(r"^##\s+Next-2\s+baton\s*$")
# Any ``## `` (H2) heading closes the section.
_RE_H2 = re.compile(r"^##\s+\S")
# Inline code spans: the shortest run of backtick-delimited text on a line.
_RE_CODE_SPAN = re.compile(r"`([^`]+)`")
# A markdown ATX heading line -> its text (for anchor resolution).
_RE_HEADING = re.compile(r"^#{1,6}\s+(.*\S)\s*$")

# Named BATON_UNRESOLVED_KIND (not a bare FINDING_KIND) — the dist concatenates
# every engine module into one namespace, so a second top-level FINDING_KIND
# would collide. The value is the finding kind.
BATON_UNRESOLVED_KIND = "baton-unresolved"


def _looks_like_path(token: str) -> bool:
    """True when ``token`` is an unambiguous repo-relative path (maybe #anchor).

    Conservative by design (fail-open): requires no whitespace, at least one
    ``/`` separator, and a ``.<ext>`` file suffix on the path part (before any
    ``#``). This excludes version strings (``v1.19.0`` — no ``/``), cron tokens
    (``2 */2 * * *`` — whitespace), CLI snippets (``check --strict`` — whitespace)
    and section headings (``## Next-2 baton`` — whitespace) so only a real path
    that fails to resolve can ever fire the advisory."""
    if not token or any(ch.isspace() for ch in token):
        return False
    path_part = token.split("#", 1)[0]
    if "/" not in path_part:
        return False
    # A ``.<ext>`` suffix on the final path segment (guards against a bare
    # ``docs/planning`` directory reference, which we do not grade).
    last_segment = path_part.rsplit("/", 1)[-1]
    return bool(re.search(r"\.\w+$", last_segment))


def _slug(heading_text: str) -> str:
    """GitHub-style heading anchor slug: lowercase, punctuation dropped, spaces→-.

    Intentionally lenient (fail-open on the anchor axis): emoji and other
    non-word characters are stripped, runs of whitespace collapse to a single
    hyphen. Not a byte-exact reproduction of GitHub's slugger (duplicate-suffix
    ``-1`` disambiguation is not modelled) — an advisory nudge, not a gate."""
    text = heading_text.strip().lower()
    text = re.sub(r"[^\w\s-]", "", text)  # drop punctuation / emoji
    text = re.sub(r"\s+", "-", text.strip())
    return text


def _baton_tokens(text: str) -> list[str]:
    """Path-like code-span tokens inside the ``## Next-2 baton`` section, in order."""
    lines = text.splitlines()
    in_section = False
    tokens: list[str] = []
    for line in lines:
        stripped = line.strip()
        if not in_section:
            if _RE_BATON_HEADING.match(stripped):
                in_section = True
            continue
        # In the section: an H2 heading (other than the baton one itself) closes it.
        if _RE_H2.match(stripped):
            break
        for span in _RE_CODE_SPAN.findall(line):
            candidate = span.strip()
            if _looks_like_path(candidate):
                tokens.append(candidate)
    return tokens


def _anchor_resolves(file_path: Path, anchor: str) -> bool | None:
    """Whether ``anchor`` names a heading in ``file_path``.

    Returns True/False when the file is a readable markdown file that carries at
    least one heading; returns None (fail open — skip the anchor check) when the
    file is unreadable or carries no headings, so an anchor is never flagged
    against a file we could not fairly slug."""
    try:
        body = file_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None
    slugs = {_slug(m.group(1)) for m in (_RE_HEADING.match(ln) for ln in body.splitlines()) if m}
    if not slugs:
        return None
    return _slug(anchor) in slugs


def check_baton_resolves(target: Path, config=None) -> list[Finding]:
    """Advisory: warn when a ``## Next-2 baton`` entry cites a path/anchor that
    no longer resolves on disk.

    Advisory only — the caller wires this on posture="advisory" and never counts
    it toward the exit code. Input-gated + fail-open. config accepted for
    signature parity with the other advisory checks; unused today."""
    control_dir = target / _CONTROL_RELDIR
    if not control_dir.is_dir():
        return []  # input-gated: no control plane here

    findings: list[Finding] = []
    for status_path in sorted(control_dir.glob(_STATUS_GLOB)):
        try:
            text = status_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue  # fail open — an unreadable heartbeat is not a verdict
        rel = f"{_CONTROL_RELDIR}/{status_path.name}"
        seen: set[str] = set()
        for token in _baton_tokens(text):
            if token in seen:
                continue  # one advisory per distinct dangling token per file
            seen.add(token)
            path_part, _, anchor = token.partition("#")
            referent = target / path_part
            if not referent.exists():
                findings.append(
                    Finding(
                        rel,
                        BATON_UNRESOLVED_KIND,
                        f"the `## Next-2 baton` cites `{token}`, but "
                        f"`{path_part}` does not resolve on disk — a stale baton "
                        "pointer strands the next wake; update the baton to a "
                        "path that exists (or remove the dead reference).",
                    ),
                )
                continue
            if anchor and referent.is_file():
                resolves = _anchor_resolves(referent, anchor)
                if resolves is False:
                    findings.append(
                        Finding(
                            rel,
                            BATON_UNRESOLVED_KIND,
                            f"the `## Next-2 baton` cites `{token}`: the file "
                            f"`{path_part}` resolves but no heading matches the "
                            f"`#{anchor}` anchor — update the anchor to a real "
                            "heading (or drop it).",
                        ),
                    )
    return findings
