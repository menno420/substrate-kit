# 2026-07-14 · ORDER 020 (d)+(e) — check-time outbox advisory + fleet-master pointer casing

> **Status:** `in-progress`

About to happen (opening declaration): close the two open BUILD sub-items of
ORDER 020 (fm lane-write relay, 2026-07-14T04:12Z; the other three — a/b/c —
were premise-checked SATISFIED at HEAD and need no action):

- **(d) — A10 outbox-size advisory in `check --strict`.** The friction-outbox
  drain reminder (`list_outbox` → "N report(s) pending, file them then delete")
  lives ONLY in `cmd_session_close` today, so a stranded envelope — a §9.1
  friction report the engine could not file (no GitHub reach) — is invisible to
  every plain `check` / `check --strict` between session-close seams. Lift the
  same pending-count reminder into the `check` advisory lane: a new
  `check_outbox_pending` (checks/check_outbox.py) wired into `cmd_check`'s full
  lane with the identical warn-only emit + guard-fire block as every other
  advisory, so a stranded outbox is visible at check time, never exit-affecting.
- **(e) — INC-29 / fm plan B2: dead lowercase `docs/capabilities.md` → uppercase
  `docs/CAPABILITIES.md`** at the three seat-digest/CAPABILITIES surfaces
  (`CAPABILITIES.md.tmpl:8`, `seatdigest.py:31` docstring, `seatdigest.py:442`
  rendered "No third copy" block). fm (authority on its own repo) states its
  fleet-master ledger is uppercase `docs/CAPABILITIES.md`; the lowercase pointer
  is a dead link. One template fix heals ~14 adopters (the pointer plants into
  every adopter's `docs/CAPABILITIES.md`). The template-pointer guard's
  `_EXTERNAL_REPO_REFS["docs/capabilities.md"]` entry goes stale on the fix
  (no template emits lowercase anymore) — remove it; the uppercase pointer then
  resolves via `_PLAN_DESTS` (it is an ADOPT_PLAN destination).

Both are kit-owned, contained, reversible; tests + dist byte-pin regen in the
same PR. ORDER 020 done-when: (d) and (e) shipped in a kit release (or declined).

- **📊 Model:** Opus 4.8 · high · feature build

Run type: routine · lab

## What shipped

_(filled at close)_

## Verify

_(filled at close)_

## Enders

_(filled at close)_
