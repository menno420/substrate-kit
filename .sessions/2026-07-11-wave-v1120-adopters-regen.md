# 2026-07-11 — v1.12.0 wave close-out: adopters registry regen

> **Status:** `complete`

- **📊 Model:** fable-5 · medium · docs-only

## Scope (what is about to happen)

Kit-seat close-out of the v1.12.0 distribution wave: regenerate
`docs/adopters.md` via `python3 dist/bootstrap.py currency` after the four
wave repos landed v1.12.0 (superbot-next #198 @ e81bc9e · websites #146 @
31cfd9f · gba-homebrew #49 @ 399bb01 · venture-lab #42 @ 881445c). The
parallel trio (fleet-manager · superbot-games · trading-strategy) is a
SIBLING worker's lane — their rows are recorded as-of snapshot time;
still-v1.11.0 / mid-flight there is expected, not chased. Expected ⚠️ DRIFT
rows for the quad minus websites (tree v1.12.0, self-report lags — heartbeat
bump is lane-owed, deliberate; websites bumped in-lane on #129 but NOT on
#146, so it lags this wave too) and the kit's chronic config-pin v1.0.0 row
— all truthful output, committed as generated, never hand-edited. Tree truth
for every row is re-verified against each adopter's origin/main via the
local clones (`git fetch` + `git show origin/main:bootstrap.py`), per the
#192-style manual ancestry pass owed on the first regen after a release.
Files: `docs/adopters.md` (regen only) and this card. NO engine/dist/src
changes; NEVER `control/inbox.md` or `bench/`. Touching ONLY this card in
`.sessions/`. No claim file (registry-regen precedent #142/#161/#174/#192/#207).

## Close-out

Shipped the declared scope exactly. `docs/adopters.md` regenerated via
`python3 dist/bootstrap.py currency` (snapshot **2026-07-11T17:44:47Z**, 10
repos scanned). **All 8 engaged adopter trees now CURRENT at v1.12.0** —
the full fleet is on the release: the wave quad (superbot-next @ 99962a6 ·
websites @ 31cfd9f · gba-homebrew @ 4bfcf3a · venture-lab @ 881445c) AND
the sibling worker's trio, which had ALREADY landed by snapshot time
(fleet-manager @ 0677be8 · superbot-games @ 5d38593 · trading-strategy @
2dd955d) — all scan tree v1.12.0 + config pin v1.12.0, independently
re-verified against each origin/main via the local clones (`git fetch` +
`git show origin/main:bootstrap.py|substrate.config.json`) — scanner and
manual ancestry pass agree on every row. Drift rows are all the expected
classes, none chased: 7 heartbeat-lag rows (superbot-next v1.10.1 ·
websites v1.11.0 · gba-homebrew v1.11.0 · venture-lab v1.10.1 ·
fleet-manager v1.7.0 · trading-strategy v1.7.1 · superbot-games
mining/exploration v1.7.1 — all lane-owed bumps) + the kit's chronic
config-pin v1.0.0. The kit's own self-report is CLEAN this time
(v1.12.0 — the release session's mid-close DRIFT self-healed here as the
recipe predicts); note websites lags this wave (its #146 upgrade PR did
NOT bump the heartbeat, unlike its #129 in-lane bump last wave).
**Headline discrepancy (pre-existing, not from this regen):**
pokemon-mod-lab's row says `— / — / no heartbeat file → not adopted /
unknown`, but its origin/main tree @ d46b282d carries `bootstrap.py
KIT_VERSION = "1.6.0"` + `substrate.config.json kit_version 1.6.0` + a
`- **kit:** v1.6.0` status bullet. Root cause verified live:
raw.githubusercontent.com returns **HTTP 404** for pokemon-mod-lab paths
(200 for websites' same path) — the unauthenticated raw fetcher is blind
to that repo (private-repo signature), while authenticated git sees it.
Row identical in the 13:34 and 16:45 regens — chronic scanner blind spot,
shipped as generated (never hand-edit), routed as this card's 💡 idea.
Verified on this branch: `python3 -m pytest tests/ -q` → **1034 passed**;
pre-flip `check --strict` sole finding was this card's own designed
born-red hold.

## 💡 Session idea

The currency scanner treats a raw-fetch 404 as "no artifact = not
adopted", but 404 from raw.githubusercontent.com is exactly what a
PRIVATE adopted repo returns for every path — so pokemon-mod-lab (tree
truly at v1.6.0 with a config pin and a heartbeat bullet) renders as "not
adopted / unknown", indistinguishable from a repo that never adopted.
Teach the fetcher to distinguish *repo unreachable* from *file absent*:
one probe per repo (any 200 on any candidate path = reachable; all-404
across bootstrap.py + config + heartbeat + a known-existing file like
README.md = likely auth-blind) and render an honest `unreachable
(raw fetch 404 — private repo?)` verdict instead of "not adopted". The
registry's whole premise is "the tree is truth" — a row that silently
converts *can't see the tree* into *there is no tree* undermines it, and
the fix is pure fetcher/verdict logic already behind the injectable
`fetch()` seam, cheap to unit-test.

## ⟲ Previous-session review

The v1.11.0 regen card (#192's successor in this lane) closed its loop
well — it live-verified the venture-lab bulleted-heartbeat parser fix and
its improvement note asked the lane recipe to say when the manual
tree-truth ancestry pass is owed vs redundant. This session ANSWERED that
open question by doing both (scan + independent git-show pass) and they
agreed on all 10 rows — evidence the recipe can now say "manual pass owed
on the first regen after a release; agreement recorded once makes the
next mid-cycle regen scan-only". What it could have done better: it
reported "10 repos scanned" while one row (pokemon-mod-lab) was a
scanner blind spot the whole time — the all-clean close-out prose made
the blind spot easy to inherit unquestioned. Improvement to the system:
the lane recipe should require one line per NON-adopted/unknown row
confirming the negative against tree truth (a negative row is a claim
too), which is exactly what surfaced this session's headline finding.
