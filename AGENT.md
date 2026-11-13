# R.I.S.A.R.M.S. — AGENT.md (Canonical)

> Canonical agent operating guide. Root `AGENT.md` points here.

## 1. Role + Scope

**Role:** You are a BUILD MODE coding agent operating in `C:\Users\rishi\Desktop\RISARMS` (Windows). You edit files, run tests, and report files changed/deleted + test results. Do NOT commit unless explicitly requested.

**In-scope (6 active top-level entries):**

- `ASIS/` — A Smart Intelligence System (primary AI layer, v0.1.0 with Pi policy/worker update)
- `ASCS/` — A Smart Coding System (standalone coding agent, v0.3.0 with Pi headless path; ASIS direct integration IMPLEMENTED, CORE-mediated future)
- `CORE/` — combined C.O.R.E. project, v0.5.0: `CORE-HOST/` (`core` package), `CORE-CLIENT/` (`client` package), `services/`, `deployment/`, `install/`, `validation/`
- `RESCS/` — Cloud storage system, v0.4.0 with Pi signed-scope/mount validation
- `TIVISS/` — Separate AI agent (v0.2.0: OllamaProvider, SQLiteMemoryStore, Web/Calc/Translation/Voice config, offline-tested transports)
- `DOCS/` — Architecture source of truth (this repo docs; remote `RISARMS-DOCS`)

**Explicitly excluded:**

- `Flavora/` sibling if present on disk — not an ecosystem member.
- `.incoming/`, `.backups/`, `old-versions/` — release staging/rollback/archive, not active code.
- Git history (`.git/`) — never delete, rewrite, or force-push.

**Independence rule:** The owning RESCS, ASIS, ASCS, and TIVISS repositories live *beside* CORE. `CORE/services/*` holds release mirrors for the combined deployment; edits belong in the owning repo and are synced in. Integration is only via defined interfaces; no shared source of truth.

## 2. Method — 6 Parallel Sub-Agents

For any ecosystem-wide audit/fix, fan out 6 parallel workers, one per in-scope root:

1. `ASIS` agent
2. `ASCS` agent
3. `CORE` agent (covers `CORE-HOST/` and `CORE-CLIENT/`)
4. `RESCS` agent
5. `TIVISS` agent
6. `DOCS` agent

Rules:

- One directory per agent, no cross-writes.
- Each agent: inspect → edit → run scoped tests → report.
- Coordinator merges reports, runs cross-system checks, returns unified changed/deleted + test results.
- Prefer specialized file tools (`read`/`edit`/`write`) over shell for file ops; use `bash` only for `pytest`, `ruff`, `git status/diff`, and file existence/removal checks.

## 3. Taxonomy

- **Status vocabulary:** `IMPLEMENTED` / `IN DEVELOPMENT` / `PLANNED` / `FUTURE` (see `DOCS/architecture/overview.md`). Never describe unbuilt as built.
- **Top-level layout:** see `DOCS/README.md §7 Repository structure`.
- **Per-system ownership:** see `DOCS/systems/` and `DOCS/architecture/system-boundaries.md`.
- **Interactions:** all cross-system traffic flows through C.O.R.E. (see `DOCS/architecture/system-interactions.md`).
- **Stale-tree rule:** `__pycache__`-only legacy trees with 0× `.py` (e.g. ex-`ASIS/core/`, ex-`ASIS/02_voice/`) may be deleted with `Remove-Item -Recurse` after verifying `(Get-ChildItem -Filter *.py).Count -eq 0`.
- **Orphan-venv rule:** `Lib/site-packages`-only fragments may be deleted; project scripts (e.g. `CORE/CORE-HOST/Scripts/windows/`) must be kept. Verify the path first.
- **Audit-report rule:** root `.pytest_cache/`, root `AUDIT_REPORT.md`, `DOCS/AUDIT_*.md` are disposable artifacts when user says "remove audit_report from everywhere". Never delete `.git/`.

## 4. Master Prompt

```text
You are in BUILD MODE. Work in C:\Users\rishi\Desktop\RISARMS.
Scope: ASIS, ASCS, CORE, RESCS, TIVISS, DOCS.
Method: 6 parallel sub-agents (one per in-scope root).
For each task: read target files first, make minimal edits, run scoped pytest/ruff, verify no .py deleted before any recursive remove, never touch .git history.
Do NOT commit. Return files changed/deleted + test results.
Canonical guide: DOCS/AGENT.md.
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

Reference: `DOCS/README.md`, `DOCS/architecture/`, `DOCS/systems/`, `DOCS/interfaces/`, `DOCS/security/`, `DOCS/development/`.

## 6. Canonical Reference Documents

- `DOCS/R.I.S.A.R.M.S brief.txt` — High-level system overview (R.I.S.A.R.M.S, C.O.R.E, R.E.S.C.S, A.S.I.S, T.I.V.I.S.S, RadarS.A.R.D)
- `DOCS/README.md` — Repository structure and navigation
- `DOCS/architecture/overview.md` — System status vocabulary and architecture
- `DOCS/systems/` — Per-system ownership and interfaces
- `DOCS/architecture/system-interactions.md` — Cross-system communication flows
- `DOCS/architecture/system-boundaries.md` — Independence rules and boundaries

## 7. Repository Sync Protocol

Before any BUILD MODE work, sync all 6 ecosystem repos:

```bash
git -C ASCS pull
git -C ASIS pull
git -C CORE pull
git -C DOCS pull
git -C RESCS pull
git -C TIVISS pull
```

Or single command:
```bash
git -C ASCS pull; git -C ASIS pull; git -C CORE pull; git -C DOCS pull; git -C RESCS pull; git -C TIVISS pull
```

Verify all report "Already up to date" or fast-forward. Note any conflicts.

**Enhanced verification (recommended):**
```bash
for dir in ASCS ASIS CORE RESCS DOCS TIVISS; do
  echo "=== $dir ==="
  git -C "$dir" status --short
done
```

If new repositories are added to the ecosystem after pull, they will appear as new directories. Add them to the sync list and update this protocol accordingly.
