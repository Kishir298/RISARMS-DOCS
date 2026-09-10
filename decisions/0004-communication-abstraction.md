# Communication is abstracted behind a transport interface

## Context

R.I.S.A.R.M.S. must eventually deliver messages in-process, to other systems (R.E.S.C.S.), and to external devices. If callers pinned themselves to one delivery mechanism, every new transport (device, network, serial) would ripple through routing and services. The design needs delivery to be replaceable.

## Decision

Communication in C.O.R.E. is expressed against a **`Transport` abstraction**, not a concrete mechanism.

- Callers depend on the transport interface (send/request semantics).
- The in-process `LocalTransport` serves development/tests; `TcpTransport` now reaches external devices (TCP + TLS).
- Additional transports implement the same interface.
- Adding a transport must require implementing the interface only — no caller changes.

## Alternatives

- **Direct concrete transport calls everywhere** — rejected: replacing in-process delivery with a device/network transport would touch every caller.
- **Single "everything" transport object** — rejected: couples unrelated concerns (local, network, device) and defeats testability.
- **No abstraction (sync calls only)** — rejected: storage/device traffic is inherently asynchronous across process boundaries.

## Consequences

- Positive: routing, services, and adapters are transport-agnostic; each transport is independently testable (a fake transport in tests, the real one in integration).
- Cost: an interface with defined semantics must be maintained across concrete implementations.
- Guardrail: new transports conform to the interface or they do not ship.

## Status

Accepted and realized: `Transport` + `LocalTransport` + `TcpTransport` (TLS, external devices) are **implemented** in C.O.R.E. The abstraction's value is proven — multiple transports coexist without caller changes.