# Audit / Fix To-Do — 2026-11-12

**Status:** follow-up list after the 2026-11-12 build and Phase 2 follow-up. Ranked by risk and effort.
**Priority legend:** `P0` blocking/security · `P1` should be next · `P2` hygiene · `P3` later.
**Phase 2 results:** see [build-report-2026-11-12.md](build-report-2026-11-12.md) and the remaining-work list in [audit-todo-2026-11-12-phase2.md](audit-todo-2026-11-12-phase2.md).

## P0 — Security / correctness

- [x] **0.1 Review the standalone `CORE-CLIENT` vs `CORE/CORE-CLIENT` divergence.** `CORE/CORE-CLIENT` is canonical; the standalone checkout is a legacy mirror. Exact model matching, portal tests, and CI gates were aligned in both copies. Retiring the duplicate remains open as item 5.1.
- [x] **0.2 Add explicit negative tests for the portal security boundary.** Both copies now cover foreign/credentialed/path/query/wrong-port `Host`, missing/wrong-scheme/wrong-host/wrong-port/userinfo/path/query/fragment `Origin`, missing `X-Core-Request`, wrong content type, non-object/empty/oversized/invalid-length JSON, and the IPv6 positive case. Missing `Origin` is allowed only with `X-Core-Request`.
- [ ] **0.3 Validate the Windows cancellation fix on a real long-running stream.** The regression test uses a short-lived local server and now covers repeated cancels. Confirm cancel returns promptly while Ollama is generating on Windows and that the detached socket does not leak handles over a long session.
- [x] **0.4 Decide whether `CORE/config/core.lan.yaml` should be updated locally.** The ignored machine-local file now points TLS paths at `CORE\CORE-HOST\tls` and validates as YAML.

## P1 — Verification gaps

- [ ] **1.1 Physical Raspberry Pi / ARM64 validation.** `CORE` host/client, `ASCS` Pi generation path, and `RESCS` signed-scope/mount validation still need real hardware runs. The `fcntl`-dependent tests are skipped on Windows and must run on Linux.
- [ ] **1.2 Windows ↔ Mac LAN/TLS validation.** Exercise the real TLS listener, certificate trust, firewall rule, reconnect, and portal loopback assumptions on two machines.
- [ ] **1.3 Extended 24/7 operation.** Run endurance, reconnect-storm, disk-full, and log-rotation checks; the current suites are deterministic unit/integration tests, not soak tests.
- [x] **1.4 Add a CI matrix for Windows and Linux.** `CORE` runs full Windows suites for host and client alongside Linux; `ASCS` runs a Windows full suite alongside Ubuntu for the `fcntl`/Pi tests. `ASIS`, `RESCS`, and `TIVISS` still only gate lint, so a full Windows test job there remains open.
- [ ] **1.5 Add a regression test for `_recv_exact` deadline expiry with a partially received frame.** The local frame-deadline work has one timeout-recovery test; add the deadline-exceeded path and the no-data timeout path.

## P1 — Repository hygiene

- [ ] **2.1 Reduce the broad ruff backlog.** The blocking gate is now `E9,F,I` and passes everywhere. Default `ruff check` is clean in `CORE/CORE-HOST`, `CORE/CORE-CLIENT`, standalone `CORE-CLIENT`, `ASCS`, and `RESCS`; `ASIS` reports 504 findings and `TIVISS` 147. Either adopt a shared explicit rule set with a baseline or fix incrementally by directory.
- [x] **2.2 Review and commit or discard the 22 modified `TIVISS` files.** Reviewed and committed in three stages: `.gitignore`, style/typing, and the CI ruff gate. Full suite passes (279).
- [x] **2.3 Fix or remove stale generator scripts in `DOCS/`.** Removed `write_full.py`, `write_req.py`, `write_requirements.py`, `extract_sections.py`, `fix_requirements.py`, `requirements-no-host.txt`, and `requirements-no-client.txt`; `DOCS/requirements.txt` now points at the root manifest.
- [x] **2.4 Decide what to do with the stale `RISARMS-DOCS/` folder.** The two unique files were archived under `DOCS/development/archive/` with an archive README, then the stale folder was removed.
- [ ] **2.5 Remove duplicate `.gitignore` entries.** Several repos still list `*.key`, `.pytest_cache/`, and `__pycache__/` more than once. Cosmetic, but it makes future audits noisier.
- [ ] **2.6 Version workspace-level files.** Root `requirements.txt`, `requirements-dev.txt`, `skills/`, and the build/audit to-dos are still outside any git repository. Move them into `DOCS/` or create a small workspace repository if they should be tracked.
- [x] **2.7 Review remaining workspace-root clutter.** Removed `Regression Tests Added (`tests`, root `requirements/development.txt`, and the empty `rescs_storage/` and `rescs_test_storage/`. `Rewiseorist/` was intentionally left untouched.

## P2 — Documentation / naming

- [ ] **3.1 Add the Windows baseline to the docs.** `DOCS/README.md` and `DOCS/development/testing.md` still quote macOS/Linux counts (839 host / 200 client). The current Windows baseline is 837 host + 7 skipped, 235 bundle client + 1 skipped, and 185 standalone client; label historical counts clearly and link the build report.
- [ ] **3.2 Keep `CORE-HOST` naming consistent.** The internal folder, package, GitHub remote, and historical release notes still use `CORE-HOST`; active paths use `CORE/`. Add a short naming note to `DOCS/README.md` so future edits do not reintroduce top-level `CORE-HOST/` paths.
- [ ] **3.3 Refresh `DOCS/development/pi-release-2026-11-06.md` only if it is still active.** It is a historical release record; do not rewrite its test counts. Add a superseded-by link if the release is no longer current.
- [ ] **3.4 Document the portal security model.** The client portal is loopback-only and has no remote authentication; write down the Host/Origin/CSRF assumptions and the threat model as a standalone document so future changes do not weaken them.

## P2 — Code quality

- [ ] **4.1 Deduplicate the inference `ChatStream` implementation.** `CORE/CORE-HOST/core/inference.py` and `CORE/CORE-CLIENT/client/inference.py` carry near-identical cancellation logic; consider a shared helper or a contract test that runs both.
- [x] **4.2 Add a test for repeated Windows cancel calls.** Both inference suites now call `close()` repeatedly and assert it stays safe.
- [ ] **4.3 Review the portal dashboard `api()` helper.** It sets JSON/CSRF headers for non-GET requests; add a browser-level smoke test or at least a JS syntax check to catch template breakage.
- [ ] **4.4 Review AI offload error mapping.** The portal raises `ConnectionError` for `success: false`; confirm the UI surfaces the message without leaking host internals.

## P3 — Later

- [ ] **5.1 Consolidate the standalone `CORE-CLIENT` into `CORE/CORE-CLIENT`.** Keeping two copies invites drift; retire the standalone checkout once the bundle is canonical.
- [ ] **5.2 Add a release checklist step for the `CORE` rename.** Verify install paths, editable installs, and docs before tagging.
- [ ] **5.3 Consider a root-level workspace manifest.** A small file listing the active repos, remotes, and local-only exceptions would make future syncs safer than a skill document alone.
- [ ] **5.4 Re-run the full matrix after any dependency upgrade.** The current results are tied to the installed Python/pytest/ruff versions.

---

## Verification commands used

```powershell
# CORE
cd CORE\CORE-HOST; python -m pytest -q --tb=short
cd ..\CORE-CLIENT; python -m pytest -q --tb=short
python -m ruff check --select E9,F,I core tests

# Standalone client
cd CORE-CLIENT; .venv\Scripts\python -m pytest -q --tb=short
python -m ruff check --select E9,F,I client tests

# Other repos
cd ASCS; .venv\Scripts\python -m pytest -q --tb=short
cd ..\ASIS; .venv\Scripts\python -m pytest -q --tb=short
cd ..\RESCS; .venv\Scripts\python -m pytest -q --tb=short
cd ..\TIVISS; .venv\Scripts\python -m pytest -q --tb=short
```
