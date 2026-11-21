# C.O.R.E. Client — external-device client

> [!NOTE] **Status:** v0.6.0 **IMPLEMENTED** (beta source). Split out of the former `CORE` monorepo into its own repository on 2026-11-21 (remote `Kishir298/CORE-CLIENT`). Stdlib-only by design: the client never imports the `core` host package. Verified: **225 passed / 1 skipped** (macOS Python 3.14, 2026-11-21; the skip is the `tkinter` GUI test, environment-dependent).

- **Repository:** `RISARMS/CORE-CLIENT/` — remote `https://github.com/Kishir298/CORE-CLIENT`
- **Distribution:** `core-client` (version `0.6.0`), `requires-python >= 3.10`, no runtime dependencies (optional extras: `test`, `monitoring`)
- **Console script:** `core-client` → `client.entrypoint:main`
- **Protocol compatibility:** wire protocol `0.4.0` (negotiated with the host; package versions track 0.6.0)
- **Counterpart:** [C.O.R.E. host](core.md) — this repository contains no server code

## What it is

The external-device client that connects a Mac / R.I.S.A.R.M.S. device to a running C.O.R.E. host over TCP+TLS: Option A login semantics (never imports `core`), device registration/presence, and a local presentation portal. Works offline: remote sections of the portal report `C.O.R.E. HOST OFFLINE` while local features stay usable.

## Layout

```text
CORE-CLIENT/
├── client/            package `client`
│   ├── core_device_client.py   stdlib external-device client (Option A login)
│   ├── entrypoint.py           `core-client` console entry point
│   ├── portal/                 client portal (default http://127.0.0.1:8766)
│   ├── desktop/                desktop launcher integration
│   ├── monitoring/             optional Prometheus/fastapi extras
│   ├── capabilities.py geo.py inference.py model_support.py models.py web.py
├── docs/               architecture, client-portal, setup, lan-testing, audit notes
├── desktop/            .desktop / start-core launchers, certificates/
├── runtime/            runtime artifacts
├── tests/              20 test files (225 passed / 1 skipped, 2026-11-21)
├── open-core.cmd .command        one-click launchers (Windows / macOS)
└── pyproject.toml      core-client 0.6.0
```

## Division of responsibility (host vs client)

| Concern | Owner |
|---|---|
| Server runtime, routing, services, scheduler, security infrastructure | `CORE-HOST` (`core` package) |
| External-device connection, Option A login, local portal, device-side presentation | `CORE-CLIENT` (`client` package) |
| Deployment, vendored services, release manifests, `risarms-host` CLI | `RISARMS-HOST` (umbrella) |

## CI

`.github/workflows/ci.yml` in `CORE-CLIENT` — Python 3.10–3.14 matrix, `ruff check --select E9,F,I client tests`, `pytest -q`. Cross-repo tests that need sibling checkouts are skipped when siblings are absent (documented in-repo).

## Related

- [C.O.R.E. host](core.md) — the host this client connects to
- [RISARMS-UI](risarms-ui.md) — the canonical desktop app that embeds this client as a sibling checkout
- [System Boundaries](../architecture/system-boundaries.md)
