"""Owner-action quality checker — ⚑ needs-owner asks must be actionable.

Why + provenance: the owner-action quality band (inbox ORDER 008, owner
directive 2026-07-09). Agents' ``⚑ needs-owner`` items were too often
(a) unnecessary — based on assumed walls nobody actually hit — or
(b) phrased so a non-technical owner couldn't act on them directly. The
owner is the scarcest resource in the program; every unclear or
unnecessary ask burns attention and stalls the asking lane. The contract
(canonical: ``control/README.md`` § the OWNER-ACTION item format) gives
every ask six REQUIRED fields:

- ``WHAT`` — one plain sentence, zero jargon
- ``WHERE`` — exact click path or URL
- ``HOW`` — paste-ready text/values where applicable
- ``WHY-IT-MATTERS`` — one sentence in product terms
- ``UNBLOCKS`` — what starts moving the moment it's done
- ``VERIFIED-NEEDED`` — the attempt made + the exact error/wall proving
  only the owner can do this (assumption-based asks are banned)

Posture: **advisory-only, never exit-affecting** — the deliberate mirror
of ``check_status_current``'s staleness warning. Existing adopters carry
free-text asks today; a gate would pre-redden every heartbeat the moment
this ships. The warning surfaces in every ``check`` run (both CI lanes —
the asks live in the heartbeat files the control fast lane already
validates) and the ``session-close`` skill asks the same question at close;
migration pressure without a locked door.

Detection is deliberately coarse (one finding per heartbeat file naming
the absent field labels, scanning the whole file so inline items and
linked blocks both count): the point is a nudge toward the format, not a
parser for every free-text shape an ask can take. Input-gated like every
checker — engages only when the ``control/`` protocol is present and the
file's ``⚑ needs-owner`` value is something other than ``none``. Stdlib
only; unreadable files fail open.

Owner-assist output standard (grounded-skills slice 4, plan §3/§7.4;
added 2026-07-12, §8 Q2=B advisory-first): two further advisory findings
extend the same contract —

- ``owner-action-risk-class`` — an ``⚑ OWNER-ACTION`` block whose
  contiguous text carries no risk-class token (``✅ / ↩️ / ⚠️`` — the
  maintainer-profile standing rule: a risk class on every manual step).
- ``owner-action-vague-destination`` — a ``WHERE:`` value naming a
  settings-like surface with no deep shape at all (no URL, no click-path
  arrow, no path): the "go to settings" anti-pattern from the Q-0263
  incident. Deep values ("Settings → Rules → …", a URL, a repo path)
  never fire.

Reliability of the two new checks (PL-008): UNVERIFIED — confirm their
findings against ground truth a few times across sessions before trusting
them; **delete these two checks if they prove unreliable over multiple
sessions.** Both are advisory-only by the same contract as the fields nag.
"""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

from engine.checks.check_docs import Finding
from engine.checks.check_status_current import (
    CONTROL_README_RELPATH,
    INBOX_RELPATH,
    heartbeat_relpaths,
)

# The six REQUIRED field labels (ORDER 008) + the ⚑ needs-owner token are
# kit-owned grammar with ONE home — engine.grammar (EAP §6.8): the writer
# templates and this enforcer consume the same constants, so they cannot
# drift apart. Field semantics (canonical-first spelling, the lenient
# WHY:/VERIFIED-WHEN: alternates) are documented there. Re-exported here
# unchanged for existing importers.
from engine.grammar import (
    DESTINATION_SHAPE_MARKS,
    NEEDS_OWNER_TOKEN,
    OWNER_ACTION_BLOCK_TOKEN,
    OWNER_ACTION_FIELDS,
    RISK_CLASS_TOKENS,
    VAGUE_DESTINATION_WORDS,
)


def _needs_owner_value(text: str) -> str | None:
    """Return the ``⚑ needs-owner`` value, or None when the line is absent.

    The heartbeat contract writes one ``⚑ needs-owner: <...>`` line; the
    value is everything after the first colon following the token. Only the
    first occurrence counts — the format block in a README copy would
    otherwise self-trigger.
    """
    idx = text.find(NEEDS_OWNER_TOKEN)
    if idx == -1:
        return None
    line = text[idx:].splitlines()[0]
    _, _, value = line.partition(":")
    return value.strip()


# The canonical WHERE label (one spelling — no lenient alternates exist).
_WHERE_LABEL = OWNER_ACTION_FIELDS[1][0]


def _unrisked_block_count(text: str) -> int:
    """Return how many ⚑ OWNER-ACTION blocks carry no risk-class token.

    A block is the contiguous paragraph after its ``⚑ OWNER-ACTION`` marker
    (up to the first blank line or the next marker) — a risk token elsewhere
    in the file never vouches for a block that lacks one.
    """
    count = 0
    for segment in text.split(OWNER_ACTION_BLOCK_TOKEN)[1:]:
        block = segment.split("\n\n", 1)[0]
        if not any(token in block for token in RISK_CLASS_TOKENS):
            count += 1
    return count


def _vague_destinations(text: str) -> list[str]:
    """Return WHERE: values that name a surface without any deep shape.

    Fires only on the intersection of *both* signals — a settings-like word
    (``VAGUE_DESTINATION_WORDS``) AND no shape mark at all
    (``DESTINATION_SHAPE_MARKS``: URL, click-path arrow, path separator) —
    so "Settings → Rules → …", any URL, and any repo path stay clean, and a
    value like "any channel" (no surface word) never fires either.
    """
    vague: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith(_WHERE_LABEL):
            continue
        value = stripped.partition(":")[2].strip()
        lowered = value.lower()
        if any(word in lowered for word in VAGUE_DESTINATION_WORDS) and not any(
            mark in value for mark in DESTINATION_SHAPE_MARKS
        ):
            vague.append(value)
    return vague


def check_owner_actions(
    target: Path,
    *,
    status_files: Sequence[str] | None = None,
) -> list[Finding]:
    """Return advisory findings for unstructured ⚑ needs-owner asks.

    One ``owner-action-fields`` finding per configured heartbeat file whose
    ``⚑ needs-owner`` value is present and not ``none`` while the file lacks
    one or more OWNER-ACTION field labels (the whole file is scanned, so an
    inline item and a structured block below the list both satisfy the
    contract). Advisory by contract: callers must never count these toward
    an exit code (see module docstring). Empty when the ``control/``
    protocol is absent.
    """
    relpaths = heartbeat_relpaths(status_files)
    control_evidence = [INBOX_RELPATH, CONTROL_README_RELPATH, *relpaths]
    if not any((target / rel).is_file() for rel in control_evidence):
        return []
    findings: list[Finding] = []
    for rel in relpaths:
        path = target / rel
        if not path.is_file():
            continue  # missing heartbeat is check_status_current's finding
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue  # fail open — an unreadable file is not a verdict
        value = _needs_owner_value(text)
        if value is None or value.lower().startswith("none") or not value:
            continue
        missing = [
            alts[0].rstrip(":")
            for alts in OWNER_ACTION_FIELDS
            if not any(alt in text for alt in alts)
        ]
        if missing:
            findings.append(
                Finding(
                    rel,
                    "owner-action-fields",
                    "⚑ needs-owner carries asks without the OWNER-ACTION "
                    f"fields (missing: {', '.join(missing)}) — the owner is "
                    "the scarcest resource: structure each ask per "
                    "control/README.md § OWNER-ACTION format (attempt it "
                    "yourself or cite the exact wall — VERIFIED-NEEDED; "
                    "assumption-based asks are banned), and withdraw stale "
                    "asks.",
                ),
            )
        # Owner-assist output standard (slice 4) — advisory, same contract.
        unrisked = _unrisked_block_count(text)
        if unrisked:
            findings.append(
                Finding(
                    rel,
                    "owner-action-risk-class",
                    f"{unrisked} ⚑ OWNER-ACTION block(s) carry no risk-class "
                    "token — every manual step names its class (✅ safe / "
                    "read-only · ↩️ reversible, say how to undo · ⚠️ "
                    "irreversible / destructive), e.g. a `RISK:` line per "
                    "block (control/README.md § Owner-assist output "
                    "standard).",
                ),
            )
        vague = _vague_destinations(text)
        if vague:
            findings.append(
                Finding(
                    rel,
                    "owner-action-vague-destination",
                    "WHERE: names a surface without a deep destination "
                    f"({'; '.join(vague)}) — name the exact destination: a "
                    "deep URL, a console path to the exact field "
                    "(Surface → section → field), or a repo path + line; "
                    'never a bare "go to settings" (control/README.md § '
                    "Owner-assist output standard).",
                ),
            )
    return findings
