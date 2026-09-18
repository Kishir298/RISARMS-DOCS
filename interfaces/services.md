# Services Contract

> [!NOTE] **Purpose:** Defines the lifecycle and behavior of services — the executable unit C.O.R.E. manages. The C.O.R.E. service layer (9 services in v0.3.0, including the agent scheduler service) is **IMPLEMENTED**; cross-system services reuse these semantics but are **PLANNED**.

## 1. What a service is

A service is a C.O.R.E.-managed unit of work that:

- **Registers** with an identifier and metadata,
- **Has a lifecycle** (its own start/stop, dependency-aware),
- **Is invocable** — receives a request, executes an operation, returns a result,
- **Fails deterministically**.

## 2. Contract

### Registration
- Services register with a stable identifier and optional dependencies before they can be invoked.
- Duplicate/invalid registration is a defined error.

### Lifecycle
- Services start/stop under the runtime's ordering rules ([Lifecycle](../architecture/lifecycle.md)).
- A service reflects its state via health ([core.md](../systems/core.md)).

### Invocation
- Callers invoke through the message/service path, not by reaching into a service's internals.
- Every invocation returns a result (`ServiceResponse`) — success or a defined error.

### Failure behavior
- An operation failure must not destabilize the service, the runtime, or other services.
- Failures are observable (response + `[IMPLEMENTED]` event/log via C.O.R.E.).

## 3. Current implementation

[IMPLEMENTED] `Service`, `ServiceRequest`/`ServiceResponse`, `ServiceStatus`, `ServiceManager` (dependency-aware lifecycle, real operation-handler execution), and `ServiceDispatcher` (Message → ServiceRequest → operation → ServiceResponse → Message). See [core.md](../systems/core.md).

## 4. Events

Events are the service layer's way of announcing state changes.

| Field | Requirement |
|---|---|
| Event type | Stable, documented type token |
| Source | Which service/system produced it |
| Payload | Validated payload describing the change |
| Timestamp | UTC production time |
| Subscribers | Decoupled — publish succeeded once; handlers may subscribe without publisher knowledge |

[IMPLEMENTED] C.O.R.E.'s `EventBus` already provides subscribe/unsubscribe/publish, with isolated handler failures so subscribers cannot destabilize publishers ([core.md](../systems/core.md)).

## Related

- [Messaging Contract](messaging.md)
- [Service lifecycle](../architecture/lifecycle.md)
- [RadarS.A.R.D. reporting](../systems/radar-sard.md)
- [C.O.R.E. system page](../systems/core.md)