# Hardware-Gated Validation Runbook

> [!NOTE] **Status:** These validations require physical hardware, network access, or
> cloud credentials that are NOT available in the automated localhost environments.
> Until exercised, every item below is **NOT PERFORMED** — automated localhost
> testing must never be presented as hardware/cloud validation. Run serially, one
> item at a time, and never on a machine you need to keep free.

## Current status (2026-11-16)

Most items are **BLOCKED** in this workspace — the preconditions below cannot be
satisfied here (no booted Void host or HP 14 access, no Apple Silicon/Windows/Linux
runtime hosts, no cloud credentials, no dedicated endurance hardware, voice/model
live runs forbidden by AGENT.md). These are honest blockers, not open bugs:
re-open only when the listed resource exists.

| # | Validation | Status | Blocker |
|---|------------|--------|---------|
| 1 | CORE 0.6.0 Void x86_64 install on HP 14 | ❌ BLOCKED | No booted Void host, physical HP, or installer execution environment |
| 2 | CORE Void reboot, runit, Caddy trust, nftables load | ❌ BLOCKED | Requires item 1 |
| 3 | CORE upgrade, rollback, backup/restore, storage-failure drills | ❌ BLOCKED | Requires item 1 and a disposable data set |
| 4 | Physical HP firmware, thermal and planned 2 x 8 GB DDR4-2666 upgrade | ❌ BLOCKED | Installed RAM is unverified (earlier report: 4 GB); the upgrade is PLANNED — not installed or verified; no physical HP access |
| 5 | RISARMS-ui Apple Silicon/Windows/Linux/Void runs and native installers | ❌ BLOCKED | No runtime hosts and no authenticated CI run |
| 6 | Physical LAN (Void host ↔ device) | ❌ BLOCKED | No Void host on the LAN; firewall + TLS certs not re-verifiable |
| 7 | R.E.S.C.S. live S3 | ❌ BLOCKED | No bucket or `RESCS_LIVE_S3_*` credentials (keys must rotate after) |
| 8 | R.E.S.C.S. live PostgreSQL/Supabase | ❌ BLOCKED | No live DB or `RESCS_INTEGRATION_DATABASE_URL` |
| 9 | R.E.S.C.S. 24/7 endurance | ❌ BLOCKED | Needs non-primary hardware; >5 s budget is forbidden on the MacBook |
| 10 | A.S.I.S./A.S.C.S. live voice + model | ❌ BLOCKED | Requires mic/speaker + Ollama 30b; live flags forbidden by AGENT.md here |
| 11 | T.I.V.I.S.S. external verification | ✅ LOCAL VERIFIED | Local `TIVISS-HOST/` checkout passes 279 tests; upstream re-clone still optional |
| 12 | Historical Pi/ARM64 deployment (CORE + RESCS) | ❌ HISTORICAL / BLOCKED | Not a CORE 0.6.0 server target; no Pi hardware or systemd host |

## Rules that always apply

- Never commit `*.key`, `*.pem`, `*.crt`, `*.jks`, `var/rescs.json`,
  `*-device.json`, `.env*`, or any file containing a credential/token.
- Never disable TLS or fall back to plaintext for LAN validation.
- Rotate cloud keys after any live-cloud run.
- Keep live runs separate from CI/dev machines. On shared hardware do not set
  `RESCS_ENDURANCE_SECONDS` above its default (5 s).

## 0. CORE 0.6.0 Void Linux HP 14

| Preconditions | HP 14-dq1037wm, Void Linux x86_64 glibc, runit, at least 5 GiB free, release archive, reviewed `core.env`/`rescs.env`/Caddy origin |
| Source of truth | `CORE-HOST/README.md`, `RISARMS-HOST/deployment/void/README.md`, `RISARMS-HOST/deployment/void/install.sh` |
| Procedure | Extract the release, run `sudo ./deployment/void/install.sh`, review configuration, enable runit services, run `sudo risarms-doctor`, reboot, then test login and backup/restore |
| Acceptance | Services start on boot; Caddy trust works; CORE/RESCS health endpoints pass; nftables does not lock out SSH; keys do not rotate; upgrade, rollback, backup, restore and storage-failure drills pass; no secrets in logs |
| Do NOT | Claim signed server updates or hardware validation; this release ships a source archive and no server update signature |
| Memory note | Installed RAM on the HP is **unverified** (earlier report: 4 GB — do not state a figure as fact). The 2 x 8 GB Samsung DDR4-2666 upgrade to 16 GB is **PLANNED, not installed or verified**. Validate firmware/thermal behavior only after the upgrade is physically present |

## 0b. Historical physical Raspberry Pi / ARM64 deployment (CORE + RESCS)

| Preconditions | Raspberry Pi 4/5 (ARM64), Raspberry Pi OS 64-bit, cgroup v2, systemd, dedicated SSD mounted at `/srv/core` |
| Source of truth | `RISARMS-HOST/deployment/pi/install.sh`, `RESCS/deploy/pi/` (no Pi README exists in the umbrella yet) |
| Procedure | Run the CORE Pi installer on clean hardware; verify systemd units, `/srv/core` guard, service health, and reboot persistence; then exercise CORE ↔ RESCS loopback |
| Acceptance | Services start on boot, `/srv/core` is enforced, loopback passes, no secrets in logs, clean restart after power loss |
| Do NOT | Treat macOS x86_64 unit tests as Pi/ARM64 validation; commit device certs or provisioning tokens. Pi is not a CORE 0.6.0 server target |

## 1. Physical LAN — Void CORE host ↔ RISARMS-ui device

| Preconditions | Installed Void host on the LAN with trusted Caddy; RISARMS-ui desktop client on a separate device; only TCP `443` exposed |
| Source of truth | `CORE-HOST/docs/lan-readiness.md` (preflight §0, checklist) and `CORE-HOST/README.md` |
| Procedure | Complete item 0, then sign in from the desktop client and exercise messaging, reconnect and revocation over the LAN |
| Acceptance | All checklist boxes ticked; certificate verification stays enabled; host logs contain no credentials; desktop profile contains NO session token |
| Do NOT | Wait 24 h for lease expiry (fake-clock tests cover it), disable TLS, or commit `var/rescs.json` / cert material |

## 2. R.E.S.C.S. live S3

| Preconditions | A real S3 bucket + credentials |
| Run | `bash scripts/rescs_s3_live.sh` in RESCS (self-skips without
  `RESCS_LIVE_S3_*`) |
| Acceptance | Live suite unsets `skipIf` and passes against the real bucket |
| After | Rotate the access/secret keys |

Gated tests: `RESCS/tests/integration/test_s3_live.py` (`requires_live_s3`).

## 3. R.E.S.C.S. live PostgreSQL / Supabase

| Preconditions | A live PostgreSQL (or Supabase) instance |
| Run | `RESCS_INTEGRATION_DATABASE_URL=... pytest tests/integration/test_postgres_compat.py -q` |
| Acceptance | `requires_postgres` guard unsets and the backend assertion passes |
| After | Tear down any seeded data |

## 4. R.E.S.C.S. endurance

| Preconditions | Non-primary hardware; run 24/7 as a future task, not a flag |
| Run | `RESCS_ENDURANCE_SECONDS=86400 pytest tests/integration/test_reliability.py -q` (budget default 5 s) |
| Acceptance | Clean run across the full budget |
| Do NOT | Set endurance > 5 s on the MacBook (AGENT.md) |

## 5. A.S.I.S. / A.S.C.S. live voice + model

| Preconditions | Real microphone/speaker HW; Ollama `qwen3-coder:30b` (~19 GB) for A.S.C.S. |
| Run | ASIS: `ASIS_REAL_VOICE_TESTS=1`, `ASIS_TRANSLATION_LIVE=1`, `ASIS_WEB_LIVE=1`
  (see `ASIS/tests/test_voice_real.py`, `test_translation_live.py`, `test_web_live.py`);
  ASCS: `RISALIVE=1` |
| Acceptance | `needs_real`/live guards unsets and pass |
| Do NOT | Run these on this MacBook — voice live flags and 30b model are
  explicitly forbidden in AGENT.md; document only |

## 6. T.I.V.I.S.S. external verification

| Status | **LOCAL VERIFIED** — local checkout exists at `RISARMS/TIVISS-HOST/` and passes **279 tests**. To re-verify against upstream, clone `https://github.com/Kishir298/TIVISS-HOST` fresh and run its test suite. Do not clone it into the RISARMS workspaces without explicit direction |

## Related

- [Testing](testing.md)
- [LAN Readiness](https://github.com/Kishir298/CORE-HOST/blob/main/docs/lan-readiness.md) — canonical host-side checklist