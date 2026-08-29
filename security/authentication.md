# Authentication

> [!NOTE] **Status:** **PLANNED** (foundation only). C.O.R.E.'s `SecurityManager.authenticate()` exists but only verifies identity existence; credential verification is deferred to a dedicated provider (v0.2 Phase 8).

## 1. Definition

Authentication answers: *"Is this actor genuinely who they claim to be?"* It sits between **identity** (who claims to act) and **authorization** (what they may do).

```
Identity → Authentication → Authorization
```

## 2. Current reality

- **C.O.R.E.** maintains identities via `SecurityManager` (implemented). `authenticate()` currently succeeds for any *registered* identity — it does not verify credentials. This is documented in code as intentionally deferred.
- **R.E.S.C.S.** accepts an API-key contract (`X-API-Key`, `RESCS_API_KEY`) at configuration time but does not enforce it.
- **A.S.I.S.** has no network-facing authentication; it is a local single-user client.

> [!IMPORTANT] **No cross-system authentication exists today.**

## 3. Contract requirements (target)

When the authentication provider lands (v0.2 Phase 8), the following must hold:

1. An **authentication provider** abstraction verifies credentials — it is the single insertion point for credential logic.
2. Unauthenticated or failed-authentication attempts:
   - are rejected with a defined error ([Messaging Errors](../interfaces/messaging.md#errors)),
   - are observable (logged, evented), and
   - never partially execute the requested operation.
3. Authentication state is per-identity and per-request, never globally shared across disagreed identities.
4. Secret material (API keys, tokens) comes from configuration/environment, never from source or docs.
5. R.E.S.C.S. enforces its own API-key authentication as part of its perimeter; C.O.R.E.'s adapter presents valid credentials ([Integration Contracts](../interfaces/integration-contracts.md)).

## 4. Out of scope

- PKI / certificate identity — not planned.
- Remote identity federation between independent systems — not planned; each system authenticates its own callers and the contract maps identity across the boundary.
- T.I.V.I.S.S. handover authentication — defined when T.I.V.I.S.S. identity/ownership is designed ([tiviss.md](../systems/tiviss.md)).

## Related

- [Authorization](authorization.md)
- [Security Overview](overview.md)
- [C.O.R.E. v0.2 Phase 8](../systems/core.md#phase-8--security-integration)
- ADR [0006](../decisions/0006-security-architecture.md)