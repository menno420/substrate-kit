#!/usr/bin/env python3
"""run_ab — the A/B runner harness (founding plan §5.0/§5.1, companion D §3).

The harness does the MECHANICAL half of a paired run; the cold sessions
themselves are spawned by the runner session (the lab loop spawns a dedicated
fresh runner — never inline in its own warm context) and the judge is a
separate invocation seeing only transcripts + `bench/rubric/`. This script
never talks to a model.

Three subcommands, in run order:

``prepare``
    Build the arm directories for one run: generate the seed project ONCE
    (``seeds/make_seed.py --seed N``), copy it identically into ``on/repo``
    and ``off/repo``, ``git init`` + one identical seed commit in each, adopt
    the kit on the ON arm only (``--wire-enforcement`` when the task set
    includes T5 or a merge-shaped task), then run the §5.1 **smoke step** —
    walk the ON arm (planted docs exist, `check --strict` exits 0) before any
    paired session runs (run 1's root cause was discoverable at setup).
    Writes ``manifest.json`` + per-task prompt pointers.

``collect``
    File one session's artifacts into the run directory:
    ``<run>/<arm>/<task>/transcript.jsonl`` (the score_m1 event format),
    ``diff.patch``, and anything else passed. Also scores M1 immediately and
    stores ``m1.json`` next to the transcript (text is cheap and the
    raw-artifacts-were-lost failure must not recur — plan §5.0).

``record``
    Append ONE row to ``bench/results/<family>/index.json`` (schema-checked;
    append-only — the checker holds existing rows immutable) and remind the
    runner what belongs in the run directory (report.md, metrics.json,
    transcripts/).

Who may run what (the separation law, §5.0/§6.2): the loop/runner uses this
harness; the RUBRIC is never edited here; results are append-only; and no
session ever grades work it produced.

Bench-side tooling, not engine code: subprocess/print are fine here.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

BENCH_ROOT = Path(__file__).resolve().parent
KIT_ROOT = BENCH_ROOT.parent
DEFAULT_KIT = KIT_ROOT / "dist" / "bootstrap.py"

TASKS = ("T1", "T2", "T3", "T4", "T5")
# Task sets that exercise the enforcement half adopt with --wire-enforcement
# (§5.1 correction 2: the thesis is the door, not the notebook).
ENFORCEMENT_TASKS = frozenset({"T5"})

# One row per run — the §5.1 results-home schema, keys required verbatim.
INDEX_ROW_KEYS = (
    "date",
    "kit_version",
    "run_id",
    "tasks",
    "m1_on",
    "m1_off",
    "m2",
    "m3",
    "verdict",
    "judge_model",
    "notes",
)


def _run(cmd: list[str], cwd: Path) -> None:
    """Run one command, failing loudly (the harness never hides a red step)."""
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        sys.stderr.write(result.stdout + result.stderr)
        raise SystemExit(f"command failed in {cwd}: {' '.join(cmd)}")


def _git_seed_commit(repo: Path) -> None:
    """git init + one identical seed commit (companion D §2)."""
    _run(["git", "init", "-q"], repo)
    _run(["git", "config", "user.email", "bench@substrate-kit"], repo)
    _run(["git", "config", "user.name", "bench-runner"], repo)
    _run(["git", "add", "-A"], repo)
    _run(["git", "commit", "-q", "-m", "seed"], repo)


def cmd_prepare(args) -> int:
    run_dir = args.out / args.run_id
    if run_dir.exists():
        raise SystemExit(f"refusing to overwrite existing run dir {run_dir}")
    tasks = [t.strip() for t in args.tasks.split(",") if t.strip()]
    unknown = [t for t in tasks if t not in TASKS]
    if unknown:
        raise SystemExit(f"unknown task(s) {unknown} — corpus is {TASKS}")

    # 1. Generate the seed ONCE, then copy byte-identically to both arms.
    seed_src = run_dir / "seed-src"
    seed_src.mkdir(parents=True)
    _run(
        [
            sys.executable,
            str(BENCH_ROOT / "seeds" / "make_seed.py"),
            "--dest",
            str(seed_src),
            "--seed",
            str(args.seed),
        ],
        KIT_ROOT,
    )
    arms = {}
    for arm in ("on", "off"):
        repo = run_dir / arm / "repo"
        shutil.copytree(seed_src, repo)
        _git_seed_commit(repo)
        arms[arm] = str(repo)

    # 2. Adopt the kit on the ON arm only (guided mode is adopt's default —
    #    what a genuinely new adopter runs; --include-claude per companion D).
    on_repo = run_dir / "on" / "repo"
    shutil.copy2(args.kit, on_repo / "bootstrap.py")
    adopt_cmd = [sys.executable, "bootstrap.py", "adopt", "--include-claude"]
    wire = args.wire_enforcement or any(t in ENFORCEMENT_TASKS for t in tasks)
    if wire:
        adopt_cmd.append("--wire-enforcement")
    _run(adopt_cmd, on_repo)
    _run(["git", "add", "-A"], on_repo)
    _run(["git", "commit", "-q", "-m", "adopt substrate-kit"], on_repo)

    # 3. The §5.1 smoke step: walk the ON arm before any paired session runs.
    smoke = []
    for rel in ("CONSTITUTION.md", "docs/current-state.md", ".sessions"):
        smoke.append(f"{rel}: {'present' if (on_repo / rel).exists() else 'MISSING'}")
    check = subprocess.run(
        [sys.executable, "bootstrap.py", "check", "--strict"],
        cwd=on_repo,
        capture_output=True,
        text=True,
    )
    smoke.append(f"check --strict exit={check.returncode}")
    if any("MISSING" in line for line in smoke) or check.returncode != 0:
        sys.stderr.write("\n".join(smoke) + "\n" + check.stdout + check.stderr)
        raise SystemExit("SMOKE FAILED — fix the arm before running any session (§5.1).")

    manifest = {
        "run_id": args.run_id,
        "date": date.today().isoformat(),
        "seed": args.seed,
        "tasks": tasks,
        "wire_enforcement": wire,
        "kit": str(args.kit),
        "arms": arms,
        "task_prompts": {t: str(BENCH_ROOT / "tasks" / f"{t}.md") for t in tasks},
        "rubric": str(BENCH_ROOT / "rubric" / "cold-start-rubric.md"),
        "smoke": smoke,
    }
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2))
    print(
        f"\nprepared {run_dir}. Next: spawn each task's COLD session per arm "
        "(prompt text = the fenced block in the task file; the session sees "
        "only its arm repo), `collect` each transcript/diff, judge with the "
        "pinned rubric in a SEPARATE invocation, then `record` the row.",
    )
    return 0


def cmd_collect(args) -> int:
    dest = args.run_dir / args.arm / args.task
    dest.mkdir(parents=True, exist_ok=True)
    shutil.copy2(args.transcript, dest / "transcript.jsonl")
    if args.diff:
        shutil.copy2(args.diff, dest / "diff.patch")
    # Score M1 immediately and keep it next to the transcript.
    score = subprocess.run(
        [sys.executable, str(BENCH_ROOT / "score_m1.py"), "--json", str(dest / "transcript.jsonl")],
        capture_output=True,
        text=True,
    )
    if score.returncode == 0 and score.stdout.strip():
        (dest / "m1.json").write_text(score.stdout, encoding="utf-8")
        print(score.stdout.strip())
    else:
        sys.stderr.write(score.stderr)
        print(f"warning: M1 scoring failed for {dest} — transcript kept, score later.")
    print(f"collected {args.arm}/{args.task} into {dest}")
    return 0


def cmd_record(args) -> int:
    row = json.loads(args.row)
    missing = [k for k in INDEX_ROW_KEYS if k not in row]
    if missing:
        raise SystemExit(f"row is missing required key(s): {missing} (schema: {INDEX_ROW_KEYS})")
    index_path = BENCH_ROOT / "results" / args.family / "index.json"
    rows = json.loads(index_path.read_text(encoding="utf-8")) if index_path.exists() else []
    if not isinstance(rows, list):
        raise SystemExit(f"{index_path} is not a JSON array — refusing to touch it.")
    if any(existing.get("run_id") == row.get("run_id") for existing in rows):
        raise SystemExit(f"run_id {row.get('run_id')!r} already recorded — results are append-only.")
    rows.append(row)
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
    print(f"appended run {row.get('run_id')!r} to {index_path} ({len(rows)} row(s) total).")
    print(
        "Commit the run directory alongside it (report.md + metrics.json + "
        "transcripts/) — raw artifacts are committed, plan §5.0.",
    )
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)

    prepare = sub.add_parser("prepare", help="build the arm dirs for one run")
    prepare.add_argument("--run-id", required=True, help="e.g. 2026-07-15-run01")
    prepare.add_argument("--seed", type=int, required=True, help="seed-corpus RNG seed (fresh per run)")
    prepare.add_argument("--tasks", default="T2,T4,T5", help="comma list (minimum firing: T2,T4,T5 — §5.1)")
    prepare.add_argument("--kit", type=Path, default=DEFAULT_KIT, help="bootstrap.py to adopt on the ON arm")
    prepare.add_argument("--out", type=Path, required=True, help="scratch dir for arm repos (NOT bench/results)")
    prepare.add_argument("--wire-enforcement", action="store_true", help="force --wire-enforcement on the ON adopt")
    prepare.set_defaults(func=cmd_prepare)

    collect = sub.add_parser("collect", help="file one session's artifacts + score M1")
    collect.add_argument("--run-dir", type=Path, required=True)
    collect.add_argument("--arm", choices=("on", "off"), required=True)
    collect.add_argument("--task", choices=TASKS, required=True)
    collect.add_argument("--transcript", type=Path, required=True, help="event-JSONL (see score_m1.py)")
    collect.add_argument("--diff", type=Path, default=None)
    collect.set_defaults(func=cmd_collect)

    record = sub.add_parser("record", help="append one row to a results index (append-only)")
    record.add_argument("--family", choices=("cold-start", "allocation", "guards", "ideas", "friction"), required=True)
    record.add_argument("--row", required=True, help="the row as a JSON object string")
    record.set_defaults(func=cmd_record)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
