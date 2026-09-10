# R.E.S.C.S. is independent from C.O.R.E.

## Context

R.I.S.A.R.M.S. is an ecosystem of systems. Storage (R.E.S.C.S.) and the control engine (C.O.R.E.) both need to evolve with different cadences, different failure domains, and different operational requirements. The requirement "R.E.S.C.S. must never live inside CORE" exists because bundling storage into the control engine couples their lifecycles, failure modes, and deployment.

## Decision

R.E.S.C.S. is an **independent project**, developed, versioned, and maintained separately from C.O.R.E.

- Filesystem: `RISARMS/RESCS/` — a sibling of `CORE/`, not a child.
- C.O.R.E. and R.E.S.C.S. communicate only through defined interfaces and communication contracts ([integration-contracts](../interfaces/integration-contracts.md)).
- C.O.R.E. never contains R.E.S.C.S. code; R.E.S.C.S. never imports C.O.R.E. internals.

## Alternatives

- **Monorepo/bundled storage inside CORE** — rejected: couples lifecycles, blurts responsibility boundaries, and risks the control engine absorbing storage concerns.
- **Publish-as-library (R.E.S.C.S. imported by C.O.R.E.)** — rejected: hard dependency prevents independent deployment and makes the wire contract optional.
- **C.O.R.E.-own database with no dedicated storage system** — rejected in spirit: R.E.S.C.S. exists as an independent storage service by design ([R.E.S.C.S.](../systems/rescs.md)).

## Consequences

- Positive: independent change and release cadences; storage can be deployed/operated separately; clear responsibility ownership. Both projects are now at v0.3.0 and were developed entirely independently.
- Cost: integration work is required to bridge the two; an explicit protocol/contract must be maintained (now implemented on both sides — see [integration contracts](../interfaces/integration-contracts.md)).
- Guardrail: the adapter must be the *only* bridge; direct coupling invalidates the decision.

## Status

Accepted. Enforced in the filesystem layout and reinforced throughout the documentation.