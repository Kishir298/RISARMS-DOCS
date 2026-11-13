# Implementation Status

> [!IMPORTANT] Status reflects evidence gathered on **2026-11-13** on the
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
| HTTPS API, sessions, CSRF, approvals | Complete / verified | 870 passed |
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
| Dependency self-check (`--doctor`) | Complete / verified | Reads `importlib.metadata.version("core-client")` so the repo's legacy `client` package cannot mask a missing dependency |
| Messaging delivery states | Complete / verified | `queued` is never reported as delivered |
| Cloud Files folders/quota/details/progress | Implemented / unverified | No GUI run |
| Light/dark theme, keyboard navigation | Implemented / unverified | Existing theme module; no accessibility audit |
| Installer creation | Implemented / **unverified** | `packaging/installers.py`; local build refuses without Tk |
| Signed/notarized artifacts | Blocked | No signing credentials |

## 3. Subsystems

| Project | Status | Evidence |
|---|---|---|
| ASIS | Complete / verified at its own suite | Latest main CI was green; not re-run here. Its release matrix had an invalid `macos-15-intel` label, now corrected on a review branch |
| ASCS | Complete / verified | 993 passed; `doctor --offline` smoke verified locally (exit 0) and CI **green** on `c2f4464` |
| RESCS | Complete / verified | 318 passed; CLI configuration errors actionable; CI **green** on `cdbd6fa`; live tests now report unavailable services instead of failing the run |
| TIVISS | Complete / verified | 285 passed; CI **green** on `2ec78e1` (3.11–3.13) |

## 4. Cross-cutting

| Item | Status |
|---|---|
| Repository ownership documented | Yes — see [Repository Ownership](../architecture/README.md) and decision 0010 |
| Multi-user isolation tests | Verified at API level (records, files, messages) |
| Live CORE→ASIS/ASCS/RESCS/TIVISS integration | Blocked — needs provisioned services |
| Raspberry Pi / ARM64 | Blocked |
| 24/7 operation | Blocked |
| Documentation drift review | Partial — this update covers desktop, messaging, packaging, recovery |

## 5. Open items carried forward

1. Produce and inspect real installers on GitHub runners. The release workflow
   now builds Linux from a Tk-enabled distribution interpreter, verifies the
   Windows installer toolchain before building, and can honour
   `workflow_dispatch`, so this is a missing *run*, not missing code.
2. CORE feature-branch CI was still queued at the time of writing; re-check the
   run before merging.
2. Validate Ollama cancellation on Windows with a real model.
3. Portal CSRF/Origin behavior against a proxied deployment.
4. Exact model tag behavior across ASIS/ASCS/TIVISS.
5. Partial frame receive timeout coverage.
6. Legacy `client/` package still ships beside CORE-CLIENT's `client`
   namespace; the desktop app no longer imports it, but the duplicate name
   remains a packaging hazard for the legacy portal entry point.
