# Hardware-Gated Validation Runbook

> [!NOTE] **Status:** These validations require physical hardware, network access, or
> cloud credentials that are NOT available in the automated localhost environments.
> Until exercised, every item below is **NOT PERFORMED** — automated localhost
> testing must never be presented as hardware/cloud validation. Run serially, one
> item at a time, and never on a machine you need to keep free.

## Current status (2026-11-09)

Most items are **BLOCKED** in this workspace — the preconditions below cannot be
satisfied here (no Raspberry Pi/ARM64 hardware, no Windows host on LAN, no cloud
credentials, no dedicated endurance hardware, voice/model live runs forbidden by
AGENT.md). These are honest blockers, not open bugs: re-open only when the listed
resource exists.

| # | Validation | Status | Blocker |
|---|------------|--------|---------|
| 1 | Physical Pi/ARM64 deployment (CORE + RESCS) | ❌ BLOCKED | No Pi/ARM64 hardware, cgroup v2 systemd host, `/srv/core` mount, or SSD removal test |
| 2 | Physical LAN (host ↔ device) | ❌ BLOCKED | No Windows host on the LAN; firewall + TLS certs not re-verifiable |
| 3 | R.E.S.C.S. live S3 | ❌ BLOCKED | No bucket or `RESCS_LIVE_S3_*` credentials (keys must rotate after) |
| 4 | R.E.S.C.S. live PostgreSQL/Supabase | ❌ BLOCKED | No live DB or `RESCS_INTEGRATION_DATABASE_URL` |
| 5 | R.E.S.C.S. 24/7 endurance | ❌ BLOCKED | Needs non-primary hardware; >5 s budget is forbidden on the MacBook |
| 6 | A.S.I.S./A.S.C.S. live voice + model | ❌ BLOCKED | Requires mic/speaker + Ollama 30b; live flags forbidden by AGENT.md here |
| 7 | T.I.V.I.S.S. external verification | ✅ LOCAL VERIFIED | Local `TIVISS/` checkout passes 279 tests; upstream re-clone still optional |

## Rules that always apply

- Never commit `*.key`, `*.pem`, `*.crt`, `*.jks`, `var/rescs.json`,
  `*-device.json`, `.env*`, or any file containing a credential/token.
- Never disable TLS or fall back to plaintext for LAN validation.
- Rotate cloud keys after any live-cloud run.
- Keep live runs separate from CI/dev machines. On shared hardware do not set
  `RESCS_ENDURANCE_SECONDS` above its default (5 s).

## 0. Physical Raspberry Pi / ARM64 deployment (CORE + RESCS)

| Preconditions | Raspberry Pi 4/5 (ARM64), Raspberry Pi OS 64-bit, cgroup v2, systemd, dedicated SSD mounted at `/srv/core` |
| Source of truth | `CORE/deployment/pi/README.md`, `CORE/deployment/pi/install.sh`, `RESCS/deploy/pi/` |
| Procedure | Run the CORE Pi installer on clean hardware; verify systemd units, `/srv/core` guard, service health, and reboot persistence; then exercise CORE ↔ RESCS loopback |
| Acceptance | Services start on boot, `/srv/core` is enforced, loopback passes, no secrets in logs, clean restart after power loss |
| Do NOT | Treat macOS x86_64 unit tests as Pi/ARM64 validation; commit device certs or provisioning tokens |

## 1. Physical LAN — C.O.R.E. host ↔ R.I.S.A.R.M.S. device

| Preconditions | Windows host + Mac on the same LAN; firewall rule `C.O.R.E. TCP 5000`
  re-verified per `CORE/CORE-HOST/docs/windows-firewall.md`; fresh TLS cert — private
  `core.key` host-only, public `core.crt` copied to the Mac; CORE-HOST +
  CORE-CLIENT `--help` smoke |
| Source of truth | `CORE/CORE-HOST/docs/lan-readiness.md` (preflight §0, checklist)
  and `CORE/CORE-HOST/docs/device-communication.md` (status NOT YET PERFORMED) |
| Procedure | Follow `lan-readiness.md` preflight → run the live window → tick
  every box in the validation checklist (§0 checklist) in-docs |
| Acceptance | All checklist boxes ticked; host log shows authenticated external
  device with token visible only when `log_external_device_tokens: true`;
  remembered-device file contains NO session token/credential |
| Do NOT | Wait 24 h for lease expiry (fake-clock tests cover it), disable TLS,
  or commit `var/rescs.json` / cert material |

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

| Status | **LOCAL VERIFIED** — local checkout exists at `RISARMS/TIVISS/` and passes **279 tests**. To re-verify against upstream, clone `https://github.com/Kishir298/TIVISS` fresh and run its test suite. Do not clone it into the RISARMS workspaces without explicit direction |

## Related

- [Testing](testing.md)
- [LAN Readiness](../../CORE/CORE-HOST/docs/lan-readiness.md) — canonical host-side checklist