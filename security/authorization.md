# Authorization

> [!NOTE] **Status:** **Implemented as primitives and a config-gated enforcement mechanism; enforcement is inactive in the default development configuration.** C.O.R.E. authorization engages at the service-dispatch boundary only when `security.enforce_authorization` is true. External-device access control is enforced via authentication + identity binding (see [Authentication](authentication.md)). End-to-end, cross-system authorization enforcement remains future work.

## 1. Definition

Authorization answers: *"Given a proven identity, what may this actor do?"* It sits between **authentication** and **permission checking**.

## 2. Current reality

- **C.O.R.E.** `SecurityManager` exposes `authorize` and permission checks, with `IdentityType` and `Permission` primitives. These are implemented and usable in-process.
- **Enforcement is config-gated and inactive by default.** Dispatch-level enforcement exists at the service boundary but engages only when a `SecurityPolicy` is enforced (`security.enforce_authorization: true`). The shipped development configuration keeps it **false**; a LAN deployment must decide and document its setting.
- **External devices** are constrained by authentication and message-identity binding rather than by permission sets: they can only act as their authenticated identity, and unregistered devices cannot use application-level communication.
- No cross-system authorization exists — A.S.I.S./T.I.V.I.S.S. traffic that would need boundary authorization does not yet exist.

## 3. Contract requirements (target)

1. **Authorize before execute.** An operation runs only after authorization succeeds; the check precedes any side effect.
2. **Permission sets per identity/type.** Identities carry permitted operations; enforcement consults them.
3. **Gated operations.** The [Services contract](../interfaces/services.md) states that invocation returns a result or a defined error — unauthorized invocation is a defined authorization error, not a silent no-op.
4. **Border enforcement at C.O.R.E.** Cross-system calls entering C.O.R.E. (A.S.I.S., RadarS.A.R.D., devices) are authorized at the boundary before routing onward.
5. **Observable denials.** Every denial is logged/evented for operational visibility.

## 4. What authorization is NOT

- It is not authentication (covered by the previous step).
- It is not the same as per-system perimeter security (e.g., R.E.S.C.S.'s API key). Both exist; the ecosystem contract maps them ([Integration Contracts](../interfaces/integration-contracts.md)).

## Related

- [Authentication](authentication.md)
- [Security Overview](overview.md)
- [Trust Boundaries](trust-boundaries.md)
- [Security Overview](overview.md)