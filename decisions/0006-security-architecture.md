# Security is layered: identity → authentication → authorization

## Context

R.I.S.A.R.M.S. spans independent systems and will eventually cross trust boundaries to external devices and a handover-able agent (T.I.V.I.S.S.). A single "is this allowed?" gate is insufficient; the ecosystem needs separated, individually developable security steps — and it needs them *without pretending* that production-grade security exists today.

## Decision

Security follows a **layered model** owned by C.O.R.E.'s security infrastructure:

```text
Identity → Authentication → Authorization → Permission checking → Resource/service access
```

- **Identity** — who is acting (systems, agents, operators; per-identity profiles).
- **Authentication** — proving identity with credentials, via a dedicated provider. **Implemented at two perimeters:** C.O.R.E.'s token provider for external devices (with TLS) and R.E.S.C.S.'s enforced `X-API-Key`. Internal/legacy C.O.R.E. use retains an existence-based provider.
- **Authorization** — what the proven identity may do. Primitives and a config-gated dispatch-boundary enforcement exist; the shipped development config leaves enforcement off.
- **Permission checking** — enforcement on concrete operations.
- **Access** — the gated resource/service call.

Each system also secures its own perimeter consistently (R.E.S.C.S. enforces its API key; C.O.R.E. enforces TLS + token auth externally).

## Alternatives

- **Single monolithic auth gate** — rejected: cannot model per-system/perimeter security or the future handover-able agent's independent identity.
- **Embedded/logic-level auth throughout** — rejected: security is infrastructure by decision (ADR 0003) and must be enforced at boundaries, not scattered.
- **Defer all security until v1** — rejected: the foundation (identities, permissions, manager) is cheap and already exists.

## Consequences

- Positive: each layer is developable and testable in isolation; boundaries have a clear place to enforce ([trust-boundaries](../security/trust-boundaries.md)); honest status docs prevent false claims of protection.
- Cost: **the stack is enforced only at the two perimeters built so far** (C.O.R.E. external devices, R.E.S.C.S. API). There is no cross-system identity federation, no end-to-end authorization across ecosystem flows, and development configs deliberately run without authorization enforcement. These must not be misread as shipping end-to-end security.
- Guardrail: no boundary is claimed secured until its enforcement lands with it — and no boundary is claimed production-hardened until it is deployment-validated.

## Status

Accepted. Implementation: **perimeter enforcement at two boundaries; foundation elsewhere; cross-system enforcement planned.**