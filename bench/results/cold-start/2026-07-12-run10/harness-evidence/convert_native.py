#!/usr/bin/env python3
"""convert_native v3 (run-7 rebuild, semantics per run-6 manifest runner_notes).

Native Claude Code subagent JSONL -> the bench event-JSONL format that
bench/score_m1.py consumes:

    {"type": "user",        "content": "<user text>"}
    {"type": "text",        "content": "<assistant text>"}
    {"type": "tool_use",    "name": "<Tool>", "input": {...}}
    {"type": "tool_result", "content": "<text>"[, "is_error": true]}

v3 semantics (run-6):
- ``is_error`` carried through on tool_result events (score_m1's
  error-cancels-candidate rule needs it).
- user TEXT messages emitted as events (type "user") — includes any
  system-reminder / claudeMd content embedded in user content, since that is
  model-visible worker input.
- hook-injected model-visible worker content captured if present in the
  worker stream: attachment entries whose payload carries model-visible text
  (e.g. hook_success additionalContext) are emitted as user events prefixed
  with nothing (verbatim text). Non-model-visible bookkeeping attachments
  (deferred_tools_delta, skill_listing, agent_listing_delta, queue-operation,
  ai-title, last-prompt) are skipped.
- assistant thinking blocks are not events (not tool output, not text shown).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

SKIP_ATTACHMENTS = {
    "deferred_tools_delta",
    "skill_listing",
    "agent_listing_delta",
    "queue-operation",
    "ai-title",
    "last-prompt",
    "todo",
    "plan_mode",
}


def _text_of(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict):
                parts.append(str(block.get("text", "")))
            else:
                parts.append(str(block))
        return "\n".join(p for p in parts if p)
    return str(content)


def convert(path: Path):
    events = []
    for lineno, line in enumerate(path.open(encoding="utf-8"), 1):
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            print(f"warning: {path}:{lineno}: unparseable line skipped", file=sys.stderr)
            continue
        kind = entry.get("type")
        if kind == "user":
            content = entry.get("message", {}).get("content")
            if isinstance(content, str):
                events.append({"type": "user", "content": content})
                continue
            for block in content or []:
                if not isinstance(block, dict):
                    events.append({"type": "user", "content": str(block)})
                    continue
                btype = block.get("type")
                if btype == "tool_result":
                    ev = {"type": "tool_result", "content": _text_of(block.get("content", ""))}
                    if block.get("is_error") is True:
                        ev["is_error"] = True
                    events.append(ev)
                elif btype == "text":
                    events.append({"type": "user", "content": str(block.get("text", ""))})
        elif kind == "assistant":
            for block in entry.get("message", {}).get("content", []) or []:
                if not isinstance(block, dict):
                    continue
                btype = block.get("type")
                if btype == "text":
                    events.append({"type": "text", "content": str(block.get("text", ""))})
                elif btype == "tool_use":
                    events.append(
                        {
                            "type": "tool_use",
                            "name": str(block.get("name", "")),
                            "input": block.get("input") if isinstance(block.get("input"), dict) else {},
                        }
                    )
        elif kind == "attachment":
            att = entry.get("attachment", {})
            atype = att.get("type", "")
            if atype in SKIP_ATTACHMENTS:
                continue
            # Model-visible hook content: capture verbatim if any text payload.
            text = att.get("additionalContext") or att.get("content") or att.get("message") or ""
            text = _text_of(text)
            if text:
                events.append({"type": "user", "content": text})
        # system / progress / other bookkeeping kinds: skipped
    return events


def main():
    src = Path(sys.argv[1])
    dest = Path(sys.argv[2])
    events = convert(src)
    with dest.open("w", encoding="utf-8") as fh:
        for ev in events:
            fh.write(json.dumps(ev) + "\n")
    print(f"{src.name}: {len(events)} events -> {dest}")


if __name__ == "__main__":
    main()
