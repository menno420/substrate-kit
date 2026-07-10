"""The inbox append-only gate (issue #36, report 2).

``control/inbox.md`` is the manager's ORDER bus: one writer, append-only
(``control/README.md``). That law was convention-only — PR #34 (an ORDER
append) merged 19 s after open with nothing checking it was pure-append or
even a valid ORDER block. These tests pin the enforced law: a NON-append diff
(an edit or deletion to an existing order line) reds, a legitimate pure-append
of a well-formed ORDER block passes, and a malformed appended block reds on
grammar. Diff access mirrors the session-log gate — CI extracts the merge-base
blob to a file and hands the path in (the engine never shells out to git), so
the checker only reads two files and compares them.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest

pytest.importorskip("engine.checks.check_inbox_append")

from engine.checks.check_inbox_append import INBOX_RELPATH, check_inbox_append
from engine.cli import cmd_check

# A minimal but real inbox: header + intro + one well-formed ORDER block.
BASE_INBOX = (
    "# x · inbox\n"
    "> ORDERS to this Project. ONE writer: the manager. Never edit this file.\n"
    "\n"
    "## ORDER 001 · 2026-07-09T12:07Z · status: new\n"
    "priority: P1\n"
    "do: adopt the coordination protocol.\n"
    "why: the bus is live.\n"
    "done-when: status reports acked=001, done=001.\n"
)

# A legal second ORDER block, appended verbatim after the base.
ORDER_002 = (
    "\n"
    "## ORDER 002 · 2026-07-09T14:15Z · status: new\n"
    "priority: P2\n"
    "do: ship the visibility band.\n"
    "why: adopters need it.\n"
    "done-when: status reports done=002.\n"
)


def _write(root: Path, rel: str, text: str) -> Path:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _base_file(tmp_path: Path, text: str) -> Path:
    """Write a merge-base copy of the inbox to a side file (as CI's git show does)."""
    base = tmp_path / "inbox.base"
    base.write_text(text, encoding="utf-8")
    return base


# ---------------------------------------------------------------------------
# check_inbox_append — the pure-append law
# ---------------------------------------------------------------------------


def test_pure_append_of_new_order_passes(tmp_path):
    _write(tmp_path, INBOX_RELPATH, BASE_INBOX + ORDER_002)
    base = _base_file(tmp_path, BASE_INBOX)
    assert check_inbox_append(tmp_path, base) == []


def test_no_change_passes(tmp_path):
    _write(tmp_path, INBOX_RELPATH, BASE_INBOX)
    base = _base_file(tmp_path, BASE_INBOX)
    assert check_inbox_append(tmp_path, base) == []


def test_edit_to_existing_order_line_reds(tmp_path):
    # Flip ORDER 001's priority P1 -> P0 in place: the old bytes are no longer
    # a prefix of the new file — the append-only law is violated.
    edited = BASE_INBOX.replace("priority: P1", "priority: P0")
    _write(tmp_path, INBOX_RELPATH, edited)
    base = _base_file(tmp_path, BASE_INBOX)
    findings = check_inbox_append(tmp_path, base)
    assert [f.kind for f in findings] == ["inbox-not-append"]


def test_deletion_of_existing_order_reds(tmp_path):
    # Erase ORDER 001 entirely and keep only a header — not a prefix.
    _write(tmp_path, INBOX_RELPATH, "# x · inbox\n")
    base = _base_file(tmp_path, BASE_INBOX)
    findings = check_inbox_append(tmp_path, base)
    assert [f.kind for f in findings] == ["inbox-not-append"]


def test_reorder_within_existing_block_reds(tmp_path):
    # Swap two existing lines — same bytes, different order — still non-append.
    reordered = BASE_INBOX.replace(
        "priority: P1\ndo: adopt the coordination protocol.\n",
        "do: adopt the coordination protocol.\npriority: P1\n",
    )
    _write(tmp_path, INBOX_RELPATH, reordered)
    base = _base_file(tmp_path, BASE_INBOX)
    assert [f.kind for f in check_inbox_append(tmp_path, base)] == ["inbox-not-append"]


# ---------------------------------------------------------------------------
# check_inbox_append — the ORDER grammar of the appended text
# ---------------------------------------------------------------------------


def test_appended_block_missing_fields_reds_on_grammar(tmp_path):
    bad = "\n## ORDER 002 · 2026-07-09T14:15Z · status: new\npriority: P2\n"
    _write(tmp_path, INBOX_RELPATH, BASE_INBOX + bad)
    base = _base_file(tmp_path, BASE_INBOX)
    findings = check_inbox_append(tmp_path, base)
    assert [f.kind for f in findings] == ["inbox-order-grammar"]
    assert "do:" in findings[0].message


def test_appended_malformed_header_reds_on_grammar(tmp_path):
    bad = "\n## ORDER 002 no separators no status\npriority: P2\n"
    _write(tmp_path, INBOX_RELPATH, BASE_INBOX + bad)
    base = _base_file(tmp_path, BASE_INBOX)
    findings = check_inbox_append(tmp_path, base)
    assert [f.kind for f in findings] == ["inbox-order-grammar"]


def test_appended_non_order_prose_reds_on_grammar(tmp_path):
    bad = "\nrandom prose that is not an order block\n"
    _write(tmp_path, INBOX_RELPATH, BASE_INBOX + bad)
    base = _base_file(tmp_path, BASE_INBOX)
    assert [f.kind for f in check_inbox_append(tmp_path, base)] == ["inbox-order-grammar"]


def test_header_with_trailing_comment_is_allowed(tmp_path):
    # The README's own example header carries a trailing `# ...` manager note.
    ok = (
        "\n## ORDER 002 · 2026-07-09T14:15Z · status: new   # flips new->done\n"
        "priority: P2\ndo: x.\nwhy: y.\ndone-when: z.\n"
    )
    _write(tmp_path, INBOX_RELPATH, BASE_INBOX + ok)
    base = _base_file(tmp_path, BASE_INBOX)
    assert check_inbox_append(tmp_path, base) == []


def test_fresh_file_creation_with_header_and_order_passes(tmp_path):
    # The change CREATES the inbox (empty merge-base): the whole body is the
    # appended region and its file header (# / >) is legitimate preamble.
    _write(tmp_path, INBOX_RELPATH, BASE_INBOX)
    base = _base_file(tmp_path, "")
    assert check_inbox_append(tmp_path, base) == []


# ---------------------------------------------------------------------------
# fail-open / input-gating
# ---------------------------------------------------------------------------


def test_missing_inbox_is_noop(tmp_path):
    base = _base_file(tmp_path, BASE_INBOX)
    assert check_inbox_append(tmp_path, base) == []


def test_missing_base_is_noop(tmp_path):
    _write(tmp_path, INBOX_RELPATH, BASE_INBOX + ORDER_002)
    assert check_inbox_append(tmp_path, tmp_path / "does-not-exist") == []


# ---------------------------------------------------------------------------
# cmd_check integration — the gate reds strict on the control fast lane
# ---------------------------------------------------------------------------


def _fresh_status(tmp_path: Path) -> None:
    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    _write(
        tmp_path,
        "control/status.md",
        f"# x · status\nupdated: {now_iso}\nphase: t\nhealth: green\n"
        "last-shipped: none\nblockers: none\norders: acked= done=\n"
        "⚑ needs-owner: none\nnotes: none\n",
    )


def test_cmd_check_status_only_greens_on_pure_append(tmp_path):
    _fresh_status(tmp_path)
    _write(tmp_path, INBOX_RELPATH, BASE_INBOX + ORDER_002)
    base = _base_file(tmp_path, BASE_INBOX)
    assert cmd_check(tmp_path, strict=True, status_only=True, inbox_base=base) == 0


def test_cmd_check_status_only_reds_strict_on_non_append(tmp_path, capsys):
    _fresh_status(tmp_path)
    _write(tmp_path, INBOX_RELPATH, BASE_INBOX.replace("priority: P1", "priority: P0"))
    base = _base_file(tmp_path, BASE_INBOX)
    assert cmd_check(tmp_path, strict=True, status_only=True, inbox_base=base) == 1
    assert "inbox-not-append" in capsys.readouterr().out


def test_cmd_check_without_inbox_base_ignores_inbox(tmp_path):
    # No --inbox-base handed in (no diff context) → the inbox gate is a no-op,
    # even when the working-tree inbox would otherwise fail a grammar check.
    _fresh_status(tmp_path)
    _write(tmp_path, INBOX_RELPATH, "garbage not an order\n")
    assert cmd_check(tmp_path, strict=True, status_only=True) == 0
