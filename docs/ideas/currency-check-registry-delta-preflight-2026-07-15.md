---
state: promoted
origin: lab
shipped_pr: 392
shipped_repo: menno420/substrate-kit
merged_date: 2026-07-15
outcome: shipped
---

# `currency --check` — a cheap registry-delta preflight verb (2026-07-15)

> **Status:** `ideas`
>
> **State:** captured (originated as the 💡 in
> `.sessions/2026-07-15-adopter-currency-websites-v1170.md`, PR #389; filed
> here by the 2026-07-15 currency-fm-kit-line session, which found the baton
> pointing at a Backlog entry that didn't exist) → promoted → **shipped**
> (PR #392, 2026-07-15 — the in-PR flip convention; anticipated merge date):
> `registry_delta()` in `engine.currency` + the `--check` lane on
> `cmd_currency` — rows-only compare, stamp-insensitive, dark-never-delta,
> exit 0/1, no write.

## The idea

A `bootstrap.py currency --check` verb that fetches only the self-report /
tree evidence (the same read-only scan `currency` already does) and exits
**0** (registry current) / **1** (a regen would change rows) — without
writing `docs/adopters.md`.

## Why

Every wake currently decides "is a currency slice due?" by hand-fetching
adopter self-report lines and eyeballing them against the registry (the #388
heartbeat did exactly this in prose), or by running the full regen and
diffing. Two paid instances in one day: the #388 spot-check ("websites
v1.15.0 — no currency slice due") was stale within the hour when websites
bumped, and the fleet-manager `kit:` line bump (fm#232, 12:58:30Z) needed a
coordinator route to detect at all. A `--check` verb makes the wake-scan
turnkey: any session (or a preflight leg) can detect "registry stale" itself
via a plain exit code, instead of relying on coordinator recon to re-derive
the delta.

## Sketch

- Reuse the existing `currency` scan (read-only fetch of every roster row's
  tree header + config pin + heartbeat `kit:` line).
- Render the would-be registry in memory; compare against the committed
  `docs/adopters.md` **rows only** (ignore the `Generated:` timestamp line,
  or a timestamp-only delta false-positives every run).
- Exit 0 = no row delta; exit 1 = regen would change rows (print the
  changed rows); network-dark repos read as dark, never as delta.
- Tests: fixture registry vs synthetic scan results — current / row-delta /
  timestamp-only cases.

next: built — PR #392 shipped exactly this slice (engine + tests + dist
byte-pin regen in one PR); the survive-window revert-scan owns the rest.
