#!/usr/bin/env python3
"""score_m1 — scripted M1: words of tool output before the first mutating action.

M1's definition (companion D §4, as run in both Phase-2.5 passes): the number
of **whitespace-separated words of tool output the session consumed strictly
before its first mutating action**. It is scripted, never judged — the judge
receives these numbers.

Transcript format (what ``run_ab.py collect`` stores): **event JSONL** — one
JSON object per line, minimum fields:

    {"type": "tool_use",    "name": "<ToolName>", "input": {...}}
    {"type": "tool_result", "content": "<text>"}            # or content: [...]
    {"type": "text",        "content": "<assistant text>"}  # NOT counted

Rules:

- Only ``tool_result`` content counts toward M1 (tool output the session
  read); assistant text and tool inputs don't.
- The first **mutating** ``tool_use`` stops the count. Mutating =
  a file-writing tool (``Write``/``Edit``/``MultiEdit``/``NotebookEdit``), or
  a ``Bash`` command matching the mutation patterns below (redirection,
  rm/mv/cp/mkdir/touch, in-place sed/tee, git state changes, installs).
- **Read-only fd redirects are not mutations** (run-1 artifact fix, idea
  ``score-m1-mutation-artifacts-2026-07-09``): ``2>/dev/null``, ``2>&1``,
  ``>/dev/null`` and friends send a stream to the void or another fd —
  nothing in the repo is written. They are stripped from the command before
  the mutation pattern runs; genuine file redirection (``> out.txt``,
  ``2> err.log``, ``>> log``) still matches.
- **A mutating ``tool_use`` whose paired ``tool_result`` is an error did not
  mutate** (the other run-1 artifact — OFF-T5's counted "first mutation" was
  an Edit that failed ``File has not been read yet``). Pairing follows the
  collect stream shape: a tool's result is the next ``tool_result`` event
  after its ``tool_use``, before any other ``tool_use``. An error result
  (``is_error: true`` or ``<tool_use_error>`` content) cancels the candidate
  — its error text still counts as consumed output — and the walk continues
  to the next genuine mutation. A mutating ``tool_use`` with **no** paired
  result before the next ``tool_use`` (or end of stream) still stops the
  count: over-counting "mutating" is the conservative direction.
- ``content`` may be a string or a list of ``{"type": "text", "text": ...}``
  blocks (the Anthropic message shape) — both are handled.
- Unparseable lines are skipped with a warning to stderr (fail loud, score
  what's readable).

Bench-side tooling, not engine code: print/argparse/regex freely.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

MUTATING_TOOLS = frozenset({"Write", "Edit", "MultiEdit", "NotebookEdit"})

# Bash commands that mutate state (kept deliberately broad — an over-count of
# "mutating" only ever STOPS the word count earlier, which is conservative).
_BASH_MUTATION_RE = re.compile(
    r"(?:^|[;&|]\s*)"
    r"(?:rm|mv|cp|mkdir|touch|tee|ln|chmod|chown|truncate|patch|dd)\b"
    r"|>{1,2}"
    r"|\bsed\s+-[a-zA-Z]*i"
    r"|\bgit\s+(?:add|commit|checkout|switch|restore|apply|merge|rebase|reset|rm|mv|cherry-pick|stash|tag|push)\b"
    r"|\b(?:pip|pip3|npm|yarn|pnpm|cargo|apt|apt-get|brew)\s+(?:install|add|remove|uninstall)\b"
    r"|\bpython3?\s+\S*bootstrap\.py\s+(?:adopt|init|answer|mode|upgrade)\b",
)

# Read-only redirect forms, stripped BEFORE the mutation pattern runs (run-1
# artifact: ON-T2's `git log --oneline -5 2>/dev/null | head` and OFF-T4's
# line-1 twin scored as the first mutation via the bare `>{1,2}` branch).
# Matches: `2>/dev/null`, `>/dev/null`, `&>/dev/null`, `>>/dev/null`,
# `2>&1`, `>&2`. Does NOT match a redirect to a real file (`> out.txt`,
# `2> err.log`) — that stays a mutation.
_READONLY_REDIRECT_RE = re.compile(r"(?:\d+|&)?>{1,2}\s*(?:/dev/null\b|&\d+)")

# An error tool_result (the collect stream keeps the harness's error wrapper).
_TOOL_USE_ERROR_MARKER = "<tool_use_error>"


def _is_mutating(name: str, tool_input: dict) -> bool:
    """Return True when one tool_use event is a mutating action."""
    if name in MUTATING_TOOLS:
        return True
    if name == "Bash":
        command = str(tool_input.get("command", ""))
        command = _READONLY_REDIRECT_RE.sub(" ", command)
        return bool(_BASH_MUTATION_RE.search(command))
    return False


def _result_is_error(event: dict) -> bool:
    """Return True when one tool_result event records a FAILED tool call."""
    if event.get("is_error") is True:
        return True
    content = event.get("content", "")
    if isinstance(content, list):
        text = " ".join(
            str(block.get("text", "")) if isinstance(block, dict) else str(block)
            for block in content
        )
    else:
        text = str(content)
    return _TOOL_USE_ERROR_MARKER in text


def _content_words(content) -> int:
    """Count whitespace-separated words in a tool_result content payload."""
    if isinstance(content, str):
        return len(content.split())
    if isinstance(content, list):
        total = 0
        for block in content:
            if isinstance(block, dict):
                total += len(str(block.get("text", "")).split())
            else:
                total += len(str(block).split())
        return total
    return len(str(content).split())


def score_transcript(path: Path) -> dict:
    """Score one event-JSONL transcript; return the M1 record.

    A mutating tool_use is only the stopping point once its paired result
    proves it ran (or it has no paired result at all — conservative). While
    a candidate is pending, the very next tool_result decides: error →
    cancel the candidate and keep walking; anything else → stop.
    """
    words = 0
    events = 0
    first_mutation = None
    pending_mutation = None  # mutating tool_use awaiting its paired result
    with path.open(encoding="utf-8") as handle:
        for lineno, line in enumerate(handle, 1):
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                print(f"warning: {path}:{lineno}: unparseable line skipped", file=sys.stderr)
                continue
            if not isinstance(event, dict):
                continue
            events += 1
            kind = event.get("type")
            if kind == "tool_use":
                if pending_mutation is not None:
                    # The previous mutating tool_use never got a result before
                    # the next tool_use — treat it as executed (conservative).
                    first_mutation = pending_mutation
                    break
                name = str(event.get("name", ""))
                tool_input = event.get("input") if isinstance(event.get("input"), dict) else {}
                if _is_mutating(name, tool_input):
                    pending_mutation = {
                        "line": lineno,
                        "tool": name,
                        "command": str(tool_input.get("command", ""))[:200],
                    }
            elif kind == "tool_result":
                if pending_mutation is not None:
                    if _result_is_error(event):
                        # The mutation FAILED — nothing was written. Its error
                        # text is still tool output the session consumed.
                        pending_mutation = None
                        words += _content_words(event.get("content", ""))
                    else:
                        first_mutation = pending_mutation
                        break
                else:
                    words += _content_words(event.get("content", ""))
    if first_mutation is None and pending_mutation is not None:
        # Stream ended on an unanswered mutating tool_use — conservative stop.
        first_mutation = pending_mutation
    return {
        "transcript": str(path),
        "m1_words_before_first_mutation": words,
        "first_mutation": first_mutation,  # None = the session never mutated
        "events_seen": events,
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "transcripts",
        nargs="+",
        type=Path,
        help="event-JSONL transcript file(s) (see module docstring for the format)",
    )
    parser.add_argument("--json", action="store_true", help="emit one JSON object per file")
    args = parser.parse_args(argv)
    for path in args.transcripts:
        record = score_transcript(path)
        if args.json:
            print(json.dumps(record, sort_keys=True))
        else:
            mutation = record["first_mutation"]
            stop = (
                f"first mutation at line {mutation['line']} ({mutation['tool']})"
                if mutation
                else "no mutating action found (whole transcript counted)"
            )
            print(f"{path}: M1 = {record['m1_words_before_first_mutation']} words — {stop}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
