#!/bin/bash
# seam-smoke.sh — run-9 delegation-seam smoke (run-7 §6 preconditions 1+2, run-8 mechanics).
set -u
B=/tmp/claude-0/-home-user/84318bc8-297a-5dfa-abef-d81000430bbb/scratchpad/run09
H=$B/harness
REPO=$B/seam-smoke
PROJ=/root/.claude/projects/$(echo "$REPO" | tr '/' '-')
OUT=$H/seam-smoke-evidence
mkdir -p "$OUT"
ls "$PROJ"/*/subagents/agent-*.jsonl 2>/dev/null | sort > "$OUT/agents-before.txt" || true
ls "$PROJ"/*.jsonl 2>/dev/null | sort > "$OUT/orch-before.txt" || true
date -u +%Y-%m-%dT%H:%M:%SZ > "$OUT/start-utc.txt"
( cd "$REPO" && env \
    -u CLAUDE_AUTO_BACKGROUND_TASKS \
    -u CLAUDE_CODE_BG_TASKS_REPORT_RUNNING \
    -u CLAUDE_CODE_COORDINATOR_MODE \
    -u CLAUDE_CODE_COORDINATOR_EXTRA_TOOLS \
    -u CLAUDE_CODE_CHILD_SESSION \
    claude -p "$(cat "$H/prompt-smoke.txt")" \
    --permission-mode acceptEdits \
    --allowedTools "Bash(git add:*)" "Bash(git commit:*)" "Bash(python3 -m pytest:*)" "Bash(python -m pytest:*)" \
    --model sonnet ) > "$OUT/cli-stdout.txt" 2> "$OUT/cli-stderr.txt"
echo "exit=$?" > "$OUT/cli-exit.txt"
date -u +%Y-%m-%dT%H:%M:%SZ > "$OUT/end-utc.txt"
ls "$PROJ"/*/subagents/agent-*.jsonl 2>/dev/null | sort > "$OUT/agents-after.txt" || true
ls "$PROJ"/*.jsonl 2>/dev/null | sort > "$OUT/orch-after.txt" || true
comm -13 "$OUT/agents-before.txt" "$OUT/agents-after.txt" > "$OUT/agents-new.txt"
comm -13 "$OUT/orch-before.txt" "$OUT/orch-after.txt" > "$OUT/orch-new.txt"
echo "spawn exit: $(cat "$OUT/cli-exit.txt")"
echo "new session streams: $(wc -l < "$OUT/orch-new.txt")"
echo "new subagent streams (decomposition if >0): $(wc -l < "$OUT/agents-new.txt")"
cat "$OUT/orch-new.txt"
