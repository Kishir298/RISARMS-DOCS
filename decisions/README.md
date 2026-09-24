# Architecture Decision Records

> [!NOTE] **Purpose:** The record of *why* R.I.S.A.R.M.S. is shaped the way it is. Architectural choices are decided here so future agents can determine what was intentional and what was accidental.

## 1. Index

| ADR | Title |
|---|---|
| [0001](0001-rescs-independent-from-core.md) | R.E.S.C.S. is independent from C.O.R.E. |
| [0002](0002-asis-independent-from-core.md) | A.S.I.S. is independent from C.O.R.E. |
| [0003](0003-core-is-integration-layer.md) | C.O.R.E. is the integration/control layer |
| [0004](0004-communication-abstraction.md) | Communication is abstracted behind a transport interface |
| [0005](0005-storage-integration-via-adapter.md) | Storage integrates with C.O.R.E. through an adapter |
| [0006](0006-security-architecture.md) | Security is layered: identity → authentication → authorization |
| [0007](0007-ascs-standalone-coding-agent.md) | A.S.C.S. is an ecosystem member that runs standalone until a contract exists |
| [0008](0008-web-portals-presentation-only.md) | Web portals are presentation-only control planes |

## 2. Template

Every ADR follows this structure:

```markdown
# <Title>

## Context

## Decision

## Alternatives

## Consequences

## Status
```

**Decision rules:**

- Record decisions for architectural choices (boundaries, integration strategy, abstractions with lasting consequences).
- Do **not** create ADRs for trivial implementation details.
- Status values: **Accepted** / **Proposed** / **Superseded by ADR-NNN** / **Deprecated**.
- To revisit a decision, write a new ADR and mark the old one superseded — do not edit history in place (except for factual corrections).

## 3. How to add an ADR

1. Copy the template above.
2. Number sequentially (`0009-…`; 0008 already taken).
3. Fill Context (the problem), Decision (what we chose), Alternatives (what we rejected and why), Consequences (what the choice costs and enables), Status.
4. Link the ADR from the [System Boundaries](../architecture/system-boundaries.md) or the relevant system documentation.
5. Reference the ADR from the docs that rely on it.

## Related

- [Development Contributions](../development/contribution.md)
- [System Boundaries](../architecture/system-boundaries.md)