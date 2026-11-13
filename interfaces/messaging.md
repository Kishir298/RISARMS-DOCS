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

## 6. Human-to-human messaging (implemented 2026-11-13)

This is a distinct feature from assistant chat. It carries plain text between
two **approved** CORE accounts and grants no tool, shell, model or service
access.

### 6.1 Endpoints

| Endpoint | Semantics |
|---|---|
| `POST /api/messages` | `{recipient, body, client_id}` → `201 {id, sender, recipient, created, delivered, read}` |
| `GET /api/messages` | `{threads: [{peer, username, name, last_body, last_at, unread}]}` |
| `GET /api/messages?peer=<id>&after=<ts>` | `{messages: [...]}`; marks delivered messages as read |
| `POST /api/messages/<id>/read` | Recipient-only read acknowledgement |

### 6.2 Guarantees

1. **Server identity.** The server generates the message id; the client never
   invents one.
2. **Idempotency.** `client_id` (or `Idempotency-Key`) is unique per sender, so
   a retry returns the original message instead of duplicating it.
3. **Authorization.** Sender must be `owner` or `member`; recipient must be an
   approved account. Pending, rejected and revoked accounts cannot obtain a
   session at all.
4. **Isolation.** Reads are derived from the authenticated account id; a third
   account sees an empty thread, never another account's messages.
5. **Delivery honesty.** A message stored on the device but not acknowledged by
   the server is `queued`, never `delivered`.
6. **Offline durability.** The queue is persisted in the per-profile SQLite
   database and flushed by the synchronization loop after reconnect.
7. **No privilege escalation.** Messaging exposes no coding, shell or
   privileged AI surface to public members.

### 6.3 Event

`message.received` is published to the recipient's authenticated control
channels with `{from, message_id}`; it carries no message body.

## Related

- [Human Messaging in the desktop client](../systems/risarms-ui.md)
- [Communication Contract](communication.md)
- [Routing Contract](routing.md)
- [Services Contract](services.md)
- [Communication Flow](../architecture/communication-flow.md)