# Desktop Application Build and Release

> [!NOTE] **Status:** Build configuration and CI workflow are IMPLEMENTED.
> Artifacts are unsigned unless signing credentials are supplied. No signed
> release has been produced from this workspace.

## 1. Repository layout

```text
RISARMS-ui/
├── risarms_ui/          Tkinter application package
├── tests/               UI/HTTP/connection tests (no display required)
├── packaging/
│   ├── launcher.py      PyInstaller entry script
│   ├── risarms-ui.spec  one-directory bundle; .app on macOS
│   └── build.py         build, signing hooks, archives, SHA-256
└── .github/workflows/desktop-release.yml
```

## 2. Local development

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e ../CORE/CORE-CLIENT
.venv/bin/python -m pip install -e ".[test]"
.venv/bin/python -m pytest -q
.venv/bin/python -m risarms_ui --doctor
.venv/bin/python -m risarms_ui
```

Tkinter must be available for the GUI. The `--doctor` command checks Tk, the
display, keyring, websockets, core-client and writable application directories
without opening a window.

## 3. Packaging

```bash
python -m pip install -e ".[package]"
python packaging/build.py
```

Outputs:

| Platform | Artifact |
|---|---|
| macOS | `RISARMS-Portal-0.6.0-macos-<arch>.zip` containing `RISARMS Portal.app` |
| Windows | `RISARMS-Portal-0.6.0-windows-<arch>.zip` with `risarms-ui.exe` |
| Linux | `RISARMS-Portal-0.6.0-linux-<arch>.tar.gz` |

`dist/SHA256SUMS` records the archive digest.

### Signing hooks (optional)

| Variable | Effect |
|---|---|
| `RISARMS_SIGN_IDENTITY` | macOS Developer ID identity; otherwise ad-hoc signing |
| `RISARMS_NOTARY_PROFILE` | `xcrun notarytool` keychain profile; notarizes and staples |
| `RISARMS_SIGN_CERT` | Windows `.pfx` path |
| `RISARMS_SIGN_PASSWORD` | Windows certificate password |
| `RISARMS_TIMESTAMP_URL` | Windows RFC3161 timestamp server |

Never commit certificates, private keys, notarization profiles or passwords.

## 4. CI

`.github/workflows/desktop-release.yml` runs on manual dispatch and `v*` tags.
It checks out `Kishir298/CORE-HOST` as a sibling for the `core-client`
dependency, runs lint/tests/doctor, builds unsigned artifacts on macOS 13,
Windows and Ubuntu 22.04, and uploads them with checksums.

The workflow uses `main` for the CORE dependency by default. Release from a
matching CORE branch/tag only after the desktop control endpoints are merged.

## 5. Validation status

| Item | Status |
|---|---|
| Unit/contract tests | IMPLEMENTED |
| Tk GUI launch on macOS | Blocked in the authoring environment until Tk is installed |
| Physical Windows run | NOT YET PERFORMED |
| Physical Linux run | NOT YET PERFORMED |
| Signed/notarized artifacts | NOT YET PERFORMED (hooks only) |
| LAN reconnect/revocation testing | NOT YET PERFORMED on physical devices |

## Related

- [RISARMS-UI system specification](../systems/risarms-ui.md)
- [Cross-platform release engineering](cross-platform-release.md)
- [Hardware-gated validation](hw-gated-validation.md)
