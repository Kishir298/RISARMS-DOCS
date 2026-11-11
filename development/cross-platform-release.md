# Cross-Platform Standalone Release Engineering

Status as of 2026-11-11. Applies to C.O.R.E. (host + client), R.E.S.C.S.,
A.S.I.S. and A.S.C.S. T.I.V.I.S.S. is unchanged by this work.

## Model

Each subsystem is an **independent repository** with its own version, history,
tag namespace (`vX.Y.Z` per repo) and release pipeline. CORE integration is
optional for every other component; no component requires CORE, a Raspberry
Pi or another subsystem to start.

Shared rules:

- Package versions follow `MAJOR.MINOR.PATCH`; a version tag must match the
  package metadata and the machine-readable manifest.
- CORE's wire protocol version is independent of its package version.
- Releases are built on native runners; no cross-compilation.

## Installable commands

| Repository | Commands | Setup / diagnostics |
| --- | --- | --- |
| CORE | `core-host`, `core-client` | `core-host setup`, `core-host doctor`, `core-client setup`, `core-client doctor` |
| RESCS | `rescs` | `rescs setup`, `rescs doctor` |
| ASIS | `asis`, `asis-tui` | `asis setup`, `asis doctor` |
| ASCS | `ascs`, `risa` (alias) | `ascs setup`, `ascs doctor`, `--doctor`, `--check` |

`setup` is always offline and never overwrites existing configuration.
`doctor` is read-only and never mutates workspace or state.

## Manifests

`compatibility.json` at the root of each repository declares name, version,
status, supported platforms (with minimum OS and architecture), runtime
versions and integration status. Tests in each repository assert that the
manifest version matches the package version.

CORE additionally declares `protocol_version` and `protocol_compatibility`.

## Release pipelines

Each repository has `.github/workflows/release.yml`:

- Triggers: push tag `v*`, plus `workflow_dispatch` with channel
  `stable|beta|development`.
- Validates tag/version/manifest agreement before building.
- Builds a Python wheel and sdist.
- Builds standalone executables on native runners: Windows x64, Windows ARM64
  (experimental), macOS Intel, macOS ARM64, Linux x64, Linux ARM64.
- Writes `SHA256SUMS` and a CycloneDX JSON SBOM.
- Publishes a GitHub Release for tags (prerelease for `-beta.N`), and only
  uploads artifacts for manual runs.
- The publish job requires every build job to succeed.

CORE additionally publishes a Linux server bundle (`install-server.sh` +
`core.service`).

## Artifact naming

`<SYSTEM>-<version>-<os>-<arch>-<format>` and, for CORE,
`CORE-<Host|Client|Server>-<version>-<os>-<arch>-<format>`.

Formats: `.zip` (Windows), `.tar.gz` (macOS/Linux), `.whl`, sdist.

## Supported platform matrix

| OS | Architectures | Minimum declared |
| --- | --- | --- |
| Windows | x86_64, arm64 | Windows 10 22H2 |
| macOS | x86_64, arm64 | macOS 12 |
| Linux | x86_64, arm64 | glibc 2.28 |

PowerShell 5.1 and cmd.exe are sufficient on Windows; WSL, Windows Terminal,
winget and Bash are not required.

## Validation level definitions

1. **Compiled** — source compiles/imports.
2. **Packaged** — wheels and executables produced by the workflow.
3. **Installed command** — console script or frozen binary runs from an
   unrelated working directory (`platform-smoke` CI jobs).
4. **Runtime tested** — the subsystem's test suite passes on that OS.
5. **Hardware validated** — actually exercised on that OS/architecture.

Claims in subsystem docs must state which level applies. This workspace can
only verify levels 1–4 for macOS locally; levels 2–4 for Windows/Linux are CI
claims; level 5 is **not** claimed anywhere except the Pi deployments that
already documented hardware runs.

## Known limitations

- Windows ARM64 jobs are marked experimental (`continue-on-error`) because
  dependency wheels are less complete than x64.
- macOS artifacts are unsigned unless signing secrets are configured; this is
  stated in each repository's `RELEASES.md`.
- No MSI/DMG/`.deb`/RPM installers are produced; portable archives and wheels
  are the supported formats.
- Executables must be built per OS/architecture (PyInstaller cannot
  cross-compile).
- GitHub Actions cannot be executed in this local workspace; workflow validity
  is established by YAML parsing and by local PyInstaller builds of the same
  entry scripts.
- Workflow runner labels such as `macos-15-intel`, `windows-11-arm` and
  `ubuntu-24.04-arm` are assumptions until the first CI run confirms them.
