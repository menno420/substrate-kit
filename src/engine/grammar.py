"""Control-plane grammar — THE single source of truth (EAP §6.8).

Why + provenance: the EAP program review (menno420/superbot
``docs/eap/eap-program-review-2026-07-10.md`` §6 item 8) found the
control-plane grammar — the ORDER header + required fields, the ``orders:
acked=/done=/claimed-by:`` status line, the six-field ⚑ OWNER-ACTION format,
the ``kit:``/``check:``/``engaged:`` heartbeat self-report, the work-claim
bullet — living implicitly in the planted control templates while each
enforcer re-derived its own copy (``check_inbox_append``,
``check_owner_actions``, ``check_status_current``, ``check_claims``,
``currency``). Writer and enforcer can silently drift apart when the grammar
has no owner: the manager's own seeded orders once failed the kit's 1.7.0
grammar. This module makes the grammar a kit-owned CONSTANT with exactly one
home; the writer half (templates, ``control/README.md`` teaching text) and
the enforcer half (the checkers) both point here, and
``tests/test_grammar.py`` pins writer↔enforcer agreement — the format the
templates teach must satisfy the regexes the enforcers run.

Layout: one section per grammar surface, each carrying (a) the tokens /
field lists / compiled regexes the enforcers consume and (b) a canonical
example renderer — the smallest text that a correct writer produces and a
correct enforcer accepts. The examples are the agreement-test fixtures; they
double as reference text for docs.

Behavioral contract: the constants here are byte-identical moves of the
regexes the checkers shipped with — centralizing the grammar changed **no
behavior** (pinned by the pre-existing checker suites passing unchanged).
House-style note (D-7): these are declared grammar, deliberately hardcoded —
a consumer that truly needs a different grammar forks the constant, the kit
does not grow config knobs for it. Stdlib only, no engine imports — this
module sits below every checker.
"""

from __future__ import annotations

import re

# ── control/inbox.md — the ORDER block (manager-written, append-only) ───────
#
# Taught in control/README.md § "inbox.md order format":
#   ## ORDER <nnn> · <ISO8601> · status: <state>     [# optional manager note]
#   priority: P0 | P1 | P2
#   do: <pointer to a committed doc/section + the ask>
#   why: <one line>
#   done-when: <acceptance test>
# The `·` is U+00B7 (the protocol's separator). A trailing `#` note is
# allowed on the header (the README's own example carries one), so each
# header value is read as its first token. Enforced by check_inbox_append.

ORDER_HEADER_PREFIX = "## ORDER "
ORDER_HEADER_RE = re.compile(r"^## ORDER \S+ · .+ · status: \S+")
# Every ORDER block carries these body fields, one per line.
ORDER_REQUIRED_FIELDS = ("priority:", "do:", "why:", "done-when:")


def order_block_example() -> str:
    """Canonical ORDER block — what a correct manager append looks like."""
    return (
        "## ORDER 001 · 2026-07-10T12:00Z · status: new\n"
        "priority: P1\n"
        "do: read docs/example.md §1 and execute the ask it names\n"
        "why: one line of motivation\n"
        "done-when: the acceptance test in docs/example.md §1 passes\n"
    )


# ── control/status*.md — the orders ack/done line (heartbeat-side) ──────────
#
# Taught in control/README.md § "status.md format" and § "Claiming an order":
#   orders: acked=<ids> done=<ids> [claimed-by: <ids> <lane-or-session> <ISO8601>]
# The ids tokens are `,`/`+`-separated and may carry inclusive ranges
# (`001-006`); the claimed-by annotation is three whitespace tokens — the ids
# may be `+`-joined (`007+008`) and the lane token may itself carry hyphens
# (`coordinator-lane`), so the lane is a whole token, never parsed. Enforced
# by check_claims (order-claim hygiene).

ORDERS_LINE_RE = re.compile(r"^orders:\s*(.*)$", re.MULTILINE)
ORDERS_DONE_RE = re.compile(r"\bdone=(\S*)")
ORDERS_CLAIMED_BY_RE = re.compile(r"claimed-by:\s*(\S+)\s+(\S+)\s+(\S+)")


def orders_line_example(*, claimed: bool = False) -> str:
    """Canonical ``orders:`` line (optionally carrying a live claim)."""
    line = "orders: acked=001-003 done=001,002"
    if claimed:
        line += " claimed-by: 003 example-lane 2026-07-10T12:00Z"
    return line + "\n"


# ── control/status*.md — the `updated:` heartbeat line ──────────────────────
#
# The heartbeat's first field: `updated: <ISO8601>` — stale = the manager
# treats the Project as dark. The value is the line's first token (ISO-8601,
# minutes or seconds precision, `Z` or offset). Enforced by
# check_status_current (parse_heartbeat).
#
# The prefix match is CASE-INSENSITIVE (the KIT_LINE_RE leniency instinct:
# accepting an alternate only ever *withholds* a red, never adds one). A live
# heartbeat written as `Updated:` failed `[status-no-heartbeat]` and had to
# be hand-fixed in-PR (kit #326, 2026-07-13) — a casing slip is a writer
# spelling variant, not a dead heartbeat, so the enforcer forgives it. The
# canonical WRITER form stays lowercase `updated:` (the example below, every
# planted template, control/README.md's taught block).

UPDATED_LINE_RE = re.compile(r"^updated:\s*(\S+)", re.MULTILINE | re.IGNORECASE)


def updated_line_example() -> str:
    """Canonical ``updated:`` heartbeat line."""
    return "updated: 2026-07-10T12:00:00Z\n"


# ── control/status*.md — the `kit:` self-report line (ORDER 003) ────────────
#
# Taught in control/README.md § "status.md format":
#   kit: v<X.Y.Z> · check: green|red · engaged: yes|no
# Parsed leniently — real heartbeats decorate the line, so the version is the
# first `v<digit...>` token after `kit:` and the check/engaged fields are
# scanned anywhere on the line. The line anchor is lenient too: adopters
# embed the heartbeat as a markdown bullet with a bold label (venture-lab's
# live shape, found at the v1.10.1 wave: `- **kit heartbeat:** kit: v… ·
# check: … · engaged: …`), so an optional leading list marker and/or
# `**bold label**` prefix is accepted before `kit:` — the old start-of-line
# anchor silently degraded that row to "no `kit:` line" in the fleet
# registry and lost its engaged signal. Consumed by currency.parse_kit_line
# (the fleet registry's self-report evidence).
#
# The leniency has a hard edge (hardening report 2026-07-12 §a.4, map §(b)
# row 8): the optional bold group cannot contain the `kit:` token itself, so
# the bold-label form `- **kit:** v…` does NOT parse — pokemon-mod-lab's live
# heartbeat wrote exactly that shape and the registry read "no `kit:` line".
# The negative renderer below is the taught counter-example; the control
# templates carry it verbatim (test-pinned, the shared-pin precedent) so the
# writer-side warning and the enforcer's rejection cannot drift.

KIT_LINE_RE = re.compile(
    r"^(?:[-*+]\s+)?(?:\*\*[^*\n]+\*\*\s*)?kit:\s*(.*)$",
    re.MULTILINE,
)
KIT_VERSION_TOKEN_RE = re.compile(r"\bv(\d[\w.\-]*)")
KIT_CHECK_FIELD_RE = re.compile(r"\bcheck:\s*(green|red)\b")
KIT_ENGAGED_FIELD_RE = re.compile(r"\bengaged:\s*(yes|no)\b")


def kit_line_example(version: str = "1.2.3") -> str:
    """Canonical ``kit:`` self-report line for ``version``."""
    return f"kit: v{version} · check: green · engaged: yes\n"


def kit_line_negative_example(version: str = "1.2.3") -> str:
    """The bold-label form ``KIT_LINE_RE`` REJECTS — the taught negative.

    The ``kit:`` token itself sits inside the bold, and the optional bold
    group cannot contain the token, so the registry reads the row as "no
    ``kit:`` line" and the lane's engaged signal silently vanishes (the
    pokemon-mod-lab live incident). A bold label *before* a plain ``kit:``
    token stays valid — see the leniency note above. Carried verbatim by
    the control templates; ``tests/test_grammar.py`` pins both that the
    templates teach this exact string and that it never parses.
    """
    return f"- **kit:** v{version} · check: green · engaged: yes\n"


# ── control/status*.md — the six-field ⚑ OWNER-ACTION format (ORDER 008) ────
#
# Taught in control/README.md § "⚑ needs-owner — the OWNER-ACTION item
# format". Canonical spelling first per field; two fields also accept a
# shorthand adopters write inline (WHY:/VERIFIED-WHEN:) because accepting an
# alternate only ever *withholds* the advisory nag, never adds one. Enforced
# by check_owner_actions.

NEEDS_OWNER_TOKEN = "⚑ needs-owner"
OWNER_ACTION_FIELDS = (
    ("WHAT:",),
    ("WHERE:",),
    ("HOW:",),
    ("WHY-IT-MATTERS:", "WHY:"),
    ("UNBLOCKS:",),
    ("VERIFIED-NEEDED:", "VERIFIED-WHEN:"),
)


def owner_action_block_example() -> str:
    """Canonical ⚑ OWNER-ACTION block — every REQUIRED field present."""
    return (
        "⚑ OWNER-ACTION\n"
        "WHAT: flip the example setting to on\n"
        "WHERE: Settings → Example → the toggle\n"
        "HOW: one checkbox\n"
        "RISK: ↩️ reversible — flip the toggle back to undo\n"
        "WHY-IT-MATTERS: the lane stalls without it\n"
        "UNBLOCKS: the next slice starts moving the moment it's done\n"
        "VERIFIED-NEEDED: attempted via the API — 403, owner-only surface\n"
    )


# ── Owner-facing output — the owner-assist standard (grounded-skills §3) ────
#
# Taught in control/README.md § "Owner-assist output standard" (canonical
# home) and the collaboration-model / CONSTITUTION / question-router
# doctrine. The structured-choice phrases are ALSO the /intake skill body's
# Q-0263.2 pins (engine.skills.skills._INTAKE_BODY) — one home, so skill
# text, template text, and enforcer cannot drift; agreement is pinned by
# tests/test_owner_assist.py. Enforced (advisory-only, §8 Q2=B) by
# check_owner_actions.
#
# Risk-class tokens are the BASE characters (no VS16 emoji selector) so the
# scan matches both the plain and the emoji-presentation spellings adopters
# write (`"↩" in "↩️ reversible"` is True).

RISK_CLASS_LABEL = "RISK:"
RISK_CLASS_TOKENS = ("✅", "↩", "⚠")
OWNER_ACTION_BLOCK_TOKEN = "⚑ OWNER-ACTION"
# Q-0263.2 pinned phrases — a decision put to the owner is options A/B(/C)
# with a **bolded recommendation**, answerable with one letter; an ask that
# requires the owner to parse, derive, or transform anything is a drafting
# defect, never an owner task.
STRUCTURED_CHOICE_PHRASES = (
    "**bolded recommendation**",
    "answerable with one letter",
    "parse, derive, or transform",
)
# The destination anti-pattern (the Q-0263 incident class): a WHERE: value
# naming a settings-like surface with no deep shape at all — no URL, no
# click-path arrow, no path. "Settings → Rules → the main ruleset" is fine;
# a bare "go to settings" is not.
VAGUE_DESTINATION_WORDS = ("settings", "console", "dashboard", "portal", "admin")
DESTINATION_SHAPE_MARKS = ("http", "→", "/", ">")


def risk_class_line_example() -> str:
    """Canonical ``RISK:`` line — one class token + how to undo."""
    return "RISK: ↩️ reversible — delete the variable to undo.\n"


def structured_choice_example() -> str:
    """Canonical structured-choice question (the Q-0263.2 shape)."""
    return (
        "Q1 — Default channel for large owner-facing outputs?\n"
        "  A) Rendered link + 3-line digest in chat.\n"
        "  B) Full text in chat every time.\n"
        "  RECOMMENDATION: A — one tap on a phone; B stays the fallback.\n"
    )


# ── docs/CAPABILITIES.md — the venue-scoped capability ledger (§4.2) ─────────
#
# Taught in the planted ledger (CAPABILITIES.md.tmpl § "Append log"):
#   - YYYY-MM-DD · capability|wall · <venue> · finding · evidence · workaround
# The `·` is U+00B7 (the protocol's separator). The venue token scopes a
# finding to where it was verified — the grounded-skills evidence base
# (fleet night review 2026-07-12) saw ONE operation behave three ways in one
# night depending on venue, so a flat CAN/CANNOT ledger is wrong somewhere by
# construction. BACKWARD-COMPATIBLE: the older five-field form without a
# venue token stays valid — readers treat it as venue `any` and enforcers
# never flag it (an old line must not become advisory noise). Enforced
# (advisory-only) by check_capability_xref; the kit-owned seed block between
# the fence markers below is refreshed at upgrade by
# engine.upgrade.refresh_capability_seed — the ONLY channel that reaches a
# consumer-edited ledger (--apply-docs never covers one).

CAPABILITY_VENUE_TOKENS = (
    "owner-live",
    "autonomous-project",
    "routine-fired",
    "subagent",
    "any",
)
CAPABILITY_ENTRY_TAGS = ("capability", "wall")
# The taught append-line format — the template carries this string verbatim
# (test-pinned agreement, the owner-assist shared-pin precedent), so the
# writer half and the enforcer half cannot drift.
CAPABILITY_LOG_TAUGHT_FORMAT = (
    "- YYYY-MM-DD · capability|wall · <venue> · finding · evidence · workaround"
)
# An append-log entry line: a leading ISO date, then the ·-separated fields.
CAPABILITY_LOG_LINE_RE = re.compile(r"^- (20\d{2}-\d{2}-\d{2}) · (.+)$")
# What field 3 looks like when the writer MEANT a venue: one lowercase
# hyphenated token, no spaces. A field-3 value with spaces is an old-format
# finding and is never judged (fail open).
CAPABILITY_VENUE_SHAPE_RE = re.compile(r"^[a-z][a-z-]{2,}$")
# Seed rows carry a per-row freshness stamp (§4.2b) — no freshness data
# means confidently stale, which is worse than ignorant.
CAPABILITY_LAST_VERIFIED_RE = re.compile(r"LAST-VERIFIED:\s*(20\d{2}-\d{2}-\d{2})")
# The kit-owned seed fence (§4.2c): upgrade re-renders ONLY the block between
# these markers inside a consumer-edited ledger; everything outside — the
# append log, all consumer text — is preserved byte-for-byte. Prefix-matched
# by the refresher so a future tweak to the warning wording cannot orphan an
# existing fence.
CAPABILITY_SEED_BEGIN_PREFIX = "<!-- substrate-kit:capability-seed BEGIN"
CAPABILITY_SEED_END_PREFIX = "<!-- substrate-kit:capability-seed END"
CAPABILITY_SEED_BEGIN = (
    CAPABILITY_SEED_BEGIN_PREFIX
    + " — kit-owned, refreshed at upgrade. Append your findings BELOW the"
    " fence (## Append log), never inside it. -->"
)
CAPABILITY_SEED_END = CAPABILITY_SEED_END_PREFIX + " -->"


def capability_log_line_example(*, venue: str | None = "routine-fired") -> str:
    """Canonical append-log entry (``venue=None`` renders the legacy 5-field form)."""
    venue_field = f" {venue} ·" if venue else ""
    return (
        f"- 2026-07-12 · wall ·{venue_field} fire_trigger on a cross-session"
        " binding refused · exact error: not enabled for this organization ·"
        " workaround: fire from the owning session\n"
    )


# ── docs/seat-digest.md — the seat-digest blocks (grounded-skills §7.6) ──────
#
# The kit-generated seat-prompt-feeding render surface (plan §7 slice 6,
# §8 Q3=A): ONE planted doc carrying two fence-marked digest blocks — the
# skills-index digest and the venue-filtered WALLS digest — that
# fleet-manager's seat-prompt regen tool extracts WITHOUT executing kit code
# (tree scan + fence-prefix match + byte compare, its v3.3 consumption
# model). Together with the capability-seed pair above, these fence-prefix
# pairs are THE machine extraction contract: consumers match the PREFIX only
# (never the full marker wording, so a future tweak to the trailing warning
# text cannot orphan a fence), and the bytes BETWEEN a BEGIN/END pair are the
# canonical block. Design invariant (plan §2): digest + pointer, never
# inline — every block ends with a pointer line to its source doc and stays
# within SEAT_DIGEST_BLOCK_BUDGET, because the downstream seat-prompt pastes
# sit at 7,943–7,998 of 8,000 chars (effectively zero headroom).

SEAT_DIGEST_BLOCK_BUDGET = 1500
SKILLS_DIGEST_BEGIN_PREFIX = "<!-- substrate-kit:skills-digest BEGIN"
SKILLS_DIGEST_END_PREFIX = "<!-- substrate-kit:skills-digest END"
WALLS_DIGEST_BEGIN_PREFIX = "<!-- substrate-kit:walls-digest BEGIN"
WALLS_DIGEST_END_PREFIX = "<!-- substrate-kit:walls-digest END"
SKILLS_DIGEST_BEGIN = (
    SKILLS_DIGEST_BEGIN_PREFIX
    + " — derived render, kit-generated; regenerate with `python3 bootstrap.py"
    " seat-digest`, never edit. -->"
)
SKILLS_DIGEST_END = SKILLS_DIGEST_END_PREFIX + " -->"
WALLS_DIGEST_END = WALLS_DIGEST_END_PREFIX + " -->"
# The walls-digest BEGIN marker carries the venue filter it was rendered
# with (`venues=<comma-joined tokens>`), so a regen or drift check re-renders
# with the SAME venues the committed doc chose — the venue set is
# parameterizable per seat (Project-seat default below), never hardcoded.
WALLS_DIGEST_VENUES_RE = re.compile(r"venues=([a-z][a-z,-]*)")
# Project seats read entries verified in their own venue plus the
# venue-agnostic ones (slice-5 prerequisite: the venue column makes the
# {{WALLS}}-class filter mechanical instead of editorial).
SEAT_DIGEST_DEFAULT_VENUES = ("autonomous-project", "any")


def walls_digest_begin_marker(venues: tuple[str, ...]) -> str:
    """Compose the walls-digest BEGIN marker carrying ``venues``."""
    return (
        WALLS_DIGEST_BEGIN_PREFIX
        + f" venues={','.join(venues)}"
        + " — derived render, kit-generated; regenerate with `python3"
        " bootstrap.py seat-digest`, never edit. -->"
    )


# ── control/claims/ — the work-claim bullet (EAP §6.4) ───────────────────────
#
# Taught in control/claims/README.md: one file per claim, a single bullet
#   - `branch-or-scope` · **scope** — detail · YYYY-MM-DD
# The bullet must carry a backticked branch/scope token (the duplicate scan's
# key) and an ISO date anywhere after it. Enforced by check_claims
# (work-claim hygiene).

WORK_CLAIM_BULLET_RE = re.compile(r"^-\s.*`([^`\n]+)`", re.MULTILINE)
WORK_CLAIM_DATE_RE = re.compile(r"\b(20\d{2}-\d{2}-\d{2})\b")


def work_claim_bullet_example(date: str = "2026-07-10") -> str:
    """Canonical work-claim bullet dated ``date``."""
    return (
        f"- `example-branch` · **scope** — one-line detail · "
        f"expected files/area · {date}\n"
    )


# ── Self-propagation doctrine — the registration reflex (grounded-skills §7.8) ─
#
# Taught in the CONSTITUTION.md.tmpl working-agreement clause and in the
# planted skill index's "Growing the set" section (SKILLS-index.md.tmpl) —
# the clause's pointer target, so the reflex is stated where agents actually
# look. Agreement between the two templates and this one home is pinned by
# tests/test_self_propagation.py; clause and index cannot drift.
#
# Executable twin of superbot doctrine (mined from superbot .claude/CLAUDE.md
# + docs/owner/maintainer-question-router.md — cited, never paraphrased into
# drift):
#   - Q-0194 (2026-06-22, promoted binding 2026-06-28) — friction → guard:
#     convert recurring friction into the cheapest ENFORCING prevention
#     before session end (checker/CI/test → hook → journal rule; "enforce,
#     don't exhort", Q-0132). Ownership split: docs / journal / test /
#     checker guards are free to ship now; a hook / settings / binding
#     working-agreement rule is owner-gated (build if owner-directed
#     in-session, else propose a router DISCUSS Q).
#   - Q-0106 (2026-06-12) — agents do NOT self-edit the working agreement /
#     executable config on their own initiative; a binding rule evolves by
#     PROPOSING it (a router Q-block), never applying it. The one exception:
#     an in-session owner-directed change (the owner is the live reviewer),
#     applied directly and recorded with its provenance id.
#   - Q-0172 (2026-06-17) — ideas promote to plans and ship anytime without
#     approval; the single requirement is ACCOUNTABILITY (the self-initiated
#     flag on the run report). Safety brakes unchanged.

SELF_PROPAGATION_REFLEX = "add or extend the skill"
SELF_PROPAGATION_REGISTRY = "a registry entry, not ad-hoc prose"
SELF_PROPAGATION_GROWTH_LOOP = "prose workflow → index row → promoted skill"
SELF_PROPAGATION_FREE_LANE = "free to ship directly"
SELF_PROPAGATION_BOUND_LANE = "never self-applied"
SELF_PROPAGATION_PHRASES = (
    SELF_PROPAGATION_REFLEX,
    SELF_PROPAGATION_REGISTRY,
    SELF_PROPAGATION_GROWTH_LOOP,
    SELF_PROPAGATION_FREE_LANE,
    SELF_PROPAGATION_BOUND_LANE,
)
# The compact in-clause provenance cite (Q-numbers; the dates live in this
# comment block — templates state current value only, per their own header).
SELF_PROPAGATION_PROVENANCE = "superbot Q-0194 · Q-0106 · Q-0172"
