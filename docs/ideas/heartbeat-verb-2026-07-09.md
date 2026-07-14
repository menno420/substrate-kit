---
state: promoted
origin: lab
shipped_pr: 346
shipped_repo: menno420/substrate-kit
merged_date: 2026-07-13
outcome: shipped
---

# `bootstrap heartbeat` — a mechanical status.md writer (2026-07-09)

> **Status:** `ideas`
>
> **State:** captured (band KL-8 session, 2026-07-09) → shipped (PR #346,
> 2026-07-13, ORDER 019 item 7 — restamp default lane + `--full` contract
> lane). **Origin:** lab — the control protocol just gained an enforced
> heartbeat; hand-formatting it is now the weakest link.

**One line:** a `bootstrap.py heartbeat --phase "…" --health green --orders
"acked=001,002 done=001" [--blockers …] [--needs-owner …] [--notes …]` verb
that overwrites `control/status.md` in the exact contract shape with a
correct UTC `updated:` stamp — so the protocol's LAST step is one command,
not hand-assembled markdown.

## Why (friction observed the day the gate shipped)

KL-8 makes the heartbeat enforced: `check_status_current` gates a
heartbeat-less `status.md` strict-RED and warns on staleness. That
immediately makes the *hand-written* timestamp the failure surface — a
session that writes `updated: 2026-7-9 13:00` (unparseable) or forgets the
`T`/zone goes red for formatting, not for darkness; a routine wake has to
template the whole file by hand in its prompt. The engine already owns
atomic writes, UTC time, and the contract text (the seed template) — one
verb closes the gap:

- always-parseable `updated:` (the verb stamps `datetime.now(utc)`);
- contract-complete fields (missing flags default honestly: `blockers:
  none`, `⚑ needs-owner: none`);
- overwrite-own semantics preserved (whole-file write, never append);
- routines get a mechanical LAST step (`… && python3 bootstrap.py
  heartbeat --phase "routine wake" …`), the same enforce-don't-exhort
  motion as the KL-5 auto-drafted card.

## Guard recipe

Engine-side `loop/` or `cli.py` verb (`cmd_heartbeat`), reusing
`atomic_write_text` + the `check_status_current.parse_heartbeat` round-trip
as its own test (write → parse → equal); wire a session-close advisory
pointer ("status stale — run `bootstrap.py heartbeat …`"). Tests:
round-trip, field defaults, refuses outside a control-carrying host.

**Next:** a groomed-ideas increment (ordinary lane — additive CLI verb,
MINOR).
