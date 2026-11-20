# External Validation Runbook

> [!NOTE] **Status:** These validations require physical hardware, network access, or
> cloud credentials that are NOT available in the automated localhost environments.
> Until exercised, every item below is **NOT PERFORMED** — automated localhost
> testing must never be presented as hardware/cloud validation.

## Overview

All software defects from the 2026-10-01 audit have been fixed and verified in localhost
environments. The following validations require infrastructure that cannot be
provisioned in CI/dev environments. They are documented here for execution when
the required resources are available.

Each validation is **independent** and can be run in any order when its
prerequisites are met.

---

## Validation Inventory

| # | Validation | Category | Blockers | Est. Duration |
|---|------------|----------|----------|---------------|
| 1 | Physical LAN (Void CORE host ↔ RISARMS-ui clients: macOS Intel, macOS Apple Silicon, Windows x86_64, Linux x86_64 — NOT YET PERFORMED) | Network | Installed Void host on LAN, Caddy trust | 2-4 hours |
| 2 | Live PostgreSQL/Supabase (RESCS) | Cloud | DB instance + credentials | 30 min |
| 3 | Live S3 (RESCS) | Cloud | S3 bucket + credentials | 30 min |
| 4 | 24/7 Endurance (RESCS) | Hardware | Dedicated non-primary machine | 24 hours |
| 5 | Live Voice + Model (ASIS/ASCS) | Hardware | Mic/speaker, GPU, 32GB+ RAM | 2-4 hours |
| 6 | TIVISS Upstream Verification | Network | Fresh clone of upstream | 10 min |
| 7 | Historical physical Pi/ARM64 (CORE + RESCS) | Hardware | Not a CORE 0.6.0 target | 2-4 hours |

---

## 1. Physical LAN — Void CORE ↔ RISARMS-ui

> [!NOTE] **Target matrix (NOT YET PERFORMED):** physical Void CORE host ↔
> RISARMS-ui clients on **macOS Intel, macOS Apple Silicon, Windows x86_64 and
> Linux x86_64**. Historical two-machine Windows-host ↔ Mac tests retain their
> original dates/context in earlier reports; they do not satisfy this matrix.

### Prerequisites
- HP 14 (reference deployment machine) running Void Linux, installed per [Void Linux host](void-linux.md), Caddy trusted
- RISARMS-ui on a separate LAN device (macOS Intel, macOS Apple Silicon, Windows x86_64 or Linux x86_64)
- Only TCP `443` exposed publicly; CORE and RESCS remain loopback-bound

### Procedure
```bash
# On the Void host
sudo risarms-doctor
curl https://core.local/api/health

# On the desktop client
# Sign in at https://core.local, then verify messaging, reconnect and revocation.
```

### Validation Checklist
- [ ] Device registers and the owner device is bound
- [ ] TLS trust works without disabling certificate verification
- [ ] Human-to-human messaging works over WSS
- [ ] Revocation takes effect on reconnect
- [ ] Portal mutations require the CSRF header
- [ ] No session token or private key is written to the desktop profile
- [ ] Host logs contain no credentials or provisioning tokens

### Acceptance Criteria
All checklist boxes ticked; traffic works over the LAN with certificate verification enabled; no secrets in logs.

### Do NOT
- Wait 24h for lease expiry (fake-clock tests cover it)
- Disable TLS or fall back to plaintext
- Commit `var/rescs.json` or cert material

---

## 2. Live PostgreSQL / Supabase (RESCS)

### Prerequisites
- Live PostgreSQL instance (local or Supabase)
- `RESCS_INTEGRATION_DATABASE_URL` environment variable set

### Procedure
```bash
cd RESCS
RESCS_INTEGRATION_DATABASE_URL="postgresql://user:pass@host:5432/db" \
  .venv/bin/python -m pytest tests/integration/test_postgres_compat.py -q -v
```

### Acceptance Criteria
- `requires_postgres` pytest guard unsets
- All backend assertions pass
- Connection pooling / migration / query tests pass

### Cleanup
Tear down any seeded data after run.

---

## 3. Live S3 (RESCS)

### Prerequisites
- Real S3 bucket + credentials:
  - `RESCS_LIVE_S3_ACCESS_KEY`
  - `RESCS_LIVE_S3_SECRET_KEY`
  - `RESCS_LIVE_S3_BUCKET`
  - `RESCS_LIVE_S3_REGION`
- Keys must rotate after test

### Procedure
```bash
cd RESCS
RESCS_LIVE_S3_ACCESS_KEY=... \
RESCS_LIVE_S3_SECRET_KEY=... \
RESCS_LIVE_S3_BUCKET=... \
RESCS_LIVE_S3_REGION=... \
  .venv/bin/python -m pytest tests/integration/test_s3_live.py -q -v
```

### Acceptance Criteria
- `requires_live_s3` pytest guard unsets
- Suite passes against real bucket (upload/download/list/delete)

### After
**Rotate the access/secret keys immediately after run.**

---

## 4. RESCS 24/7 Endurance

### Prerequisites
- Non-primary hardware (dedicated test machine)
- NOT the development MacBook (AGENT.md forbids >5s budget on shared hardware)

### Procedure
```bash
cd RESCS
RESCS_ENDURANCE_SECONDS=86400 .venv/bin/python -m pytest tests/integration/test_reliability.py -q
```

### Acceptance Criteria
- Clean run across full 24h budget (86400 seconds)
- No memory leaks, connection leaks, or degradation

### Do NOT
- Set endurance > 5s on shared hardware

---

## 5. Live Voice + Model (ASIS / ASCS)

### Prerequisites
- Physical microphone + speaker hardware
- Ollama `qwen3-coder:30b` (~19 GB) for ASCS; `qwen3:14b` for ASIS
- ≥32 GB RAM machine (16 GB → fallback model `qwen2.5-coder:14b`)
- `RISALIVE=1` explicitly set (never enabled in CI/dev)

### Procedure

**ASIS:**
```bash
cd ASIS
ASIS_REAL_VOICE_TESTS=1 \
ASIS_TRANSLATION_LIVE=1 \
ASIS_WEB_LIVE=1 \
  .venv/bin/python -m pytest \
  tests/test_voice_real.py \
  tests/test_translation_live.py \
  tests/test_web_live.py -q -v
```

**ASCS:**
```bash
cd ASCS
RISALIVE=1 .venv/bin/python -m pytest tests/integration/test_ollama_live.py -q -v
```

### Acceptance Criteria
- `needs_real` / live pytest guards unset and pass
- Voice capture → STT → chat → TTS pipeline works end-to-end
- Translation with live model produces coherent output
- Web search/fetch with live model works

### Do NOT
- Run these on CI/dev machines — voice live flags and 30b model are explicitly forbidden in AGENT.md

---

## 6. TIVISS External Verification

### Prerequisites
- Internet access
- Fresh clone of upstream (not the local `RISARMS/TIVISS/` clone)

### Procedure
```bash
git clone https://github.com/Kishir298/TIVISS
cd TIVISS
python3 -m pytest -q -v
```

### Acceptance Criteria
- Upstream test suite passes (279+ tests; local clone verified at 279)
- No regressions vs local clone

---

## Test Markers Reference

Each repo uses pytest markers to gate live tests:

| Repo | Marker | Env Var | Command |
|------|--------|---------|---------|
| RESCS | `requires_postgres` | `RESCS_INTEGRATION_DATABASE_URL` | `pytest -m requires_postgres` |
| RESCS | `requires_live_s3` | `RESCS_LIVE_S3_*` | `pytest -m requires_live_s3` |
| RESCS | `requires_endurance` | `RESCS_ENDURANCE_SECONDS` | `pytest -m requires_endurance` |
| ASIS | `needs_real` (voice) | `ASIS_REAL_VOICE_TESTS=1` | `pytest -m needs_real` |
| ASIS | `needs_real` (translation) | `ASIS_TRANSLATION_LIVE=1` | `pytest -m needs_real` |
| ASIS | `needs_real` (web) | `ASIS_WEB_LIVE=1` | `pytest -m needs_real` |
| ASCS | `live` | `RISALIVE=1` | `pytest -m live` |
| TIVISS | (none) | — | `pytest` |

---

## Running All External Validations (When Infrastructure Ready)

```bash
# 1. LAN (run on the Void host + RISARMS-ui desktop client)
# 2. PostgreSQL
cd RESCS && RESCS_INTEGRATION_DATABASE_URL=... .venv/bin/python -m pytest tests/integration/test_postgres_compat.py -q

# 3. S3 (rotate keys after!)
cd RESCS && RESCS_LIVE_S3_*=... .venv/bin/python -m pytest tests/integration/test_s3_live.py -q

# 4. Voice + Model (dedicated GPU machine)
cd ASIS && ASIS_REAL_VOICE_TESTS=1 ASIS_TRANSLATION_LIVE=1 ASIS_WEB_LIVE=1 .venv/bin/python -m pytest tests/test_voice_real.py tests/test_translation_live.py tests/test_web_live.py -q
cd ASCS && RISALIVE=1 .venv/bin/python -m pytest tests/integration/test_ollama_live.py -q

# 5. Endurance (dedicated machine, 24h)
cd RESCS && RESCS_ENDURANCE_SECONDS=86400 .venv/bin/python -m pytest tests/integration/test_reliability.py -q

# 6. TIVISS upstream
git clone https://github.com/Kishir298/TIVISS && cd TIVISS && python3 -m pytest -q
```

---

## 7. Historical physical Raspberry Pi / ARM64 — CORE + RESCS

> [!WARNING]
> Historical only. CORE 0.6.0 targets Void Linux x86_64 with runit; the current
> path is [Void Linux host](void-linux.md).

### Prerequisites
- Raspberry Pi 4/5 (ARM64), Raspberry Pi OS 64-bit, cgroup v2, systemd
- Dedicated SSD mounted at `/srv/core`
- Release artifacts from `CORE/install/` and `RESCS/`

### Procedure
```bash
# On the Pi
sudo bash CORE/deployment/pi/install.sh
# Verify services and boot persistence
systemctl status core-host rescs
curl http://127.0.0.1:8081/health
# From CORE/CORE-HOST, exercise the real loopback
.venv/bin/python ../../RESCS/scripts/validate_core_loopback.py
```

### Validation Checklist
- [ ] Installer completes on clean ARM64 hardware
- [ ] `core-host` and `rescs` start on boot
- [ ] `/srv/core` mount guard blocks a missing mount
- [ ] CORE ↔ RESCS loopback passes
- [ ] Reboot and power-loss restart are clean
- [ ] No credentials appear in logs

### Acceptance Criteria
All checklist boxes ticked; reboot persistence verified; loopback passes on-device.

---

## Recording Results

When validations are performed, record:

1. **Date / Environment** (OS, hardware, network)
2. **Command Run** (exact command with redacted secrets)
3. **Outcome** (PASS / FAIL / PARTIAL)
4. **Failures** (exact error messages, logs)
5. **Duration** (wall-clock time)
6. **Artifacts** (logs, screenshots, metrics)

Store results in `validation-results/<date>-<validation>/` for audit trail.

---

## Related Documentation

- [Testing](testing.md) — Local test suite status
- [Hardware-Gated Validation](hw-gated-validation.md) — Original blocker matrix
- [LAN Readiness](https://github.com/Kishir298/CORE/blob/main/CORE-HOST/docs/lan-readiness.md) — Host-side preflight
- [ADR 0007](../decisions/0007-ascs-standalone-coding-agent.md) — ASIS↔ASCS local-tool exception