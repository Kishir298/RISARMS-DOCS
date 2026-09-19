# Architecture Overview

> [!NOTE] **Status:** The architecture described here is the *target* architecture. Per-system implementation status is marked individually and defined below.

## Purpose

This document is the top-level view of the R.I.S.A.R.M.S. ecosystem. It defines:

- what R.I.S.A.R.M.S. is,
- how the systems fit together,
- the meaning of every arrow between systems,
- the vocabulary used to describe implementation status,
- and the principles that govern the whole architecture.

Detail lives in the sibling documents:

- [System Boundaries](system-boundaries.md) — who owns which responsibility
- [System Interactions](system-interactions.md) — who talks to whom and how
- [Data Flow](data-flow.md) — where data and records live
- [Communication Flow](communication-flow.md) — how messages travel
- [Lifecycle](lifecycle.md) — how systems start, stop and recover

## 1. Definition

**R.I.S.A.R.M.S.** — **R**ishik's **I**ntelligent **S**mart **A**dministration and **R**esource **M**anagement **S**ystem — is the ecosystem name for a set of cooperating subsystems:

| System | Expansion | Role |
|---|---|---|
| **C.O.R.E.** | Communication, Organization and Resource Engine | Central management and control engine |
| **R.E.S.C.S.** | Rishik's Efficient System for Cloud Storage | Cloud/data storage |
| **A.S.I.S.** | A Smart Intelligence System | Primary AI / intelligence layer |
| **T.I.V.I.S.S.** | Though I'm Vanquished, I'm Still Stronger | Separate AI agent (handover-oriented, remote foundation) |
| **RadarS.A.R.D.** | Radar Security, Anomaly Reconnaissance Device | Security and anomaly detection |
| **A.S.C.S.** | A Smart Coding System | Autonomous coding agent (currently standalone) |

The systems are modular. They are independently developed. They are ultimately intended to operate as **one ecosystem**.

## 2. The ecosystem diagram

```mermaid
graph TB
    R["R.I.S.A.R.M.S."]
    CORE["C.O.R.E."]
    RESCS["R.E.S.C.S."]
    ASIS["A.S.I.S."]
    TIVISS["T.I.V.I.S.S."]
    RADAR["RadarS.A.R.D."]
    ASCS["A.S.C.S."]

    R --> CORE
    CORE -->|coordinate & route| RESCS
    CORE -->|coordinate & route| ASIS
    CORE -->|coordinate & route| TIVISS
    CORE -->|coordinate & route| RADAR
    CORE -.->|"future: coding capability"| ASCS
    ASIS -->|request via| CORE
    RESCS -->|serve via| CORE
```

### What each arrow means

- **`R.I.S.A.R.M.S.` → `C.O.R.E.`** — the ecosystem exercises its management, communication and control functions *through* C.O.R.E. C.O.R.E. is the operational hub.
- **`C.O.R.E.` → subsystem** — C.O.R.E. is the coordinator: it routes requests, manages communication, governs lifecycle, and owns the shared security infrastructure for the flow. This is management/coordination, not ownership of the subsystem's core purpose.
- **`A.S.I.S.` → `C.O.R.E.`** — the AI layer issues requests (service calls, storage access, device control) to C.O.R.E. rather than reaching other systems directly.
- **`R.E.S.C.S.` → `C.O.R.E.`** — storage serves results back through C.O.R.E., and is invoked by C.O.R.E. on behalf of callers.
- **`C.O.R.E. -.-> A.S.C.S.` (dashed)** — future, not built: coding capability reached through C.O.R.E. No traffic exists today.

> [!NOTE] **Arrow direction ≠ implemented today.** These arrows describe intended architecture. What is implemented today is stated in each system's page under [`systems/`](../systems/) and in [System Interactions](system-interactions.md#3-implemented-vs-planned-by-pair).

### The conceptual inner diagram

```mermaid
graph TB
    EXT["External Devices"] -->|TLS + token auth| CORE["C.O.R.E."]
    CORE --> SERVICES["Services"]
    CORE --> RESOURCES["Resources"]
    CORE --> COMM["Communication"]
    SERVICES --> ECOSYSTEM["R.I.S.A.R.M.S."]
    RESOURCES --> ECOSYSTEM
    COMM --> ECOSYSTEM
```

C.O.R.E. receives traffic from the outside, then uses its services, resource registry and communication layer to act — and the result feeds back into the ecosystem.

## 3. Status vocabulary

Every feature or system in this documentation is labeled with one of four statuses. The labels are the single source of truth for "does this exist yet?".

> [!NOTE] **IMPLEMENTED** — the functionality exists in code and is verified by tests.

> [!NOTE] **IN DEVELOPMENT** — the functionality is actively being built; parts may work, parts may be incomplete.

> [!NOTE] **PLANNED** — the decision to build it has been made and the design is documented here; no code exists.

> [!NOTE] **FUTURE** — a longer-term aspiration; design intent only, not committed.

**Any sentence in this documentation that describes behavior carries one of these statuses.** "Planned as implemented" language is forbidden: if the behavior is described but marked PLANNED/FUTURE, it is not real yet.

> [!NOTE] **Status vocabulary — use only these four:** `IMPLEMENTED` / `IN DEVELOPMENT` / `PLANNED` / `FUTURE`. Do not use `COMPLETE`, `Shipped`, or `Current release` as status labels. `NOT YET PERFORMED` / `Ready for External Validation` means software `IMPLEMENTED`, deployment-validation `PLANNED` (physical LAN, live backends, 24/7 endurance still required).

## 4. Architectural principles

The following principles govern the entire ecosystem. See [Development Philosophy](../development/contribution.md) for the written policy.

1. **Modularity** — systems remain independently developable.
2. **Explicit boundaries** — each system has clearly defined responsibilities.
3. **No duplicated ownership** — every responsibility has exactly one clear owner (see [System Boundaries](system-boundaries.md#1-responsibility-ownership)).
4. **Contract-first integration** — systems communicate through explicit interfaces (see [Interface Contracts](../interfaces/communication.md)).
5. **Testability** — every major integration is testable independently (see [Testing](../development/testing.md)).
6. **Observable operation** — runtime state, health, events and failures are observable.
7. **Controlled dependencies** — subsystems never silently depend on implementation details of other systems.
8. **No fake functionality** — documentation never describes planned functionality as implemented.

## 5. System inventory and ownership (summary)

The full ownership table is in [System Boundaries](system-boundaries.md#1-responsibility-ownership). In brief:

| Responsibility | Owner |
|---|---|
| Communication, message protocols, routing | **C.O.R.E.** |
| Organization, resource registry, services, agent scheduling | **C.O.R.E.** |
| Runtime/lifecycle, events, dependencies, configuration, health, logging | **C.O.R.E.** |
| Security infrastructure (for ecosystem flows) | **C.O.R.E.** |
| Cloud storage, persistent data, files, sync | **R.E.S.C.S.** |
| NLP, reasoning, response generation, voice interaction | **A.S.I.S.** |
| AI-agent identity/memory/permissions/handover | **T.I.V.I.S.S.** (remote foundation) |
| Detection and reporting of anomalies | **RadarS.A.R.D.** (planned) |
| Autonomous coding execution | **A.S.C.S.** |

## 6. Current state vs future state (snapshot)

> [!NOTE] This snapshot is accurate as of the last documentation update and is maintained in [`development/roadmap.md`](../development/roadmap.md).

| System | Now | Next |
|---|---|---|
| **C.O.R.E.** | v0.3.0 software IMPLEMENTED (689 passed 2026-09-18, verify with pytest -q): TLS device transport, token auth, device registry/persistence, agent scheduling, HTTP R.E.S.C.S. adapter, data distribution | Physical Windows ↔ Mac LAN validation; 24/7 operational validation |
| **R.E.S.C.S.** | v0.3.0: versioned HTTP API, enforced API-key auth, records/files, streaming + resumable uploads, lifecycle/governance, C.O.R.E. contract | Live PostgreSQL/Supabase + real S3 validation; deployed C.O.R.E. ↔ R.E.S.C.S. interop |
| **A.S.I.S.** | Rebuilt `asis` package (CLI, Ollama provider, memory, 30-op calculator, 136-lang translation, web tools, coding mode, permissions, voice pipeline; 693 tests) + legacy `core/`/`02_voice/` trees deprecated, pending removal | Physical LAN validation; R.E.S.C.S. via C.O.R.E. (future) |
| **T.I.V.I.S.S.** | Local v0.1.0 foundation at `TIVISS/` (identity, ownership states, adapters as local/mock interfaces; still no live traffic) | Resolve the handover model |
| **RadarS.A.R.D.** | — | Define sensor/detection scope |
| **A.S.C.S.** | Standalone v0.3.0 coding agent (949 passed / 6 skipped 2026-09-18; live opt-in RISALIVE=1) | Ecosystem integration through C.O.R.E. (future) |

## 7. Filesystem reality

The documentation governs these directories:

```text
RISARMS/
├── CORE-HOST/      <- C.O.R.E. server/runtime (package `core`)
├── CORE-CLIENT/    <- C.O.R.E. external-device client (package `client`, stdlib-only)
├── RESCS/
├── ASIS/
├── ASCS/
└── DOCS/           <- this repository (remote: RISARMS-DOCS; TIVISS is cloned locally at `TIVISS/`)
```

> [!NOTE] **Out-of-scope sibling:** `Flavora/` (local-first food companion) may sit beside these directories on disk. It is not an ecosystem member and is not governed by this architecture.

> [!IMPORTANT] **Independence rule:** R.E.S.C.S., A.S.I.S., A.S.C.S. and T.I.V.I.S.S. are independent projects and must never be placed inside CORE. Integration occurs through interfaces and communication contracts, governed by [Integration Contracts](../interfaces/integration-contracts.md). Referenced in ADR [0001](../decisions/0001-rescs-independent-from-core.md), [0002](../decisions/0002-asis-independent-from-core.md) and [0007](../decisions/0007-ascs-standalone-coding-agent.md).

## Next steps

- Read [System Boundaries](system-boundaries.md) to learn exactly who owns what.
- Read [System Interactions](system-interactions.md) to learn how the systems connect.
- Read each system page in [`../systems`](../systems/) for detailed, current status.
