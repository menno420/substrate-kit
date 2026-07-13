"""Build ``dist/bootstrap.py`` from the readable ``src/engine`` tree.

This is the manifest->artifact step (the same shape as the host repo's
``build_pack.py`` — but that script is **inspiration only, not a trusted
reference**: it carries a Q-0105 "delete if unreliable" header, so this builder
owns its own discipline and a recursion test). It reads the engine modules in
dependency order, strips their intra-package imports, concatenates the bodies
into one stdlib-only file, and stamps ``KIT_VERSION`` into the header line so
every vendored copy self-identifies (founding plan §4.1). The old
``_ENGINE_MANIFEST`` source embedding was dropped at v1.0.0 (§3.4): the
``init --unpack`` it served never shipped, and it doubled every consumer's
vendored file for nothing.

Regenerate with::

    python3 substrate-kit/src/build_bootstrap.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

KIT_ROOT = Path(__file__).resolve().parents[1]
ENGINE_ROOT = KIT_ROOT / "src" / "engine"
TEMPLATES_ROOT = KIT_ROOT / "src" / "engine" / "templates"
DIST_PATH = KIT_ROOT / "dist" / "bootstrap.py"

# Dependency order: a module appears after everything it references.
MODULE_ORDER = (
    "lib/atomicio.py",
    "lib/config.py",
    "lib/state.py",
    "lib/guardrail.py",
    "lib/modes.py",
    # Before every control-band checker + currency.py: the kit-owned
    # control-plane grammar constants they all consume (EAP §6.8). Pure
    # stdlib-re, no engine references.
    "grammar.py",
    "interview/question_bank.py",
    "interview/stages.py",
    "interview/interview.py",
    "checks/check_docs.py",
    "checks/allowlist.py",
    "checks/check_session_log.py",
    "checks/check_namespace.py",
    "checks/check_seam_authority.py",
    "checks/check_orientation_budget.py",
    # Before hooks/stop_check.py (which references its heartbeat_relpaths) and
    # cli.py: only needs check_docs.Finding, defined above.
    "checks/check_status_current.py",
    # After check_status_current.py: reuses its heartbeat_relpaths + path
    # constants (ORDER 008 owner-action quality band).
    "checks/check_owner_actions.py",
    # After check_status_current.py: reuses its INBOX_RELPATH constant
    # (issue #36 report 2 inbox append-only gate).
    "checks/check_inbox_append.py",
    # After check_status_current.py: reuses its heartbeat_relpaths + path
    # constants (ORDER 007 order-claim hygiene advisory).
    "checks/check_claims.py",
    # After check_status_current.py: reuses its heartbeat_relpaths + path
    # constants (queue item 8 OWNER-ACTION ↔ CAPABILITIES cross-reference).
    "checks/check_capability_xref.py",
    # Only needs check_docs.Finding, defined above (EAP §6.5 setup-script
    # contract enforcer — the writer half is env-setup.sh.tmpl).
    "checks/check_setup_script.py",
    "ledger.py",
    "loop/kpis.py",
    "loop/reflections.py",
    "loop/friction.py",
    "loop/telemetry.py",
    # Before loop/handoff.py + hooks/session_start.py: both import its
    # shared handoff-lines composer / pointer writer (the B1 run-6
    # delivery-gap fix — one composer, two delivery surfaces).
    "loop/handoff_pointer.py",
    "loop/handoff.py",
    "loop/episodes.py",
    "loop/triggers.py",
    "loop/maintenance.py",
    "loop/review_seam.py",
    "economy/engine.py",
    "economy/harvest.py",
    "economy/simulator.py",
    "stances/stances.py",
    "skills/skills.py",
    "agents/agents.py",
    "hooks/stance_guard.py",
    "hooks/session_start.py",
    "hooks/post_edit.py",
    "hooks/stop_check.py",
    "hooks/settings.py",
    "render.py",
    "derive.py",
    "contextpack.py",
    # Before adopt.py (which plants the doc it renders), upgrade.py (the
    # derived-render refresh), and the slice-6 drift checker: the
    # seat-digest render surface imports only grammar/skills/config.
    "seatdigest.py",
    "adopt.py",
    # After adopt.py on purpose: the engagement gate scans the ADOPT_PLAN
    # destinations and keys off adopt's UNRENDERED banner marker.
    "checks/check_engagement.py",
    # After adopt.py (imports ADOPT_PLAN for the kit-planted path set) and
    # after skills/skills.py (scans the SKILLS bodies + grounds): the
    # grounded-skills slice-2 command-grounding advisory.
    "checks/check_skill_grounds.py",
    # After seatdigest.py (byte-compares the planted doc against its fresh
    # render): the grounded-skills slice-6 drift guard.
    "checks/check_seat_digest.py",
    # After adopt.py: reuses its enabler branch-expr generator + config
    # params (enabler-install-preflight, the branch-allowlist drift advisory).
    "checks/check_automerge_preflight.py",
    # After adopt.py: reuses its dist_version header parser (EAP §6.3
    # currency scanner — tree truth vs heartbeat self-report).
    "currency.py",
    # After currency.py: imports its GENERATED marker/stamp constants so the
    # generator and the CI-side format gate can never drift apart.
    "checks/check_adopters_current.py",
    "upgrade.py",
    "cli.py",
)
# Intra-package imports are dropped: in the concatenated file the referenced
# names already live in the same module namespace.
_INTRA_PKG_PREFIXES = ("from engine", "import engine", "from .")

# The version is stamped into the first header line (``bootstrap vX.Y.Z``) so
# a vendored single file self-identifies; ``upgrade`` parses it back out of an
# archived dist to name the backup.
_HEADER_TEMPLATE = '''"""substrate-kit bootstrap v{version} — GENERATED, DO NOT EDIT.

Single-file, stdlib-only. Regenerate from source with:
    python3 substrate-kit/src/build_bootstrap.py
Source of truth: substrate-kit/src/engine/. Edits here are overwritten.
"""'''


def _read(rel: str) -> str:
    """Return the text of an engine-relative source file."""
    return (ENGINE_ROOT / rel).read_text(encoding="utf-8")


def kit_version() -> str:
    """Return ``KIT_VERSION`` parsed from ``lib/config.py`` (the one home).

    Parsed textually rather than imported so the builder needs no sys.path
    setup and stays a plain script.
    """
    source = _read("lib/config.py")
    match = re.search(r'^KIT_VERSION = "([^"]+)"$', source, re.MULTILINE)
    if match is None:
        msg = "KIT_VERSION not found in src/engine/lib/config.py"
        raise ValueError(msg)
    return match.group(1)


def _triple_quote_toggles(line: str, active: str | None) -> str | None:
    """Track triple-quoted string state across a line; return the new state.

    ``active`` is the open triple-quote delimiter (double or single form) or
    None. Naive by design (counts delimiter occurrences; a line mixing both
    delimiter forms is not handled) — module docstrings and the embedded prose
    blocks this builder must survive are all well-formed.
    """
    if active is not None:
        return None if line.count(active) % 2 == 1 else active
    for delim in ('"""', "'''"):
        if line.count(delim) % 2 == 1:
            return delim
    return None


def _split_imports(source: str) -> tuple[list[str], list[str], list[str]]:
    """Split a module into (future imports, kept imports, body lines).

    Intra-package imports are dropped — in the concatenated file their names
    already live in the same namespace. A *parenthesized multi-line* intra-package
    import is dropped **whole**: its continuation lines must not leak into the body
    (that produced an ``IndentationError`` in the generated bootstrap). Lines
    inside triple-quoted strings are never treated as imports — a docstring
    sentence starting with ``from ...`` once got hoisted into the import block
    and broke the generated file's syntax.
    """
    future: list[str] = []
    imports: list[str] = []
    body: list[str] = []
    dropping_multiline = False
    in_string: str | None = None
    for line in source.splitlines():
        if in_string is not None:
            body.append(line)
            in_string = _triple_quote_toggles(line, in_string)
            continue
        if dropping_multiline:
            if ")" in line:
                dropping_multiline = False
            continue
        if line.startswith("from __future__"):
            future.append(line)
        elif any(line.startswith(p) for p in _INTRA_PKG_PREFIXES):
            if "(" in line and ")" not in line:
                dropping_multiline = True
            continue
        elif line.startswith(("import ", "from ")):
            imports.append(line)
        else:
            body.append(line)
            in_string = _triple_quote_toggles(line, None)
    return future, imports, body


def build() -> str:
    """Assemble the full text of ``dist/bootstrap.py``."""
    future: list[str] = []
    imports: list[str] = []
    body: list[str] = []

    for rel in MODULE_ORDER:
        source = _read(rel)
        mod_future, mod_imports, mod_body = _split_imports(source)
        for line in mod_future:
            if line not in future:
                future.append(line)
        for line in mod_imports:
            if line not in imports:
                imports.append(line)
        body.append(f"\n# --- engine/{rel} ---")
        body.extend(mod_body)

    lines: list[str] = [_HEADER_TEMPLATE.format(version=kit_version()), ""]
    lines.extend(future)
    lines.append("")
    lines.extend(sorted(imports))
    lines.extend(body)
    lines.append("")
    lines.append("_TEMPLATES = {")
    for tpath in sorted(TEMPLATES_ROOT.glob("*")):
        lines.append(f"    {tpath.name!r}: {tpath.read_text(encoding='utf-8')!r},")
    lines.append("}")
    lines.append("")
    lines.append('if __name__ == "__main__":')
    lines.append("    raise SystemExit(main())")
    return "\n".join(lines) + "\n"


def main() -> int:
    """Generate ``dist/bootstrap.py`` from ``src/engine``.

    The reported size is the real written BYTE count (``len`` of the UTF-8
    encoding), not ``len(content)`` — that counts *characters*, and the
    templates carry multi-byte glyphs (💡/⟲/📊/·/—), so the old print
    understated the file by ~3 KB (622084 chars vs 625066 bytes at v1.8.0;
    queued kit fix 2, re-confirmed on #160/#161). Writing the encoded bytes
    directly also pins the artifact against platform newline translation.
    """
    data = build().encode("utf-8")
    DIST_PATH.parent.mkdir(parents=True, exist_ok=True)
    DIST_PATH.write_bytes(data)
    sys.stdout.write(f"wrote {DIST_PATH} ({len(data)} bytes)\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
