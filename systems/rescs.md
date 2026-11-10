# R.E.S.C.S. — Rishik's Efficient System for Cloud Storage

> [!NOTE] **Status:** v0.4.0 **IMPLEMENTED** (FastAPI storage service: versioned HTTP API, enforced API-key authentication, record/file storage, streaming + resumable uploads, lifecycle/governance, backup tooling, and the Raspberry Pi storage foundation). Verified: 312 passed / 4 skipped (macOS Python 3.12). Live PostgreSQL/Supabase deployment, real S3 backend, deployed C.O.R.E. ↔ R.E.S.C.S. interop, real Pi/ARM64, and 24/7 endurance are **Ready for External Validation** — documented and implemented, but not validated against live production infrastructure. R.E.S.C.S. is an **independent project**.

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

- Location: `RISARMS/RESCS/` (sibling of `CORE/`, `ASIS/`, `ASCS/`, `TIVISS/`, `RISARMS-DOCS/`); also mirrored at `CORE/services/RESCS/` for the combined release
- Own git repository (origin `https://github.com/Kishir298/RESCS`, branch `main`)
- Stack: Python ≥ 3.11, FastAPI + uvicorn, SQLAlchemy 2.0, psycopg 3 (PostgreSQL), Pydantic v2 + pydantic-settings
- Version: **`0.4.0`** (pyproject, package and CHANGELOG agree)

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
- **Storage domains (logical ownership)** — reserved namespace prefixes `asis.*` (A.S.I.S.), `tiviss.*` (T.I.V.I.S.S.), `personal.*` (general user cloud data), alongside `core.*`/`rescs.*`. Reservation is advisory by convention; agents enforce their own prefix client-side. Documented in `RESCS/docs/storage-domains.md`; no schema changes, no separate databases.

## 4b. Device-Scoped Access Validation

RESCS enforces device-scoped access at the API level via `rescs/security.py`. When
C.O.R.E. (via `RescsDeviceProxy`) or another client sends `X-Device-Id`,
namespaces and owners are automatically scoped to that device:

### Namespace Enforcement

- **Reserved prefixes** — `core.`, `rescs.`, `asis.`, `tiviss.` cannot be accessed by devices
- **Device-scoped format** — `personal.device.{device_id}.{namespace}`
- **Automatic prefixing** — Unprefixed namespaces are automatically prefixed with `personal.device.{device_id}.`
- **Cross-device protection** — Devices cannot access other devices' namespaces

```python
# rescs/security.py
validate_device_namespace(namespace, device_id, operation) -> str
# Returns device-scoped namespace, raises UnauthorizedError on violation
```

### Owner Enforcement

- **Device-scoped format** — `personal.device.{device_id}.{owner}`
- **Cross-device protection** — Devices cannot use other devices' owner scopes
- **Automatic prefixing** — Unprefixed owners are automatically prefixed

```python
validate_device_owner(owner, device_id, operation) -> str | None
```

### Ownership Assertion

```python
assert_device_ownership(
    resource_owner=...,
    resource_namespace=...,
    device_id=...,
    operation=...
)
# Verifies both owner and namespace belong to the requesting device
```

### Integration with C.O.R.E.

`RescsDeviceProxy` in C.O.R.E. (`core/services/rescs_proxy.py`) automatically rewrites namespaces and owners before forwarding to RESCS, providing defense-in-depth: namespaces are rewritten at the gateway **and** validated at the API.

---

## 4c. Raspberry Pi storage foundation (v0.4.0)

The 0.4.0 release adds the Pi deployment path:

- **Signed CORE owner scope** — CORE sends `X-RESCS-Owner`, `X-RESCS-Expires`, and `X-RESCS-Signature`; RESCS verifies the signature and owner scope before serving records/files.
- **Required mount guard** — `RESCS_REQUIRED_MOUNT=/srv/core`; startup and every HTTP request reject a missing/invalid mount instead of silently writing to the microSD card.
- **Pi installer and systemd unit** — `deploy/pi/install.sh` and `deploy/pi/rescs.service` create the unprivileged `rescs` account/environment and bind the service to `srv-core.mount`.
- **Loopback validation** — `scripts/validate_core_loopback.py` exercises the real CORE storage adapter against a real RESCS uvicorn server (record save/list, upload/download, cross-owner rejection, soft-delete). It passed on macOS Python 3.12; no physical Pi/ARM64 run has been performed.

The 0.4.0 line is based on the published 0.3.0 code plus the Pi storage scope and signed owner scope. Device-scoped namespace/owner validation is present. The local 0.3.1 line (owner-scoped record uniqueness/idempotency, monitoring exports, `python -m rescs`, RES-1..8 tests) is archived at `old-versions/RESCS-0.3.1` and is **not** part of 0.4.0. Existing schema 0.3.0 is unchanged; namespace/key uniqueness is unchanged, so CORE must keep distinct service namespaces.

---

## 5. Known gaps (Ready for External Validation)

These are implemented but **not yet validated against live external infrastructure**:

- **Live PostgreSQL/Supabase deployment** — SQLite is the dev/test default; the PostgreSQL path is implemented and compatibility-tested, but no production database is deployed.
- **Real S3 backend** — implemented behind the object-store abstraction; not exercised against a real S3 provider.
- **Deployed C.O.R.E. ↔ R.E.S.C.S. interop** — both sides implement the contract, and the real loopback adapter test passes, but traffic has not been exercised across a deployed pair.
- **Real Raspberry Pi / ARM64** — cgroup v2, systemd boot, SSD mount/removal, disk-full recovery, and the Pi installer have not been run on physical hardware.
- **24/7 endurance** — not performed.
- **Local 0.3.1 features** — owner-scoped record uniqueness/idempotency, monitoring exports, `python -m rescs`, and RES-1..8 tests are not in 0.4.0; they remain in the separate archive.

## 6. Roadmap (as documented in R.E.S.C.S. itself)

R.E.S.C.S. documents its own evolution in `RESCS/docs/architecture.md` and `CHANGELOG.md`: the 13-phase plan completed through v0.2.0, followed by v0.3.0 reliability/governance hardening and v0.4.0 Pi storage scope/mount foundation. The v0.4.0 status (see header) tracks external validation as the remaining work. The consuming side of the contract is C.O.R.E.'s `HttpRescsAdapter` ([core.md](core.md)).

The cross-system view lives in [Development Roadmap](../development/roadmap.md).

## Related

- [Data Flow](../architecture/data-flow.md)
- [Integration Contracts](../interfaces/integration-contracts.md) — now reflecting the implemented contract
- [Trust Boundaries](../security/trust-boundaries.md)
- ADR [0001](../decisions/0001-rescs-independent-from-core.md), [0005](../decisions/0005-storage-integration-via-adapter.md)
