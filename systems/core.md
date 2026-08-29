# C.O.R.E. — Communication, Organization and Resource Engine

> [!NOTE] **Status:** v0.1 foundation **IMPLEMENTED** · C.O.R.E. v0.2 **IN DEVELOPMENT**

## 1. What C.O.R.E. is

C.O.R.E. is the **central management and control engine** of R.I.S.A.R.M.S. It is the operational hub of the ecosystem.

**It is NOT the primary AI.** Intelligence belongs to A.S.I.S. and T.I.V.I.S.S. C.O.R.E. provides the substrate they operate on.

**It runs on the control laptop.**

### Responsibilities

- Communication
- Message protocols
- Routing
- Organization
- Resource management
- Services
- Runtime / lifecycle management
- Events
- Dependencies
- Configuration
- Health monitoring
- Logging
- Security infrastructure
- Integration with other R.I.S.A.R.M.S. systems

### Non-responsibilities

- Natural-language understanding (→ [A.S.I.S.](../systems/asis.md))
- Cloud/persistent storage (→ [R.E.S.C.S.](../systems/rescs.md))
- Security *sensing*/anomaly detection (→ [RadarS.A.R.D.](../systems/radar-sard.md))
- AI-agent identity/ownership (→ [T.I.V.I.S.S.](../systems/tiviss.md))

## 2. Filesystem and project

- Location: `RISARMS/CORE/` (a sibling of `RESCS/`, `ASIS/`, `DOCS/`)
- Language: Python (>= 3.10), package name `core`
- Runtime requirements: `PyYAML`, `pytest` only — no web framework
- CLI entry point: `python -m core` → `core.cli.main.main()`
- Application entry point: `core.application.app.CoreApplication`
- Version markers: `pyproject.toml` = `0.1.0`; `config/core.yaml` and CLI banner = `0.2.0`

## 3. v0.1 vs v0.2 — the operating distinction

> **v0.1 established the architecture and behavioral contracts.**

> **v0.2 is intended to make that architecture genuinely operational.**

v0.1 is deliberately a foundation: the subsystem layout, interfaces, models and tests exist and are meaningful, but several deeper integrations (network communication, real authentication, live resource/organization initialization, full CLI lifecycle) were intentionally deferred. v0.2 is the program of work that turns this skeleton into a running, integrated engine. The complete v0.2 build order is in [Section 6](#6-core-v02-roadmap).

## 4. Subsystem structure (v0.1)

The implemented structure:

```text
core/
├── application/   CoreApplication orchestration
├── cli/           argparse CLI
├── communication/ Message models, serializer, transport abstraction
├── configuration/ Configuration, loader, validator, manager
├── dependencies/  DependencyManager (cycle detection, start order)
├── errors/        CoreError hierarchy
├── events/        Event model, EventBus, event types
├── health/        HealthStatus, HealthResult, HealthMonitor
├── logging/       CoreLogger (stdout wrapper)
├── organization/  OrganizationEngine, OrganizationEntry
├── resources/     Resource model, ResourceRegistry
├── routing/       Router (message-type → destination)
├── runtime/       Runtime, state machine, lifecycle orchestration
├── security/      Identity, IdentityType, Permission, SecurityManager
└── services/      Service model, ServiceManager, ServiceDispatcher
```

### 4.1 Purpose of each subsystem

| Subsystem | Purpose |
|---|---|
| `application` | `CoreApplication` — builds the component graph (12 runtime components, 6 internal services), wires operation handlers and health checks, exposes `start` / `stop` / `restart` / `health_check` |
| `cli` | Command-line front-end. Subcommands: `status`, `start`, `stop`, `services`, `resources`, `connections`, `health`. Terminal banner prints `C.O.R.E. v0.2` |
| `communication` | The messaging layer: `Message` dataclass, JSON `MessageSerializer`, `Transport` abstraction, concrete in-process `LocalTransport` (thread-safe, endpoint registry, `send`/`request`, counters), and `LocalCommunication` alias for v0.1 compatibility |
| `configuration` | Hierarchical `Configuration` (dot-path get/set/require, env-var loading with `CORE_` prefix, deep merge), `ConfigurationLoader` (YAML), `ConfigurationValidator` (requires `core.name`, `core.version`, `environment`), operational `ConfigurationManager` |
| `dependencies` | `DependencyManager` — validates dependency graphs and computes start order |
| `errors` | Central exception hierarchy rooted at `CoreError` (~15 subclasses: configuration, service, resource, communication/message/routing, health, dependency/circular, initialization, shutdown) |
| `events` | `Event` model and thread-safe `EventBus` (subscribe/unsubscribe/publish/emit, isolated handler failures, metrics); ~20 event-type constants |
| `health` | `HealthStatus` (unknown/healthy/degraded/unhealthy), `HealthResult`, aggregating `HealthMonitor` with per-component counters and `on_change` callbacks |
| `logging` | `CoreLogger` — thin wrapper over stdlib logging writing to stdout |
| `organization` | `OrganizationEngine` — categorizes resources and entries (by category/resource), linked to the resource registry |
| `resources` | `Resource` model and `ResourceRegistry` — register/unregister/update/mark-seen/list/discover, auto-categorized into the organization engine |
| `routing` | `Router` — routes messages by message type to service endpoints, delegates delivery to a `Transport` |
| `runtime` | `Runtime` — dependency-aware component start order (DFS/topological sort), lifecycle states, reverse-order shutdown, failure rollback, restart |
| `security` | `Identity`, `IdentityType`, `Permission` enums, and `SecurityManager` — register/unregister identities, authenticate, authorize, permission checks, metrics, event emission |
| `services` | `Service`, `ServiceRequest`/`ServiceResponse`, `ServiceStatus`, `ServiceManager` (lifecycle, dependency-aware start/stop, execution of operation handlers), `ServiceDispatcher` (Message → ServiceRequest → operation → ServiceResponse → Message) |

### 4.2 The implemented end-to-end flow

The following flow is **IMPLEMENTED and covered by tests** (unit + integration):

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

### 4.3 Known v0.1 limitations (explicit)

These are boundaries, not bugs. They are deliberately deferred and are addressed by v0.2 phases:

- **Only an in-process transport exists.** `config/core.yaml` sets `network.enabled: false`. Delivery is local only (Phase 2 groundwork landed, network transport is Phase 10 territory).
- **Authentication is not implemented.** `SecurityManager.authenticate()` currently verifies identity existence only; credential verification is explicitly deferred to a dedicated authentication provider (Phase 8).
- **Resource/organization initialization is stubbed.** `CoreApplication._initialize_resources()` and `_initialize_organization()` are empty; they are wired in Phase 4.
- **Logging is a thin stdout wrapper.** No file handlers or structured output yet.
- **CLI `execute()` (Runtime-only compatibility path) is partially stubbed.** The application-aware `execute_application()` is the real path.

## 5. Test coverage

- **22 test files, 259 test functions** (as of the last documentation update).
- Tests mirror the subsystem layout under `tests/`.
- Includes end-to-end coverage of application orchestration, event-driven lifecycle, health integration, and the router→service flow.
- The full integration test spine is v0.2 Phase 12 — see below.

## 6. C.O.R.E. v0.2 Roadmap

The v0.2 build order. Phases are listed in strict order; later phases assume earlier ones. Work already landed in git history is marked **IN DEVELOPMENT**; code that does not exist yet is marked **PLANNED**.

> [!NOTE] **Status legend:** In this roadmap, a phase marked as having "landed work" means partial groundwork exists in the codebase (often recognizable in commit history and tests). A phase's *items* may still be open. Treat the `Expected behavior` and `Completion criteria` of each phase as the requirements, not the current state.

### Phase overview

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

---

### Phase 1 — Runtime + application orchestration

- **Objective:** Make the runtime genuinely orchestrate component lifecycle: dependency-aware startup, ordered shutdown, restart, failure rollback.
- **Why:** v0.1 declared the shapes; v0.2 must *run* them so that everything else has a reliable context to live in.
- **Components involved:** `core/runtime`, `core/application`, `core/dependencies`.
- **Inputs:** Component declarations and a dependency graph.
- **Outputs:** A started/stopped application instance whose subsystem state matches expectations at every step.
- **Dependencies:** None (foundation).
- **Expected behavior:** `start()` initializes components in dependency order and emits `SYSTEM_STARTED`; `stop()` shuts down in reverse order and emits `SYSTEM_STOPPED`; `restart()` returns to a healthy running state; component failures roll back cleanly.
- **Tests required:** unit tests for state transitions and ordering; integration test that start→work→stop transitions are correct and idempotent.
- **Completion criteria:** An application starts and stops predictably with no ordering violations; rollback leaves no partially-started components.
- **Must NOT implement yet:** Network transports, R.E.S.C.S. connectivity, authentication providers.
- **Current state:** Core runtime orchestration and lifecycle states are implemented and tested. Treat outstanding items as hardening.

### Phase 2 — Communication + transport abstraction

- **Objective:** Abstract *how* messages are delivered so callers depend on a `Transport` interface, not a concrete mechanism.
- **Why:** The ecosystem requires local, network and future transports; everything upstream (routing, services, adapters) must be transport-agnostic.
- **Components involved:** `core/communication` (`Transport`, `LocalTransport`, `Message`, serializer).
- **Inputs:** Message objects produced by callers.
- **Outputs:** Delivered messages/responses through whatever transport is active.
- **Dependencies:** Phase 1 (runtime context to host transports).
- **Expected behavior:** `send`/`request` work against the abstract `Transport`; the in-process `LocalTransport` remains the default; serialization is JSON.
- **Tests required:** Transport-interface conformance tests; LocalTransport send/request/counter tests; round-trip serialization tests.
- **Completion criteria:** No code above the transport layer references a concrete transport; adding a new transport requires implementing the interface only.
- **Must NOT implement yet:** Any *specific* network protocol.
- **Current state:** `Transport` abstraction, `LocalTransport`, `MessageSerializer` and `LocalCommunication` alias are implemented and tested. Network transport is intentionally out of scope (Phase 10).

### Phase 3 — Routing + service execution

- **Objective:** Connect the message path all the way to service operations: `Message → Router → endpoint → ServiceDispatcher → ServiceManager.execute → operation handler → response`.
- **Why:** This is the behavioral core of C.O.R.E. — requests in, responses out.
- **Components involved:** `core/routing`, `core/services`.
- **Inputs:** Messages addressed by type; registered services with operation handlers.
- **Outputs:** Executed operations and response messages; defined failure behavior for unknown routes/unavailable services.
- **Dependencies:** Phase 1 (runtime), Phase 2 (transport).
- **Expected behavior:** Routes exist per message type; the dispatcher converts messages to service requests and back; unknown routes and handler failures produce deterministic errors rather than silent drops.
- **Tests required:** Router-to-service integration tests; failure-path tests (unknown route, failing handler).
- **Completion criteria:** The full message→response flow works end to end within C.O.R.E.
- **Must NOT implement yet:** Cross-system routing, external protocols.
- **Current state:** The router→service flow is implemented and tested end to end.

### Phase 4 — Resource + organization integration

- **Objective:** Make the resource registry and organization engine operational: resources register, discover, categorize and are observable.
- **Why:** Resources are the assets C.O.R.E. manages; organization is how they are navigated.
- **Components involved:** `core/resources`, `core/organization`, `core/application`.
- **Inputs:** Resource declarations from components/services.
- **Outputs:** A live registry of tracked resources, organized/categorized, discoverable by callers.
- **Dependencies:** Phase 1, Phase 2.
- **Expected behavior:** `_initialize_resources()` and `_initialize_organization()` are real (not empty); registered resources appear in `services`/`resources` CLI/status output; categorization is consistent between registry and engine.
- **Tests required:** Registry lifecycle tests; categorization consistency tests; CLI visibility tests where applicable.
- **Completion criteria:** The empty stubs in `CoreApplication` are replaced by working initialization; resource discovery returns live data.
- **Must NOT implement yet:** R.E.S.C.S. object mapping (its resource model is separate), device enumeration.
- **Current state:** Registry/engine logic and their integration are implemented; the application-level initialization stubs are the known gap.

### Phase 5 — Event-driven integration

- **Objective:** Propagate lifecycle/state changes across subsystems through the event bus, so components react instead of being wired to each other.
- **Why:** Reduces coupling and makes the system observable.
- **Components involved:** `core/events`, all subsystems emitting/subscribing.
- **Inputs:** Event publications from components (start/stop, health change, security events, etc.).
- **Outputs:** Subscribers reacting correctly; no subscriber failure cascading to publishers.
- **Dependencies:** Phase 1 (lifecycle events).
- **Expected behavior:** Subsystems emit on key transitions; the bus isolates handler failures; ordering is deterministic where required.
- **Tests required:** cross-subsystem event integration tests; failure-isolation tests.
- **Completion criteria:** Lifecycle changes are observable via events end to end and handlers cannot destabilize publishers.
- **Must NOT implement yet:** Distributed/queue-based event delivery.
- **Current state:** Event-driven lifecycle and event emission across subsystems (including security-bus bridge) are implemented and tested.

### Phase 6 — Health integration

- **Objective:** Aggregate real per-subsystem health into an overall application state, with change callbacks and event emission.
- **Why:** The ecosystem must know when a piece of it is degraded, not just up/down.
- **Components involved:** `core/health`, all subsystems, `core/application`.
- **Inputs:** Registered health checks per component.
- **Outputs:** Aggregated `HealthStatus` with per-component provenance; state-change events.
- **Dependencies:** Phase 1, Phase 5 (change events).
- **Expected behavior:** A degraded or unhealthy component moves overall health accordingly; the change is observable (event + `health` CLI).
- **Tests required:** aggregation tests; transition/event tests.
- **Completion criteria:** Health reflects real subsystem state; transitions are observable.
- **Must NOT implement yet:** External health endpoints (R.E.S.C.S. exposes its own), alerting.
- **Current state:** Stateful health monitoring with event emission is implemented and tested.

### Phase 7 — Configuration drives runtime

- **Objective:** Runtime behavior (logging level, transport choice/network flag, service registration, timeouts) is driven by the loaded configuration, not hard-coded.
- **Why:** v0.1 configuration is a foundation; v0.2 must *consume* it.
- **Components involved:** `core/configuration`, `core/runtime`, `core/application`, `config/core.yaml`.
- **Inputs:** `config/core.yaml` + `CORE_*` environment overrides.
- **Outputs:** A runtime whose behavior matches configuration.
- **Dependencies:** Phase 1, Phase 2.
- **Expected behavior:** Changing configuration changes runtime behavior deterministically; validation fails fast on bad config.
- **Tests required:** configuration-driven behavior tests; validation tests.
- **Completion criteria:** No remaining hard-coded runtime decisions that configuration is supposed to control, per the config contract.
- **Must NOT implement yet:** Dynamic hot-reload of configuration.
- **Current state:** Configuration manager, loader, validator and environment merges are in place; consumption across the runtime is the remaining work.

### Phase 8 — Security integration

- **Objective:** Real authentication and authorization behind the existing security foundation: identities, permissions, and an actual authentication provider.
- **Why:** `SecurityManager.authenticate()` is explicitly deferred in v0.1; v0.2 makes identity verification real.
- **Components involved:** `core/security`, `core/application`, authentication provider.
- **Inputs:** Credentials/identities; permission requirements per operation.
- **Outputs:** Authenticated identities; authorized operations; permission failures rejected deterministically.
- **Dependencies:** Phase 1, Phase 5 (security event emission exists).
- **Expected behavior:** `authenticate()` verifies credentials via a provider; authorization gates service operations; failures produce defined errors/events.
- **Tests required:** authentication provider tests; authorization-gating tests; negative tests for unauthorized access.
- **Completion criteria:** No operation can be invoked by an unauthenticated/unpermitted actor; boundaries documented in [`../security/trust-boundaries.md`](../security/trust-boundaries.md).
- **Must NOT implement yet:** PKI, remote identity federation, per-subsystem internal auth between local C.O.R.E. components.
- **Current state:** Security foundation (identities, permissions, manager, event emission) exists; the authentication provider is the missing piece.

### Phase 9 — R.E.S.C.S. adapter

- **Objective:** A C.O.R.E. adapter that lets callers issue storage requests to R.E.S.C.S. through C.O.R.E.'s routing/communication/services, without C.O.R.E. knowing R.E.S.C.S. internals.
- **Why:** This is how the ecosystem gets persistence. R.E.S.C.S. stays independent; the adapter is the bridge.
- **Components involved:** `core/services` (adapter service), `core/communication` (outbound transport), R.E.S.C.S. API.
- **Inputs:** C.O.R.E. service requests for storage operations.
- **Outputs:** R.E.S.C.S. calls and responses routed back to the original requester.
- **Dependencies:** Phase 3 (service execution), Phase 10-adjacent transport to reach R.E.S.C.S., R.E.S.C.S. record/file API (see [R.E.S.C.S.](../systems/rescs.md)).
- **Expected behavior:** The request path from [Integration Architecture](../architecture/system-interactions.md#integration-path) works: requester → C.O.R.E. → router → communication → adapter → R.E.S.C.S. → response.
- **Tests required:** adapter unit tests (with R.E.S.C.S. via its API contract), integration test spine hookup.
- **Completion criteria:** C.O.R.E. can store and retrieve records/files through R.E.S.C.S. without internal coupling.
- **Must NOT implement yet:** Any R.E.S.C.S. code inside C.O.R.E., storage logic in C.O.R.E., or Ctrl-C the R.E.S.C.S. *ownership* of storage.
- **Current state:** **PLANNED.** No adapter code exists.

### Phase 10 — External-device transport

- **Objective:** A transport that reaches external devices, enabling the ecosystem to talk off-host (devices, sensors, future RadarS.A.R.D. integration).
- **Why:** The ecosystem's arrows point outward to devices; C.O.R.E. needs a delivery mechanism to them.
- **Components involved:** `core/communication` (new `Transport` implementation), device protocol definition.
- **Inputs:** Messages destined for off-host endpoints.
- **Outputs:** Delivery to / responses from external devices over a defined protocol.
- **Dependencies:** Phase 2 (transport abstraction), Phase 3 (routing).
- **Expected behavior:** The transport implements the `Transport` interface so nothing above it changes; failures surface as defined communication errors.
- **Tests required:** transport conformance tests; simulated-device integration tests.
- **Completion criteria:** A device can be a message peer of C.O.R.E. using the same routing/services that local peers use.
- **Must NOT implement yet:** Any *specific* third-party device protocols; physical sensor drivers (those belong to RadarS.A.R.D.).
- **Current state:** **PLANNED.**

### Phase 11 — Real CLI lifecycle

- **Objective:** The CLI fully drives the application lifecycle: `python -m core start` genuinely starts/stops the engine, and the runtime-only compatibility path is retired.
- **Why:** The operator interface currently has a partly stubbed fallback path (`execute()`); operators must see real state.
- **Components involved:** `core/cli`, `core/application`.
- **Inputs:** User commands.
- **Outputs:** Real engine behavior driven from the CLI; accurate status of services/resources/connections/health.
- **Dependencies:** Phases 1, 3, 4, 6.
- **Expected behavior:** All subcommands reflect live application state; the stubbed path prints no placeholders.
- **Tests required:** CLI unit tests + application-level CLI integration tests.
- **Completion criteria:** The CLI is a faithful, complete operator console for C.O.R.E.
- **Must NOT implement yet:** Remote administration, web UI.
- **Current state:** CLI is application-aware and prints `C.O.R.E. v0.2`; the runtime-only compatibility path remains partially stubbed.

### Phase 12 — Full integration test spine

- **Objective:** An integration test suite that runs the whole application through every phase's behaviors together, plus the store/retrieve path via the R.E.S.C.S. adapter.
- **Why:** Phases are individually testable, but the ecosystem's value is the *combination*.
- **Components involved:** `tests/integration`, application harness, adapter.
- **Inputs:** The assembled application + fake/bounded R.E.S.C.S.
- **Outputs:** A repeatable end-to-end verification.
- **Dependencies:** All prior phases.
- **Expected behavior:** Start → configure → send message → route → execute service → (optionally) persist via adapter → respond → health reflects activity → clean stop, all asserted in one spine.
- **Tests required:** the spine tests themselves.
- **Completion criteria:** `pytest` green with the full integration spine.
- **Must NOT implement yet:** Multi-host integration, real cloud dependencies in the test suite.
- **Current state:** **PLANNED** (individual integration tests exist; the full spine does not).

### Phase 13 — v0.2 cleanup/documentation/release

- **Objective:** Align version markers (0.1.0 → 0.2.0 everywhere), complete C.O.R.E. docs, write the v0.2 release summary.
- **Why:** The system must present a coherent versioned face to the rest of the ecosystem.
- **Components involved:** `pyproject.toml`, `config/core.yaml`, CLI, this documentation.
- **Inputs:** The finished v0.2 feature set.
- **Outputs:** A tagged, consistent, documented v0.2 release.
- **Dependencies:** All prior phases.
- **Expected behavior:** `pyproject.toml`, config and CLI agree on 0.2.0; changelog/release notes exist.
- **Tests required:** full suite green on the release candidate.
- **Completion criteria:** A consistent, documented v0.2.
- **Must NOT implement yet:** v0.3 features.
- **Current state:** **PLANNED.** Version markers are currently inconsistent (pyproject `0.1.0` vs config/CLI `0.2.0`) — that inconsistency is a Phase 13 item, not a bug to fix piecemeal.

## 7. Related documentation

- [System Boundaries](../architecture/system-boundaries.md) — C.O.R.E.'s responsibility ownership
- [Communication Flow](../architecture/communication-flow.md) — the message path
- [Lifecycle](../architecture/lifecycle.md) — C.O.R.E. runtime semantics
- [Integration Contracts](../interfaces/integration-contracts.md) — how C.O.R.E. bridges to R.E.S.C.S./A.S.I.S.
- [Interface Contracts](../interfaces/communication.md) — messaging/routing/service contracts
- [Security Overview](../security/overview.md) — C.O.R.E.'s security infrastructure role
- [Development Roadmap](../development/roadmap.md) — the consolidated, cross-system roadmap
- ADR: [0003](../decisions/0003-core-is-integration-layer.md), [0004](../decisions/0004-communication-abstraction.md)