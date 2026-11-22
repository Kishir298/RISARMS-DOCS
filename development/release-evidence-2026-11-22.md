# Release evidence — 2026-11-22

Every claim here names the run and the artifact revision it came from. Evidence
classes are kept apart:

- **CI build** — a workflow produced and checksummed the artifact.
- **Container** — the artifact was installed and exercised in
  `ghcr.io/void-linux/void-glibc-full`. This is not a booted system and not
  hardware.
- **Booted system** — installed on a running OS, rebooted, services supervised
  by the init system across a reboot. **Not performed.**
- **Hardware** — exercised on the reference machine (HP 14) or a real LAN.
  **Not performed.**

## 1. Pinned component revisions

`RISARMS-HOST/components.lock.json` pins six components. Each pin names a commit
whose own repository CI passed:

| Component | Revision | Own CI |
|---|---|---|
| CORE-HOST | `33963b007b12630c2ad4f37985ab5327efad1a8a` | CI 45007023219 success |
| CORE-CLIENT | `a060bdbd0a14beb6e68bcec06053e58edb16fad5` | CI 44887572906 success |
| RESCS | `6b8e78084c1dbed1ef643f4dc0f6412b8b79b90c` | CI 45011800457 success on `main` |
| ASCS | `aaeb6515dc4d10adce1b42c459affb98770e556f` | CI 45011809574 success on `main` |
| ASIS | `00564c614f6a4241abc9b31fb821529272e4db4c` | CI 43176766339 success |
| TIVISS-HOST | `d3c5b65df332416af942a7abf60133a03ca05665` | CI 44992652858 success |

## 2. CORE server bundle

Run [45013778229](https://github.com/Kishir298/RISARMS-HOST/actions/runs/45013778229)
(`main` @ `337e36a`, `workflow_dispatch`, channel `beta`). All jobs passed; the
draft-release job is tag-gated and skipped, so nothing was published.

- Artifact: `CORE-Server-0.6.0-void-x86_64.tar.gz`,
  SHA-256 `db097bc4cce83b36b4f24092b4826f1132dd19cab221af085a6898ca05bc52f7`
- `provenance.json` resolves all six revisions in §1 (verified in the downloaded
  statement, not just in the lock file).
- Container image `ghcr.io/void-linux/void-glibc-full@sha256:e98f8cdd…`.
- Assembly is byte-reproducible: the workflow re-assembles and `cmp`s the
  archive; locally, two staged trees produced identical archives (1,385
  entries).

Container report (`container-install-report.txt`, 30 PASS, 0 FAIL):

| Check | Result |
|---|---|
| Archive checksums, runtime packages, installer | PASS |
| Pinned core version imports, `core-host`/`rescs` console scripts run | PASS |
| `risarms-core` and `risarms-rescs` `run:` under runit | PASS |
| Caddy serves the installed config; TLS via internal CA; HTTP→HTTPS 308 | PASS |
| `risarms-backup` archive; `risarms-restore` returns a deleted asset byte-identically | PASS |
| Upgrade to a synthetic newer version stays healthy; rollback returns healthy | PASS |
| `risarms-doctor` after upgrade/rollback | PASS |
| Free-space refusal at install/upgrade preflight | PASS |

Not verified by this run: reboot persistence, nftables load (`nft` needs
`NET_ADMIN`, unavailable in the container), physical LAN, endurance, and the
packaged Void `caddy` runit service (it cannot create `supervise/` in that
image; the RISARMS-installed Caddy configuration was verified by starting Caddy
with a fixed data directory).

### Defects found and fixed by this run

1. Pins named failing or superseded commits (CORE-HOST `8021b3b`, RESCS
   `f1f1918`, ASCS `d8900a9`). RESCS/ASCS `main` was fast-forwarded to the green
   fix commits so the pin is on `main` itself.
2. `risarms-backup` archived `etc/sv/*/supervise`, runit's live control state.
   Restoring it killed the supervisor (`runsv not running`) and both services.
   Backups now exclude it and restore skips it, so older archives are safe.

## 3. Desktop installers

Build run [45012833473](https://github.com/Kishir298/RISARMS-ui/actions/runs/45012833473)
(`main` @ `18c38aa`, `validation_build=true`) produced macOS Intel/Apple Silicon
zip+dmg, Windows zip+`-setup.exe`+`.msi`, and Linux tar.gz+deb on all four
platforms. The release job is tag-gated and skipped.

Verification run
[45013788806](https://github.com/Kishir298/RISARMS-ui/actions/runs/45013788806)
consumed that artifact set:

- `sha256sum -c` re-verified `RISARMS-Portal-0.6.0-linux-x86_64.tar.gz` and
  `risarms-portal_0.6.0_amd64.deb` in CI: OK.
- The `.deb` installed through `apt` (`risarms-portal 0.6.0`), and the installed
  `/opt/risarms-portal/risarms-ui` ran from a different working directory.
- `--doctor` under Xvfb: `tkinter: Tk 8.6`, `display: available`, websockets and
  cryptography present; `result: not ready: keyring` because a CI runner has no
  SecretService.
- The GUI process stayed up for the full 20 s timeout under Xvfb.
- Messaging e2e against a real `core web` process at the pinned CORE-HOST
  revision passed (2 tests: two-client HTTP+WSS delivery and its companion).

Defect found and fixed: the Linux artifact could not start at all —
`ModuleNotFoundError: No module named '_struct'`. `actions/setup-python` exported
`LD_LIBRARY_PATH` to its own libpython while the Linux build created its venv
from `/usr/bin/python3` for Tk support, so PyInstaller mixed two Python 3.12
toolchains. Linux now uses only the distribution Python, and `build.py` runs the
frozen executable with `--version` so an unstartable bundle fails the build.

Artifacts still carry `VALIDATION-ONLY` notices because no production update key
exists.

## 4. Blocked, unchanged

- `UPDATE_PUBLIC_KEY` and `UPDATE_SIGNING_KEY`: absent (repository variables and
  secrets both list zero entries). Production desktop release stays fail-closed.
- Apple Developer ID/notarization and Windows code signing: no credentials.
- Booted Void system: install-under-reboot, `/var/service` persistence, Caddy
  under the packaged service, nftables load, storage exhaustion at runtime.
- Physical HP 14 / LAN matrix / 24-7 endurance.
- HP 14 installed RAM unverified; the 2×8 GB → 16 GB upgrade is still planned,
  not installed.
