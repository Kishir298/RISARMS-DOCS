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
| 1 | Physical LAN (CORE-HOST ↔ CORE-CLIENT) | Network | Windows host on LAN, TLS certs | 2-4 hours |
| 2 | Live PostgreSQL/Supabase (RESCS) | Cloud | DB instance + credentials | 30 min |
| 3 | Live S3 (RESCS) | Cloud | S3 bucket + credentials | 30 min |
| 4 | 24/7 Endurance (RESCS) | Hardware | Dedicated non-primary machine | 24 hours |
| 5 | Live Voice + Model (ASIS/ASCS) | Hardware | Mic/speaker, GPU, 32GB+ RAM | 2-4 hours |
| 6 | TIVISS Upstream Verification | Network | Fresh clone of upstream | 10 min |
| 7 | Physical Pi/ARM64 (CORE + RESCS) | Hardware | Raspberry Pi, 64-bit OS, SSD at `/srv/core` | 2-4 hours |

---

## 1. Physical LAN — CORE-HOST ↔ CORE-CLIENT

### Prerequisites
- Windows host + Mac/Linux client on same LAN
- Firewall rule `C.O.R.E. TCP 5000` verified per `CORE/CORE-HOST/docs/windows-firewall.md`
- Fresh TLS cert: private `core.key` (host-only), public `core.crt` copied to client
- CORE-HOST + CORE-CLIENT `--help` smoke test passes

### Procedure
```bash
# On Windows host (CORE-HOST)
cd CORE/CORE-HOST
venv\Scripts\python -m core --host 0.0.0.0 --port 5000 --tls --certfile core.crt --keyfile core.key

# On client machine (CORE-CLIENT)
cd CORE/CORE-CLIENT
.venv/bin/python -m client.core_device_client \
  --host <WINDOWS_HOST_IP> \
  --port 5000 \
  --device-file ./device.json \
  --ca-file core.crt \
  --token <PROVISIONING_TOKEN>
```

### Validation Checklist
- [ ] Device registers successfully (`DEVICE_REGISTER_RESPONSE` with `registered: true`)
- [ ] Device discovery works (`DEVICE_DISCOVER_RESPONSE` lists both devices)
- [ ] Device-to-device relay works (sender gets no reply, receiver gets message)
- [ ] Portal accessible at `http://<WINDOWS_HOST>:8765` from client browser
- [ ] Portal mutations require `X-Core-Request` header (403 without)
- [ ] Host log shows authenticated external device (token only visible with `log_external_tokens: true`)
- [ ] Remembered device file (`~/.risarms-device.json`) contains NO session token/credential
- [ ] Reconnect works: client reconnects with same provisioning token, new session token issued

### Acceptance Criteria
All checklist boxes ticked; host log shows authenticated external device; remembered-device file contains NO session token.

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
# 1. LAN (run on Windows host + client machine)
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

## 7. Physical Raspberry Pi / ARM64 — CORE + RESCS

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
- [LAN Readiness](../../CORE/CORE-HOST/docs/lan-readiness.md) — Host-side preflight
- [ADR 0007](../decisions/0007-ascs-standalone-coding-agent.md) — ASIS↔ASCS local-tool exception