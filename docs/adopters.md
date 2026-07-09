# Fleet adopter registry

> **Status:** `living-ledger` · **Sole writer: kit-lab** (this repo)
>
> Who runs which kit version — the substrate-coordinator's visibility surface
> (inbox ORDER 003; manager research 2026-07-09). kit-lab is the fleet's
> substrate coordinator but has **zero write access to adopter repos** (KF-2:
> the lab never writes to consumers); this registry is therefore maintained
> from *evidence relayed inward*: each adopter self-reports in its own
> `control/status.md` `kit:` line (`kit: v<X.Y.Z> · check: green|red ·
> engaged: yes|no` — planted by adopt from v1.3.0, documented in the planted
> `control/README.md`), the manager relays those heartbeats plus adoption
> facts as orders/inbox context, and direct reads happen only where a repo is
> readable to a kit-lab session (e.g. a fleet review). Update a row whenever
> fresher evidence arrives; `last-seen` is the date of the evidence, never a
> guess.

## Registry

| repo | kit_version | engaged | last-seen | evidence / notes |
|---|---|---|---|---|
| menno420/substrate-kit (kit-lab) | HEAD (consumer #0) | yes | 2026-07-09 | Self-adopted per founding plan §3.3; dogfoods every band pre-release. |
| menno420/superbot-next | v1.2.0 | yes | 2026-07-09 | Rollout PR superbot-next#69 (ENGAGED on v1.2.0); fleet review 2026-07-09 verdict DEGRADED→covered — required-check + workflow half remain (friction #38). |
| menno420/websites | v1.2.0 | yes | 2026-07-09 | Rollout PR websites#31 (ENGAGED on v1.2.0); fleet review verdict OK-recovered; ⚑ owner still confirms the required check in Settings → Rules. |
| menno420/superbot | v1.0.0 (pin-only) | no | 2026-07-09 | Deliberate stance: `substrate.config.json` pin + vendored dist only (superbot#1879/#1882); fleet review verdict OK-pin-only; the v1.2.0+ upgrade is an owner decision (⚑ carried in control/status.md). |
| menno420/superbot-games | — (not yet relayed) | — | 2026-07-09 | **The two-lane adopter** (SHARED multi-Project repo, manager relay via inbox ORDER 004): per-lane heartbeats `control/status-mining.md` + `control/status-exploration.md` per its `control/README.md` multi-Project extension. The kit's configurable `heartbeat_files` (v1.4.0) exists for exactly this shape — its config should list both lane files. `kit_version`/`engaged` pending the first relayed per-lane `kit:` line. |
| trading-strategy (planned) | — | — | — | Not yet created/adopted; PL-ruled third in the adoption order, "on a matured kit" (docs/program/rulings.md). Row activates at its adopt. |
| game repos (coming) | — | — | — | Named by the manager (ORDER 003) as coming adopters; rows added when the repos exist and adopt. superbot-games (above) is the first to materialize. |

## Row protocol

- **Columns:** `repo` (owner/name) · `kit_version` (the vendored dist the repo
  *runs*, not the newest release) · `engaged` (the KL-7 post-adopt engagement
  gate: yes/no) · `last-seen` (date of the evidence) · evidence/notes (PR
  numbers, review verdicts, relayed heartbeat).
- **One writer:** only kit-lab sessions edit this file (same one-writer rule
  as the `control/` bus). Adopters never write here — their channel is their
  own `control/status.md` `kit:` line.
- **Staleness reads as dark**, not as wrong: an old `last-seen` means no fresh
  evidence has been relayed, and a fleet-review pass (or the manager) should
  refresh it.
- **Releases point back here:** every release's notes carry the adopter
  upgrade checklist (`src/build_release_json.py` appends it to `notes.md`),
  whose last step is updating the adopter's own `kit:` status line — the loop
  that keeps this registry fed.
