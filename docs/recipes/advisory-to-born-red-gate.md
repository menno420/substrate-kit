# Advisory → born-red gate — graduating a warn-only check into an exit-affecting one

> **Status:** `reference`
>
> **applies-when:** `content:posture="advisory", content:check_added_card`
>
> A recipe: the proven discipline for **promoting a warn-only advisory check
> into an exit-affecting merge gate** once it has caught the same real leak more
> than once. Graduated from the estate pattern shipped 2026-07-19 — the
> `📊 Model:` line exit-gate trilogy (substrate-kit PR #512 task-class, #513
> exact-model-ID, #514 effort), each built on an advisory precedent
> (#495 / #498 / #500). **NOT SOURCE OF TRUTH** for any adopter's code — it is
> the pattern to copy, not a contract to import.

## When this applies

You have an **advisory** check — warn-only findings, riding `posture="advisory"`,
kept off your required-check floor — and it keeps naming the same class of real
defect that a human then fixes by hand. The advisory did its discovery job: the
drift it flags is real and it recurs. That is the moment this pattern applies —
**an advisory that has proven a real, repeating leak has earned promotion to a
gate that blocks the merge instead of merely whispering at it.**

The whole point of the advisory tier is that a new rule can prove itself
*without* the blast radius of a red. So do not graduate on the first sighting,
and do not graduate a check whose red would detonate across every
already-adopted repo during a version-skew window (the **fleet-bomb**
constraint — such a check stays advisory forever). Graduate only a check you can
scope so tightly that its red can touch nothing but the PR in front of it.
Part 2 is how.

## The pattern, in five parts

**1 — Graduate on a *repeat* real leak, never on the first sighting.**
The advisory is the probation period. Let it run warn-only until the same real
defect has slipped past the warning at least twice — proof that the warning
alone does not change behavior. A leak that has recurred is a leak a gate should
stop; a leak seen once might be noise, and a premature red spends trust you
cannot refund. Each rule in the trilogy had a warn-only precedent
(#495 / #498 / #500) that fired on real cards before the exit-affecting version
shipped.

**2 — Scope the gate to the PR's OWN added artifact — this is what keeps it from
being a fleet bomb.**
An exit-affecting check earns its red only if that red can never fire on
anything the author did not just write. Grade the *single artifact this PR adds*
— the one new session card, the one new recipe — never the repo's existing tree.
A gate scoped to the PR's own added card can never retroactively redden a card
that merged last week, so promoting it cannot detonate across the fleet the way
a tree-wide required check would. This scoping is the entire difference between a
check that *may* be exit-affecting and one that *must* stay advisory: the trilogy
grades only the card the PR adds, so no already-merged card is ever at risk.

**3 — Fail open on everything you did not come to grade.**
An exit-affecting check must red *only* on the specific defect it was promoted to
catch. Every other condition — the marker is absent, the line is unparseable, the
file is unreadable, the input directory does not exist — returns *no finding*, so
ownership of that case stays with whatever check already owns it and you never
double-red. In the trilogy each segment grader returns `[]` the moment the
`📊 Model:` line is missing or unparseable; the completeness marker check owns
"the line is absent," and the segment checks own only "the line is present but
its value is off-taxonomy."

**4 — Add the exit-affecting behavior WITHOUT touching your strict-subcheck floor
(the underscore-helper trick).**
If your strict-subcheck registry is guarded by a parity test that scans one
function's body for `check_<name>(` call tokens and asserts set-equality with a
registry, a naively-named new check forces a registry edit and bumps the
anchor-floor count — noise on every promotion, and a tempting place to
accidentally weaken the floor. Avoid both: name the grader with a **leading
underscore** (`_effort_findings_for_card`, not `check_effort`) so it never
matches the `\bcheck_(\w+)\(` scan token, and call it from the gate lane
(`check_added_card`) rather than from the scanned aggregator
(`_extra_check_findings`). The behavior is exit-affecting; the parity test and
the strict-subcheck count never move. (substrate-kit shipped three exit-affecting
segment checks with `EXPECTED_STRICT_SUBCHECKS` still at 7.)

**5 — Mutation-test both directions, and pin the fail-open.**
Every graduated rule ships a triad: hold a known-good card constant, mutate
*exactly one* segment to the off-taxonomy value, and assert (a) the mutated card
reds with *exactly one* finding that names the bad value and lists the valid set,
(b) the held-constant card stays green, and (c) with the graded line absent, the
gate returns exactly what the completeness check alone returns (no double-red —
the fail-open of part 3, pinned as a test). One-direction tests rot silently: a
green-only test passes forever even after the check stops firing, and a red-only
test cannot catch a rule that reds valid input.

## Skeleton (copy-paste)

```python
# In your gate module (the lane that grades the PR's own added artifact),
# NOT in the aggregator your strict-subcheck parity test scans.

def _off_taxonomy_findings_for_card(text: str) -> list[str]:
    payload = _last_payload(text)          # fail-open source of truth
    if payload is None:                    # part 3: line absent/unparseable
        return []                          #   -> the marker check owns this
    value = payload["segment"]
    if value in KNOWN_VALUES:              # part 3: valid -> green
        return []
    known = " | ".join(KNOWN_VALUES)
    return [                               # part 2: one finding, names the bad
        f"an off-taxonomy segment {value!r} on this added card — it is not "
        f"one of ({known}); fix this card's line to the taught form ..."
    ]

def check_added_card(path, markers) -> list[str]:
    text = path.read_text(encoding="utf-8")
    if _is_born_red(text):                 # in-progress -> the designed HOLD
        return [BORN_RED_HOLD_MESSAGE]
    findings = check_completeness(path, markers)          # owns "line absent"
    findings.extend(_off_taxonomy_findings_for_card(text))  # owns "value wrong"
    return findings
```

```python
# The both-directions triad (part 5), one per graduated rule.

def test_off_taxonomy_value_reds(tmp_path):
    card = _good_card(tmp_path, segment="not-a-real-value")   # mutate ONE segment
    misses = check_added_card(card, _MARKERS)
    assert len(misses) == 1
    assert "not-a-real-value" in misses[0]

def test_good_value_stays_green(tmp_path):
    card = _good_card(tmp_path, segment="valid-value")
    assert check_added_card(card, _MARKERS) == []

def test_missing_line_fails_open(tmp_path):
    card = _good_card(tmp_path, segment=None)                 # drop the line
    assert check_added_card(card, _MARKERS) == check_completeness(card, _MARKERS)
```

## The cold-adoption smoke — the fleet-wide safety net under all of this

Parts 2–3 keep one PR's red honest; a **cold-adoption smoke** test keeps the
whole gate honest across every repo that adopts it. It walks the merge gate
through a freshly-seeded repo and asserts the intended arc: **RED on the seed
state → ENGAGED after the first real heartbeat → GREEN**. That is the check that
would catch a promotion which accidentally reds a *virgin* adopter (a card that
has not been written yet) — the one way a well-scoped own-card gate can still
misfire on cold adoption. Ship the graduation and its cold-smoke coverage
together; a gate with no cold-adoption arc is a gate you cannot safely hand to
the fleet.

## Estate reference (the proof)

The `📊 Model:` line exit-gate trilogy, substrate-kit:

- **PR #512 (R13)** — task-class segment: `_task_class_findings_for_card`,
  prefix-match against the 9 PL-004 classes.
- **PR #513 (R14)** — exact-model-ID segment: `_exact_model_id_findings_for_card`,
  a *reject* (`EXACT_MODEL_ID_RE.search` — any provider-prefixed or dated ID reds;
  family-level names pass).
- **PR #514 (R15)** — effort segment: `_effort_findings_for_card`,
  exact-membership in `(low, medium, high)` plus the terminal `unrecorded` honest
  carve-out.

All three live as leading-underscore helpers in `check_added_card`
(`src/engine/checks/check_session_log.py`), fold in only on the card's `complete`
branch, fail open on a missing/unparseable line, and shipped with
`EXPECTED_STRICT_SUBCHECKS` unchanged. Their advisory precedents (#495 / #498 /
#500) are the probation part 1 describes. Both-directions tests:
`tests/test_checks.py` (the R13 / R14 / R15 triads). Cold-adoption arc:
`tests/test_ci_control_lane.py`.

## Scope — doctrine first, scaffolding only if it repeats

This recipe is the **doctrine** — the five decisions, in order. Copy the
decisions; do not import substrate-kit's grader. Build the checker only when
*your* repo has grown an advisory that has proven a repeat real leak on an
artifact you can scope to a single PR-added file. One graduated gate is a recipe
entry; a *second* advisory earning the same promotion is the signal to extract a
shared helper. Until then, hand-apply the pattern — a gate you write by following
these five parts is worth more than a framework you adopt before you have two
instances to generalize from.
