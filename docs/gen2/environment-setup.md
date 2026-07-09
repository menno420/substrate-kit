# Environment spec — gen-2 kit-lab (2026-07-09)

> **Status:** `owner-guidance` — the gen-2 environment specification +
> TESTED defensive setup script, written at the gen-1 wind-down (phase 2,
> PR #74). Builds on [`docs/environment-setup-script.md`](../environment-setup-script.md)
> (the PR #47 post-mortem: a web session was KILLED at provisioning by a
> wrong-cwd + hard-fail-on-missing-requirements.txt script). The script
> itself is [`setup.sh`](setup.sh) — the owner pastes its contents into the
> environment settings "Setup script" field (owner-only dialog;
> ⚑ OWNER-ACTION 11 in `control/status.md`).

## Non-negotiable script rules (each one paid for in gen-1)

1. **Always `exit 0`.** Per the platform docs, a non-zero setup exit fails
   the session at provisioning. The gen-1 casualty's provision log,
   verbatim:

   ```
   fatal: not a git repository (or any of the parent directories): .git
   [setup] Working directory: /home/user
   [setup] Installing Python dependencies...
   ERROR: Could not open requirements file: [Errno 2] No such file or directory: 'requirements.txt'
   ```

2. **Never assume the cwd is the repo clone** — the killed script ran from
   `/home/user`. Detect the clone (known path first, then scan
   `/home/user/*/` and `/workspace/*/` for a `.git`), `cd` guarded, and
   continue with a WARNING if none is found.
3. **No bare `pip install -r`** — guard on `[ -f requirements.txt ]`
   first. This repo is stdlib-only (packaging in `pyproject.toml`); there
   is no requirements.txt to install.
4. **Every install step non-fatal** (`|| echo "[setup] WARNING: ..."`), so
   real failures stay visible in the provision log without killing the
   session.
5. **Do install `pytest` + `ruff`** — CI's only dev tools
   (`.github/workflows/ci.yml` "Install dev tools"), and verified missing
   from a fresh container at wind-down:
   `/usr/local/bin/python3: No module named pytest`.

## Test evidence (run in-container at wind-down, 2026-07-09)

From `/` (the wrong-cwd case that killed the gen-1 session):

```
$ cd / && bash /home/user/substrate-kit/docs/gen2/setup.sh; echo "exit code: $?"
[setup] Working directory: /
[setup] Repo clone: /home/user/substrate-kit
[setup] Installing Python dependencies...
[setup] no requirements.txt, skipping (stdlib-only repo; packaging lives in pyproject.toml)
WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv
[setup] dev tools: pytest 9.1.1 · ruff 0.15.21
[setup] Done.
exit code: 0
```

From the repo dir:

```
$ cd /home/user/substrate-kit && bash docs/gen2/setup.sh; echo "exit code: $?"
[setup] Working directory: /home/user/substrate-kit
[setup] Repo clone: /home/user/substrate-kit
[setup] Installing Python dependencies...
[setup] no requirements.txt, skipping (stdlib-only repo; packaging lives in pyproject.toml)
WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv
[setup] dev tools: pytest 9.1.1 · ruff 0.15.21
[setup] Done.
exit code: 0
```

(The pip root-user WARNING is pip's own advisory noise in this container,
not a failure; both runs exit 0.)

## Environment variables — NAMES only, never values

The kit engine is stdlib-only and needs **no secrets to build or test**.
The names below are what a gen-2 kit-lab environment uses or will use:

- `GITHUB_TOKEN` / the session's GitHub MCP + git-proxy credentials —
  provisioned by the platform, not by this script (`printenv` before
  assuming absence; THE DISCOVERY RULE).
- `RAILWAY_TOKEN` — **future**, project-scoped to the `kit-lab` Railway
  project, only after the owner creates it (⚑ OWNER-ACTION 6 / P5).
  **Never** use ambient Railway IDs already present in an environment —
  the ambient-IDs-are-production rule.
- A read-only cross-repo PAT — **future**, only if the owner picks P13
  over the P11 public flip (⚑ OWNER-ACTION 8).

Nothing else. A setup script must not echo, require, or validate any
secret value.

## What the environment should contain beyond the script (gen-1 E2 list)

Per self-review E2, in priority order: pytest + ruff preinstalled (or the
script installs them — done above); a documented git proxy (its 403 walls
are in [`next-boot.md`](next-boot.md) §3 now); worktree-per-worker as the
default layout; repo-scoped agent instructions (no inherited foreign
CLAUDE.md); and — still owner-only — an administration-read path for
required-check status (issue #36 report 3).
