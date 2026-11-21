# R.I.S.A.R.M.S. — AGENT.md (Canonical)

> Canonical agent operating guide. Root `AGENT.md` points here.

## 1. Role + Scope

**Role:** You are a BUILD MODE coding agent operating in the RISARMS workspace root (the directory containing `ASIS/`, `ASCS/`, `CORE-HOST/`, `CORE-CLIENT/`, `RESCS/`, `TIVISS-HOST/`, `TIVISS-CLIENT/`, `RISARMS-HOST/`, `RISARMS-DOCS/`, and `RISARMS-ui/`). You edit files, run tests, and report files changed/deleted + test results. Do NOT commit unless explicitly requested.

**In-scope (10 active top-level entries):**

- `ASIS/` — A Smart Intelligence System (primary AI layer, v0.1.0 with Pi policy/worker update)
- `ASCS/` — A Smart Coding System (standalone coding agent, v0.3.0 with Pi headless path; ASIS direct integration IMPLEMENTED, CORE-mediated future)
- `CORE-HOST/` — C.O.R.E. host/server runtime (`core` package, v0.6.0, Void x86_64 server target; remote `Kishir298/CORE-HOST`)
- `CORE-CLIENT/` — C.O.R.E. external-device client (`client` package, v0.6.0, stdlib-only; remote `Kishir298/CORE-CLIENT`)
- `RESCS/` — Cloud storage system, v0.4.0 with Pi signed-scope/mount validation
- `TIVISS-HOST/` — T.I.V.I.S.S. host runtime (v0.2.0: OllamaProvider, SQLiteMemoryStore, Web/Calc/Translation/Voice config, offline-tested transports; remote `Kishir298/TIVISS-HOST`)
- `TIVISS-CLIENT/` — T.I.V.I.S.S. client library scaffold (v0.1.0, stdlib-only CLI shell; transport/protocol/security layers PLANNED; remote `Kishir298/TIVISS-CLIENT`)
- `RISARMS-HOST/` — Umbrella repository: Void/Pi deployment, vendored `services/*`, release manifests, validation evidence and the `risarms-host` operator CLI (v0.6.0; remote `Kishir298/RISARMS-HOST`)
- `RISARMS-ui/` — Canonical cross-platform desktop client (Tkinter): presents CORE/ASIS/ASCS/RESCS/TIVISS and consumes CORE-HOST over HTTPS/WSS. Presentation only, not an integration layer.
- `RISARMS-DOCS/` — Architecture source of truth (this repository; remote `Kishir298/RISARMS-DOCS`)

For every in-scope entry the local directory name equals the GitHub repository name (`https://github.com/Kishir298/<name>`). The workspace used to be a `CORE/` + `TIVISS/` monorepo; historical documents may still say `CORE/`, `CORE/CORE-HOST`, `CORE/CORE-CLIENT` or `TIVISS/` — those paths no longer exist on disk.

**Explicitly excluded:**

- `Flavora/` sibling if present on disk — not an ecosystem member.
- `integration-tests/` — local-only git repository with no remote; never pulled.
- `.incoming/`, `.backups/`, `old-versions/` — release staging/rollback/archive, not active code.
- Git history (`.git/`) — never delete, rewrite, or force-push.

**Independence rule:** The owning RESCS, ASIS, ASCS, TIVISS-HOST and TIVISS-CLIENT repositories live as separate repositories beside CORE-HOST and CORE-CLIENT. `RISARMS-HOST/services/*` holds release mirrors for the combined deployment; edits belong in the owning repo and are synced in. Integration is only via defined interfaces; no shared source of truth.

## 2. Method — 10 Parallel Sub-Agents

For any ecosystem-wide audit/fix, fan out 10 parallel workers, one per in-scope root:

1. `ASIS` agent
2. `ASCS` agent
3. `CORE-HOST` agent
4. `CORE-CLIENT` agent
5. `RESCS` agent
6. `TIVISS-HOST` agent
7. `TIVISS-CLIENT` agent
8. `RISARMS-HOST` agent
9. `RISARMS-ui` agent
10. `RISARMS-DOCS` agent

Rules:

- One directory per agent, no cross-writes.
- Each agent: inspect → edit → run scoped tests → report.
- Coordinator merges reports, runs cross-system checks, returns unified changed/deleted + test results.
- Prefer specialized file tools (`read`/`edit`/`write`) over shell for file ops; use `bash` only for `pytest`, `ruff`, `git status/diff`, and file existence/removal checks.

## 3. Taxonomy

- **Status vocabulary:** `IMPLEMENTED` / `IN DEVELOPMENT` / `PLANNED` / `FUTURE` (see `RISARMS-DOCS/architecture/overview.md`). Never describe unbuilt as built.
- **Top-level layout:** see `RISARMS-DOCS/README.md §7 Repository structure`.
- **Per-system ownership:** see `RISARMS-DOCS/systems/` and `RISARMS-DOCS/architecture/system-boundaries.md`.
- **Interactions:** all cross-system traffic flows through C.O.R.E. (see `RISARMS-DOCS/architecture/system-interactions.md`).
- **Stale-tree rule:** `__pycache__`-only legacy trees with 0× `.py` (e.g. ex-`ASIS/core/`, ex-`ASIS/02_voice/`) may be deleted with `Remove-Item -Recurse` after verifying `(Get-ChildItem -Filter *.py).Count -eq 0`.
- **Orphan-venv rule:** `Lib/site-packages`-only fragments may be deleted; project scripts (e.g. `CORE-HOST/scripts/windows/`) must be kept. Verify the path first.
- **Audit-report rule:** root `.pytest_cache/`, root `AUDIT_REPORT.md`, `RISARMS-DOCS/AUDIT_*.md` are disposable artifacts when user says "remove audit_report from everywhere". Never delete `.git/`.

## 4. Master Prompt

```text
You are in BUILD MODE. Work in the RISARMS workspace root.
Scope: ASIS, ASCS, CORE-HOST, CORE-CLIENT, RESCS, TIVISS-HOST, TIVISS-CLIENT, RISARMS-HOST, RISARMS-ui, RISARMS-DOCS.
Method: 10 parallel sub-agents (one per in-scope root).
For each task: read target files first, make minimal edits, run scoped pytest/ruff, verify no .py deleted before any recursive remove, never touch .git history.
Do NOT commit. Return files changed/deleted + test results.
Canonical guide: RISARMS-DOCS/AGENT.md.
```

## 5. Build Handoff

Each BUILD turn must return:

1. **Files changed:** absolute paths + one-line why.
2. **Files/deleted dirs:** absolute paths + pre-delete verification (`*.py count`, `Test-Path`).
3. **Test results:** exact commands run and pass/fail counts, e.g.:
   - `.venv/bin/python -m pytest tests/test_coding_tools.py -q` → `11 passed`
   - `.venv/bin/python -m pytest tests/test_memory.py tests/test_coding_tools.py tests/test_cli.py -q` → `31 passed`
   - `ruff check --select F asis tests` → `All checks passed`
4. **Remaining:** E501 line-length and SIM117 `with`-nest items are known non-blocking; F401 must be 0.
5. **No commit** performed.

Reference: `RISARMS-DOCS/README.md`, `RISARMS-DOCS/architecture/`, `RISARMS-DOCS/systems/`, `RISARMS-DOCS/interfaces/`, `RISARMS-DOCS/security/`, `RISARMS-DOCS/development/`.

## 6. Canonical Reference Documents

- `RISARMS-DOCS/R.I.S.A.R.M.S brief.txt` — High-level system overview (R.I.S.A.R.M.S, C.O.R.E, R.E.S.C.S, A.S.I.S, T.I.V.I.S.S, RadarS.A.R.D)
- `RISARMS-DOCS/README.md` — Repository structure and navigation
- `RISARMS-DOCS/architecture/overview.md` — System status vocabulary and architecture
- `RISARMS-DOCS/systems/` — Per-system ownership and interfaces
- `RISARMS-DOCS/architecture/system-interactions.md` — Cross-system communication flows
- `RISARMS-DOCS/architecture/system-boundaries.md` — Independence rules and boundaries

## 7. Repository Sync Protocol

Before any BUILD MODE work, sync all ten in-scope repositories:

```bash
git -C ASCS pull
git -C ASIS pull
git -C CORE-HOST pull
git -C CORE-CLIENT pull
git -C RISARMS-DOCS pull
git -C RESCS pull
git -C TIVISS-HOST pull
git -C TIVISS-CLIENT pull
git -C RISARMS-HOST pull
git -C RISARMS-ui pull
```

> **Local names:** every in-scope directory name equals its GitHub repository
> name. The documentation repo is checked out as `RISARMS-DOCS/` (remote
> `Kishir298/RISARMS-DOCS`); older notes may call it `DOCS/`.
> `integration-tests/` is a local-only git repository with no remote, so it
> cannot be pulled. `Flavora/` is explicitly out of scope.

Or single command:
```bash
for dir in ASCS ASIS CORE-HOST CORE-CLIENT RISARMS-DOCS RESCS TIVISS-HOST TIVISS-CLIENT RISARMS-HOST RISARMS-ui; do git -C "$dir" pull; done
```

Verify all report "Already up to date" or fast-forward. Note any conflicts.

**Enhanced verification (recommended):**
```bash
for dir in ASCS ASIS CORE-HOST CORE-CLIENT RISARMS-DOCS RESCS TIVISS-HOST TIVISS-CLIENT RISARMS-HOST RISARMS-ui; do
  echo "=== $dir ==="
  git -C "$dir" status --short
done
```

If new repositories are added to the ecosystem after pull, they will appear as new directories. Add them to the sync list and update this protocol accordingly.
