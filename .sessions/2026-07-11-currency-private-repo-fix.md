# 2026-07-11 — currency scanner: private-repo blindness fix + adopters regen

> **Status:** `complete`

- **📊 Model:** fable-5 · medium · worker

## Scope (what is about to happen)

Fix the kit-upgrade currency scanner's private-repo blindness (the #230
headline + 💡 idea): `default_fetcher` reads raw.githubusercontent.com
404 as "file absent", but a PRIVATE repo returns 404 for every path, so
pokemon-mod-lab (tree truly adopted at v1.6.0 @ d46b282d) rendered as
"not adopted / unknown". Teach the fetcher to disambiguate: raw 404 →
authenticated GitHub API contents fallback (GITHUB_TOKEN/GH_TOKEN) →
tarball-transport fallback (the transport that works in proxy-mediated
agent seats where api.github.com REST is policy-blocked — verified live
this session: API probe 403 "GitHub access is not enabled"). A 404
becomes "truly absent" ONLY once the repo is proven readable; an
unreadable repo renders an honest `unreadable` verdict, never "not
adopted". Regression tests at the fetch seam (raw 404 + API success →
adopted; raw 404 + API 404 on readable repo → absent; auth failure →
unreadable, not "not adopted"; tarball-fallback path). Then regenerate
`docs/adopters.md` with the fixed scanner (pokemon-mod-lab row must
reflect tree truth at scan time) + CHANGELOG [Unreleased] entry + dist
rebuild (byte-pin). Files: src/engine/currency.py, src/engine/cli.py (if
wiring needs it), dist/bootstrap.py, tests/test_currency.py,
docs/adopters.md, CHANGELOG.md, control/claims/currency-private-repo-fix.md
(deleted at close), this card. NEVER `control/inbox.md`,
`control/status.md`, or `bench/` (run-9 session active there).

## Close-out

Shipped the declared scope exactly (one design substitution, flagged
below). `src/engine/currency.py`: `default_fetcher` is now layered —
raw content (primary) → authenticated GitHub API contents endpoint
(`GITHUB_TOKEN`/`GH_TOKEN` via `TOKEN_ENV_VARS`, header only on API
calls) → `codeload.github.com` branch tarball held in memory
(`_TarTree`; membership is definitive tree truth). A 404 becomes
"truly absent" ONLY after the repo is proven readable (API repo-probe
200, or tarball in hand); a repo readable by NO transport raises
`RepoUnreadableError`, which `scan_repo` catches per-repo into a new
`RepoCurrency.unreadable` field → `⚠️ unreadable` verdict (never "not
adopted"; partial pre-failure evidence kept as `partially unreadable`).
Non-404 raw failures still hard-abort (`CurrencyFetchError`) — a
transport outage must not fabricate a registry. One probe per repo,
cached. `cmd_currency` prints an UNREADABLE summary line. **Design
substitution (decide-and-flag):** the scope card said git-clone
fallback; engine code bans subprocess (ruff TID251, §3.2 "pure stdlib
logic"), so the fallback is the codeload tarball instead — pure stdlib
(urllib+tarfile), verified live through this seat's proxy (200 with
proxy-injected credentials, 19.8MB for pokemon-mod-lab, membership
answers absent-vs-unreadable definitively). Verified: 12 new regression
tests at the `http_get` seam (raw 404 + API success → adopted; API 404
on proven-readable repo → truly absent; all-403 → unreadable, verdict
never "not adopted"; tarball reads + proves absence, fetched once per
repo; bearer header on API calls only + env pickup; raw 500 still
aborts; fleet scan survives one dark repo; render/report lines loud).
Full suite **1046 passed** (1034 + 12); `ruff check src/engine/` clean;
dist rebuilt in-commit (byte-pin: fresh build == committed);
`check --strict` sole finding pre-flip was this card's designed hold.
Live regen `python3 dist/bootstrap.py currency` (18.8s, 10 repos):
**pokemon-mod-lab row flipped `— / — / not adopted / unknown` →
`v1.6.0 (bootstrap.py) / v1.6.0 / stale (v1.6.0 < v1.12.0)`** — tree
truth at scan time (the parallel v1.6.0→v1.12.0 upgrade lane had not
merged at snapshot 2026-07-11T18:08:39Z; STALE is the expected-correct
reading per the wave brief). Row self-report reads "no `kit:` line" —
truthful: pokemon's heartbeat carries `- **kit:** v1.6.0 · check: …`
(bold-label form; no plain `kit: v` run for `KIT_LINE_RE`) — grammar
follow-up noted below, deliberately not smuggled into this diff.

## 💡 Session idea

The heartbeat grammar (`engine.grammar.KIT_LINE_RE`) parses
`- **kit heartbeat:** kit: v1.10.1 …` (venture-lab fix, #207-era) but
not pokemon-mod-lab's `- **kit:** v1.6.0 · check: …` — a bold-wrapped
`**kit:**` label leaves no plain `kit: v` run, so an existing, honest
heartbeat renders "no `kit:` line" and the engaged signal is lost.
Either teach the writer templates' exact line shape to the adopter
(cheap, adopter-side) or make the parser tolerate emphasis around the
`kit:` label itself (one regex alternation + two grammar tests,
kit-side, same one-home rule). Same class as the doctrine
emphasis-blind phrase (#185 idea): our parsers keep being
markdown-emphasis-blind one field at a time; worth a single sweep over
`grammar.py` for emphasis-tolerance instead of one-offs.

## ⟲ Previous-session review

The v1.12.0 regen session (#230) did exactly what a good negative-row
audit should: it refused to trust "10 repos scanned, all clean",
re-verified every row against tree truth, and headlined the one row
that was transport fiction — then routed the fix as a card idea instead
of hand-editing generated output. That discipline is why this session
existed and had a crisp spec. What it could have done better: its idea
sketched the fix as "one probe per repo, any-200 = reachable" — a
probe-only design that can say *unreachable* but cannot READ the
private tree, so pokemon's row would have upgraded from wrong to merely
dark; the actual requirement (an authenticated fallback that recovers
tree truth) only became clear against the seat's real transport walls
(API REST proxy-blocked; codeload open). Improvement to the system:
when a session routes a fix-idea touching transports/credentials, it
should record the one-probe transport matrix it already ran (what
returned 200/403/404 from THIS seat) on the card — this session spent
its first act rediscovering exactly that matrix.
