# Claude Code on the web — environment setup script

> **Status:** `owner-guidance`
>
> The corrected script below must be pasted by the repo owner into the
> project's cloud environment settings (owner-only). This file is the durable,
> version-controlled copy.

The setup script itself is NOT a repo file: per the
[Claude Code on the web docs](https://code.claude.com/docs/en/claude-code-on-the-web#setup-scripts),
setup scripts are attached to the cloud environment and configured in the
environment settings dialog ("Setup script" field), not in the repository.

## The failure this fixes

A web session died at provisioning with:

```
fatal: not a git repository (or any of the parent directories): .git
[setup] Working directory: /home/user
[setup] Installing Python dependencies...
ERROR: Could not open requirements file: [Errno 2] No such file or directory: 'requirements.txt'
```

Two bugs, one lesson each:

1. **Wrong working directory.** The setup script ran with cwd `/home/user`,
   not the repo clone at `/home/user/substrate-kit`. Setup scripts must not
   assume they start inside the clone — detect the repo directory and `cd`
   into it.
2. **Fatal exit on a missing optional file.** `pip install -r requirements.txt`
   exited 1 because this repo has no `requirements.txt` (it is stdlib-only;
   packaging lives in `pyproject.toml`). Per the docs, *"If the script exits
   non-zero, the session fails to start."* Every step must be guarded so
   missing optional files are skipped loudly instead of killing the session;
   the script must always end `exit 0` while keeping real failures visible in
   its echoed output.

## Corrected setup script (paste verbatim into the environment settings)

```bash
#!/bin/bash
# substrate-kit — Claude Code on the web environment setup script.
# Rules: never assume the cwd is the repo clone; never exit non-zero for a
# missing optional file (a non-zero exit kills the session at provisioning).
# Real failures stay visible as [setup] WARNING lines in the provision log.

echo "[setup] Working directory: $(pwd)"

# Locate the repo clone: prefer the known path, else the first git repo
# directly under /home/user.
REPO_DIR=""
if [ -e /home/user/substrate-kit/.git ]; then
  REPO_DIR=/home/user/substrate-kit
else
  for d in /home/user/*/; do
    if [ -e "${d}.git" ]; then
      REPO_DIR="${d%/}"
      break
    fi
  done
fi

if [ -n "$REPO_DIR" ] && cd "$REPO_DIR"; then
  echo "[setup] Repo clone: $REPO_DIR"
else
  echo "[setup] WARNING: no git repo found under /home/user; continuing in $(pwd)"
fi

echo "[setup] Installing Python dependencies..."
if [ -f requirements.txt ]; then
  pip install -r requirements.txt || echo "[setup] WARNING: pip install -r requirements.txt failed (continuing)"
else
  echo "[setup] no requirements.txt, skipping"
fi

# The kit engine is stdlib-only; CI's only dev tools are pytest + ruff
# (mirrors .github/workflows/ci.yml "Install dev tools").
pip install pytest ruff || echo "[setup] WARNING: pip install pytest ruff failed (continuing)"

echo "[setup] Done."
exit 0
```

## Owner action

Open the environment settings dialog for this project at
[claude.ai/code](https://claude.ai/code), replace the **Setup script** field
contents with the script above, and save. Changing the setup script rebuilds
the environment cache, so the next new session re-runs it — check its
provision log for `[setup] Repo clone:` and `[setup] Done.`.
