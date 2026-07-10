# Environment spec — gen-2 SuperBot coordinator Project (2026-07-09)

> **Status:** `owner-guidance` — what the gen-2 coordinator's Claude Code
> cloud environment must contain, from the gen-1 lane's wind-down. Names
> only for secrets — values are the owner's, never committed. Suffixed
> `-superbot-coordinator` per the multi-lane rule.

## Setup script (tested — use the committed copy)

Use the TESTED script in
[`docs/environment-setup-script.md`](../environment-setup-script.md),
pasted verbatim by the owner into the project's Environment settings →
Setup script field. It is exit-0-safe by construction: it locates the repo
clone instead of assuming the cwd, skips missing optional files loudly, and
always ends `exit 0` (a non-zero exit kills the session at provisioning —
the gen-1 failure mode that killed retro session #1).

**Re-verified at wind-down (2026-07-09T19:55Z), this session:**

| check | result |
|---|---|
| `bash -n` on the script block extracted from the doc | **exit 0** |
| executed in a scratch home with NO git repo present | **exit 0** (prints `[setup] WARNING: no git repo found ... continuing`) |
| executed in a scratch home WITH a git repo clone | **exit 0** (prints `[setup] Repo clone: ...` then `[setup] Done.`) |

(The two execution cases ran against scratch copies with the `/home/user`
base substituted for a scratch dir, since the live container cannot vacate
its own home; the verbatim script is what `bash -n` checked.)

## Environment variables (names only)

| name | what it is | gen-2 note |
|---|---|---|
| `DISCORD_BOT_TOKEN_PRODUCTION` | **a SEPARATE TEST-BOT token** — the name is misleading (owner-confirmed 2026-07-09) | **rename to `DISCORD_BOT_TOKEN_TEST` in gen-2** so no session ever hesitates before using it against MineSnakeBotTest |
| `DATABASE_URL` | local test Postgres connection string | test-only; never a production DSN |
| `HTTPS_PROXY` + CA bundle (`/root/.ccr/ca-bundle.crt`) | platform-provided egress proxy | do not unset or bypass; TLS failures mean read the proxy README, not disable verification |

## GitHub scopes needed

| repo | scope | why |
|---|---|---|
| `menno420/superbot` | read | the old bot — reference/goldens source only |
| `menno420/superbot-next` | write | the product; bands, fixes, status docs |
| `menno420/substrate-kit` | write | lane heartbeat + suffixed retro/succession docs |
| `menno420/fleet-manager` | read | blueprint + fleet protocol reference |

**Repo creation remains owner-only** — session tokens cannot create repos
(gen-1 wall, exact error in the
[next-boot doc](next-boot-2026-07-09-superbot-coordinator.md) §4); plan
around it, don't probe it.
