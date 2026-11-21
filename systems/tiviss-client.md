# T.I.V.I.S.S. Client — client library scaffold

> [!NOTE] **Status:** v0.1.0 **Scaffold** (fresh repository created 2026-11-21, remote `Kishir298/TIVISS-CLIENT`). The CLI shell (`version`, `doctor`) and project scaffolding are **IMPLEMENTED**; transport, protocol and security layers are **PLANNED** and must not be described as built. Verified: **5 passed** (macOS Python 3.14, 2026-11-21).

- **Repository:** `RISARMS/TIVISS-CLIENT/` — remote `https://github.com/Kishir298/TIVISS-CLIENT`
- **Distribution:** `tiviss-client` (version `0.1.0`), `requires-python >= 3.10`, stdlib-only (no runtime dependencies)
- **Console script:** `tiviss-client` → `tiviss_client.cli:main`
- **Counterpart:** [T.I.V.I.S.S. host](tiviss.md) — v0.2.0 host runtime in `TIVISS-HOST/`

## What exists today (v0.1.0)

- `tiviss_client/cli.py` — argparse CLI with:
  - `version` — prints the package version
  - `doctor [--root PATH]` — environment/self check; verifies the host checkout is a sibling when `--root` points at the workspace
- `tiviss_client/__main__.py` — `python -m tiviss_client`
- `tests/test_cli.py` — 5 tests covering version output, argparse wiring, doctor behavior
- `pyproject.toml` — setuptools build, `[project.scripts] tiviss-client`, ruff config (`target-version = py310`, `E9,F,I` on `tiviss_client tests`)
- `.github/workflows/ci.yml` — Python 3.10–3.14 matrix + CLI smoke (`tiviss-client version`, `tiviss-client doctor`)
- `README.md`, `LICENSE` (MIT), `.gitignore`

## Planned (not implemented — do not describe as built)

| Layer | Intent |
|---|---|
| Transport | stdlib `socket`/`ssl` client transport mirroring the host's `core_tcp` / `rescs_http` abstractions |
| Protocol | versioned message framing compatible with `TIVISS-HOST` v0.2 (protocol negotiation deferred until implemented) |
| Security | integration with the TIVISS-owned security protocol (Wave A–D scope in the parent plan; client distribution will pin `TIVISS-HOST` protocol version) |
| Client library | programmatic client API for external devices (analogous to `CORE-CLIENT`'s `client` package) |

Version-lockstep rule (same as CORE): when the security protocol lands, `tiviss-client` pins the published protocol version rather than inventing its own.

## Layout

```text
TIVISS-CLIENT/
├── tiviss_client/        package `tiviss_client`
│   ├── __init__.py       __version__ = "0.1.0"
│   ├── __main__.py       python -m tiviss_client
│   └── cli.py            version / doctor subcommands
├── tests/
│   ├── __init__.py
│   └── test_cli.py       5 tests
├── pyproject.toml        tiviss-client 0.1.0, >=3.10, console script
├── README.md LICENSE .gitignore
└── .github/workflows/ci.yml
```

## Related

- [T.I.V.I.S.S. host](tiviss.md) — the host runtime this client will talk to
- [C.O.R.E. client](core-client.md) — the analogous implemented client (reference architecture)
- [System Boundaries](../architecture/system-boundaries.md)
