"""Tests for the §9.1 friction-report protocol's consumer half (KL-4):
envelope shape, outbox mechanics, repo detection, issue text, CLI verb."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

pytest.importorskip("engine.hooks.settings")

from engine.cli import main
from engine.lib.config import Config, save_config
from engine.lib.state import JsonStateBackend, default_state
from engine.loop.friction import (
    FRICTION_SCHEMA,
    build_envelope,
    detect_repo,
    friction_issue_body,
    friction_issue_title,
    friction_reports,
    list_outbox,
    load_envelope,
    write_outbox,
)
from engine.loop.reflections import REFLECTIONS_FILENAME, add_reflection


def _install(tmp_path: Path) -> tuple[Path, Config]:
    root = tmp_path / "repo"
    config = Config()
    config.kit_version = "1.0.0"
    root.mkdir()
    save_config(root, config)
    backend = JsonStateBackend(root / config.state_dir / "state.json")
    with backend.transaction():
        for key, value in default_state(config.project_id).items():
            backend.set(key, value)
    return root, config


def _git_config(root: Path, url: str) -> None:
    git = root / ".git"
    git.mkdir(exist_ok=True)
    (git / "config").write_text(
        f'[core]\n\tbare = false\n[remote "origin"]\n\turl = {url}\n'
        "\tfetch = +refs/heads/*:refs/remotes/origin/*\n",
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# Repo detection (pure .git/config parsing — the engine may not shell out)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "url",
    [
        "https://github.com/menno420/superbot.git",
        "git@github.com:menno420/superbot.git",
        "http://local_proxy@127.0.0.1:41729/git/menno420/superbot",
    ],
)
def test_detect_repo_across_url_forms(tmp_path, url):
    root = tmp_path / "r"
    root.mkdir()
    _git_config(root, url)
    assert detect_repo(root) == "menno420/superbot"


def test_detect_repo_fails_open(tmp_path):
    root = tmp_path / "r"
    root.mkdir()
    assert detect_repo(root) == ""  # no .git at all
    _git_config(root, "")
    assert detect_repo(root) == ""  # unparseable url


# ---------------------------------------------------------------------------
# Report collection: buffer ⚑ records + the direct session-log scan (D-14)
# ---------------------------------------------------------------------------


def test_friction_reports_merge_buffer_and_log_scan(tmp_path):
    root, config = _install(tmp_path)
    add_reflection(
        root / config.state_dir / REFLECTIONS_FILENAME,
        lesson="buffered friction",
        evidence="x.md:L1",
        tags=["flag"],
    )
    add_reflection(
        root / config.state_dir / REFLECTIONS_FILENAME,
        lesson="an idea, not friction",
        evidence="x.md:L2",
        tags=["idea"],
    )
    sessions = root / config.sessions_dir
    sessions.mkdir(parents=True)
    (sessions / "2026-07-01-old.md").write_text(
        "# log\n- ⚑ un-mined friction from an old log\n",
        encoding="utf-8",
    )
    reports = friction_reports(root, config)
    lessons = {r["lesson"] for r in reports}
    assert lessons == {"buffered friction", "un-mined friction from an old log"}


def test_friction_reports_dedupe_by_lesson(tmp_path):
    root, config = _install(tmp_path)
    add_reflection(
        root / config.state_dir / REFLECTIONS_FILENAME,
        lesson="same lesson",
        evidence="a.md:L1",
        tags=["flag"],
    )
    sessions = root / config.sessions_dir
    sessions.mkdir(parents=True)
    (sessions / "2026-07-01-a.md").write_text(
        "- ⚑ same lesson\n",
        encoding="utf-8",
    )
    assert len(friction_reports(root, config)) == 1


# ---------------------------------------------------------------------------
# Envelope + outbox + issue text
# ---------------------------------------------------------------------------


def test_envelope_matches_the_wire_schema():
    reports = [{"lesson": "x", "evidence": "y", "tags": ["flag"]}]
    envelope = build_envelope(
        repo="menno420/superbot",
        project_id="8155d8c4a73f",
        kit_version="1.0.0",
        reports=reports,
    )
    assert envelope == {
        "schema": FRICTION_SCHEMA,
        "repo": "menno420/superbot",
        "project_id": "8155d8c4a73f",
        "kit_version": "1.0.0",
        "reports": reports,
    }


def test_outbox_write_list_load_roundtrip(tmp_path):
    root, config = _install(tmp_path)
    envelope = build_envelope(
        repo="o/r",
        project_id="p",
        kit_version="1.0.0",
        reports=[{"lesson": "x"}],
    )
    first = write_outbox(root, config.state_dir, envelope)
    second = write_outbox(root, config.state_dir, envelope)
    assert first != second  # serials never clobber
    assert list_outbox(root, config.state_dir) == [first, second]
    assert load_envelope(first) == envelope


def test_load_envelope_fails_open(tmp_path):
    assert load_envelope(tmp_path / "absent.json") is None
    bad = tmp_path / "bad.json"
    bad.write_text("not json", encoding="utf-8")
    assert load_envelope(bad) is None


def test_issue_text_carries_summary_and_fenced_json():
    envelope = build_envelope(
        repo="menno420/superbot",
        project_id="8155d8c4a73f",
        kit_version="1.0.0",
        reports=[{"lesson": "MCP PR reads are stale", "evidence": "e", "tags": ["flag"]}],
    )
    title = friction_issue_title(envelope)
    assert title == "[friction] menno420/superbot: 1 report @ kit v1.0.0"
    body = friction_issue_body(envelope)
    assert "MCP PR reads are stale" in body
    assert "```json" in body
    fenced = body.split("```json\n", 1)[1].split("\n```", 1)[0]
    assert json.loads(fenced) == envelope


# ---------------------------------------------------------------------------
# The CLI verb
# ---------------------------------------------------------------------------


def test_cli_export_writes_outbox_and_prints_issue(tmp_path, capsys):
    root, config = _install(tmp_path)
    _git_config(root, "https://github.com/menno420/superbot.git")
    sessions = root / config.sessions_dir
    sessions.mkdir(parents=True)
    (sessions / "2026-07-09-x.md").write_text("- ⚑ real friction\n", encoding="utf-8")
    assert main(["friction", "export", "--target", str(root)]) == 0
    out = capsys.readouterr().out
    assert "friction: wrote" in out
    assert "[friction] menno420/superbot: 1 report @ kit v1.0.0" in out
    pending = list_outbox(root, config.state_dir)
    assert len(pending) == 1
    envelope = load_envelope(pending[0])
    assert envelope["project_id"] == config.project_id
    assert envelope["reports"][0]["lesson"] == "real friction"


def test_cli_export_with_nothing_to_report_writes_nothing(tmp_path, capsys):
    root, config = _install(tmp_path)
    assert main(["friction", "export", "--target", str(root)]) == 0
    assert "nothing to export" in capsys.readouterr().out
    assert list_outbox(root, config.state_dir) == []


def test_cli_export_requires_a_repo_name(tmp_path, capsys):
    root, config = _install(tmp_path)  # no .git/config to detect
    sessions = root / config.sessions_dir
    sessions.mkdir(parents=True)
    (sessions / "2026-07-09-x.md").write_text("- ⚑ friction\n", encoding="utf-8")
    assert main(["friction", "export", "--target", str(root)]) == 2
    assert "--repo" in capsys.readouterr().out
    assert (
        main(["friction", "export", "--repo", "o/r", "--target", str(root)]) == 0
    )


def test_cli_list_and_show(tmp_path, capsys):
    root, config = _install(tmp_path)
    sessions = root / config.sessions_dir
    sessions.mkdir(parents=True)
    (sessions / "2026-07-09-x.md").write_text("- ⚑ friction\n", encoding="utf-8")
    main(["friction", "export", "--repo", "o/r", "--target", str(root)])
    capsys.readouterr()
    assert main(["friction", "list", "--target", str(root)]) == 0
    out = capsys.readouterr().out
    assert "1 pending outbox envelope(s)" in out
    name = list_outbox(root, config.state_dir)[0].name
    assert main(["friction", "show", name, "--target", str(root)]) == 0
    out = capsys.readouterr().out
    assert "title: [friction] o/r:" in out
    assert "```json" in out


def test_cli_show_without_name_or_with_bad_name(tmp_path, capsys):
    root, _ = _install(tmp_path)
    assert main(["friction", "show", "--target", str(root)]) == 2
    assert main(["friction", "show", "nope.json", "--target", str(root)]) == 1


def test_session_close_advises_on_pending_outbox(tmp_path, capsys):
    root, config = _install(tmp_path)
    sessions = root / config.sessions_dir
    sessions.mkdir(parents=True)
    (sessions / "2026-07-09-x.md").write_text(
        "# log\n> **Status:** `complete`\n- ⚑ friction\n",
        encoding="utf-8",
    )
    main(["friction", "export", "--repo", "o/r", "--target", str(root)])
    capsys.readouterr()
    assert main(["session-close", "--target", str(root)]) == 0
    assert "friction report(s) pending" in capsys.readouterr().out


def test_check_advises_on_pending_outbox(tmp_path, capsys):
    # ORDER 020 item (d), fm plan A10: `check --strict` surfaces the
    # pending friction-outbox count as an advisory — previously the
    # list_outbox nudge lived only in cmd_session_close, so a session that
    # never ran the ritual sat on undrained envelopes through every check.
    root, config = _install(tmp_path)
    sessions = root / config.sessions_dir
    sessions.mkdir(parents=True)
    (sessions / "2026-07-14-x.md").write_text(
        "# log\n> **Status:** `complete`\n- ⚑ friction\n",
        encoding="utf-8",
    )
    baseline_exit = main(["check", "--strict", "--target", str(root)])
    baseline_out = capsys.readouterr().out
    assert "friction-outbox advisory" not in baseline_out
    main(["friction", "export", "--repo", "o/r", "--target", str(root)])
    capsys.readouterr()
    exit_code = main(["check", "--strict", "--target", str(root)])
    out = capsys.readouterr().out
    # Advisory-only by contract: the pending envelope changes the OUTPUT,
    # never the exit code — whatever the tree's exit was without it.
    assert exit_code == baseline_exit
    assert "friction-outbox advisory" in out
    assert "never exit-affecting" in out
    assert "[friction-outbox-pending]" in out
    assert "1 friction report(s) pending" in out


def test_check_status_only_skips_the_outbox_advisory(tmp_path, capsys):
    # The fast lane never pays the outbox scan: friction envelopes are not
    # control-lane traffic (same full-lane-only posture as every non-control
    # advisory in cmd_check).
    root, config = _install(tmp_path)
    sessions = root / config.sessions_dir
    sessions.mkdir(parents=True)
    (sessions / "2026-07-14-x.md").write_text(
        "# log\n> **Status:** `complete`\n- ⚑ friction\n",
        encoding="utf-8",
    )
    main(["friction", "export", "--repo", "o/r", "--target", str(root)])
    (root / "control").mkdir(exist_ok=True)
    (root / "control" / "status.md").write_text(
        "# seat\nupdated: 2026-07-14T05:00Z\n", encoding="utf-8"
    )
    capsys.readouterr()
    main(["check", "--strict", "--status-only", "--target", str(root)])
    assert "friction-outbox advisory" not in capsys.readouterr().out
