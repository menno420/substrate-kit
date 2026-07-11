"""Pull-visible handoff pointer — the B1 run-6 delivery-gap fix.

Bench run-6 (PR #201, report §5) proved the #165 SessionStart handoff-push's
delivery assumption false at the orchestrator→worker harness seam: the push
fired at every ON boot but reached the measured delegated worker in **0/3**
— the seam does not forward SessionStart context, and SessionStart does not
re-fire for subagents. The signal never reached the session that acts.

What the workers *did* touch, unprompted and early, was the working tree:
``git status`` / ``ls`` / ``find`` ran in 4 of the 6 measured sessions, and
run-6's one acknowledgment-adjacent event was the ON-T2 worker noticing
untracked paths in its own ``git status``. So the kit now delivers the same
handoff content through that surface: a lean ``HANDOFF.md`` at repo root,
regenerated at every session boot (SessionStart hook / ``session-start``)
and refreshed by the ``ensure_draft`` seam (Stop hook, ``session-close``,
``draft``), carrying exactly the push's handoff section — newest session
card path + status + unresolved slot count + the previous session's resolved
"next session should know" pointer.

Design decisions (decide-and-flag):

- **Untracked by design, deliberately NOT gitignored.** A gitignored file is
  invisible in ``git status`` — the one surface with observed worker
  acknowledgment. Untracked-at-root rides both ``git status`` (shows it) and
  plain ``ls`` (a dot-dir like ``.sessions/`` does not). The file's own
  header says never to commit or edit it.
- **Marker-guarded ownership.** The writer only ever creates, overwrites, or
  deletes a file carrying ``HANDOFF_POINTER_MARKER`` — a host-owned
  ``HANDOFF.md`` is never touched.
- **One composer, two surfaces.** ``handoff_lines`` feeds both the
  orientation push (``session_start._ori_handoff``) and this file, so the
  pushed and pulled text can never drift apart.
- **Fail-open by contract**, like every hook seam: writing the pointer can
  never crash a session start or stop.
"""

from __future__ import annotations

from pathlib import Path

from engine.checks.check_session_log import (
    DRAFT_FILL_TOKEN,
    latest_session_log,
    status_in_progress,
    unresolved_fill_count,
)
from engine.lib.atomicio import atomic_write_text
from engine.lib.config import Config

# The pointer file's repo-root filename — a program-wide constant (like the
# `do-not-automerge` label), not config: every adopter's cold session should
# find the same name in the same place.
HANDOFF_POINTER_FILENAME = "HANDOFF.md"
# Ownership marker: the writer only creates/overwrites/deletes a file that
# carries this line — a host-owned HANDOFF.md is never touched.
HANDOFF_POINTER_MARKER = "<!-- substrate:handoff-pointer -->"
# Cap on the handoff-pointer excerpt — the pointer must stay terse (the B1
# M1 lesson: ON already pays a footprint premium; a fat artifact makes the
# regression worse, not better).
HANDOFF_EXCERPT_CAP = 300
# The drafted close-out's handoff field (engine.loop.handoff draft text).
HANDOFF_NEEDLE = "next session should know"
# Auto-derived trail (B1 run-8 content-gap fix): when the newest card's
# pointer is still an unresolved draft slot, the pointer surfaces the card's
# own auto-collected evidence bullets instead of pointing at a skeleton.
# These prefixes are the draft's evidence-line shapes (engine.loop.handoff
# ``_evidence_lines``) — nothing else in a card matches them.
_TRAIL_PREFIXES = (
    "- code touched",
    "- tests touched",
    "- docs touched",
    "- sessions touched",
    "- other touched",
    "- git:",
    "- commits this session",
    "- previous session's pointer:",
)
# Caps keep the trail inside the pointer's lean-budget (the ~113-word push
# footprint the bench pins): at most this many lines, each truncated.
_TRAIL_LINE_CAP = 4
_TRAIL_CHAR_CAP = 140

# Fresh-state fast path (B1 run-9 ON-T2 footprint cut). Run-9's sole failing
# axis was ON-T2 M1 (2505 vs OFF 675 words), and the transcript locates the
# cost: the previous session left NOTHING to hand off (a complete card with
# no resolved pointer and no evidence trail — the scripted adoption card),
# yet the handoff still said "Open that card FIRST", so the agent paid a
# contentless card read; and 1724 of the 2505 words (69%) were ONE repo-wide
# grep polluted by the vendored ``bootstrap.py`` (862w) plus its byte-copy
# under ``<state_dir>/backup/`` (862w) after the agent's hand-rolled
# exclusion filter failed. The kit's two existing countermeasures both
# missed that path: the planted ``.ignore`` only covers ripgrep-family
# tools (plain ``grep`` has no ignore protocol), and the CLAUDE.md hygiene
# recipe rode the claudeMd channel measured ABSENT 0/6. So when the trail is
# empty, the handoff (a) stops routing the session into history and (b)
# carries the byte-exact WORKING exclusion recipe on the one surface run-9
# proves is delivered (push 3/3) and read first (ON-T2's first tool call).
# T4-shaped (in-progress + trail) and T5-shaped (complete + resolved
# pointer) renderings are byte-equivalent to before — pinned by tests.
_FRESH_START_LINE = (
    "- Fresh start — nothing in flight: orient from the task and the code; "
    "the card and `git log` history have nothing for you here."
)
_SEARCH_HYGIENE_LINE = (
    "- Search hygiene: `bootstrap.py` + `.substrate/` are kit machinery, not "
    "project code — exclude them: `grep -r --exclude=bootstrap.py "
    "--exclude-dir=.substrate …` (ripgrep honors the planted `.ignore`)."
)


def resolved_handoff_pointer(text: str) -> str:
    """Extract the newest RESOLVED handoff pointer from a session card.

    The auto-draft writes ``- Next session should know: [[fill: …]]`` and a
    closing session resolves the slot in place, so the pointer is a line
    match, not structure. The LAST resolved match wins (drafted close-outs
    append, so the newest section sits at the bottom); a line still carrying
    an unresolved ``[[fill:`` slot is skipped — pushing a template slot at a
    cold session would be noise, not handoff.
    """
    pointer = ""
    for line in text.splitlines():
        lowered = line.lower()
        index = lowered.find(HANDOFF_NEEDLE)
        if index < 0:
            continue
        rest = line[index + len(HANDOFF_NEEDLE) :].lstrip(" :**").strip()
        if not rest or DRAFT_FILL_TOKEN in rest:
            continue
        pointer = rest
    if len(pointer) > HANDOFF_EXCERPT_CAP:
        pointer = pointer[: HANDOFF_EXCERPT_CAP - 1].rstrip() + "…"
    return pointer


def evidence_trail(text: str) -> list[str]:
    """Extract the auto-collected evidence bullets from a drafted card.

    The B1 run-8 content-gap fix: run-8 was the family's first
    card-continuity conversion — ON-T4 opened ``HANDOFF.md`` in its first
    tool call and followed it to the card — and the payload was 8 unfilled
    ``[[fill:]]`` slots, so "real context came from reading ``cli.py``"
    (run-8 report §2) exactly as OFF re-derived it. The draft's EVIDENCE
    half (files touched, HEAD movement, commit subjects) is real content the
    engine already harvested; when the judgment half is still unresolved,
    the pointer carries that evidence itself instead of pointing at a
    skeleton. Only draft-shaped bullet lines match (:data:`_TRAIL_PREFIXES`);
    lines still carrying an unresolved slot are skipped; caps keep the
    pointer lean.
    """
    trail: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith(_TRAIL_PREFIXES) or DRAFT_FILL_TOKEN in stripped:
            continue
        if len(stripped) > _TRAIL_CHAR_CAP:
            stripped = stripped[: _TRAIL_CHAR_CAP - 1].rstrip() + "…"
        trail.append(stripped)
        if len(trail) >= _TRAIL_LINE_CAP:
            break
    return trail


def handoff_lines(root: Path, config: Config) -> list[str]:
    """Compose the handoff bullet lines, or ``[]`` when no session card exists.

    The single source both delivery surfaces render: the SessionStart
    orientation push (section 2) and the ``HANDOFF.md`` pointer file. Content:
    the newest card's path, its completion state, its unresolved auto-draft
    slot count, and the previous session's resolved "Next session should
    know" pointer, capped terse (the M1 budget). A complete card that left
    neither pointer nor trail renders the fresh-state fast path instead
    (run-9 ON-T2 footprint cut — see the constants above).
    """
    card = latest_session_log(root / config.sessions_dir)
    if card is None:
        return []
    text = card.read_text(encoding="utf-8", errors="replace")
    try:
        rel = card.relative_to(root)
    except ValueError:
        rel = card
    in_progress = status_in_progress(text)
    status = "in-progress/drafted" if in_progress else "complete"
    slots = unresolved_fill_count(text)
    slot_note = f", {slots} unresolved [[fill:]] slot(s)" if slots else ""
    lines = [f"- Newest session card: `{rel}` — status: {status}{slot_note}."]
    pointer = resolved_handoff_pointer(text)
    if pointer:
        lines.append(f"- Next session should know: {pointer}")
    else:
        # No resolved pointer (an unadopted draft, usually): surface the
        # card's auto-collected evidence here so the arrival surface carries
        # content, not a pointer to a skeleton (run-8 content-gap fix).
        trail = evidence_trail(text)
        if not trail and not in_progress:
            # Fresh-state fast path (run-9 ON-T2 footprint cut): a COMPLETE
            # card that left neither a pointer nor a trail has nothing to
            # hand off — routing the session into it is pure orientation
            # tax. Say so, and arm the session with the working search
            # exclusion instead (the 1724-word grep-pollution class).
            lines.append(_FRESH_START_LINE)
            lines.append(_SEARCH_HYGIENE_LINE)
            return lines
        lines.extend(trail)
    lines.append(
        "- Open that card FIRST — it is the last session's record; prefer it "
        "over re-deriving history from `git log`/`git show`.",
    )
    return lines


def compose_pointer_file(lines: list[str]) -> str:
    """Render the ``HANDOFF.md`` body around the shared handoff lines."""
    return (
        "\n".join(
            [
                "# HANDOFF — the previous session's trail",
                "",
                HANDOFF_POINTER_MARKER,
                "<!-- regenerated by substrate-kit at every session boot; "
                "untracked by design — read it, never commit or edit it -->",
                "",
                *lines,
            ],
        )
        + "\n"
    )


def write_handoff_pointer(root: Path, config: Config) -> str | None:
    """Regenerate (or retire) the repo-root ``HANDOFF.md`` pointer file.

    Marker-guarded: an existing file without ``HANDOFF_POINTER_MARKER`` is
    host-owned and never touched. With no session card to point at, a
    kit-written pointer is removed (a stale pointer is worse than none).
    Returns a one-line advisory when the file changed, else ``None``.
    Fail-open by contract — any failure returns ``None`` rather than raising
    into a hook.
    """
    try:
        path = root / HANDOFF_POINTER_FILENAME
        existing: str | None = None
        if path.is_file():
            existing = path.read_text(encoding="utf-8", errors="replace")
            if HANDOFF_POINTER_MARKER not in existing:
                return None  # host-owned HANDOFF.md — never touch
        lines = handoff_lines(root, config)
        if not lines:
            if existing is not None:
                path.unlink()
                return f"{HANDOFF_POINTER_FILENAME}: no session card to point at — pointer removed"
            return None
        body = compose_pointer_file(lines)
        if existing == body:
            return None
        atomic_write_text(path, body)
        return (
            f"{HANDOFF_POINTER_FILENAME} refreshed → newest session card "
            "(untracked by design; do not commit)"
        )
    except Exception:  # fail open — the pointer must never crash a hook seam
        return None
