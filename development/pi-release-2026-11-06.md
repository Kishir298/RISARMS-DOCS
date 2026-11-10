# Pi release integration — 2026-11-06

> [!NOTE]
> This page records the applied Pi release set, the local verification results,
> and the limitations that remain. It is the authoritative release note for the
> 2026-11-06 integration.

## 1. Applied releases

| Component | Version | Location | Notes |
|---|---|---|---|
| C.O.R.E. | 0.5.0 | `CORE/` | Combined `CORE-HOST/` + `CORE-CLIENT/` project; package version 0.5.0, wire/protocol compatibility stays 0.4.0 |
| A.S.I.S. | 0.1.0 | `ASIS/` | Pi policy/worker/handoff update; C.O.R.E. patch not applied because 0.5.0 supersedes it |
| A.S.C.S. | 0.3.0 | `ASCS/` | Pi headless generation-only path; C.O.R.E. integration patch not applied because 0.5.0 supersedes it |
| R.E.S.C.S. | 0.4.0 | `RESCS/` | Pi storage foundation: signed CORE owner scope, mount guard, installer/systemd unit |
| T.I.V.I.S.S. | 0.2.0 | `TIVISS/` | Unchanged; re-verified only |

`CORE/` now contains `CORE-HOST/`, `CORE-CLIENT/`, `services/{ASIS,ASCS,RESCS,TIVISS}`,
`deployment/`, `install/`, `frontend/`, `validation/`, and the release manifests.
The local `CORE-CLIENT/` clone was archived and removed. The GitHub
`CORE-CLIENT` repository was left untouched; the combined project is published
to the existing `CORE-HOST` GitHub repository.

## 2. Verification performed (macOS, Python 3.12.14)

| Suite | Result |
|---|---|
| CORE-HOST | 839 passed, 1 skipped |
| CORE-CLIENT | 200 passed |
| R.E.S.C.S. | 312 passed, 4 skipped |
| A.S.I.S. | 941 passed, 24 skipped |
| A.S.C.S. | 991 passed, 6 skipped |
| T.I.V.I.S.S. | 279 passed |

Additional checks:

- `ruff check --select F` passed for CORE-HOST, CORE-CLIENT, R.E.S.C.S., A.S.I.S., A.S.C.S., and T.I.V.I.S.S.
- `compileall` passed for the CORE host/client, deployment scripts, and service sources.
- CORE wheel entry points (`core-host`, `core-client`) installed and returned help.
- `CORE-HOST`, `CORE-CLIENT`, and `RESCS` CI YAML parsed successfully.
- R.E.S.C.S. real loopback with the CORE storage adapter passed record save/list,
  upload/download, cross-owner rejection, and soft-delete.
- A.S.C.S. Pi policy tests were made platform-independent by monkeypatching the
  Linux deployment guard; the Pi runtime itself still refuses non-Linux hosts.

## 3. Limitations and external validation still required

- **No physical Pi / ARM64 run.** The release was validated on Linux x86_64
  Python 3.12 by the release authors and re-tested on macOS x86_64. Real
  Raspberry Pi, cgroup v2, systemd boot, SSD mount/removal, cold boot, and
  disk-full recovery are not validated.
- **CORE Pi installer not executed.** `CORE/deployment/pi/install.sh` requires
  Linux ARM64, an ext4 `/srv/core` mount, root, systemd, Caddy, and `runuser`;
  it was syntax-checked only.
- **No live model, voice, cloud, or multi-host tests.** `RISALIVE` was unset.
  Live PostgreSQL/Supabase, real S3, live Ollama, live voice, Windows↔Mac LAN,
  and 24/7 endurance remain external-validation items.
- **R.E.S.C.S. 0.4.0 does not include the full local 0.3.1 line.** Owner-scoped
  record uniqueness/idempotency, monitoring exports, `python -m rescs`, and the
  RES-1..8 tests were archived in `old-versions/RESCS-0.3.1` and are not part of
  0.4.0. Device-scoped namespace/owner validation is present. Namespace/key
  uniqueness is unchanged; CORE must keep distinct service namespaces.
- **Old CORE versions are archived locally.** `old-versions/CORE-HOST-0.4.0`
  and `old-versions/CORE-CLIENT-0.4.0` are snapshots outside git. Backup tags
  `backup-pre-pi-2026-11-06` and bundles in `.backups/` provide rollback.
- **A.S.I.S./A.S.C.S. Pi mode is Linux-only and generation-only.** It does not
  enable agent tools or a TUI. A.S.C.S. desktop runtime remains Windows-oriented;
  Pi uses the headless path.
- **CORE package version vs protocol.** The package is 0.5.0, while
  `core/version.py` and the wire protocol remain 0.4.0 for compatibility. This
  is intentional; do not treat the version markers as a packaging error.
- **Patch precedence.** The ASIS CORE patch, ASCS CORE integration patch, and
  RESCS CORE signed-scope patch target older CORE snapshots and were not applied.
  CORE 0.5.0 already includes the signed RESCS scope and `/api/ai-status`.

## 4. Rollback

- Tags: `backup-pre-pi-2026-11-06` in every repository.
- Bundles: `RISARMS/.backups/<repo>-pre-pi-2026-11-06.bundle`.
- Old-version snapshots: `RISARMS/old-versions/`.
- Source ZIPs are not retained; rollback uses the git tags, bundles, and
  `old-versions/` snapshots above.
