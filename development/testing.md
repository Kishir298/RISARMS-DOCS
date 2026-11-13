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
| CORE-HOST | **865 passed / 1 skipped** (2026-11-13, macOS Python 3.14, v0.5.0) | Host spine + desktop control channel; run `.venv/bin/python -m pytest` in `CORE/CORE-HOST` |
| CORE-CLIENT | **189 passed / 1 skipped** (2026-11-13, macOS Python 3.14, v0.5.0) | Native client + portal; run `python3 -m pytest` in `CORE/CORE-CLIENT` |
| R.E.S.C.S. | **314 passed / 4 skipped** (2026-11-13, macOS Python 3.14, v0.4.0) | Live PostgreSQL/S3 skipped without credentials; run `.venv/bin/python -m pytest` |
| A.S.I.S. | **941 passed / 24 skipped** (2026-11-09, macOS Python 3.12, v0.1.0) | Pi policy and release contract included |
| A.S.C.S. | **991 passed / 6 skipped** (2026-11-09, macOS Python 3.12, v0.3.0) + opt-in live suite | Pi policy tests mock the Linux guard; live gated `RISALIVE=1` |
| T.I.V.I.S.S. | **285 passed** (2026-11-13, macOS Python 3.14, v0.2.0) | Failure-first checks, atomic handover, bounded events; desktop registration metadata included |
| RISARMS-UI | **205 passed** (2026-11-13, macOS Python 3.14, v0.6.0) | UI, HTTP client, connection manager and migrated CORE-CLIENT desktop tests; GUI launch pending Tk installation | 

All run via `pytest -q` from their own roots — never from `RISARMS/` root (no root suite). The release authors' Linux x86_64 run reported CORE-HOST 840 passed; the one-test difference is platform-specific. Hardware/cloud-gated validations (physical Pi/ARM64, LAN, live S3/PG, endurance, live voice/model) have their own runbook: [hw-gated-validation.md](hw-gated-validation.md). The full Pi release evidence is in [pi-release-2026-11-06.md](pi-release-2026-11-06.md).

## 3. What is missing (PLANNED)

- **Deployed cross-host integration spine**: C.O.R.E. ↔ R.E.S.C.S. ↔ devices exercised over a physical network (the software-side spine is covered; physical LAN validation is pending).
- **Physical Raspberry Pi/ARM64 deployment**: cgroup v2, systemd boot, `/srv/core` mount, SSD removal, and the Pi installer are not exercised in this workspace.
- **24/7 endurance tests** for C.O.R.E. on the Windows host.
- **Live-cloud tests** for R.E.S.C.S. against real PostgreSQL/Supabase/S3 (PostgreSQL compatibility is already integration-tested).
- **A.S.I.S. ↔ C.O.R.E. contract tests** — blocked until that integration exists.

> [!IMPORTANT] **Hardware/cloud-gated items are BLOCKED, not bugs** — every item above
> (plus live voice/model runs and T.I.V.I.S.S. re-verification) requires physical
> hardware, network, or credentials unavailable in this workspace. Per-item blockers
> are listed in [hw-gated-validation.md](hw-gated-validation.md) §"Current status";
> they stay closed until the resource appears.

## 4. Test naming and location conventions

- Unit tests live beside the subsystem they cover (`tests/<subsystem>/`).
- Integration tests live under `tests/integration/`.
- A test that touches two systems is a *contract test* and belongs to the joint contract spec, not to either system's unit suite.

## Related

- [Development Roadmap](roadmap.md)
- [C.O.R.E. test coverage](../systems/core.md#5-test-coverage)
- [Contribution](contribution.md)
