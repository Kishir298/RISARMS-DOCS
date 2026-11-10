# Development Roadmap

> [!NOTE] **Purpose:** The consolidated, cross-system roadmap. The authoritative per-system plan is in each system page ([`../systems/`](../systems/)); this document is the strategic view and the status legend. Status: **IN DEVELOPMENT** for the overall effort (integration phase).

## 1. Status legend

Every roadmap item carries one of:

> [!NOTE] **IMPLEMENTED** / **IN DEVELOPMENT** / **PLANNED** / **FUTURE** — defined in [Architecture Overview](../architecture/overview.md#3-status-vocabulary).

## 2. Strategic order

The ecosystem matures in this order (current position in brackets):

1. ~~**C.O.R.E. v0.2** — make the control engine operational~~ — **IMPLEMENTED** (shipped 0.2.0 → 0.2.1; superseded by v0.3.0).
2. ~~**R.E.S.C.S. v0.1 completion**~~ — **IMPLEMENTED** (now v0.4.0 with full API, enforced auth, signed CORE owner scope, and Pi mount foundation).
3. **C.O.R.E. ↔ R.E.S.C.S. integration** — **IMPLEMENTED in software** (adapter + signed scope + real loopback validation); deployed cross-host interop is the remaining validation step.
4. **Deployment validation** — physical Raspberry Pi/ARM64, Windows ↔ Mac LAN, and 24/7 endurance for C.O.R.E.; live PostgreSQL/Supabase + real S3 for R.E.S.C.S. ← *current frontier*
5. **A.S.I.S. completion + integration** — wire voice into the chat loop, remove legacy `core/` + `02_voice/` trees (deprecated, pending removal), then connect A.S.I.S. to C.O.R.E. (**IN DEVELOPMENT**). **ASIS ↔ ASCS integration IMPLEMENTED** (`ascs_integration` toolset + `export_handover_state()` handover protocol). Pi policy/worker path added.
6. **A.S.I.S. ↔ C.O.R.E. contract** — the intelligence layer operates through the control engine (**PLANNED**).
7. **T.I.V.I.S.S.** — v0.2.0 local agent: OllamaProvider, SQLiteMemoryStore (dual SQLite), CLI, export/import, logging, voice abstraction, stdlib-only transports offline-tested (**IN DEVELOPMENT**; handover model unresolved).
8. **A.S.C.S. ecosystem role** — ASIS integration **IMPLEMENTED** (`export_handover_state()` + `ascs_integration` toolset). Pi headless generation-only path added. C.O.R.E.-mediated use by A.S.I.S./T.I.V.I.S.S. is **FUTURE**.
9. **RadarS.A.R.D.** — detection/reporting into C.O.R.E. (**FUTURE**).

## 3. C.O.R.E. roadmap

The 13-phase v0.2 build order is **complete**; the per-phase definitions live in CORE's git history. v0.3.0 added the external-device platform, v0.3.1 added CapabilityRouter/ModelProfile and RescsDeviceProxy, v0.4.0 added the localhost host/client portals, and v0.5.0 combined the host/client project and added Pi service integration. Current state:

| Capability area | Status |
|---|---|
| v0.2 phases 1–13 (runtime → release) | **IMPLEMENTED** |
| TLS external transport, token auth, device lifecycle/persistence, discovery, device-to-device routing | **IMPLEMENTED** |
| Agent scheduling (capability-driven, `asis-local`/`asis-offload`/`tiviss-compat` profiles) | **IMPLEMENTED** |
| CapabilityRouter with ModelProfile and RescsDeviceProxy | **IMPLEMENTED (v0.3.1)** |
| Host/client portals | **IMPLEMENTED (v0.4.0)** |
| Combined `CORE/` project, Pi service integration, signed RESCS owner scope, `/api/ai-status`, tool-free safe-chat worker | **IMPLEMENTED (v0.5.0)** |
| R.E.S.C.S. adapters (`InMemory`/`File`/`Http`) + data distribution | **IMPLEMENTED** |
| Physical Raspberry Pi/ARM64 deployment | **NOT YET PERFORMED** |
| Physical Windows ↔ Mac LAN validation | **NOT YET PERFORMED** |
| 24/7 operational validation | **NOT YET PERFORMED** |

## 4. R.E.S.C.S. roadmap (summary)

R.E.S.C.S. documents its own history in `RESCS/CHANGELOG.md` and `docs/architecture.md`. Highlights:

| Item | Status |
|---|---|
| Health API, repositories, database layer | IMPLEMENTED |
| Versioned record/file HTTP endpoints (`/api/v1`) | IMPLEMENTED |
| `X-API-Key` enforcement + owner scoping | IMPLEMENTED |
| Signed CORE owner scope (`X-RESCS-Signature`) and device ownership validation | **IMPLEMENTED (v0.4.0)** |
| Required `/srv/core` mount guard, installer, systemd units | **IMPLEMENTED (v0.4.0)** |
| Object/file storage (local, memory, S3-compatible) | IMPLEMENTED (real S3 not yet exercised) |
| Streaming + resumable uploads, TTL/lifecycle, quotas, audit, backup tooling | IMPLEMENTED |
| Machine-readable C.O.R.E. contract (`GET /api/v1/contract`) | IMPLEMENTED |
| Real C.O.R.E. loopback validation | **IMPLEMENTED (0.4.0 script)** |
| Live PostgreSQL/Supabase deployment | **Ready for External Validation** |
| Deployed C.O.R.E. ↔ R.E.S.C.S. interop | **Ready for External Validation** |
| Physical Pi/ARM64 validation | **Ready for External Validation** |
| 24/7 endurance | **Ready for External Validation** |

## 5. A.S.I.S. roadmap (summary)

| Item | Status |
|---|---|
| Rebuilt `asis` package: CLI, AI provider layer (Ollama + mock), memory, tool framework, permissions, identity, events, system/runtime | IMPLEMENTED |
| Concrete tools (Echo, CurrentTime) | IMPLEMENTED |
| Voice pipeline abstraction (engines, input/speech/speaker/tts packages) | IMPLEMENTED (standalone) |
| Test suite (941 passed / 24 skipped, v0.1.0) | IMPLEMENTED |
| Voice wired into the chat loop | IMPLEMENTED |
| Legacy tree removal (`core/`, `02_voice/`, `monitoring/`) | DEPRECATED, pending removal |
| Real C.O.R.E. uplink (opt-in adapter) | IMPLEMENTED (standalone by default) |
| **ASCS integration (`ascs_integration` toolset: subprocess + API modes, `ascs_handover`, `ascs_status`)** | **IMPLEMENTED** |
| **ASCS handover protocol (`export_handover_state()` + `ascs_handover` tool)** | **IMPLEMENTED** |
| **Pi policy/worker path (no tools/voice on Pi)** | **IMPLEMENTED** |

## 6. T.I.V.I.S.S.

Agent **IN DEVELOPMENT** (v0.2.0), local clone present (`TIVISS/`): OllamaProvider, SQLiteMemoryStore (dual SQLite), CLI, export/import, logging, voice abstraction, and stdlib-only C.O.R.E./R.E.S.C.S. transports tested offline. Verified: 279 passed. The defining open question — the handover model — is unresolved; see [systems/tiviss.md](../systems/tiviss.md).

## 7. A.S.C.S.

**IMPLEMENTED as a standalone tool** (v0.3.0, 991 passed / 6 skipped on macOS 2026-11-09; Linux/Pi headless generation-only). See [systems/asc.md](../systems/asc.md). Its own phase roadmap (00–06) lives in `ASCS/docs/phases/`. **ASIS integration IMPLEMENTED** (`export_handover_state()` + `ascs_integration` toolset). C.O.R.E.-mediated use by A.S.I.S./T.I.V.I.S.S. is **FUTURE**.

## 8. RadarS.A.R.D.

**FUTURE.** Design intent documented in [systems/radar-sard.md](../systems/radar-sard.md). C.O.R.E.'s device transport and data-distribution path are the natural reporting route when development starts.

## Related

- [Versioning](versioning.md)
- [Testing](testing.md)
- [Pi release 2026-11-06](pi-release-2026-11-06.md)
- [Contribution](contribution.md)
- [Architecture Overview](../architecture/overview.md)
