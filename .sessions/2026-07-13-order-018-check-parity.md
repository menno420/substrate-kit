# Session · 2026-07-13 · ORDER 018 — check --strict runs the CI substrate-gate preflight legs locally

> **Status:** `complete`

Intent: make repo-local `python3 bootstrap.py check --strict` run the same legs as the CI substrate-gate — a merge-base-aware inbox append-only leg (base blob derived from `origin/main` when present, self-skip otherwise) and a config-driven local preflight-scripts leg (`preflight_scripts`, default `scripts/preflight.py`, self-skip with a NOTE when absent) — so a tree failing either CI leg also fails plain local `check --strict` (ORDER 018 / idea-engine ASK 002).

## Shipped (PR #332)

- **Inbox leg, merge-base aware:** `engine.cli._derive_inbox_base` derives the merge-base blob of `control/inbox.md` from `origin/main` (`git merge-base HEAD origin/main` + `git show`, mirroring the generated gate's bash exactly, including the empty-base posture for a file absent at base) whenever `--inbox-base` is not handed in. Self-skips with a NOTE when `.git` exists but no base is derivable; silently on a bare non-git tree. CI's explicit `--inbox-base` path is untouched.
- **Preflight-scripts leg:** new config key `preflight_scripts` (default `["scripts/preflight.py"]`) — `cmd_check`'s full lane runs each entry (shlex-split; `*.py` under `sys.executable`; `cwd=target`; 900 s timeout), non-zero exits riding the strict loop as `preflight-script` findings. CI's substrate-gate full lane already invokes `bootstrap.py check --strict`, so both venues execute this ONE config list with zero workflow edits. Absent script → NOTE'd self-skip; nested runs env-guarded (`SUBSTRATE_KIT_PREFLIGHT`).
- **§3.2 carve-out, documented at every statement site:** `subprocess` stays banned for engine/checker code (ruff TID251); the ONE carve-out is `cli.py`'s two local-ritual helpers, noqa'd inline with the rationale at the import site, named in the pyproject ban message, and cross-referenced from `check_inbox_append.py`'s docstring and `cmd_check`'s.
- **Done-when proof:** `tests/test_check_parity.py` — `test_local_strict_reds_on_non_append_inbox_with_derivable_origin_main` (a tree red on CI's inbox-grammar leg is red on plain local `check --strict`) and `test_local_strict_reds_on_failing_preflight_script` (a tree red on CI's preflight leg is red locally), plus grammar-red, pure-append-green, no-git/no-origin-main/absent-script self-skips, status-only scoping, argument entries (`--outbox` shape), nested-run guard, and the default-config pin. 15 new tests; suite 1265 passed (baseline 1250). Dist rebuilt byte-stable (sha256 identical across two builds).

## Decide-and-flag

- ⚑ subprocess carve-out via inline noqa confined to `cli.py`'s local-ritual legs — honors the ORDER's exact derivation words; pure-python `.git` reading rejected as packfile-fragile.
- ⚑ convergence by folding into `cmd_check` rather than generating a new workflow step — CI already runs `check --strict`, so one code path serves both venues.
- ⚑ `preflight_scripts` defaults to the conventional wrapper path so parity arrives on plain upgrade with no adopter config edit; absence costs one NOTE line, never a red.
- ⚑ scripts run under `sys.executable` (exists in both venues by construction), not the recorded config interpreter.
- ⚑ preflight findings are allowlistable (ordinary strict-loop findings with guard-fire telemetry); the session gate stays the only never-allowlistable seam.

💡 Session idea: **kit-planted preflight wrapper template** — `preflight_scripts` now defaults to `scripts/preflight.py`, but only idea-engine actually has one, so every other adopter pays a NOTE line per check forever. Plant a minimal host-owned `scripts/preflight.py` at adopt/upgrade (the `env-setup.sh` pattern: kit plants, host owns) whose body is just a `CHECKS` list + worst-exit runner — the NOTE noise disappears fleet-wide and every repo gains the one-edit-per-new-checker ritual that made idea-engine's convergence possible. Dedup: `docs/ideas/` has no preflight-wrapper idea (`enabler-install-preflight-2026-07-13.md` is the enabler branch-allowlist checker, unrelated).

📊 Model: Claude 5 family · standard effort · kit engine feature (checker parity) + tests + dist regen

⟲ Previous-session review (PR #331 — guard-fire write announcements + commit-with-session doctrine): genuinely effective in the field — this very session hit the exact designed moment (`check: 2 guard-fire record(s) appended … commit the delta with your session`) during the mid-work smoke run, and the announcement is what routed the `.substrate/guard-fires.jsonl` delta into the implementation commit instead of a mystery-dirty-tree revert; the fix demonstrably closed the loop it targeted, one session later. Concrete workflow improvement it surfaces: the announce line tells you *to* commit but not *how much of the tail is yours* — when a session runs `check` several times, the appended-record count per run has to be summed by hand to know the delta is all self-authored before staging; a one-line `git add .substrate/guard-fires.jsonl` suggestion (or a session-total in the line) would make the instruction paste-ready, per the Q-0263.2 asks-must-be-paste-ready bar.
