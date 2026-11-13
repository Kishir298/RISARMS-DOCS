# 0010 — RISARMS-UI is the canonical desktop client

## Context

The CORE-CLIENT repository contains a Tkinter desktop workspace and legacy
TCP/TLS device helpers. Keeping two desktop applications creates drift in
authentication, record synchronization, file handling, theming and packaging.
The ecosystem needs one signed, cross-platform application that presents
C.O.R.E. and its subsystems without becoming a new integration layer.

## Decision

RISARMS-UI is the canonical desktop application. It:

- owns the migrated CORE-CLIENT desktop workspace and user-facing navigation;
- talks to CORE-HOST over HTTPS and WSS only;
- keeps a device-local profile, offline SQLite cache and explicit sync queue;
- stores only server-issued device credentials in the OS keychain;
- ships unsigned PyInstaller artifacts by default, with documented signing
  hooks for release engineers.

CORE-CLIENT remains the home of the native TCP/TLS protocol client and legacy
compatibility tests. Its desktop entrypoint is not the primary user interface.

## Alternatives

- **Keep developing both desktops:** rejected; duplicate security and UX work.
- **Move to Qt/Electron/Tauri:** rejected; Tkinter is already used, keeps the
  dependency surface small and works with the existing packaging toolchain.
- **Make the browser portal the desktop client:** rejected; it cannot provide
  offline local profiles, keychain-backed device credentials, local Ollama
  execution or native packaging.

## Consequences

- Authentication and desktop behavior are tested in one repository.
- CORE-HOST gains explicit desktop endpoints: device credentials, session
  renewal, WebSocket tickets and job idempotency.
- Unsigned builds are usable for development but Gatekeeper/SmartScreen
  warnings remain until signing credentials are supplied.
- Physical Windows/Linux and signed-release validation remain external tasks.

## Status

Accepted.
