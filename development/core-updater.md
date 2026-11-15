# CORE/RESCS host updater

Status: **PLANNED / PARTIAL**. Manifest verification exists in RISARMS-UI; the
host installer still uses release archives manually.

## Preconditions

- Registered owner device with a live owner session.
- Five-minute admin unlock.
- Current backup in `/var/lib/risarms/backups`.
- Signed `update.json` and Ed25519 public key configured out of band.

## Procedure

1. Resolve the requested version/channel and verify the manifest signature.
2. Require an explicit owner confirmation showing version, channel and hashes.
3. Stop `risarms-core`, then `risarms-rescs`.
4. Archive `/var/lib/risarms/{core,rescs}` and `/etc/risarms`.
5. Install the new RESCS wheel/archive into `/opt/risarms/rescs-venv`.
6. Install the new CORE wheel/archive into `/opt/risarms/core-venv`.
7. Start RESCS; require `/health/ready`.
8. Start CORE; require `/api/health`.
9. On any failure: stop both, restore the previous virtual environments and
   data backup, then restart.
10. Audit the result. Never auto-apply a queued action.

Void: use `sv down/up`. systemd hosts: use `systemctl`. The updater must not
assume one init system.
