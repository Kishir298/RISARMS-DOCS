# Audit / Fix To-Do — Phase 2 — 2026-11-12

**Status:** remaining limitations after the Phase 2 follow-up build. Ranked by risk and effort.
**Priority legend:** `P0` blocking/security · `P1` should be next · `P2` hygiene · `P3` later.
**Context:** [build report](build-report-2026-11-12.md) · [initial audit list](audit-todo-2026-11-12.md).

## P0 — Correctness / security validation

- [ ] **0.1 Validate cancellation against a real long-running Ollama stream on Windows.** The automated test uses a short-lived local server and repeated `close()` calls. Run a real generation, cancel mid-stream, repeat at least 50 times, and watch for leaked handles or a blocked reader.
- [ ] **0.2 Re-check the portal CSRF decision in a real browser.** Missing `Origin` is allowed only with `X-Core-Request`; confirm a cross-origin page cannot set that header without a preflight and that same-origin dashboard calls still work after a restart.
- [ ] **0.3 Confirm the exact-tag `find_model` behavior against installed Ollama tags.** The tests cover exact, `:latest`, and quantized tags; verify the host reports tags in the same form the client requests (for example `llama3:8b` vs `llama3:8b-instruct-q4_0`).
- [ ] **0.4 Review the legacy standalone client for any remaining behavior drift.** It is aligned for model matching, portal tests, and lint, but the desktop/inference code is not a byte-for-byte copy of `CORE/CORE-CLIENT`. Diff the two trees before the next release.

## P1 — Verification gaps (environment-blocked)

- [ ] **1.1 Physical Raspberry Pi / ARM64 validation.** Run `CORE` host/client, `ASCS` Pi generation, and `RESCS` signed-scope/mount validation on real hardware. The `fcntl` tests skip on Windows and must run on Linux.
- [ ] **1.2 Windows ↔ Mac LAN/TLS validation.** Exercise the real TLS listener, certificate trust, firewall rule, reconnect, and portal loopback assumptions on two machines.
- [ ] **1.3 Extended 24/7 operation.** Run endurance, reconnect-storm, disk-full, and log-rotation checks. Current suites are deterministic unit/integration tests, not soak tests.
- [ ] **1.4 Add full Windows test jobs to `ASIS`, `RESCS`, and `TIVISS`.** `CORE` and `ASCS` now run Windows suites in CI; the other three only gate lint. Add Windows jobs (and keep Ubuntu for platform-specific tests).
- [ ] **1.5 Add `_recv_exact` deadline tests.** Cover a partially received frame that exceeds the deadline and a no-data timeout, not only the recovery path.

## P1 — Repository hygiene

- [ ] **2.1 Retire or sync-check the standalone `CORE-CLIENT`.** `CORE/CORE-CLIENT` is canonical; keeping a second checkout invites drift. Either add a CI comparison of the shared files or remove the standalone copy after archiving its history.
- [ ] **2.2 Version workspace-level files.** Root `requirements.txt`, `requirements-dev.txt`, `skills/`, and the build/audit to-dos are outside git. Move them into `DOCS/` or create a small workspace repository.
- [ ] **2.3 Remove duplicate `.gitignore` entries.** Several repos repeat `*.key`, `.pytest_cache/`, and `__pycache__/`; deduplicate so audits stay readable.
- [ ] **2.4 Define a dependency-update cadence.** The 47-package root inventory is a snapshot; add a scheduled review and re-run the full matrix after upgrades.

## P2 — Code quality

- [ ] **3.1 Reduce the broad ruff backlog.** `E9,F,I` is green everywhere, but default `ruff check` reports 504 findings in `ASIS` and 147 in `TIVISS`. Adopt a shared explicit rule set with a baseline, then fix by directory.
- [ ] **3.2 Deduplicate `ChatStream`.** `CORE/CORE-HOST/core/inference.py` and `CORE/CORE-CLIENT/client/inference.py` carry near-identical cancellation logic; extract a shared helper or add a contract test that runs both.
- [ ] **3.3 Add a portal dashboard smoke test.** The `api()` helper sets JSON/CSRF headers for non-GET requests; add a browser-level smoke test or a JS syntax check to catch template breakage.
- [ ] **3.4 Review AI offload error mapping.** The portal raises `ConnectionError` for `success: false`; confirm the UI shows the message without leaking host internals.

## P2 — Documentation

- [ ] **4.1 Update the documented test baseline.** `DOCS/README.md` and `DOCS/development/testing.md` still quote macOS/Linux counts; label them historical and add the Windows Phase 2 counts (837/7 host, 235/1 bundle client, 185 standalone, 982/22 ASCS, 948/19 ASIS, 314/4 RESCS, 279 TIVISS).
- [ ] **4.2 Add a `CORE` vs `CORE-HOST` naming note.** Explain that `CORE/` is the top-level project and `CORE-HOST/` is the internal host subdirectory/package, so future edits do not reintroduce top-level `CORE-HOST/` paths.
- [ ] **4.3 Write a standalone portal threat-model document.** Record the loopback-only bind, Host/Origin validation, `X-Core-Request` CSRF control, body limits, and the intentional missing-`Origin` exception.
- [ ] **4.4 Mark the 2026-11-06 Pi release record as historical.** Add a superseded-by link if it is no longer current; do not rewrite its counts.

## P3 — Later

- [ ] **5.1 Add a release checklist step for the `CORE` rename.** Verify install paths, editable installs, and docs before tagging.
- [ ] **5.2 Add a root-level workspace manifest.** List active repos, remotes, canonical/legacy status, and local-only exceptions to make future syncs safer than a skill document alone.
- [ ] **5.3 Decide how long to keep `DOCS/development/archive/`.** Archived `RISARMS-DOCS` content is preserved; add a retention note or a pointer from the docs index.

---

## Not performed (explicit)

- Physical Raspberry Pi / ARM64 runs.
- Two-machine Windows ↔ Mac LAN/TLS validation.
- 24/7 endurance, reconnect-storm, disk-full, and log-rotation soak tests.
