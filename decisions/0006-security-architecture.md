# Security is layered: identity → authentication → authorization

## Context

R.I.S.A.R.M.S. spans independent systems and will eventually cross trust boundaries to external devices and a handover-able agent (T.I.V.I.S.S.). A single "is this allowed?" gate is insufficient; the ecosystem needs separated, individually developable security steps — and it needs them *without pretending* that production-grade security exists today.

## Decision

Security follows a **layered model** owned by C.O.R.E.'s security infrastructure:

```text
Identity → Authentication → Authorization → Permission checking → Resource/service access
```

- **Identity** — who is acting (systems, agents, operators; per-identity profiles).
- **Authentication** — proving identity with credentials, via a dedicated provider (deferred to v0.2 Phase 8; today C.O.R.E. only verifies identity existence).
- **Authorization** — what the proven identity may do.
- **Permission checking** — enforcement on concrete operations.
- **Access** — the gated resource/service call.

Each system also secures its own perimeter consistently (e.g., R.E.S.C.S. API-key enforcement — configured but not yet enforced).

## Alternatives

- **Single monolithic auth gate** — rejected: cannot model per-system/perimeter security or the future handover-able agent's independent identity.
- **Embedded/logic-level auth throughout** — rejected: security is infrastructure by decision (ADR 0003) and must be enforced at boundaries, not scattered.
- **Defer all security until v1** — rejected: the foundation (identities, permissions, manager) is cheap and already exists.

## Consequences

- Positive: each layer is developable and testable in isolation; boundaries have a clear place to enforce ([trust-boundaries](../security/trust-boundaries.md)); honest status docs prevent false claims of protection.
- Cost: **today the stack is unenforced** — there is no credential validation (C.O.R.E.), no API-key middleware (R.E.S.C.S.), and no cross-system traffic to protect yet. This is tracked (v0.2 Phase 8, R.E.S.C.S. auth) and must not be misread as shipping security.
- Guardrail: no boundary is claimed secured until its enforcement lands with it.

## Status

Accepted as architecture. Implementation is **foundation only**; enforcement is planned.