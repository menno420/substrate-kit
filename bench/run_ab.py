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
    and ``off/repo``, ``git init`` + one identical seed commit in each, run
    the generated seed's OWN test suite in both arms (red aborts the prepare
    — run 2's seed-424242 SyntaxError class dies here, at prepare time, with
    a named error instead of surfacing mid-run), adopt the kit on the ON arm
    only (``--wire-enforcement`` when the task set includes T5 or a
    merge-shaped task), walk the KL-7 **RED→ENGAGED→GREEN arc** on the ON arm
    (deterministic seed-derived interview answers, ``render --live``, staged
    gate install, first session card, seed heartbeat — a bare adopt is born
    red by design since kit v1.3.0), then run the §5.1 **smoke step** — the
    ON arm must actually read GREEN (planted docs exist, `check --strict`
    exits 0) before any paired session runs (run 1's root cause was
    discoverable at setup). Writes ``manifest.json`` + per-task prompt
    pointers on success AND on smoke failure (``smoke_failed: true`` — an
    aborted prepare leaves evidence, the run-2 lesson).

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
from datetime import date, datetime, timezone
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


# The interview slots the ON-arm engagement arc answers — the same 13 the CI
# cold-adopt smoke walks (.github/workflows/ci.yml). Deliberately pinned, not
# discovered: the arc must be byte-reproducible across runs (each runner
# hand-engaging with ad-hoc answers was a cross-run comparability variable the
# judge already flagged between runs 1 and 2). If the question bank grows a
# slot this list misses, the prepare smoke's own `check --strict` assert fails
# loudly with an `unrendered-slot` finding naming it — the same drift catcher
# CI relies on.
ENGAGE_SLOTS = (
    "integration_mode",
    "project_name",
    "primary_language",
    "architecture_layers",
    "verify_command",
    "ownership_model",
    "doc_roots",
    "owner_profile",
    "mutation_seam",
    "review_ritual",
    "drift_resolution",
    "staleness_review",
    "new_area_ownership",
)


def _seed_answers(seed: int, project: str) -> dict[str, str]:
    """Deterministic, seed-derived interview answers for the ON arm.

    Truthful where the seed project has a real value (name, language, verify
    command — every generated seed is a Python package with a pytest suite);
    a deterministic sentence everywhere else, long enough for every
    substance floor (max ``min_len`` in the bank is 20).
    """
    answers = {
        slot: (
            f"seed-{seed} {project}: deterministic bench prepare answer for "
            f"{slot} (scripted engagement arc, reproducible across runs)"
        )
        for slot in ENGAGE_SLOTS
    }
    answers["integration_mode"] = "guided"  # adopt's default — a real mode value
    answers["project_name"] = project
    answers["primary_language"] = "Python 3 (generated bench seed project)"
    answers["verify_command"] = "python3 -m pytest tests/ -q"
    return answers


def _engage_on_arm(on_repo: Path, run_id: str, seed: int, project: str) -> list[str]:
    """Walk the documented RED→ENGAGED→GREEN arc on the ON arm; return steps.

    Kit v1.3.0+ holds a bare adopt BORN RED under ``check --strict`` by
    design (the KL-7 engagement gate), so "adopted" no longer implies
    "green" — prepare scripts the same checklist the CI cold-adopt smoke
    walks (idea run-ab-prepare-engagement-arc-2026-07-09): answer every
    interview slot with deterministic seed-derived values, ``render --live``,
    install the staged gate workflow, write the first (complete) session
    card, write the first ``control/status.md`` heartbeat, commit. The §5.1
    smoke step then asserts the arm actually reads GREEN.
    """
    steps: list[str] = []
    for slot, value in _seed_answers(seed, project).items():
        _run([sys.executable, "bootstrap.py", "answer", slot, value], on_repo)
    steps.append(f"engage: answered {len(ENGAGE_SLOTS)} slots (seed-derived, deterministic)")
    _run([sys.executable, "bootstrap.py", "render", "--live"], on_repo)
    steps.append("engage: render --live")
    # Enforcement: install the staged gate (adopt --wire-enforcement already
    # planted it live when the task set includes T5).
    gate_dest = on_repo / ".github" / "workflows" / "substrate-gate.yml"
    staged = on_repo / ".substrate" / "ci" / "substrate-gate.yml"
    if gate_dest.exists():
        steps.append("engage: enforcement already wired (adopt --wire-enforcement)")
    elif staged.exists():
        gate_dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(staged, gate_dest)
        steps.append("engage: installed staged substrate-gate.yml")
    else:
        steps.append("engage: no staged gate found to install")
    # Session loop: the first real (complete) session card.
    card = on_repo / ".sessions" / f"{date.today().isoformat()}-adoption.md"
    card.parent.mkdir(parents=True, exist_ok=True)
    card.write_text(
        f"# adoption session — bench ON arm (run {run_id})\n\n"
        "> **Status:** `complete`\n\n"
        f"💡 idea: n/a — adoption arc scripted by run_ab.py prepare (seed {seed})\n"
        "⟲ previous-session review: n/a (first session on this arm)\n"
        "📊 Model: none (scripted by run_ab.py prepare) · low · adoption\n",
        encoding="utf-8",
    )
    steps.append(f"engage: session card {card.name}")
    # Control loop (KL-8): the seed status.md has no heartbeat and holds
    # strict RED until the first real overwrite.
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    status = on_repo / "control" / "status.md"
    status.parent.mkdir(parents=True, exist_ok=True)
    status.write_text(
        f"# {project} · status\n"
        f"updated: {now}\n"
        f"phase: adopted (bench ON arm, run {run_id})\n"
        "health: green\n"
        "last-shipped: none\n"
        "blockers: none\n"
        "orders: acked= done=\n"
        "⚑ needs-owner: none\n"
        "notes: seed heartbeat written by run_ab.py prepare (scripted engagement arc)\n",
        encoding="utf-8",
    )
    steps.append("engage: control/status.md heartbeat")
    _run(["git", "add", "-A"], on_repo)
    _run(["git", "commit", "-q", "-m", "engage substrate-kit (scripted arc)"], on_repo)
    steps.append("engage: committed")
    return steps


def _git_seed_commit(repo: Path) -> None:
    """git init + one identical seed commit (companion D §2)."""
    _run(["git", "init", "-q"], repo)
    _run(["git", "config", "user.email", "bench@substrate-kit"], repo)
    _run(["git", "config", "user.name", "bench-runner"], repo)
    _run(["git", "add", "-A"], repo)
    _run(["git", "commit", "-q", "-m", "seed"], repo)


def _seed_suite_smoke(repo: Path, arm: str) -> str:
    """Run the generated seed's OWN test suite in ``repo``; abort on red.

    The 2026-07-09 run-2 lesson (idea make-seed-yield-keyword-bug): a
    SyntaxError seed (seed 424242, ``yield`` measure token) reached the
    runner because nothing between "seed generated" and "session started"
    ever EXECUTED the seed project. This leg makes a broken seed die at
    prepare time with a named error, never mid-run.
    """
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-q"],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        sys.stderr.write(result.stdout + result.stderr)
        raise SystemExit(
            f"SEED SUITE RED on the {arm} arm ({repo}) — the generated seed "
            "project must be green before any session runs; fix the seed "
            "(or make_seed.py) and re-prepare (§5.1; the seed-424242 lesson)."
        )
    return f"seed suite ({arm}): green"


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
    seed_smoke = []
    for arm in ("on", "off"):
        repo = run_dir / arm / "repo"
        shutil.copytree(seed_src, repo)
        _git_seed_commit(repo)
        seed_smoke.append(_seed_suite_smoke(repo, arm))
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

    # 3. The engagement arc + §5.1 smoke step: a bare adopt is BORN RED under
    #    the KL-7 gate by design, so prepare itself walks the documented
    #    RED→ENGAGED→GREEN checklist, then asserts the arm reads GREEN before
    #    any paired session runs. The manifest is written on BOTH paths — a
    #    failed smoke leaves evidence (`smoke_failed`), never nothing (the
    #    run-2 lesson: an aborted prepare forced hand-written manifests).
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
    }
    smoke = list(seed_smoke)

    def _write_manifest() -> None:
        manifest["smoke"] = smoke
        (run_dir / "manifest.json").write_text(
            json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
        )

    project = next(
        (p.name for p in seed_src.iterdir() if p.is_dir() and p.name != "tests"),
        "seed-project",
    )
    try:
        smoke.extend(_engage_on_arm(on_repo, args.run_id, args.seed, project))
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
            raise SystemExit(
                "SMOKE FAILED — fix the arm before running any session (§5.1); "
                "manifest.json written with smoke_failed for evidence."
            )
    except SystemExit:
        manifest["smoke_failed"] = True
        _write_manifest()
        raise
    _write_manifest()
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
