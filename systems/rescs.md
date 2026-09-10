# R.E.S.C.S. — Rishik's Efficient System for Cloud Storage

> [!NOTE] **Status:** v0.3.0 **IMPLEMENTED** (FastAPI storage service: versioned HTTP API, enforced API-key authentication, record/file storage, streaming + resumable uploads, lifecycle/governance, backup tooling). Live PostgreSQL/Supabase deployment, real S3 backend, deployed C.O.R.E. ↔ R.E.S.C.S. interop, and 24/7 endurance are **Ready for External Validation** — documented and implemented, but not yet validated against live production infrastructure. R.E.S.C.S. is an **independent project**.

## 1. What R.E.S.C.S. is

R.E.S.C.S. is the **cloud/data storage system** of R.I.S.A.R.M.S. It provides storage that the rest of the ecosystem uses. R.E.S.C.S. is **not** the ecosystem controller: C.O.R.E. coordinates the ecosystem; R.E.S.C.S. provides storage.

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

> [!IMPORTANT] R.E.S.C.S. is an independent project. It must **never** be placed inside CORE. C.O.R.E. communicates with R.E.S.C.S. through defined interfaces and protocols — the adapter boundary plus the machine-readable contract both sides now ship. Rationale: ADR [0001](../decisions/0001-rescs-independent-from-core.md), ADR [0005](../decisions/0005-storage-integration-via-adapter.md).

- Location: `RISARMS/RESCS/` (sibling of `CORE/`, `ASIS/`, `ASCS/`, `RISARMS-DOCS/`)
- Own git repository (origin `https://github.com/Kishir298/RESCS`, branch `main`)
- Stack: Python ≥ 3.11, FastAPI + uvicorn, SQLAlchemy 2.0, psycopg 3 (PostgreSQL), Pydantic v2 + pydantic-settings
- Version: **`0.3.0`** (pyproject, package and CHANGELOG agree; 29 commits of phase-based development)

## 3. Project layout

```text
src/rescs/
├── main.py            # application factory + lifespan wiring
├── config.py          # pydantic-settings (RESCS_* env prefix)
├── security.py        # X-API-Key auth + owner scoping (ENFORCED)
├── observability.py   # request-ID middleware + access logging
├── contract.py        # machine-readable C.O.R.E. contract
├── health.py          # named dependency checks + aggregate report
├── domain.py          # storage-agnostic domain dataclasses
├── etag.py            # deterministic content identifiers
├── errors.py          # domain error hierarchy (stable codes + HTTP status)
├── rate_limit.py      # in-memory, single-instance rate limiting
├── db/                # engine, sessions, schema manager, bootstrap
├── models/            # SQLAlchemy ORM (records, file_objects, upload_sessions, audit)
├── schemas/           # Pydantic request/response schemas
├── interfaces/        # repository + object-store protocols
├── repositories/      # memory + SQLAlchemy backends
├── services/          # record/file/upload/audit/expiry services, composition root
├── storage/           # local, memory, s3 (+ fake) object stores
└── api/               # versioned HTTP API (v1): files, records, uploads,
                       # contract, health, admin routers
```

## 4. Current implementation (verified)

**IMPLEMENTED and tested:**

- **Versioned HTTP API (`/api/v1`)** — records, files, uploads, contract, health and admin routers; OpenAPI docs at `/docs`.
- **Enforced authentication** — `X-API-Key` is required on protected routes (`require_api_key` dependency, `hmac.compare_digest`), returning the authenticated principal; optional single-owner lock mode (`RESCS_API_KEY_OWNER`); owner scoping enforced on records and files.
- **Core storage** — record/file CRUD with etag-based optimistic concurrency, tags (up to 50/resource), advanced list/search filters, pagination.
- **Lifecycle & governance** — recoverable deletion (`DELETE` → `POST .../restore` → `DELETE .../purge`), `expires_at`/`ttl_seconds` TTL with admin cleanup, per-owner quotas and size caps (race-guarded), bulk operations (owner-isolated, documented partial success), secret-free audit trail (`/api/v1/admin/audit`).
- **Large payloads** — streaming uploads/downloads above `RESCS_STREAMING_THRESHOLD_BYTES` with bounded memory and integrity hashing; resumable uploads (`/api/v1/uploads`) with sessions, chunks, finalize and cleanup.
- **Storage abstraction** — local directory (default), in-memory, and S3-compatible backend (+ fake for tests); delegated encryption model documented in `docs/encryption.md`.
- **Operability** — live/ready health endpoints with named dependency checks, request-ID correlation middleware (`X-Request-ID`), optional in-memory rate limiting, backup tooling (`scripts/rescs_backup.py` with verify mode).
- **Machine-readable C.O.R.E. contract** — `rescs/contract.py` + `GET /api/v1/contract`, documented in `docs/core-integration-contract.md`: envelope, error-code → C.O.R.E. reaction table, reserved namespaces (`RUNNABLES`, `Ops`, `IDEAS`), transport and auth rules. C.O.R.E. ships a consuming integration-test fixture against this contract.

## 5. Known gaps (Ready for External Validation)

These are implemented but **not yet validated against live external infrastructure**:

- **Live PostgreSQL/Supabase deployment** — SQLite is the dev/test default; the PostgreSQL path is implemented and compatibility-tested, but no production database is deployed.
- **Real S3 backend** — implemented behind the object-store abstraction; not exercised against a real S3 provider.
- **Deployed C.O.R.E. ↔ R.E.S.C.S. interop** — both sides implement the contract, but traffic has not been exercised across a deployed pair.
- **24/7 endurance** — not performed.

## 6. Roadmap (as documented in R.E.S.C.S. itself)

R.E.S.C.S. documents its own evolution in `RESCS/docs/architecture.md` and `CHANGELOG.md`: the 13-phase plan completed through v0.2.0, followed by v0.3.0 reliability/governance hardening. The v0.3 status (see header) tracks external validation as the remaining work. The consuming side of the contract is C.O.R.E.'s `HttpRescsAdapter` ([core.md](core.md)).

The cross-system view lives in [Development Roadmap](../development/roadmap.md).

## Related

- [Data Flow](../architecture/data-flow.md)
- [Integration Contracts](../interfaces/integration-contracts.md) — now reflecting the implemented contract
- [Trust Boundaries](../security/trust-boundaries.md)
- ADR [0001](../decisions/0001-rescs-independent-from-core.md), [0005](../decisions/0005-storage-integration-via-adapter.md)
