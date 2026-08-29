# Data Flow

> [!NOTE] **Status:** Data ownership is fixed by the architecture. Current implementation is limited to what each system has already built (see status markers throughout and in [`systems/`](../systems/)).

## Purpose

This document describes **where data lives and flows**. It is a companion to [Communication Flow](communication-flow.md) (the message layer) and [System Boundaries](system-boundaries.md) (ownership).

## 1. Data ownership

| Data | Owner | Storage | Status |
|---|---|---|---|
| C.O.R.E. runtime/operational state (configuration, resources, health, events) | **C.O.R.E.** | Local, in-process-visible; configuration in YAML + env | **IMPLEMENTED** (in-process) |
| C.O.R.E. durable records | **C.O.R.E.** | To be decided — likely via R.E.S.C.S. through the adapter | **PLANNED** |
| Records (structured data) | **R.E.S.C.S.** | R.E.S.C.S. database (SQLAlchemy; SQLite dev, PostgreSQL prod) | Repository layer **IMPLEMENTED**; HTTP API **PLANNED** |
| Files / objects | **R.E.S.C.S.** | R.E.S.C.S. object storage (planned `storage/` layer) | **PLANNED** |
| Shared/cloud-backed data | **R.E.S.C.S.** | Cloud-backed (PostgreSQL/Supabase pathconfigured; object store planned) | **PLANNED** |
| A.S.I.S. memory (conversation context, remembered facts, user identity) | **A.S.I.S.** | Local (JSON memory file; SQLite `MemoryDatabase`) | **IMPLEMENTED** (local only) |
| T.I.V.I.S.S. memory/identity | **T.I.V.I.S.S.** | Undefined (future) | **FUTURE** |
| RadarS.A.R.D. detections/alerts | **RadarS.A.R.D.** (produces) → **C.O.R.E.** (coordinates) | Undefined (future); reports flow to C.O.R.E. | **FUTURE** |

> [!NOTE] **Storage ≠ data.** R.E.S.C.S. is the storage *system*; it does not automatically own every byte in the ecosystem. A.S.I.S. memory is local to A.S.I.S. today. The future model may persist long-term ecosystem data through R.E.S.C.S., but that is not the current implementation.

## 2. The storage request path (intended)

```mermaid
sequenceDiagram
    participant CALLER as Caller (e.g. A.S.I.S.)
    participant CORE as C.O.R.E.
    participant ADAPTER as R.E.S.C.S. Adapter
    participant RESCS as R.E.S.C.S.
    participant DB as Database / Object Store

    CALLER->>CORE: store/retrieve request
    CORE->>ADAPTER: routed service call (Phase 9)
    ADAPTER->>RESCS: HTTP request (R.E.S.C.S. API)
    RESCS->>DB: persist / query
    DB->>RESCS: result
    RESCS->>ADAPTER: response
    ADAPTER->>CORE: response
    CORE->>CALLER: result
```

**Current reality:** The adapter, the R.E.S.C.S. record/file HTTP API, and the caller contract are all **PLANNED**. What exists: R.E.S.C.S. repository backends (memory + SQLAlchemy) and its database layer, both tested at the repository level.

## 3. Data flow rules

1. **Storage logic lives in R.E.S.C.S.** C.O.R.E. adapters translate requests; they never re-implement persistence.
2. **No data-plane coupling between A.S.I.S. and R.E.S.C.S.** A.S.I.S. reaches stored data through C.O.R.E. only.
3. **Sync/shared-data semantics are owned by R.E.S.C.S.** and will be defined there (see [rescs.md](../systems/rescs.md)).
4. **Observability data** (health state, events, logs) is C.O.R.E.'s domain and stays with C.O.R.E.; radar detections are the exception, reported *into* C.O.R.E. by RadarS.A.R.D. for coordination.

## Related

- [Data ownership and caching decisions](../decisions/README.md)
- [R.E.S.C.S. system page](../systems/rescs.md)
- [A.S.I.S. system page](../systems/asis.md)
- [Integration Contracts](../interfaces/integration-contracts.md)