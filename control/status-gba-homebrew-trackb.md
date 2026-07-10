# gba-homebrew Track B (visiting adopter lane) · status

> Visiting-lane heartbeat per the v1.4.0 multi-lane pattern (`control/README.md`
> § per-lane heartbeats) and the coordinator-lane precedent (#52/#73): this
> file's sole writer is the **gba-homebrew Track B lane**, visiting to upstream
> two adopter-found defect fixes. Deliberately **not in `heartbeat_files`** —
> kit-lab owns `substrate.config.json`; decide-and-flag. This lane never writes
> `control/status.md`, `control/inbox.md`, or `substrate.config.json` — one
> writer per file. Archive/delete this file freely once the visit closes.

updated: 2026-07-10T04:59:27Z
phase: visiting — claim landed first per the claim ritual (claim → re-read → build); build PR follows this merge
health: green
kit: adopter-side v1.6.0 (menno420/gba-homebrew) · check: green · engaged: yes
last-shipped: (this visit) nothing yet — claim only
blockers: none
orders: none for this lane (no inbox order; defect-fix visit under the adopter-findings precedent, cf. #83 and the #99 adopter-findings batch) claimed-by: gate-template-sentinel-fixes gba-homebrew-trackb 2026-07-10T04:59:27Z
⚑ needs-owner: none
notes: CLAIM SCOPE — `live_ci_workflow()` in `src/engine/adopt.py` (the planted `.github/workflows/substrate-gate.yml` template) + its tests + dist regen + CHANGELOG: port two fixes found and validated live on menno420/gba-homebrew (public) PRs #3–#14. Fix 1: a PR whose diff names no session card must pass an explicitly named nonexistent `--session-log` sentinel WITHOUT `--require-session-log` (advisory per the engine contract) — the current bare mtime fallback latches onto the newest (mid-session, in-progress) card and reds every unrelated PR on a fresh CI checkout. Fix 2: a card ADDED by the PR (born-red heartbeat, conventions-style first commit) gates advisory via the absent sentinel; a card MODIFIED by the PR (close-out flip) keeps the full locked-door gate. No overlap with the live `queue-item-11-adopt-lane` claim (adopt --lane, shipped at #103) — different function, different scope. Will re-read the bus at HEAD after this claim merges, before building.
