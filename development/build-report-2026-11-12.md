# Build Report — 2026-11-12

**Workspace:** `C:\Users\rishi\Desktop\RISARMS` (Windows)
**Scope:** sync active repositories, rename `CORE-HOST/` to `CORE/`, fix failing tests and safety gaps, verify every repository, commit and push in stages.

## 1. Repository sync results

| Repository | Action | Result |
|---|---|---|
| `ASIS` | fast-forward | `16976ed..6ee0aed` |
| `ASCS` | merge origin | merge commit `4113bcb` from `e23c36b` |
| `CORE` (formerly `CORE-HOST`) | fast-forward | `3844ff5..fd05c44`, then renamed the working folder |
| `DOCS` | fast-forward | `ad40fc3..237dd9c` |
| `RESCS` | fast-forward | `dfa7ff2..8b55a55` |
| `TIVISS` | intentionally skipped | local work preserved at `53b0cb3` |
| `CORE-CLIENT` (standalone) | intentionally skipped | local work preserved at `acf3f53` |

No pull conflicts occurred. `TIVISS` and the standalone `CORE-CLIENT` checkout were not pulled because both contained local edits.

## 2. `CORE-HOST/` → `CORE/` rename

- The top-level `CORE-HOST/` folder (including its `.git`) was renamed to `CORE/`.
- `CORE/` is now the combined project root and still contains the internal `CORE-HOST/` and `CORE-CLIENT/` subdirectories, plus `services/`, `deployment/`, `install/`, and `validation/`.
- The editable install was refreshed with `python -m pip install -e CORE/CORE-HOST`; `core` reports `0.5.0` and imports from `CORE\CORE-HOST\core`.
- Active references were updated in `DOCS/AGENT.md`, `DOCS/README.md`, `DOCS/development/contribution.md`, root `requirements.txt`, and `skills/risarms-repo-sync/SKILL.md`.
- Internal `CORE-HOST/` references inside `CORE/.github/`, `CORE/BUILDING.md`, `CORE/RELEASE-MANIFEST.json`, and release evidence were intentionally left unchanged because they refer to the internal subdirectory.
- Removed the bytecode-only `CORE/core/` and empty `CORE/client/` legacy trees after confirming `CORE/core/` contained 0 `.py` files (the `AGENT.md` stale-tree rule).

## 3. Fixes and changed files

### CORE — commit `a186668`

- `CORE-HOST/core/inference.py` — on Windows, detach a blocked stream socket and close its handle through Winsock so `ChatStream.close()` wakes a reader; removed the redundant first-token `remaining()` check.
- `CORE-CLIENT/client/inference.py` — same cancellation fix.
- `CORE-HOST/tests/application/test_application_orchestration.py` — configuration and restart tests now create their own `config/core.yaml` under `tmp_path` instead of depending on an ambient file.
- `CORE-HOST/tests/test_pi_resources.py` — three `/proc`/`fcntl` tests are skipped on non-Linux.
- `.gitignore` — ignore local SQLite databases and journals.

### CORE-CLIENT (standalone) — commit `364c882`

- `client/portal/server.py` — loopback-only bind, IPv6 loopback support, Host and Origin validation, `X-Core-Request` CSRF header requirement, strict JSON bodies, `record_get` namespace/key contract, AI offload `device_id` and failure propagation, and dashboard request headers.
- `client/models.py` — exact model matching with `:latest` default and tagged prefix matching for quantized variants.
- `client/core_device_client.py` — wrap invalid remembered values in `DeviceClientError`, close the raw socket when TLS setup fails, derive the default platform from the OS, and drop unused handshake locals. This file also contains the pre-existing local frame-deadline receive work from the working tree.
- `tests/test_client_portal.py`, `tests/test_cli.py`, `tests/test_protocol.py` — updated for CSRF/origin headers, platform defaults, and the lint fix.
- `.gitignore` — ignore local SQLite databases and journals.

### ASCS — commit `73e1f03`

- `tests/integration/test_pi_policy.py` — `fcntl`-dependent Pi inference-lock tests are Linux-only.
- `.gitignore` — ignore local SQLite databases and journals.

### RESCS — commit `e22d26d`

- `.gitignore` — ignore SQLite databases and journals in addition to `*.db`.

### DOCS — this commit

- `AGENT.md` — Windows workspace path, `DOCS/` repository name, six active repos, sync commands use `CORE` and `DOCS`.
- `README.md` — repository tree shows `DOCS/`.
- `development/contribution.md` — `DOCS/` naming and remote note.
- `.gitignore` — local SQLite database/journal patterns.
- `development/build-report-2026-11-12.md` — this report.
- `development/audit-todo-2026-11-12.md` — remaining work list.

### Workspace root (not a git repository)

- `AGENT.md` — stub now points at six parallel sub-agents and cleans up the double-period typo.
- `requirements.txt` — editable install paths now use `CORE/CORE-HOST` and `CORE/CORE-CLIENT`; standalone checkout marked optional.
- `skills/risarms-repo-sync/SKILL.md` — six active repos, `CORE` replaces `CORE-HOST`, updated table and output template.
- `TODO_BUILD_2026-11-12.md` — ranked build plan with final status.
- `TODO_AUDIT_2026-11-12.md` — copy of the remaining-work list.

## 4. Test results

| Repository | Command | Result |
|---|---|---|
| `CORE/CORE-HOST` | `python -m pytest -q --tb=short` | **836 passed, 7 skipped** |
| `CORE/CORE-CLIENT` | `python -m pytest -q --tb=short` | **199 passed, 1 skipped** |
| `CORE-CLIENT` (standalone) | `.venv\Scripts\python -m pytest -q --tb=short` | **149 passed** |
| `ASCS` | `.venv\Scripts\python -m pytest -q --tb=short` | **exit 0** (Pi/`fcntl` tests skipped on Windows) |
| `ASIS` | `.venv\Scripts\python -m pytest -q --tb=short` | **exit 0** |
| `RESCS` | `.venv\Scripts\python -m pytest -q --tb=short` | **314 passed, 4 skipped** |
| `TIVISS` | `.venv\Scripts\python -m pytest -q --tb=short` | **279 passed** |

Focused checks:

- `CORE/CORE-HOST/tests/test_inference_policy.py` — 11 passed.
- `CORE/CORE-CLIENT/tests/test_inference_policy.py` — 10 passed.
- `CORE/CORE-HOST/tests/application/test_application_orchestration.py` — 11 passed.
- `CORE/CORE-HOST/tests/test_pi_resources.py` — 7 passed, 3 skipped.
- `CORE-CLIENT/tests/test_client_portal.py` — 11 passed.
- `CORE-CLIENT/tests/test_audit_regressions.py` — 12 passed.
- `CORE-CLIENT/tests/test_installed_command.py` — 8 passed.

## 5. Lint results

`ruff check --select F` (the release lint gate) passes in `CORE/CORE-HOST`, `CORE/CORE-CLIENT`, `CORE-CLIENT`, `ASCS`, `RESCS`, `ASIS`, and `TIVISS`. Three pre-existing unused-variable findings in the standalone `CORE-CLIENT` were fixed to reach that gate.

The broader default `ruff check` still reports large pre-existing style backlogs in every repository (for example 482 findings in `CORE/CORE-HOST` and 527 in `ASIS`). These are recorded in the audit to-do rather than mass-fixed here.

## 6. Safety

- SQLite database and journal patterns were added to `CORE`, `ASCS`, and `RESCS`; `CORE-CLIENT`, `DOCS`, and `TIVISS` already contained them.
- A secret-pattern scan of every staged diff found no private keys, tokens, passwords, or cloud credentials.
- No history rewrite and no force-push were performed.
- `TIVISS` local changes (22 files) were left uncommitted and untouched.
- The standalone `CORE-CLIENT` local frame-deadline work was preserved and committed together with the fixes; it is noted in the commit body.

## 7. Remaining work

See [audit-todo-2026-11-12.md](audit-todo-2026-11-12.md).
