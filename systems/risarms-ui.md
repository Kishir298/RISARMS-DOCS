# RISARMS-UI — Unified Desktop Application

> [!NOTE] **Status:** v0.6.0 **IMPLEMENTED** (source and automated tests: 222
> passing). Signed installers, physical Windows/Linux runs and long-duration
> desktop validation are **NOT YET PERFORMED**. Builds are unsigned by default.
> Installer generation is implemented and unverified — see
> [Installer Creation](../development/installers.md).

## 1. Purpose

RISARMS-UI is the single canonical desktop client for the ecosystem. It replaces
the legacy CORE-CLIENT desktop workspace and connects a user's device to
C.O.R.E. while keeping local profiles, history, records and files usable
offline.

It is a presentation and control application, not a new integration layer. All
cross-system traffic continues to flow through C.O.R.E. and its existing
contracts.

## 2. Platform and stack

- **Framework:** Python `>=3.10` with Tkinter/ttk (no Qt, Electron or browser
  runtime).
- **Packaging:** PyInstaller one-directory bundles for macOS, Windows and Linux.
- **Dependencies:** `core-client` (local inference and legacy helpers),
  `keyring` (OS-backed device credentials) and `websockets` (control channel).
- **Offline store:** per-profile SQLite database with scrypt-derived passphrase
  verification; files are capped at 8 MiB each and 250 MiB per local profile.

## 3. User-facing capabilities

| Area | Behavior |
|---|---|
| Local profiles | Separate local passphrase from the server account; no recovery service; application lock is not disk encryption |
| Connection | HTTPS login, remembered revocable device credential, automatic reconnect with bounded backoff, 12-hour server sessions with renewal, WSS control channel with polling fallback |
| Messages | Direct text messages between approved accounts, local conversation history, queued/delivered/read states, offline queue drained on reconnect |
| ASIS | Server-routed or local Ollama chat; safe-chat worker on the host |
| ASCS | Owner-only server or local coding workspace with explicit confirmation |
| TIVISS | Owner-only TIVISS workspace |
| Tasks | Server jobs with live polling, cancellation and local model execution |
| History | Device-local conversation history |
| My Storage | JSON records with optimistic concurrency and explicit/automatic synchronization |
| Cloud Files | Account-scoped folders, quota, file details, upload/download progress, SHA-256 verification, durable offline upload queue and delete |
| Devices | Lists registered devices; revocation is enforced by CORE-HOST and terminates the affected control channel |
| Administration | Owner-only accounts, access requests, settings, audit, quotas and server status with password re-authentication |
| Settings | Light/dark theme, service source paths, local model, chat storage policy and server origin |

## 4. Security model

- Passwords, session cookies and CSRF tokens remain in memory only.
- Only server-issued, scoped, revocable device credentials are written to the
  OS keychain. If keyring is unavailable the application degrades to
  memory-only credentials and requires a fresh sign-in.
- Remote origins must use HTTPS; plain HTTP is accepted only for loopback.
  Redirects, environment proxies and origins with credentials or paths are
  refused.
- Server permissions are authoritative. The UI hides owner-only pages but
  CORE-HOST enforces every role, CSRF, re-authentication and record/file scope.
- Concurrent local edits are retained and reported as conflicts instead of
  being overwritten.
- Logs never include passwords, session tokens, CSRF values or device
  credentials.

## 5. CORE-HOST contract

The application consumes these authenticated endpoints:

| Endpoint | Purpose |
|---|---|
| `POST /api/login` | Password login; returns profile, CSRF and an optional device credential |
| `POST /api/login/device` | Session from a remembered device credential |
| `POST /api/session/renew` | Extends a live session |
| `POST /api/ws-ticket` | Single-use, 60-second WebSocket ticket |
| `GET /api/devices` | Owned devices; owner may query all |
| `POST /api/devices/{id}/revoke` | Revoke a device and publish a revocation event |
| `GET /api/health` | Capabilities, version and event-channel availability |
| `GET/POST /api/messages` | Human-to-human messaging (threads, conversation, send) |
| `POST /api/messages/{id}/read` | Recipient read acknowledgement |
| `/api/records`, `/api/files`, `/api/folders`, `/api/jobs`, `/api/services`, `/api/status`, `/api/profiles`, `/api/access`, `/api/settings`, `/api/audit`, `/api/quotas` | Existing CORE workspace surfaces |

`GET /api/health` advertises `ws_ticket_v1`, `session_renewal_v1`,
`device_credentials_v1`, `device_management_v1`, `job_idempotency_v1` and
`messaging_v1`.
Job creation accepts an `Idempotency-Key` header so retries do not duplicate
work.

The WSS endpoint is loopback WebSocket at `/api/ws` behind Caddy. Caddy
terminates TLS and proxies `/api/ws` to `127.0.0.1:8781`; the HTTPS API remains
on `127.0.0.1:8780`.

## 6. Reconnection behavior

The monitor thread owns recovery. A failed heartbeat, a closed control channel
or a transport error schedules one guarded attempt with bounded exponential
backoff. The attempt re-authenticates with the stored device credential, then
restores the single-use-ticket WSS channel **before** reporting `Online`. A 401,
403 or `session.revoked` event halts automatic recovery and requires a fresh
sign-in. Queued records, uploads and messages drain after `connection.restored`.
A single-flight guard stops the periodic timer and the reconnect event from
starting two synchronization workers over the same queues.

## 7. Verification

- UI suite: **227 passed** (macOS Python 3.14 venv), including
  `tests/test_reconnection.py`, `tests/test_messaging.py`,
  `tests/test_desktop_doctor.py` and a real two-client messaging test in
  `tests/integration/test_core_messaging_e2e.py` that launches CORE-HOST and
  receives `message.received` over WSS.
- CORE-HOST suite: **870 passed / 4 skipped**.
- RESCS: **318 passed / 4 skipped**; ASCS: **993 passed / 16 skipped**;
  TIVISS: **285 passed**.
- Physical Windows/Linux desktop runs, signed/notarized artifacts, real
  installers, LAN and 24/7 operation remain **NOT YET PERFORMED**.

## 8. Non-goals

- Replacing the CORE web portal for browser-only administration.
- Implementing ASIS/ASCS/TIVISS behavior inside the desktop process.
- Bypassing CORE-HOST role, storage or audit controls.
- Shipping secrets, CA private keys or signing material in the repository.
