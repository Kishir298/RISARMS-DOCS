# C.O.R.E. — Communication, Organization and Resource Engine

> [!NOTE] **Status:** v0.3.0 **IMPLEMENTED** (all intended software components exist and are covered by automated tests). Physical Windows ↔ Mac LAN validation and extended 24/7 operational validation are **NOT YET PERFORMED** — they are deployment-validation tasks, not missing software. Compatibility with 0.2.x clients is preserved by design.

## 1. What C.O.R.E. is

C.O.R.E. is the **central management and control engine** of R.I.S.A.R.M.S. It is the operational hub of the ecosystem.

**It is NOT the primary AI.** Intelligence belongs to A.S.I.S. and T.I.V.I.S.S. C.O.R.E. provides the substrate they operate on.

**It runs on the control laptop** (Windows 11 host, which may co-host R.E.S.C.S.) and serves connected R.I.S.A.R.M.S. devices (Macs, phones, tablets, watches).

### Responsibilities

- Communication (transport abstraction, local + external TCP with TLS)
- Message protocols (handshake, device registration/discovery/error)
- Routing (including device-to-device routing through C.O.R.E.)
- Device registry (identity, presence, reconnection, persistence)
- Resource management and Organization engine
- Services (9 services in v0.3.0) and agent scheduling
- Data distribution between devices and R.E.S.C.S.
- Runtime / lifecycle management and runtime history
- Events, dependencies, configuration, health monitoring (14 checks), logging
- Security infrastructure (pluggable auth providers, TLS-external transport)
- Integration with other R.I.S.A.R.M.S. systems (R.E.S.C.S. adapters)

### Non-responsibilities

- Natural-language understanding (→ [A.S.I.S.](asis.md))
- Cloud/persistent storage authority (→ [R.E.S.C.S.](rescs.md)) — C.O.R.E. persists *through* R.E.S.C.S., it does not own a second database
- Security *sensing*/anomaly detection (→ [RadarS.A.R.D.](radar-sard.md))
- AI-agent identity/ownership (→ [T.I.V.I.S.S.](tiviss.md))
- Autonomous coding (→ [A.S.C.S.](asc.md))

## 2. Filesystem and project

- Locations: `RISARMS/CORE-HOST/` (server/runtime, package `core`) + `RISARMS/CORE-CLIENT/` (stdlib-only external-device client, package `client`, Option A login). Former single `RISARMS/CORE/` references mean this HOST+CLIENT split.
- Own git repositories (`CORE-HOST` + `CORE-CLIENT`, branch `main`)
- Language: Python (>= 3.10), package name `core`
- Runtime requirements: `PyYAML` only; no web framework
- CLI entry point: `python -m core` → `core.cli.main.main()`
- Application entry point: `core.application.app.CoreApplication`
- **Version markers agree at `0.3.0`**: `pyproject.toml`, `core/version.py` (`__version__`/`CORE_VERSION`), and `config/core.yaml`

## 3. Version history — the operating distinction

| Version | Role | Status |
|---|---|---|
| **v0.1** | Established the architectural foundation and behavioral contracts (subsystem layout, interfaces, models, tests) | Superseded, still compatible |
| **v0.2** | Made the architecture operational: TCP transport, routing-to-service execution, runtime orchestration, events/health integration, configuration-driven runtime, security integration, R.E.S.C.S. adapter groundwork, real CLI | **IMPLEMENTED** (`0.2.0` → `0.2.1`); clients remain supported via protocol negotiation |
| **v0.3** | External-device platform: TLS transport, token authentication, device registration/persistence, device discovery and device-to-device routing, capability-driven agent scheduling, HTTP R.E.S.C.S. adapter, data distribution, provisioning CLI/client | **IMPLEMENTED** (`0.3.0`); physical LAN validation pending |

v0.3.0 is not "v0.2 finished": it adds an external-device platform on top of the v0.2 operational core. Version negotiation (`core/version.py`) keeps `0.2.0`/`0.2.1` clients working; deprecated APIs are scheduled for removal only in a future breaking version.

## 4. Subsystem structure (v0.3.0)

```text
core/
├── application/   CoreApplication orchestration
├── cli/           argparse CLI + foreground control loop
├── communication/ Transport abstraction, LocalTransport, TcpTransport (TLS),
│                  serializer, protocol, device registry
├── configuration/ Configuration, loader, validator, manager, models
├── data/          DataOrganizer, R.E.S.C.S. reader, normalization, requests
├── dependencies/  DependencyManager (cycle detection, start order)
├── errors/        CoreError hierarchy
├── events/        Event model, EventBus, event types
├── health/        HealthStatus, HealthResult, HealthMonitor (14 checks)
├── logging/       CoreLogger
├── organization/  OrganizationEngine, ResourceIngestor (R.E.S.C.S. ingestion)
├── rescs/         RescsAdapter abstraction
├── resources/     Resource model, ResourceRegistry
├── routing/       Router
├── runtime/       Runtime, state machine, RuntimeHistory
├── scheduler/     AgentScheduler, agent profiles, assignments
├── security/      SecurityManager, SecurityPolicy, auth providers
└── services/      ServiceManager, ServiceDispatcher
```
Host layout: `CORE-HOST/core/` (above) + `CORE-HOST/config/` (`core.yaml` dev, `core.lan.example.yaml` LAN deployment).
Client lives separately: `CORE-CLIENT/client/core_device_client.py` — minimal stdlib external-device client with Option A login semantics (never imports `core`).
```

### 4.1 Purpose of each subsystem (highlights beyond the v0.1 foundation)

| Subsystem | Purpose |
|---|---|
| `communication` | `Transport` → `LocalTransport` (in-process) and `TcpTransport` (external devices). Framing, connection limits (10 MiB frames, 64 connections, 300 s idle), protocol negotiation, session/TLS fail-closed handshake, persistent connections, `DeviceRegistry` with distinct `device_id` / `identity_id` / `connection_id` |
| `rescs` | `RescsAdapter` implementations: `InMemoryRescsAdapter`, `FileRescsAdapter` (`var/rescs.json`), `HttpRescsAdapter` (endpoint/timeout/fallback) |
| `organization` | `OrganizationEngine` + `ResourceIngestor`: the controlled R.E.S.C.S. → C.O.R.E. ingestion boundary (strict validation, normalization, idempotent upserts, bulk ingest, authoritative `reconcile()` with backend-failure safety) |
| `scheduler` | Capability-driven agent assignment (local execution or Windows-host offloading). Default profiles: `asis-local`, `asis-offload`, `tiviss-compat`. Auto-assign on `DEVICE_CONNECTED` is opt-in; explicit `agent.assign` remains supported |
| `data` | `DataOrganizer`: owner-scoped R.E.S.C.S. retrieval → normalization → deterministic ordering (`updated_at DESC, id ASC`) → pagination (limit 1–500, max 500 items, 5 MiB metadata budget, 1 MiB inline-file limit, SHA-256 verification) → `DATA_RESPONSE` distribution over device routing |
| `security` | Pluggable providers: existence-based (internal/legacy) and token-based (required for external devices). Identity spoofing (`identity_id != connection.identity_id`) is rejected |
| `runtime` | Component lifecycle plus `RuntimeHistory` (device/agent/service lifecycle intervals, persisted through the R.E.S.C.S. adapter boundary) |
| `client` | `client/core_device_client.py` — minimal stdlib external-device client with Option A login semantics |

### 4.2 The implemented end-to-end flows

The following flows are **IMPLEMENTED and covered by tests**:

Internal message path (unchanged since v0.1/v0.2):

```mermaid
flowchart LR
    A["Message"] --> B["Router"]
    B --> C["Service endpoint"]
    C --> D["ServiceDispatcher"]
    D --> E["ServiceRequest"]
    E --> F["ServiceManager.execute"]
    F --> G["Operation handler"]
    G --> H["ServiceResponse"]
    H --> I["Response Message"]
```

External device path (new in v0.3.0):

```text
CONNECTED → TLS_ESTABLISHED → AUTHENTICATING → AUTHENTICATED
          → registration → presence → discovery → routing → delivery
          → disconnect → offline → reconnect → online (new connection_id)
```

External TCP requires TLS 1.2+, token authentication, validated protocol version and validated message identity. Plaintext downgrade is not permitted when externally exposed; binding externally without valid TLS fails closed. Local `127.0.0.1` operation keeps the legacy plaintext behavior for development and 0.2.x compatibility.

### 4.3 Current validation boundary (explicit)

These are deployment-validation items, not missing software:

- **Physical Windows ↔ Mac LAN validation has not been performed.** All external-transport behavior is covered by automated localhost tests (TLS, handshake, framing, identity, persistence, timeouts).
- **Extended 24/7 physical-host validation has not been performed** (Task Scheduler autostart and NSSM service configuration are documented but not endurance-validated).
- The development configuration (`transport: local`, `network.enabled: false`, `security.enforce_authorization: false`) is intentionally *not* the deployment configuration; see `config/core.lan.example.yaml` and CORE's own `docs/lan-readiness.md`.

## 5. Test coverage

- **50 test files approx; README-documented result: 689 passed (2026-09-18)** (verify with `pytest -q` against the current checkout).
- Coverage includes application orchestration, communication/TLS/framing, protocol negotiation, authentication, device registration/persistence/reconnect, discovery, presence, routing, services, resources, organization/reconciliation, R.E.S.C.S. adapters, scheduler, data distribution, health, events, integration behavior, and 0.2.x legacy compatibility.

## 6. Roadmap

### 6.1 v0.2 phase outcomes

The 13-phase v0.2 build order was completed; the phase definitions (objectives, completion criteria) remain in git history and previously defined the contracts v0.3 builds on. Final state:

| Phase | Focus | Outcome |
|---|---|---|
| 1 | Runtime + application orchestration | **IMPLEMENTED** |
| 2 | Communication + transport abstraction | **IMPLEMENTED** |
| 3 | Routing + service execution | **IMPLEMENTED** |
| 4 | Resource + organization integration | **IMPLEMENTED** |
| 5 | Event-driven integration | **IMPLEMENTED** |
| 6 | Health integration | **IMPLEMENTED** |
| 7 | Configuration drives runtime | **IMPLEMENTED** |
| 8 | Security integration | **IMPLEMENTED** (token auth for external devices; development config still ships with `enforce_authorization: false`) |
| 9 | R.E.S.C.S. adapter | **IMPLEMENTED** (`InMemory`/`File`/`Http` adapters) |
| 10 | External-device transport | **IMPLEMENTED** (TCP + TLS + protocol) |
| 11 | Real CLI lifecycle | **IMPLEMENTED** (foreground control loop; `execute_application` path) |
| 12 | Full integration test spine | **IMPLEMENTED** (localhost spine; physical LAN validation remains) |
| 13 | v0.2 cleanup/documentation/release | **IMPLEMENTED** (`0.2.0` → `0.2.1` release) |

### 6.2 v0.3.0 capability summary

| Capability | Status |
|---|---|
| TLS external transport (plaintext legacy fallback on localhost only) | IMPLEMENTED |
| Token-based authentication for external devices | IMPLEMENTED |
| Device registration, persistence (via R.E.S.C.S.), reconnect | IMPLEMENTED |
| Device discovery + presence | IMPLEMENTED |
| Device-to-device routing through C.O.R.E. | IMPLEMENTED |
| Capability-driven agent scheduling (+ auto-assign, opt-in) | IMPLEMENTED |
| `HttpRescsAdapter` with fallback + health | IMPLEMENTED |
| Data distribution (owner-scoped retrieval → pagination → routing) | IMPLEMENTED |
| Organization ingestion/reconciliation boundary | IMPLEMENTED |
| Provisioning API + CLI (`provision-device`) and external client | IMPLEMENTED |
| Windows autostart (Task Scheduler / NSSM docs) | IMPLEMENTED (endurance not validated) |
| Physical LAN validation | **NOT YET PERFORMED** |
| 24/7 operational validation | **NOT YET PERFORMED** |

## 7. Related documentation

- [System Boundaries](../architecture/system-boundaries.md) — C.O.R.E.'s responsibility ownership
- [Communication Flow](../architecture/communication-flow.md) — the message path
- [Lifecycle](../architecture/lifecycle.md) — C.O.R.E. runtime semantics
- [Integration Contracts](../interfaces/integration-contracts.md) — the live C.O.R.E. ↔ R.E.S.C.S. contract
- [Interface Contracts](../interfaces/communication.md) — messaging/routing/service contracts
- [Security Overview](../security/overview.md) — what is enforced vs config-gated
- [Development Roadmap](../development/roadmap.md) — the consolidated, cross-system roadmap
- ADR: [0003](../decisions/0003-core-is-integration-layer.md), [0004](../decisions/0004-communication-abstraction.md)
