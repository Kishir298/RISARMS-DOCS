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

Installer generation is **implemented but unverified**. The recovery host has
no Tk-enabled Python, so no DMG was produced locally. Treat the first successful
CI draft run as the verification event and record draft artifact hashes here.
macOS remains ad-hoc signed and unnotarized; Windows remains unsigned; public
distribution stays gated on signing credentials.
