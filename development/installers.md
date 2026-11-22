# Desktop Installer Creation

The desktop application is packaged with PyInstaller and then wrapped by each
platform's native installer tool. `packaging/build.py` drives both stages;
`packaging/installers.py` contains the native builders.

## 1. Prerequisites

| Platform | Required | Purpose |
|---|---|---|
| All | Python 3.10+ **with Tk** | The application cannot open a window without `_tkinter` |
| All | `pip install -e ".[test,package]"` | PyInstaller and test tooling |
| macOS | `hdiutil` (built in) | DMG |
| Linux | `dpkg-deb` (`dpkg-dev`, `fakeroot`) | DEB |
| Linux | `appimagetool` (optional) | AppImage |
| Windows | Inno Setup (`iscc`) | EXE installer |
| Windows | WiX (`heat`, `candle`, `light`) | MSI installer |

A build **never** claims an artifact it did not produce: a missing tool skips
that format with an explicit message, and a missing Tk aborts the build with
exit code 2.

## 2. Build

```bash
python packaging/build.py
```

Outputs land in `dist/`:

| Artifact | Platform |
|---|---|
| `RISARMS-Portal-<ver>-macos-{x86_64,arm64}.zip` | macOS archive |
| `RISARMS-Portal-<ver>-macos-{x86_64,arm64}.dmg` | macOS installer |
| `RISARMS-Portal-<ver>-windows-x86_64.zip` | Windows archive |
| `RISARMS-Portal-<ver>-windows-x86_64-setup.exe` | Windows installer |
| `RISARMS-Portal-<ver>-windows-x86_64.msi` | Windows MSI |
| `RISARMS-Portal-<ver>-linux-x86_64.tar.gz` | Linux archive |
| `risarms-portal_<ver>_amd64.deb` | Debian package |
| `RISARMS-Portal-<ver>-linux-x86_64.AppImage` | AppImage |
| `SHA256SUMS-<platform>` | Per-platform checksums for the artifacts above |
| `sbom-<platform>.cdx.json` | Per-platform CycloneDX SBOM |

## 3. CI

`.github/workflows/desktop-release.yml` runs on `workflow_dispatch` and on `v*`
tags. It validates the tag against project metadata, installs Tk and the
packaging tools, runs the test suite, verifies Tk importability, embeds the
update public key, builds, and uploads unique per-platform artifacts. Tagged
runs verify checksums, merge SBOMs, sign `update.json`, and create a **draft**
release; manual runs do not publish. Signing credentials are supplied only
through CI secrets and are never committed.

## 4. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `Tk is required to package…` (exit 2) | Python built without `_tkinter` | Install `python-tk` (Homebrew) or `python3-tk` (Debian) |
| `hdiutil is unavailable` | Not on macOS | Build the DMG on macOS |
| `dpkg-deb is unavailable` | Missing `dpkg-dev` | `sudo apt-get install dpkg-dev fakeroot` |
| `Inno Setup (iscc) is unavailable` | Tool absent | Install Inno Setup and put `iscc` on `PATH` |
| `WiX (candle/light) is unavailable` | Tool absent | Install the WiX toolset |
| App opens then closes | Missing runtime dependency | Run `risarms-ui --doctor` from the extracted directory |

## 5. Current validation state

Installer generation is **implemented and produced in CI**. The recovery host
has no Tk-enabled Python, so nothing is built locally; the workflow is the
verification environment.

Build run: [RISARMS-ui desktop-release 45012833473](https://github.com/Kishir298/RISARMS-ui/actions/runs/45012833473)
(`main` @ `18c38aa`, `workflow_dispatch` with `validation_build=true`). All five
jobs passed.

Install verification: [desktop-smoke 45013788806](https://github.com/Kishir298/RISARMS-ui/actions/runs/45013788806).
The published checksums re-verified, the `.deb` installed with its dependencies,
the installed binary reported `Tk 8.6` with a real display under Xvfb, the GUI
stayed up for the full 20 s timeout, and the messaging end-to-end test passed
against a real CORE server at the pinned revision. The runner has no
SecretService, so `--doctor` correctly reports `not ready: keyring` there.

| Platform | Artifacts produced | Checksums |
|---|---|---|
| macOS Intel | `RISARMS-Portal-0.6.0-macos-x86_64.zip`, `.dmg` | `SHA256SUMS-macos-x86_64` written |
| macOS Apple Silicon | `RISARMS-Portal-0.6.0-macos-arm64.zip`, `.dmg` | `SHA256SUMS-macos-arm64` written |
| Windows x86_64 | `.zip`, `-setup.exe` (Inno Setup 6.7), `.msi` (WiX 3.14) | `SHA256SUMS-windows-x86_64` written |
| Linux x86_64 | `.tar.gz`, `risarms-portal_0.6.0_amd64.deb` | `sha256sum -c` OK in CI |

Each platform also uploaded `sbom-<platform>.cdx.json` (CycloneDX 1.5) and a
`SHA256SUMS-<platform>` file. The Linux set was re-verified in CI by the smoke
run; installing the macOS and Windows installers remains unverified.

The desktop workflow found five real packaging defects across its runs, all
now fixed (four covered by unit tests): the PyInstaller spec resolved
`launcher.py` outside `packaging/`; the WiX build compiled only the harvested
fragment; Inno Setup 6 wrote to `dist/Output` instead of `dist/`; and checksum
files were written with CRLF line endings, which broke `sha256sum -c` elsewhere.
The Windows job had also reported success while `build.py` crashed, because a
`pwsh` step propagates only the last command's exit code; the build step now
runs under `bash` with `pipefail`. The fifth was found only by installing the
Linux artifact: it died with `No module named '_struct'` because
`actions/setup-python` exported `LD_LIBRARY_PATH` to its own libpython while the
Linux build created its venv from `/usr/bin/python3` for Tk support, so
PyInstaller mixed two Python 3.12 toolchains. Linux now uses only the
distribution Python, and `build.py` runs the frozen executable with `--version`
so an unstartable bundle fails the build.

### Signing status (deliberately unsigned)

- **Update signing is separate from OS code signing.** The workflow signs
  `update.json` with `UPDATE_SIGNING_KEY`; no such secret is configured, so no
  update manifest is produced and nothing claims signed auto-updates.
- `UPDATE_PUBLIC_KEY` is not configured either. This validation run therefore
  used an ephemeral Ed25519 key (fingerprint
  `f68e30260bf7927776abf9ab26031d2cd73ad5dc4674c3b1a0e3f88328401320`), and every
  artifact set carries a `RISARMS-Portal-VALIDATION-ONLY-<platform>.txt` notice
  saying it must not be distributed.
- macOS builds are ad-hoc signed only (no Developer ID, not notarized);
  Windows builds are unsigned. These are Apple/Microsoft OS-signing gaps, not
  update-key gaps, and neither has been resolved.
- Nothing from this run was published: the release job is tag-gated and skipped.
