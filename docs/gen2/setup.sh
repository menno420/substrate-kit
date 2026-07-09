#!/bin/bash
# substrate-kit gen-2 — defensive environment setup script.
#
# Contract (every rule paid for by a gen-1 incident — see
# docs/gen2/environment-setup.md and docs/environment-setup-script.md):
#   1. ALWAYS `exit 0` — a non-zero exit kills the session at provisioning
#      (the PR #47 casualty: "Setup script failed with exit code 1").
#   2. NEVER assume the cwd is the repo clone — the killed session's script
#      ran from /home/user, not the clone. Detect and cd, guarded.
#   3. NEVER run a bare `pip install -r` — guard on file existence first
#      (this repo is stdlib-only and has NO requirements.txt).
#   4. Every install step is non-fatal (`|| echo WARNING`); real failures
#      stay visible as [setup] WARNING lines in the provision log.

echo "[setup] Working directory: $(pwd)"

# --- Locate the repo clone (never assume cwd) -------------------------------
REPO_DIR=""
if [ -e /home/user/substrate-kit/.git ]; then
  REPO_DIR=/home/user/substrate-kit
else
  for d in /home/user/*/ /workspace/*/; do
    if [ -e "${d}.git" ]; then
      REPO_DIR="${d%/}"
      break
    fi
  done
fi

if [ -n "$REPO_DIR" ] && cd "$REPO_DIR"; then
  echo "[setup] Repo clone: $REPO_DIR"
else
  echo "[setup] WARNING: no git repo found under /home/user or /workspace; continuing in $(pwd)"
fi

# --- Python dependencies (all guarded) --------------------------------------
echo "[setup] Installing Python dependencies..."
if [ -f requirements.txt ]; then
  pip install -r requirements.txt || echo "[setup] WARNING: pip install -r requirements.txt failed (continuing)"
else
  echo "[setup] no requirements.txt, skipping (stdlib-only repo; packaging lives in pyproject.toml)"
fi

# CI's only dev tools are pytest + ruff (mirrors .github/workflows/ci.yml
# "Install dev tools"). Verified 2026-07-09: a fresh container does NOT have
# pytest preinstalled ("/usr/local/bin/python3: No module named pytest").
if command -v pip >/dev/null 2>&1; then
  pip install -q pytest ruff || echo "[setup] WARNING: pip install pytest ruff failed (continuing)"
  echo "[setup] dev tools: $(python3 -m pytest --version 2>/dev/null || echo 'pytest UNAVAILABLE') · $(python3 -m ruff --version 2>/dev/null || echo 'ruff UNAVAILABLE')"
else
  echo "[setup] WARNING: pip not found; skipping dev tools"
fi

echo "[setup] Done."
exit 0
