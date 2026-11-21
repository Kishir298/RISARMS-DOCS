# Desktop Application Build and Release

> [!NOTE] **Status:** Build configuration and draft-only CI workflow are
> IMPLEMENTED. Beta artifacts are unsigned on Windows and ad-hoc-signed,
> unnotarized on macOS unless signing credentials are supplied. No signed or
> public release has been produced from this workspace. Public distribution and
> signed auto-updates remain gated.

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
.venv/bin/python -m pip install -e ../CORE-CLIENT
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
| macOS | `RISARMS-Portal-0.6.0-macos-{x86_64,arm64}.zip` containing `RISARMS Portal.app`, plus `.dmg` |
| Windows | `RISARMS-Portal-0.6.0-windows-x86_64.zip` with `risarms-ui.exe`, plus `.exe`/`.msi` installers |
| Linux | `RISARMS-Portal-0.6.0-linux-x86_64.tar.gz`, plus `.deb`/`.AppImage` |

`dist/SHA256SUMS-<platform>` records the platform archive and installer digests.
`dist/sbom-<platform>.cdx.json` records the platform dependency inventory.

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
It validates `v0.6.0` / `v0.6.0-beta.N` against `pyproject.toml` and
`risarms_ui.__version__`, runs lint/tests, verifies Tk, embeds
`UPDATE_PUBLIC_KEY`, and builds on `macos-15-intel`, `macos-15`,
`windows-2022` and `ubuntu-24.04`. It uploads unique per-platform artifacts,
checksums and SBOMs.

For tags, a release job verifies checksums, merges SBOMs, requires
`UPDATE_SIGNING_KEY` to sign `update.json`, writes aggregate `SHA256SUMS`, and
creates a **draft** GitHub release. It never publishes automatically and
refuses to modify an existing release. Beta releases are marked prerelease and
labeled unsigned. `workflow_dispatch` builds artifacts only.

The old `macos-13`/`macos-14` labels are retired. A first real CI draft run,
native installers, signing and notarization remain pending.

## 5. Validation status

| Item | Status |
|---|---|
| Unit/contract tests | IMPLEMENTED (286 passed) |
| Tk GUI launch on macOS | Blocked in the authoring environment until Tk is installed |
| Physical Apple Silicon run | NOT YET PERFORMED |
| Physical Windows run | NOT YET PERFORMED |
| Physical Linux / Void glibc smoke run | NOT YET PERFORMED |
| Native installers from CI | NOT YET PERFORMED |
| Signed/notarized artifacts | NOT YET PERFORMED (hooks only) |
| Public signed auto-updates | GATED (no production key) |
| LAN reconnect/revocation testing | NOT YET PERFORMED on physical devices |
| iOS TestFlight / Android beta | FUTURE WORK |

## Related

- [RISARMS-UI system specification](../systems/risarms-ui.md)
- [Cross-platform release engineering](cross-platform-release.md)
- [Hardware-gated validation](hw-gated-validation.md)
