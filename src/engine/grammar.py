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

UPDATED_LINE_RE = re.compile(r"^updated:\s*(\S+)", re.MULTILINE)


def updated_line_example() -> str:
    """Canonical ``updated:`` heartbeat line."""
    return "updated: 2026-07-10T12:00:00Z\n"


# ── control/status*.md — the `kit:` self-report line (ORDER 003) ────────────
#
# Taught in control/README.md § "status.md format":
#   kit: v<X.Y.Z> · check: green|red · engaged: yes|no
# Parsed leniently — real heartbeats decorate the line, so the version is the
# first `v<digit...>` token after `kit:` and the check/engaged fields are
# scanned anywhere on the line. Consumed by currency.parse_kit_line (the
# fleet registry's self-report evidence).

KIT_LINE_RE = re.compile(r"^kit:\s*(.*)$", re.MULTILINE)
KIT_VERSION_TOKEN_RE = re.compile(r"\bv(\d[\w.\-]*)")
KIT_CHECK_FIELD_RE = re.compile(r"\bcheck:\s*(green|red)\b")
KIT_ENGAGED_FIELD_RE = re.compile(r"\bengaged:\s*(yes|no)\b")


def kit_line_example(version: str = "1.2.3") -> str:
    """Canonical ``kit:`` self-report line for ``version``."""
    return f"kit: v{version} · check: green · engaged: yes\n"


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
        "WHY-IT-MATTERS: the lane stalls without it\n"
        "UNBLOCKS: the next slice starts moving the moment it's done\n"
        "VERIFIED-NEEDED: attempted via the API — 403, owner-only surface\n"
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
