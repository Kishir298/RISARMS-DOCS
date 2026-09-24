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
| CORE-HOST | 52 test files; **723 passed** (2026-09-24, pytest, v0.4.0) | Host spine; run `py -m pytest` in CORE-HOST |
| CORE-CLIENT | **123 passed** (2026-09-24, 13 files, v0.4.0) | Client + portal; run `py -m pytest` in CORE-CLIENT |
| R.E.S.C.S. | Comprehensive unit + API + integration suite, **308 passed / 4 skipped** (2026-09-24) | Bounded chunk intake, LIKE-escape, S3 close; run `.venv/bin/python -m pytest` |
| A.S.I.S. | 56 files / **812 collected, EXIT 0** (2026-09-24, .venv py3.12) | Rebuilt `asis` + `asis/identities` + `/identity` CLI |
| A.S.C.S. | **957 collected, EXIT 0** (2026-09-24, offline) + opt-in live suite | `.ascs` guards + UI token; live gated `RISALIVE=1` |
| T.I.V.I.S.S. | **254 passed** (2026-09-23) | Failure-first checks, atomic handover, bounded events |

All run via `pytest -q` from their own roots — never from `RISARMS/` root (no root suite; root `.pytest_cache/` deleted). Counts drift between docs (e.g. ASCS 943 vs 949 vs 951; ASIS 693 vs 789) — re-verify with `pytest -q` in each repo; do not treat hardcoded counts as authoritative. Portal suites included in host/client counts.

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
