# Authorization

> [!NOTE] **Status:** **Implemented, config-gated, and inactive by default.** C.O.R.E. has authorization/permission primitives and now a config-gated enforcement mechanism (`SecurityPolicy.enforced` / the `security.enforce_authorization` config knob, both defaulting to inactive). Enforcement engages at the service-dispatch boundary only when a policy is present **and** enforced; the authentication provider and end-to-end (cross-system) enforcement remain v0.2 Phase 8 work.

## 1. Definition

Authorization answers: *"Given a proven identity, what may this actor do?"* It sits between **authentication** and **permission checking**.

## 2. Current reality

- **C.O.R.E.** `SecurityManager` exposes `authorize` and permission checks, with `IdentityType` and `Permission` primitives. These are implemented and usable in-process.
- **Enforcement is config-gated and inactive by default.** Dispatch-level enforcement exists at the service boundary (see [Phase 8](../systems/core.md#phase-8-security-integration)) but engages only when a `SecurityPolicy` is enforced (`security.enforce_authorization: true`). It is not yet enforced by default nor end to end across every ecosystem flow — that remains Phase 8 work.

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
- [C.O.R.E. v0.2 Phase 8](../systems/core.md#phase-8-security-integration)