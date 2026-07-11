#!/bin/bash
# spawn.sh <arm:on|off> <task:T2|T4|T5> — spawn one measured cold session and harvest it.
set -u
ARM="$1"; TASK="$2"
H=/tmp/claude-0/-home-user/2568bc4d-6464-5fda-b39e-b82c5674376c/scratchpad/run07/harness
RUN=/tmp/claude-0/-home-user/2568bc4d-6464-5fda-b39e-b82c5674376c/scratchpad/run07/2026-07-11-run07
REPO=$RUN/$ARM/repo
PROJ=/root/.claude/projects/$(echo "$REPO" | tr '/' '-')
SESS=$H/sessions/$ARM-$TASK
mkdir -p "$SESS"

# pre-state
git -C "$REPO" rev-parse HEAD > "$SESS/pre-head.txt"
ls "$PROJ"/*/subagents/agent-*.jsonl 2>/dev/null | sort > "$SESS/agents-before.txt"
for f in "$PROJ"/*.jsonl; do [ -f "$f" ] && wc -l < "$f" > "$SESS/orch-lines-before.txt" && echo "$f" > "$SESS/orch-file.txt"; done 2>/dev/null
[ -f "$SESS/orch-lines-before.txt" ] || echo 0 > "$SESS/orch-lines-before.txt"
[ -f "$REPO/.substrate/guard-fires.jsonl" ] && wc -l < "$REPO/.substrate/guard-fires.jsonl" > "$SESS/guardfires-before.txt" || echo 0 > "$SESS/guardfires-before.txt"

date -u +%Y-%m-%dT%H:%M:%SZ > "$SESS/start-utc.txt"
( cd "$REPO" && claude -p "$(cat "$H/prompt-$TASK.txt")" \
    --permission-mode acceptEdits \
    --allowedTools "Bash(git add:*)" "Bash(git commit:*)" "Bash(python3 -m pytest:*)" "Bash(python -m pytest:*)" \
    --model sonnet ) > "$SESS/cli-stdout.txt" 2> "$SESS/cli-stderr.txt"
echo "exit=$?" > "$SESS/cli-exit.txt"
date -u +%Y-%m-%dT%H:%M:%SZ > "$SESS/end-utc.txt"

# post-state
git -C "$REPO" rev-parse HEAD > "$SESS/post-head.txt"
ls "$PROJ"/*/subagents/agent-*.jsonl 2>/dev/null | sort > "$SESS/agents-after.txt"
comm -13 "$SESS/agents-before.txt" "$SESS/agents-after.txt" > "$SESS/agents-new.txt"
for f in "$PROJ"/*.jsonl; do [ -f "$f" ] && wc -l < "$f" > "$SESS/orch-lines-after.txt" && echo "$f" > "$SESS/orch-file.txt"; done 2>/dev/null
[ -f "$REPO/.substrate/guard-fires.jsonl" ] && wc -l < "$REPO/.substrate/guard-fires.jsonl" > "$SESS/guardfires-after.txt" || echo 0 > "$SESS/guardfires-after.txt"
[ -f "$REPO/HANDOFF.md" ] && cp "$REPO/HANDOFF.md" "$SESS/HANDOFF-at-end.md"
echo "spawned $ARM-$TASK: exit $(cat "$SESS/cli-exit.txt"), new agents: $(wc -l < "$SESS/agents-new.txt")"
cat "$SESS/agents-new.txt"
