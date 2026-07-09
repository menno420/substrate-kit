"""Tests for the reasons-required check allowlist (KL-3, plan §5.3 triage)."""

import json

from engine import cli
from engine.checks.allowlist import (
    EXCEPTIONS_FILENAME,
    apply_allowlist,
    load_allowlist,
    parse_allowlist,
)
from engine.checks.check_docs import Finding
from engine.lib.config import Config, save_config
from engine.loop.telemetry import GUARD_FIRES_FILENAME

VALID = """\
# triaged exceptions — reason is REQUIRED
- path: bad.md
  kind: badge
  reason: "generated import, migrates at KL-5"
  triaged: 2026-07-09
  by: session-kl3
"""


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------


def test_parse_valid_entry():
    entries, findings = parse_allowlist(VALID, "x.yml")
    assert findings == []
    (entry,) = entries
    assert entry["path"] == "bad.md"
    assert entry["kind"] == "badge"
    assert entry["reason"] == "generated import, migrates at KL-5"
    assert entry["verdict"] == "accepted_risk"  # the default


def test_parse_explicit_false_positive_verdict():
    text = "- path: a.md\n  kind: link\n  reason: checker bug\n  verdict: false_positive\n"
    entries, findings = parse_allowlist(text, "x.yml")
    assert findings == []
    assert entries[0]["verdict"] == "false_positive"


def test_reasonless_entry_is_refused_and_reported():
    text = "- path: a.md\n  kind: badge\n  by: someone\n"
    entries, findings = parse_allowlist(text, "x.yml")
    assert entries == []
    (finding,) = findings
    assert finding.kind == "allowlist"
    assert "no reason" in finding.message
    assert "refused" in finding.message


def test_blank_reason_is_refused():
    text = '- path: a.md\n  kind: badge\n  reason: ""\n'
    entries, findings = parse_allowlist(text, "x.yml")
    assert entries == []
    assert findings and "no reason" in findings[0].message


def test_unknown_verdict_is_refused():
    text = "- path: a.md\n  kind: badge\n  reason: why\n  verdict: fine\n"
    entries, findings = parse_allowlist(text, "x.yml")
    assert entries == []
    assert findings and "unknown verdict" in findings[0].message


def test_unknown_key_and_unparseable_line_are_findings():
    text = "- path: a.md\n  kind: badge\n  reason: why\n  wildcard: yes\nloose text\n"
    entries, findings = parse_allowlist(text, "x.yml")
    assert len(entries) == 1  # the entry itself still counts — reason present
    messages = " | ".join(f.message for f in findings)
    assert "unknown key 'wildcard'" in messages
    assert "unparseable" in messages


def test_reason_keeps_inline_hash():
    text = '- path: a.md\n  kind: badge\n  reason: "see PR #1770"\n'
    entries, _ = parse_allowlist(text, "x.yml")
    assert entries[0]["reason"] == "see PR #1770"


def test_load_allowlist_absent_is_empty(tmp_path):
    assert load_allowlist(tmp_path, ".substrate") == ([], [])


# ---------------------------------------------------------------------------
# Matching
# ---------------------------------------------------------------------------


def test_apply_allowlist_exact_path_and_kind_only():
    findings = [
        Finding("bad.md", "badge", "missing"),
        Finding("bad.md", "link", "dead"),
        Finding("other.md", "badge", "missing"),
    ]
    entries = [{"path": "bad.md", "kind": "badge", "reason": "why"}]
    kept, suppressed = apply_allowlist(findings, entries)
    assert [f.path for f in kept] == ["bad.md", "other.md"]
    assert [(f.kind) for f, _ in suppressed] == ["badge"]


# ---------------------------------------------------------------------------
# cmd_check integration
# ---------------------------------------------------------------------------


def _repo(tmp_path, allowlist: str | None):
    root = tmp_path / "repo"
    (root / ".substrate").mkdir(parents=True)
    save_config(root, Config())
    (root / "docs").mkdir()
    # A doc that is badge-clean and linked from a read-path root, so the ONLY
    # finding in play is the one we plant below.
    (root / "docs" / "AGENT_ORIENTATION.md").write_text(
        "> **Status:** `binding`\n\nsee [bad](bad.md) and "
        "[state](current-state.md)\n",
        encoding="utf-8",
    )
    (root / "docs" / "current-state.md").write_text(
        "> **Status:** `living-ledger`\n\nok\n",
        encoding="utf-8",
    )
    (root / "docs" / "bad.md").write_text("no badge\n", encoding="utf-8")
    if allowlist is not None:
        (root / ".substrate" / EXCEPTIONS_FILENAME).write_text(
            allowlist,
            encoding="utf-8",
        )
    return root


def _fires(root):
    path = root / ".substrate" / GUARD_FIRES_FILENAME
    if not path.exists():
        return []
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def test_cmd_check_suppresses_with_reason_and_records_verdict(tmp_path, capsys):
    root = _repo(tmp_path, VALID)
    rc = cli.cmd_check(root, strict=True)
    out = capsys.readouterr().out
    assert rc == 0
    assert "suppressed by allowlist" in out
    suppressed = [r for r in _fires(root) if r["verdict"] is not None]
    (record,) = suppressed
    assert record["verdict"] == "accepted_risk"
    assert record["reason"] == "generated import, migrates at KL-5"
    assert record["finding"]["kind"] == "badge"


def test_cmd_check_reasonless_entry_suppresses_nothing(tmp_path, capsys):
    root = _repo(tmp_path, "- path: bad.md\n  kind: badge\n")
    rc = cli.cmd_check(root, strict=True)
    out = capsys.readouterr().out
    assert rc == 1  # the badge finding survives AND the refusal is a finding
    assert "[badge]" in out
    assert "[allowlist]" in out
    assert "no reason" in out


def test_cmd_check_without_allowlist_unchanged(tmp_path, capsys):
    root = _repo(tmp_path, None)
    rc = cli.cmd_check(root, strict=True)
    out = capsys.readouterr().out
    assert rc == 1
    assert "suppressed" not in out
