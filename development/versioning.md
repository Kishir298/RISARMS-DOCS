# Versioning

> [!NOTE] **Status:** Versioning *policy* is defined here; the *practice* is now mostly harmonized. C.O.R.E. and R.E.S.C.S. are internally consistent; A.S.I.S. still carries minor drift, and A.S.C.S. distribution/package naming differs intentionally.

## 1. Policy

- **SemVer** (`MAJOR.MINOR.PATCH`) for each system's own project, per [semver.org](https://semver.org/).
- **Each system versions independently** — C.O.R.E. 0.3.z, R.E.S.C.S. 0.3.z, A.S.I.S. 0.1.z, A.S.C.S. 0.3.z can advance on their own cadence.
- **The ecosystem has no single version number**; a release refers to a matrix of component versions.
- **Breaking changes** to a [contract](../interfaces/communication.md) bump MAJOR (or the contract's own version) and require a [Decision Record](../decisions/README.md).
- C.O.R.E. additionally maintains an explicit **protocol-version negotiation** layer (`core/version.py`): supported versions `0.2.0`/`0.2.1`/`0.3.0`, with legacy clients kept working by design.

## 2. Where versions must agree (per system)

A version is only coherent when these agree:

| System | Authority locations |
|---|---|
| C.O.R.E. | `pyproject.toml`, `core/version.py`, `config/core.yaml`, CLI banner, docs |
| R.E.S.C.S. | `pyproject.toml`, package `__version__`, `SchemaManager.SCHEMA_VERSION`, README/CHANGELOG |
| A.S.I.S. | `pyproject.toml`, `asis/__init__.py`, config settings, docs |
| A.S.C.S. | `pyproject.toml`, package docstring/docs |

## 3. Current version matrix (verified)

| System | Version | Consistency |
|---|---|---|
| **C.O.R.E.** | `0.3.0` | Consistent (pyproject, version module, config) |
| **R.E.S.C.S.** | `0.3.0` | Consistent (pyproject + CHANGELOG) |
| **A.S.I.S.** | `0.1.0` | Consistent for the new `asis` package; deprecated legacy trees are not versioned |
| **A.S.C.S.** | `0.3.0` | Consistent; note distribution name `coding-agent` vs package `agent` vs command `risa` |

## 4. Known, accepted quirks (tracked)

- **A.S.I.S.** legacy trees (`core/`, `02_voice/`) are unversioned deprecated remnants still present in the working tree — do not treat their internals as part of the current 0.1.0 package.
- **A.S.C.S.** naming spread (`coding-agent` / `agent` / `risa`) is a distribution-name choice, not a version conflict.
- **C.O.R.E.** keeps `0.2.x` behavior reachable through negotiation — that is compatibility, not version inconsistency.

> [!IMPORTANT] **Rule for agents:** do not "fix" version markers as drive-by edits. Version alignment belongs to the owning system's release/cleanup phase. Note the discrepancy, don't change it arbitrarily.

## Related

- [Development Roadmap](roadmap.md)
- [Contribution](contribution.md)
