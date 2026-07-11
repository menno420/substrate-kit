#!/usr/bin/env python3
"""Extract the fenced task prompt from a bench/tasks/<T>.md file.

The prompt is the text between the FIRST pair of lines that are exactly
`---`, with leading/trailing blank lines stripped (verified against the
run-6 committed transcripts: the worker's first user message equals this
extraction byte-for-byte).
"""
import sys
from pathlib import Path

lines = Path(sys.argv[1]).read_text(encoding="utf-8").split("\n")
fences = [i for i, l in enumerate(lines) if l.strip() == "---"]
if len(fences) < 2:
    sys.exit("no fenced block found")
block = lines[fences[0] + 1 : fences[1]]
while block and not block[0].strip():
    block.pop(0)
while block and not block[-1].strip():
    block.pop()
sys.stdout.write("\n".join(block))
