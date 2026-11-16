# Implementation Status

> [!IMPORTANT] Status reflects evidence gathered on **2026-11-15** on the
> macOS recovery host. "Verified" means a command was run in this session and
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
| HTTPS API, sessions, CSRF, approvals | Complete / verified | 896 passed / 4 skipped |
| Device credentials, single-use WSS tickets, session renewal | Complete / verified | `test_desktop_control.py`, merged from the feature branch |
| Revocation events | Complete / verified | Messaging + device revocation tests |
| Job idempotency | Complete / verified | Existing contract tests |
| Human-to-human messaging (`/api/messages`) | Complete / verified | 7 new tests in `tests/test_messages.py` |
| Messaging over WSS push | Complete / verified | Real `core web` process with two clients: `message.received` received over WSS, see `tests/integration/test_core_messaging_e2e.py` in RISARMS-ui |
| Windows/macOS LAN validation | Blocked | No second machine or certificate chain |

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
| Signed update check | Complete / verified (logic) | `tests/test_updates.py`; no install/apply UI yet |
| Installer creation | Implemented / **unverified** | `packaging/installers.py`; local build refuses without Tk |
| Signed/notarized artifacts | Blocked | No signing credentials |

## 3. Subsystems

| Project | Status | Evidence |
|---|---|---|
| ASIS | Complete / verified | 948 passed / 24 skipped; full ruff still reports pre-existing style debt |
| ASCS | Complete / verified | 996 passed / 16 skipped; `doctor --offline` smoke verified locally (exit 0) |
| RESCS | Complete / verified | 318 passed / 4 skipped; CLI configuration errors actionable; live tests report unavailable services instead of failing the run |
| TIVISS | Complete / verified | 299 passed; full ruff still reports pre-existing style debt |

## 4. Cross-cutting

| Item | Status |
|---|---|
| Repository ownership documented | Yes — see [Repository Ownership](../architecture/README.md) and decision 0010 |
| Multi-user isolation tests | Verified at API level (records, files, messages) |
| Live CORE→ASIS/ASCS/RESCS/TIVISS integration | Blocked — needs provisioned services |
| Raspberry Pi / ARM64 | Blocked |
| 24/7 operation | Blocked |
| Branch CI on pushed commits | CORE, RISARMS-UI, ASCS, RESCS and TIVISS green (2026-11-15); ASIS CI only runs on `main`/PR; RISARMS-DOCS has no code CI |
| Documentation drift review | Partial — current pages refreshed; historical reports intentionally retain their original evidence |

## 5. Open items carried forward

1. Produce and inspect real installers on GitHub runners. The release workflow
   builds Linux from a Tk-enabled distribution interpreter, verifies the
   Windows installer toolchain before building, and can honour
   `workflow_dispatch`, so this is a missing *run*, not missing code. No
   authenticated `gh` client is available here to trigger it.
2. Provision the production Ed25519 public key/fingerprint in the packaged
   application. Signed-manifest check, SHA-256 download verification and an
   explicit OS-installer handoff exist; unattended install/rollback and
   post-install health verification do not.
3. Validate the Void installer on the physical HP 14: runit, Caddy, nftables,
   lid-close behavior, first-owner setup and backup/restore.
4. Run the ASIS suite through a PR because its CI workflow does not trigger on
   feature-branch pushes; local 948/24 is not a substitute for the matrix.
5. Validate Ollama cancellation on Windows with a real model.
6. Exact model tag behavior across ASIS/ASCS/TIVISS.
7. Burn down the pre-existing full-ruff debt in ASIS and TIVISS; changed-file
   lint is clean today.
