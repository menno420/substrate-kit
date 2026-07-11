"""Render the project's content docs from templates + filled interview slots.

Templates use ``${slot_name}`` placeholders (``string.Template``). A slot the
interview has filled substitutes in; an unfilled slot is left as ``${slot_name}``
and reported — so a half-onboarded project's gaps stay visible rather than going
silently blank. Templates ship embedded in the bootstrap (the generated
``_TEMPLATES`` dict) and, in the source/pip layouts, under
``engine/templates/`` (inside the package so a wheel ships them).
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from engine.lib.config import KIT_VERSION

_PLACEHOLDER_RE = re.compile(r"\$\{([a-zA-Z_][a-zA-Z0-9_]*)\}")

# Markdown code carriers, stripped by find_placeholders_outside_code before
# scanning (the #148/#150 poison: a status heartbeat's `${VAR}` inside
# backticks read as an unfilled interview slot and held strict RED). The
# same proven pair check_session_log uses for its `[[fill:]]` counting —
# fences first (a fence line may contain no backtick-span boundary), then
# inline spans.
_MD_CODE_SPAN_RE = re.compile(r"`[^`\n]*`")
_MD_CODE_FENCE_RE = re.compile(r"^```.*?^```", re.MULTILINE | re.DOTALL)

# Context keys the ENGINE computes and injects itself — never interview
# slots. The template/bank coherence guard (tests/test_render.py) exempts
# exactly this set, so a template may reference them without a bank question
# existing. Grows deliberately: every addition must be injected by
# build_context (or a caller) unconditionally, or templates strand unfilled.
ENGINE_CONTEXT_KEYS = frozenset({"kit_version"})


def find_placeholders(text: str) -> set[str]:
    """Return the set of ``${name}`` placeholders remaining in ``text``."""
    return set(_PLACEHOLDER_RE.findall(text))


def find_placeholders_outside_code(text: str) -> set[str]:
    """Return the ``${name}`` placeholders outside code spans / fenced blocks.

    The engagement gate's unrendered-slot scan reads host-maintained planted
    docs (a control/status.md heartbeat above all), where a literal
    ``${VAR}`` inside backticks or a fenced block is *prose about* a token,
    never an unfilled interview slot — kit PR #148 poisoned main with exactly
    that (a status code span), redding every subsequent full-lane PR until a
    hand-fix (#150). Fenced blocks are stripped first, then inline spans —
    the same order :mod:`engine.checks.check_session_log` uses for its
    ``[[fill:]]`` counting. The full-text :func:`find_placeholders` stays the
    writer-side truth (banner placement, render coverage): a template slot is
    real wherever it sits, including inside backticks.
    """
    return find_placeholders(_MD_CODE_SPAN_RE.sub("", _MD_CODE_FENCE_RE.sub("", text)))


def render(text: str, context: dict[str, str]) -> str:
    """Substitute ``${slot}`` placeholders from ``context`` (unfilled left as-is).

    Only the braced ``${name}`` form is a placeholder — the *same* form
    ``find_placeholders`` reports, so render and the "unfilled slots stay
    visible" safety net can never disagree. Deliberately NOT
    ``string.Template.safe_substitute``: that also collapses ``$$`` → ``$`` and
    substitutes unbraced ``$word``, silently mangling host-authored ``$``
    content (shell ``$$``/``$1``, ``$5`` prices, ``$$LaTeX$$``) on the routine
    ``render --live`` in-place fill — and turning an escaped ``$${VERSION}``
    into a live-looking ``${VERSION}`` that then reports as an unfilled slot.
    A regex sub over the braced form leaves every other ``$`` byte untouched.
    """
    return _PLACEHOLDER_RE.sub(
        lambda m: context[m.group(1)] if m.group(1) in context else m.group(0),
        text,
    )


def build_context(state: dict[str, Any]) -> dict[str, str]:
    """Build the substitution context from a state document's filled slots.

    ``kit_version`` is always present (never a slot): it is the running
    engine's own :data:`KIT_VERSION`, injected here — the single point every
    render path (adopt / upgrade / ``render --live``) flows through — so the
    ``kit:`` self-report line in the planted ``control/status.md`` seed
    (inbox ORDER 003, adopter-visibility band) renders with the real version
    instead of stranding as an unfilled placeholder. A slot named
    ``kit_version`` (none exists) would win over the constant by design.
    (Top-level import on purpose: ``lib/config.py`` precedes ``render.py``
    in the dist's MODULE_ORDER, so the intra-package import strips cleanly;
    a function-body ``from engine...`` would survive into the single file
    and fail at dist runtime.)
    """
    values = state.get("slot_values", {})
    context = {slot: str(entry.get("value", "")) for slot, entry in values.items()}
    context.setdefault("kit_version", KIT_VERSION)
    return context


def load_templates() -> dict[str, str]:
    """Return ``{filename: text}`` for every template (embedded or packaged).

    The single-file bootstrap embeds them as ``_TEMPLATES``; the source/pip
    layouts read ``engine/templates/`` (INSIDE the package, so a wheel ships
    them — they once lived a level up and a pip install silently had none).
    An empty template set is a hard error, never a silent no-op render.
    """
    embedded = globals().get("_TEMPLATES")
    if embedded is not None:
        return dict(embedded)
    root = Path(__file__).resolve().parent / "templates"
    templates = {
        p.name: p.read_text(encoding="utf-8") for p in sorted(root.glob("*.tmpl"))
    }
    if not templates:
        msg = f"no templates found at {root} — broken install"
        raise FileNotFoundError(msg)
    return templates
