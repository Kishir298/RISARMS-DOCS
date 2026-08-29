# Testing

> [!NOTE] **Status:** Each system has its own test suite (below). A cross-system integration spine is **PLANNED** (C.O.R.E. Phase 12). Test *policy* is defined here.

## 1. Testing principles

1. **Every major integration is testable independently** — contract-first integration means a system can be tested against a fake/stubbed peer.
2. **Behavioral contracts are tested** — message envelope, routing, service invocation, errors ([interfaces](../interfaces/communication.md)).
3. **Failures are tested, not just happy paths** — unknown routes, failing handlers, unauthorized access, transport failure.
4. **No integration is "tested by running the demo."** Automated tests are the bar.
5. **Round-trip fidelity** — serialization and message correlation are asserted in tests, not assumed.

## 2. Current suites (verified)

| System | Suite | Notes |
|---|---|---|
| C.O.R.E. | 22 files / 259 test functions (pytest) | Mirrors `core/` subsystems; includes application orchestration, events, health, routing→service integration |
| R.E.S.C.S. | Unit + API tests (pytest, TestClient) | Config, errors, health, domain, models, schemas, both repository backends, db layer, health routes |
| A.S.I.S. | Empty (`tests/`) | Voice smoke test exists at `02_voice/test_cross_platform.py`; not pytest-integrated |

C.O.R.E. and R.E.S.C.S. both run via `pytest` from their own roots.

## 3. What is missing (PLANNED)

- C.O.R.E. **full integration test spine** (Phase 12): start → configure → send → route → execute → (adapter persist) → respond → health reflects activity → clean stop.
- R.E.S.C.S. integration tests (`tests/integration/` empty).
- Cross-system contract tests (adapter ↔ R.E.S.C.S. API).
- A.S.I.S. automated tests.

## 4. Test naming and location conventions

- Unit tests live beside the subsystem they cover (`tests/<subsystem>/`).
- Integration tests live under `tests/integration/`.
- A test that touches two systems is a *contract test* and belongs to the joint contract spec, not to either system's unit suite.

## Related

- [Development Roadmap](roadmap.md)
- [C.O.R.E. test coverage](../systems/core.md#5-test-coverage)
- [Contribution](contribution.md)