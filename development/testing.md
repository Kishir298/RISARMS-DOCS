# Testing

> [!NOTE] **Status:** Every active system has a real test suite. A cross-system (deployed) integration spine is still **PLANNED** — automated contract tests exist on both sides of the C.O.R.E. ↔ R.E.S.C.S. boundary, but no deployed multi-host suite runs. Test *policy* is defined here.

## 1. Testing principles

1. **Every major integration is testable independently** — contract-first integration means a system can be tested against a fake/stubbed peer.
2. **Behavioral contracts are tested** — message envelope, routing, service invocation, errors ([interfaces](../interfaces/communication.md)).
3. **Failures are tested, not just happy paths** — unknown routes, failing handlers, unauthorized access, transport failure.
4. **No integration is "tested by running the demo."** Automated tests are the bar.
5. **Round-trip fidelity** — serialization and message correlation are asserted in tests, not assumed.

## 2. Current suites (verified)

| System | Suite | Notes |
|---|---|---|
| C.O.R.E. | 50 test files approx; README-documented result **689 passed** (pytest) | Covers orchestration, communication/TLS/framing, protocol negotiation, auth, device registration/persistence/reconnect, discovery, routing, services, organization/reconciliation, adapters, scheduler, data distribution, health, events, 0.2.x compatibility |
| R.E.S.C.S. | Comprehensive unit + API + integration suite (pytest, httpx TestClient) | Includes API, security, rate limiting, observability, lifecycle, quotas, concurrency, backups, PostgreSQL compatibility, contract-consumer tests |
| A.S.I.S. | 42 files / 693 passed (pytest) + voice tests | Covers the rebuilt `asis` package |
| A.S.C.S. | 949 passed / 6 skipped + opt-in live suite | Live Ollama tests gated behind `RISALIVE=1`, skipped by default; cross-platform dev testing, Windows-only runtime |
| T.I.V.I.S.S. | 14 files / offline deterministic suite (pytest) | Covers identity, ownership, conversation, memory, models, permissions, tools, events, handover, config + CORE/RESCS mock adapters; no external services |

All five run via `pytest` from their own roots. Counts drift as development continues — verify against the current checkout rather than trusting any documented number.

## 3. What is missing (PLANNED)

- **Deployed cross-host integration spine**: C.O.R.E. ↔ R.E.S.C.S. ↔ devices exercised over a physical network (the software-side spine is covered; physical LAN validation is pending).
- **24/7 endurance tests** for C.O.R.E. on the Windows host.
- **Live-cloud tests** for R.E.S.C.S. against real PostgreSQL/Supabase/S3 (PostgreSQL compatibility is already integration-tested).
- **A.S.I.S. ↔ C.O.R.E. contract tests** — blocked until that integration exists.

## 4. Test naming and location conventions

- Unit tests live beside the subsystem they cover (`tests/<subsystem>/`).
- Integration tests live under `tests/integration/`.
- A test that touches two systems is a *contract test* and belongs to the joint contract spec, not to either system's unit suite.

## Related

- [Development Roadmap](roadmap.md)
- [C.O.R.E. test coverage](../systems/core.md#5-test-coverage)
- [Contribution](contribution.md)
