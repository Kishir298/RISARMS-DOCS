# RISARMS-HOST — the umbrella repository

> [!NOTE] **Status:** v0.6.0 **IMPLEMENTED** (fresh repository created 2026-11-21, remote `Kishir298/RISARMS-HOST`). The `risarms-host` operator CLI, layout/compat/bundle checks, Void asset tests, pinned-revision staging, deterministic archive assembly, provenance generation and the server release workflow are **IMPLEMENTED**; physical-Void runtime validation remains **NOT YET PERFORMED**. Verified: **72 passed** (macOS Python 3.14, 2026-11-22) and CI green for Python 3.10–3.14.

- **Repository:** `RISARMS/RISARMS-HOST/` — remote `https://github.com/Kishir298/RISARMS-HOST`
- **Distribution:** `risarms-host` (version `0.6.0`, lockstep with `compatibility.json`), `requires-python >= 3.10`
- **Console script:** `risarms-host` → `risarms_host.cli:main`
- **Role:** release/deployment umbrella — it owns what used to live in the monorepo root: `deployment/`, `install/`, `services/`, `validation/`, release manifests, **server release orchestration** and operator docs. It contains no host (`core`) or client code; those live in [CORE-HOST](core.md) / [CORE-CLIENT](core-client.md).

## CLI

```text
risarms-host version      # umbrella + release version (lockstep with compatibility.json)
risarms-host components   # list workspace component checkouts
risarms-host doctor       # operator checks (exit 1 on failure)
risarms-host stage        # materialise the commits pinned in components.lock.json
risarms-host bundle       # assemble a release bundle (flat layout: CORE-HOST/, CORE-CLIENT/, services/, deployment/, compatibility.json, components.lock.json)
risarms-host provenance   # write the unsigned SLSA-shaped statement for release artifacts
```

`doctor --root .` runs `risarms_host.checks.run_checks` / `workspace_checks`; failures exit non-zero so CI and operators can gate on it.

## Layout

```text
RISARMS-HOST/
├── risarms_host/        package `risarms_host`
│   ├── __init__.py      __version__ = "0.6.0"
│   ├── __main__.py      python -m risarms_host
│   ├── cli.py           version / components / doctor / stage / bundle / provenance
│   ├── layout.py        Component model, workspace discovery, bundle/stage paths
│   ├── compat.py        compatibility.json load + validate (version lockstep)
│   ├── revisions.py     components.lock.json validation + pinned staging
│   ├── bundle.py        deterministic release bundle assembly (flat layout contract)
│   ├── provenance.py    unsigned SLSA-shaped build provenance
│   └── checks.py        operator + workspace checks
├── tests/               72 tests (CLI, layout, compat, bundle, revisions, provenance, Void assets)
├── deployment/          Void installer/services (runit, Caddy, nftables, storage guard, backup/restore, upgrade/rollback, diagnostics); legacy Pi assets retained historically
├── install/             release wheels (core, core-client, rescs) — historical 0.5.0 wheels
├── services/            release mirrors: ASIS, ASCS, RESCS, TIVISS-HOST (owning repos remain separate)
├── validation/          release evidence
├── scripts/             standalone operator scripts (e.g. run — smoke/doctor helpers)
├── docs/                operator docs (BUILDING, INSTALLATION, VALIDATION, RELEASES, SECURITY, ...)
├── compatibility.json   machine-readable component/source/version matrix (sources point at CORE-HOST/..., TIVISS-HOST/...)
├── components.lock.json exact commit of every component in a server release
├── RELEASE-MANIFEST.json  FROZEN historical record of release 0.5.0 (1046 sha256 entries, dated 2026-11-06) — never regenerate/rewrite
├── pyproject.toml       risarms-host 0.6.0
├── deployment/void/tests/container-install.sh   Void container install verification
└── .github/workflows/  ci.yml (matrix 3.10–3.14, bash -n, ruff E9,F,I, 3-OS CLI smoke)
                         release.yml (stage → assemble → verify install → draft release)
```

## Bundle layout contract

`risarms-host bundle` assembles a **flat** release bundle — `CORE-HOST/`, `CORE-CLIENT/`, `services/`, `deployment/`, `compatibility.json` at bundle root — so `deployment/void/install.sh` (`$SOURCE/CORE-HOST/core/web/portal.html`, `build_venv core "$SOURCE/CORE-HOST"`) works unchanged.

## Server release pipeline

`release.yml` is the **only** owner of CORE server releases. It stages the six
components from their own repositories at the commits in `components.lock.json`
(never from the `services/*` mirrors), assembles and re-assembles the archive to
prove byte identity, installs it with the shipped Void installer in a
`void-glibc-full` container, and uploads `SHA256SUMS`, `provenance.json` and a
CycloneDX SBOM. Tag pushes create a **draft** release; manual runs upload
artifacts only. Physical Void hardware validation stays out of scope for CI, and
no release is described as hardware-certified or signed.

## Independence rule

Owning sources are the standalone repos (`RESCS/`, `ASIS/`, `ASCS/`, `TIVISS-HOST/`); `RISARMS-HOST/services/*` holds release mirrors only — edits belong in the owning repo and are synced in (ADR [0001](../decisions/0001-rescs-independent-from-core.md), [0002](../decisions/0002-asis-independent-from-core.md)).

## Related

- [C.O.R.E. host](core.md), [C.O.R.E. client](core-client.md)
- [Development Contributions](../development/contribution.md) — directory forms after the split
- [Void Linux host](../development/void-linux.md) — deployment target
- ADR: [0011](../decisions/0011-void-linux-hp14-host.md)
