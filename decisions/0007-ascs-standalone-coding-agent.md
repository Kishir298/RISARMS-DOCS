# A.S.C.S. is an ecosystem member that runs standalone until a contract exists

## Context

A.S.C.S. ("A Smart Coding System") is a local, autonomous coding agent built on Ollama. Its own package documentation states it is "intended to integrate with RISARMS and eventually be usable by ASIS and TIVISS," and it lives in the ecosystem workspace (`RISARMS/ASCS/`) with its own GitHub repository. However, it currently shares no code, contracts, or traffic with C.O.R.E., R.E.S.C.S., or A.S.I.S. During the ecosystem audit it was undocumented in the architecture docs.

Meanwhile C.O.R.E. v0.3.0 introduced capability-driven **agent scheduling** with default profiles `asis-local`, `asis-offload`, and `tiviss-compat` — agent-execution slots that a coding agent could eventually occupy.

## Decision

A.S.C.S. is recognized as a **member system of the R.I.S.A.R.M.S. ecosystem** with one clear responsibility: **autonomous coding execution**. Until a C.O.R.E.-mediated contract exists, it **runs and develops standalone**:

- A.S.C.S. remains an independent project beside the others; no system imports it and it imports no ecosystem system.
- Documentation describes it as standalone (**IMPLEMENTED** as a tool) and marks ecosystem integration as **FUTURE**.
- When integration happens, it follows the standard rule: A.S.I.S./T.I.V.I.S.S. reach coding capability **through C.O.R.E.**, never by invoking A.S.C.S. directly. The contract must be defined first ([Integration Contracts](../interfaces/integration-contracts.md)), per contract-first integration.
- A.S.C.S. must not grow ecosystem coordination, storage, or security-infrastructure responsibilities; those owners are unchanged ([System Boundaries](../architecture/system-boundaries.md)).

## Alternatives

- **Leave A.S.C.S. undocumented** — rejected: the docs must reflect the actual repository network, and an unrecorded system invites accidental coupling.
- **Treat A.S.C.S. as a tool inside A.S.I.S.** — rejected: it is a separately developed, separately versioned project with its own lifecycle; folding it in would couple AI releases to agent releases (same reasoning as ADR [0002](0002-asis-independent-from-core.md)).
- **Wire A.S.C.S. into C.O.R.E. immediately** — rejected: no contract exists; premature wiring would bypass the contract-first principle.

## Consequences

- Positive: the architecture reflects the real ecosystem; A.S.C.S. keeps an independent cadence (already at v0.3.0 with ~560 tests); the future integration path (via C.O.R.E.) is explicit.
- Cost: until integration, the ecosystem map shows a member with no live edges; the `asis-local`/`asis-offload` scheduler profiles are reservations, not integrations, and must not be documented as working paths.
- Guardrail: any direct A.S.C.S. call from A.S.I.S. or T.I.V.I.S.S. that bypasses C.O.R.E. invalidates this decision.

## Status

Accepted (recorded during the ecosystem documentation audit).
