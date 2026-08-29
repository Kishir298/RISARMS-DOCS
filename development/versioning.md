# Versioning

> [!NOTE] **Status:** Versioning *policy* is defined here; the *practice* is still being harmonized. Current version markers are inconsistent (see below) — harmonization is C.O.R.E. v0.2 Phase 13 and an A.S.I.S. cleanup item.

## 1. Policy

- **SemVer** (`MAJOR.MINOR.PATCH`) for each system's own project, per [semver.org](https://semver.org/).
- **Each system versions independently** — C.O.R.E. 0.2.z, R.E.S.C.S. 0.1.z, A.S.I.S. 0.1.z can advance on their own cadence.
- **The ecosystem has no single version number**; a release refers to a matrix of component versions.
- **Breaking changes** to a [contract](../interfaces/communication.md) bump MAJOR (or the contract's own version) and require a [Decision Record](../decisions/README.md).

## 2. Where versions must agree (per system)

A version is only coherent when these agree:

| System | Authority locations |
|---|---|
| C.O.R.E. | `pyproject.toml`, `config/core.yaml`, CLI banner, docs |
| R.E.S.C.S. | `pyproject.toml`, package `__version__`, `SchemaManager.SCHEMA_VERSION`, README/CHANGELOG |
| A.S.I.S. | `pyproject.toml`, config defaults, docs |

## 3. Current discrepancies (known, tracked)

- **C.O.R.E.:** `pyproject.toml` = `0.1.0`; `config/core.yaml` + CLI banner = `0.2.0`. The v0.1→v0.2 transition is mid-flight; consolidation is Phase 13.
- **A.S.I.S.:** `pyproject.toml` = `0.1.0`; `core/config/defaults.py` = `2.0.0`; packaging name "asis" vs code branding "Forza". Tracked under the A.S.I.S. cleanup item ([roadmap.md](roadmap.md)).
- **R.E.S.C.S.:** consistent at `0.1.0`.

> [!IMPORTANT] **Rule for agents:** do not "fix" version markers as drive-by edits. Version alignment belongs to the owning system's release/cleanup phase. Note the discrepancy, don't change it arbitrarily.

## Related

- [Development Roadmap](roadmap.md)
- [Contribution](contribution.md)
- [Release phases](../systems/core.md#phase-13--v02-cleanupdocumentationrelease)