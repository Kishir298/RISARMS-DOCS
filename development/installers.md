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
| `RISARMS-Portal-<ver>-macos-<arch>.zip` | macOS archive |
| `RISARMS-Portal-<ver>-macos-<arch>.dmg` | macOS installer |
| `RISARMS-Portal-<ver>-windows-<arch>.zip` | Windows archive |
| `RISARMS-Portal-<ver>-windows-<arch>-setup.exe` | Windows installer |
| `RISARMS-Portal-<ver>-windows-<arch>.msi` | Windows MSI |
| `RISARMS-Portal-<ver>-linux-<arch>.tar.gz` | Linux archive |
| `risarms-portal_<ver>_<arch>.deb` | Debian package |
| `RISARMS-Portal-<ver>-linux-<arch>.AppImage` | AppImage |
| `SHA256SUMS` | Checksums for every artifact above |

## 3. CI

`.github/workflows/desktop-release.yml` runs on `workflow_dispatch` and on `v*`
tags. It pins the CORE-CLIENT source commit, installs Tk and the packaging
tools, runs the test suite, runs `python -m risarms_ui --doctor`, builds, and
uploads the artifacts. Signing credentials are supplied only through CI secrets
and are never committed.

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

Installer generation is **implemented but unverified**. The recovery host had no
Tk-enabled Python, so no DMG was produced. Treat the first successful CI run as
the verification event and record the artifact hashes here.
