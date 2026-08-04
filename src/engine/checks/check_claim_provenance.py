"""Measurement-claim provenance advisory — warn-only, NEVER exit-affecting.

Provenance: PL-014 (``docs/program/rulings.md``), imported from the spider-swing
session of 2026-08-01. The owner corrected ~14 published claims in a single run;
the *measurements* were overwhelmingly sound and the **summary sentences** were
not. The load-bearing case: "4.71 taps/s" was sampled at 30 fps from a natively
60 fps recording, a design constraint was built on that number, and that
constraint was then cited as the reason the design was trustworthy — three
layers, each internally consistent, none catchable by any gate. It was caught
only because the owner knew how fast he taps.

Why this exists: PL-006 says source wins and a false green is the check's bug.
But a number with **no stated instrument has no source to lose to** — nothing
can ever show it wrong. Recording the instrument is what makes a measurement
falsifiable at all, and an unfalsifiable number compounds silently into every
decision taken on top of it. The owner's own name for the failure class,
"verifiable but didn't verify", is what this checker mechanizes: it puts the
question on the page instead of leaving it to whether the author happened to
mention their method.

What it does: over documents under a measurements-style directory whose badge is
a result-bearing token, emit ONE advisory per document that presents numeric
result tables while carrying no **labelled** provenance statement. It never
inspects individual numbers and never proposes a value — it asks only whether
the document says where its numbers came from.

Two conditions, deliberately AND-ed — the document must carry the literal label
``provenance`` (a heading, a bolded lead, a table column) AND at least one word
of the PL-014 vocabulary (``measured`` / ``inferred`` / ``assumed``).

**Why the label is required, and it is not pedantry.** The first draft tested
for the vocabulary alone, and measured against the seven spider-swing documents
this ruling was extracted FROM, it fired on **zero of seven** — every one of
them already used "measured" incidentally in prose ("the exploit is now
measured", "measured per track in isolation"). A check with no sensitivity on
the corpus that motivated it is a false green, which PL-006 calls the check's
own bug. Emphasis alone does not rescue it either: two of the seven carry
*bolded* incidental uses. The literal label is the discriminator that survived
the corpus, because "provenance" is a word nobody writes by accident in a
results table — and it has the side benefit PL-014 actually wants, that the
instrument becomes greppable rather than merely present.

Posture — ADVISORY only (warn-only, never exit-affecting): returns a single
``list[Finding]`` with no gate tier, wired on the advisory path in ``cli.py``
(``posture="advisory"``) exactly like ``check_dateless_walls``. It is
deliberately NOT in ``STRICT_SUBCHECKS``: a hard red would flag every existing
measurement document at once, which is exhortation wearing enforcement's clothes
and the precise opposite of the nudge intended (PL-014 scope). Input-gated +
fail-open like every checker: no measurements directory, or an unreadable file,
yields nothing (an absent or unreadable document is not a verdict). Stdlib only.

Reliability: UNVERIFIED as of 2026-08-01 — confirm its output against ground
truth across a few sessions before trusting it. **Delete this checker if it
proves unreliable over multiple sessions** (PL-008 kill-switch); a lying check
left in place is worse than no check.
"""

from __future__ import annotations

import re

from engine.checks.check_docs import Finding, badge_token

# Named CLAIM_PROVENANCE_KIND, not a bare FINDING_KIND: the dist concatenates
# every engine module into one namespace, where a second top-level
# ``FINDING_KIND`` would collide (check_folded_gate.py already owns one).
CLAIM_PROVENANCE_KIND = "claim-provenance"

# Directory names that hold instrumentation output. A document only falls in
# scope when it lives under one of these — ordinary prose docs quote numbers all
# the time and are not making measurement claims.
_MEASUREMENT_DIRS = ("measurements", "benchmarks", "instrumentation")

# The provenance vocabulary from PL-014. Matched case-insensitively as whole
# words so "measured", "Measured," and "(measured, 60 fps)" all count.
_RE_PROVENANCE_WORD = re.compile(
    r"\b(measured|inferred|assumed)\b",
    re.IGNORECASE,
)

# The deliberate LABEL. Prose about a measurement uses "measured" constantly and
# the word "provenance" essentially never, which is what makes this the half of
# the test that carries the signal (see the module docstring for the corpus
# measurement that forced it). Any shape counts — `## Provenance`, `**Claim
# provenance (PL-014)**`, a `| Provenance |` table column — because the point is
# that the author labelled the statement, not that they matched a template.
_RE_PROVENANCE_LABEL = re.compile(r"\bprovenance\b", re.IGNORECASE)

# A markdown table row carrying at least one number — the shape of a reported
# result. Deliberately crude: this checker asks whether the document states its
# provenance at all, never whether any particular row is well-sourced.
_RE_NUMERIC_TABLE_ROW = re.compile(r"^\s*\|.*\d.*\|")

# Badge tokens whose documents report results. A `plan` or `ideas` doc may carry
# illustrative numbers without claiming to have measured anything.
_RESULT_BADGES = ("reference", "living-ledger", "audit")


def _reports_numbers(text: str) -> bool:
    """True when the document presents at least two numeric table rows.

    Two rather than one so a lone header-ish row or a single incidental figure
    does not pull a prose document into scope.
    """
    hits = 0
    for line in text.splitlines():
        if _RE_NUMERIC_TABLE_ROW.match(line) is not None:
            hits += 1
            if hits >= 2:
                return True
    return False


def _in_measurement_dir(relative_parts) -> bool:
    return any(part.lower() in _MEASUREMENT_DIRS for part in relative_parts)


def check_claim_provenance(target, config=None) -> list[Finding]:
    """Return advisory findings for measurement docs that state no provenance.

    Advisory only — the caller wires this on the ``posture="advisory"`` path and
    NEVER counts it toward the exit code. Input-gated + fail-open: an absent
    ``docs/`` tree, or an unreadable file, yields no finding. ``config`` is
    accepted for call-site symmetry with its advisory siblings but unused (there
    is no threshold — stating provenance is a binary property).
    """
    docs_root = target / "docs"
    if not docs_root.is_dir():
        return []  # input-gated: nothing to scan

    findings: list[Finding] = []
    for path in sorted(docs_root.rglob("*.md")):
        try:
            relative = path.relative_to(docs_root)
        except ValueError:  # pragma: no cover - rglob keeps these under root
            continue
        if not _in_measurement_dir(relative.parts[:-1]):
            continue
        # check_docs.badge_token is the kit's ONE badge reader (its own words:
        # "one badge reader, not per-module copies"), and it already fails open
        # to None on an unreadable or non-UTF-8 file.
        if badge_token(path) not in _RESULT_BADGES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue  # fail open — an unreadable document is not a verdict
        if not _reports_numbers(text):
            continue
        labelled = _RE_PROVENANCE_LABEL.search(text) is not None
        classified = _RE_PROVENANCE_WORD.search(text) is not None
        if labelled and classified:
            continue
        if labelled:
            detail = (
                "labels a provenance statement but never classifies a claim — "
                "use the PL-014 vocabulary"
            )
        elif classified:
            detail = (
                "uses provenance words in prose but carries no labelled "
                "provenance statement, so the instrument is not findable — "
                "add one (a `## Provenance` section, or a **Provenance:** lead "
                "under each result table)"
            )
        else:
            detail = "reports numeric results but states no provenance"
        findings.append(
            Finding(
                str(relative).replace("\\", "/"),
                CLAIM_PROVENANCE_KIND,
                f"{detail} — say of each claim `measured` (with the method AND "
                "the instrument's resolution), `inferred` (from what), or "
                "`assumed` (PL-014). A number with no stated instrument has no "
                "source to lose to, so nothing can ever show it wrong, and it "
                "compounds silently into the decisions taken on top of it.",
            ),
        )
    return findings
