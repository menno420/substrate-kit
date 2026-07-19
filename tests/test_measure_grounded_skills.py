"""Tests for scripts/measure_grounded_skills.py — fixture trees, no network.

The harness is the pre-registered grounded-skills measurement instrument
(docs/operations/grounded-skills-measurement.md); these tests pin the frozen
metric definitions so a silent behavior change is a red suite, not a silent
protocol amendment.
"""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from datetime import date
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPT = _REPO_ROOT / "scripts" / "measure_grounded_skills.py"

_spec = importlib.util.spec_from_file_location("measure_grounded_skills", _SCRIPT)
mgs = importlib.util.module_from_spec(_spec)
sys.modules.setdefault("measure_grounded_skills", mgs)
_spec.loader.exec_module(mgs)

WINDOW = dict(start=date(2026, 7, 1), boundary=date(2026, 7, 12), end=date(2026, 7, 20))


# ── roster ───────────────────────────────────────────────────────────────────


def test_parse_roster_drops_comments_and_lane_tokens():
    text = (
        "# comment\n"
        "\n"
        "menno420/substrate-kit\n"
        "menno420/superbot-games control/status-mining.md control/status-exploration.md\n"
    )
    assert mgs.parse_roster(text) == [
        "menno420/substrate-kit",
        "menno420/superbot-games",
    ]


# ── bucketing ────────────────────────────────────────────────────────────────


def test_card_date_parses_and_rejects():
    assert mgs.card_date("2026-07-13-some-slug.md") == date(2026, 7, 13)
    assert mgs.card_date("README.md") is None
    assert mgs.card_date("2026-13-99-bad.md") is None


def test_bucket_boundary_day_excluded_from_both():
    assert mgs.bucket(date(2026, 7, 11), **WINDOW) == "before"
    assert mgs.bucket(date(2026, 7, 12), **WINDOW) == "boundary-day"
    assert mgs.bucket(date(2026, 7, 13), **WINDOW) == "after"
    assert mgs.bucket(date(2026, 6, 30), **WINDOW) is None
    assert mgs.bucket(date(2026, 7, 21), **WINDOW) is None


# ── M1 ───────────────────────────────────────────────────────────────────────


def test_skill_names_come_from_engine_skills_list():
    names = mgs.skill_names()
    assert "session-close" in names
    assert "intake" in names


def test_card_references_skill_matches_all_three_surfaces():
    names = ("session-close", "intake")
    assert mgs.card_references_skill("ran /session-close at the end", names)
    assert mgs.card_references_skill("see .claude/skills/intake/SKILL.md", names)
    assert mgs.card_references_skill("checked docs/SKILLS.md first", names)
    assert not mgs.card_references_skill("improvised the close-out by hand", names)


# ── M2 ───────────────────────────────────────────────────────────────────────

_COMPLIANT_BLOCK = (
    "⚑ OWNER-ACTION\n"
    "WHAT: flip the setting\n"
    "WHERE: Settings → Example → toggle\n"
    "HOW: one checkbox\n"
    "RISK: ↩️ reversible\n"
    "WHY-IT-MATTERS: the lane stalls\n"
    "UNBLOCKS: the next slice\n"
    "VERIFIED-NEEDED: attempted, 403\n"
)

_NONCOMPLIANT_BLOCK = "⚑ OWNER-ACTION\nWHAT: do the thing\nWHERE: settings\n"


def test_owner_action_blocks_split_on_blank_lines_and_markers():
    text = _COMPLIANT_BLOCK + "\n" + _NONCOMPLIANT_BLOCK
    blocks = mgs.owner_action_blocks(text)
    assert len(blocks) == 2
    assert mgs.block_compliant(blocks[0]) is True
    assert mgs.block_compliant(blocks[1]) is False


def test_owner_action_blocks_detect_named_asks_and_reject_prose_mentions():
    # named heartbeat ask (no literal OWNER-ACTION token) — detected
    named = (
        "⚑ P10 required-check swap\n"
        "WHAT: swap the required CI check\n"
        "WHERE: repo Settings → Rules\n"
    )
    assert len(mgs.owner_action_blocks(named)) == 1
    # mid-line prose mention (the 29:0 noise class) — rejected
    prose = "after this PR merges, will mark ⚑ OWNER-ACTION 13 RESOLVED.\n"
    assert mgs.owner_action_blocks(prose) == []
    # ⚑ line-start but no WHAT: field (e.g. ⚑ Self-initiated flag) — rejected
    flag = "⚑ Self-initiated: picked from the backlog.\n"
    assert mgs.owner_action_blocks(flag) == []


def test_block_compliant_accepts_field_alternates():
    alt = _COMPLIANT_BLOCK.replace("WHY-IT-MATTERS:", "WHY:").replace(
        "VERIFIED-NEEDED:", "VERIFIED-WHEN:"
    )
    assert mgs.block_compliant(alt) is True


def test_block_compliant_requires_risk_token():
    no_risk = _COMPLIANT_BLOCK.replace("RISK: ↩️ reversible\n", "RISK: none\n")
    assert mgs.block_compliant(no_risk) is False


# ── M3 ───────────────────────────────────────────────────────────────────────


def test_capability_lines_venue_verdicts_and_fail_open():
    text = (
        "- 2026-07-14 · wall · routine-fired · finding · evidence · workaround\n"
        "- 2026-07-14 · capability · not-a-venue · finding · evidence · none\n"
        "- 2026-07-10 · wall · some old style finding · evidence · none\n"
        "not a log line\n"
    )
    lines = mgs.capability_lines(text)
    assert [line.venue_ok for line in lines] == [True, False, None]
    assert lines[2].day == date(2026, 7, 10)


# ── measure_repo over a fixture tree ─────────────────────────────────────────


@pytest.fixture()
def fixture_tree(tmp_path: Path) -> Path:
    root = tmp_path / "adopter"
    (root / ".sessions").mkdir(parents=True)
    (root / "docs").mkdir()
    (root / "control").mkdir()
    # before-window card: no skill reference, one non-compliant ask
    (root / ".sessions" / "2026-07-10-old-work.md").write_text(
        "# card\nimprovised procedure\n\n" + _NONCOMPLIANT_BLOCK, encoding="utf-8"
    )
    # boundary-day card: excluded from both buckets
    (root / ".sessions" / "2026-07-12-boundary.md").write_text(
        "ran /session-close", encoding="utf-8"
    )
    # after-window cards: one grounded + compliant, one improvised
    (root / ".sessions" / "2026-07-14-grounded.md").write_text(
        "opened docs/SKILLS.md then ran /session-close\n\n" + _COMPLIANT_BLOCK,
        encoding="utf-8",
    )
    (root / ".sessions" / "2026-07-15-improvised.md").write_text(
        "did it by hand", encoding="utf-8"
    )
    (root / ".sessions" / "README.md").write_text("index", encoding="utf-8")
    (root / "docs" / "CAPABILITIES.md").write_text(
        "# ledger\n\n## Append log\n"
        "- 2026-07-09 · wall · old style no venue finding · evidence · none\n"
        "- 2026-07-14 · wall · routine-fired · finding · evidence · none\n",
        encoding="utf-8",
    )
    (root / "control" / "status.md").write_text(
        "# heartbeat\n\n" + _COMPLIANT_BLOCK, encoding="utf-8"
    )
    return root


def test_measure_repo_buckets_and_counts(fixture_tree: Path):
    res = mgs.measure_repo(
        "fixture", fixture_tree, names=("session-close",), **WINDOW
    )
    assert res.ok
    assert res.cards["before"] == {
        "cards": 1,
        "skill_cards": 0,
        "oa_blocks": 1,
        "oa_compliant": 0,
    }
    assert res.cards["boundary-day"]["cards"] == 1
    assert res.cards["after"] == {
        "cards": 2,
        "skill_cards": 1,
        "oa_blocks": 1,
        "oa_compliant": 1,
    }
    assert res.capability["before"] == {"lines": 1, "venue_judged": 0, "venue_ok": 0}
    assert res.capability["after"] == {"lines": 1, "venue_judged": 1, "venue_ok": 1}
    assert res.status_oa_blocks == 1 and res.status_oa_compliant == 1
    # not a git repo → M4 is an honest null
    assert res.merged is None


def test_merged_counts_from_git_history(tmp_path: Path):
    repo = tmp_path / "gitrepo"
    repo.mkdir()

    def git(*args: str, day: str | None = None) -> None:
        env = None
        if day:
            import os

            env = dict(
                os.environ,
                GIT_AUTHOR_DATE=f"{day}T12:00:00 +0000",
                GIT_COMMITTER_DATE=f"{day}T12:00:00 +0000",
            )
        subprocess.run(
            ["git", "-C", str(repo), *args],
            check=True,
            capture_output=True,
            env=env,
        )

    git("init", "--quiet")
    git("config", "user.email", "t@example.com")
    git("config", "user.name", "t")
    (repo / "f.txt").write_text("1", encoding="utf-8")
    git("add", "f.txt")
    git("commit", "-q", "-m", "Ship thing (#1)", day="2026-07-10")
    (repo / "f.txt").write_text("2", encoding="utf-8")
    git("commit", "-q", "-am", "no suffix commit", day="2026-07-13")
    (repo / "f.txt").write_text("3", encoding="utf-8")
    git("commit", "-q", "-am", "Ship other (#2)", day="2026-07-14")

    counts = mgs.merged_counts(repo, **WINDOW)
    assert counts == {"before": 1, "boundary-day": 0, "after": 1, "shallow": False}


def test_render_marks_shallow_clone_m4_null(fixture_tree: Path):
    res = mgs.measure_repo("fixture", fixture_tree, names=(), **WINDOW)
    res.merged = {"before": 0, "boundary-day": 0, "after": 5, "shallow": True}
    report = mgs.render_report([res], **WINDOW)
    assert "null (shallow clone" in report


# ── shallow-clone --json refuse-to-publish (M4 would be zeroed) ────────────────


@pytest.fixture()
def git_fixture_tree(fixture_tree: Path) -> Path:
    """The fixture tree, made a real (full, non-shallow) git repo.

    Reuses ``fixture_tree`` so the measured metrics are non-trivial, then adds
    one committed PR-suffixed merge so M4 has real history to (correctly)
    count on the full-clone path.
    """
    def git(*args: str) -> None:
        subprocess.run(
            ["git", "-C", str(fixture_tree), *args],
            check=True,
            capture_output=True,
        )

    git("init", "--quiet")
    git("config", "user.email", "t@example.com")
    git("config", "user.name", "t")
    git("add", "-A")
    subprocess.run(
        ["git", "-C", str(fixture_tree), "commit", "-q", "-m", "Seed fixture (#1)"],
        check=True,
        capture_output=True,
    )
    return fixture_tree


def test_json_refuses_on_shallow_clone(git_fixture_tree: Path, tmp_path: Path, capsys, monkeypatch):
    # force the shallow verdict (mirror how the harness detects it, via the
    # already-present ``_is_shallow`` flag) instead of building a real shallow
    # clone — the refuse condition reads only that flag.
    monkeypatch.setattr(mgs, "_is_shallow", lambda repo_dir: True)
    js = tmp_path / "results.json"
    code = mgs.main(["--local", f"fixture={git_fixture_tree}", "--json", str(js)])
    # refuses: non-zero exit, no JSON written, loud REFUSE marker on stderr
    assert code == 2
    assert not js.exists()
    err = capsys.readouterr().err
    assert err.startswith("REFUSE: shallow clone detected")
    assert "fixture" in err
    assert "git fetch --unshallow" in err


def test_json_writes_on_full_clone(git_fixture_tree: Path, tmp_path: Path, monkeypatch):
    # a full (non-shallow) clone still writes JSON and returns 0
    monkeypatch.setattr(mgs, "_is_shallow", lambda repo_dir: False)
    js = tmp_path / "results.json"
    code = mgs.main(["--local", f"fixture={git_fixture_tree}", "--json", str(js)])
    assert code == 0
    assert js.exists()
    import json as _json

    payload = _json.loads(js.read_text(encoding="utf-8"))
    assert payload["repos"][0]["name"] == "fixture"
    assert payload["repos"][0]["merged"]["shallow"] is False


# ── --commit-results durable-artifact flag (R9) ───────────────────────────────


def test_commit_results_writes_durable_artifact(git_fixture_tree: Path, tmp_path: Path, monkeypatch):
    # --commit-results writes the machine-readable results to a durable PATH,
    # with the same shape --json emits (valid results JSON the chain re-reads).
    monkeypatch.setattr(mgs, "_is_shallow", lambda repo_dir: False)
    durable = tmp_path / "results.json"
    code = mgs.main(["--local", f"fixture={git_fixture_tree}", "--commit-results", str(durable)])
    assert code == 0
    assert durable.exists()
    import json as _json

    payload = _json.loads(durable.read_text(encoding="utf-8"))
    assert payload["repos"][0]["name"] == "fixture"
    assert payload["window"]["boundary"] == "2026-07-12"


def test_commit_results_creates_parent_dirs(git_fixture_tree: Path, tmp_path: Path, monkeypatch):
    # a durable location may not exist yet (e.g. docs/reports/data/): the flag
    # creates its parent dirs so the artifact lands rather than crashing.
    monkeypatch.setattr(mgs, "_is_shallow", lambda repo_dir: False)
    durable = tmp_path / "docs" / "reports" / "data" / "results.json"
    assert not durable.parent.exists()
    code = mgs.main(["--local", f"fixture={git_fixture_tree}", "--commit-results", str(durable)])
    assert code == 0
    assert durable.exists()


def test_commit_results_and_json_are_byte_identical(git_fixture_tree: Path, tmp_path: Path, monkeypatch):
    # passing both flags writes the exact same bytes to each target — one
    # payload build, so the durable artifact and the ephemeral --json agree.
    monkeypatch.setattr(mgs, "_is_shallow", lambda repo_dir: False)
    js = tmp_path / "ephemeral.json"
    durable = tmp_path / "durable.json"
    code = mgs.main(
        [
            "--local",
            f"fixture={git_fixture_tree}",
            "--json",
            str(js),
            "--commit-results",
            str(durable),
        ]
    )
    assert code == 0
    assert js.read_bytes() == durable.read_bytes()


def test_commit_results_refuses_on_shallow_clone(git_fixture_tree: Path, tmp_path: Path, capsys, monkeypatch):
    # the durable artifact honors the same shallow-clone refuse-to-publish guard
    # as --json — a committed-but-zeroed M4 artifact would be worse than an
    # ephemeral one, so nothing is written and the exit is non-zero.
    monkeypatch.setattr(mgs, "_is_shallow", lambda repo_dir: True)
    durable = tmp_path / "results.json"
    code = mgs.main(["--local", f"fixture={git_fixture_tree}", "--commit-results", str(durable)])
    assert code == 2
    assert not durable.exists()
    err = capsys.readouterr().err
    assert err.startswith("REFUSE: shallow clone detected")
    assert "--commit-results" in err


def test_commit_results_default_off(fixture_tree: Path, tmp_path: Path):
    # without the flag: no stray durable artifact is written (backward-compat).
    out = tmp_path / "report.md"
    stray = tmp_path / "results.json"
    code = mgs.main(["--local", f"fixture={fixture_tree}", "--out", str(out)])
    assert code == 0
    assert not stray.exists()


# ── rendering ────────────────────────────────────────────────────────────────


def test_render_report_carries_n_and_honest_nulls(fixture_tree: Path):
    res = mgs.measure_repo("fixture", fixture_tree, names=("session-close",), **WINDOW)
    skipped = mgs.RepoResult(name="menno420/private", ok=False, skip_reason="clone failed: 404")
    report = mgs.render_report([res, skipped], **WINDOW)
    assert "menno420/private — clone failed: 404" in report
    assert "1/2 (50%)" in report  # M1 after
    assert "null (n=0)" in report  # empty denominators print as nulls
    assert "null (no git history)" in report  # M4 non-git null
    assert "docs/operations/grounded-skills-measurement.md" in report


def test_results_json_shape(fixture_tree: Path):
    res = mgs.measure_repo("fixture", fixture_tree, names=(), **WINDOW)
    payload = mgs.results_json([res], **WINDOW)
    assert payload["window"]["boundary"] == "2026-07-12"
    assert payload["repos"][0]["name"] == "fixture"
    assert payload["repos"][0]["cards"]["after"]["cards"] == 2


# ── opt-in --api-latency mode (graduated from GSW-4) ──────────────────────────


def test_load_latency_module():
    mod = mgs._load_latency_module()
    # exposes the pure (network-free) logic the harness mode reuses
    assert hasattr(mod, "parse_roster")
    assert hasattr(mod, "build_payload")
    assert hasattr(mod, "summarize")


def test_api_latency_skips_without_token(monkeypatch, tmp_path: Path):
    # delete every token env var → the credential-less/offline SKIP guarantee
    for var in ("GITHUB_PAT", "GH_TOKEN", "GITHUB_TOKEN"):
        monkeypatch.delenv(var, raising=False)
    # guard: if the network path is ever reached without a token, this fails
    real = mgs._load_latency_module()

    def boom(*args, **kwargs):
        raise AssertionError("network attempted despite no token")

    monkeypatch.setattr(real, "make_session", boom)
    monkeypatch.setattr(mgs, "_load_latency_module", lambda: real)

    result = mgs.run_api_latency(["menno420/substrate-kit"], **WINDOW)
    assert result["status"] == "skipped"
    assert "no GitHub token" in result["reason"]

    # end-to-end through main(): SKIPPED line rendered, exit 0, no exception
    out = tmp_path / "report.md"
    code = mgs.main(["--local", f"self={tmp_path}", "--api-latency", "--out", str(out)])
    assert code == 0
    assert "API latency: SKIPPED" in out.read_text(encoding="utf-8")


def test_api_latency_default_off(fixture_tree: Path, tmp_path: Path):
    # without the flag: no api_latency JSON key, no latency section in the report
    out = tmp_path / "report.md"
    js = tmp_path / "results.json"
    code = mgs.main(
        ["--local", f"fixture={fixture_tree}", "--out", str(out), "--json", str(js)]
    )
    assert code == 0
    import json as _json

    payload = _json.loads(js.read_text(encoding="utf-8"))
    assert "api_latency" not in payload
    assert "API latency" not in out.read_text(encoding="utf-8")


def test_freeze_writes_sidecar_and_prints_block(
    git_fixture_tree: Path, tmp_path: Path, capsys, monkeypatch
):
    # --freeze emits a self-citing sidecar next to the JSON and a paste-ready
    # block on stderr, whose sha256 is the hash of the exact bytes written.
    import hashlib
    import json as _json

    monkeypatch.setattr(mgs, "_is_shallow", lambda repo_dir: False)
    js = tmp_path / "results.json"
    code = mgs.main(["--local", f"fixture={git_fixture_tree}", "--json", str(js), "--freeze"])
    assert code == 0
    sidecar = tmp_path / "results.json.freeze"
    assert sidecar.exists()
    record = _json.loads(sidecar.read_text(encoding="utf-8"))
    assert record["algo"] == "sha256"
    assert record["sha256"] == hashlib.sha256(js.read_bytes()).hexdigest()
    assert record["bytes"] == len(js.read_bytes())
    err = capsys.readouterr().err
    assert "frozen run" in err
    assert record["sha256"] in err
    assert "sha256sum" in err


def test_freeze_reproduce_command_is_exact(
    git_fixture_tree: Path, tmp_path: Path, monkeypatch
):
    # the reproduce field is the exact command (paste-ready): interpreter,
    # repo-relative script path, and every flag actually passed, incl. --freeze.
    import json as _json

    monkeypatch.setattr(mgs, "_is_shallow", lambda repo_dir: False)
    js = tmp_path / "out.json"
    argv = ["--local", f"fixture={git_fixture_tree}", "--json", str(js), "--freeze"]
    code = mgs.main(argv)
    assert code == 0
    record = _json.loads((tmp_path / "out.json.freeze").read_text(encoding="utf-8"))
    repro = record["reproduce"]
    assert repro.startswith("python3 scripts/measure_grounded_skills.py ")
    assert "--freeze" in repro
    assert "--json" in repro
    assert str(js) in repro


def test_freeze_requires_json_or_commit(fixture_tree: Path, tmp_path: Path):
    # --freeze without a JSON sink is a usage error (exit 2), not a silent no-op.
    with pytest.raises(SystemExit) as exc:
        mgs.main(
            ["--local", f"fixture={fixture_tree}", "--out", str(tmp_path / "r.md"), "--freeze"]
        )
    assert exc.value.code == 2


def test_freeze_default_off(git_fixture_tree: Path, tmp_path: Path, monkeypatch):
    # without --freeze: JSON is written but no .freeze sidecar appears.
    monkeypatch.setattr(mgs, "_is_shallow", lambda repo_dir: False)
    js = tmp_path / "results.json"
    code = mgs.main(["--local", f"fixture={git_fixture_tree}", "--json", str(js)])
    assert code == 0
    assert js.exists()
    assert not (tmp_path / "results.json.freeze").exists()


def test_freeze_refuses_on_shallow_clone(
    git_fixture_tree: Path, tmp_path: Path, capsys, monkeypatch
):
    # the shallow-clone refuse guard runs before freeze: no JSON, no sidecar.
    monkeypatch.setattr(mgs, "_is_shallow", lambda repo_dir: True)
    js = tmp_path / "results.json"
    code = mgs.main(["--local", f"fixture={git_fixture_tree}", "--json", str(js), "--freeze"])
    assert code == 2
    assert not js.exists()
    assert not (tmp_path / "results.json.freeze").exists()
    assert capsys.readouterr().err.startswith("REFUSE: shallow clone detected")


def test_freeze_commit_results_sidecar(
    git_fixture_tree: Path, tmp_path: Path, monkeypatch
):
    # --freeze with --commit-results writes a durable sidecar next to the
    # durable artifact, citing the same bytes.
    import hashlib
    import json as _json

    monkeypatch.setattr(mgs, "_is_shallow", lambda repo_dir: False)
    durable = tmp_path / "data" / "results.json"
    code = mgs.main(
        ["--local", f"fixture={git_fixture_tree}", "--commit-results", str(durable), "--freeze"]
    )
    assert code == 0
    sidecar = tmp_path / "data" / "results.json.freeze"
    assert sidecar.exists()
    record = _json.loads(sidecar.read_text(encoding="utf-8"))
    assert record["sha256"] == hashlib.sha256(durable.read_bytes()).hexdigest()


def test_freeze_both_sinks_share_digest(
    git_fixture_tree: Path, tmp_path: Path, monkeypatch
):
    # both sinks are byte-identical, so both sidecars cite the same sha256.
    import json as _json

    monkeypatch.setattr(mgs, "_is_shallow", lambda repo_dir: False)
    js = tmp_path / "ephemeral.json"
    durable = tmp_path / "durable.json"
    code = mgs.main(
        [
            "--local",
            f"fixture={git_fixture_tree}",
            "--json",
            str(js),
            "--commit-results",
            str(durable),
            "--freeze",
        ]
    )
    assert code == 0
    a = _json.loads((tmp_path / "ephemeral.json.freeze").read_text(encoding="utf-8"))
    b = _json.loads((tmp_path / "durable.json.freeze").read_text(encoding="utf-8"))
    assert a["sha256"] == b["sha256"]
    assert js.read_bytes() == durable.read_bytes()
