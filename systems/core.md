# C.O.R.E. — Communication, Organization and Resource Engine

> [!NOTE] **Status:** v0.6.0 **IMPLEMENTED** (beta source; split since 2026-11-21 into the `CORE-HOST` + `CORE-CLIENT` repositories — see [systems/core-client.md](core-client.md) for the client and [systems/risarms-host.md](risarms-host.md) for the umbrella). Package version is 0.6.0; wire/protocol compatibility remains 0.4.0. The server release targets **Void Linux x86_64 glibc with runit** (the HP 14-dq1037wm is the **reference deployment machine**, not a hardware gate). An additive **Ubuntu Server 24.04 systemd candidate** exists in the RISARMS-HOST umbrella (`deployment/ubuntu/`): static checks only, **not boot-validated and not a release target** ([Ubuntu 24.04 candidate](../development/ubuntu-24.04.md)). Booted Void install, reboot, upgrade/rollback, storage failure, backup restore, physical HP, physical LAN validation (Void CORE host ↔ RISARMS-ui clients on macOS Intel, macOS Apple Silicon, Windows x86_64 and Linux x86_64), and extended 24/7 operational validation are **NOT YET PERFORMED** — deployment-validation tasks, not missing server software. Compatibility with older clients is preserved by design.

## 1. What C.O.R.E. is

C.O.R.E. is the **central management and control engine** of R.I.S.A.R.M.S. It is the operational hub of the ecosystem.

**It is NOT the primary AI.** Intelligence belongs to A.S.I.S. and T.I.V.I.S.S. C.O.R.E. provides the substrate they operate on.

**It runs on the control host** — Void Linux x86_64 glibc with runit (HP 14 as the reference deployment machine), co-hosting R.E.S.C.S. — and serves connected R.I.S.A.R.M.S. devices (Macs, phones, tablets, watches). Raspberry Pi/ARM64 and systemd server deployments are historical for this release. Windows, macOS and Linux x86_64 remain supported through the separate RISARMS-ui desktop client.

### Responsibilities

- Communication (transport abstraction, local + external TCP with TLS)
- Message protocols (handshake, device registration/discovery/error)
- Routing (including device-to-device routing through C.O.R.E.)
- Device registry (identity, presence, reconnection, persistence)
- Resource management and Organization engine
- Services (9 services) and agent scheduling
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

- Location: `RISARMS/CORE-HOST/` — the C.O.R.E. host/runtime repository (server, package `core`). The client lives in `RISARMS/CORE-CLIENT/` (stdlib-only external-device client, package `client`, Option A login); umbrella assets (`services/`, `deployment/`, `install/`, `validation/`) live in `RISARMS/RISARMS-HOST/`
- Git repositories: `CORE-HOST` (remote `Kishir298/CORE-HOST`) and `CORE-CLIENT` (remote `Kishir298/CORE-CLIENT`) — split from the former `CORE` monorepo on 2026-11-21; umbrella `RISARMS-HOST` (remote `Kishir298/RISARMS-HOST`)
- Language: Python (>= 3.10), package name `core`
- Runtime requirements: `PyYAML`; optional monitoring extra adds `prometheus-client` + `fastapi`
- CLI entry point: `core-host` (or `python -m core`); client entry point: `core-client`
- Application entry point: `core.application.app.CoreApplication`
- **Package version `0.6.0`** in `pyproject.toml`; `core/version.py` reports `0.6.0`, while the wire protocol intentionally remains `0.4.0` for compatibility

## 3. Version history — the operating distinction

| Version | Role | Status |
|---|---|---|
| **v0.1** | Established the architectural foundation and behavioral contracts (subsystem layout, interfaces, models, tests) | Superseded, still compatible |
| **v0.2** | Made the architecture operational: TCP transport, routing-to-service execution, runtime orchestration, events/health integration, configuration-driven runtime, security integration, R.E.S.C.S. adapter groundwork, real CLI | **IMPLEMENTED** (`0.2.0` → `0.2.1`); clients remain supported via protocol negotiation |
| **v0.3** | External-device platform: TLS transport, token authentication, device registration/persistence, device discovery and device-to-device routing, capability-driven agent scheduling, HTTP R.E.S.C.S. adapter, data distribution, provisioning CLI/client | **IMPLEMENTED** (`0.3.0`); physical LAN validation pending |
| **v0.4** | Localhost host/client portals; capability router/model profiles; device-scoped R.E.S.C.S. proxy | **IMPLEMENTED** (`0.4.0`) |
| **v0.5** | Combined host/client project; Pi service integration; signed R.E.S.C.S. owner scope; `/api/ai-status`; tool-free `CORE_SAFE_CHAT` worker | **IMPLEMENTED** (`0.5.0`, historical); physical Pi/ARM64 validation pending |
| **v0.6** | Void Linux x86_64 server release; per-profile service grants; session-bound registered owner devices; queued owner actions; versioned venvs; storage guard; runit/Caddy/nftables; backup/restore, upgrade/rollback, diagnostics | **IMPLEMENTED (beta source, `0.6.0`)**; HP 14 Void runtime validation pending |

v0.3.0 is not "v0.2 finished": it adds an external-device platform on top of the v0.2 operational core. Version negotiation (`core/version.py`) keeps older clients working; deprecated APIs are scheduled for removal only in a future breaking version.

## 4. Subsystem structure (v0.6.0)

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
├── monitoring/    Optional Prometheus exports
├── organization/  OrganizationEngine, ResourceIngestor (R.E.S.C.S. ingestion)
├── portal/        Localhost host portal
├── rescs/         RescsAdapter abstraction
├── resources/     Resource model, ResourceRegistry
├── routing/       Router
├── runtime/       Runtime, state machine, RuntimeHistory
├── scheduler/     AgentScheduler, agent profiles, assignments
├── security/      SecurityManager, SecurityPolicy, auth providers
├── services/      ServiceManager, ServiceDispatcher
└── web/           Owner portal gateway, RESCS storage adapter, safe-chat worker
```
Host layout: `CORE-HOST/core/` + `CORE-HOST/config/` (`core.yaml` dev, `core.lan.example.yaml` LAN deployment).
Client: `CORE-CLIENT/client/core_device_client.py` — minimal stdlib external-device client with Option A login semantics (never imports `core`).
Umbrella repository also carries `services/{ASIS,ASCS,RESCS,TIVISS}` (in `RISARMS-HOST/`), `deployment/void/` (the v0.6.0 installer/services; legacy Pi deployment assets retained historically), `install/` wheels, and `validation/` release evidence — see [systems/risarms-host.md](risarms-host.md).

### 4.1 Purpose of each subsystem (highlights beyond the v0.1 foundation)

| Subsystem | Purpose |
|---|---|
| `communication` | `Transport` → `LocalTransport` (in-process) and `TcpTransport` (external devices). Framing, connection limits (10 MiB frames, 64 connections, 300 s idle), protocol negotiation, session/TLS fail-closed handshake, persistent connections, `DeviceRegistry` with distinct `device_id` / `identity_id` / `connection_id` |
| `rescs` | `RescsAdapter` implementations: `InMemoryRescsAdapter`, `FileRescsAdapter` (`var/rescs.json`), `HttpRescsAdapter` (endpoint/timeout/fallback). **New in v0.3.1**: `RescsDeviceProxy` — device-scoped namespace enforcement. Rewrites namespaces to `personal.device.{device_id}.{namespace}` format, enforces reserved prefix protection (`core.`, `rescs.`, `asis.`, `tiviss.`), validates device ownership on owner field. RESCS API validates device ownership via `validate_device_namespace()`, `validate_device_owner()`, `assert_device_ownership()`. |
| `organization` | `OrganizationEngine` + `ResourceIngestor`: the controlled R.E.S.C.S. → C.O.R.E. ingestion boundary (strict validation, normalization, idempotent upserts, bulk ingest, authoritative `reconcile()` with backend-failure safety) |
| `scheduler` | Capability-driven agent assignment (local execution or Windows-host offloading). Default profiles: `asis-local`, `asis-offload`, `tiviss-compat`. Auto-assign on `DEVICE_CONNECTED` is opt-in; explicit `agent.assign` remains supported. **New in v0.3.1**: `CapabilityRouter` with `ModelProfile` — device-capability-based model selection (RAM/CPU/GPU-aware). Profiles: `asis-local-heavy` (qwen3-coder:30b, 24GB RAM, CUDA), `asis-local-medium` (qwen2.5-coder:14b, 12GB RAM), `asis-local-light` (qwen3:14b, 8GB RAM), `asis-offload-phone`/`asis-offload-watch` for low-capability devices. `CapabilityRouter.select_model_profile(device_caps)` scores profiles by RAM, CPU, GPU match. |
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

- **Physical LAN validation — Void CORE host ↔ RISARMS-ui clients on macOS Intel, macOS Apple Silicon, Windows x86_64 and Linux x86_64 — has NOT YET BEEN PERFORMED.** (Historical two-machine Windows-host ↔ Mac tests retain their original dates/context elsewhere and do not satisfy this matrix.) All external-transport behavior is covered by automated localhost tests (TLS, handshake, framing, identity, persistence, timeouts).
- **Launcher-owned `ollama serve` lifecycle: PERFORMED 2026-09-19** (tray quit → owned autostart → owned stop → tray restored; pre-existing servers untouched). See CORE-HOST's `docs/serve-autostart-manual-test.md`.
- **Extended 24/7 physical-host validation has not been performed** (Task Scheduler autostart and NSSM service configuration are documented but not endurance-validated).
- The development configuration (`transport: local`, `network.enabled: false`, `security.enforce_authorization: false`) is intentionally *not* the deployment configuration; see `config/core.lan.example.yaml` and CORE-HOST's own `docs/lan-readiness.md`.

## 5. Test coverage

- **CORE-HOST: 888 passed / 4 skipped on macOS Python 3.14 (2026-11-21, post-split).** CORE-CLIENT: **225 passed / 1 skipped** (2026-11-21; the skip is the `tkinter` GUI test, environment-dependent). Pre-split the combined suite reported 911 passed / 4 skipped — the 23 deployment/manifest asset tests moved with `deployment/` to `RISARMS-HOST/` (see [systems/risarms-host.md](risarms-host.md), 57 tests). Public-origin proxy checks ignore `X-Forwarded-Host`; partial control frames are covered across read timeouts.
- Coverage includes application orchestration, communication/TLS/framing, protocol negotiation, authentication, device registration/persistence/reconnect, discovery, presence, routing, services, resources, organization/reconciliation, R.E.S.C.S. adapters, scheduler, data distribution, health, events, integration behavior, Pi policy, and legacy compatibility.

## 5b. Web portals (v0.6.0)

Localhost-only presentation planes (no new authorities):

- **Host portal** (`CORE-HOST/core/portal/`, default `http://127.0.0.1:8765`, configurable via the `web:` config section): 16 sections — Overview, Devices, Network, Resources, Services, Agents, R.E.S.C.S., Health, Events, Routing, Data Distribution, Sessions, Security, Configuration, Logs, Diagnostics. Starts with the host (`core-host` prints the URL); CLI remains fully available.
- **Client portal** (`CORE-CLIENT/client/portal/`, default `http://127.0.0.1:8766`): 8 sections — Dashboard, Devices, R.E.S.C.S., Services, AI, Network, Session, Settings. Works offline (remote sections report `C.O.R.E. HOST OFFLINE`); starts with the client CLI unless `--no-portal`.
- **Capability detection** is deterministic (HIGH/MEDIUM/LOW/UNKNOWN from RAM + CPU cores; Qwen model profiles centralized in one policy module; no LLM involved).
- **AI offload** routes through the existing `AgentScheduler` (`agent` service `infer` operation): placement truthfully returned, never fabricated model output.
- **Security**: recursive response redaction (credentials, session tokens shown only as `ACTIVE`, TLS keys, RESCS/S3 secrets never leave the backend); localhost binding default; location is opt-in manual/device-reported with precision controls; Haversine distance only with both coordinates.
- Physical LAN validation is still NOT PERFORMED; portal behavior over LAN is covered by automated tests with fakes only.

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
| **CapabilityRouter with ModelProfile (device-capability-based model selection)** | **IMPLEMENTED (v0.3.1)** |
| **RescsDeviceProxy (device-scoped namespace enforcement)** | **IMPLEMENTED (v0.3.1)** |
| `HttpRescsAdapter` with fallback + health | IMPLEMENTED |
| Data distribution (owner-scoped retrieval → pagination → routing) | IMPLEMENTED |
| Organization ingestion/reconciliation boundary | IMPLEMENTED |
| Provisioning API + CLI (`provision-device`) and external client | IMPLEMENTED |
| Windows autostart (Task Scheduler / NSSM docs) | IMPLEMENTED (endurance not validated) |
| Physical LAN validation | **NOT YET PERFORMED** |
| 24/7 operational validation | **NOT YET PERFORMED** |

### 6.3 v0.6.0 capability summary

| Capability | Status |
|---|---|
| Combined `CORE-HOST` + `CORE-CLIENT` repository and root CI | IMPLEMENTED (v0.6.0 release; split 2026-11-21 into separate `CORE-HOST`, `CORE-CLIENT` and `RISARMS-HOST` repositories, each with its own CI) |
| Void x86_64 installer, versioned venvs, storage guard, Caddy/nftables, runit services and svlogd rotation | IMPLEMENTED (static tests only; booted Void pending) |
| Backup/restore, upgrade/rollback, diagnostics and install-state snapshots | IMPLEMENTED (static tests only; runtime drill pending) |
| Historical Pi deployment scripts, wheels, and validation evidence | RETAINED (not a 0.6.0 server target) |
| Signed R.E.S.C.S. owner scope (`X-RESCS-Signature`) | IMPLEMENTED |
| Per-profile service grants (`GET /api/service-grants`, `PUT/DELETE /api/profiles/{id}/service-grants/{service}`) | IMPLEMENTED |
| Registered owner-device binding for admin unlock | IMPLEMENTED |
| Durable owner-action queue with owner-device + password approval; crash-safe two-phase apply | IMPLEMENTED |
| `/api/ai-status` health surface | IMPLEMENTED |
| Tool-free `CORE_SAFE_CHAT` worker (account-isolated Ollama) | IMPLEMENTED |
| Booted Void install, reboot, runit start/stop, Caddy trust, nftables load | **NOT YET PERFORMED** |
| Upgrade, rollback, backup/restore and storage-failure drills on HP | **NOT YET PERFORMED** |
| Physical HP firmware, thermal and planned 2 x 8 GB DDR4-2666 upgrade (installed RAM unverified — earlier report: 4 GB; upgrade PLANNED, not installed) | **NOT YET PERFORMED** |

## 7. Related documentation

- [Void Linux host](../development/void-linux.md) — canonical 0.6.0 server target
- [Ubuntu 24.04 candidate](../development/ubuntu-24.04.md) — additive systemd candidate, not a release target
- [System Boundaries](../architecture/system-boundaries.md) — C.O.R.E.'s responsibility ownership
- [Communication Flow](../architecture/communication-flow.md) — the message path
- [Lifecycle](../architecture/lifecycle.md) — C.O.R.E. runtime semantics
- [Integration Contracts](../interfaces/integration-contracts.md) — the live C.O.R.E. ↔ R.E.S.C.S. contract
- [Interface Contracts](../interfaces/communication.md) — messaging/routing/service contracts
- [Security Overview](../security/overview.md) — what is enforced vs config-gated
- [Development Roadmap](../development/roadmap.md) — the consolidated, cross-system roadmap
- ADR: [0003](../decisions/0003-core-is-integration-layer.md), [0004](../decisions/0004-communication-abstraction.md)
