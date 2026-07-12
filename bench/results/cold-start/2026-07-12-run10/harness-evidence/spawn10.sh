#!/bin/bash
# spawn10.sh <arm:on|off> <task:T2|T4|T5> — spawn one measured cold session, harvest evidence.
# run-10 = run-9 spawn9.sh mechanics: env mitigation + flat-seam harvest + shared-stream segment offsets.
set -u
ARM="$1"; TASK="$2"
B=/tmp/claude-0/-home-user/dc36b696-9936-52c9-96ea-e75e9ea92515/scratchpad/run10
H=$B/harness
RUN=$B/2026-07-12-run10
REPO=$RUN/$ARM/repo
PROJ=/root/.claude/projects/$(echo "$REPO" | tr '/' '-')
SESS=$H/sessions/$ARM-$TASK
mkdir -p "$SESS"

git -C "$REPO" rev-parse HEAD > "$SESS/pre-head.txt"
ls "$PROJ"/*/subagents/agent-*.jsonl 2>/dev/null | sort > "$SESS/agents-before.txt" || true
ls "$PROJ"/*.jsonl 2>/dev/null | sort > "$SESS/sessions-before.txt" || true
for f in "$PROJ"/*.jsonl; do [ -f "$f" ] && echo "$f $(wc -l < "$f")"; done > "$SESS/stream-lines-before.txt" 2>/dev/null || true
[ -f "$REPO/.substrate/guard-fires.jsonl" ] && wc -l < "$REPO/.substrate/guard-fires.jsonl" > "$SESS/guardfires-before.txt" || echo 0 > "$SESS/guardfires-before.txt"
[ -f "$REPO/HANDOFF.md" ] && cp "$REPO/HANDOFF.md" "$SESS/HANDOFF-at-start.md"

date -u +%Y-%m-%dT%H:%M:%SZ > "$SESS/start-utc.txt"
( cd "$REPO" && env \
    -u CLAUDE_AUTO_BACKGROUND_TASKS \
    -u CLAUDE_CODE_BG_TASKS_REPORT_RUNNING \
    -u CLAUDE_CODE_COORDINATOR_MODE \
    -u CLAUDE_CODE_COORDINATOR_EXTRA_TOOLS \
    -u CLAUDE_CODE_CHILD_SESSION \
    claude -p "$(cat "$H/prompt-$TASK.txt")" \
    --permission-mode acceptEdits \
    --allowedTools "Bash(git add:*)" "Bash(git commit:*)" "Bash(python3 -m pytest:*)" "Bash(python -m pytest:*)" \
    --model sonnet ) > "$SESS/cli-stdout.txt" 2> "$SESS/cli-stderr.txt"
echo "exit=$?" > "$SESS/cli-exit.txt"
date -u +%Y-%m-%dT%H:%M:%SZ > "$SESS/end-utc.txt"

git -C "$REPO" rev-parse HEAD > "$SESS/post-head.txt"
ls "$PROJ"/*/subagents/agent-*.jsonl 2>/dev/null | sort > "$SESS/agents-after.txt" || true
ls "$PROJ"/*.jsonl 2>/dev/null | sort > "$SESS/sessions-after.txt" || true
for f in "$PROJ"/*.jsonl; do [ -f "$f" ] && echo "$f $(wc -l < "$f")"; done > "$SESS/stream-lines-after.txt" 2>/dev/null || true
comm -13 "$SESS/agents-before.txt" "$SESS/agents-after.txt" > "$SESS/agents-new.txt"
comm -13 "$SESS/sessions-before.txt" "$SESS/sessions-after.txt" > "$SESS/sessions-new.txt"
[ -f "$REPO/.substrate/guard-fires.jsonl" ] && wc -l < "$REPO/.substrate/guard-fires.jsonl" > "$SESS/guardfires-after.txt" || echo 0 > "$SESS/guardfires-after.txt"
[ -f "$REPO/HANDOFF.md" ] && cp "$REPO/HANDOFF.md" "$SESS/HANDOFF-at-end.md"
git -C "$REPO" diff HEAD > "$SESS/worktree-diff-at-end.patch" 2>/dev/null || true
echo "spawned $ARM-$TASK: $(cat "$SESS/cli-exit.txt"), new streams: $(wc -l < "$SESS/sessions-new.txt"), new subagents (decomposition if >0): $(wc -l < "$SESS/agents-new.txt")"
