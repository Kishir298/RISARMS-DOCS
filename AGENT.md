# R.I.S.A.R.M.S. — AGENT.md (Canonical)

> Canonical agent operating guide. Root `AGENT.md` points here.

## 1. Role + Scope

**Role:** You are a BUILD MODE coding agent operating in `C:\Users\rishi\Desktop\RISARMS`.
You edit files, run tests, and report files changed/deleted + test results. Do NOT commit unless explicitly requested.

**In-scope (7 top-level entries):**

- `ASIS/` — A Smart Intelligence System (primary AI layer)
- `ASCS/` — A Smart Coding System (standalone coding agent)
- `CORE-HOST/` — C.O.R.E. server/runtime (`core` package)
- `CORE-CLIENT/` — C.O.R.E. external-device client (`client` package)
- `RESCS/` — Cloud storage system
- `TIVISS/` — Separate AI agent (foundation-only, no live handover)
- `DOCS/` — Architecture source of truth (this repo docs)

**Explicitly excluded:**

- `IMH/` — Personal / food-companion and chat-log data (`AI/`, `WhatsApp_Chat_Logs_*.zip`). Never read, edit, index, or infer ecosystem membership from it.
- `Flavora/` sibling if present on disk — not an ecosystem member.
- Git history (`.git/`) — never delete, rewrite, or force-push.

**Independence rule:** RESCS, ASIS, ASCS, TIVISS live *beside* CORE, not inside it. Integration only via defined interfaces. No code sharing across systems.

## 2. Method — 7 Parallel Sub-Agents

For any ecosystem-wide audit/fix, fan out 7 parallel workers, one per in-scope root:

1. `ASIS` agent
2. `ASCS` agent
3. `CORE-HOST` agent
4. `CORE-CLIENT` agent
5. `RESCS` agent
6. `TIVISS` agent
7. `DOCS` agent

Rules:

- One directory per agent, no cross-writes.
- Each agent: inspect → edit → run scoped tests → report.
- Coordinator merges reports, runs cross-system checks, returns unified changed/deleted + test results.
- `IMH` never gets an agent.
- Prefer specialized file tools (`read`/`edit`/`write`) over shell for file ops; use `bash` only for `pytest`, `ruff`, `git status/diff`, `Test-Path`/`Remove-Item`.

## 3. Taxonomy

- **Status vocabulary:** `IMPLEMENTED` / `IN DEVELOPMENT` / `PLANNED` / `FUTURE` (see `DOCS/architecture/overview.md`). Never describe unbuilt as built.
- **Top-level layout:** see `DOCS/README.md §7 Repository structure`.
- **Per-system ownership:** see `DOCS/systems/` and `DOCS/architecture/system-boundaries.md`.
- **Interactions:** all cross-system traffic flows through C.O.R.E. (see `DOCS/architecture/system-interactions.md`).
- **Stale-tree rule:** `__pycache__`-only legacy trees with 0× `.py` (e.g. ex-`ASIS/core/`, ex-`ASIS/02_voice/`) may be deleted with `Remove-Item -Recurse` after verifying `(Get-ChildItem -Filter *.py).Count -eq 0`.
- **Orphan-venv rule:** `Lib/site-packages`-only fragments may be deleted; project scripts (e.g. `CORE-HOST/Scripts/windows/`) must be kept. Verify with `Test-Path` first.
- **Audit-report rule:** root `.pytest_cache/`, root `AUDIT_REPORT.md`, `DOCS/AUDIT_*.md` are disposable artifacts when user says "remove audit_report from everywhere". Never delete `.git/`.

## 4. Master Prompt

```text
You are in BUILD MODE. Work in C:\Users\rishi\Desktop\RISARMS.
Scope: ASIS, ASCS, CORE-HOST, CORE-CLIENT, RESCS, TIVISS, DOCS. Exclude IMH.
Method: 7 parallel sub-agents (one per in-scope root).
For each task: read target files first, make minimal edits, run scoped pytest/ruff, verify no .py deleted before any Remove-Item -Recurse, never touch .git history.
Do NOT commit. Return files changed/deleted + test results.
Canonical guide: DOCS/AGENT.md.
```

## 5. Build Handoff

Each BUILD turn must return:

1. **Files changed:** absolute paths + one-line why.
2. **Files/deleted dirs:** absolute paths + pre-delete verification (`*.py count`, `Test-Path`).
3. **Test results:** exact commands run and pass/fail counts, e.g.:
   - `.venv\Scripts\python -m pytest tests/test_coding_tools.py -q` → `11 passed`
   - `.venv\Scripts\python -m pytest tests/test_memory.py tests/test_coding_tools.py tests/test_cli.py -q` → `31 passed`
   - `.venv\Scripts\python -m ruff check asis tests --fix` → `59 fixed, 17 remaining (E501/SIM117)`
4. **Remaining:** E501 line-length and SIM117 `with`-nest items are known non-blocking; F401 must be 0.
5. **No commit** performed.

Reference: `DOCS/README.md`, `DOCS/architecture/`, `DOCS/systems/`, `DOCS/interfaces/`, `DOCS/security/`, `DOCS/development/`.
