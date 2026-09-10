# Communication Contract

> [!NOTE] **Purpose:** These are the **architectural requirements** for how systems communicate in R.I.S.A.R.M.S. They describe what a contract must guarantee, not a locked API. Where something is already implemented, it is marked **IMPLEMENTED**; otherwise it is **PLANNED**.

## 1. Scope

This contract governs communication between:

- C.O.R.E. and each other system (A.S.I.S., R.E.S.C.S., T.I.V.I.S.S., RadarS.A.R.D.),
- C.O.R.E. and external devices.

It does **not** govern intra-C.O.R.E. logic, which is covered by [Routing](routing.md), [Services](services.md), and the [C.O.R.E. page](../systems/core.md).

## 2. Core guarantees

Every conversation across a system boundary must satisfy:

| Guarantee | Meaning |
|---|---|
| **Identify** | Every message identifies its source and destination |
| **Correlate** | Requests and responses share a request ID; messages carry an ID |
| **Type** | Every message has a defined type so routers/adapters can act |
| **Payload** | The payload is validated, serializable, and bounded |
| **Timestamp** | Every message is timestamped |
| **Fail loudly** | Failures are surfaced as defined errors, never silent drops |
| **Transport-agnostic** | Callers use a transport abstraction, not a concrete mechanism ([ADR 0004](../decisions/0004-communication-abstraction.md)) |

## 3. Transport abstraction

- [IMPLEMENTED] C.O.R.E. defines a `Transport` interface; callers depend on it.
- [IMPLEMENTED] An in-process `LocalTransport` provides thread-safe `send`/`request` with counters.
- [IMPLEMENTED] `TcpTransport` reaches external devices (TCP + mandatory TLS when externally bound, framing, connection limits, session handshake, persistent connections).
- [IMPLEMENTED] Structured protocol messages with version negotiation (0.2.x clients remain supported) — see [core.md](../systems/core.md).
- [PLANNED] Additional transports implement the same interface. See [Communication Flow](../architecture/communication-flow.md).

**Rule:** adding a transport must require implementing the interface only; no caller changes.

## 4. Serialization

- [IMPLEMENTED] Messages serialize as JSON for the local path.
- Contract requirement: serialization must be lossless for the fields in [Messaging](messaging.md), and must round-trip independently of transport.

## 5. Out-of-scope for this contract

- Security/authentication of communication channels → [Security](../security/overview.md) (note: external TCP transport requires TLS + token authentication — see [Authentication](../security/authentication.md)).
- Specific R.E.S.C.S. HTTP endpoints → [Integration Contracts](integration-contracts.md) (now implemented).
- Device wire-protocol message details → [core.md](../systems/core.md) (implemented).

## Related

- [Messaging Contract](messaging.md)
- [Routing Contract](routing.md)
- [Services Contract](services.md)
- [Communication Flow](../architecture/communication-flow.md)