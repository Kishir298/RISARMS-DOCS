# System Boundaries

> [!NOTE] **Status:** Boundaries are the *target* architecture and are already enforced in the project layout. Implementation status of individual features is in [`systems/`](../systems/).

## Purpose

This document defines **who owns which responsibility**. The rule throughout R.I.S.A.R.M.S. is *no duplicated ownership*: every responsibility has exactly one clear owner. If a future agent is unsure where a capability belongs, this table is the answer.

## 1. Responsibility ownership

| Responsibility | Owner | Owner page |
|---|---|---|
| Communication | **C.O.R.E.** | [core.md](../systems/core.md) |
| Message protocols | **C.O.R.E.** | [core.md](../systems/core.md) |
| Routing | **C.O.R.E.** | [core.md](../systems/core.md) |
| Organization | **C.O.R.E.** | [core.md](../systems/core.md) |
| Resource management | **C.O.R.E.** | [core.md](../systems/core.md) |
| Services | **C.O.R.E.** | [core.md](../systems/core.md) |
| Runtime / lifecycle | **C.O.R.E.** | [core.md](../systems/core.md) |
| Events | **C.O.R.E.** | [core.md](../systems/core.md) |
| Dependencies | **C.O.R.E.** | [core.md](../systems/core.md) |
| Configuration | **C.O.R.E.** | [core.md](../systems/core.md) |
| Health monitoring | **C.O.R.E.** | [core.md](../systems/core.md) |
| Logging | **C.O.R.E.** | [core.md](../systems/core.md) |
| Security infrastructure | **C.O.R.E.** | [core.md](../systems/core.md) |
| System integration/coordination | **C.O.R.E.** | [core.md](../systems/core.md) |
| Cloud-backed storage (records, files, persistent data) | **R.E.S.C.S.** | [rescs.md](../systems/rescs.md) |
| Data synchronization / retrieval | **R.E.S.C.S.** | [rescs.md](../systems/rescs.md) |
| Storage used by other systems | **R.E.S.C.S.** | [rescs.md](../systems/rescs.md) |
| Natural-language understanding | **A.S.I.S.** | [asis.md](../systems/asis.md) |
| Reasoning | **A.S.I.S.** | [asis.md](../systems/asis.md) |
| Response generation | **A.S.I.S.** | [asis.md](../systems/asis.md) |
| AI model interaction | **A.S.I.S.** | [asis.md](../systems/asis.md) |
| Voice functionality | **A.S.I.S.** | [asis.md](../systems/asis.md) |
| AI-agent identity, memory, permissions, ownership, handover | **T.I.V.I.S.S.** | [tiviss.md](../systems/tiviss.md) |
| Device registry, device routing, agent scheduling, data distribution | **C.O.R.E.** | [core.md](../systems/core.md) |
| Detection/reporting of security anomalies | **RadarS.A.R.D.** | [radar-sard.md](../systems/radar-sard.md) |
| Environmental/device/sensor monitoring | **RadarS.A.R.D.** | [radar-sard.md](../systems/radar-sard.md) |
| Alert generation / security event reporting | **RadarS.A.R.D.** | [radar-sard.md](../systems/radar-sard.md) |
| Autonomous coding execution | **A.S.C.S.** | [asc.md](../systems/asc.md) |

## 2. Explicit non-ownership

Equally important is what each system does **not** own:

- **C.O.R.E does not own** the AI brain, the storage, the anomaly sensors, agent identity, or autonomous coding. It coordinates them. It does not contain R.E.S.C.S., A.S.I.S. or A.S.C.S. code.
- **R.E.S.C.S. does not own** the message bus, routing, or runtime; it serves storage. It must not grow a UI or an intelligence layer.
- **A.S.I.S. does not own** C.O.R.E.'s responsibilities (message routing, resource registry, runtime, security infrastructure). It may only *use* them.
- **T.I.V.I.S.S. does not** copy A.S.I.S.; it owns a distinct identity and handover model.
- **RadarS.A.R.D. does not own** the handling of its detections. It **detects and reports**; C.O.R.E. owns event coordination, logging, health state, and system response.
- **A.S.C.S. does not own** ecosystem coordination or storage. It is a standalone coding agent; when integrated, C.O.R.E. mediates access to it.

## 3. Independent projects

> [!IMPORTANT] **Independence rule** — R.E.S.C.S. and A.S.I.S. are independent projects, developed separately from C.O.R.E.:

```text
RISARMS/
├── CORE/           <- owned by C.O.R.E. development
├── RESCS/          <- owned by R.E.S.C.S. development (independent)
├── ASIS/           <- owned by A.S.I.S. development (independent)
├── ASCS/           <- owned by A.S.C.S. development (independent)
└── RISARMS-DOCS/   <- this documentation (TIVISS is GitHub-only)
```

C.O.R.E. must never contain `RESCS/`, `ASIS/` or `ASCS/`. Integration is contract-based. Rationale: ADR [0001](../decisions/0001-rescs-independent-from-core.md), ADR [0002](../decisions/0002-asis-independent-from-core.md), ADR [0005](../decisions/0005-storage-integration-via-adapter.md), ADR [0007](../decisions/0007-ascs-standalone-coding-agent.md).

## 4. Boundary rules for agents

When adding or moving functionality, apply these checks:

1. **Is there already an owner?** If yes, the change belongs to that owner, not a new location.
2. **Does this create duplicated ownership?** If a responsibility would have two owners, stop and consult [Decisions](../decisions/README.md).
3. **Does this reach into another system's internals?** If yes, rewrite it as a call through the appropriate interface ([interfaces](../interfaces/communication.md)).
4. **Does this put cross-system code inside C.O.R.E.?** Storage logic belongs to R.E.S.C.S., not C.O.R.E.; intelligence belongs to A.S.I.S., not C.O.R.E.

## Related

- [System Interactions](system-interactions.md)
- [Trust Boundaries](../security/trust-boundaries.md)
- [Integration Contracts](../interfaces/integration-contracts.md)
- [Development Contributions](../development/contribution.md)