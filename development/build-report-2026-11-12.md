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

---

# Phase 2 follow-up build — 2026-11-12

**Scope:** canonical client alignment, portal security tests, Windows/CI hardening, `TIVISS` cleanup, workspace/docs/requirements hygiene, ruff ratchet, staged commits and pushes. Hardware and soak validation could not be performed in this environment.

## 8. Canonical client and model matching

- `CORE/CORE-CLIENT` is the canonical client. The standalone `CORE-CLIENT` checkout is retained as a legacy mirror and is now aligned where practical; its `README.md` carries a legacy banner.
- `find_model` now requires exact tags in both copies. An untagged request resolves to `:latest`; the old prefix match that could select a different quantized model is gone.
- The standalone copy received the same exact-match fix and updated capability tests.

## 9. Portal security boundary tests

A negative matrix now exists in both `CORE/CORE-CLIENT/tests/test_audit_regressions.py` and standalone `CORE-CLIENT/tests/test_audit_regressions.py`:

- `Host`: foreign host, embedded credentials, path, query, and wrong port rejected; loopback and IPv6 loopback accepted.
- `Origin`: missing, wrong scheme, wrong host, wrong port, userinfo, path, query, and fragment rejected.
- Missing `X-Core-Request`, wrong content type, non-object JSON, empty body, oversized body, and invalid `Content-Length` rejected.
- Missing `Origin` is intentionally allowed only when `X-Core-Request` is present. Browsers cannot set that custom header cross-origin without a preflight, so it is the CSRF control for non-browser and same-origin callers.

## 10. Windows cancellation and CI

- Both inference suites now cover repeated `ChatStream.close()` calls; the test servers suppress Windows `ConnectionAbortedError` socket noise.
- `CORE/.github/workflows/ci.yml` runs full Windows suites for `CORE-HOST` and `CORE-CLIENT` in addition to the existing Linux jobs.
- `ASCS/.github/workflows/ci.yml` runs the full Windows suite while Ubuntu keeps the `fcntl`/Pi tests.
- Every repository now gates on `ruff check --select E9,F,I` in CI (and in release workflows where one exists).

## 11. `TIVISS` local work

The 22 modified files were reviewed and split into three commits:

1. `.gitignore` — local database and journal patterns.
2. Style/typing — import sorting and modern typing only, no behavior changes.
3. CI — ratchet the ruff gate to `E9,F,I`.

The full suite passes: **279 passed**.

## 12. Workspace, docs, and requirements hygiene

- Root `requirements.txt` was rebuilt as a complete ecosystem inventory: **47 unique dependencies** from every `pyproject.toml`/requirements manifest, including `tomli`, `tomli-w`, `prometheus-client`, `rich`, `transformers`, `build`, `pyinstaller`, and `cyclonedx-bom`.
- Root `requirements-dev.txt` was rebuilt with **7 dev/test tools**. A duplicate `ruff` entry and an invalid `pytest==9.1.1; extra == ...` marker were removed; both files parse with `packaging.requirements.Requirement`.
- `CORE/config/core.lan.yaml` (ignored local config) now points TLS paths at `CORE\CORE-HOST\tls`; the YAML validates.
- Unique files from the stale `RISARMS-DOCS/` folder were archived under `DOCS/development/archive/` (`architecture-2026-10-12.md`, `ecosystem-audit-2026-10-12.md`, plus an archive `README.md`), then the stale folder was removed.
- Removed stray workspace artifacts: `Regression Tests Added (`tests`, root `requirements/development.txt`, and the empty `rescs_storage/` and `rescs_test_storage/`. `Rewiseorist/` was left untouched.
- Removed stale `DOCS` generators and manifests: `write_full.py`, `write_req.py`, `write_requirements.py`, `extract_sections.py`, `fix_requirements.py`, `requirements-no-host.txt`, and `requirements-no-client.txt`.
- `DOCS/requirements.txt` now points at the root `requirements.txt` instead of duplicating a stale list.
- `CORE/config/core.lan.yaml` remains ignored and machine-local; it is not committed.

## 13. Ruff ratchet

`ruff check --select E9,F,I` is green in every repository:

| Repository | `E9,F,I` | Default `ruff check` |
|---|---|---|
| `CORE/CORE-HOST` | pass | pass |
| `CORE/CORE-CLIENT` | pass | pass |
| `CORE-CLIENT` (standalone) | pass | pass |
| `ASCS` | pass | pass |
| `RESCS` | pass | pass |
| `ASIS` | pass | 504 findings (documented backlog) |
| `TIVISS` | pass | 147 findings (documented backlog) |

The `ASIS` and `TIVISS` broad-rule backlogs are recorded in the Phase 2 audit list rather than mass-fixed.

## 14. Phase 2 test results

| Repository | Command | Result |
|---|---|---|
| `CORE/CORE-HOST` | `python -m pytest -q --tb=short` | **837 passed, 7 skipped** |
| `CORE/CORE-CLIENT` | `python -m pytest -q --tb=short` | **235 passed, 1 skipped** |
| `CORE-CLIENT` (standalone) | `.venv\Scripts\python -m pytest -q --tb=short` | **185 passed** |
| `ASCS` | `.venv\Scripts\python -m pytest -q --tb=short` | **982 passed, 22 skipped** |
| `ASIS` | `.venv\Scripts\python -m pytest -q --tb=short` | **948 passed, 19 skipped** |
| `RESCS` | `.venv\Scripts\python -m pytest -q --tb=short` | **314 passed, 4 skipped** |
| `TIVISS` | `.venv\Scripts\python -m pytest -q --tb=short` | **279 passed** |

## 15. Phase 2 commits

| Repository | Commits |
|---|---|
| `CORE` | `5d6f1bf` portal/repeated-cancel tests · `5702373` Windows CI + ruff gate · `c1eaaaa` import sorting |
| `CORE-CLIENT` (standalone) | `4f9dbbd` exact model tags · `b4628fb` portal rejection matrix · `7b218df` CI gate + import sorting |
| `ASCS` | `cb4289d` Windows CI + ruff gate · `d8900a9` import sorting |
| `ASIS` | `1501bcf` ruff gate · `00564c6` import sorting |
| `RESCS` | `079df86` ruff gate · `f1f1918` import sorting |
| `TIVISS` | `bfce61c` `.gitignore` · `42d777b` style/typing · `06acf81` CI gate |
| `DOCS` | this report, the updated audit list, the Phase 2 audit list, and the archive cleanup |

All commits are normal fast-forward pushes; no history was rewritten and no force-push was used.

## 16. Safety

- Secret-pattern scans of the staged diffs found no private keys, tokens, passwords, or cloud credentials.
- `.gitignore` coverage was audited in every repository: `.env*`, TLS keys/certs, device files, and SQLite databases/journals are ignored. Tracked matches were code/docs only.
- Root `requirements.txt`, `requirements-dev.txt`, and the workspace TODO files live outside any git repository; they are recorded here because they cannot be pushed.
- `Rewiseorist/` remains a separate repository and was not modified.

## 17. Not performed (environment limits)

- Physical Raspberry Pi / ARM64 validation for `CORE`, `ASCS`, and `RESCS`.
- Windows ↔ Mac LAN/TLS validation (certificate trust, firewall, reconnect).
- 24/7 endurance, reconnect-storm, disk-full, and log-rotation soak testing.

See [audit-todo-2026-11-12-phase2.md](audit-todo-2026-11-12-phase2.md) for the remaining ranked work.
