"""Tests for the orientation-budget gate (Lane B6, the K0 word cap)."""

from pathlib import Path

from engine.checks.check_orientation_budget import (
    check_orientation_budget,
    check_orientation_headroom,
    orientation_word_count,
)
from engine.lib.config import Config


def _write(p: Path, text: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def _config(**orientation) -> Config:
    base = {"budget_words": 7000, "boot_docs": []}
    base.update(orientation)
    return Config(orientation=base)


# ---------------------------------------------------------------------------
# orientation_word_count
# ---------------------------------------------------------------------------


def test_word_count_per_doc_and_total(tmp_path):
    a = tmp_path / "docs" / "a.md"
    b = tmp_path / "docs" / "b.md"
    _write(a, "one two three\n")
    _write(b, "four five\n")
    counts = orientation_word_count(tmp_path, [a, b])
    assert counts == {"docs/a.md": 3, "docs/b.md": 2, "_total": 5}


def test_word_count_missing_file_counts_zero(tmp_path):
    counts = orientation_word_count(tmp_path, [tmp_path / "gone.md"])
    assert counts == {"gone.md": 0, "_total": 0}


# ---------------------------------------------------------------------------
# check_orientation_budget — budget over/under
# ---------------------------------------------------------------------------


def test_under_budget_is_clean(tmp_path):
    _write(tmp_path / "docs" / "boot.md", "a few words only\n")
    config = _config(budget_words=100, boot_docs=["boot.md"])
    assert check_orientation_budget(tmp_path, config) == []


def test_over_budget_fires_naming_total_and_budget(tmp_path):
    _write(tmp_path / "docs" / "boot.md", "w " * 30)
    config = _config(budget_words=10, boot_docs=["boot.md"])
    findings = check_orientation_budget(tmp_path, config)
    assert len(findings) == 1
    f = findings[0]
    assert f.kind == "orientation-budget"
    assert "30 words" in f.message and "10-word" in f.message


def test_missing_boot_doc_reported(tmp_path):
    config = _config(budget_words=100, boot_docs=["ghost.md"])
    findings = check_orientation_budget(tmp_path, config)
    assert len(findings) == 1
    assert findings[0].kind == "orientation-missing"
    assert findings[0].path == "docs/ghost.md"


def test_empty_boot_docs_falls_back_to_readpath_docs(tmp_path):
    _write(tmp_path / "docs" / "AGENT_ORIENTATION.md", "short\n")
    _write(tmp_path / "docs" / "current-state.md", "short\n")
    config = Config(orientation={"budget_words": 100, "boot_docs": []})
    assert config.readpath_docs == ["AGENT_ORIENTATION.md", "current-state.md"]
    assert check_orientation_budget(tmp_path, config) == []


def test_entry_with_slash_resolves_from_project_root(tmp_path):
    _write(tmp_path / ".session-journal.md", "root level doc\n")
    config = _config(budget_words=100, boot_docs=[".session-journal.md"])
    # Bare name -> docs_root -> missing; with a slash -> project root -> found.
    assert len(check_orientation_budget(tmp_path, config)) == 1
    config = _config(budget_words=100, boot_docs=["./.session-journal.md"])
    assert check_orientation_budget(tmp_path, config) == []


# ---------------------------------------------------------------------------
# Per-doc self-caps
# ---------------------------------------------------------------------------


def test_self_cap_over_fires(tmp_path):
    body = "<!-- substrate-budget: 5 words -->\n" + "word " * 20
    _write(tmp_path / "docs" / "capped.md", body)
    config = _config(budget_words=1000, boot_docs=["capped.md"])
    findings = check_orientation_budget(tmp_path, config)
    assert len(findings) == 1
    f = findings[0]
    assert f.kind == "orientation-doc-cap" and f.path == "docs/capped.md"
    assert "5-word self-cap" in f.message


def test_self_cap_under_is_clean(tmp_path):
    body = "<!-- substrate-budget: 50 words -->\njust a few words\n"
    _write(tmp_path / "docs" / "capped.md", body)
    config = _config(budget_words=1000, boot_docs=["capped.md"])
    assert check_orientation_budget(tmp_path, config) == []


def test_self_cap_only_read_from_first_12_lines(tmp_path):
    body = "\n" * 15 + "substrate-budget: 1 words\n" + "word " * 10
    _write(tmp_path / "docs" / "late.md", body)
    config = _config(budget_words=1000, boot_docs=["late.md"])
    assert check_orientation_budget(tmp_path, config) == []


# ---------------------------------------------------------------------------
# Headroom advisory — the K0 gauge (PR #308; advisory-only, never a gate)
# ---------------------------------------------------------------------------


def test_headroom_fires_in_band_with_split(tmp_path):
    _write(tmp_path / "docs" / "boot.md", "w " * 96)
    config = _config(budget_words=100, boot_docs=["boot.md"])
    findings = check_orientation_headroom(tmp_path, config)
    assert len(findings) == 1
    f = findings[0]
    assert f.kind == "orientation-headroom"
    assert "96/100" in f.message
    assert "4 words" in f.message
    assert "docs/boot.md 96" in f.message


def test_headroom_silent_below_threshold(tmp_path):
    _write(tmp_path / "docs" / "boot.md", "w " * 94)  # 94 < 95 = 100 * 0.95
    config = _config(budget_words=100, boot_docs=["boot.md"])
    assert check_orientation_headroom(tmp_path, config) == []


def test_headroom_silent_over_budget(tmp_path):
    # Over budget is the exit-affecting gate's verdict — the advisory
    # self-silences so one condition is never double-reported.
    _write(tmp_path / "docs" / "boot.md", "w " * 120)
    config = _config(budget_words=100, boot_docs=["boot.md"])
    assert check_orientation_headroom(tmp_path, config) == []
    gate = check_orientation_budget(tmp_path, config)
    assert [f.kind for f in gate] == ["orientation-budget"]


def test_headroom_fires_at_exact_budget(tmp_path):
    _write(tmp_path / "docs" / "boot.md", "w " * 100)
    config = _config(budget_words=100, boot_docs=["boot.md"])
    findings = check_orientation_headroom(tmp_path, config)
    assert len(findings) == 1
    assert "0 words" in findings[0].message


def test_headroom_ratio_configurable(tmp_path):
    _write(tmp_path / "docs" / "boot.md", "w " * 60)
    config = _config(
        budget_words=100, boot_docs=["boot.md"], headroom_warn_ratio=0.5
    )
    assert len(check_orientation_headroom(tmp_path, config)) == 1


def test_headroom_ratio_at_or_above_one_disables(tmp_path):
    _write(tmp_path / "docs" / "boot.md", "w " * 100)
    config = _config(
        budget_words=100, boot_docs=["boot.md"], headroom_warn_ratio=1
    )
    assert check_orientation_headroom(tmp_path, config) == []


def test_headroom_bad_ratio_falls_back_to_default(tmp_path):
    _write(tmp_path / "docs" / "boot.md", "w " * 96)
    config = _config(
        budget_words=100, boot_docs=["boot.md"], headroom_warn_ratio="bogus"
    )
    assert len(check_orientation_headroom(tmp_path, config)) == 1


def test_headroom_split_orders_largest_first(tmp_path):
    _write(tmp_path / "docs" / "small.md", "w " * 6)
    _write(tmp_path / "docs" / "big.md", "w " * 90)
    config = _config(budget_words=100, boot_docs=["small.md", "big.md"])
    findings = check_orientation_headroom(tmp_path, config)
    assert len(findings) == 1
    msg = findings[0].message
    assert msg.index("docs/big.md 90") < msg.index("docs/small.md 6")


def test_over_budget_gate_message_carries_split(tmp_path):
    _write(tmp_path / "docs" / "a.md", "w " * 20)
    _write(tmp_path / "docs" / "b.md", "w " * 10)
    config = _config(budget_words=10, boot_docs=["a.md", "b.md"])
    findings = check_orientation_budget(tmp_path, config)
    assert len(findings) == 1
    msg = findings[0].message
    assert "docs/a.md 20" in msg and "docs/b.md 10" in msg
    assert msg.index("docs/a.md 20") < msg.index("docs/b.md 10")


# ---------------------------------------------------------------------------
# cmd_check integration — the advisory NEVER touches the exit code
# ---------------------------------------------------------------------------


def test_cmd_check_strict_stays_green_on_headroom(tmp_path, capsys):
    # A root-level boot doc ("/" entry) keeps the ordinary docs-hygiene
    # checkers out of the picture; a minimal fresh heartbeat keeps the
    # control-protocol gate green. Only the headroom advisory should fire —
    # surfaced, warn-only, exit 0 under --strict.
    from datetime import datetime, timezone

    from engine.cli import cmd_check

    _write(tmp_path / "boot.md", "w " * 96)
    (tmp_path / "substrate.config.json").write_text(
        '{"orientation": {"budget_words": 100, "boot_docs": ["./boot.md"]}}',
        encoding="utf-8",
    )
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    _write(
        tmp_path / "control" / "status.md",
        f"# x · status\nupdated: {stamp}\nphase: testing\nhealth: green\n"
        "last-shipped: none\nblockers: none\norders: acked=001 done=001\n"
        "⚑ needs-owner: none\nnotes: none\n",
    )
    assert cmd_check(tmp_path, strict=True) == 0
    out = capsys.readouterr().out
    assert "orientation-headroom" in out
    assert "never exit-affecting" in out
