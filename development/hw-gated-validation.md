# Hardware-Gated Validation Runbook

> [!NOTE] **Status:** These validations require physical hardware, network access, or
> cloud credentials that are NOT available in the automated localhost environments.
> Until exercised, every item below is **NOT PERFORMED** — automated localhost
> testing must never be presented as hardware/cloud validation. Run serially, one
> item at a time, and never on a machine you need to keep free.

## Current status (2026-09-24)

Every item is **BLOCKED** in the current workspace — the preconditions below cannot
be satisfied here (no Windows host on LAN, no cloud credentials, no dedicated
hardware, no TIVISS checkout, voice/model live runs forbidden by AGENT.md). These
are honest blockers, not open bugs: re-open only when the listed resource exists.

| # | Validation | Status | Blocker |
|---|------------|--------|---------|
| 1 | Physical LAN (host ↔ device) | ❌ BLOCKED | No Windows host on the LAN; firewall + TLS certs not re-verifiable |
| 2 | R.E.S.C.S. live S3 | ❌ BLOCKED | No bucket or `RESCS_LIVE_S3_*` credentials (keys must rotate after) |
| 3 | R.E.S.C.S. live PostgreSQL/Supabase | ❌ BLOCKED | No live DB or `RESCS_INTEGRATION_DATABASE_URL` |
| 4 | R.E.S.C.S. 24/7 endurance | ❌ BLOCKED | Needs non-primary hardware; >5 s budget is forbidden on the MacBook |
| 5 | A.S.I.S./A.S.C.S. live voice + model | ❌ BLOCKED | Requires mic/speaker + Ollama 30b; live flags forbidden by AGENT.md here |
| 6 | T.I.V.I.S.S. external verification | ❌ BLOCKED | No local checkout; requires fresh clone of `Kishir298/TIVISS` |

## Rules that always apply

- Never commit `*.key`, `*.pem`, `*.crt`, `*.jks`, `var/rescs.json`,
  `*-device.json`, `.env*`, or any file containing a credential/token.
- Never disable TLS or fall back to plaintext for LAN validation.
- Rotate cloud keys after any live-cloud run.
- Keep live runs separate from CI/dev machines. On shared hardware do not set
  `RESCS_ENDURANCE_SECONDS` above its default (5 s).

## 1. Physical LAN — C.O.R.E. host ↔ R.I.S.A.R.M.S. device

| Preconditions | Windows host + Mac on the same LAN; firewall rule `C.O.R.E. TCP 5000`
  re-verified per `CORE-HOST/docs/windows-firewall.md`; fresh TLS cert — private
  `core.key` host-only, public `core.crt` copied to the Mac; CORE-HOST +
  CORE-CLIENT `--help` smoke |
| Source of truth | `CORE-HOST/docs/lan-readiness.md` (preflight §0, checklist)
  and `CORE-HOST/docs/device-communication.md` (status NOT YET PERFORMED) |
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

| Status | **OUT OF SCOPE** here — no local checkout exists (docs previously claimed
  `RISARMS/TIVISS/`; it is not present). The `254` count in the testing matrix
  is inherited and **unverified** until a fresh clone of
  `https://github.com/Kishir298/TIVISS` is exercised. Do not clone it into the
  RISARMS workspaces without explicit direction |

## Related

- [Testing](testing.md)
- [LAN Readiness](CORE-HOST `docs/lan-readiness.md` — canonical host-side checklist)