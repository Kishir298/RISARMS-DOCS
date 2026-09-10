# Authentication

> [!NOTE] **Status:** **Implemented at two perimeters; absent everywhere else.** C.O.R.E. enforces token-based authentication for external devices (with TLS), and R.E.S.C.S. enforces `X-API-Key` on its API. Internal/legacy C.O.R.E. use retains an existence-based provider. No cross-system authentication model exists — there is no A.S.I.S./T.I.V.I.S.S. traffic to authenticate.

## 1. Definition

Authentication answers: *"Is this actor genuinely who they claim to be?"* It sits between **identity** (who claims to act) and **authorization** (what they may do).

```
Identity → Authentication → Authorization
```

## 2. Current reality

- **C.O.R.E. (external devices)** — **IMPLEMENTED.** Pluggable providers: existence-based for internal/legacy use, **token-based for external devices**. External TCP requires TLS 1.2+ and a validated credential bound to the connection identity; identity/source spoofing (`identity_id != connection.identity_id`) rejects or closes the connection. Plaintext downgrade is not permitted when externally exposed; external binding without valid TLS fails closed. Local `127.0.0.1` keeps the legacy plaintext path for development and 0.2.x compatibility.
- **C.O.R.E. (internal/legacy)** — the existence-based provider authenticates any registered identity. Acceptable for internal/localhost use; do not expose it externally.
- **R.E.S.C.S.** — **IMPLEMENTED.** `X-API-Key` (min 16 chars) is verified with a constant-time compare on protected routes; the authenticated principal drives owner scoping. Optional single-owner lock mode (`RESCS_API_KEY_OWNER`). One shared key — not a per-client identity system.
- **A.S.I.S.** — no network-facing authentication; local single-user client.
- **A.S.C.S.** — local-only tool; no network-facing authentication by design.
- **A.S.I.S.** — no network-facing authentication; local single-user client.
- **A.S.C.S.** — local-only tool; no network-facing authentication by design.
- **T.I.V.I.S.S. / RadarS.A.R.D.** — no code connected.

> [!IMPORTANT] **There is no cross-system (ecosystem-wide) authentication scheme.** The two implemented mechanisms protect two specific perimeters. Anything beyond them is future work.

## 3. Contract requirements (target for remaining boundaries)

When A.S.I.S./T.I.V.I.S.S. integration lands, the following must hold:

1. An **authentication provider** abstraction verifies credentials — the single insertion point for credential logic (C.O.R.E. already has this shape; extend rather than bypass).
2. Unauthenticated or failed-authentication attempts:
   - are rejected with a defined error ([Messaging Errors](../interfaces/messaging.md#4-errors)),
   - are observable (logged, evented), and
   - never partially execute the requested operation.
3. Authentication state is per-identity and per-connection, never globally shared across disagreed identities.
4. Secret material (API keys, tokens) comes from configuration/environment, never from source or docs.
5. R.E.S.C.S. remains authoritative for its own perimeter; C.O.R.E.'s adapter presents valid credentials ([Integration Contracts](../interfaces/integration-contracts.md)).

## 4. Out of scope

- PKI / certificate identity beyond TLS transport certificates — not planned.
- Remote identity federation between independent systems — not planned; each system authenticates its own callers and the contract maps identity across the boundary.
- T.I.V.I.S.S. handover authentication — defined when T.I.V.I.S.S. identity/ownership is designed ([tiviss.md](../systems/tiviss.md)).

## Related

- [Authorization](authorization.md)
- [Security Overview](overview.md)
- [Trust Boundaries](trust-boundaries.md)
- ADR [0006](../decisions/0006-security-architecture.md)
