"""Tests for the bench/ harness (band KL-5, plan §5.0): seeds, M1, recorder."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[1]
_BENCH = _REPO / "bench"
if str(_BENCH) not in sys.path:
    sys.path.insert(0, str(_BENCH))
if str(_BENCH / "seeds") not in sys.path:
    sys.path.insert(0, str(_BENCH / "seeds"))

import make_seed  # noqa: E402
import run_ab  # noqa: E402
import score_m1  # noqa: E402

# ---------------------------------------------------------------------------
# make_seed — fresh names, same shape, deterministic, seeded bug present
# ---------------------------------------------------------------------------


def test_make_seed_deterministic(tmp_path):
    a, b = tmp_path / "a", tmp_path / "b"
    make_seed.generate(a, seed=42)
    make_seed.generate(b, seed=42)
    files_a = sorted(p.relative_to(a) for p in a.rglob("*") if p.is_file())
    files_b = sorted(p.relative_to(b) for p in b.rglob("*") if p.is_file())
    assert files_a == files_b
    for rel in files_a:
        assert (a / rel).read_bytes() == (b / rel).read_bytes()


def test_make_seed_fresh_surface_names_per_seed(tmp_path):
    names_1 = make_seed._names(1)
    names_2 = make_seed._names(7)
    assert names_1["project"] != names_2["project"]  # anti-memorization


def test_make_seed_same_shape_every_seed(tmp_path):
    for seed in (1, 7):
        dest = tmp_path / f"s{seed}"
        make_seed.generate(dest, seed=seed)
        packages = [p for p in dest.iterdir() if p.is_dir() and p.name != "tests"]
        assert len(packages) == 1
        module_names = sorted(p.name for p in packages[0].glob("*.py"))
        assert module_names == ["__init__.py", "cli.py", "ops.py", "store.py"]
        assert list((dest / "tests").glob("test_*.py"))
        assert (dest / "README.md").exists()


def test_make_seed_tests_pass_and_bug_is_seeded(tmp_path):
    make_seed.generate(tmp_path, seed=3)
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-q"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    # The seeded bug: docstring/README promise case-insensitive filtering,
    # the implementation compares raw strings, and no test covers it.
    names = make_seed._names(3)
    ops_text = (tmp_path / names["project"] / "ops.py").read_text(encoding="utf-8")
    assert "case-insensitive" in ops_text  # the promise
    assert 'r["category"] == category' in ops_text  # the raw comparison
    assert "case-insensitive" in (tmp_path / "README.md").read_text(encoding="utf-8")
    tests_text = (tmp_path / "tests" / f"test_{names['project']}.py").read_text(encoding="utf-8")
    assert "lower" not in tests_text  # the gap is untested


# The 2026-07-09 run-2 keyword class (idea make-seed-yield-keyword-bug):
# seed 424242 drew the harvest domain whose measure token was `yield` — a
# Python keyword — and the generated project was a SyntaxError.


def test_make_seed_seed_424242_regression(tmp_path):
    # The exact live-bug seed must generate a project whose every module
    # compiles (it was a SyntaxError until the vocabulary fix).
    make_seed.generate(tmp_path, seed=424242)
    modules = list(tmp_path.rglob("*.py"))
    assert modules
    for module in modules:
        compile(module.read_text(encoding="utf-8"), str(module), "exec")


def test_make_seed_every_pool_token_is_identifier_safe():
    # The whole vocabulary is screened — keywords, soft keywords, builtins.
    for token in (*make_seed._ADJECTIVES, *make_seed._VERBS):
        assert make_seed._identifier_safe(token), token
    for domain in make_seed._DOMAINS:
        for token in domain:
            assert make_seed._identifier_safe(token), token


def test_make_seed_seed_sweep_all_identifiers_keyword_safe(tmp_path):
    # A seed sweep: every drawn surface token is identifier-safe, and the
    # generated modules compile (the 424242 class, generalized).
    for seed in range(0, 500, 7):
        names = make_seed._names(seed)  # raises ValueError on any unsafe draw
        for token in names.values():
            assert make_seed._identifier_safe(token), (seed, token)
    for seed in (0, 42, 424242, 424243, 499):
        dest = tmp_path / f"sweep-{seed}"
        make_seed.generate(dest, seed=seed)
        for module in dest.rglob("*.py"):
            compile(module.read_text(encoding="utf-8"), str(module), "exec")


def test_make_seed_names_screen_rejects_keyword_tokens(monkeypatch):
    # Defense in depth: a future pool edit that reintroduces a keyword dies
    # at generation time with the token named, never as a SyntaxError seed.
    monkeypatch.setattr(make_seed, "_DOMAINS", (("harvest", "harvests", "yield"),))
    with pytest.raises(ValueError, match="yield"):
        make_seed._names(424242)


# ---------------------------------------------------------------------------
# run_ab prepare — the seed-suite smoke leg (a broken seed dies at prepare)
# ---------------------------------------------------------------------------


def test_prepare_seed_suite_smoke_green_on_valid_seed(tmp_path):
    make_seed.generate(tmp_path, seed=3)
    line = run_ab._seed_suite_smoke(tmp_path, "on")
    assert line == "seed suite (on): green"


def test_prepare_seed_suite_smoke_aborts_on_red_seed(tmp_path):
    # A seed whose own suite is red (here: a SyntaxError module, the exact
    # run-2 shape) must abort the prepare with a named error.
    make_seed.generate(tmp_path, seed=3)
    names = make_seed._names(3)
    ops = tmp_path / names["project"] / "ops.py"
    ops.write_text(
        ops.read_text(encoding="utf-8") + "\ndef broken(records, yield):\n    pass\n",
        encoding="utf-8",
    )
    with pytest.raises(SystemExit, match="SEED SUITE RED"):
        run_ab._seed_suite_smoke(tmp_path, "off")


# ---------------------------------------------------------------------------
# score_m1 — words before the first mutating action
# ---------------------------------------------------------------------------


def _write_transcript(path, events):
    path.write_text("\n".join(json.dumps(e) for e in events) + "\n", encoding="utf-8")


def test_score_m1_counts_until_first_mutation(tmp_path):
    transcript = tmp_path / "t.jsonl"
    _write_transcript(
        transcript,
        [
            {"type": "tool_use", "name": "Read", "input": {"file_path": "x"}},
            {"type": "tool_result", "content": "one two three"},
            {"type": "text", "content": "assistant words never count"},
            {"type": "tool_use", "name": "Bash", "input": {"command": "ls -la"}},
            {"type": "tool_result", "content": "four five"},
            {"type": "tool_use", "name": "Write", "input": {"file_path": "y"}},
            {"type": "tool_result", "content": "after mutation not counted"},
        ],
    )
    record = score_m1.score_transcript(transcript)
    assert record["m1_words_before_first_mutation"] == 5
    assert record["first_mutation"]["tool"] == "Write"


def test_score_m1_bash_mutations_stop_the_count(tmp_path):
    for command, mutating in (
        ("git commit -m x", True),
        ("echo hi > file.txt", True),
        ("sed -i s/a/b/ f", True),
        ("rm -rf build", True),
        ("git log --oneline", False),
        ("grep -r pattern .", False),
        ("python3 -m pytest -q", False),
    ):
        transcript = tmp_path / "t.jsonl"
        _write_transcript(
            transcript,
            [
                {"type": "tool_result", "content": "a b c"},
                {"type": "tool_use", "name": "Bash", "input": {"command": command}},
                {"type": "tool_result", "content": "d e"},
            ],
        )
        record = score_m1.score_transcript(transcript)
        expected = 3 if mutating else 5
        assert record["m1_words_before_first_mutation"] == expected, command


# Run-1 artifact regressions (idea score-m1-mutation-artifacts-2026-07-09;
# evidence: bench/results/cold-start/2026-07-09-run01/ — ON-T2 line 15,
# OFF-T4 line 1, OFF-T5 lines 5-9).


def test_score_m1_readonly_fd_redirects_are_not_mutations_on_t2_off_t4(tmp_path):
    # ON-T2's line-15 artifact (`git log ... 2>/dev/null | head` counted as
    # the first mutation) and OFF-T4's identical artifact at line 1 (-> m1 0).
    for command in (
        "cd /repo && git status && git log --oneline -5 2>/dev/null | head",
        "cd /repo && ls -la && git log --oneline -15 2>/dev/null | head -20",
        "grep -r pattern . 2>&1",
        "python3 -m pytest -q >/dev/null 2>&1",
    ):
        transcript = tmp_path / "t.jsonl"
        _write_transcript(
            transcript,
            [
                {"type": "tool_use", "name": "Bash", "input": {"command": command}},
                {"type": "tool_result", "content": "one two three"},
                {"type": "tool_use", "name": "Edit", "input": {"file_path": "x"}},
            ],
        )
        record = score_m1.score_transcript(transcript)
        assert record["m1_words_before_first_mutation"] == 3, command
        assert record["first_mutation"]["tool"] == "Edit", command


def test_score_m1_genuine_file_redirects_still_mutate(tmp_path):
    for command in ("echo hi > out.txt", "make 2> err.log", "run >> build.log"):
        transcript = tmp_path / "t.jsonl"
        _write_transcript(
            transcript,
            [
                {"type": "tool_result", "content": "a b"},
                {"type": "tool_use", "name": "Bash", "input": {"command": command}},
                {"type": "tool_result", "content": "c d e"},
            ],
        )
        record = score_m1.score_transcript(transcript)
        assert record["m1_words_before_first_mutation"] == 2, command
        assert record["first_mutation"]["tool"] == "Bash", command


def test_score_m1_failed_mutation_result_does_not_stop_the_count_off_t5(tmp_path):
    # OFF-T5's artifact: the counted "first mutation" (Edit @ line 5) FAILED
    # with `tool_use_error: File has not been read yet`; the first successful
    # mutation is the Edit at line 9. The error text still counts as consumed
    # tool output.
    transcript = tmp_path / "t.jsonl"
    _write_transcript(
        transcript,
        [
            {"type": "tool_use", "name": "Grep", "input": {"pattern": "total"}},
            {"type": "tool_result", "content": "one two three four"},  # 4 words
            {"type": "tool_use", "name": "Edit", "input": {"file_path": "cli.py"}},
            {
                "type": "tool_result",
                "content": "<tool_use_error>File has not been read yet.</tool_use_error>",
            },  # 6 words, counted — the Edit never mutated
            {"type": "tool_use", "name": "Read", "input": {"file_path": "cli.py"}},
            {"type": "tool_result", "content": "five six"},  # 2 words
            {"type": "tool_use", "name": "Edit", "input": {"file_path": "cli.py"}},
            {"type": "tool_result", "content": "The file cli.py has been updated"},
        ],
    )
    record = score_m1.score_transcript(transcript)
    assert record["first_mutation"] is not None
    assert record["first_mutation"]["line"] == 7  # the SUCCESSFUL Edit
    assert record["m1_words_before_first_mutation"] == 4 + 6 + 2


def test_score_m1_error_flag_result_also_cancels_the_candidate(tmp_path):
    # The Anthropic message shape signals failure via is_error, not a marker.
    transcript = tmp_path / "t.jsonl"
    _write_transcript(
        transcript,
        [
            {"type": "tool_result", "content": "a b c"},
            {"type": "tool_use", "name": "Write", "input": {"file_path": "x"}},
            {"type": "tool_result", "content": "permission denied", "is_error": True},
        ],
    )
    record = score_m1.score_transcript(transcript)
    assert record["first_mutation"] is None  # the only mutation attempt failed
    assert record["m1_words_before_first_mutation"] == 5


def test_score_m1_unpaired_mutation_still_stops_conservatively(tmp_path):
    # No paired result before the next tool_use / end of stream -> the
    # mutating tool_use still stops the count (over-counting "mutating" is
    # the conservative direction, per the module docstring).
    transcript = tmp_path / "t.jsonl"
    _write_transcript(
        transcript,
        [
            {"type": "tool_result", "content": "a b"},
            {"type": "tool_use", "name": "Write", "input": {"file_path": "x"}},
            {"type": "tool_use", "name": "Read", "input": {"file_path": "y"}},
            {"type": "tool_result", "content": "c d e"},
        ],
    )
    record = score_m1.score_transcript(transcript)
    assert record["first_mutation"] is not None
    assert record["first_mutation"]["tool"] == "Write"
    assert record["m1_words_before_first_mutation"] == 2
    # ... and at end-of-stream too.
    _write_transcript(
        transcript,
        [
            {"type": "tool_result", "content": "a b"},
            {"type": "tool_use", "name": "Bash", "input": {"command": "rm -rf build"}},
        ],
    )
    record = score_m1.score_transcript(transcript)
    assert record["first_mutation"] is not None
    assert record["m1_words_before_first_mutation"] == 2


def test_score_m1_block_content_and_no_mutation(tmp_path):
    transcript = tmp_path / "t.jsonl"
    _write_transcript(
        transcript,
        [
            {"type": "tool_result", "content": [{"type": "text", "text": "one two"}]},
            {"type": "tool_result", "content": "three"},
        ],
    )
    record = score_m1.score_transcript(transcript)
    assert record["m1_words_before_first_mutation"] == 3
    assert record["first_mutation"] is None


# ---------------------------------------------------------------------------
# run_ab record — schema-checked, append-only, dedupe by run_id
# ---------------------------------------------------------------------------


def _row(run_id="2026-07-15-run01"):
    return {
        "date": "2026-07-15",
        "kit_version": "1.0.0",
        "run_id": run_id,
        "tasks": ["T2", "T4", "T5"],
        "m1_on": 1700,
        "m1_off": 549,
        "m2": "OFF",
        "m3": "tie",
        "verdict": "FAIL",
        "judge_model": "opus-x",
        "notes": "test row",
    }


@pytest.fixture()
def bench_results(tmp_path, monkeypatch):
    results = tmp_path / "results" / "cold-start"
    results.mkdir(parents=True)
    (results / "index.json").write_text("[]\n", encoding="utf-8")
    monkeypatch.setattr(run_ab, "BENCH_ROOT", tmp_path)
    return results / "index.json"


def test_record_appends_row(bench_results, capsys):
    rc = run_ab.main(["record", "--family", "cold-start", "--row", json.dumps(_row())])
    assert rc == 0
    rows = json.loads(bench_results.read_text(encoding="utf-8"))
    assert len(rows) == 1
    assert rows[0]["run_id"] == "2026-07-15-run01"


def test_record_rejects_missing_keys(bench_results):
    bad = _row()
    del bad["judge_model"]
    with pytest.raises(SystemExit):
        run_ab.main(["record", "--family", "cold-start", "--row", json.dumps(bad)])


def test_record_rejects_duplicate_run_id(bench_results):
    run_ab.main(["record", "--family", "cold-start", "--row", json.dumps(_row())])
    with pytest.raises(SystemExit):
        run_ab.main(["record", "--family", "cold-start", "--row", json.dumps(_row())])
    rows = json.loads(bench_results.read_text(encoding="utf-8"))
    assert len(rows) == 1  # history untouched
