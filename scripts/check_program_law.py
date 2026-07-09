#!/usr/bin/env python3
"""check_program_law — the PL-register + planted-pointer checker (KL-2, plan §8.3.4).

Why + provenance: the program-law convention (founding plan §8, KF-6) ships
with its checker in the same PR — the drift-before-next-session failure mode.
Added 2026-07-09 (band KL-2). Reliability (PL-008): UNVERIFIED — confirm its
findings against ground truth a few times across sessions before trusting it;
**delete this if it proves unreliable over multiple sessions.**

What it enforces (exit 1 on any finding, 0 clean):

1. **Register grammar** — ``docs/program/rulings.md`` blocks are
   ``## [PL-NNN] <title>`` with required fields ``status`` (decided |
   superseded | retired), ``date`` (YYYY-MM-DD), ``provenance`` (non-empty —
   REQUIRED on every block), ``verdict``; a superseded block names its
   ``superseded-by``.
2. **Monotonic IDs** — PL-001..PL-N sequential, no gaps, no duplicates
   (append-only: next free number).
3. **Pointer sections cite, never copy** — the planted templates that must
   carry a "Program law" pointer section (CONSTITUTION.md.tmpl,
   collaboration-model.md.tmpl) each have one, citing the register path and
   at least one PL-ID; and no pointer section (templates or the kit's own
   planted copies) contains a ruling *body* — any 8-word run from a PL
   verdict found inside a pointer section is a copy, which is drift by
   construction (README.md § citation rule).

Repo-level tooling, not engine code: lives in scripts/, uses print, never
ships in dist/bootstrap.py.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import NamedTuple

REGISTER_RELPATH = "docs/program/rulings.md"
TEMPLATES_RELDIR = "src/engine/templates"
# Templates that MUST carry a "Program law" pointer section (plan §8.3.2).
REQUIRED_POINTER_TEMPLATES = ("CONSTITUTION.md.tmpl", "collaboration-model.md.tmpl")
# The kit's own planted copies (consumer #0): validated when they carry the section.
LOCAL_POINTER_DOCS = ("CONSTITUTION.md", "docs/collaboration-model.md")

# What a pointer section must cite.
REGISTER_CITE = "docs/program/rulings.md"
_PL_ID_RE = re.compile(r"\bPL-\d{3,}\b")

_HEADING_RE = re.compile(r"^## \[PL-(\d{3,})\] (.+)$")
# A heading that mentions PL- but doesn't match the grammar exactly.
_LOOSE_HEADING_RE = re.compile(r"^##+ .*PL-\d", re.IGNORECASE)
_FIELD_RE = re.compile(r"^- (status|date|supersedes|superseded-by|provenance|verdict|why|scope):\s*(.*)$")
_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_ALLOWED_STATUS = ("decided", "superseded", "retired")
_POINTER_HEADING_RE = re.compile(r"^#{2,4} .*program law", re.IGNORECASE)

# A verdict n-gram this long found inside a pointer section = a copied body.
NGRAM_WORDS = 8


class Finding(NamedTuple):
    path: str
    kind: str
    message: str


class Block(NamedTuple):
    number: int
    title: str
    fields: dict[str, str]
    line: int


def _normalize_words(text: str) -> list[str]:
    """Lowercase, strip markdown emphasis + punctuation, return the word list."""
    text = text.lower()
    text = re.sub(r"[`*_>#|]", " ", text)
    text = re.sub(r"[^\w\s-]", " ", text)
    return text.split()


def _ngrams(words: list[str], n: int) -> set[str]:
    return {" ".join(words[i : i + n]) for i in range(len(words) - n + 1)}


def parse_register(path: Path) -> tuple[list[Block], list[Finding]]:
    """Parse the PL register into blocks + grammar findings."""
    rel = REGISTER_RELPATH
    findings: list[Finding] = []
    if not path.exists():
        return [], [Finding(rel, "register", "missing — the program-law home must exist")]
    lines = path.read_text(encoding="utf-8").splitlines()

    blocks: list[Block] = []
    current: tuple[int, str, int] | None = None  # (number, title, line)
    fields: dict[str, str] = {}
    field_key: str | None = None
    in_comment = False

    def close() -> None:
        if current is not None:
            blocks.append(Block(current[0], current[1], dict(fields), current[2]))

    for lineno, raw in enumerate(lines, 1):
        stripped = raw.strip()
        if "<!--" in stripped:
            in_comment = "-->" not in stripped
            continue
        if in_comment:
            in_comment = "-->" not in stripped
            continue
        match = _HEADING_RE.match(raw)
        if match:
            close()
            current = (int(match.group(1)), match.group(2).strip(), lineno)
            fields = {}
            field_key = None
            continue
        if raw.startswith("## "):
            # A new non-PL section ends the current block.
            if _LOOSE_HEADING_RE.match(raw):
                findings.append(
                    Finding(rel, "grammar", f"L{lineno}: malformed PL heading `{stripped}` (want `## [PL-NNN] <title>`)"),
                )
            close()
            current = None
            fields = {}
            field_key = None
            continue
        if current is None:
            continue
        fmatch = _FIELD_RE.match(raw)
        if fmatch:
            field_key = fmatch.group(1)
            if field_key in fields:
                findings.append(
                    Finding(rel, "grammar", f"L{lineno}: [PL-{current[0]:03d}] duplicate field `{field_key}`"),
                )
            fields[field_key] = fmatch.group(2).strip()
        elif field_key and (raw.startswith("  ") or raw.startswith("\t")):
            # Continuation line of the previous field.
            fields[field_key] = (fields[field_key] + " " + stripped).strip()
        elif stripped:
            field_key = None
    close()

    if not blocks:
        findings.append(Finding(rel, "register", "no [PL-NNN] blocks found"))
    return blocks, findings


def check_blocks(blocks: list[Block]) -> list[Finding]:
    """Required fields + status/date validity + monotonic sequential IDs."""
    rel = REGISTER_RELPATH
    findings: list[Finding] = []
    for block in blocks:
        pl = f"[PL-{block.number:03d}]"
        for required in ("status", "date", "provenance", "verdict"):
            value = block.fields.get(required, "")
            if not value:
                findings.append(
                    Finding(rel, "field", f"L{block.line}: {pl} missing required field `{required}`"),
                )
        status = block.fields.get("status", "")
        if status and status not in _ALLOWED_STATUS:
            findings.append(
                Finding(rel, "field", f"L{block.line}: {pl} invalid status `{status}` (allowed: {', '.join(_ALLOWED_STATUS)})"),
            )
        if status == "superseded" and not block.fields.get("superseded-by"):
            findings.append(
                Finding(rel, "field", f"L{block.line}: {pl} superseded without `superseded-by`"),
            )
        date = block.fields.get("date", "")
        if date and not _DATE_RE.match(date):
            findings.append(
                Finding(rel, "field", f"L{block.line}: {pl} invalid date `{date}` (want YYYY-MM-DD)"),
            )

    numbers = [b.number for b in blocks]
    seen: set[int] = set()
    for block in blocks:
        if block.number in seen:
            findings.append(
                Finding(rel, "ids", f"L{block.line}: duplicate id [PL-{block.number:03d}]"),
            )
        seen.add(block.number)
    if numbers:
        expected = list(range(1, max(numbers) + 1))
        missing = sorted(set(expected) - set(numbers))
        if missing:
            gaps = ", ".join(f"PL-{n:03d}" for n in missing)
            findings.append(Finding(rel, "ids", f"id gap(s): {gaps} (append-only: next free number, no gaps)"))
        if numbers != sorted(numbers):
            findings.append(Finding(rel, "ids", "blocks out of order (register is append-only, ascending)"))
    return findings


def _pointer_section(text: str) -> str | None:
    """Extract the 'Program law' section body, or None when absent."""
    lines = text.splitlines()
    start: int | None = None
    level = 0
    for i, line in enumerate(lines):
        if _POINTER_HEADING_RE.match(line):
            start = i
            level = len(line) - len(line.lstrip("#"))
            break
    if start is None:
        return None
    body: list[str] = []
    for line in lines[start + 1 :]:
        if line.startswith("#") and (len(line) - len(line.lstrip("#"))) <= level:
            break
        body.append(line)
    return "\n".join(body)


def check_pointers(root: Path, blocks: list[Block]) -> list[Finding]:
    """Pointer sections exist where required, cite the register, copy no bodies."""
    findings: list[Finding] = []
    verdict_grams: set[str] = set()
    for block in blocks:
        words = _normalize_words(block.fields.get("verdict", ""))
        verdict_grams |= _ngrams(words, NGRAM_WORDS)

    templates_dir = root / TEMPLATES_RELDIR
    candidates: list[tuple[str, Path, bool]] = []  # (rel, path, required)
    for name in REQUIRED_POINTER_TEMPLATES:
        candidates.append((f"{TEMPLATES_RELDIR}/{name}", templates_dir / name, True))
    if templates_dir.exists():
        for tmpl in sorted(templates_dir.glob("*.tmpl")):
            if tmpl.name not in REQUIRED_POINTER_TEMPLATES:
                candidates.append((f"{TEMPLATES_RELDIR}/{tmpl.name}", tmpl, False))
    for rel in LOCAL_POINTER_DOCS:
        candidates.append((rel, root / rel, False))

    for rel, path, required in candidates:
        if not path.exists():
            if required:
                findings.append(Finding(rel, "pointer", "missing template (must carry the Program law pointer section)"))
            continue
        section = _pointer_section(path.read_text(encoding="utf-8"))
        if section is None:
            if required:
                findings.append(Finding(rel, "pointer", "no `Program law` pointer section (plan §8.3.2: planted templates cite the home)"))
            continue
        if REGISTER_CITE not in section:
            findings.append(Finding(rel, "pointer", f"Program law section does not cite the register path `{REGISTER_CITE}`"))
        if not _PL_ID_RE.search(section):
            findings.append(Finding(rel, "pointer", "Program law section cites no PL-ID"))
        if verdict_grams:
            section_grams = _ngrams(_normalize_words(section), NGRAM_WORDS)
            copied = verdict_grams & section_grams
            if copied:
                sample = sorted(copied)[0]
                findings.append(
                    Finding(rel, "body-copy", f"Program law section copies a ruling body (`{sample} …`) — cite the PL-ID, never the text"),
                )
    return findings


def run_checks(root: Path) -> list[Finding]:
    blocks, findings = parse_register(root / REGISTER_RELPATH)
    findings += check_blocks(blocks)
    findings += check_pointers(root, blocks)
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="repo root (default: this script's repo)",
    )
    args = parser.parse_args(argv)
    findings = run_checks(args.root)
    if findings:
        print(f"check_program_law: {len(findings)} finding(s)")
        for f in findings:
            print(f"  {f.path} [{f.kind}] {f.message}")
        return 1
    print("check_program_law: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
