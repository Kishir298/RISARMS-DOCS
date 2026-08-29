# Trust Boundaries

> [!NOTE] **Status:** The trust model below is the **target** architecture. Today there is no cross-system traffic, so no boundaries are actually crossed in production. Treat this as the contract for when they are.

## 1. Purpose

A trust boundary is a point where the security model must re-validate: identity, authentication, authorization, and channel integrity. This document enumerates every boundary in the ecosystem.

## 2. Boundaries map

```mermaid
graph TB
    EXT["External Devices"] ---|B5| CORE["C.O.R.E."]
    ASIS["A.S.I.S."] ---|B1| CORE
    TIVISS["T.I.V.I.S.S."] ---|B2| CORE
    RADAR["RadarS.A.R.D."] ---|B3| CORE
    CORE ---|B4| RESCS["R.E.S.C.S."]
```

| Boundary | Between | Trust posture |
|---|---|---|
| **B1** | A.S.I.S. ↔ C.O.R.E. | External (independent project). A.S.I.S. is untrusted until authenticated/authorized at the boundary. |
| **B2** | T.I.V.I.S.S. ↔ C.O.R.E. | External, plus ownership/handover isolation; a transferred T.I.V.I.S.S. keeps its own identity profile. |
| **B3** | RadarS.A.R.D. ↔ C.O.R.E. | External sensor source; reports are untrusted until validated; RadarS.A.R.D. must not be able to mutate C.O.R.E. state directly. |
| **B4** | C.O.R.E. ↔ R.E.S.C.S. | External (independent project). API-key-authenticated; request correlation enforced; R.E.S.C.S. owns its perimeter. |
| **B5** | External devices ↔ C.O.R.E. | Least-trusted. Device inputs validated; commands authorized; device transport cannot impersonate C.O.R.E. |

## 3. Cross-boundary rules (target)

1. **No implicit trust.** Every boundary re-validates identity and authorization, even between ecosystem members.
2. **Least privilege.** Each actor gets the minimum permission set required by its role.
3. **Validation at the edge.** Payloads are validated and normalized at the boundary, never parsed by core logic as trusted.
4. **Correlation survives.** Request IDs cross boundaries so audit trails are continuous ([Messaging](../interfaces/messaging.md)).
5. **Detection is cooperative.** RadarS.A.R.D. reports into C.O.R.E.; C.O.R.E. decides and coordinates responses ([radar-sard.md](../systems/radar-sard.md)).

## 4. Current boundary inventory (reality check)

| Boundary | Exists today? | Today's posture |
|---|---|---|
| B1 A.S.I.S. ↔ C.O.R.E. | **No** | No traffic; A.S.I.S. standalone. |
| B2 T.I.V.I.S.S. ↔ C.O.R.E. | **No** | No code. |
| B3 RadarS.A.R.D. ↔ C.O.R.E. | **No** | No code. |
| B4 C.O.R.E. ↔ R.E.S.C.S. | **No** | No adapter; R.E.S.C.S. API key not yet enforced. |
| B5 Devices ↔ C.O.R.E. | **No** | No device transport (v0.2 Phase 10). |

> [!IMPORTANT] **Until a boundary has code, it has no implemented security.** Building the boundary (Phase 9/10 and R.E.S.C.S. auth) must include its trust enforcement, not bolt it on later.

## Related

- [Security Overview](overview.md)
- [System Boundaries](../architecture/system-boundaries.md)
- [Integration Contracts](../interfaces/integration-contracts.md)
- ADR [0006](../decisions/0006-security-architecture.md)