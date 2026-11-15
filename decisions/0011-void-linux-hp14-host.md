# 0011 — Void Linux is the HP 14 host baseline

- Status: Accepted
- Date: 2026-11-15

## Context

The HP 14 previously had no fixed OS assumption. The host must run 24/7,
headless, co-host C.O.R.E. and R.E.S.C.S., and provide HTTPS to desktop and
mobile clients without relying on a desktop session.

## Decision

Use **Void Linux x86_64 glibc** as the HP 14 host baseline.

- Headless installation; no desktop environment is required.
- runit supervises `risarms-core`, `risarms-rescs` and `caddy`; the installer
  also keeps init-agnostic commands where practical.
- Caddy terminates TLS on `443` and proxies CORE `8780/8781`; RESCS stays on
  loopback `8081`.
- Data lives under `/var/lib/risarms`, configuration under `/etc/risarms`, logs
  under `/var/log/risarms`, and the service account is `risarms`.
- Windows and macOS remain supported release/client targets, not the server
  baseline.
- Raspberry Pi/ARM64 deployment remains supported separately.

## Consequences

- The Void installer is documented in `RISARMS-DOCS/development/void-linux.md`.
- Physical HP 14 validation is still required.
- Deployment scripts must not assume systemd; runit is the default on this host.
- Existing Pi/systemd deployment assets remain valid for Pi hosts.
