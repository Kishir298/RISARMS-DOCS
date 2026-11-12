# Audit / Fix To-Do — 2026-11-12

**Status:** follow-up list after the 2026-11-12 build. Ranked by risk and effort.
**Priority legend:** `P0` blocking/security · `P1` should be next · `P2` hygiene · `P3` later.

## P0 — Security / correctness

- [ ] **0.1 Review the standalone `CORE-CLIENT` vs `CORE/CORE-CLIENT` divergence.** The standalone checkout now has portal hardening, model matching, TLS cleanup, and local frame-deadline work that may not be identical to the bundle copy. Decide which copy is canonical, diff them file by file, and add a sync check or retire the duplicate.
- [ ] **0.2 Add explicit negative tests for the portal security boundary.** Current coverage checks a foreign `Host`, a mismatched `Origin` port, CSRF header presence, remote-bind refusal, strict JSON, and `record_get`; add cases for missing `Origin`, wrong scheme, missing `X-Core-Request`, non-object JSON, oversized bodies, and `Host` with credentials/path/query.
- [ ] **0.3 Validate the Windows cancellation fix on a real long-running stream.** The regression test uses a short-lived local server. Confirm cancel returns promptly while Ollama is generating on Windows and that the detached socket does not leak handles across repeated cancels.
- [ ] **0.4 Decide whether `CORE/config/core.lan.yaml` should be updated locally.** The ignored machine-local file still contains the old `CORE-HOST` TLS paths after the rename. It is not committed, but a stale local config can break LAN startup.

## P1 — Verification gaps

- [ ] **1.1 Physical Raspberry Pi / ARM64 validation.** `CORE` host/client, `ASCS` Pi generation path, and `RESCS` signed-scope/mount validation still need real hardware runs. The `fcntl`-dependent tests are skipped on Windows and must run on Linux.
- [ ] **1.2 Windows ↔ Mac LAN/TLS validation.** Exercise the real TLS listener, certificate trust, firewall rule, reconnect, and portal loopback assumptions on two machines.
- [ ] **1.3 Extended 24/7 operation.** Run endurance, reconnect-storm, disk-full, and log-rotation checks; the current suites are deterministic unit/integration tests, not soak tests.
- [ ] **1.4 Add a CI matrix for Windows and Linux.** The Windows-only fixes and Linux-only Pi skips make platform coverage explicit; CI should run both.
- [ ] **1.5 Add a regression test for `_recv_exact` deadline expiry with a partially received frame.** The local frame-deadline work has one timeout-recovery test; add the deadline-exceeded path and the no-data timeout path.

## P1 — Repository hygiene

- [ ] **2.1 Reduce the broad ruff backlog.** Default `ruff check` reports roughly 482 findings in `CORE/CORE-HOST`, 99 in `CORE/CORE-CLIENT`, 236 in `ASCS`, 167 in `RESCS`, 527 in `ASIS`, 147 in `TIVISS`, and 71 in standalone `CORE-CLIENT`. Either adopt a shared `ruff` config with an explicit rule set and baseline, or fix incrementally by directory. The `--select F` gate is green.
- [ ] **2.2 Review and commit or discard the 22 modified `TIVISS` files.** They were preserved during this build and are unrelated to the CORE rename. Split them into logical commits after review.
- [ ] **2.3 Fix or remove stale generator scripts in `DOCS/`.** `DOCS/write_full.py` still points at `RISARMS-DOCS\requirements.txt` and says "7 repos"; `DOCS/write_req.py` uses the nonstandard `pip --exclude` flag. Decide whether these are maintained tools or disposable one-offs.
- [ ] **2.4 Decide what to do with the stale `RISARMS-DOCS/` folder.** The real docs repository is `DOCS/`; the old folder contains only two markdown files and is not a git repository. Archive or delete it after confirming nothing unique remains.
- [ ] **2.5 Remove duplicate `.gitignore` entries.** Several repos list `*.key`, `.pytest_cache/`, and `__pycache__/` more than once. Cosmetic, but it makes future audits noisier.
- [ ] **2.6 Version workspace-level files.** Root `requirements.txt`, `skills/`, and the build/audit to-dos are outside any git repository. Move them into `DOCS/` or create a small workspace repository if they should be tracked.

## P2 — Documentation / naming

- [ ] **3.1 Add the Windows baseline to the docs.** `DOCS/README.md` and `DOCS/development/testing.md` quote macOS/Linux counts (839 host / 200 client). The current Windows baseline is 836 host + 7 skipped and 199 client + 1 skipped; label historical counts clearly and link this build report.
- [ ] **3.2 Keep `CORE-HOST` naming consistent.** The internal folder, package, GitHub remote, and historical release notes still use `CORE-HOST`; active paths use `CORE/`. Add a short naming note to `DOCS/README.md` so future edits do not reintroduce top-level `CORE-HOST/` paths.
- [ ] **3.3 Refresh `DOCS/development/pi-release-2026-11-06.md` only if it is still active.** It is a historical release record; do not rewrite its test counts. Add a superseded-by link if the release is no longer current.
- [ ] **3.4 Document the portal security model.** The client portal is loopback-only and has no remote authentication; write down the Host/Origin/CSRF assumptions and the threat model so future changes do not weaken them.

## P2 — Code quality

- [ ] **4.1 Deduplicate the inference `ChatStream` implementation.** `CORE/CORE-HOST/core/inference.py` and `CORE/CORE-CLIENT/client/inference.py` carry near-identical cancellation logic; consider a shared helper or a contract test that runs both.
- [ ] **4.2 Add a test for repeated Windows cancel calls.** Ensure `sock.detach()` plus `closesocket` is idempotent and does not double-close a reused handle.
- [ ] **4.3 Review the portal dashboard `api()` helper.** It sets JSON/CSRF headers for non-GET requests; add a browser-level smoke test or at least a JS syntax check to catch template breakage.
- [ ] **4.4 Review AI offload error mapping.** The portal now raises `ConnectionError` for `success: false`; confirm the UI surfaces the message without leaking host internals.

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
python -m ruff check --select F core tests

# Standalone client
cd CORE-CLIENT; .venv\Scripts\python -m pytest -q --tb=short

# Other repos
cd ASCS; .venv\Scripts\python -m pytest -q --tb=short
cd ..\ASIS; .venv\Scripts\python -m pytest -q --tb=short
cd ..\RESCS; .venv\Scripts\python -m pytest -q --tb=short
cd ..\TIVISS; .venv\Scripts\python -m pytest -q --tb=short
```
