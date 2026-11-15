# Void Linux host — HP 14

> [!NOTE]
> This is the canonical deployment target for the HP 14: **Void Linux x86_64
> glibc, headless**, co-hosting C.O.R.E. and R.E.S.C.S. behind Caddy. It has not
> been executed on the physical HP 14 yet.

## Layout

| Item | Path |
|---|---|
| Service account | `risarms` (no login shell) |
| C.O.R.E. data | `/var/lib/risarms/core` |
| R.E.S.C.S. data | `/var/lib/risarms/rescs` |
| C.O.R.E. frontend | `/var/lib/risarms/frontend` |
| Configuration | `/etc/risarms/{core.env,rescs.env,gateway.json}` (canonical) and `/var/lib/risarms/core/gateway.json` (CORE runtime copy) |
| Logs | `/var/log/risarms/{core,rescs}` |
| Virtual environments | `/opt/risarms/{core-venv,rescs-venv}` |
| Backups | `/var/lib/risarms/backups` |
| Caddy site | `/etc/caddy/risarms/portal.caddy` |

C.O.R.E. listens on `127.0.0.1:8780` (API) and `127.0.0.1:8781` (WebSocket).
R.E.S.C.S. listens on `127.0.0.1:8081`. Caddy terminates TLS on `443`; the
firewall exposes only `443`, SSH and mDNS.

## Install

```sh
sudo xbps-install -S python3 caddy runit-void nftables avahi elogind
sudo bash CORE/deployment/void/install.sh
```

The installer refuses to overwrite existing configuration or keys. On first
run it generates one `RESCS_API_KEY` and writes the same gateway to
`/etc/risarms/gateway.json` and `/var/lib/risarms/core/gateway.json`; CORE and
R.E.S.C.S. must always use the key in `/etc/risarms/rescs.env`. On later runs it
verifies both copies, adopts the canonical file only when the runtime copy is
absent, and fails loudly instead of rotating keys when they disagree. Repair a
mismatch by aligning both files to `RESCS_API_KEY` manually, then re-run the
installer.

It installs runit service directories but does **not** enable them. Review the
generated origin and paths first, then:

```sh
sudo ln -s /etc/sv/risarms-rescs /var/service/
sudo ln -s /etc/sv/risarms-core /var/service/
sudo ln -s /etc/sv/caddy /var/service/
sudo sv status risarms-core risarms-rescs caddy
```

Read the first-owner setup key from `/var/log/risarms/core/current`, then open
`https://core.local` and trust the Caddy local CA on each client before entering
credentials. If a real DNS name is used, change `CORE_PUBLIC_ORIGIN`, the
Caddy site address and `gateway.json.public_origin` together.

## Host hardening

- nftables: the installer copies `risarms.nft` into `/etc/nftables.d/`, but it
  cannot safely edit every host's base ruleset. Add
  `include "/etc/nftables.d/*.nft"` to `/etc/nftables.conf` (or include the file
  explicitly), review the SSH rule, and run `sudo nft -f /etc/nftables.conf`.
  Do not enable the firewall until the SSH rule is verified.
- elogind: `HandleLidSwitch=ignore` keeps the headless host awake with the lid
  closed. Apply with `sudo sv restart elogind` or reboot.
- Avahi advertises the host on the LAN. Disable it if mDNS is not wanted.
- Caddy uses `tls internal`; for a public name, replace it with an ACME-enabled
  site and open only `443`.

## Operate

```sh
sudo sv status risarms-core risarms-rescs caddy
sudo sv down risarms-core risarms-rescs
sudo sv up risarms-rescs risarms-core
sudo /usr/local/sbin/risarms-backup
```

Backups stop CORE first, then RESCS, archive both data trees, and restart RESCS
before CORE. Keep backups off the host.

## Update order

1. Take a backup.
2. Stop CORE, then RESCS.
3. Install the signed RESCS release into `/opt/risarms/rescs-venv`.
4. Install the signed CORE release into `/opt/risarms/core-venv`.
5. Start RESCS and check `http://127.0.0.1:8081/health/ready`.
6. Start CORE and check `https://core.local/api/health`.
7. Roll back the previous virtual environments if either health check fails.

Never auto-apply an owner action or an update. Signed update manifests and
Ed25519 verification are tracked separately in the updater workstream.

## Validation checklist

- [ ] `sv status` shows both services up after a cold boot.
- [ ] `RESCS_API_KEY` matches both gateway files; a reconfigure never rotates it.
- [ ] CORE binds only loopback; Caddy is the only public listener.
- [ ] Owner login creates and binds a registered device; admin unlock fails
      without it.
- [ ] Service-grant changes require admin unlock and appear in the audit log.
- [ ] A queued owner action stays pending until approved from the owner device.
- [ ] RESCS health is checked before CORE starts.
- [ ] Lid close does not suspend the host.
- [ ] Backup restore is tested on a second directory.
