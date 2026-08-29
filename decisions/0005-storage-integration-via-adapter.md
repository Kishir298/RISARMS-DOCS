# Storage integrates with C.O.R.E. through an adapter

## Context

R.E.S.C.S. is an independent storage system (ADR 0001) with its own API, database, and object-store direction. C.O.R.E. callers (eventually A.S.I.S. and operators) need storage capability without C.O.R.E. knowing R.E.S.C.S. internals — and without R.E.S.C.S. becoming part of C.O.R.E.

## Decision

Storage is reached **through a C.O.R.E. adapter service**.

- A **R.E.S.C.S. adapter** lives in C.O.R.E. (v0.2 Phase 9), registered with the routing/services layers as a normal service.
- The adapter translates C.O.R.E. service requests into R.E.S.C.S. API calls and back ([integration-contracts](../interfaces/integration-contracts.md)).
- The adapter is the *only* bridge between C.O.R.E. logic and R.E.S.C.S..
- R.E.S.C.S. exposes its record/file API (currently planned) as the other side of the contract.
- Callers inside the ecosystem reach storage through C.O.R.E., never by calling R.E.S.C.S. directly ([data-flow](../architecture/data-flow.md)).

## Alternatives

- **Direct client libraries in every caller** — rejected: couples every caller to R.E.S.C.S., fragments tracing/authorization, and defeats C.O.R.E.'s hub role.
- **Fold R.E.S.C.S. into C.O.R.E.** — rejected by ADR 0001.
- **Storage proxied inside the communication layer without a service model** — rejected: storage needs service semantics (lifecycle, operation handlers, failure behavior) that the service layer already provides.

## Consequences

- Positive: storage appears to the ecosystem as just another C.O.R.E. service; authorization, correlation, and health apply uniformly.
- Cost: adapter and contract work (Phase 9); R.E.S.C.S. must first expose its record/file HTTP API and enforce authentication.
- Guardrail: no storage logic ever moves from R.E.S.C.S. into C.O.R.E.; the adapter translates, it does not store.

## Status

Accepted. Adapter is **PLANNED** (C.O.R.E. v0.2 Phase 9).