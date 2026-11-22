# Implementation Status

> [!IMPORTANT] Status reflects evidence gathered on **2026-11-16** on the
> macOS recovery host; the repository sync and hygiene section was updated
> **2026-11-17**, and the release/CI/desktop sections were updated
> **2026-11-22** from dispatched GitHub Actions runs. "Verified" means a
> command or CI run was executed and its result is quoted. "Unverified" means
> the code exists but no run supports the claim. Never read this table as a
> release approval.

## Legend

| Status | Meaning |
|---|---|
| **Complete / verified** | Implemented and a test or command demonstrated it |
| **Implemented / unverified** | Code and tests exist; the target environment was not available |
| **Partial** | Works, but a named part of the requirement is missing |
| **Not implemented** | No code yet |
| **Blocked** | Requires hardware, credentials or a runtime that is unavailable |

## 1. CORE-HOST

| Capability | Status | Evidence / note |
|---|---|---|
| HTTPS API, sessions, CSRF, approvals | Complete / verified | 917 passed / 4 skipped (macOS Python 3.14, 2026-11-22); CI green on 3.10–3.14 plus the full Windows job |
| Authorization PDP adapter (embedded parity, T.I.V.I.S.S. daemon delegation, fail-closed) | Complete / verified | `tests/security/test_pdp.py` 16 tests. The daemon transport is AF_UNIX-only by design, so the two listening-daemon tests skip only on platforms without `socket.AF_UNIX`; embedded and fail-closed coverage runs everywhere and daemon mode raises an actionable `PDPUnavailableError` instead of `AttributeError` |
| Device credentials, single-use WSS tickets, session renewal | Complete / verified | `test_desktop_control.py`, merged from the feature branch |
| Revocation events | Complete / verified | Messaging + device revocation tests |
| Job idempotency | Complete / verified | Existing contract tests |
| Human-to-human messaging (`/api/messages`) | Complete / verified | 7 new tests in `tests/test_messages.py` |
| Messaging over WSS push | Complete / verified | Real `core web` process with two clients: `message.received` received over WSS, see `tests/integration/test_core_messaging_e2e.py` in RISARMS-ui |
| Physical LAN validation (Void CORE host ↔ RISARMS-ui clients: macOS Intel, macOS Apple Silicon, Windows x86_64, Linux x86_64) | Blocked | No second machine, Void host or certificate chain; matrix NOT YET PERFORMED (historical Windows-host ↔ Mac tests keep their dates/context and do not satisfy this matrix) |
| CORE 0.6.0 Void release assets (versioned venvs, storage guard, Caddy/nftables, backup/restore, upgrade/rollback, doctor) | Implemented / **unverified** at runtime | Static tests only; no booted Void host or physical HP |
| CORE 0.6.0 runtime validation (install, reboot, runit, rollback, storage failure) | Blocked | Requires the reference HP 14 (HP 14-dq1037wm) with Void installed |

## 2. CORE server release orchestration (RISARMS-HOST)

| Capability | Status | Evidence / note |
|---|---|---|
| Release ownership after the split | Complete / verified | `RISARMS-HOST/.github/workflows/release.yml`; CORE-HOST only runs test CI |
| Pinned component revisions | Complete / verified | `components.lock.json` pins CORE-HOST, CORE-CLIENT, RESCS, ASCS, ASIS and TIVISS-HOST to 40-character commits, each with a passing CI run in its own repository; `risarms-host stage` fetches exactly those commits. Revisions and run ids: [release evidence](release-evidence-2026-11-22.md) |
| Reproducible assembly | Complete / verified locally | Sorted entries, normalised ownership and `SOURCE_DATE_EPOCH`; two assemblies of the same staged tree were byte-identical (`cmp`) |
| Verification from the assembled bundle | Complete / **verified in CI** | [Run 45013778229](https://github.com/Kishir298/RISARMS-HOST/actions/runs/45013778229) staged the pinned components, assembled, re-assembled byte-identically, and ran the shipped installer in `ghcr.io/void-linux/void-glibc-full` (`sha256:e98f8c…`). 30 assertions passed: both services `run:`, Caddy TLS over the internal CA (HTTP→HTTPS 308), backup/restore round-trip, upgrade and rollback healthy, `risarms-doctor` clean. Container evidence only, not hardware |
| Checksums, provenance, SBOM | Complete / verified locally | `SHA256SUMS`, unsigned SLSA-shaped `provenance.json`, CycloneDX SBOM (`cyclonedx-bom` 9.0.0) |
| Draft-only publishing | Complete / verified (code) | Publish job is gated on a `v*` tag and always passes `--draft`; no tag has been created for this work |

## 3. RISARMS-ui desktop application

| Capability | Status | Evidence / note |
|---|---|---|
| Tkinter desktop window (no browser/server) | Implemented / unverified | Import and unit paths tested; the host has no `_tkinter`, so no window was opened |
| Local profiles and SQLite store | Complete / verified | Existing suite |
| Automatic connection on launch | Complete / verified | Device credential path covered |
| **Automatic reconnection with backoff** | Complete / verified | `tests/test_reconnection.py` (9 tests) |
| WSS control channel + restoration | Implemented / unverified | Channel logic unit-tested with a fake stream; no live server run |
| Offline record sync | Complete / verified | Existing + updated sync tests |
| Offline file sync (durable queue) | Complete / verified | `test_messaging.py` style store tests, `sync_files` |
| Human messaging UI | Complete / verified (logic) | Store/queue tests plus a real two-client HTTP+WSS test; UI rendering not exercised without Tk |
| Single background sync worker | Implemented / partially verified | A guard prevents the timer and reconnect event from syncing concurrently; the guard needs a Tk loop to exercise |
| Dependency self-check (`--doctor`) | Complete / verified | Imports packaged UI modules, reports missing Tk and checks optional `cryptography` without importing the legacy `client` package |
| Messaging delivery states | Complete / verified | `queued` is never reported as delivered |
| Cloud Files folders/quota/details/progress | Implemented / unverified | No GUI run |
| Light/dark theme, keyboard navigation | Implemented / unverified | Existing theme module; no accessibility audit |
| Per-profile service grants and cached authorization | Complete / verified | `tests/test_authorization.py`; CORE remains authoritative; grants refresh on reconnect and every 60 seconds, and newly granted services become selectable |
| Loopback local-action approvals | Complete / verified (logic) | `tests/test_approvals.py`; broker denies on timeout, close or transport error |
| Informed owner-action review | Complete / verified (logic) | `tests/test_owner_actions_view.py`; full payload shown before password re-auth and confirmation |
| Signed update check | Complete / verified (logic) | `tests/test_updates.py`; verified download and explicit OS-installer handoff; unattended install/rollback remains open |
| Installer creation (DMG, EXE, MSI, DEB, archives) | Complete / **validated in CI** | All four platforms built in [run 45012833473](https://github.com/Kishir298/RISARMS-ui/actions/runs/45012833473); the Linux set was installed and launched in [smoke run 45013788806](https://github.com/Kishir298/RISARMS-ui/actions/runs/45013788806); see §3.1 and [installers.md](installers.md#5-current-validation-state) |
| Release tag/version validation, beta metadata, SBOM merge, draft-only CI | Complete / verified | 295 tests; ruff clean; workflow YAML parsed |
| Signed/notarized artifacts | Blocked | No Apple Developer ID or Windows code-signing certificate; macOS beta is ad-hoc, Windows unsigned |
| Public signed auto-updates | Blocked | Repository variables and secrets contain no `UPDATE_PUBLIC_KEY` or `UPDATE_SIGNING_KEY` (verified by listing names only). Production builds still fail closed; an explicit `validation_build=true` dispatch generates an ephemeral key and marks artifacts non-publishable so installers can be exercised |

### 3.1 Desktop installer validation run

`desktop-release.yml` was dispatched with `validation_build=true` because no
production update keys exist. Iterations found five packaging defects that
ordinary CI could not catch (see [installers.md](installers.md#5-current-validation-state));
the final build run [45012833473](https://github.com/Kishir298/RISARMS-ui/actions/runs/45012833473)
passed all jobs:

| Platform | Artifacts | Checksums |
|---|---|---|
| macOS Intel (`macos-15-intel`) | zip + dmg | verified |
| macOS Apple Silicon (`macos-15`) | zip + dmg | verified |
| Windows x86_64 (`windows-2022`) | zip + Inno Setup `-setup.exe` + WiX `.msi` | verified |
| Linux x86_64 (`ubuntu-24.04`) | tar.gz + `.deb` | re-verified in CI |

That artifact set was then installed by desktop-smoke run 45013788806: the
`.deb` was installed with its dependencies, the installed binary reported
`Tk 8.6` with a real display under Xvfb, the GUI stayed up for the 20 s timeout,
and the messaging e2e test passed against a real CORE server. Every set is marked
`VALIDATION-ONLY` because the build used an ephemeral update key; nothing was
published (the release job is tag-gated and skipped). macOS is ad-hoc signed
and unnotarized, Windows is unsigned — OS code signing remains blocked, and
that is a different gate from update-manifest signing.

## 4. Subsystems

| Project | Status | Evidence |
|---|---|---|
| ASIS | Complete / verified | 948 passed / 24 skipped; full ruff still reports pre-existing style debt |
| ASCS | Complete / verified | 996 passed / 16 skipped (macOS Python 3.14, recorded 2026-11-15, **re-verified 2026-11-20** on Python 3.14.7); `doctor --offline` smoke verified locally (exit 0) |
| RESCS | Complete / verified | 318 passed / 4 skipped; CLI configuration errors actionable; live tests report unavailable services instead of failing the run |
| TIVISS | Complete / verified | 299 passed; full ruff still reports pre-existing style debt |

## 5. Cross-cutting

| Item | Status |
|---|---|
| Repository ownership documented | Yes — see [Repository Ownership](../architecture/README.md) and decision 0010 |
| Multi-user isolation tests | Verified at API level (records, files, messages) |
| Live CORE→ASIS/ASCS/RESCS/TIVISS integration | Blocked — needs provisioned services |
| Booted Void Linux / physical HP 14 | Blocked |
| Raspberry Pi / ARM64 | Historical / not a CORE 0.6.0 target |
| 24/7 operation | Blocked |
| Branch CI on pushed commits | CORE, RISARMS-UI, ASCS, RESCS and TIVISS green (2026-11-15). CORE and RESCS regressed on 2026-11-20 and were fixed and pushed the same day: CORE [`b5ba79f`](https://github.com/Kishir298/CORE-HOST/actions/runs/44775446911) 15/15 jobs green incl. `core-host (Windows, full)`; RESCS [`6b8e780`](https://github.com/Kishir298/RESCS/actions/runs/44767993130) green; RISARMS-UI [`24ce7a6`](https://github.com/Kishir298/RISARMS-ui/actions/runs/44030726524) green. ASIS CI only runs on `main`/PR; RISARMS-DOCS has no code CI |
| Documentation drift review | Partial — current pages refreshed; historical reports intentionally retain their original evidence |

## 6. Open items carried forward

1. ~~Produce and inspect real installers on GitHub runners.~~ **Done
   2026-11-22** — see §3.1. Remaining: OS-sign the artifacts (Apple Developer
   ID + notarization, Windows code-signing certificate); none are configured.
2. Provision the production Ed25519 public key as `UPDATE_PUBLIC_KEY` and
   `UPDATE_SIGNING_KEY` for the release workflow. Both are absent from
   repository variables and secrets, so packaging fails closed for production
   and only the explicit validation path works. Unattended install/rollback and
   post-install health verification still do not exist.
3. Validate the Void installer on the physical HP 14: runit, Caddy, nftables,
   lid-close behavior, first-owner setup and backup/restore.
4. Run the ASIS suite through a PR because its CI workflow does not trigger on
   feature-branch pushes; local 948/24 is not a substitute for the matrix.
5. Validate Ollama cancellation on Windows with a real model.
6. Exact model tag behavior across ASIS/ASCS/TIVISS.
7. Burn down the pre-existing full-ruff debt in ASIS and TIVISS; changed-file
   lint is clean today.

## 7. Runtime checks executed (2026-11-22)

Only checks the available environment could actually run are marked passed.

| Check | Environment | Command | Result |
|---|---|---|---|
| Installed CORE command | macOS 14.6 x86_64, Python 3.14 | `core-host --help`, `core-host doctor --data /tmp/risarms-core-doctor` | Passed, exit 0 |
| CORE ↔ RESCS loopback | macOS, sibling `RESCS/` checkout | `pytest tests/integration/test_real_rescs_contract.py -q` | 1 passed in 12.24 s against the real RESCS app on throwaway SQLite |
| Desktop dependency self-check | macOS, no `_tkinter` | `python -m risarms_ui --doctor` | `not ready: tkinter` — window startup blocked on this host |
| Installed desktop binary (Linux) | ubuntu-24.04 + Xvfb, CI | desktop-smoke 45013788806 | `.deb` installed; `Tk 8.6`, display available, `not ready: keyring` (no SecretService on the runner); GUI stayed up 20 s; messaging e2e 2 passed |
| Void install, runit start, Caddy TLS, backup/restore, upgrade/rollback | `void-glibc-full` container, CI | run 45013778229 | Passed: 30/30 assertions, both services `run:`, TLS via internal CA, HTTP→HTTPS 308, backup round-trip, upgrade+rollback healthy, doctor clean |
| nftables load, reboot persistence, runtime storage exhaustion, physical LAN, 24/7 | — | — | **BLOCKED**: the container lacks `NET_ADMIN`, there is no Void host, and only one machine |

Untested items stay untested: nothing in this document treats the container run
as hardware certification. Per-run detail, artifact digests and the evidence
classes are recorded in [release evidence 2026-11-22](release-evidence-2026-11-22.md).

## 8. Repository sync and hygiene (2026-11-17)

Fast-forward-only sync was run for every remote-backed repository; all were
already at their remote branch tips. HEADs below are the sync point, before the
hygiene commits in §6.1. `Flavora/` was intentionally excluded, and
`integration-tests/` has no configured remote, so it cannot be pulled.

| Repository | Branch | HEAD |
|---|---|---|
| ASCS | `fix/doctor-offline-smoke` | `f6de931` |
| ASIS | `fix/release-runner-labels` | `e627729` |
| CORE | `feat/desktop-control-channel` | `f321b6c` |
| RISARMS-DOCS | `docs/desktop-integration` | `4810f02` |
| RESCS | `fix/cli-configuration-diagnostics` | `18bd8aa` |
| TIVISS | `fix/ci-test-dependencies` | `074dd58` |
| RISARMS-ui | `feat/risarms-ui-desktop` | `8e06179` |

### 6.1 Ignore-rule hardening

Safety/privacy gaps were fixed, along with a few generated-artifact hygiene
rules; no tracked source was removed except Python bytecode caches in
`integration-tests/`.

| Repository | Change | Reason |
|---|---|---|
| `integration-tests/` | Added `.gitignore`; removed six tracked `__pycache__/*.pyc` files from the index | The repo had no ignore rules; caches were tracked |
| `RESCS/` | Ignore `rescs_storage/`, `rescs_test_storage/`, `rescs_storage_test/`, `rescs.env`, and SSH private keys | Default runtime storage and CLI-generated config can hold user data or an API key |
| `ASIS/` | Ignore SQLite sidecars and SSH private keys | Runtime DB journals and local keys must never be committed |
| `ASCS/` | Ignore SSH private keys, `.mypy_cache/`, `.ipynb_checkpoints/`; stopped ignoring the tracked `uv.lock` | Removed a tracked-but-ignored inconsistency |
| `TIVISS-HOST/` | Ignore `.ascs/` workspace state and SSH private keys | Integration state can contain workspace context |
| `RISARMS-HOST/services/{ASCS,RESCS,TIVISS-HOST,ASIS}/` | Applied runtime-storage, database-journal, SSH-key and local-cache fixes to the mirrored services | Keeps release mirrors consistent with their sources |
| `RISARMS-ui/` | Un-ignored the tracked `packaging/risarms-ui.spec` | Removed a tracked-but-ignored inconsistency |
| `RISARMS-DOCS/` | Ignore coverage, generated build outputs, and temporary/editor backup files | Prevent accidental commits of generated artifacts |

Additionally, `CORE-HOST/config/core.lan.example.yaml` is now tracked (the local
`core.yaml` remains ignored), so the LAN setup docs resolve from a fresh clone.

Verification: `git check-ignore -v` matched every newly covered path and left
`.env.example` / `requirements.txt` unignored. The documentation venv was synced
with `RISARMS-DOCS/.venv/bin/python -m pip install -r RISARMS-DOCS/requirements.txt`;
`pip check` reported "No broken requirements found." No new Python packages or
modules were needed, so `requirements.txt` is unchanged.

### 6.2 Residual items

- `integration-tests/` has no remote; its hygiene changes can only be committed
  locally (no push target).
- `RISARMS-ui` still tracks generated validation evidence
  (`validation/command-tests.xml`, `source-sha256.json`,
  `installed-command-smoke.json`) and a historical `install/*.whl`; these are
  release evidence, not secrets, and need a policy decision before untracking.
- `RISARMS-HOST/install/core-0.5.0` and `core_client-0.5.0` lag the 0.6.0 package
  metadata; `rescs-0.4.0` matches its package. This predates the sync and is
  outside the ignore-rule scope.
- `ASIS/.gitignore` still lists `uv.lock` although ASIS has no lockfile; it is
  harmless until ASIS adopts uv.
- `RISARMS-HOST/services/ASCS/.gitignore` still ignores `uv.lock` because the outer
  CORE repository does not track nested lockfiles; standalone ASCS tracks it.
  This is intentional but differs from the owning repo.
