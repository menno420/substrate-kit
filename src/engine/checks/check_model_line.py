"""📊 Model-line payload lint — the run-report line's VALUES, not just its needle.

Why + provenance: idea ``docs/ideas/model-line-payload-lint-advisory-2026-07-11.md``
(Night-8 triage #3). The ``- **📊 Model:** <model> · <effort> · <task-class>``
run-report line is grammar-checked for the needle's presence
(``session_markers``), but its PAYLOAD drifts silently: the ORDER 013
self-review measured 4 of the 5 newest complete cards carrying off-PL-004
segment-2/3 values (W-10a — fixed by hand in a later flip commit), and the
telemetry harvest then records the drifted values as ground truth. The
harvest's own payload advisories fire once, at session-close time, on the
single card being closed; nothing re-checks at ``check`` time, so drift that
slips past one close-out is invisible until a human sweep.

This lint closes that gap: every ``check`` full-lane run scans the newest
COMPLETED cards under ``sessions_dir`` (a bounded window — see
:data:`MODEL_LINE_LINT_WINDOW`; ``window=0`` is the unbounded measurement
lane) and warns when a card's harvested Model line

- has the needle but no valid three-field ``·`` payload (``model-line-shape``),
- carries an exact model-ID token in the model segment instead of a
  family-level name (``model-line-exact-id`` — fleet reporting bar, ORDER 012),
- files an effort segment outside the taxonomy (``model-line-effort``) —
  except the sanctioned terminal value :data:`MODEL_EFFORT_UNRECORDED`
  (idea ``model-line-unrecorded-effort-marker-2026-07-15``): a retroactive
  repair of a card whose author never self-reported a tier records
  ``unrecorded`` honestly instead of inventing telemetry, and nagging it
  invites exactly that invention — so it is advisory-silent here while the
  harvest still records it verbatim; or
- files a task-class segment that does not prefix-match one of the 9 PL-004
  classes (``model-line-class`` — prefix-match on purpose: a decorated class
  like ``docs-only — oracle pin edit`` is a valid report, not drift).

Every finding quotes the expected byte-form verbatim
(:data:`engine.grammar.MODEL_LINE_TAUGHT_FORMAT`) — the run-1 ON-arm
false-red lesson: a message must name the exact expected form, never
contradict what the agent can see on the card.

Posture: **advisory-only, never exit-affecting** (PL-008 / the §8 Q2=B
advisory-first pattern, same contract as ``check_owner_actions`` /
``check_seat_digest``) — existing adopters carry drifted historical cards
today, and a gate would pre-redden every one of them on upgrade. Migration
pressure without a locked door; the fix is editing one line on one card.

Scope discipline (mirrors ``loop.telemetry`` exactly, by shared constants —
the EAP §6.8 writer/enforcer pattern; the grammar lives in
``engine.grammar``):

- Only **completed** cards are judged (``status_in_progress`` /
  ``unresolved_fill_count`` gate, the same machinery ``reconcile_model_usage``
  uses) — a born-red / drafted card has no finished report to lint.
- Inline code spans and fenced blocks are stripped first — prose that
  *mentions* the marker (docs about the mechanism do) never fires.
- ``[[fill:]]`` stand-in lines are skipped (an auto-draft is not a report).
- **Last-valid-wins**, exactly like ``parse_model_line``: the payload checks
  judge the line the harvest would record, so a corrected report later in
  the card supersedes an earlier one and the lint flags precisely what would
  pollute (or, for shape, silently miss) ``telemetry/model-usage.jsonl``.

Reliability (PL-008): UNVERIFIED — added 2026-07-14; confirm its findings
against ground truth a few times across sessions before trusting it, and
**delete this check if it proves unreliable over multiple sessions.** It is
advisory-only by contract either way. Stdlib only; unreadable files fail open.
"""

from __future__ import annotations

from pathlib import Path

from engine.checks.check_docs import Finding
from engine.checks.check_session_log import (
    _CODE_SPAN_RE,
    _FENCE_RE,
    DRAFT_FILL_TOKEN,
    status_in_progress,
    unresolved_fill_count,
)
from engine.grammar import (
    EXACT_MODEL_ID_RE,
    MODEL_EFFORT_VALUES,
    MODEL_LINE_NEEDLE,
    MODEL_LINE_TAUGHT_FORMAT,
    MODEL_TASK_CLASSES,
    parse_model_payload,
)

# The code-span/fence stripping is check_session_log's — imported, not
# mirrored: the namespace guard (test_check_namespace) rejects duplicate
# top-level names because the dist concatenation would silently shadow the
# earlier definition. A card whose prose mentions the needle in backticks or
# a fenced example is not a report.

# How many of the NEWEST completed cards the check-time scan judges.
# Measured at build time (2026-07-14, this lint's own session): an unbounded
# scan over the kit's own tree found 124 of 178 completed cards drifted (174
# findings) — surfacing all of it on every `check` run would bury the
# actionable signal in archaeology and burst the guard-fires journal past its
# dedupe scan window. The lint's job is friction→guard at session velocity
# (the W-10a evidence was "4 of the 5 NEWEST complete cards"), so the shipped
# default judges the newest window only; ``window=0`` scans unbounded (the
# drift-measurement lane). Sorted by filename — cards are date-prefixed by
# convention, so name order IS date order.
MODEL_LINE_LINT_WINDOW = 10

# The sanctioned TERMINAL effort value for retroactive payload repairs
# (idea model-line-unrecorded-effort-marker-2026-07-15, from the PR #390
# sweep): when a repairing session is not the card's author and the author
# never self-reported an effort tier, backfilling ``low|medium|high`` would
# be invented telemetry — ``unrecorded`` is the honest marker. It is NOT
# part of :data:`engine.grammar.MODEL_EFFORT_VALUES` (the real taxonomy live
# sessions must report — a live card filing it off-taxonomy still nags with
# the taught values); it is only exempt from the ``model-line-effort``
# advisory, and the telemetry harvest records it verbatim like any value.
MODEL_EFFORT_UNRECORDED = "unrecorded"

# The loud fix-path tail every finding carries — quotes the taught byte-form
# verbatim so the fix is a copy-edit, never a re-derivation.
_FIX_PATH = (
    f"fix the card's line to the taught form `{MODEL_LINE_TAUGHT_FORMAT}` "
    "(family-level model · effort · PL-004 task class; see .sessions/README.md)"
)


def model_line_findings(text: str) -> list[tuple[str, str]]:
    """Lint one completed card's text; return ``(kind, message)`` pairs.

    Returns ``[]`` when the card carries no needle at all — marker PRESENCE
    is the session-log gate's job (``missing_markers``), not this lint's;
    double-reporting the same miss would be advisory noise.
    """
    stripped = _CODE_SPAN_RE.sub("", _FENCE_RE.sub("", text))
    candidates = [
        line
        for line in stripped.splitlines()
        if MODEL_LINE_NEEDLE in line and DRAFT_FILL_TOKEN not in line
    ]
    if not candidates:
        return []
    last_valid: dict | None = None
    first_malformed: str | None = None
    for line in candidates:
        parsed = parse_model_payload(line.split(MODEL_LINE_NEEDLE, 1)[1])
        if parsed is not None:
            last_valid = parsed
        elif first_malformed is None:
            first_malformed = line.strip()
    if last_valid is None:
        return [
            (
                "model-line-shape",
                f"the `{MODEL_LINE_NEEDLE}` line {first_malformed!r} has no "
                "valid three-field payload (needs two `\N{MIDDLE DOT}` "
                "separators: model \N{MIDDLE DOT} effort \N{MIDDLE DOT} "
                "task-class) — the telemetry harvest records NOTHING from "
                f"this card; {_FIX_PATH}",
            ),
        ]
    findings: list[tuple[str, str]] = []
    model = last_valid["model"]
    if EXACT_MODEL_ID_RE.search(model):
        findings.append(
            (
                "model-line-exact-id",
                f"model segment {model!r} looks like an exact model-ID token "
                "— record the family-level model name only (e.g. `fable-5`, "
                "`opus-4.8`), never an exact model ID, dated or not (fleet "
                f"reporting bar, ORDER 012); {_FIX_PATH}",
            ),
        )
    effort = last_valid["effort"]
    if effort not in MODEL_EFFORT_VALUES and effort != MODEL_EFFORT_UNRECORDED:
        known = " | ".join(MODEL_EFFORT_VALUES)
        findings.append(
            (
                "model-line-effort",
                f"effort segment {effort!r} is not one of the taxonomy "
                f"values ({known}) — the PL-004 dataset records it verbatim; "
                f"{_FIX_PATH}",
            ),
        )
    task_class = last_valid["task_class"]
    if not any(task_class.startswith(known) for known in MODEL_TASK_CLASSES):
        known = " | ".join(MODEL_TASK_CLASSES)
        findings.append(
            (
                "model-line-class",
                f"task-class segment {task_class!r} does not prefix-match "
                f"any of the {len(MODEL_TASK_CLASSES)} PL-004 classes "
                f"({known}) — the PL-004 dataset records it verbatim; "
                f"{_FIX_PATH}",
            ),
        )
    return findings


def check_model_line(
    root: Path,
    *,
    sessions_dir: str,
    window: int = MODEL_LINE_LINT_WINDOW,
) -> list[Finding]:
    """Lint the ``window`` newest completed session cards under ``root/sessions_dir``.

    ``window=0`` lints every completed card (the drift-measurement lane; see
    :data:`MODEL_LINE_LINT_WINDOW` for why the check-time default is bounded).
    Advisory-only by contract — the caller (``cmd_check``'s full lane) emits
    these as never-exit-affecting warnings. Input-gated: a missing sessions
    directory (un-adopted tree) returns nothing; unreadable cards fail open;
    in-progress / drafted / fill-carrying cards are never judged.
    """
    findings: list[Finding] = []
    directory = root / sessions_dir
    if not directory.is_dir():
        return findings
    completed: list[tuple[Path, str]] = []
    for card in sorted(directory.glob("*.md")):
        if card.name == "README.md":
            continue
        try:
            text = card.read_text(encoding="utf-8")
        except OSError:
            continue
        if status_in_progress(text) or unresolved_fill_count(text):
            continue
        completed.append((card, text))
    if window:
        completed = completed[-window:]
    for card, text in completed:
        rel = f"{sessions_dir}/{card.name}"
        findings.extend(
            Finding(path=rel, kind=kind, message=message)
            for kind, message in model_line_findings(text)
        )
    return findings
