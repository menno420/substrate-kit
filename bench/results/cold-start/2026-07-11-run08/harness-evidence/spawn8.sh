#!/bin/bash
# spawn8.sh <arm:on|off> <task:T2|T4|T5> — spawn one measured cold session and harvest it.
# run-8 = run-7's spawn.sh + the §6 env mitigation (background/coordinator vars
# removed from the spawned CLI's environment) + flat-seam harvest (the measured
# stream is the spawned session's own stream; any delegated subagent = decomposition).
set -u
ARM="$1"; TASK="$2"
B=/tmp/claude-0/-home-user/2fd357f9-ee27-520d-af7b-eb0ef75942e2/scratchpad/run08
H=$B/harness
RUN=$B/2026-07-11-run08
REPO=$RUN/$ARM/repo
PROJ=/root/.claude/projects/$(echo "$REPO" | tr '/' '-')
SESS=$H/sessions/$ARM-$TASK
mkdir -p "$SESS"

# pre-state
git -C "$REPO" rev-parse HEAD > "$SESS/pre-head.txt"
ls "$PROJ"/*/subagents/agent-*.jsonl 2>/dev/null | sort > "$SESS/agents-before.txt" || true
ls "$PROJ"/*.jsonl 2>/dev/null | sort > "$SESS/sessions-before.txt" || true
[ -f "$REPO/.substrate/guard-fires.jsonl" ] && wc -l < "$REPO/.substrate/guard-fires.jsonl" > "$SESS/guardfires-before.txt" || echo 0 > "$SESS/guardfires-before.txt"

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

# post-state
git -C "$REPO" rev-parse HEAD > "$SESS/post-head.txt"
ls "$PROJ"/*/subagents/agent-*.jsonl 2>/dev/null | sort > "$SESS/agents-after.txt" || true
ls "$PROJ"/*.jsonl 2>/dev/null | sort > "$SESS/sessions-after.txt" || true
comm -13 "$SESS/agents-before.txt" "$SESS/agents-after.txt" > "$SESS/agents-new.txt"
comm -13 "$SESS/sessions-before.txt" "$SESS/sessions-after.txt" > "$SESS/sessions-new.txt"
[ -f "$REPO/.substrate/guard-fires.jsonl" ] && wc -l < "$REPO/.substrate/guard-fires.jsonl" > "$SESS/guardfires-after.txt" || echo 0 > "$SESS/guardfires-after.txt"
[ -f "$REPO/HANDOFF.md" ] && cp "$REPO/HANDOFF.md" "$SESS/HANDOFF-at-end.md"
echo "spawned $ARM-$TASK: exit $(cat "$SESS/cli-exit.txt"), new session streams: $(wc -l < "$SESS/sessions-new.txt"), new subagents (decomposition if >0): $(wc -l < "$SESS/agents-new.txt")"
cat "$SESS/sessions-new.txt"
