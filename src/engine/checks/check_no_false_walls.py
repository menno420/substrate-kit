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
from engine.seatdigest import seat_digest_relpath

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

# ── Class (b) (v1.20.2): kit-generated derived-render exemption ────────────────
#
# A file (or a fenced block within one) that the kit RENDERS from an
# independently-scanned source (docs/SKILLS.md + docs/CAPABILITIES.md — the
# seat-digest render) carries a render marker. Re-scanning the render is
# redundant (the SOURCE is already in the scan set and flags any real wall at
# its true home) and can re-red a wall phrase that only APPEARS in the render.
# Exempt by MARKER, never by path or content — a normal doc without the marker
# is still scanned. Sound ONLY because the source docs stay scanned.
_RENDER_FILE_MARKER = re.compile(
    r"never\s+edit\s+this\s+file[:\s].{0,80}?regenerate\s+with[^\n]*?seat-digest",
    re.I,
)
_DIGEST_FENCE_BEGIN = re.compile(
    r"<!--\s*substrate-kit:[\w-]*digest\s+BEGIN\b.*?-->", re.I
)
_DIGEST_FENCE_END = re.compile(
    r"<!--\s*substrate-kit:[\w-]*digest\s+END\b.*?-->", re.I
)

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

# ── Clearing — ATTACHMENT-BASED (never section-based) ─────────────────────────
#
# A matched wall clears ONLY when a repudiation / date marker is ATTACHED to the
# wall claim itself — in the SAME CLAUSE of the SAME physical line (or, for the
# ``FALSE "…"`` label, a quote whose content IS the matched wall phrase). A cue
# that merely shares a dated section, sits on a neighbouring bullet line, or
# appears in a different clause of the same line NEVER clears — that neighbour-
# bleed / section-sheltering blinds the gate to a genuine standing wall placed
# under a dated heading or beside an unrelated repudiation (adversarial review,
# fm ORDER 048). Safety wins: a false positive that stays red is cheaper than a
# real wall that goes green.

# Repudiation / correction cues (case-insensitive). Matched against the CLAUSE
# that contains the wall phrase, so the correction has to be about THIS wall.
_REPUDIATION_CUES = re.compile(
    r"no\s+standing|"
    r"not\s+a\s+wall|"
    r"not\s+walled|"  # "Merging … is NOT walled" — a direct repudiation.
    r"corrects?\s+a\s+prior\s+false|"  # "corrects a prior false '…' entry".
    r"do(?:es)?\s+not\s+(?:invent|record|apply|stand|hold|establish)|"  # "do not establish that agents cannot merge".
    r"don'?t\s+invent|"
    r"never\s+route\s+a\s+mergeable\s+green\s+pr\s+to\s+the\s+owner|"
    r"normal\s+agent\s+(?:action|work)|"
    r"is\s+a\s+normal\s+agent|"
    r"not\s+an\s+owner\s+action|"
    r"(?:merging\s+)?works?\s+agent[-\s]side|"
    r"land\s+your\s+own|"
    r"no\s+longer\s+(?:applies|a\b|an\b|the\b|stands|holds)|"
    r"\bthe\s+old\b|"
    r"proven\s+(?:repeatedly|by\b|~?\d)|"
    # ── G2 (v1.20.2): same-clause repudiation cues (each still requires the
    # repudiating context — never clears on a bare trigger phrase) ──
    r"(?:never|not)\s+a\s+standing\b[^.\n]{0,40}?\bwall\b|"  # "never a standing '…' wall".
    r"was\s+(?:based\s+on\s+)?a\s+false\s+(?:standing\s+)?wall|"  # "was (based on) a false (standing) wall".
    r"does(?:n'?t|\s+not)\s+reproduce",  # "does not reproduce".
    re.I,
)
# G2: a bare "false standing wall" clears ONLY when accompanied by a SECOND
# repudiation signal (superseded / proven) in the same clause — the two-signal
# bar keeps it from clearing on the phrase alone.
_FALSE_STANDING_WALL = re.compile(r"false\s+standing\s+wall", re.I)
_SUPERSEDE_OR_PROVEN = re.compile(r"\bsuperseded\b|\bproven\b", re.I)
# The repo's repudiation label: FALSE "…" / false "…". The uppercase bare token
# is the canonical marker (matched in-clause). The lowercase QUOTED form only
# clears when the QUOTED CONTENT contains the matched wall phrase — i.e. it is
# THIS wall that is being called false ('corrects a prior false "self-merge
# classifier"'), not an unrelated false-quote elsewhere in the sentence.
_FALSE_LABEL = re.compile(r"\bFALSE\b")
_FALSE_QUOTE = re.compile(r"\bfalse\s+[\"“'`]([^\"”'`]*)[\"”'`]", re.I)
# G4 (v1.20.2): position-aware "false/superseded AFTER the quote" — the quote is
# characterised as false/superseded IMMEDIATELY after its closing quote, same
# clause ('"…self-merge classifier…" was a false standing wall', '"…" —
# superseded', '"…" was based on a false … wall'). The wall phrase must be
# INSIDE the quote (group 1), and only a dash / "was" / "is" may sit between the
# quote and the false/superseded marker (attachment-tight — an unrelated quote
# elsewhere in the sentence cannot clear a bare wall).
_QUOTE_THEN_FALSE = re.compile(
    r"[\"“'`]([^\"”'`]*)[\"”'`]"
    r"\s*(?:[—–-]\s*)?"
    r"(?:\(?\s*(?:was|is)\s+)?"
    r"(?:based\s+on\s+a\s+false[^.\n]*?\bwall\b|a\s+false\s+standing\s+wall|superseded)",
    re.I,
)

# Markdown emphasis / code markers stripped before running the CLEARING cues so
# a bolded repudiation ("they do **not** establish …") still matches. Only the
# clearing pass strips them — the blocklist match is left untouched.
_EMPHASIS = re.compile(r"[*`]")

# ── Capability families — P2 wrapped-lookback same-capability gate ─────────────
#
# The wrapped-sentence lookback (see :func:`is_cleared`) lets a repudiation on
# the PREVIOUS line clear a wall that wraps onto the current line. Without a
# gate, a prior-line clause that repudiates a DIFFERENT capability ("Pushing is
# NOT walled …, and" ↑ "agents cannot merge …") would bleed onto — and wrongly
# clear — the current wall (follow-up hardening (a) from PR #549's card). A
# bridge is now allowed only when the prev-line trailing clause names the SAME
# capability family as the current wall phrase, or names no capability at all (a
# genuine sentence continuation). It can only ADD reds — never blind the gate.
_CAP_FAMILY_PATTERNS: tuple[tuple[str, "re.Pattern[str]"], ...] = (
    (
        "merge",
        re.compile(
            r"self[-\s]?merge|auto[-\s]?merge|\bmerg(?:e|es|ed|ing)\b|"
            r"ready[-\s]?flip|\barm(?:s|ed|ing)?\b|\bland(?:s|ed|ing)?\b",
            re.I,
        ),
    ),
    ("deploy", re.compile(r"\bre?deploy(?:s|ed|ing|ment)?\b", re.I)),
    ("push", re.compile(r"\bpush(?:es|ed|ing)?\b", re.I)),
    (
        "branch",
        re.compile(r"branch\s+deletion|delete[sd]?\s+(?:a\s+|the\s+)?branch(?:es)?", re.I),
    ),
    (
        "infra",
        re.compile(
            r"\brailway\b|\benv(?:ironment)?\b|\binfra(?:structure)?\b|"
            r"\bvariables?\b|\bsecrets?\b",
            re.I,
        ),
    ),
)


def _capability_families(text: str) -> frozenset[str]:
    """The capability families named in ``text`` (merge/deploy/push/branch/infra).

    Used only by the P2 wrapped-lookback gate to compare the previous line's
    trailing-clause repudiation against the current wall's capability so a
    repudiation of an UNRELATED capability can't bridge across the wrap.
    """
    return frozenset(name for name, pat in _CAP_FAMILY_PATTERNS if pat.search(text))

# Strong clause separators. A wall clears only via a cue in the SAME clause, so
# "Nothing here is 'not walled'; agents cannot merge" does NOT clear (the cue
# and the wall are in different clauses). Comma is NOT a separator — too weak.
_CLAUSE_SEP = re.compile(
    r";|—|:\s|\.\s|"
    # FIX A (v1.20.2): a mid-line contrast / coordination conjunction after a
    # comma is a clause boundary too — otherwise a capability-AGNOSTIC cue (e.g.
    # "does not reproduce") in the first half blinds a genuine wall in the
    # second ("… does not reproduce now, but agents cannot merge in prod"). The
    # split — not the family gate — is what closes that blind: an empty-family
    # cue lands in its own clause, leaving the wall's clause cue-less → RED.
    r",\s*(?:but|however|yet|and|so|though|although|whereas|while|still)\b",
    re.I,
)

# A wall sentence can WRAP onto its line from the one above ("… no standing\n
# 'classifier-denied' merge wall …"). A tight one-line lookback lets the
# repudiation on the previous line clear it — but ONLY when the current line is
# a genuine continuation, never a contrasting neighbour ("… agent-side\n but
# agents cannot merge") whose "but" marks a distinct wall clause.
_CONTRAST_START = re.compile(
    r"^\s*>?\s*(?:but|however|except|though|although|yet|whereas|still|"
    r"nonetheless|nevertheless)\b",
    re.I,
)
_SENTENCE_END = re.compile(r"[.!?]\s*[)\"”'`*]*\s*$")

# Inline dated-record markers (this clause is itself a dated record).
_DATED_LINE = re.compile(
    r"\bLAST-VERIFIED\b|\bSUPERSEDED\b|"
    r"[—·(]\s*\d{4}-\d{2}-\d{2}|"
    r"\bverified\s+\d{4}-\d{2}-\d{2}",
)
# A bullet that STARTS with a date is an attached dated-record row (append-log
# form) — the date is on the item's own first line, so its lines are records.
_DATED_BULLET = re.compile(r"^\s*[-*]\s+\d{4}-\d{2}-\d{2}\b")
# A markdown heading.
_HEADING = re.compile(r"^\s*#{1,6}\s+(.*)$")
_HISTORICAL_HEADING = re.compile(r"append\s+log|historical", re.I)


class RawHit(NamedTuple):
    """One false-wall match in a text: 1-based ``line``, ``phrase``, ``rule``."""

    line: int
    phrase: str
    rule: str


def _clause_at(line: str, idx: int) -> str:
    """Return the CLAUSE of ``line`` that spans character offset ``idx``.

    Clauses are split on strong separators (:data:`_CLAUSE_SEP`). A cue only
    clears a wall when it lands in the SAME clause as the wall phrase, so a
    repudiation in a different clause of the same line ("Nothing here is 'not
    walled'; agents cannot merge …") does not bleed onto the wall. Offset-based
    (not phrase-find-based) so a SECOND occurrence of a repeated phrase is graded
    in its OWN clause, not the first occurrence's (P3 position-awareness).
    """
    lo, hi = 0, len(line)
    for m in _CLAUSE_SEP.finditer(line):
        if m.start() <= idx:
            lo = m.end()  # a separator ends the clause before the offset
        else:
            hi = m.start()  # …and the next separator ends the offset's clause
            break
    return line[lo:hi]


def _clause_containing(line: str, phrase: str) -> str:
    """The clause of ``line`` containing the FIRST occurrence of ``phrase``.

    Falls back to the whole line when the phrase is not found verbatim (e.g. the
    synthetic wrapped-lookback ``combined`` string).
    """
    idx = line.find(phrase)
    return line if idx < 0 else _clause_at(line, idx)


def _false_quote_attached(line: str, phrase: str) -> bool:
    """True when a ``false "…"`` label on ``line`` names THIS wall — the matched
    wall ``phrase`` is contained in the quoted content. An unrelated false-quote
    ('a prior false "weather" note aside, sessions may not self-merge') does not
    clear, because "weather" does not contain the wall phrase. Line-wide by
    phrase (used only on the synthetic wrapped-lookback string, where character
    offsets are meaningless)."""
    p = phrase.lower().strip()
    if not p:
        return False
    for pat in (_FALSE_QUOTE, _QUOTE_THEN_FALSE):
        if any(p in m.group(1).lower() for m in pat.finditer(line)):
            return True
    return False


def _false_quote_covers(line: str, start: int, end: int) -> bool:
    """True when the match span ``[start, end)`` lies INSIDE a ``false "…"``
    quote's content. Position-aware (P3): a genuine wall OUTSIDE the quote on the
    same physical line ('false "self-merge classifier" aside — the real
    self-merge classifier still blocks') is NOT cleared, because only the quoted
    occurrence's span is covered."""
    for pat in (_FALSE_QUOTE, _QUOTE_THEN_FALSE):
        for m in pat.finditer(line):
            qs, qe = m.span(1)
            if qs <= start and end <= qe:
                return True
    return False


def _last_clause(line: str) -> str:
    """The final clause of ``line`` (text after the last strong separator)."""
    seps = list(_CLAUSE_SEP.finditer(line))
    return line[seps[-1].end() :] if seps else line


def _wall_starts_line(line: str, phrase: str) -> bool:
    """True when ``phrase`` sits in the FIRST clause of ``line`` (no strong
    separator precedes it) — i.e. the wall's sentence may have begun above."""
    idx = line.find(phrase)
    return idx >= 0 and not _CLAUSE_SEP.search(line[:idx])


def _first_clause(line: str) -> str:
    """The first clause of ``line`` (text before the first strong separator).

    Mirror of :func:`_last_clause`; used by the G1 bounded lookforward so a
    repudiation that WRAPS onto the next line clears the wall that ended the
    current line."""
    m = _CLAUSE_SEP.search(line)
    return line[: m.start()] if m else line


def _wall_ends_line(
    line: str, phrase: str, match_span: tuple[int, int] | None
) -> bool:
    """True when the wall sits in the LAST clause of ``line`` (no strong
    separator follows it) — i.e. the wall's sentence may continue below. The
    forward-facing mirror of :func:`_wall_starts_line`, gating the G1 lookforward
    the same way the lookback is gated by ``_wall_starts_line``."""
    if match_span is not None:
        idx = match_span[1]
    else:
        pos = line.find(phrase)
        if pos < 0:
            return False
        idx = pos + len(phrase)
    return not _CLAUSE_SEP.search(line[idx:])


# A markdown list bullet start (used as a G1 lookforward STOP boundary).
_NEW_BULLET = re.compile(r"^\s*[-*]\s")


def _clause_cleared(
    clause: str,
    line: str,
    phrase: str,
    *,
    match_span: tuple[int, int] | None = None,
) -> bool:
    """Run the attachment cues over one ``clause``.

    The ``false "…"`` label clears position-aware when ``match_span`` is given
    (the quote must SPAN this match — P3), and line-wide by ``phrase`` otherwise
    (the synthetic wrapped-lookback string, where offsets are meaningless)."""
    scrubbed = _EMPHASIS.sub("", clause)
    if _DATED_LINE.search(clause):
        return True
    # FIX A (v1.20.2) hardening: a cue in this clause clears the wall ONLY when
    # it is not a DIFFERENT-capability bleed. If the clause's non-wall remainder
    # names a capability family disjoint from the wall's own family, the cue is
    # about a different capability and must not clear this wall (mirror of the
    # G1 / wrapped-lookback family gate). This is hardening only — an
    # empty-family cue ("does not reproduce") is NOT gated here; the
    # comma-conjunction clause split (above) is what stops that class of bleed.
    wall_fams = _capability_families(phrase)
    rest_fams = _capability_families(scrubbed.replace(phrase, " ", 1))
    cue_family_conflict = bool(
        wall_fams and rest_fams and rest_fams.isdisjoint(wall_fams)
    )
    if not cue_family_conflict:
        if _REPUDIATION_CUES.search(scrubbed):
            return True
        # G2: bare "false standing wall" clears only with a second repudiation
        # signal (superseded / proven) in the same clause.
        if _FALSE_STANDING_WALL.search(scrubbed) and _SUPERSEDE_OR_PROVEN.search(
            scrubbed
        ):
            return True
    if _FALSE_LABEL.search(clause):
        return True
    if match_span is not None:
        return _false_quote_covers(line, match_span[0], match_span[1])
    return _false_quote_attached(line, phrase)


def is_cleared(
    line: str,
    phrase: str,
    *,
    in_dated_block: bool,
    in_historical: bool,
    prev_line: str | None = None,
    next_lines: list[str] | None = None,
    match_span: tuple[int, int] | None = None,
) -> bool:
    """True when the matched wall ``phrase`` on ``line`` must NOT count.

    Clearing is ATTACHMENT-BASED: a cue clears only when it is attached to the
    wall claim — in the same clause (repudiation cues, inline date, uppercase
    ``FALSE`` label) or naming the wall in a ``false "…"`` quote. Section state
    (:data:`_DATED_BULLET` append-log rows, ``append log`` / ``historical``
    headings) is the one sanctioned non-clause path and is genuinely attached: a
    ``- YYYY-MM-DD`` bullet carries its date on its own first line.

    ``match_span`` (P3) makes clearing position-aware: the wall's clause is the
    clause spanning that offset (so a SECOND occurrence of a repeated phrase is
    graded in its own clause), and a ``false "…"`` quote clears the match only
    when it SPANS it — a genuine wall sharing a line with a repudiated false
    quote is no longer masked.

    One tight cross-line allowance: when the wall opens ``line`` (its sentence
    wrapped from above) and the line is NOT a contrasting neighbour, the
    previous line's trailing clause is prepended so a wrapped repudiation ("…no
    standing\\n 'classifier-denied' merge wall") still clears. A "but …" / dated
    neighbour never qualifies, and (P2) a prev-line clause that repudiates a
    DIFFERENT capability family than this wall never bridges either.
    """
    if in_dated_block or in_historical:
        return True
    clause = (
        _clause_at(line, match_span[0]) if match_span is not None else _clause_containing(line, phrase)
    )
    if _clause_cleared(clause, line, phrase, match_span=match_span):
        return True
    # Tight one-line lookback for a wrapped repudiation.
    if (
        prev_line is not None
        and prev_line.strip()
        and not _HEADING.match(prev_line)
        and not _DATED_BULLET.match(prev_line)
        and not _SENTENCE_END.search(prev_line)
        and not _CONTRAST_START.match(line)
        and _wall_starts_line(line, phrase)
    ):
        prev_clause = _last_clause(prev_line)
        # P2 same-capability gate: only bridge when the prev-line clause's
        # repudiation is about the SAME capability as this wall (or names no
        # capability at all — a genuine sentence continuation). A prev clause
        # naming a DIFFERENT family repudiates an unrelated capability and must
        # not clear this wall.
        wall_fams = _capability_families(phrase)
        prev_fams = _capability_families(prev_clause)
        different_capability = bool(wall_fams and prev_fams and prev_fams.isdisjoint(wall_fams))
        if not different_capability:
            combined = prev_clause + " " + clause
            if _clause_cleared(combined, line, phrase):
                return True
    # G1 (v1.20.2): tight bounded lookforward — the forward-facing mirror of the
    # lookback. When the wall CLOSES its line and the sentence has NOT ended, the
    # repudiation may wrap onto the next line(s). Scan 1–2 lines forward ONLY
    # within the SAME bullet / blockquote / paragraph — STOP at a blank line, a
    # new `- `/`* ` bullet, a heading, a dated bullet, or a contrasting
    # neighbour ("but …"). The P2 same-capability family gate applies exactly as
    # in the lookback: a forward clause naming a DIFFERENT capability family than
    # this wall never bridges. This can only ADD clears for genuine wrapped
    # repudiations; it never blinds the gate to a standing wall.
    if (
        next_lines
        and _wall_ends_line(line, phrase, match_span)
        and not _SENTENCE_END.search(line)
    ):
        wall_fams = _capability_families(phrase)
        acc = clause
        for fwd in next_lines[:2]:
            if not fwd.strip():
                break
            if (
                _HEADING.match(fwd)
                or _DATED_BULLET.match(fwd)
                or _NEW_BULLET.match(fwd)
                or _CONTRAST_START.match(fwd)
            ):
                break
            fwd_clause = _first_clause(fwd)
            fwd_fams = _capability_families(fwd_clause)
            if wall_fams and fwd_fams and fwd_fams.isdisjoint(wall_fams):
                break
            acc = acc + " " + fwd_clause
            if _clause_cleared(acc, line, phrase):
                return True
            if _SENTENCE_END.search(fwd):
                break
    return False


def match_blocklist(line: str) -> tuple[str, str] | None:
    """Return (rule_name, matched_phrase) for the FIRST false-wall match on
    ``line`` (blocklist order), or ``None``. Retained for :func:`explain_wall`,
    which grades a bare phrase; the line scanner uses
    :func:`match_blocklist_all`."""
    matches = match_blocklist_all(line)
    if matches:
        rule, phrase, _s, _e = matches[0]
        return rule, phrase
    return None


def match_blocklist_all(line: str) -> list[tuple[str, str, int, int]]:
    """Every false-wall match on ``line`` as ``(rule, phrase, start, end)``.

    In blocklist (rule) order, and within a rule in position order, so the FIRST
    entry reproduces the legacy :func:`match_blocklist` result. Returning ALL
    matches (P3) lets the scanner grade each independently and un-mask a genuine
    wall that shares a line with a repudiated ``false "…"`` quote — the cleared
    quote-hit no longer ends the line."""
    out: list[tuple[str, str, int, int]] = []
    for name, pat in _BLOCKLIST:
        for m in pat.finditer(line):
            out.append((name, m.group(0), m.start(), m.end()))
    owner_gated = _OWNER_GATED.search(line)
    if owner_gated and _OWNER_GATED_DIRECTIVE.search(line):
        out.append(
            ("owner-gated-rule", owner_gated.group(0), owner_gated.start(), owner_gated.end())
        )
    review_label = _REVIEW_LABEL.search(line)
    if review_label and _PROHIBITION_FRAME.search(line):
        out.append(
            (
                "review-label-prohibition",
                review_label.group(0),
                review_label.start(),
                review_label.end(),
            )
        )
    return out


def scan_text(text: str, *, is_render_path: bool = False) -> list[RawHit]:
    """Scan ``text`` line by line, returning every uncleared false-wall hit.

    The stateful loop tracks dated-record blocks (a ``- YYYY-MM-DD …`` bullet
    and its continuation) and historical headings (``## Append log`` /
    ``historical``) so a match inside a history section clears. Shared by the
    engine leg and the standalone ``tools/`` wrapper — the single home for the
    grammar (no duplicate logic).

    Every wall match on a line is graded independently (P3), reporting the FIRST
    UNCLEARED one — so a genuine wall sharing a line with a repudiated
    ``false "…"`` quote still reds, while the line still yields at most one hit
    (the legacy count contract).

    ``is_render_path`` (FIX B, v1.20.2) enables the class (b) generated-render
    exemption ONLY when the file being scanned IS the kit's known render path
    (``docs/seat-digest.md`` per :func:`seat_digest_relpath`). The render marker
    / digest fence is NOT honoured on any other file — an author cannot
    blanket-exempt a real doc (``CONSTITUTION.md`` / ``CAPABILITIES.md``) by
    pasting the marker; the exemption is sound only because the render's SOURCE
    docs are independently scanned, which is guaranteed only for that one path.
    """
    # Class (b): the whole known-render file is exempt (its source docs are
    # scanned independently). Marker gated to the render path (FIX B).
    if is_render_path and _RENDER_FILE_MARKER.search(text):
        return []

    hits: list[RawHit] = []
    in_historical = False
    in_digest_fence = False
    prev_line: str | None = None
    lines = text.splitlines()
    for i, line in enumerate(lines, start=1):
        # Class (b): skip lines inside a kit-generated derived-render fence
        # (<!-- substrate-kit:*-digest BEGIN … --> … <!-- … END -->) — but only
        # on the known render path (FIX B).
        if is_render_path and _DIGEST_FENCE_BEGIN.search(line):
            in_digest_fence = True
            prev_line = line
            continue
        if is_render_path and _DIGEST_FENCE_END.search(line):
            in_digest_fence = False
            prev_line = line
            continue
        if in_digest_fence:
            prev_line = line
            continue

        heading = _HEADING.match(line)
        if heading:
            in_historical = bool(_HISTORICAL_HEADING.search(heading.group(1)))

        # A dated append-log bullet ("- 2026-07-16 · …") clears ONLY its own
        # physical line — the date attaches to the row it heads, never to a
        # continuation line that carries a distinct wall (neighbour-bleed).
        in_dated_block = bool(_DATED_BULLET.match(line))
        next_lines = lines[i : i + 2]  # i is 1-based; lines[i] is the next line
        for rule, phrase, start, end in match_blocklist_all(line):
            if not is_cleared(
                line,
                phrase,
                in_dated_block=in_dated_block,
                in_historical=in_historical,
                prev_line=prev_line,
                next_lines=next_lines,
                match_span=(start, end),
            ):
                hits.append(RawHit(i, phrase.strip(), rule))
                break  # ≤1 finding per line (legacy count contract)
        prev_line = line
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


# Per-repo product-copy allowlist (FIX D, v1.20.2): NOT a bespoke path here.
# false-wall findings ride the strict loop into `cmd_check`, which post-processes
# EVERY finding through the repo's generic REASON-REQUIRED allowlist seam
# (`engine.checks.allowlist.load_allowlist` + `apply_allowlist`, file
# `<state_dir>/check-exceptions.yml`, schema `{path, kind, reason REQUIRED,
# triaged, by, verdict?}`). An entry suppresses a `false-wall:<rule>` finding
# only on an exact path+kind match WITH a non-empty reason; a reason-less entry
# suppresses nothing and is itself reported as a `kind=allowlist` finding
# (fail-CLOSED, loud). The earlier bespoke `_finding_excepted` path (exact
# path+kind+optional phrase but reason-OPTIONAL — fail-open) was removed in
# favour of that audited seam.


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
    # FIX B (v1.20.2): the ONE file on which the class (b) generated-render
    # exemption is honoured — the kit's known render path. Any other file
    # carrying the render marker/fence is still fully scanned.
    try:
        render_rel = seat_digest_relpath(config)
    except Exception:  # noqa: BLE001 — a missing/odd config never breaks the gate
        render_rel = "docs/seat-digest.md"
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
        for hit in scan_text(text, is_render_path=(rel == render_rel)):
            # S6: inline the rule's per-rule ground-truth correction (the same
            # WALL_CORRECTIONS the R6 `check --explain-wall` lookup returns) so
            # the red gate names the SPECIFIC capability truth for this rule,
            # not just the generic blurb. Detection is unchanged — same
            # `false-wall:<rule>` kind, same paths, same exit-affecting loop;
            # only the human-readable message gains the per-rule sentence.
            correction = WALL_CORRECTIONS.get(hit.rule, _UNKNOWN_RULE_CORRECTION)
            findings.append(
                Finding(
                    rel,
                    f"false-wall:{hit.rule}",
                    (
                        f"line {hit.line}: false agent-capability wall "
                        f"{hit.phrase!r} [{hit.rule}] — {correction} "
                        "Correct the line, or date-stamp/repudiate it if it "
                        "records a genuine momentary refusal."
                    ),
                )
            )
    return findings


# --- R6: per-rule ground-truth corrections for `check --explain-wall` ---
# check_no_false_walls flags a line as a false agent-capability wall; the
# `bootstrap.py check --explain-wall <phrase>` lookup (alias `--why`) answers
# "which rule, and what's the ground truth?" Each rule name match_blocklist can
# return maps to one capability-positive correction sentence. The shared tail
# (point at the CAPABILITIES.md dated-row form) is appended by the CLI, not
# here. tests/test_explain_wall.py asserts every rule in all_rule_names() has an
# entry, so a future blocklist rule cannot ship without its correction.
WALL_CORRECTIONS: dict[str, str] = {
    "agent-negated-capability": (
        "Merging, pushing, deploying, arming auto-merge, ready-flipping and "
        "landing PRs are all normal agent work — there is no owner-imposed "
        "capability limit on them."
    ),
    "agent-negated-infra-mutation": (
        "Agents mutate infrastructure — Railway variables, env, deploys, config "
        "— as normal work via the documented paths; only owner-console settings "
        "and secrets are genuinely gated."
    ),
    "capability-is-owner-authority": (
        "Merging is not owner-only authority: agents merge their own green PRs "
        "directly (MCP/REST), and the only merge gate is CI green."
    ),
    "capability-asserted-owner-only": (
        "This is not owner-only — merging, deploying and pushing are ordinary "
        "agent actions; never route a mergeable green PR to the owner."
    ),
    "standing-platform-wall": (
        "A platform refusal is a transient per-call classifier state, not a "
        "standing wall: attempt once, record the venue + exact error, and route "
        "around it."
    ),
    "classifier-denied-standing": (
        "A classifier denial is momentary and specific to one call, not a "
        "standing rule — re-attempt on material change rather than recording it "
        "as a wall."
    ),
    "classifier-denied-since": (
        "A dated 'denied since' line records one past refusal, not a durable "
        "wall; the capability still holds — re-verify rather than assume."
    ),
    "classifier-denies-merge": (
        "Merging works agent-side; a merge refusal is a one-off transient — "
        "attempt once and record the exact error, do not generalize it."
    ),
    "agents-do-not-land": (
        "Agents do land PRs: they land their own and sibling green PRs directly "
        "on green CI."
    ),
    "agents-cannot-land": (
        "Agents can land PRs — landing a green PR is normal agent work, not an "
        "owner-only step."
    ),
    "never-agent-side": (
        "This works agent-side: merging, deploying and pushing are all done by "
        "agents through the documented paths."
    ),
    "never-arm-automerge": (
        "Arming auto-merge is normal agent work — a claude/* PR arms it at open "
        "and lands on green CI."
    ),
    "owner-is-merge-authority": (
        "The owner is not the merge authority: the only merge gate is CI green, "
        "and agents merge their own green PRs."
    ),
    "the-owner-merges": (
        "Agents merge their own green PRs; the owner need not click merge for a "
        "mergeable green PR."
    ),
    "self-merge-classifier": (
        "Self-merge is normal agent work; a classifier refusal on one call is "
        "transient — attempt once, record the error, and route around it."
    ),
    "agent-unlandable": (
        "An agent PR is landable: it lands on green CI like any other, by direct "
        "merge or the auto-merge-enabler."
    ),
    "must-not-land": (
        "A green PR does land — owner direction (a session prompt or in-chat "
        "instruction) is itself the review; only a do-not-automerge label holds "
        "a PR back."
    ),
    "owner-gated-rule": (
        "Most actions are not owner-gated: merging, deploying and pushing are "
        "agent work — only console settings, rulesets, secrets and protected "
        "main-push are genuinely gated."
    ),
    "review-label-prohibition": (
        "The needs-hermes-review review gate is retired; every green PR "
        "auto-merges, so a review-label prohibition no longer applies."
    ),
}

_UNKNOWN_RULE_CORRECTION = (
    "This phrase matched the false-wall blocklist but has no dedicated "
    "correction yet — the ground truth still holds: merging, deploying and "
    "pushing are normal agent work."
)


def all_rule_names() -> frozenset[str]:
    """Every rule name ``match_blocklist`` can return — the coverage surface
    WALL_CORRECTIONS must cover. Used by the R6 explain-wall lookup and its
    coverage test so a new blocklist rule can't ship without a correction."""
    return frozenset(name for name, _ in _BLOCKLIST) | {
        "owner-gated-rule",
        "review-label-prohibition",
    }


def explain_wall(phrase: str) -> tuple[str, str, str] | None:
    """R6: map ``phrase`` to ``(rule, matched_phrase, correction)`` or ``None``
    if no false-wall rule matches. Reuses the checker's own ``match_blocklist``
    so the explanation and the check never drift. Powers
    ``bootstrap.py check --explain-wall <phrase>`` (alias ``--why``)."""
    hit = match_blocklist(phrase)
    if hit is None:
        return None
    rule, matched = hit
    return rule, matched, WALL_CORRECTIONS.get(rule, _UNKNOWN_RULE_CORRECTION)
