# C.O.R.E. is the integration/control layer

## Context

An ecosystem of independent systems (storage, intelligence, agents, sensing) needs a single place where traffic converges — otherwise systems must know each other's internals and responsibility ownership fragments. R.I.S.A.R.M.S. needs a hub that owns coordination without owning the systems' purposes.

## Decision

**C.O.R.E. is the integration and control layer of the ecosystem.**

- All cross-system traffic flows through C.O.R.E. ([interactions](../architecture/system-interactions.md)). External devices route through C.O.R.E. as a central hub — never peer-to-peer — as implemented in v0.3.0.
- C.O.R.E. owns: communication, message protocols, routing, organization, resources, services, runtime/lifecycle, events, dependencies, configuration, health, logging, security infrastructure.
- C.O.R.E. is *not* the primary AI (that is A.S.I.S./T.I.V.I.S.S.) and is not the storage system (that is R.E.S.C.S.).
- C.O.R.E. coordinates the ecosystem's response to events; detection itself belongs to the sensor layer (RadarS.A.R.D.).

## Alternatives

- **P2P mesh (systems peer directly)** — rejected: every system would need shared knowledge of every other system; no single responsible owner; observability fragmented.
- **One mega-system** — rejected by ADR 0001/0002: independent systems are a stated requirement.
- **No hub (all systems autonomous with point integrations)** — rejected: contradicts testability, observability, and contract-first principles.

## Consequences

- Positive: single point of coordination; one responsibility table that agents can rely on ([boundaries](../architecture/system-boundaries.md)); security has a choke point ([trust-boundaries](../security/trust-boundaries.md)).
- Cost: C.O.R.E. is on every critical path, so its health, lifecycle, and reliability matter disproportionately; C.O.R.E. must maintain strict discipline not to absorb subsystems' purposes.
- Guardrail: a responsibility belongs to C.O.R.E. only if the boundary table says so.

## Status

Accepted.