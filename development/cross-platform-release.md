# Cross-Platform Standalone Release Engineering

Status as of 2026-11-16. CORE 0.6.0 releases a Void Linux x86_64 server bundle;
RISARMS-ui releases desktop artifacts for macOS Intel/Apple Silicon, Windows
x86_64 and Linux x86_64. R.E.S.C.S., A.S.I.S., A.S.C.S. and T.I.V.I.S.S. retain
their own pipelines.

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

CORE server releases are owned by **RISARMS-HOST**
(`RISARMS-HOST/.github/workflows/release.yml`). CORE-HOST no longer builds or
publishes server releases; it only runs its own test CI.

- Triggers on `vX.Y.Z` / `vX.Y.Z-beta.N` tags and manual dispatch.
- Validates tag/version/`compatibility.json`/`components.lock.json` agreement
  and the Void x86_64 target before building.
- Stages `CORE-HOST`, `CORE-CLIENT`, `RESCS`, `ASCS`, `ASIS` and `TIVISS-HOST`
  from their owning repositories at the exact commits pinned in
  `components.lock.json`, then runs the umbrella and deployment suites.
- Assembles `CORE-Server-<version>-void-x86_64.tar.gz` deterministically
  (sorted entries, normalised ownership, `SOURCE_DATE_EPOCH`) and re-assembles
  it to prove the bytes are identical.
- Installs the archive with the shipped Void installer in a
  `ghcr.io/void-linux/void-glibc-full` container and asserts the installed
  venvs import. This is container evidence, not hardware certification.
- Emits `SHA256SUMS`, an unsigned SLSA-shaped `provenance.json` and a
  CycloneDX SBOM of the build environment.
- Creates a **draft** GitHub release for tags, prerelease for beta, without
  publishing automatically. Manual runs upload artifacts only.

RISARMS-ui `.github/workflows/desktop-release.yml`:

- Runs tests and packaging on `macos-15-intel`, `macos-15`, `windows-2022` and
  `ubuntu-24.04`.
- Builds unsigned/ad-hoc beta desktop archives and native installers, unique
  per-platform checksums and SBOMs.
- Requires `UPDATE_PUBLIC_KEY` for a production build and `UPDATE_SIGNING_KEY`
  to sign `update.json`; without the signing key the release job refuses to
  create an unsigned manifest. A `workflow_dispatch` run with
  `validation_build=true` generates an ephemeral update key and marks its
  artifacts non-publishable so installers can still be validated.
- Creates a **draft** release for tags, and never publishes automatically.

Other repositories retain their own release workflows; do not assume the CORE
Void bundle is a cross-platform server binary.

## Artifact naming

`<SYSTEM>-<version>-<os>-<arch>-<format>` and, for CORE,
`CORE-Server-<version>-void-x86_64-<format>`.

Formats: `.zip` (Windows), `.tar.gz` (macOS/Linux/source), `.dmg`, `.exe`, `.msi`,
`.deb`, `.AppImage`, `.whl`, sdist.

## Supported platform matrix

| System | OS | Architectures | Notes |
| --- | --- | --- | --- |
| CORE server | Void Linux | x86_64, glibc, runit | HP 14 reference machine; release target |
| RISARMS-ui | macOS | x86_64, arm64 | Ad-hoc signed, unnotarized beta |
| RISARMS-ui | Windows | x86_64 | Unsigned beta |
| RISARMS-ui | Linux | x86_64 | Includes a pending Void glibc smoke test |

CORE-CLIENT remains a legacy protocol client on Windows/macOS/Linux; it is not a
CORE 0.6.0 server release target. iOS TestFlight and Android beta distribution
are future work. PowerShell 5.1 and cmd.exe are sufficient on Windows; WSL,
Windows Terminal, winget and Bash are not required.

## Validation level definitions

1. **Compiled** — source compiles/imports.
2. **Packaged** — wheels and executables produced by the workflow.
3. **Installed command** — console script or frozen binary runs from an
   unrelated working directory (`platform-smoke` CI jobs).
4. **Runtime tested** — the subsystem's test suite passes on that OS.
5. **Container installed** — for the CORE server only: the shipped Void
   installer completes in a Void glibc container and the installed venvs import.
6. **Hardware validated** — actually exercised on that OS/architecture.

Claims in subsystem docs must state which level applies. This workspace can
only verify levels 1–4 for macOS locally; levels 2–4 for Windows/Linux are CI
claims; level 5 is **not** claimed anywhere except the Pi deployments that
already documented hardware runs.

## Known limitations

- CORE server artifacts are source release archives for Void; they are not
  server binaries and are not code-signed.
- macOS desktop artifacts are ad-hoc signed and unnotarized unless Developer ID
  and notarization credentials are configured.
- Windows desktop artifacts are unsigned unless a code-signing certificate is
  configured.
- Native installers are generated by the desktop workflow; their validation
  status is recorded in [installers.md](installers.md) and
  [implementation-status.md](implementation-status.md).
- Public signed auto-updates remain gated on a production Ed25519 public key
  fingerprint. A validation build uses a throwaway key and is not an update
  channel.
- Windows ARM64 CORE jobs were removed with the Void-only server change;
  RISARMS-ui targets Windows x86_64.
- Executables must be built per OS/architecture (PyInstaller cannot
  cross-compile).
- GitHub Actions runs are now dispatched from this workspace through an
  authenticated `gh` client; CI success is not the same as artifact or runtime
  evidence, so record the run id and result for any claim.
- `macos-13` and `macos-14` runners are retired/retiring; the desktop workflow
  uses `macos-15-intel` for Intel and `macos-15` for Apple Silicon. These labels
  still need confirmation from the first real CI run.
