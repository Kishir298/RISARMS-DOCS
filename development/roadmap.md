# Development Roadmap

> [!NOTE] **Purpose:** The consolidated, cross-system roadmap. The authoritative per-system plan is in each system page ([`../systems/`](../systems/)); this document is the strategic view and the status legend. Status: **IN DEVELOPMENT** for the overall effort.

## 1. Status legend

Every roadmap item carries one of:

> [!NOTE] **IMPLEMENTED** / **IN DEVELOPMENT** / **PLANNED** / **FUTURE** — defined in [Architecture Overview](../architecture/overview.md#3-status-vocabulary).

## 2. Strategic order

The ecosystem matures in this order:

1. **C.O.R.E. v0.2** — make the control engine operational (13 phases).
2. **R.E.S.C.S. v0.1 completion** — record/file HTTP API, auth enforcement, object storage.
3. **C.O.R.E. ↔ R.E.S.C.S. integration** — the adapter contract goes live (C.O.R.E. Phase 9 + R.E.S.C.S. API).
4. **A.S.I.S. completion + integration** — finish voice, rename cleanup, connect A.S.I.S. to C.O.R.E.
5. **A.S.I.S. ↔ C.O.R.E. contract** — the intelligence layer operates through the control engine.
6. **External-device transport** — C.O.R.E. reaches off-host peers (Phase 10).
7. **RadarS.A.R.D.** — detection/reporting into C.O.R.E. (FUTURE).
8. **T.I.V.I.S.S.** — identity/ownership/handover model (FUTURE).

## 3. C.O.R.E. v0.2 roadmap

The authoritative detail (per-phase objectives, completion criteria, and "must not implement yet") is in [systems/core.md#6-core-v02-roadmap](../systems/core.md#6-core-v02-roadmap).

| Phase | Focus | Status |
|---|---|---|
| 1 | Runtime + application orchestration | Landed groundwork |
| 2 | Communication + transport abstraction | Landed groundwork |
| 3 | Routing + service execution | Landed groundwork |
| 4 | Resource + organization integration | Landed groundwork (partial) |
| 5 | Event-driven integration | Landed groundwork |
| 6 | Health integration | Landed groundwork |
| 7 | Configuration drives runtime | IN DEVELOPMENT |
| 8 | Security integration | IN DEVELOPMENT |
| 9 | R.E.S.C.S. adapter | PLANNED |
| 10 | External-device transport | PLANNED |
| 11 | Real CLI lifecycle | IN DEVELOPMENT |
| 12 | Full integration test spine | PLANNED |
| 13 | v0.2 cleanup/documentation/release | PLANNED |

## 4. R.E.S.C.S. roadmap (summary)

R.E.S.C.S. maintains its own detailed roadmap in `RESCS/docs/architecture.md` (13 phases; 1–2 complete). Cross-system highlights:

| Item | Status |
|---|---|
| Health API | IMPLEMENTED |
| Record/file repositories (memory + SQLAlchemy) | IMPLEMENTED |
| Database layer | IMPLEMENTED (groundwork) |
| Record/file HTTP endpoints | PLANNED |
| API-key enforcement | PLANNED |
| Object/file storage | PLANNED |
| C.O.R.E. integration contract | PLANNED (C.O.R.E. Phase 9) |

## 5. A.S.I.S. roadmap (summary)

| Item | Status |
|---|---|
| Chat runtime (Ollama) | IMPLEMENTED |
| Memory system | IMPLEMENTED |
| Tool framework | IMPLEMENTED (no concrete tools) |
| Event bus / security helpers | IMPLEMENTED |
| Voice input pipeline (mic → VAD → whisper → normalizer) | IMPLEMENTED (standalone) |
| Voice speaker/wakeword/TTS | PLANNED |
| Voice integrated into chat loop | PLANNED |
| Forza → A.S.I.S. naming/version cleanup | IN DEVELOPMENT |
| C.O.R.E. integration | PLANNED |

## 6. T.I.V.I.S.S.

**FUTURE.** Design intent documented in [systems/tiviss.md](../systems/tiviss.md). No roadmap until its open questions are resolved.

## 7. RadarS.A.R.D.

**FUTURE.** Design intent documented in [systems/radar-sard.md](../systems/radar-sard.md). Watch the C.O.R.E. Phase 10 device transport — RadarS.A.R.D. will report through a similar path.

## Related

- [Versioning](versioning.md)
- [Testing](testing.md)
- [Contribution](contribution.md)
- [Architecture Overview](../architecture/overview.md)