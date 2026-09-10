# Routing Contract

> [!NOTE] **Purpose:** Defines how messages are directed to the right endpoint. The in-C.O.R.E. router and device-to-device routing are **IMPLEMENTED**; A.S.I.S.-facing cross-system routing builds on the same principles and is **PLANNED**.

## 1. Responsibilities

Routing owns:

- Mapping **message type → destination endpoint**
- Delegating delivery to the active [transport](communication.md)
- Resolving unknown routes deterministically

Routing does **not** own: authorization (see [Authorization](../security/authorization.md)), payload construction, or business logic.

## 2. Contract

| Requirement | Behavior |
|---|---|
| Type-driven | Routes keyed by message type; no destination guessing in callers |
| Single hop | Caller → router → destination; the router is the point of dispatch |
| Deterministic failure | Unknown destination/type yields a defined error, never a silent drop |
| Transparent transport | Router hands delivery to a `Transport` abstraction; no transport knowledge in the caller |
| Observable | Routes and deliveries are inspectable (metrics/logs) |

## 3. Current implementation

[IMPLEMENTED] C.O.R.E.'s `Router` maps message type → service endpoint and delegates to the `Transport` with counters; the full `Message → Router → Service → Response` path is tested ([core.md](../systems/core.md)).

[IMPLEMENTED] Device-to-device routing: C.O.R.E. acts as the central hub (`DEVICE A → C.O.R.E. → DEVICE B`), validating source identity, destination registration, online state and active connection before forwarding; forwarded messages preserve `message_id`, `message_type`, `payload`, `request_id`, `identity_id`, source and destination. Offline/unavailable destinations produce structured device errors, never silent drops.

[IMPLEMENTED] Device-oriented routing of distributed data: retrieved R.E.S.C.S. data is normalized, deterministically ordered, paginated and delivered as `DATA_RESPONSE` messages over this routing layer.

## 4. A.S.I.S.-facing cross-system routing (PLANNED)

When C.O.R.E. routes outward (R.E.S.C.S. adapter, device transport), the *delivery endpoint* becomes an adapter or device endpoint registered with the router under a message type. The router itself does not change shape — only the endpoints behind the types change. This preserves the contract as integrations land.

## Related

- [Communication Contract](communication.md)
- [Messaging Contract](messaging.md)
- [Services Contract](services.md)
- [System Interactions](../architecture/system-interactions.md)