# 2026-07-11 — currency scanner: private-repo blindness fix + adopters regen

> **Status:** `in-progress`

- **📊 Model:** fable-5 · medium · worker

## Scope (what is about to happen)

Fix the kit-upgrade currency scanner's private-repo blindness (the #230
headline + 💡 idea): `default_fetcher` reads raw.githubusercontent.com
404 as "file absent", but a PRIVATE repo returns 404 for every path, so
pokemon-mod-lab (tree truly adopted at v1.6.0 @ d46b282d) rendered as
"not adopted / unknown". Teach the fetcher to disambiguate: raw 404 →
authenticated GitHub API contents fallback (GITHUB_TOKEN/GH_TOKEN) →
git-transport fallback (blobless depth-1 clone; the transport that works
in proxy-mediated agent seats where api.github.com REST is
policy-blocked — verified live this session: API probe 403 "GitHub
access is not enabled", `git clone --filter=blob:none` 1s/848K success).
A 404 becomes "truly absent" ONLY once the repo is proven readable; an
unreadable repo renders an honest `unreadable` verdict, never "not
adopted". Regression tests at the fetch seam (raw 404 + API success →
adopted; raw 404 + API 404 on readable repo → absent; auth failure →
unreadable, not "not adopted"; git-fallback path). Then regenerate
`docs/adopters.md` with the fixed scanner (pokemon-mod-lab row must
reflect tree truth at scan time) + CHANGELOG [Unreleased] entry + dist
rebuild (byte-pin). Files: src/engine/currency.py, src/engine/cli.py (if
wiring needs it), dist/bootstrap.py, tests/test_currency.py,
docs/adopters.md, CHANGELOG.md, control/claims/currency-private-repo-fix.md
(deleted at close), this card. NEVER `control/inbox.md`,
`control/status.md`, or `bench/` (run-9 session active there).
