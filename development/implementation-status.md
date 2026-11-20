# Implementation Status

> [!IMPORTANT] Status reflects evidence gathered on **2026-11-16** on the
> macOS recovery host; the repository sync and hygiene section was updated
> **2026-11-17**. "Verified" means a command was run in this session and
> its result is quoted. "Unverified" means the code exists but no run supports
> the claim. Never read this table as a release approval.

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
| HTTPS API, sessions, CSRF, approvals | Complete / verified | 911 passed / 4 skipped |
| Device credentials, single-use WSS tickets, session renewal | Complete / verified | `test_desktop_control.py`, merged from the feature branch |
| Revocation events | Complete / verified | Messaging + device revocation tests |
| Job idempotency | Complete / verified | Existing contract tests |
| Human-to-human messaging (`/api/messages`) | Complete / verified | 7 new tests in `tests/test_messages.py` |
| Messaging over WSS push | Complete / verified | Real `core web` process with two clients: `message.received` received over WSS, see `tests/integration/test_core_messaging_e2e.py` in RISARMS-ui |
| Physical LAN validation (Void CORE host ↔ RISARMS-ui clients: macOS Intel, macOS Apple Silicon, Windows x86_64, Linux x86_64) | Blocked | No second machine, Void host or certificate chain; matrix NOT YET PERFORMED (historical Windows-host ↔ Mac tests keep their dates/context and do not satisfy this matrix) |
| CORE 0.6.0 Void release assets (versioned venvs, storage guard, Caddy/nftables, backup/restore, upgrade/rollback, doctor) | Implemented / **unverified** at runtime | Static tests only; no booted Void host or physical HP |
| CORE 0.6.0 runtime validation (install, reboot, runit, rollback, storage failure) | Blocked | Requires the reference HP 14 (HP 14-dq1037wm) with Void installed |

## 2. RISARMS-ui desktop application

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
| Installer creation | Implemented / **unverified** | `packaging/installers.py`; local build refuses without Tk; first CI draft run pending |
| Release tag/version validation, beta metadata, SBOM merge, draft-only CI | Complete / verified | 286 tests; ruff clean; workflow YAML parsed |
| Signed/notarized artifacts | Blocked | No Apple Developer ID or Windows code-signing certificate; macOS beta is ad-hoc, Windows unsigned |
| Public signed auto-updates | Blocked | No production `UPDATE_PUBLIC_KEY` fingerprint or `UPDATE_SIGNING_KEY` |

## 3. Subsystems

| Project | Status | Evidence |
|---|---|---|
| ASIS | Complete / verified | 948 passed / 24 skipped; full ruff still reports pre-existing style debt |
| ASCS | Complete / verified | 996 passed / 16 skipped (historical evidence, macOS Python 3.14, 2026-11-15); `doctor --offline` smoke verified locally (exit 0) |
| RESCS | Complete / verified | 318 passed / 4 skipped; CLI configuration errors actionable; live tests report unavailable services instead of failing the run |
| TIVISS | Complete / verified | 299 passed; full ruff still reports pre-existing style debt |

## 4. Cross-cutting

| Item | Status |
|---|---|
| Repository ownership documented | Yes — see [Repository Ownership](../architecture/README.md) and decision 0010 |
| Multi-user isolation tests | Verified at API level (records, files, messages) |
| Live CORE→ASIS/ASCS/RESCS/TIVISS integration | Blocked — needs provisioned services |
| Booted Void Linux / physical HP 14 | Blocked |
| Raspberry Pi / ARM64 | Historical / not a CORE 0.6.0 target |
| 24/7 operation | Blocked |
| Branch CI on pushed commits | CORE, RISARMS-UI, ASCS, RESCS and TIVISS green (2026-11-15). CORE and RESCS regressed on 2026-11-20 and were fixed and pushed the same day: CORE [`b5ba79f`](https://github.com/Kishir298/CORE/actions/runs/44775446911) 15/15 jobs green incl. `core-host (Windows, full)`; RESCS [`6b8e780`](https://github.com/Kishir298/RESCS/actions/runs/44767993130) green; RISARMS-UI [`24ce7a6`](https://github.com/Kishir298/RISARMS-ui/actions/runs/44030726524) green. ASIS CI only runs on `main`/PR; RISARMS-DOCS has no code CI |
| Documentation drift review | Partial — current pages refreshed; historical reports intentionally retain their original evidence |

## 5. Open items carried forward

1. Produce and inspect real installers on GitHub runners. The release workflow
   builds Linux from a Tk-enabled distribution interpreter, verifies the
   Windows installer toolchain before building, and can honour
   `workflow_dispatch`, so this is a missing *run*, not missing code. No
   authenticated `gh` client is available here to trigger it.
2. Provision the production Ed25519 public key as `UPDATE_PUBLIC_KEY` for the
   release workflow. Packaging now fails closed without a valid key, embeds it
   into frozen builds, and performs signed-manifest plus SHA-256 download
   verification with an explicit OS-installer handoff. Unattended
   install/rollback and post-install health verification do not exist.
3. Validate the Void installer on the physical HP 14: runit, Caddy, nftables,
   lid-close behavior, first-owner setup and backup/restore.
4. Run the ASIS suite through a PR because its CI workflow does not trigger on
   feature-branch pushes; local 948/24 is not a substitute for the matrix.
5. Validate Ollama cancellation on Windows with a real model.
6. Exact model tag behavior across ASIS/ASCS/TIVISS.
7. Burn down the pre-existing full-ruff debt in ASIS and TIVISS; changed-file
   lint is clean today.

## 6. Repository sync and hygiene (2026-11-17)

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
| `TIVISS/` | Ignore `.ascs/` workspace state and SSH private keys | Integration state can contain workspace context |
| `CORE/services/{ASCS,RESCS,TIVISS,ASIS}/` | Applied runtime-storage, database-journal, SSH-key and local-cache fixes to the mirrored services | Keeps release mirrors consistent with their sources |
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
- `CORE/install/core-0.5.0` and `core_client-0.5.0` lag the 0.6.0 package
  metadata; `rescs-0.4.0` matches its package. This predates the sync and is
  outside the ignore-rule scope.
- `ASIS/.gitignore` still lists `uv.lock` although ASIS has no lockfile; it is
  harmless until ASIS adopts uv.
- `CORE/services/ASCS/.gitignore` still ignores `uv.lock` because the outer
  CORE repository does not track nested lockfiles; standalone ASCS tracks it.
  This is intentional but differs from the owning repo.
