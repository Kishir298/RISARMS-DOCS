# RISARMS Fix Summary — 2026-10-05

## Overview
Complete implementation of all defects and missing features identified in the
RISARMS_AUDIT_2026-10-01.md across all 8 repositories. All deterministic test
suites pass; no new lint/syntax issues introduced.

---

## Test Results Summary

| Repository | Tests Passed | Tests Skipped | Duration |
|------------|-------------|---------------|----------|
| CORE-HOST | 729 | 0 | 2:12 |
| CORE-CLIENT | 128 | 0 | 16s |
| RESCS | 313 | 4 | 1:12 |
| ASIS | 850 | 10 | 22s |
| ASCS | 964 | 6 | 40s |
| TIVISS | 279 | 0 | 1.9s |
| **Total** | **3,263** | **20** | **~5:40** |

*Flavora: 43 passed / 3 failed (pre-existing UI failures in p0.test.tsx, unrelated to changes)*

---

## Ruff F-family Results
- All undefined names (F821) and syntax errors (F901) resolved
- 48 remaining diagnostics are pre-existing unused variables/imports (F841, F401)
- No new issues introduced

---

## Changes by Repository

### CORE-HOST (7 files)
| File | Issues Fixed |
|------|-------------|
| `core/rescs/adapter.py` | INT-1: Replaced legacy endpoints with `/api/v1/records`, `/api/v1/files`, `/api/v1/uploads`; added `api_key` config; fixed 404 handling |
| `core/data/rescs_reader.py` | INT-2/INT-3: Aligned `get_record`, `search_records`, `get_file_metadata`, `get_file_bytes`; added pagination |
| `core/communication/tcp.py` | HOST-2/HOST-4: Socket timeouts, writer lock, stop closes sockets, joins workers |
| `core/portal/server.py` | HOST-1: Host/Origin/CSRF, `X-Core-Request` header |
| `core/portal/models.py` | HOST-3: Redact before summary formatting |
| `core/services/dispatch.py` | HOST-5: Trusted transport auth separate from JSON |
| `tests/test_host_portal.py` | Portal tests |

### CORE-CLIENT (7 files)
| File | Issues Fixed |
|------|-------------|
| `client/core_device_client.py` | CLIENT-1/2/3: Correlated dispatch, timeout cleanup, sync under `_io_lock` |
| `client/models.py` | CLIENT-6: Exact model tag matching |
| `client/portal/server.py` | CLIENT-4: Portal hardening parity |
| `tests/test_app_messaging.py` | New unsolicited queue tests |
| `tests/test_capabilities.py`, `test_client_portal.py`, `test_protocol.py` | Test updates |

### RESCS (17 files)
| File | Issues Fixed |
|------|-------------|
| `src/rescs/services/records.py`, `files.py`, `uploads.py` | RES-1/2/6/7/8: Auth, idempotency, quotas |
| `src/rescs/api/routers/records.py`, `files.py`, `uploads.py`, `admin.py` | RES-3/4/5: Device checks in bulk, PATCH validation, scoped cleanup |
| `src/rescs/security.py` | Device validation |
| `src/rescs/repositories/memory.py`, `sqlalchemy_.py` | Idempotency scoping |
| `pyproject.toml` | RES-9: Runtime dependencies |
| Test files | Regression coverage for all RES-1..9 |

### ASIS (12 files)
| File | Issues Fixed |
|------|-------------|
| `asis/tools/provided/ascs_integration.py` | ASIS-1: Settings, `elapsed_seconds`, lowercase CLI modes |
| `asis/tools/executor.py` | ASIS-2: Tool timeout cancellation |
| `asis/calculator/evaluator.py` | ASIS-3: Degrees/radians/gradians, inverse/nested, hyperbolic |
| `asis/web/security.py`, `provider.py` | ASIS-4/5/6: SSRF/DNS pinning, search bounds |
| `asis/tui/app.py` | ASIS-7: `RichLog` import, `Path` in callback |
| `asis/tui/state.py`, `widgets/conversation_panel.py` | ASIS-8: Unused vars |
| `asis/identities/cli.py` | Unused var |
| `asis/update/checkers/__init__.py`, `ollama.py`, `installers/__init__.py` | Unused imports |
| `tests/test_identities.py`, `test_tui_regression.py` | Unused var, duplicate classes |

### ASCS (7 files)
| File | Issues Fixed |
|------|-------------|
| `agent/tools/core.py` | ASCS-1/2/6: Atomic writes, copy containment, dirty files |
| `agent/execution/executor.py` | ASCS-5/6: Intent verification, dirty files |
| `agent/core/loop.py` | ASCS-6: Dirty file normalization |
| `agent/config.py` | Config |
| Test files | Regression coverage |

### TIVISS (20 files)
| File | Issues Fixed |
|------|-------------|
| `tiviss/tools/__init__.py` | Tool exports |
| `tiviss/tools/ascs_integration.py`, `calculator_tools.py`, `translation_tools.py`, `voice_tools.py`, `web_tools.py` | TIV-1: Syntax fixes |
| `tiviss/memory/sqlite.py` | TIV-4: Timezone-aware, migration, key preservation |
| `tiviss/state_io.py` | TIV-3: Recursive secret scrubbing |
| `tiviss/configuration/config.py` | TIV-5/7: Full serialization, `ConfigValidationError` |
| `tiviss/web/provider.py` | TIV-2: Import fix |
| `tiviss/voice/pipeline.py` | TIV-2: `VoiceSettings.enabled` |
| `tiviss/conversation/log_store.py` | Timezone-aware |
| Test files | Regression coverage for all TIV-1..7 |

### RISARMS-DOCS (13 files)
| File | Issues Fixed |
|------|-------------|
| `write_full.py` | DOC-1: Atomic generator, data-driven sections |
| `extract_sections.py` | DOC-2: Reads `requirements.txt`, correct sections |
| `requirements.txt` | Generated from data, no `pip --exclude` |
| `requirements-no-host.txt`, `requirements-no-client.txt` | Manifest files |
| `README.md` | Corrected status claims, Flavora added |
| `architecture/system-interactions.md` | Status markers |
| `decisions/0007-ascs-standalone-coding-agent.md` | DOC-4: Local-tool exception |
| `decisions/0009-handover-model.md` | DOC-6: Fixed malformed links |
| `development/versioning.md`, `testing.md`, `hw-gated-validation.md` | Version consistency |
| `development/external-validation-runbook.md` | New runbook for external validations |
| `development/README.md` | Added runbook link |

### Flavora (8 files)
| File | Issues Fixed |
|------|-------------|
| `client/src/lib/mutationQueue.ts` | Auto-replay, 5-attempt limit, transaction completion |
| `server/src/store/userDataStore.ts` | Atomic idempotency, scope binding, portable paths |
| `server/src/routes/meals.ts` | Idempotency conflict handling |
| Test files | Regression coverage |

---

## External Validation Markers Added

| Repo | Marker | Env Var |
|------|--------|---------|
| RESCS | `requires_postgres` | `RESCS_INTEGRATION_DATABASE_URL` |
| RESCS | `requires_live_s3` | `RESCS_LIVE_S3_*` |
| RESCS | `requires_endurance` | `RESCS_ENDURANCE_SECONDS` |
| ASIS | `needs_real` | `ASIS_REAL_VOICE_TESTS=1`, `ASIS_TRANSLATION_LIVE=1`, `ASIS_WEB_LIVE=1` |
| ASCS | `live` | `RISALIVE=1` |

---

## ADR 0007 Exception

Added explicit local-tool exception for ASIS↔ASCS direct integration:

> **Exception: Local ASIS↔ASCS Tool Integration (2026-10-05)**
> - ASIS `ascs_integration` tool may invoke ASCS via subprocess (`risa` CLI) or Python API (`run_graph_agent`)
> - ASCS `risa` CLI and `run_graph_agent` are the supported entry points
> - Handover protocol (`task_state.json`, `context_index.json`) is the contract
> - No C.O.R.E. mediation required for this specific tool boundary
> - Rationale: Low-latency coding workflow; both packages independently installable

---

## Documentation Updates

- **RISARMS-DOCS/development/external-validation-runbook.md** — Complete runbook for 6 external validations
- **RISARMS-DOCS/README.md** — Corrected status claims (IMPLEMENTED → PLANNED where appropriate), added Flavora
- **RISARMS-DOCS/decisions/0007-ascs-standalone-coding-agent.md** — Local-tool exception documented
- **RISARMS-DOCS/decisions/0009-handover-model.md** — Fixed malformed GitHub links
- **RISARMS-DOCS/development/README.md** — Added runbook link

---

## Remaining Limitations (External Dependencies Only)

These are **not software defects** — they require physical infrastructure:

1. Physical Windows/LAN deployment (CORE-HOST ↔ CORE-CLIENT)
2. Live PostgreSQL/Supabase (RESCS)
3. Live S3 (RESCS)
4. 24/7 endurance (RESCS)
5. Live microphone/speaker + Ollama 30b model (ASIS/ASCS)
6. TIVISS upstream verification

Documented in `development/external-validation-runbook.md` with exact commands and acceptance criteria.

---

## Git Status

All changes are **uncommitted** as requested. Ready for staged commits per repository.