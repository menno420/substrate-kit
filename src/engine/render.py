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

from engine.grammar import DEFAULT_SESSIONS_DIRNAME
from engine.lib.config import KIT_VERSION, owner_context_declaration
from engine.lib.profiles import profile_for_config
from engine.skills.skills import skills_index_table

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
ENGINE_CONTEXT_KEYS = frozenset(
    {
        "agreement_home",
        "agreement_boot_tail",
        "boot_read_path",
        "kit_version",
        "sessions_dir",
        "owner_context_pointer",
        "skills_index",
    },
)


def agreement_home(root: Path, *, include_claude: bool = False) -> str:
    """Return the boot pointer to the target repo's working agreement.

    ``.claude/CLAUDE.md`` only when it is actually live in ``root`` (or the
    current adopt run is about to write it, via ``include_claude``);
    otherwise the root ``CONSTITUTION.md``, which ``ADOPT_PLAN`` always
    plants. Engine-computed (an :data:`ENGINE_CONTEXT_KEYS` member, like
    ``kit_version``) because no interview answer can know what the run
    installs: the planted ``docs/AGENT_ORIENTATION.md`` used to hardcode
    ``.claude/CLAUDE.md`` while the default adopt deliberately only STAGES
    CLAUDE.md — a dead boot pointer verified live in 3/3 adopters
    (inbox ORDER 015, 2026-07-12).
    """
    if include_claude or (root / ".claude" / "CLAUDE.md").is_file():
        return ".claude/CLAUDE.md"
    return "CONSTITUTION.md"


# The boot list the planted working agreement carries, per adoption shape.
# Kept as literal blocks rather than composed from the plan: this is PROSE a
# cold session reads first, and prose assembled from a path list reads like a
# manifest. The default block is byte-identical to the pre-profile template.
_BOOT_READ_PATH_DEFAULT = """\
Read in this order at session start. **This is the one list** — the task router
at `docs/AGENT_ORIENTATION.md` points here rather than repeating it, so a boot
set can never exist in two places that disagree.

1. This file — the working agreement + autonomy rails.
2. `docs/current-state.md` — the living status ledger. Source and merged PRs
   always win over it.
3. `docs/CAPABILITIES.md` — verified session capabilities and walls. THE
   DISCOVERY RULE lives there: append what you verify, never a limitation.

Then `docs/AGENT_ORIENTATION.md` when a task needs a route into the deeper
docs — it is a router, not boot reading."""

_BOOT_READ_PATH_SPARSE = """\
Read in this order at session start. **This is the one list**: a router that
repeated it could disagree with it, so nothing else in this repository carries
a boot order.

1. This file — the working agreement + autonomy rails.

This install's adoption profile plants no generic doc set, so the list above is
the whole kit-supplied boot path. Add this repository's own boot docs here as
they are written — numbered, in reading order, each with one line saying what
it gives you. Every path named here must resolve on disk (`check_boot_path`
asserts it), which is exactly why the kit does not seed the list with documents
it did not plant."""


def boot_read_path(config: Any | None = None) -> str:
    """Return the working agreement's boot list for one install's shape.

    The kit's own measured defect, one level up: on 2026-08-06, 0 of 11 adopter
    trees had a boot path that resolved end to end, because the pointer and the
    documents it named were maintained in different places. Planting a fixed
    three-document list into a shape that plants none of those three would
    reproduce that defect deliberately — a cold session told to read two files
    that were never going to exist.

    So the list follows the shape. Engine-computed (an
    :data:`ENGINE_CONTEXT_KEYS` member) for the ``agreement_home`` reason: no
    interview answer can know what the profile planted.
    """
    if config is None:
        return _BOOT_READ_PATH_DEFAULT
    profile = profile_for_config(config)
    if profile.omits("docs/current-state.md"):
        return _BOOT_READ_PATH_SPARSE
    return _BOOT_READ_PATH_DEFAULT


# The staged working agreement's orientation tail, per adoption shape. Same
# rule as _BOOT_READ_PATH_*: the default block is byte-identical to the
# pre-profile template, and the sparse block names no document the shape does
# not plant while keeping every habit the kit is actually asking for.
_AGREEMENT_BOOT_TAIL_DEFAULT = """\
3. `docs/current-state.md` — what is true right now.

That is the whole boot set **for acting** — a floor, not a ceiling. Everything
else is routed, **not front-loaded** (reading every planted doc up front buys
ceremony, not context — measured):
open `docs/AGENT_ORIENTATION.md` when a task needs its reading route,
`docs/SKILLS.md` (the skill index) **before improvising a procedure for a
recurring action**, and
`docs/CAPABILITIES.md` (the verified can/cannot ledger) **before declaring
any wall or missing credential** — its discovery rule: check the file →
check the env → attempt once + capture the exact error → append the finding
same session — and `docs/ROUTINES.md` (the wake-chain/trigger doctrine)
**before arming, deleting, or auditing any scheduled trigger/routine**."""

_AGREEMENT_BOOT_TAIL_SPARSE = """\
3. This install's adoption profile plants no generic doc set, so items 0-2
   are the whole kit-supplied boot set. Add this repository's own boot
   documents here as they are written — numbered, in reading order, one line
   each saying what the document gives you.

That is a floor, not a ceiling, and the routing rule holds whatever this
repository ends up calling its documents: read what the task needs when the
task needs it, rather than front-loading every document at boot (reading
everything up front buys ceremony, not context — measured). Two habits the kit
asks for by name, wherever this repository files them: consult the recurring-
action index **before improvising a procedure**, and consult the verified
capability ledger **before declaring any wall or missing credential** — its
discovery rule is check the file → check the env → attempt once + capture the
exact error → append the finding same session."""


def agreement_boot_tail(config: Any | None = None) -> str:
    """Return the staged agreement's orientation tail for one install's shape.

    The twin of :func:`boot_read_path`, for the OTHER document that can become
    the live working agreement (``.claude/CLAUDE.md`` under ``include_claude``,
    which is what :func:`agreement_home` then points every cold session at). A
    shape that plants no generic doc set must not open its live agreement by
    telling the session to read four documents that do not exist — the same
    dead-pointer class, one file over.
    """
    if config is None:
        return _AGREEMENT_BOOT_TAIL_DEFAULT
    if profile_for_config(config).omits("docs/current-state.md"):
        return _AGREEMENT_BOOT_TAIL_SPARSE
    return _AGREEMENT_BOOT_TAIL_DEFAULT


def owner_context_pointer(config: Any | None = None) -> str:
    """Return the planted owner profile's canonical-context pointer, or ``""``.

    An estate of N repositories that each plant a self-contained owner profile
    gets N independent copies of the same two answers, and the copies drift.
    The fix is a POINTER: one repository holds the broader working profile and
    every other names it, keeping only the slots that are genuinely local.

    The kit ships the sentence, never its destination — ``owner_context``'s
    ``canonical`` is a free string the host writes (a URL, a sibling path, a
    document path) and this function only quotes it. Nothing here knows or may
    ever know which repository an estate designates.

    Empty — the default, and every install that declares nothing — renders the
    planted doc byte-identically to the pre-key output: the template's
    substitution site sits at the end of an existing line, so an empty value
    adds no line, no blank, and no heading. Engine-computed rather than an
    interview slot for the ``agreement_home`` reason: no answer can know what
    the *config* declares, and an uninjected slot would strand as
    ``${owner_context_pointer}`` under the UNRENDERED banner.
    """
    if config is None:
        return ""
    canonical, label = owner_context_declaration(config)
    if not canonical:
        return ""
    home = f"{label} ({canonical})" if label else canonical
    return (
        "\n>\n"
        f"> **Canonical owner context:** {home}. That is the broader working "
        "profile;\n"
        "> this file carries only what is specific to THIS repository, so the "
        "two\n"
        "> never drift apart by being written twice."
    )


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


def build_context(
    state: dict[str, Any],
    config: Any | None = None,
) -> dict[str, str]:
    """Build the substitution context from a state document's filled slots.

    ``kit_version`` is always present (never a slot): it is the running
    engine's own :data:`KIT_VERSION`, injected here — the single point every
    render path (adopt / upgrade / ``render --live``) flows through — so the
    ``kit:`` self-report line in the planted ``control/status.md`` seed
    (inbox ORDER 003, adopter-visibility band) renders with the real version
    instead of stranding as an unfilled placeholder. A slot named
    ``kit_version`` (none exists) would win over the constant by design.
    ``skills_index`` follows the same shape (grounded-skills plan §2, slice
    1): the planted ``docs/SKILLS.md`` table is rendered FROM the kit's
    ``SKILLS`` list — the same source that emits the skills — so the index
    can never hand-drift from what the kit installs; injected here so every
    render path fills it, and a same-named slot (none exists) would win.
    (Top-level imports on purpose: ``lib/config.py`` and ``skills/skills.py``
    both precede ``render.py`` in the dist's MODULE_ORDER, so the
    intra-package imports strip cleanly; a function-body ``from engine...``
    would survive into the single file and fail at dist runtime.)
    """
    values = state.get("slot_values", {})
    context = {slot: str(entry.get("value", "")) for slot, entry in values.items()}
    context.setdefault("kit_version", KIT_VERSION)
    # The slot context is passed INTO the table (slice 2): grounds-column
    # slot references (e.g. a ``${verify_command}`` ground) fill from the
    # project's own answers; render() cannot fill them later because the
    # table is itself a substitution VALUE — re.sub never rescans
    # replacements, so anything unfilled here would strand as literal
    # ``${...}`` and re-banner the planted index (skills._ground_cell docs).
    context.setdefault("skills_index", skills_index_table(context))
    # ``owner_context_pointer`` is injected on EVERY path, including the
    # config-less ones, where it is "" — the docstring rule above (an
    # engine key not injected unconditionally strands templates unfilled)
    # is why this is a default-empty injection rather than a caller
    # setdefault like ``agreement_home``.
    context.setdefault("owner_context_pointer", owner_context_pointer(config))
    context.setdefault("boot_read_path", boot_read_path(config))
    context.setdefault("agreement_boot_tail", agreement_boot_tail(config))
    # The card directory is CONFIG, not an interview answer, and planted
    # prose names it. Injected unconditionally (the historical default when
    # no config is supplied) so no template can strand it.
    context.setdefault(
        "sessions_dir",
        getattr(config, "sessions_dir", None) or DEFAULT_SESSIONS_DIRNAME,
    )
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
