"""Inbox append-only gate — ``control/inbox.md`` may only grow, ORDER-shaped.

Why + provenance: the fleet coordination protocol (``control/README.md``)
makes ``control/inbox.md`` the manager's ORDER bus with **one writer** and an
**append-only** law — but that law was convention-only, enforced by nothing.
The fleet adoption review 2026-07-09 (issue #36, report 2) proved the gap
live: PR #34 (an ORDER 003 append) merged 19 s after it opened on the CI
control fast lane, with zero validation that the change was pure-append, that
existing ORDERs were untouched, or that the appended text was even a valid
ORDER block. Any session could silently rewrite or erase orders on a green
control-only PR.

This checker closes the LAW half (PL-007, "enforce, don't exhort"): a change
to ``control/inbox.md`` must be **PURE-APPEND** vs the merge-base — the base
file's bytes are a *prefix* of the new file (existing bytes unchanged,
additions only at/after the end) — and the appended text must follow the
ORDER-block grammar (``control/README.md`` → "inbox.md order format"). Writer
IDENTITY is deliberately NOT enforced: on a single-account program it is not
enforceable in-repo (issue #36 report 2, stated honestly in the protocol
doc); this gate enforces the part of the law that lives in the bytes.

Diff access without shelling out: engine code is pure stdlib — ``subprocess``
is banned (§3.2). So, exactly like the session-log gate, CI does the git work
in bash (extract the merge-base blob of ``control/inbox.md`` to a file) and
hands the path in via ``check --inbox-base <file>``; this checker only reads
two files and compares them. No base path (a local ``check`` with no diff
context, or the file/base absent) → **no-op**, the same fail-open posture as
the mtime session-log fallback. It engages only when there is a real diff to
judge, so ``check`` stays meaningful on a tree with no inbox change.
"""

from __future__ import annotations

from pathlib import Path

from engine.checks.check_docs import Finding
from engine.checks.check_status_current import INBOX_RELPATH  # "control/inbox.md"

# The ORDER grammar (header shape + required body fields) is kit-owned with
# ONE home — engine.grammar (EAP §6.8): writer templates and this enforcer
# consume the same constants, so they cannot drift apart. The shapes are
# documented there. (No import aliases: the dist builder drops intra-package
# imports whole, so the canonical names must be the ones used.)
from engine.grammar import (
    ORDER_HEADER_PREFIX,
    ORDER_HEADER_RE,
    ORDER_REQUIRED_FIELDS,
)


def _order_grammar_findings(appended: str) -> list[Finding]:
    """Return grammar findings for the ``appended`` region of the inbox.

    The region is either the freshly appended ORDER block(s) (normal append)
    or — when the change *created* the file — its whole body, which may open
    with the file header (a ``#`` title + a ``>`` blockquote intro). Content
    before the first ``## ORDER`` header is allowed only if it is that header
    (blank / ``#`` / ``>`` lines); anything else is stray. Each ORDER block is
    validated for a well-formed header and the four required fields.
    """
    lines = appended.splitlines()
    header_idxs = [i for i, ln in enumerate(lines) if ln.startswith(ORDER_HEADER_PREFIX)]
    findings: list[Finding] = []

    preamble_end = header_idxs[0] if header_idxs else len(lines)
    for ln in lines[:preamble_end]:
        stripped = ln.strip()
        if stripped and not stripped.startswith(("#", ">")):
            findings.append(
                Finding(
                    INBOX_RELPATH,
                    "inbox-order-grammar",
                    "appended content that is neither the file header nor a "
                    "`## ORDER` block — the inbox appends ORDER blocks only "
                    "(control/README.md order format).",
                ),
            )
            break

    bounds = header_idxs + [len(lines)]
    for b in range(len(header_idxs)):
        block = lines[bounds[b] : bounds[b + 1]]
        findings += _validate_block(block)
    return findings


def _validate_block(block: list[str]) -> list[Finding]:
    """Return findings for one ORDER block (header line through its body)."""
    header = block[0]
    if not ORDER_HEADER_RE.match(header):
        return [
            Finding(
                INBOX_RELPATH,
                "inbox-order-grammar",
                f"malformed ORDER header {header.strip()!r} — expected "
                "`## ORDER <nnn> · <ISO8601> · status: <state>` "
                "(control/README.md order format).",
            ),
        ]
    missing = [
        field
        for field in ORDER_REQUIRED_FIELDS
        if not any(ln.lstrip().startswith(field) for ln in block[1:])
    ]
    if missing:
        label = header.strip()
        return [
            Finding(
                INBOX_RELPATH,
                "inbox-order-grammar",
                f"{label!r} is missing required field(s): {', '.join(missing)} "
                "— every order carries priority/do/why/done-when "
                "(control/README.md order format).",
            ),
        ]
    return []


def check_inbox_append(target: Path, base_path: Path) -> list[Finding]:
    """Return the append-only findings for ``target``'s ``control/inbox.md``.

    ``base_path`` is the merge-base version of the file, extracted by CI (the
    engine never shells out to git). Empty list means the change is a legal
    pure-append of well-formed ORDER block(s) — or there is nothing to judge
    (inbox or base absent/unreadable → fail open, like every other checker).
    """
    inbox = target / INBOX_RELPATH
    base = Path(base_path)
    if not inbox.is_file() or not base.is_file():
        return []
    try:
        new_text = inbox.read_text(encoding="utf-8")
        old_text = base.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return []  # fail open — an unreadable file is not a verdict

    if not new_text.startswith(old_text):
        # The append-only law is violated the instant the old bytes are no
        # longer a prefix: an existing ORDER line was edited, reordered, or
        # deleted. Grammar of the "appended" tail is meaningless here.
        return [
            Finding(
                INBOX_RELPATH,
                "inbox-not-append",
                "control/inbox.md changed non-append vs the merge-base — the "
                "one-writer/append-only law (control/README.md) allows only "
                "additions at the end; an existing ORDER was edited, "
                "reordered, or deleted. Restore the prior bytes verbatim and "
                "append your new ORDER block instead.",
            ),
        ]
    appended = new_text[len(old_text) :]
    return _order_grammar_findings(appended)
