# Storage integrates with C.O.R.E. through an adapter

## Context

R.E.S.C.S. is an independent storage system (ADR 0001) with its own API, database, and object-store direction. C.O.R.E. callers (eventually A.S.I.S. and operators) need storage capability without C.O.R.E. knowing R.E.S.C.S. internals — and without R.E.S.C.S. becoming part of C.O.R.E.

## Decision

Storage is reached **through a C.O.R.E. adapter boundary**.

- A **`RescsAdapter`** abstraction lives in C.O.R.E. with `InMemory`, `File` and `Http` implementations; the HTTP adapter is the deployment path.
- The adapter translates C.O.R.E. requests into R.E.S.C.S. API calls and back ([integration-contracts](../interfaces/integration-contracts.md)).
- The adapter is the *only* bridge between C.O.R.E. logic and R.E.S.C.S.
- R.E.S.C.S. exposes its versioned record/file API **and a machine-readable contract** (`GET /api/v1/contract`) as the other side of the contract.
- Callers inside the ecosystem reach storage through C.O.R.E., never by calling R.E.S.C.S. directly ([data-flow](../architecture/data-flow.md)).
- R.E.S.C.S. remains the persistence authority: C.O.R.E. persists device identities and runtime history *through* the adapter and never creates a second database.

## Alternatives

- **Direct client libraries in every caller** — rejected: couples every caller to R.E.S.C.S., fragments tracing/authorization, and defeats C.O.R.E.'s hub role.
- **Fold R.E.S.C.S. into C.O.R.E.** — rejected by ADR 0001.
- **Storage proxied inside the communication layer without a service model** — rejected: storage needs service semantics (lifecycle, operation handlers, failure behavior) that the service layer already provides.

## Consequences

- Positive: storage appears to the ecosystem as just another C.O.R.E. service; authorization, correlation, and health apply uniformly.
- Cost: adapter and contract maintenance; both sides must keep the machine-readable contract in agreement.
- Guardrail: no storage logic ever moves from R.E.S.C.S. into C.O.R.E.; the adapter translates, it does not store.

## Status

Accepted and **implemented**: the adapter family and the contract exist on both sides, with contract-consuming tests. Deployed cross-host interop remains to be exercised (external validation).