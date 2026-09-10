# Messaging Contract

> [!NOTE] **Purpose:** Defines the required shape of a message and the request/response/error semantics. These are architectural requirements — implement them in whatever concrete form the owning system uses, but do not omit the semantics.

## 1. Message envelope

Every message must carry:

| Field | Requirement | Notes |
|---|---|---|
| Source | Who sent it | system + component identity |
| Destination | Who should receive it | system + component/endpoint identity |
| Message type | Stable, documented type token | drives routing ([Routing](routing.md)) |
| Message ID | Unique identifier | for tracing/dedup |
| Request ID | Correlation ID of the request thread | links request, response, events |
| Payload | Validated, serializable payload | structure per message type |
| Timestamp | When the message was produced | UTC |

> [!NOTE] **Implementation status:** A `Message` model with these semantics is [IMPLEMENTED] inside C.O.R.E. (`core/communication`), and the external device protocol enforces message identity (source must equal the authenticated connection identity). Cross-system message envelopes beyond the device protocol (e.g. an A.S.I.S.-facing envelope) remain **PLANNED** — field names lock when that transport lands.

## 2. Requests

A request is a message that expects a response. Contract requirements:

1. **Format** — requests conform to the message envelope above; payload validated before dispatch.
2. **Validation** — invalid requests fail fast with a defined error, not a malformed downstream call.
3. **Response** — every request receives a response (success or error); no orphaned calls.
4. **Correlation** — response carries the same request ID as the triggering request.

## 3. Responses

- Return a defined success payload or a defined error.
- Preserve request correlation (request ID, source/destination mirrored).

## 4. Errors

Contract requirements:

- Errors are typed and carry a stable code (not free-text only). C.O.R.E. already does this — see `errors/` in [core.md](../systems/core.md) — and R.E.S.C.S. exposes a stable JSON error envelope with machine-readable codes ([Integration Contracts](integration-contracts.md)).
- Transport/routing/validation failures produce defined error types.
- An error must never be a silent drop from the ecosystem's perspective; it must be observable (response, event, or log).
- Cross-system error codes will be mapped per-adapter ([integration-contracts.md](integration-contracts.md)).

## 5. Service requests

Service-specific requests (invoking an operation on a service) are covered by [Services Contract](services.md).

## Related

- [Communication Contract](communication.md)
- [Routing Contract](routing.md)
- [Services Contract](services.md)
- [Communication Flow](../architecture/communication-flow.md)