"""The residue-surface coverage pin (the #424 card's filed 💡).

Every ``[[fill:]]``-writing drafter in the engine plants *hint text* that a
session is meant to wholesale-replace. The KL-5 residue guard fingerprints
those hints so marker-stripping shams read as residue — but the guard only
covers hints someone remembered to register: the S2 evidence hints sat
unguarded for two days (#424) because the drafter injected them outside the
template extraction, and nothing noticed. This pin makes the coverage
mechanical:

1. **Discover** every fill-slot *constructor* in the engine by AST — a
   function returning an f-string that references the fill token
   (``DRAFT_FILL_TOKEN`` / ``RESIDUE_FILL_TOKEN``) or embeds a literal
   ``[[fill:`` opener. Known today: ``loop.handoff._fill`` and
   ``loop.archive._judgment_slot``.
2. **Enumerate** every call site of every constructor and statically
   resolve the hint argument (string literal, module-level constant, or an
   ``x or "fallback"`` default).
3. **Assert** each resolved hint is either **residue-guarded** (a body in a
   registry actually probed via ``engine.lib.residue.probe_residue`` — and
   the fingerprint demonstrably fires) or an explicit **settled-empty**
   entry in :data:`engine.lib.residue.RESIDUE_SETTLED_EMPTY` with a reason.
   A hint in neither place fails with a message naming the surface — a
   future drafted surface cannot ship unguarded silently.

The pin also fails on an *inline* fill-token f-string outside a constructor
(route slot writes through a constructor so their hints stay enumerable)
and on a stale settled-empty entry no call site uses anymore.
"""

from __future__ import annotations

import ast
import importlib
from pathlib import Path

import engine
from engine.lib.residue import (
    CARD_GUARDED_HINTS,
    RESIDUE_SETTLED_EMPTY,
    probe_residue,
)
from engine.loop.archive import ARCHIVE_EVIDENCE_HINTS

_ENGINE_ROOT = Path(engine.__file__).resolve().parent

# The fill-token constant names a constructor may reference in its f-string.
_TOKEN_NAMES = {"DRAFT_FILL_TOKEN", "RESIDUE_FILL_TOKEN"}
# Prose legitimately *mentions* the closed token (`[[fill:]]` in checker
# messages); only an OPEN `[[fill:` remaining after those mentions are
# removed marks an f-string as a slot writer.
_CLOSED_MENTION = "[[fill:]]"
_OPEN_TOKEN = "[[fill:"

# The guarded registries the engine probes today. A NEW drafted surface
# adds its ``(name, body)`` registry here *and* wires it through
# ``probe_residue`` in a checker/probe — the failure message below walks
# you through it.
_GUARDED_REGISTRIES: tuple[tuple[str, tuple[tuple[str, str], ...]], ...] = (
    ("engine.lib.residue.CARD_GUARDED_HINTS", CARD_GUARDED_HINTS),
    ("engine.loop.archive.ARCHIVE_EVIDENCE_HINTS", ARCHIVE_EVIDENCE_HINTS),
)


def _module_name(path: Path) -> str:
    rel = path.resolve().relative_to(_ENGINE_ROOT.parent)
    parts = rel.with_suffix("").parts
    if parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join(parts)


def _joinedstr_writes_slot(node: ast.JoinedStr) -> bool:
    """True when this f-string constructs a fill slot (not a prose mention)."""
    for value in node.values:
        if isinstance(value, ast.FormattedValue):
            inner = value.value
            if isinstance(inner, ast.Name) and inner.id in _TOKEN_NAMES:
                return True
        elif isinstance(value, ast.Constant) and isinstance(value.value, str):
            if _OPEN_TOKEN in value.value.replace(_CLOSED_MENTION, ""):
                return True
    return False


def _iter_engine_sources():
    for path in sorted(_ENGINE_ROOT.rglob("*.py")):
        yield path, ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def _find_constructors() -> dict[str, list[tuple[Path, str]]]:
    """Map constructor function name -> [(file, module)] defining it.

    A constructor is a function whose body contains a slot-writing f-string.
    """
    constructors: dict[str, list[tuple[Path, str]]] = {}
    for path, tree in _iter_engine_sources():
        module = _module_name(path)
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if any(
                    isinstance(sub, ast.JoinedStr) and _joinedstr_writes_slot(sub)
                    for sub in ast.walk(node)
                ):
                    constructors.setdefault(node.name, []).append((path, module))
    return constructors


def _resolve_hint(node: ast.expr, module: str) -> list[str] | None:
    """Statically resolve a hint argument to its possible string values.

    Returns ``None`` for a shape the pin cannot resolve (the caller fails
    with a helpful message). A ``x or "fallback"`` BoolOp resolves to its
    resolvable operands; purely dynamic operands (locals/params — host
    config data) contribute nothing and are acceptable only because the
    fallback literal still gets pinned.
    """
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return [node.value]
    if isinstance(node, ast.Name):
        mod = importlib.import_module(module)
        value = getattr(mod, node.id, None)
        return [value] if isinstance(value, str) else None
    if isinstance(node, ast.BoolOp) and isinstance(node.op, ast.Or):
        resolved: list[str] = []
        for operand in node.values:
            got = _resolve_hint(operand, module)
            if got:
                resolved.extend(got)
        return resolved or None
    return None


def _constructor_call_sites() -> list[tuple[Path, int, str, ast.Call]]:
    """Every ``(file, line, module, call)`` invoking a discovered constructor."""
    names = set(_find_constructors())
    sites: list[tuple[Path, int, str, ast.Call]] = []
    for path, tree in _iter_engine_sources():
        module = _module_name(path)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func = node.func
                called = (
                    func.id
                    if isinstance(func, ast.Name)
                    else func.attr if isinstance(func, ast.Attribute) else None
                )
                if called in names:
                    sites.append((path, node.lineno, module, node))
    return sites


def _known_hint_values() -> tuple[set[str], set[str]]:
    guarded = {body for _, registry in _GUARDED_REGISTRIES for _, body in registry}
    settled = {hint for _, hint, _ in RESIDUE_SETTLED_EMPTY}
    return guarded, settled


def test_constructor_discovery_sees_the_known_drafters():
    # The discovery pass itself is load-bearing: if the AST heuristic ever
    # goes blind, every downstream assertion trivially passes. Pin the two
    # known constructors so blindness reads as a failure, not a pass.
    constructors = _find_constructors()
    assert "_fill" in constructors, "loop.handoff._fill not discovered"
    assert "_judgment_slot" in constructors, "loop.archive._judgment_slot not discovered"


def test_every_drafted_hint_is_guarded_or_settled_empty():
    guarded, settled = _known_hint_values()
    problems: list[str] = []
    seen_values: set[str] = set()
    for path, lineno, module, call in _constructor_call_sites():
        where = f"{path.relative_to(_ENGINE_ROOT.parent)}:{lineno}"
        if not call.args:
            problems.append(f"{where}: constructor call with no hint argument")
            continue
        resolved = _resolve_hint(call.args[0], module)
        if resolved is None:
            problems.append(
                f"{where}: hint argument is not statically resolvable — use a "
                "string literal or a module-level constant so the coverage "
                "pin can enumerate the drafted surface",
            )
            continue
        for hint in resolved:
            seen_values.add(hint)
            if hint in guarded or hint in settled:
                continue
            problems.append(
                f"{where}: drafted hint {hint!r} is UNGUARDED — either add it "
                "to a (name, body) registry probed via engine.lib.residue."
                "probe_residue (and list that registry in _GUARDED_REGISTRIES "
                "here), or add an explicit (name, hint, reason) entry to "
                "engine.lib.residue.RESIDUE_SETTLED_EMPTY. A drafted surface "
                "must never ship silently unguarded (#424).",
            )
    # Stale settled-empty entries: a registry line whose hint no call site
    # writes anymore is dead weight that hides the next real hole.
    for name, hint, _reason in RESIDUE_SETTLED_EMPTY:
        if hint not in seen_values:
            problems.append(
                f"RESIDUE_SETTLED_EMPTY entry {name!r} ({hint!r}) matches no "
                "constructor call site — remove the stale entry",
            )
    assert not problems, "\n".join(problems)


def test_no_inline_fill_slot_construction_outside_constructors():
    # A slot write that bypasses a constructor is invisible to the call-site
    # enumeration above — hold the line: fill-slot f-strings live inside
    # constructor functions only.
    constructors = _find_constructors()
    constructor_files = {path for sites in constructors.values() for path, _ in sites}
    offenders: list[str] = []
    for path, tree in _iter_engine_sources():
        # Collect the constructor function nodes in this file.
        allowed_spans: list[tuple[int, int]] = []
        for node in ast.walk(tree):
            if (
                isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                and node.name in constructors
                and path in constructor_files
            ):
                allowed_spans.append((node.lineno, node.end_lineno or node.lineno))
        for node in ast.walk(tree):
            if isinstance(node, ast.JoinedStr) and _joinedstr_writes_slot(node):
                if not any(a <= node.lineno <= b for a, b in allowed_spans):
                    offenders.append(
                        f"{path.relative_to(_ENGINE_ROOT.parent)}:{node.lineno}: "
                        "inline fill-slot f-string — route it through a "
                        "constructor function so the coverage pin can "
                        "enumerate its hint",
                    )
    assert not offenders, "\n".join(offenders)


def test_guarded_registries_actually_fingerprint():
    # "Guarded" must mean the probe FIRES on a marker-stripped hint, not
    # just that the body sits in a list: probe each registry body bare and
    # expect its name guilty.
    for registry_name, registry in _GUARDED_REGISTRIES:
        for name, body in registry:
            guilty = probe_residue(f"prefix text {body} suffix text", [(name, body)])
            assert guilty == [name], (
                f"{registry_name} entry {name!r}: probe_residue did not "
                "fingerprint its body — the registry is listed but not "
                "actually guarding"
            )


def test_settled_empty_entries_carry_reasons():
    for name, hint, reason in RESIDUE_SETTLED_EMPTY:
        assert name.strip() and hint.strip(), "settled-empty entry missing name/hint"
        assert len(reason.strip()) >= 20, (
            f"settled-empty entry {name!r} needs a real reason — the registry "
            "documents WHY a hint is deliberately unguarded"
        )
