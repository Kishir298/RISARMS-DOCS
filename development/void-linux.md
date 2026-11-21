# Void Linux host — HP 14

> [!NOTE]
> This is the canonical CORE 0.6.0 server target: **Void Linux x86_64 glibc,
> headless, with runit**, co-hosting C.O.R.E. and R.E.S.C.S. behind Caddy on the
> HP 14-dq1037wm. The installer and assets have static tests, but the install,
> reboot, runit, Caddy trust, nftables load, storage-failure, upgrade, rollback,
> backup/restore and physical HP runs have **not** been executed yet.
> Raspberry Pi/ARM64 and systemd server deployments are historical for this release.

## Layout

| Item | Path |
|---|---|
| Service account | `risarms` (no login shell) |
| Versioned environments | `/opt/risarms/venvs/<version>/{core,rescs}` |
| Stable environment links | `/opt/risarms/{core-venv,rescs-venv}` |
| C.O.R.E. data | `/var/lib/risarms/core` |
| R.E.S.C.S. data | `/var/lib/risarms/rescs` |
| C.O.R.E. frontend | `/var/lib/risarms/frontend` |
| Configuration | `/etc/risarms/{core.env,rescs.env,gateway.json}` (canonical) and `/var/lib/risarms/core/gateway.json` (CORE runtime copy) |
| Logs | `/var/log/risarms/{core,rescs}` (svlogd, 1 MiB, 10 archives, daily) |
| Install state and snapshots | `/var/lib/risarms/install-state` |
| Backups | `/var/lib/risarms/backups` |
| Caddy site | `/etc/caddy/risarms/portal.caddy` |
| nftables table | `/etc/nftables.d/risarms.nft` |

C.O.R.E. listens on `127.0.0.1:8780` (API) and `127.0.0.1:8781` (WebSocket).
R.E.S.C.S. listens on `127.0.0.1:8081`. Caddy terminates TLS on `443`; the
supplied firewall table exposes only `443`, SSH and mDNS.

## Prerequisites

```sh
sudo xbps-install -S python3 python3-pip caddy runit-void nftables elogind
```

> [!NOTE]
> Void has **no `python3-venv` package** (404 in void-packages); Void's `python3`
> is built `--without-ensurepip`. `python3-pip` provides pip, and the installer
> creates environments with `python3 -m venv --without-pip` + `python3 -m pip
> --python "$staging/bin/python" install ...`. Always install `python3-pip`,
> never `python3-venv`.

The installer requires root, Void Linux, x86_64, glibc, the commands above, and
at least **5 GiB free** under `/var/lib/risarms`. It does not partition or format
storage. Override `RISARMS_MIN_FREE_GIB` only after checking the disk.

Installed RAM on the HP is **unverified** (an earlier report said 4 GB — do not
state a figure as fact). The planned 2 x 8 GB Samsung DDR4-2666 upgrade to
16 GB is **PLANNED — not installed or verified**; do not document it as present.

## Install

```sh
sudo ./deployment/void/install.sh
sudo tail -n 50 /var/log/risarms/core/current
```

The default origin is `https://core.local`. Set a different HTTPS origin without
editing keys:

```sh
sudo RISARMS_PUBLIC_ORIGIN=https://core.example.test ./deployment/void/install.sh
```

On first run the installer generates one `RESCS_API_KEY`, writes the same
gateway to `/etc/risarms/gateway.json` and
`/var/lib/risarms/core/gateway.json`, installs versioned virtual environments,
and records install state. On later runs it verifies both gateway copies,
updates the configured origin without rotating keys, and fails loudly on a key
mismatch. Repair a mismatch manually before rerunning.

It installs runit service directories but does **not** enable them. Review the
generated origin, paths and firewall before enabling:

```sh
sudo ln -s /etc/sv/risarms-rescs /var/service/
sudo ln -s /etc/sv/risarms-core /var/service/
sudo ln -s /etc/sv/caddy /var/service/
sudo sv status risarms-core risarms-rescs caddy
sudo risarms-doctor
```

Read the first-owner setup key from `/var/log/risarms/core/current`, then open
`https://core.local` and trust Caddy's local CA on each client. Copy only the
public root certificate, never the private key.

## Host hardening

- nftables: the installer copies `risarms.nft` into `/etc/nftables.d/`, adds
  `include "/etc/nftables.d/*.nft"` to an existing `/etc/nftables.conf` when
  absent, and validates it. It does not load the rules automatically. Review the
  SSH rule and run `sudo nft -f /etc/nftables.conf` only when ready.
- elogind: `HandleLidSwitch=ignore` keeps the headless host awake with the lid
  closed. Apply with `sudo sv restart elogind` or reboot.
- Avahi is not installed by the release installer; install it separately only if
  mDNS is wanted.
- Caddy uses `tls internal`; for a public name, replace it with an ACME-enabled
  site and open only `443`.

## Operate

```sh
sudo sv status risarms-core risarms-rescs caddy
sudo sv down risarms-core risarms-rescs
sudo sv up risarms-rescs risarms-core
sudo risarms-backup
sudo risarms-restore --yes /var/lib/risarms/backups/risarms-<stamp>.tar.gz
sudo risarms-doctor
```

Backups stop CORE first, then RESCS, archive both data trees plus
`/etc/risarms`, Caddy/nftables/elogind and runit configuration, and restart only
services that were running. Backups contain secrets, are mode `0600`, are not
encrypted by the installer, and default to 14-day retention. Keep copies off the
host on equally protected media.

## Upgrade and rollback

```sh
sudo ./deployment/void/upgrade.sh /path/to/new/CORE-Server-<version>-void-x86_64
sudo risarms-rollback
```

Upgrade validates the new manifest, builds new versioned environments before
switching stable symlinks, and records the previous version. A failed install
restores the previous links. Rollback switches back to the previous environments
and restarts services that were running; use `risarms-restore` for data and
configuration rollback. Never auto-apply an owner action or an update.

## Validation checklist

- [ ] Booted Void install on the HP completes from the release archive.
- [ ] `sv status` shows services up after a cold boot.
- [ ] Caddy local CA trust and `https://core.local/api/health` work.
- [ ] `RESCS_API_KEY` matches both gateway files; reconcile never rotates it.
- [ ] CORE binds only loopback; Caddy is the only public listener.
- [ ] nftables loads without locking out SSH.
- [ ] Owner login creates and binds a registered device; admin unlock fails
      without it.
- [ ] Service-grant changes require admin unlock and appear in the audit log.
- [ ] A queued owner action stays pending until approved from the owner device.
- [ ] Lid close does not suspend the host.
- [ ] Upgrade, rollback, backup, restore and storage-failure drills pass.
- [ ] Physical HP firmware, thermal and planned 2 x 8 GB upgrade checks pass.

## Related

- [CORE-HOST repository README](https://github.com/Kishir298/CORE-HOST/blob/main/README.md)
- [Void deployment README](https://github.com/Kishir298/RISARMS-HOST/blob/main/deployment/void/README.md)
  — lives on `RISARMS-HOST` `main` (moved from `feat/desktop-control-channel` on `CORE` at the 2026-11-21 split)
- [Hardware-gated validation](hw-gated-validation.md)
- [Update supply chain](update-supply-chain.md)
