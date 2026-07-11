#!/bin/bash
# seam-smoke.sh — run-8 delegation-seam smoke (run-7 report §6 precondition 1+2).
# Spawns ONE `claude -p` in the throwaway smoke repo with the mitigated env and
# harvests: (a) how many delegated worker streams appeared in the harness
# project store for this spawn; (b) whether any worker's first user message is
# byte-identical to the prompt.
set -u
B=/tmp/claude-0/-home-user/2fd357f9-ee27-520d-af7b-eb0ef75942e2/scratchpad/run08
H=$B/harness
REPO=$B/seam-smoke
PROJ=/root/.claude/projects/$(echo "$REPO" | tr '/' '-')
OUT=$H/seam-smoke-evidence
mkdir -p "$OUT"

# pre-state
ls "$PROJ"/*/subagents/agent-*.jsonl 2>/dev/null | sort > "$OUT/agents-before.txt" || true
ls "$PROJ"/*.jsonl 2>/dev/null | sort > "$OUT/orch-before.txt" || true

# ENV MITIGATION (recorded verbatim in manifest): remove background-task +
# coordinator delegation-policy vars from the spawned CLI's environment.
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

# post-state
ls "$PROJ"/*/subagents/agent-*.jsonl 2>/dev/null | sort > "$OUT/agents-after.txt" || true
ls "$PROJ"/*.jsonl 2>/dev/null | sort > "$OUT/orch-after.txt" || true
comm -13 "$OUT/agents-before.txt" "$OUT/agents-after.txt" > "$OUT/agents-new.txt"
comm -13 "$OUT/orch-before.txt" "$OUT/orch-after.txt" > "$OUT/orch-new.txt"
echo "spawn exit: $(cat "$OUT/cli-exit.txt")"
echo "new orchestrator streams: $(wc -l < "$OUT/orch-new.txt")"
echo "new worker streams: $(wc -l < "$OUT/agents-new.txt")"
cat "$OUT/agents-new.txt"
