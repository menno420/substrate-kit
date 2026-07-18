"""check_no_false_walls — engine leg guarding EVERY adopter against writing a
FALSE agent-capability limitation into a forward-binding surface.

This is the ENGINE-shipped port of ``tools/check_no_false_walls.py`` (added
2026-07-18, PR #448/#449): the grammar, blocklist, and clearing logic live
here **once**, and `bootstrap.py check` runs :func:`check_no_false_walls` as an
additive finding leg so every adopter enforces the rule with zero per-repo
wiring — the kit's own ``tools/`` copy delegates to this module (no duplicate
logic). The standalone tool keeps scanning the kit-only surfaces (templates,
skill bodies) that adopters do not have; this module scans the surfaces an
ADOPTER *does* have (its live ``docs/``, root ``CONSTITUTION.md`` /
``CAPABILITIES.md``, and any live ``.claude/**`` skill/rule bodies).

OWNER'S PRINCIPLE (the reason this check exists — bake it in, do not soften it):
**agents have NO owner-imposed limitations.** A capability refusal, when it
happens at all, is a TRANSIENT auto-mode-classifier state that Anthropic reworks
continually — so any wall written down is stale on the very next platform update
AND it makes the next session not even try (a real prior failure: a session read
a wall list and replied "this is accurate, I will not attempt anything").
Therefore the docs must record **capabilities, never limitations.** CI is the
authoritative enforcement of that rule — an agent cannot argue with a red check,
so no session can quietly re-seed a false limitation. The genuine, momentary
refusals still get recorded — but as DATED ledger rows / ``LAST-VERIFIED`` walls
that carry their own expiry, never as forward-binding standing doctrine.

It reports a finding (kind ``false-wall:<rule>``, exit-affecting under
``--strict``) when a forward-binding surface asserts ANY of:
  * a SUBJECT {agent|session|worker|seat|the bot|you} is unable / not-allowed to
    perform a capability {merge|deploy|push|arm|ready-flip|flip|land|delete a
    branch|update Railway/env/infra variables};
  * a capability ACTION is asserted owner-only / owner-gated / owner-must /
    only-the-owner-can, for a merge / deploy / branch-deletion action;
  * a standing platform wall {classifier-denied, 403-walled, permission-walled,
    agent-unlandable, self-merge classifier, blocked for agents, …}.

GROUND TRUTH (owner-confirmed, proven ~20× live on 2026-07-18): merging is
NORMAL agent work; so is deploying / pushing / arming.

DELIBERATELY NOT FLAGGED — false positives are the failure mode (owner: a false
positive that reds CI is worse than a rare miss):
  * CODE / architecture rules — "services must NOT import views", "never call
    pool.execute" — the patterns require an agent-capability subject + a
    GitHub/merge/deploy/infra object, so a bare "must not" over a code noun
    never trips.
  * GENUINE walls that DO stand and are dated — ref/branch DELETION 403,
    tag-push / release 403, repo Settings / rulesets / secrets / env-var
    provisioning = owner: these survive because each carries a
    ``LAST-VERIFIED`` / dated marker. The verb list EXCLUDES read / create /
    access / provision / write precisely because those collide with genuine
    standing walls.
  * MISSING-CREDENTIAL owner-INPUT requests — "needs a Stripe account from the
    owner" is a missing input, not a capability wall.
  * dated ledger records, repudiation lines (``no standing …``, ``NOT a wall``,
    a ``FALSE "…"`` quote), historical dirs / dated report files / append-log
    sections.

Engine code, not repo tooling: stdlib only, no print/subprocess (§3.2 bans),
returns :class:`engine.checks.check_docs.Finding` objects that ride the strict
loop. Reliability (PL-008): UNVERIFIED at birth — confirm its findings against
ground truth a few times across sessions before trusting it; **delete this if it
proves unreliable over multiple sessions.** Ported to the engine 2026-07-18.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import NamedTuple

from engine.checks.check_docs import Finding

# ── Scan scope ────────────────────────────────────────────────────────────────

# Forward-binding doc roots that are ALWAYS excluded (historical corpora — they
# are allowed to record the old, now-false reading).
_HISTORICAL_DIR_PREFIXES = (
    "retro/",
    "planning/",
    "audits/",
)

# Directory subtrees never scanned at all (session memory, kit machinery, build
# artifacts). Extended at scan time with the host's configured state/sessions
# dirs so a non-default install stays quiet too.
_SKIP_DIR_PARTS = frozenset({".sessions", ".substrate", ".git"})

# gen-2 corpus: only the queue/proposal records are historical; the rest of
# docs/gen2 (next-boot, README, …) is forward-binding.
_GEN2_HISTORICAL = re.compile(r"gen2/[^/]*(?:queue|proposal)[^/]*\.md$", re.I)

# A file whose basename carries an ISO date is a dated record (reports,
# snapshots, walkthroughs) — skipped wholesale.
_DATED_FILENAME = re.compile(r"\d{4}-\d{2}-\d{2}")

# ── Shared grammar fragments for the generalized capability-wall class ─────────
#
# SUBJECT: an agent/session actor. Scoped tight — "services" / "views" / "the
# function" are NOT actors, so a CODE rule ("services must not import views")
# can never satisfy the subject slot.
_SUBJECT = (
    r"(?:agents?|(?:a\s+)?sessions?|workers?|seats?|the\s+bot|the\s+agent|you)"
)
# NEGATED capability framing ("cannot", "are not allowed to", "do not", …).
_NEGATION = (
    r"(?:can\s?not|can'?t|may\s+not|must\s+not|"
    r"are\s+not\s+(?:allowed|permitted)\s+to|is\s+not\s+(?:allowed|permitted)\s+to|"
    r"are\s+unable\s+to|is\s+unable\s+to|are\s+blocked\s+from|is\s+blocked\s+from|"
    r"do(?:es)?\s+not)"
)
# FALSE-wall capability verbs — the auto-mode / classifier-TRANSIENT actions an
# agent is falsely told it cannot do. DELIBERATELY EXCLUDES read / create /
# access / provision / write / trigger / run / set / modify / configure: those
# collide with GENUINE standing walls documented (dated) on real trees
# ("sessions cannot read fleet-manager", "session tokens cannot create repos",
# "host provisioning / env-var config owner-only") and would red CI as false
# positives. Infra-mutation verbs (update/change Railway variables) are handled
# by a separate object-scoped pattern below, never bare.
_CAP_VERB = (
    r"(?:merge|self[-\s]?merge|deploy|redeploy|push|arm(?:\s+auto[-\s]?merge)?|"
    r"ready[-\s]?flip|flip|land|delete\s+(?:a\s+|the\s+)?branch)"
)
# Up to two short filler words between the negation and the verb
# ("cannot *immediately* merge") — bounded, so it can't bridge to a far verb.
_FILL = r"(?:[a-z'’-]+\s+){0,2}?"
# Infra object a mutation verb must land on for the infra pattern to fire.
_INFRA_OBJ = (
    r"(?:railway|env(?:ironment)?|deploy(?:ment)?|infra(?:structure)?|"
    r"variables?|secrets?|config)"
)
# Owner-authority framings that assert a capability is the owner's to perform.
_OWNER_AUTHORITY = (
    r"(?:the\s+owner\s+must|only\s+the\s+owner\s+(?:can|may|must)|"
    r"requires?\s+the\s+owner\s+to)"
)
# Capability NOUNS that, asserted owner-only / owner-gated / classifier-denied,
# are false walls. Scoped to merge/deploy/branch-deletion — NOT repo-creation,
# settings, secrets, release or seat/plan config (those are genuine, dated).
_CAP_NOUN = (
    r"(?:merging|merge|self[-\s]?merge|auto[-\s]?merge|arming|"
    r"deploying|deployment|deploy|redeploy(?:ing|ment)?|"
    r"branch\s+deletion|ready[-\s]?flip|pushing)"
)

# ── Blocklist — the curated FALSE standing prohibitions ───────────────────────
#
# Each entry matches the PROHIBITION, not keywords in isolation. Case-insensitive.
# A match becomes a finding ONLY if the line is not cleared (dated / repudiated /
# historical). Entries flagged owner_gated require an extra same-line directive
# verb (handled below) so the adjective use ("owner-gated PRs #26 are MERGED")
# does not trip.

_BLOCKLIST: tuple[tuple[str, "re.Pattern[str]"], ...] = (
    # ── Generalized capability-wall class (owner directive 2026-07-18) ──
    # SUBJECT + NEGATION + a FALSE-wall capability verb.
    #   "agents cannot delete branches", "sessions may not self-merge",
    #   "workers are not allowed to deploy".
    (
        "agent-negated-capability",
        re.compile(_SUBJECT + r"\s+" + _NEGATION + r"\s+" + _FILL + _CAP_VERB, re.I),
    ),
    # SUBJECT + NEGATION + infra-MUTATION verb + infra object.
    #   "sessions are not allowed to update Railway variables".
    (
        "agent-negated-infra-mutation",
        re.compile(
            _SUBJECT
            + r"\s+"
            + _NEGATION
            + r"\s+"
            + _FILL
            + r"(?:update|change|set|modify|provision|configure|edit)\s+"
            + r"(?:[a-z'’-]+\s+){0,2}?"
            + _INFRA_OBJ,
            re.I,
        ),
    ),
    # OWNER-AUTHORITY + a capability verb ("the owner must merge PRs",
    # "only the owner can deploy"). The 0-25-char window keeps it same-clause,
    # so "the owner must ENTER/paste/parse" (owner-assist doctrine) never trips.
    (
        "capability-is-owner-authority",
        re.compile(
            _OWNER_AUTHORITY
            + r"[^.\n]{0,25}?"
            + r"(?:merge\b|self[-\s]?merge|deploy\b|redeploy\b|"
            r"ready[-\s]?flip|arm\s+auto|land\s+(?:a|the|your)\b|push\b)",
            re.I,
        ),
    ),
    # A capability NOUN asserted owner-only / owner-gated / classifier-denied /
    # not-agent as a STANDING property ("branch deletion is owner-only",
    # "deploying is classifier-denied for agent seats", "merging = owner-gated").
    (
        "capability-asserted-owner-only",
        re.compile(
            _CAP_NOUN
            + r"\s+(?:is|are|remains?|stays?|=)\s+"
            + r"(?:owner[-\s]only|owner[-\s]gated|classifier[-\s]den(?:y|ies|ied)|"
            r"blocked\s+for\s+agents|not\s+enabled\s+for\s+agents|"
            r"not\s+(?:an?\s+)?agent[-\s](?:side|action|capability))",
            re.I,
        ),
    ),
    # Standing platform-wall tokens (compound adjectives — never bare "wall"):
    #   agent-unlandable, 403-walled, permission-walled, classifier-walled,
    #   "blocked for agents", "not enabled for agents", "agents/sessions get 403".
    (
        "standing-platform-wall",
        re.compile(
            r"\bagent[-\s]unlandable\b|"
            r"\b(?:403|permission|classifier)[-\s]?walled\b|"
            r"\bblocked\s+for\s+agents\b|"
            r"\bnot\s+enabled\s+for\s+agents\b|"
            r"\b(?:agents?|sessions?|workers?|seats?)\s+get\s+403\b",
            re.I,
        ),
    ),
    # Standalone "classifier-denied / classifier-denies" — the signature
    # transient-freeze assertion, no "since <date>" required. Dated ledger rows
    # ("classifier freeze … denies") stay cleared by the dated-block rule;
    # repudiations ('no standing "classifier-denied" wall; do not invent one')
    # by the repudiation cue.
    (
        "classifier-denied-standing",
        re.compile(r"classifier[-\s]den(?:y|ies|ied)\b", re.I),
    ),
    # ── Original merge-specific prohibitions (retained verbatim) ──
    # "classifier-denied since 2026-07-15" — the signature dated-freeze assertion.
    ("classifier-denied-since", re.compile(r"classifier[-\s]denied\s+since", re.I)),
    # classifier den* applied to a merge/ready-flip/arm action.
    (
        "classifier-denies-merge",
        re.compile(
            r"classifier[-\s]den(?:y|ies|ied)\b[^.\n]{0,40}?"
            r"\b(?:merge|ready[-\s]?flip|self[-\s]?merge|arm)",
            re.I,
        ),
    ),
    # "agents do NOT ready-flip / arm / self-merge / merge / REST-MCP-merge".
    (
        "agents-do-not-land",
        re.compile(
            r"\bagents?\s+do(?:es)?\s+not\s+"
            r"(?:ready[-\s]?flip|arm|self[-\s]?merge|merge\b|"
            r"rest[/\s-]*(?:mcp[-\s]*)?merge|mcp[/\s-]*rest[-\s]*merge)",
            re.I,
        ),
    ),
    # "agents / a session cannot | may not | are not allowed to merge / arm / flip".
    (
        "agents-cannot-land",
        re.compile(
            r"\b(?:agents?|(?:a\s+)?(?:agent\s+)?sessions?|workers?)\s+"
            r"(?:can\s?not|can'?t|may\s+not|are\s+not\s+(?:allowed|permitted)\s+to)\s+"
            r"(?:ready[-\s]?flip|arm[-\s]?auto|self[-\s]?merge|merge\b)",
            re.I,
        ),
    ),
    # "never agent-side (merge)" / "no agent-side merge" / "never self-merge".
    (
        "never-agent-side",
        re.compile(
            r"\bnever\s+(?:agent[-\s]side|self[-\s]?merge)\b|"
            r"\bno\s+agent[-\s]side\s+merge\b",
            re.I,
        ),
    ),
    # "NEVER arm auto-merge".
    ("never-arm-automerge", re.compile(r"\bnever\s+arm\s+auto[-\s]?merge\b", re.I)),
    # "owner is the merge authority".
    (
        "owner-is-merge-authority",
        re.compile(r"\bowner\s+is\s+the\s+merge\s+authority\b", re.I),
    ),
    # "the owner merges (your PRs)" as a standing rule.
    ("the-owner-merges", re.compile(r"\bthe\s+owner\s+merges\b", re.I)),
    # "self-merge classifier".
    ("self-merge-classifier", re.compile(r"\bself[-\s]?merge\s+classifier\b", re.I)),
    # "agent-unlandable" / "green PR is agent-unlandable".
    ("agent-unlandable", re.compile(r"\bagent[-\s]unlandable\b", re.I)),
    # "agents / you / a session must NOT merge | open READY | flip | arm".
    (
        "must-not-land",
        re.compile(
            r"\b(?:agents?|you|(?:a\s+)?sessions?|the\s+agent|workers?)\s+"
            r"must\s+not\s+"
            r"(?:merge\b|open\s+(?:it\s+|the\s+|its\s+)?(?:pr\s+)?ready|"
            r"flip\b|self[-\s]?merge|arm)",
            re.I,
        ),
    ),
)

# owner-gated: candidate substring + a same-line STANDING-DIRECTIVE verb.
_OWNER_GATED = re.compile(r"\bowner[-\s]gated\s+(?:pr|merge)s?\b", re.I)
_OWNER_GATED_DIRECTIVE = re.compile(
    r"\b(?:route|routed|send|hand|escalate|wait\s+for|only\s+the\s+owner|"
    r"owner[-\s]only|must\b|cannot\s+merge|can'?t\s+merge|refus)",
    re.I,
)

# "Merge Without Review" / "Self-Approval" as a standing agent-merge prohibition:
# candidate string + a same-line prohibition frame (they are classifier
# refusal-reason strings, so only a framed standing use is a false wall).
_REVIEW_LABEL = re.compile(r"\bmerge\s+without\s+review\b|\bself[-\s]approval\b", re.I)
_PROHIBITION_FRAME = re.compile(
    r"\b(?:never|refus|deny|denied|deny-wins|cannot|can'?t|terminal|"
    r"prohibit|forbid|standing\s+(?:rule|wall)|classifier)",
    re.I,
)

# ── Clearing — a candidate line PASSES if any of these hold ────────────────────

# Repudiation / correction cues (case-insensitive). A line that CORRECTS the
# wall is exactly the forward-binding phrasing we WANT to keep.
_REPUDIATION_CUES = re.compile(
    r"no\s+standing|"
    r"not\s+a\s+wall|"
    r"do(?:es)?\s+not\s+(?:invent|record|apply|stand|hold)|"
    r"don'?t\s+invent|"
    r"never\s+route\s+a\s+mergeable\s+green\s+pr\s+to\s+the\s+owner|"
    r"normal\s+agent\s+(?:action|work)|"
    r"is\s+a\s+normal\s+agent|"
    r"not\s+an\s+owner\s+action|"
    r"(?:merging\s+)?works?\s+agent[-\s]side|"
    r"land\s+your\s+own|"
    r"no\s+longer\s+(?:applies|a\b|an\b|the\b|stands|holds)|"
    r"\bthe\s+old\b|"
    r"proven\s+(?:repeatedly|by\b|~?\d)",
    re.I,
)
# The repo's repudiation label: FALSE "…" (case-sensitive uppercase).
_FALSE_LABEL = re.compile(r"\bFALSE\b")

# Inline dated-record markers (this line is itself a dated record).
_DATED_LINE = re.compile(
    r"\bLAST-VERIFIED\b|\bSUPERSEDED\b|"
    r"[—·(]\s*\d{4}-\d{2}-\d{2}|"
    r"\bverified\s+\d{4}-\d{2}-\d{2}",
)
# A bullet that STARTS a dated record block.
_DATED_BULLET = re.compile(r"^\s*[-*]\s+\d{4}-\d{2}-\d{2}\b")
# A markdown heading.
_HEADING = re.compile(r"^\s*#{1,6}\s+(.*)$")
_HISTORICAL_HEADING = re.compile(r"append\s+log|historical", re.I)


class RawHit(NamedTuple):
    """One false-wall match in a text: 1-based ``line``, ``phrase``, ``rule``."""

    line: int
    phrase: str
    rule: str


def is_cleared(line: str, *, in_dated_block: bool, in_historical: bool) -> bool:
    """True when a blocklist match on ``line`` must NOT count as a finding."""
    if in_dated_block or in_historical:
        return True
    if _DATED_LINE.search(line):
        return True
    if _REPUDIATION_CUES.search(line):
        return True
    if _FALSE_LABEL.search(line):
        return True
    return False


def match_blocklist(line: str) -> tuple[str, str] | None:
    """Return (rule_name, matched_phrase) if ``line`` asserts a false wall."""
    for name, pat in _BLOCKLIST:
        m = pat.search(line)
        if m:
            return name, m.group(0)
    owner_gated = _OWNER_GATED.search(line)
    if owner_gated and _OWNER_GATED_DIRECTIVE.search(line):
        return "owner-gated-rule", owner_gated.group(0)
    review_label = _REVIEW_LABEL.search(line)
    if review_label and _PROHIBITION_FRAME.search(line):
        return "review-label-prohibition", review_label.group(0)
    return None


def scan_text(text: str) -> list[RawHit]:
    """Scan ``text`` line by line, returning every uncleared false-wall hit.

    The stateful loop tracks dated-record blocks (a ``- YYYY-MM-DD …`` bullet
    and its continuation) and historical headings (``## Append log`` /
    ``historical``) so a match inside a history section clears. Shared by the
    engine leg and the standalone ``tools/`` wrapper — the single home for the
    grammar (no duplicate logic).
    """
    hits: list[RawHit] = []
    in_dated_block = False
    in_historical = False
    for i, line in enumerate(text.splitlines(), start=1):
        heading = _HEADING.match(line)
        if heading:
            in_historical = bool(_HISTORICAL_HEADING.search(heading.group(1)))
            in_dated_block = False
        elif _DATED_BULLET.match(line):
            in_dated_block = True
        elif line.strip() and not line[:1].isspace() and not line.startswith(("-", "*", ">")):
            # A fresh left-margin paragraph ends the current dated bullet block.
            in_dated_block = False

        hit = match_blocklist(line)
        if hit is None:
            continue
        if is_cleared(line, in_dated_block=in_dated_block, in_historical=in_historical):
            continue
        rule, phrase = hit
        hits.append(RawHit(i, phrase.strip(), rule))
    return hits


def _skip_parts(state_dir: str, sessions_dir: str) -> frozenset[str]:
    """The dir-part skip set, extended with the host's state/sessions dirs."""
    extra = {p for p in (state_dir, sessions_dir) if p and "/" not in p}
    return _SKIP_DIR_PARTS | extra


def _docs_targets(root: Path, docs_root: str) -> list[Path]:
    """Every forward-binding ``<docs_root>/**/*.md`` (minus historical / dated)."""
    docs = root / docs_root
    out: list[Path] = []
    if not docs.is_dir():
        return out
    for md in sorted(docs.rglob("*.md")):
        rel_to_docs = md.relative_to(docs).as_posix()
        if any(rel_to_docs.startswith(p) for p in _HISTORICAL_DIR_PREFIXES):
            continue
        if _GEN2_HISTORICAL.search(rel_to_docs):
            continue
        if md.name.upper().startswith("CHANGELOG"):
            continue
        if _DATED_FILENAME.search(md.name):
            continue
        out.append(md)
    return out


def iter_adopter_files(
    root: Path,
    docs_root: str = "docs",
    *,
    state_dir: str = ".substrate",
    sessions_dir: str = ".sessions",
) -> list[Path]:
    """Collect the forward-binding surfaces an ADOPTER carries.

    These are the surfaces a rendered/adopted repo actually has: its live
    ``<docs_root>/**/*.md`` (minus historical corpora and dated records), the
    root ``CONSTITUTION.md`` / ``CAPABILITIES.md``, and any live ``.claude/**``
    markdown (the working agreement, rule bodies, and skill ``SKILL.md``
    bodies). Kit-only surfaces (``src/engine/templates/*.tmpl``,
    ``skills/skills.py``) are NOT here — the standalone ``tools/`` wrapper adds
    those for the kit's own CI.
    """
    skip = _skip_parts(state_dir, sessions_dir)
    targets: list[Path] = _docs_targets(root, docs_root)

    # Root constitution / capabilities.
    for name in ("CONSTITUTION.md", "CAPABILITIES.md"):
        p = root / name
        if p.is_file():
            targets.append(p)

    # Live .claude/** markdown (working agreement, rules, skill bodies). Absent
    # on a default cold adopt (the kit STAGES .claude under the state dir); a
    # host that opts into a live .claude tree is scanned like any other surface.
    claude = root / ".claude"
    if claude.is_dir():
        for md in sorted(claude.rglob("*.md")):
            targets.append(md)

    # De-dup, and drop anything under a skipped subtree.
    seen: set[Path] = set()
    out: list[Path] = []
    for p in targets:
        if p in seen:
            continue
        parts = set(p.relative_to(root).parts)
        if skip & parts:
            continue
        if p.name == "bootstrap.py":
            continue
        seen.add(p)
        out.append(p)
    return out


def check_no_false_walls(target: Path, config) -> list[Finding]:  # noqa: ANN001
    """Engine leg: flag any FALSE agent-capability wall on an adopter's surfaces.

    Rides the ``check`` strict loop like every other checker (added to
    :func:`engine.cli._extra_check_findings`), so ``bootstrap.py check
    --strict`` reds when a session documents a false limitation into the repo's
    own forward docs — the propagation of the kit-only ``tools/`` guard to every
    adopter with zero per-repo wiring. Additive: it only ADDS the
    ``false-wall:<rule>`` finding class; it changes no existing check semantics.
    """
    docs_root = getattr(config, "docs_root", "docs")
    state_dir = getattr(config, "state_dir", ".substrate")
    sessions_dir = getattr(config, "sessions_dir", ".sessions")
    findings: list[Finding] = []
    for path in iter_adopter_files(
        target,
        docs_root,
        state_dir=state_dir,
        sessions_dir=sessions_dir,
    ):
        rel = path.relative_to(target).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for hit in scan_text(text):
            findings.append(
                Finding(
                    rel,
                    f"false-wall:{hit.rule}",
                    (
                        f"line {hit.line}: false agent-capability wall "
                        f"{hit.phrase!r} — agents have no owner-imposed "
                        "limitations; merging/deploying/pushing is normal agent "
                        "work. Correct the line, or date-stamp/repudiate it if "
                        "it records a genuine momentary refusal."
                    ),
                )
            )
    return findings
