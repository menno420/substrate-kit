"""Tests for the KL-3 telemetry substrate (guard fires + model-usage harvest)."""

import io
import json
from pathlib import Path

from engine import cli
from engine.checks.check_docs import Finding
from engine.lib.config import Config, save_config
from engine.lib.state import JsonStateBackend, default_state
from engine.loop.telemetry import (
    GUARD_FIRES_FILENAME,
    MODEL_USAGE_RELPATH,
    TASK_CLASSES,
    harvest_model_usage,
    parse_model_line,
    reconcile_model_usage,
    record_guard_fires,
)

MODEL_LINE = "- **📊 Model:** fable-5 · high · test writing\n"


def _read_jsonl(path: Path) -> list[dict]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _fires(root: Path) -> list[dict]:
    return _read_jsonl(root / ".substrate" / GUARD_FIRES_FILENAME)


# ---------------------------------------------------------------------------
# Taxonomy
# ---------------------------------------------------------------------------


def test_task_classes_are_the_nine_pl004_classes_verbatim():
    # The 8 founding Q-0248 classes + `feature build` (PL-010 amendment).
    assert TASK_CLASSES == (
        "docs-only",
        "mechanical refactor",
        "test writing",
        "runtime bugfix",
        "kernel/architecture design",
        "review/verify",
        "research",
        "idea/planning",
        "feature build",
    )


# ---------------------------------------------------------------------------
# record_guard_fires
# ---------------------------------------------------------------------------


def test_record_guard_fires_writes_the_5_3_record_shape(tmp_path):
    (tmp_path / ".substrate").mkdir()
    n = record_guard_fires(
        tmp_path,
        ".substrate",
        cmd="check",
        surface="check",
        posture="blocking",
        findings=[Finding("docs/x.md", "badge", "missing badge")],
    )
    assert n == 1
    (record,) = _fires(tmp_path)
    assert record["guard"] == "badge"
    assert record["cmd"] == "check"
    assert record["surface"] == "check"
    assert record["posture"] == "blocking"
    assert record["finding"] == {
        "path": "docs/x.md",
        "kind": "badge",
        "message": "missing badge",
    }
    # Triage fields start null — a later, different party fills them.
    assert record["verdict"] is None
    assert record["reason"] is None
    assert record["judge"] is None
    assert record["outcome"] is None
    assert "ts" in record


def test_record_guard_fires_appends_never_rewrites(tmp_path):
    (tmp_path / ".substrate").mkdir()
    for i in range(3):
        record_guard_fires(
            tmp_path,
            ".substrate",
            cmd="check",
            surface="check",
            posture="advisory",
            findings=[Finding(f"doc-{i}.md", "link", "dead")],
        )
    assert [r["finding"]["path"] for r in _fires(tmp_path)] == [
        "doc-0.md",
        "doc-1.md",
        "doc-2.md",
    ]


def test_record_guard_fires_skips_unadopted_tree(tmp_path):
    # No state dir → `check` stays read-only on a pre-onboarding tree.
    n = record_guard_fires(
        tmp_path,
        ".substrate",
        cmd="check",
        surface="check",
        posture="blocking",
        findings=[Finding("x.md", "badge", "missing")],
    )
    assert n == 0
    assert not (tmp_path / ".substrate").exists()


def test_record_guard_fires_fails_open_on_unwritable_path(tmp_path):
    # Make the JSONL path a directory: the append must swallow, not raise.
    (tmp_path / ".substrate" / GUARD_FIRES_FILENAME).mkdir(parents=True)
    n = record_guard_fires(
        tmp_path,
        ".substrate",
        cmd="check",
        surface="check",
        posture="blocking",
        findings=[Finding("x.md", "badge", "missing")],
    )
    assert n == 0


def test_record_guard_fires_carries_allowlist_verdict(tmp_path):
    (tmp_path / ".substrate").mkdir()
    record_guard_fires(
        tmp_path,
        ".substrate",
        cmd="check",
        surface="check",
        posture="blocking",
        findings=[Finding("x.md", "badge", "missing")],
        verdict="accepted_risk",
        reason="legacy import, migrates at KL-5",
    )
    (record,) = _fires(tmp_path)
    assert record["verdict"] == "accepted_risk"
    assert record["reason"] == "legacy import, migrates at KL-5"


def _fire_once(tmp_path, finding, posture="blocking", **kwargs):
    return record_guard_fires(
        tmp_path,
        ".substrate",
        cmd="check",
        surface="check",
        posture=posture,
        findings=[finding],
        **kwargs,
    )


def test_record_guard_fires_dedupes_identical_fire_within_window(tmp_path):
    # trading-strategy #57's card: the gate lane re-runs `check` 2-3x per
    # push, filling the log with identical designed-hold echoes seconds
    # apart. An identical (guard, path, message) within the window skips.
    (tmp_path / ".substrate").mkdir()
    finding = Finding(".sessions/2026-07-11-x.md", "session-log", "in-progress")
    assert _fire_once(tmp_path, finding) == 1
    assert _fire_once(tmp_path, finding) == 0
    # Posture is NOT in the key — the blocking/advisory re-run pair of the
    # same finding is exactly the observed duplicate class.
    assert _fire_once(tmp_path, finding, posture="advisory") == 0
    assert len(_fires(tmp_path)) == 1


def test_record_guard_fires_distinct_findings_not_deduped(tmp_path):
    (tmp_path / ".substrate").mkdir()
    assert _fire_once(tmp_path, Finding("a.md", "badge", "missing")) == 1
    assert _fire_once(tmp_path, Finding("a.md", "badge", "stale")) == 1
    assert _fire_once(tmp_path, Finding("b.md", "badge", "missing")) == 1
    assert len(_fires(tmp_path)) == 3


def test_record_guard_fires_dedupe_expires_outside_window(tmp_path):
    # A record older than the window never suppresses a fresh fire — a
    # PERSISTING finding still re-records on later real activity.
    from datetime import datetime, timedelta, timezone

    from engine.loop.telemetry import GUARD_FIRES_DEDUPE_WINDOW_S

    (tmp_path / ".substrate").mkdir()
    old_ts = (
        datetime.now(timezone.utc)
        - timedelta(seconds=GUARD_FIRES_DEDUPE_WINDOW_S + 60)
    ).isoformat(timespec="seconds")
    stale = {
        "ts": old_ts,
        "guard": "badge",
        "cmd": "check",
        "surface": "check",
        "posture": "blocking",
        "finding": {"path": "x.md", "kind": "badge", "message": "missing"},
        "verdict": None,
        "reason": None,
        "judge": None,
        "outcome": None,
    }
    fires = tmp_path / ".substrate" / GUARD_FIRES_FILENAME
    fires.write_text(json.dumps(stale, sort_keys=True) + "\n", encoding="utf-8")
    assert _fire_once(tmp_path, Finding("x.md", "badge", "missing")) == 1
    assert len(_fires(tmp_path)) == 2


def test_record_guard_fires_verdict_records_never_deduped(tmp_path):
    # A verdict-carrying record (allowlist suppression) is a datum, not
    # noise: it always appends, and it never swallows a later plain fire.
    (tmp_path / ".substrate").mkdir()
    finding = Finding("x.md", "badge", "missing")
    assert _fire_once(tmp_path, finding, verdict="false_positive") == 1
    assert _fire_once(tmp_path, finding, verdict="false_positive") == 1
    # The plain fire after the verdict events still records once.
    assert _fire_once(tmp_path, finding) == 1
    assert _fire_once(tmp_path, finding) == 0
    assert len(_fires(tmp_path)) == 3


# ---------------------------------------------------------------------------
# parse_model_line
# ---------------------------------------------------------------------------


def test_parse_model_line_house_format():
    parsed = parse_model_line("junk\n- **📊 Model:** fable-5 · high · docs-only\n")
    assert parsed == {
        "model": "fable-5",
        "effort": "high",
        "task_class": "docs-only",
        "tokens_out": None,
    }


def test_parse_model_line_optional_tokens_segment():
    parsed = parse_model_line("📊 Model: sonnet · medium · research · 12,345\n")
    assert parsed is not None
    assert parsed["tokens_out"] == 12345
    # A non-numeric 4th segment stays honestly null (KF-9 — no fake meter).
    parsed = parse_model_line("📊 Model: sonnet · medium · research · unknown\n")
    assert parsed is not None
    assert parsed["tokens_out"] is None


def test_parse_model_line_last_occurrence_wins():
    text = "📊 Model: a · b · c\n📊 Model: sonnet · low · docs-only\n"
    parsed = parse_model_line(text)
    assert parsed is not None
    assert parsed["model"] == "sonnet"


def test_parse_model_line_absent_or_underfilled():
    assert parse_model_line("no needle here") is None
    assert parse_model_line("📊 Model: only-model · effort") is None


def test_parse_model_line_prose_mention_does_not_shadow_valid_line():
    # websites#31 regression: a later line that merely MENTIONS the marker in
    # prose (no `·` payload) must not shadow the real telemetry line above it
    # — last-needle selection returned None and the harvest advisory claimed
    # "no line" while the marker scan passed.
    text = (
        "# card\n"
        "- **📊 Model:** fable-5 · high · runtime bugfix\n"
        "Later prose that mentions the 📊 Model: marker convention in passing.\n"
    )
    parsed = parse_model_line(text)
    assert parsed is not None
    assert parsed["model"] == "fable-5"
    assert parsed["task_class"] == "runtime bugfix"
    # Last-VALID still wins between two genuine reports (the original intent).
    text += "📊 Model: sonnet · low · docs-only\n"
    parsed = parse_model_line(text)
    assert parsed is not None
    assert parsed["model"] == "sonnet"


# ---------------------------------------------------------------------------
# harvest_model_usage
# ---------------------------------------------------------------------------


def _write_log(root: Path, name: str, model_line: str = MODEL_LINE) -> Path:
    sessions = root / ".sessions"
    sessions.mkdir(exist_ok=True)
    log = sessions / name
    log.write_text(f"# card\n\n> **Status:** `complete`\n\n{model_line}", "utf-8")
    return log


def test_harvest_writes_the_pl004_record(tmp_path):
    log = _write_log(tmp_path, "2026-07-09-kl3.md")
    lines = harvest_model_usage(tmp_path, log)
    assert any("recorded" in line for line in lines)
    (record,) = _read_jsonl(tmp_path / MODEL_USAGE_RELPATH)
    assert record == {
        "session": "2026-07-09-kl3",
        "date": "2026-07-09",
        "model": "fable-5",
        "effort": "high",
        "task_class": "test writing",
        "tokens_out": None,
        "outcome": {
            "ci_green_first_push": None,
            "checker_findings": None,
            "merged_pr": None,
            "reverted_within_window": None,
        },
    }


def test_harvest_dedupes_by_session_slug(tmp_path):
    log = _write_log(tmp_path, "2026-07-09-kl3.md")
    harvest_model_usage(tmp_path, log)
    lines = harvest_model_usage(tmp_path, log)
    assert any("already recorded" in line for line in lines)
    assert len(_read_jsonl(tmp_path / MODEL_USAGE_RELPATH)) == 1


def test_harvest_advises_when_line_missing(tmp_path):
    log = _write_log(tmp_path, "2026-07-09-kl3.md", model_line="no line\n")
    lines = harvest_model_usage(tmp_path, log)
    assert any("no" in line and "Model:" in line for line in lines)
    assert not (tmp_path / MODEL_USAGE_RELPATH).exists()


def test_harvest_warns_on_off_taxonomy_class_but_records(tmp_path):
    log = _write_log(
        tmp_path,
        "2026-07-09-kl3.md",
        model_line="📊 Model: fable-5 · high · vibes\n",
    )
    lines = harvest_model_usage(tmp_path, log)
    assert any("not one of the 9" in line for line in lines)
    (record,) = _read_jsonl(tmp_path / MODEL_USAGE_RELPATH)
    assert record["task_class"] == "vibes"


def test_harvest_none_log_is_an_advisory(tmp_path):
    lines = harvest_model_usage(tmp_path, None)
    assert lines and "no session log" in lines[0]


# ---------------------------------------------------------------------------
# reconcile_model_usage (whole-tree write-at-commit sweep)
# ---------------------------------------------------------------------------


def _write_card(root: Path, name: str, *, status: str = "complete") -> Path:
    """Write a session card with a chosen Status badge + a valid 📊 line."""
    sessions = root / ".sessions"
    sessions.mkdir(exist_ok=True)
    card = sessions / name
    card.write_text(
        f"# card\n\n> **Status:** `{status}`\n\n{MODEL_LINE}", "utf-8"
    )
    return card


def test_reconcile_records_every_complete_card_not_just_latest(tmp_path):
    # The undercount fix: the lossy single-latest harvest missed any card
    # committed under a newer one. Reconcile sweeps them all.
    for i in range(3):
        _write_card(tmp_path, f"2026-07-0{i + 1}-card-{i}.md")
    lines = reconcile_model_usage(tmp_path, tmp_path / ".sessions")
    assert any("reconcile recorded 3" in line for line in lines)
    sessions = {r["session"] for r in _read_jsonl(tmp_path / MODEL_USAGE_RELPATH)}
    assert sessions == {"2026-07-01-card-0", "2026-07-02-card-1", "2026-07-03-card-2"}


def test_reconcile_count_equals_eligible_cards_no_undercount(tmp_path):
    # Done-when: stored count == eligible (complete + valid line) card count.
    for i in range(5):
        _write_card(tmp_path, f"2026-07-0{i + 1}-eligible-{i}.md")
    # A card with no 📊 line is NOT eligible and must not inflate the count.
    (tmp_path / ".sessions" / "2026-07-06-noline.md").write_text(
        "# card\n\n> **Status:** `complete`\n\nno telemetry line here\n", "utf-8"
    )
    reconcile_model_usage(tmp_path, tmp_path / ".sessions")
    assert len(_read_jsonl(tmp_path / MODEL_USAGE_RELPATH)) == 5


def test_reconcile_skips_in_progress_card_until_it_flips_complete(tmp_path):
    # Write-at-card-commit: a born-red / in-progress card has no finished
    # session to report — it earns its row only once it commits complete.
    card = _write_card(tmp_path, "2026-07-01-born-red.md", status="in-progress")
    reconcile_model_usage(tmp_path, tmp_path / ".sessions")
    assert not (tmp_path / MODEL_USAGE_RELPATH).exists()
    # Flip to complete → the very next reconcile picks it up.
    card.write_text(f"# card\n\n> **Status:** `complete`\n\n{MODEL_LINE}", "utf-8")
    reconcile_model_usage(tmp_path, tmp_path / ".sessions")
    (record,) = _read_jsonl(tmp_path / MODEL_USAGE_RELPATH)
    assert record["session"] == "2026-07-01-born-red"


def test_reconcile_skips_drafted_fill_slots(tmp_path):
    # A KL-5 auto-draft still carrying a bare [[fill:]] slot is drafted, not
    # completed — reconcile leaves it for a real close-out.
    (tmp_path / ".sessions").mkdir()
    (tmp_path / ".sessions" / "2026-07-01-drafted.md").write_text(
        "# card\n\n> **Status:** `complete`\n\n"
        "- **📊 Model:** [[fill: model]] · high · docs-only\n",
        "utf-8",
    )
    reconcile_model_usage(tmp_path, tmp_path / ".sessions")
    assert not (tmp_path / MODEL_USAGE_RELPATH).exists()


def test_reconcile_is_idempotent(tmp_path):
    _write_card(tmp_path, "2026-07-01-once.md")
    reconcile_model_usage(tmp_path, tmp_path / ".sessions")
    lines = reconcile_model_usage(tmp_path, tmp_path / ".sessions")
    assert any("no unrecorded complete cards" in line for line in lines)
    assert len(_read_jsonl(tmp_path / MODEL_USAGE_RELPATH)) == 1


def test_reconcile_preserves_rows_harvest_already_wrote(tmp_path):
    # Reconcile only APPENDS the missing — it never disturbs the latest-card
    # row harvest wrote, and dedupes against it.
    log = _write_card(tmp_path, "2026-07-02-latest.md")
    harvest_model_usage(tmp_path, log)
    _write_card(tmp_path, "2026-07-01-older.md")
    reconcile_model_usage(tmp_path, tmp_path / ".sessions")
    sessions = [r["session"] for r in _read_jsonl(tmp_path / MODEL_USAGE_RELPATH)]
    assert sorted(sessions) == ["2026-07-01-older", "2026-07-02-latest"]
    assert sessions.count("2026-07-02-latest") == 1  # no double-append


def test_reconcile_no_sessions_dir_is_a_noop(tmp_path):
    assert reconcile_model_usage(tmp_path, tmp_path / ".sessions") == []
    assert not (tmp_path / MODEL_USAGE_RELPATH).exists()


# ---------------------------------------------------------------------------
# The two choke points (cmd_check / cmd_hook)
# ---------------------------------------------------------------------------


def _repo_with_finding(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    (root / ".substrate").mkdir(parents=True)
    config = Config()
    save_config(root, config)
    (root / "docs").mkdir()
    (root / "docs" / "bad.md").write_text("no badge\n", encoding="utf-8")
    return root


def test_cmd_check_records_guard_fires(tmp_path, capsys):
    root = _repo_with_finding(tmp_path)
    rc = cli.cmd_check(root, strict=True)
    assert rc == 1
    capsys.readouterr()
    fires = _fires(root)
    kinds = {r["finding"]["kind"] for r in fires}
    assert "badge" in kinds
    assert all(r["surface"] == "check" for r in fires)
    assert all(r["posture"] == "blocking" for r in fires)


def test_cmd_check_unadopted_tree_writes_no_telemetry(tmp_path, capsys):
    root = tmp_path / "bare"
    (root / "docs").mkdir(parents=True)
    (root / "docs" / "bad.md").write_text("no badge\n", encoding="utf-8")
    cli.cmd_check(root, strict=True)
    capsys.readouterr()
    assert not (root / ".substrate").exists()


def test_cmd_check_gate_miss_records_session_log_fire(tmp_path, capsys):
    root = tmp_path / "repo"
    (root / ".substrate").mkdir(parents=True)
    save_config(root, Config())
    rc = cli.cmd_check(root, strict=True, require_session_log=True)
    assert rc == 1
    capsys.readouterr()
    (record,) = _fires(root)
    assert record["guard"] == "session-log"
    assert record["posture"] == "blocking"


def test_cmd_hook_dispatch_records_stance_fire(tmp_path, monkeypatch, capsys):
    config = Config()
    save_config(tmp_path, config)
    backend = JsonStateBackend(tmp_path / config.state_dir / "state.json")
    with backend.transaction():
        for key, value in default_state(config.project_id).items():
            backend.set(key, value)
        backend.set("stance", "review")
    monkeypatch.setattr("sys.stdin", io.StringIO('{"tool_name": "Edit"}'))
    assert cli.cmd_hook(tmp_path, "pretooluse") == 0
    capsys.readouterr()
    (record,) = _fires(tmp_path)
    assert record["guard"] == "stance"
    assert record["surface"] == "hook"
    assert record["posture"] == "advisory"
    assert record["cmd"] == "hook pretooluse"


def test_cmd_hook_in_stance_records_nothing(tmp_path, monkeypatch, capsys):
    config = Config()
    save_config(tmp_path, config)
    backend = JsonStateBackend(tmp_path / config.state_dir / "state.json")
    with backend.transaction():
        for key, value in default_state(config.project_id).items():
            backend.set(key, value)
        backend.set("stance", "debug")
    monkeypatch.setattr("sys.stdin", io.StringIO('{"tool_name": "Edit"}'))
    assert cli.cmd_hook(tmp_path, "pretooluse") == 0
    capsys.readouterr()
    assert not (tmp_path / ".substrate" / GUARD_FIRES_FILENAME).exists()


def test_cmd_session_close_harvests_model_line(tmp_path, capsys):
    # Full ritual: init-shaped state + a complete card carrying the 📊 line.
    config = Config()
    save_config(tmp_path, config)
    backend = JsonStateBackend(tmp_path / config.state_dir / "state.json")
    with backend.transaction():
        for key, value in default_state(config.project_id).items():
            backend.set(key, value)
    _write_log(tmp_path, "2026-07-09-close.md")
    rc = cli.cmd_session_close(tmp_path)
    assert rc == 0
    out = capsys.readouterr().out
    assert "model-usage: recorded 2026-07-09-close" in out
    (record,) = _read_jsonl(tmp_path / MODEL_USAGE_RELPATH)
    assert record["model"] == "fable-5"


def test_cmd_session_close_reconciles_every_card_not_just_latest(tmp_path, capsys):
    # The write-at-commit fix at the session-close choke point: an older card
    # that never got its own close-out is swept in alongside the latest.
    config = Config()
    save_config(tmp_path, config)
    backend = JsonStateBackend(tmp_path / config.state_dir / "state.json")
    with backend.transaction():
        for key, value in default_state(config.project_id).items():
            backend.set(key, value)
    _write_log(tmp_path, "2026-07-08-older.md")
    _write_log(tmp_path, "2026-07-09-latest.md")
    rc = cli.cmd_session_close(tmp_path)
    assert rc == 0
    out = capsys.readouterr().out
    assert "reconcile recorded" in out
    sessions = {r["session"] for r in _read_jsonl(tmp_path / MODEL_USAGE_RELPATH)}
    assert sessions == {"2026-07-08-older", "2026-07-09-latest"}
