# Audit / Fix To-Do — 2026-11-22

**Status:** residual list after the pin reconciliation, container runtime
extension and desktop install verification. Ranked by risk.
**Priority legend:** `P0` blocking/security · `P1` should be next · `P2` hygiene · `P3` later.
**Evidence baseline:** [release evidence 2026-11-22](release-evidence-2026-11-22.md).

## P0 — Blocking, needs credentials or hardware

- [ ] **0.1 Provision the production update keys.** `UPDATE_PUBLIC_KEY` and
  `UPDATE_SIGNING_KEY` do not exist (repository variables and secrets both list
  zero entries). Until they do, every desktop build is `VALIDATION-ONLY` and no
  `update.json` is produced, so the signed auto-update channel is unimplemented
  end to end. gh authentication cannot supply these keys.
- [ ] **0.2 Acquire OS code-signing identities.** Apple Developer ID +
  notarization for the DMG/zip, a Windows code-signing certificate for the EXE
  and MSI. These are separate from update signing and are why beta artifacts are
  labelled ad-hoc/unsigned.
- [ ] **0.3 Booted Void validation.** Install the archive on the HP 14, enable
  `/var/service` links, reboot, and confirm services survive; then exercise
  Caddy, nftables load and storage exhaustion on a real disk. Container evidence
  covers install, TLS, backup/restore and upgrade/rollback but not a boot.

## P1 — Verification gaps found by this round

- [ ] **1.1 Packaged Void `caddy` runit service.** In `void-glibc-full` it cannot
  create `supervise/` (`runsv caddy: fatal: unable to open supervise/lock`), so
  the installer's instruction to enable it is unproven. Confirm on real Void and
  either document the requirement or fix the installer if the service needs a
  prepared data directory or user home.
- [ ] **1.2 nftables ruleset load.** Even `nft -c` needs a netlink cache, so no
  environment yet proves the ruleset parses or loads. Requires `NET_ADMIN` or a
  real host.
- [ ] **1.3 macOS and Windows installer execution.** Only archives are built for
  those platforms; mounting the DMG, running the EXE and installing the MSI are
  unverified, and the Linux-only smoke job is the only install evidence.
  Extending `desktop-smoke.yml` with macOS/Windows jobs is the natural next step.
- [ ] **1.4 GUI interaction flows.** The GUI process is proven to start on
  Linux/Xvfb, and messaging is proven at the protocol level, but login,
  connection, reconnection and file/message interaction in the window are not
  driven by any automated test.
- [ ] **1.5 Downgrade and cross-version migration.** Upgrade/rollback is proven
  with a synthetic version bump of the same code; no test covers a real schema or
  data migration between releases, or rollback after a failed migration.

## P2 — Hygiene

- [ ] **2.1 Physical LAN matrix and 24/7 endurance.** Void host ↔ desktop clients
  on macOS Intel/Apple Silicon, Windows and Linux; reconnect storms, disk-full,
  log rotation under load. Single-machine workspace cannot cover this.
- [ ] **2.2 HP 14 installed RAM and the 2 × 8 GB → 16 GB upgrade.** Still
  unverified and still PLANNED; record the actual configuration when the machine
  is next available.
- [ ] **2.3 `integration-tests/` has no remote.** The workspace directory is not
  published; decide whether it becomes a repository or is folded into an
  existing one.
- [ ] **2.4 Container test runtime.** The extended check now rebuilds two venvs
  for the upgrade/rollback step; keep an eye on the CI job duration and split it
  if it approaches the job timeout on slower runners.

## Done in this round

- Pins reconciled: CORE-HOST `33963b0`, RESCS `6b8e780`, ASCS `aaeb651`; each
  names a revision with passing CI in its own repository.
- Container checks extended to Caddy TLS, HTTP→HTTPS redirect, backup/restore,
  free-space refusal, upgrade/rollback and `risarms-doctor` — 30/30 pass.
- Backups no longer archive runit's `supervise/`; restore skips it.
- Linux desktop binary fixed (`_struct` mixed-toolchain failure), build now
  refuses to ship an unstartable bundle, and the `.deb` install + GUI launch +
  messaging e2e are verified in CI.
