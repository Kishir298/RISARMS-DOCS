# R.E.S.C.S. — Rishik's Efficient System for Cloud Storage

> [!NOTE] **Status:** v0.1 **IMPLEMENTED** (Phases 1–2 per its own roadmap). Record/file HTTP API, authentication enforcement, and object storage are **PLANNED**. R.E.S.C.S. is an **independent project**.

## 1. What R.E.S.C.S. is

R.E.S.C.S. is the **cloud/data storage system** of R.I.S.A.R.M.S. It provides storage that the rest of the ecosystem uses.

### Responsibilities

- Cloud storage
- Persistent data
- File storage
- Data retrieval
- Synchronization
- Shared data
- Cloud-backed records
- Storage used by other systems

### Non-responsibilities

- Message routing, runtime, events, health-of-the-ecosystem (→ C.O.R.E.)
- Intelligence (→ A.S.I.S.)

## 2. Independence

> [!IMPORTANT] R.E.S.C.S. is an independent project. It must **never** be placed inside CORE. C.O.R.E. communicates with R.E.S.C.S. through defined interfaces and protocols — eventually the adapter defined in [Integration Contracts](../interfaces/integration-contracts.md). Rationale: ADR [0001](../decisions/0001-rescs-independent-from-core.md), ADR [0005](../decisions/0005-storage-integration-via-adapter.md).

- Location: `RISARMS/RESCS/` (sibling of `CORE/`, `ASIS/`, `DOCS/`)
- Own git repository (origin `https://github.com/Kishir298/RESCS.git`)
- Stack: Python ≥ 3.11, FastAPI + uvicorn, SQLAlchemy 2.0, psycopg 3 (PostgreSQL), Pydantic v2 + pydantic-settings
- Version: `0.1.0` (pyproject, package, schema manager, README all agree)

## 3. Project layout

```text
src/rescs/
├── main.py            # app factory + HTTP routes (health endpoints live)
├── config.py          # pydantic-settings (RESCS_* env prefix)
├── logging.py
├── errors.py          # RESCSError hierarchy with codes + HTTP statuses
├── health.py          # HealthService (named checks, worst-status aggregation)
├── domain.py          # RecordData, FileObjectData, Page dataclasses
├── api/routers/       # EMPTY — record/file routes planned
├── db/                # engine, schema manager, session scope, bootstrap
├── models/            # records + file_objects SQLAlchemy ORM
├── schemas/           # Pydantic request/response models
├── interfaces/        # repository Protocols (RecordRepository, FileObjectRepository)
├── repositories/      # memory.py + sqlalchemy_.py backends
├── services/          # EMPTY — business/service layer planned
└── storage/           # EMPTY — object/blob store planned
```

## 4. Current implementation (verified)

**IMPLEMENTED and tested:**

- **App factory** (`create_app`), lifespan logging, global `RESCSError` handler.
- **Live HTTP routes:** `GET /`, `GET /health/live`, `GET /health/ready`, `GET /health` (OpenAPI at `/docs`).
- **Config:** `RESCS_*` env vars, `.env` support, validators (API key min length, allowed environments).
- **Error hierarchy:** `RESCSError` base + configuration/invalid-request/unauthorized/forbidden/not-found/conflict/unprocessable/storage/dependency-unavailable, each with stable codes.
- **Domain + schema layer:** record/file-object dataclasses, Pydantic schemas (extra fields forbidden), JSON-serializability validation.
- **Repository layer:** runtime-checkable Protocols; in-memory (thread-safe) and SQLAlchemy backends with CRUD/list/pagination and conflict/not-found translation.
- **Database layer:** engine builder (SQLite dev / PostgreSQL prod), `SchemaManager` (idempotent schema setup), transactional session scope mapping integrity/connectivity errors, `bootstrap_database()`.

## 5. Known gaps (PLANNED)

- **Record & file HTTP endpoints** — CRUD exists at repository level only; `api/routers/` is empty.
- **Authentication enforcement** — `RESCS_API_KEY` validates at config load, but no middleware/dependency enforces the `X-API-Key` header. `X-Request-ID` is configured but unused.
- **Database bootstrap on startup** — `bootstrap_database()` is not yet called by `create_app()`.
- **Service layer** (`services/`) and **object storage** (`storage/`) — empty.
- **Integration tests** (`tests/integration/`) — empty.
- **C.O.R.E. integration contract** — referenced as `docs/core-integration-contract.md` but not yet present; the contract in this repository ([integration-contracts.md](../interfaces/integration-contracts.md)) is the working specification.

## 6. Roadmap (as documented in R.E.S.C.S. itself)

R.E.S.C.S. keeps its own 13-phase roadmap in `RESCS/docs/architecture.md`. Phases 1–2 (foundation; data model + storage abstraction) are marked complete; phases 3–13 are pending. C.O.R.E. adapter integration corresponds to C.O.R.E. v0.2 Phase 9 ([core.md](core.md#phase-9--rescs-adapter)).

The cross-system view lives in [Development Roadmap](../development/roadmap.md).

## Related

- [Data Flow](../architecture/data-flow.md)
- [Integration Contracts](../interfaces/integration-contracts.md)
- [Trust Boundaries](../security/trust-boundaries.md)
- ADR [0001](../decisions/0001-rescs-independent-from-core.md), [0005](../decisions/0005-storage-integration-via-adapter.md)