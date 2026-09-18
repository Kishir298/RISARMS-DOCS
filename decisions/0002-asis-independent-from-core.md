# A.S.I.S. is independent from C.O.R.E.

## Context

The intelligence layer (A.S.I.S.) and the control engine (C.O.R.E.) serve different purposes: A.S.I.S. talks to humans, reasons, and generates responses; C.O.R.E. organizes, routes, and manages. If A.S.I.S. absorbed C.O.R.E. responsibilities — or vice versa — the ecosystem would gain a single system that is neither a good AI assistant nor a good control engine.

## Decision

A.S.I.S. is an **independent project**, developed and versioned separately from C.O.R.E.

- Filesystem: `RISARMS/ASIS/` — a sibling of `CORE-HOST/` + `CORE-CLIENT/`, not a child.
- A.S.I.S. uses C.O.R.E. through interfaces and communication contracts.
- A.S.I.S. does **not** directly own C.O.R.E.'s responsibilities (routing, resource registry, runtime, configuration, health, security infrastructure).
- A.S.I.S. reaches storage ([R.E.S.C.S.](../systems/rescs.md)) through C.O.R.E., never directly.

## Alternatives

- **A.S.I.S. built inside CORE** — rejected: the AI already grew (as Forza-AI) as its own project; folding it in would couple AI releases to engine releases.
- **A.S.I.S. becomes a thin C.O.R.E. shell** — rejected: A.S.I.S. legitimately owns intelligence and voice, which are its own domain.
- **C.O.R.E. embeds the AI logic** — rejected: C.O.R.E. is explicitly "not the primary AI."

## Consequences

- Positive: A.S.I.S. can pick its own AI stack, model integrations, and cadence; C.O.R.E. stays neutral infrastructure.
- Cost: a documented A.S.I.S. ↔ C.O.R.E. contract is required before the two interact ([integration-contracts](../interfaces/integration-contracts.md)), and A.S.I.S. must discipline itself not to grow control-engine features.
- Guardrail: any "system interaction" A.S.I.S. performs goes through C.O.R.E., not around it.

## Status

Accepted.