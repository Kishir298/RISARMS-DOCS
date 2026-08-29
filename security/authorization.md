# Authorization

> [!NOTE] **Status:** **PLANNED** (foundation only). C.O.R.E. has authorization/permission primitives; end-to-end enforcement on operations is part of v0.2 Phase 8.

## 1. Definition

Authorization answers: *"Given a proven identity, what may this actor do?"* It sits between **authentication** and **permission checking**.

## 2. Current reality

- **C.O.R.E.** `SecurityManager` exposes `authorize` and permission checks, with `IdentityType` and `Permission` primitives. These are implemented and usable in-process.
- Permissions are **not yet enforced** end to end across the ecosystem flow (routing → service execution), which is Phase 8 work.

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
- [C.O.R.E. v0.2 Phase 8](../systems/core.md#phase-8--security-integration)