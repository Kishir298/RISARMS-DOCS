# Ubuntu Server 24.04 candidate — x86_64/systemd

> [!NOTE]
> **Status: CANDIDATE, NOT a release target.** This is an additive Ubuntu
> Server **24.04 LTS x86_64** port with systemd, merged into the RISARMS-HOST
> umbrella under `deployment/ubuntu/`. Static tests, shell syntax checks and a
> reproducible candidate archive exist; the install, service startup, reboot,
> Caddy TLS, backup/restore, upgrade/rollback and physical hardware runs have
> **not** been executed. The canonical CORE 0.6.0 server target remains
> [Void Linux](void-linux.md). Never describe this candidate as validated.

## Where the files live

| Item | Path |
|---|---|
| Umbrella repository | `RISARMS-HOST` (GitHub `Kishir298/RISARMS-HOST`; local folder `RISARMS-HO`) |
| Deployment assets | `deployment/ubuntu/` (installer, lib, doctor, backup/restore/upgrade/rollback, systemd units, Caddy site, `configure.py`, `validate-backup.py`) |
| Archive builder | `risarms_host/ubuntu_release.py` → `CORE-Server-<version>-ubuntu24.04-x86_64.tar.gz` |
| CI workflow | `.github/workflows/ubuntu-candidate.yml` (manual dispatch only; never publishes) |
| Integration record | `UBUNTU-PORT-FILES.md` (repository root) |
| Tests | `tests/test_ubuntu_port.py` |

The Void release workflow (`.github/workflows/release.yml`) and the Void
installer are unchanged; the Ubuntu candidate writes its own
`compatibility.json` (`server_deployment.distribution: ubuntu`, role
`server-candidate`) into its own archive only.

## Layout

Same fixed paths as the Void target; custom install paths are refused:

| Item | Path |
|---|---|
| Service account | `risarms` (no login shell, shared by CORE and RESCS) |
| Versioned environments | `/opt/risarms/venvs/<version>/{core,rescs}` |
| Stable environment links | `/opt/risarms/{core-venv,rescs-venv}` |
| C.O.R.E. data | `/var/lib/risarms/core` |
| R.E.S.C.S. data | `/var/lib/risarms/rescs` |
| C.O.R.E. frontend | `/var/lib/risarms/frontend` |
| Configuration | `/etc/risarms/{core.env,rescs.env,gateway.json}` |
| Logs | `/var/log/risarms/{core,rescs}` (journald + files) |
| Install state and snapshots | `/var/lib/risarms/install-state` |
| Backups | `/var/lib/risarms/backups` |
| Caddy site | `/etc/caddy/risarms/portal.caddy` |
| systemd units | `/etc/systemd/system/{risarms-core,risarms-rescs}.service` (hardened: `NoNewPrivileges`, `ProtectSystem=strict`, `ProtectHome`, `UMask=0077`, `ReadWritePaths` scoped) |

C.O.R.E. listens on `127.0.0.1:8780` (API) and `127.0.0.1:8781` (WebSocket);
R.E.S.C.S. on `127.0.0.1:8081`; Caddy terminates TLS on `443`. The installer
does not load firewall rules; preserve SSH access before enabling any
UFW/nftables policy.

## Build (development machine)

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -e '.[test]'
.venv/bin/python -m pytest -q
.venv/bin/python -m risarms_host.ubuntu_release --out build/ubuntu
```

Or dispatch the **Ubuntu server candidate** workflow in GitHub Actions; it
builds artifacts only — no install, no release, no signing claim.

## Install (disposable 24.04 VM first)

```sh
sudo apt update
sudo apt install python3 python3-venv python3-pip caddy nftables ca-certificates
sha256sum -c SHA256SUMS
tar -xzf CORE-Server-0.6.0-ubuntu24.04-x86_64.tar.gz
cd CORE-Server-0.6.0-ubuntu24.04-x86_64
sudo ./deployment/ubuntu/install.sh
```

The installer refuses an existing Void deployment, refuses same-version
installs, writes units but does **not** enable them. Review
`/etc/risarms/*.env` and `/etc/caddy/risarms/portal.caddy`, then:

```sh
sudo systemctl enable --now risarms-rescs risarms-core caddy
sudo systemctl restart caddy
sudo risarms-doctor
```

First-owner setup keys appear in `journalctl -u risarms-core`. Never share
logs containing keys; trust only the public Caddy root CA on clients.

## Operate

```sh
sudo risarms-backup
sudo risarms-restore --yes /var/lib/risarms/backups/risarms-<stamp>.tar.gz
sudo risarms-upgrade /path/to/extracted-NEW-version
sudo risarms-rollback
sudo risarms-doctor
```

Backups stop services, archive `/etc/risarms`, both data trees, the Caddy
site/`Caddyfile` and the units, write mode `0600`, are not encrypted, and keep
14-day retention by default. Same-version upgrades are refused; rollback
switches versioned venv symlinks and does not reverse database changes — use
`risarms-restore` for data.

## Validation checklist (all pending)

- [ ] Fresh install on a disposable booted 24.04 VM completes.
- [ ] `systemctl status` shows services up after a cold boot.
- [ ] Caddy local CA trust and `https://core.local/api/health` work.
- [ ] `RESCS_API_KEY` matches both gateway files; reconcile never rotates it.
- [ ] CORE binds only loopback; Caddy is the only public listener.
- [ ] Firewall/SSH reachability preserved with the operator's policy.
- [ ] Backup/restore, newer-version upgrade and rollback drills pass.
- [ ] Low-space refusal and failure recovery behave like the Void target.
- [ ] Repeat on the HP reference machine before any draft prerelease.

After validation, an explicitly marked draft prerelease may be created from the
verified CI artifacts under an Ubuntu-specific tag (for example
`ubuntu-v0.6.0-beta.1`) so the Void `v*` workflow is not triggered. No draft or
release was created while preparing this candidate.

## Related

- [Void Linux host](void-linux.md) — canonical CORE 0.6.0 server target
- [Hardware-gated validation](hw-gated-validation.md)
- [Cross-platform release engineering](cross-platform-release.md)
- RISARMS-HOST: `deployment/ubuntu/README.md`, `UBUNTU-PORT-FILES.md`
