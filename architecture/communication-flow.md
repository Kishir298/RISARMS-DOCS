# Communication Flow

> [!NOTE] **Status:** The in-process message path is **IMPLEMENTED** (tested in C.O.R.E.). The C.O.R.E.-side HTTP adapter chain to R.E.S.C.S. and the external TCP+TLS device transport are also **IMPLEMENTED** (software complete; physical LAN validation pending). A.S.I.S.-originated cross-system traffic is **PLANNED**.

## Purpose

This document explains **how a message travels** through R.I.S.A.R.M.S., from the contract that describes it ([Messaging](../interfaces/messaging.md)) to the mechanisms that carry it (C.O.R.E.'s communication layer).

## 1. Message path inside C.O.R.E.

```mermaid
flowchart LR
    SRC["Source (caller)"] --> MSG["Message"]
    MSG --> ROUTER["Router"]
    ROUTER --> COMM["Communication / Transport"]
    COMM --> DISPATCH["ServiceDispatcher"]
    DISPATCH --> EXEC["ServiceManager.execute"]
    EXEC --> HANDLER["Operation handler"]
    HANDLER --> RESP["Response Message"]
    RESP --> SRC
```

Each of these steps exists today (see [core.md](../systems/core.md)):

| Step | Component | Notes |
|---|---|---|
| Message creation | `core/communication` | `Message` model carrying type, source, destination, payload |
| Routing | `core/routing.Router` | maps message type → destination; delegates to a `Transport` |
| Delivery | `core/communication.Transport` | abstract; concrete in-process `LocalTransport` |
| Dispatch | `core/services.ServiceDispatcher` | Message → `ServiceRequest` |
| Execution | `core/services.ServiceManager` | runs the operation handler |
| Response | `core/services` | `ServiceResponse` → Message |

## 2. Transport abstraction

The `Transport` interface is the contract every delivery mechanism must satisfy. Implemented transports today:

- `LocalTransport` — in-process (thread-safe send/request, endpoint registry, counters); default for development and tests.
- `TcpTransport` — external devices over TCP with mandatory TLS when externally bound (TLS 1.2+), framing, connection limits, session handshake, persistent connections.

The R.E.S.C.S. HTTP path rides the adapter layer (`HttpRescsAdapter`) rather than a message transport.

> [!IMPORTANT] **Transport rule:** callers depend on the `Transport` interface, never on a concrete transport directly. Adding a new transport must require implementing the interface only ([ADR 0004](../decisions/0004-communication-abstraction.md)).

## 3. Protocol and serialization

- Messages are serialized as JSON by `MessageSerializer`.
- The message envelope contract (fields, types, IDs) is defined in [Messaging Contract](../interfaces/messaging.md).
- Serialization is transport-independent; outbound adapters marshal messages into whatever R.E.S.C.S. or device protocols require, at the adapter boundary.
- The external device protocol adds structured protocol messages (`CORE_HANDSHAKE`, `DEVICE_REGISTER`, `DEVICE_DISCOVER`, `DEVICE_INFO`, `DEVICE_ERROR`, …) with version negotiation that keeps 0.2.x clients working; see [core.md](../systems/core.md).

## 4. Failure behavior

Failure behavior is part of the contract, not an afterthought:

- Unknown route / unknown destination → defined error ([Error model](../interfaces/messaging.md#4-errors)).
- Handler failure → isolated, recorded, surfaced as a response error (dispatch guarantees `ServiceResponse`, even on failure).
- Transport failure → a `transport`/`communication` error class; behavior surfaces deterministically rather than silently dropping.

## Related

- [Messaging Contract](../interfaces/messaging.md)
- [Routing Contract](../interfaces/routing.md)
- [Services Contract](../interfaces/services.md)
- [C.O.R.E. system page](../systems/core.md)
- [System Interactions](system-interactions.md)