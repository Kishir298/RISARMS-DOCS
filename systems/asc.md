# A.S.C.S. — A Smart Coding System

> [!NOTE] **File note:** this page lives at `systems/asc.md` (abbreviation `asc`) for historical link stability; it documents **A.S.C.S.**

> [!NOTE] **Status:** **IMPLEMENTED as a standalone tool** (v0.3.0, 949 passed / 6 skipped 2026-09-18 + opt-in live tests). A.S.C.S. is a local, private, autonomous coding agent built on Ollama: it plans, writes, runs and verifies code inside an explicit workspace, with three session modes, a web UI and a terminal TUI. **ASIS integration is IMPLEMENTED** — ASIS can invoke ASCS via `ascs_integration` tool with handover protocol; ASCS exposes `export_handover_state()` for session continuity. Full C.O.R.E.-mediated integration remains **PLANNED/FUTURE**.

## 1. What A.S.C.S. is

A.S.C.S. is the ecosystem's **autonomous coding agent**: a local, privacy-first developer tool driven by a locally-running Ollama model (default `qwen3-coder:30b`, fallback `qwen2.5-coder:14b`). No code leaves the machine; the only runtime dependency is the standard library plus Ollama.

Its declared long-term role in R.I.S.A.R.M.S. is as a coding capability that A.S.I.S. and T.I.V.I.S.S. can eventually use. Today it runs entirely standalone.

## 2. Project facts

- Location: `RISARMS/ASCS/` (sibling of `CORE-HOST/` + `CORE-CLIENT/`, `RESCS/`, `ASIS/`, `TIVISS/`, `DOCS/`)
- Own git repository (origin `https://github.com/Kishir298/ASCS.git`, branch `main`, 82 commits)
- Package: `agent` (distribution name `coding-agent`), version `0.3.0`
- Entry point: `risa` (e.g. `risa --auto "…"`, `risa --tasks "…"`, `risa --ui`, `risa --tui`, `risa --doctor`)
- Runtime: **Windows-only** (web UI/TUI + Ollama; 32 GB target); **dev testing is cross-platform** (pytest passes on macOS/Linux)
- Tests: 949 passed / 6 skipped 2026-09-18 (live Ollama tests opt-in via `RISALIVE=1`, skipped by default; verify with `pytest -q`)

## 3. What is implemented

| Area | Status |
|---|---|
| Agent lifecycle `RECEIVING_TASK → PLANNING → EXECUTING → VERIFYING → COMPLETE/FAILED/CANCELLED/TIMEOUT` | IMPLEMENTED |
| Structured planning (`set_plan`; plan-before-edit in BUILD mode) | IMPLEMENTED |
| Task-graph engine (objective → DAG of tasks, persisted/resumable in `.ascs`) | IMPLEMENTED |
| Intent-aware request classification (conversation / question / inspection / code change / file op / command / verification / ambiguous) with mode gating | IMPLEMENTED |
| Real interactive shell: streaming, scroll, cancel, double-ESC interrupt, Ctrl+C confirm | IMPLEMENTED |
| Web UI (`http://127.0.0.1:8787`) and terminal TUI (responsive tiers, themes, cursor-aware input) | IMPLEMENTED |
| Windows-aware tool execution (python/pip/pytest resolution; transparent `python`→`python3` fallback for dev testing) | IMPLEMENTED |
| Ollama integration (streaming + resilient chat, model fallback auto-switch, stop-on-exit) | IMPLEMENTED |
| Project context (workspace, toolchain, context index; dual chunk limits 30B/14B) | IMPLEMENTED |
| Experience store (phase 5 learning groundwork) | IMPLEMENTED (early) |
| Verification engine (tool success vs objective success) | IMPLEMENTED |

## 5. Integration with ASIS (IMPLEMENTED)

A.S.C.S. exposes `export_handover_state()` on `AgentLoop` which serializes the current session state for ASIS takeover. The ASIS `ascs_integration` toolset (`ascs_integration`, `ascs_handover`, `ascs_status`) invokes ASCS via subprocess (`risa` CLI) or Python API, with optional handover state extraction for session continuity.

**Handover State Includes:**
- `task` — original task/objective
- `plan` — current plan (if any)
- `completed_actions` — list of completed actions with results
- `observations` — key observations from execution
- `partial_results` — any partial results from tools
- `context_index_ref` — path to `.ascs/context_index.json`
- `experience_tags` — relevant experience tags for continuation
- `workspace` — workspace path
- `timestamp` — ISO format timestamp

ASIS invokes ASCS via `ascs_integration` tool with two invocation modes:
- `subprocess` (default): runs `risa` CLI command — clean isolation
- `api`: uses Python API directly — better event streaming

## 6. Boundaries and ownership

- A.S.C.S. owns **autonomous coding execution**. No other R.I.S.A.R.M.S. system owns this today.
- It does not import C.O.R.E., R.E.S.C.S. or A.S.I.S. code, and none of them import it.
- When integration happens, it should follow the ecosystem pattern: A.S.I.S./T.I.V.I.S.S. reach coding capability **through C.O.R.E.** rather than invoking A.S.C.S. directly. That contract does not exist yet and must be defined before wiring ([Integration Contracts](../interfaces/integration-contracts.md)).

## 7. Roadmap direction

A.S.C.S. tracks its own phase roadmap (`ASCS/docs/phases/`, phases 00–06: architecture, brain audit, modes, powershell, language intelligence, experience/learning, verification). Phases 0–1 are documented as closed in its own docs; later phases are in progress.

**ASIS integration is IMPLEMENTED** — the `ascs_integration` toolset in ASIS and `export_handover_state()` in ASCS provide a working handover protocol. Full C.O.R.E.-mediated integration (usable by A.S.I.S./T.I.V.I.S.S. through C.O.R.E.) remains **PLANNED/FUTURE** and unstarted. The integration contract must be defined before wiring ([Integration Contracts](../interfaces/integration-contracts.md)).

## Related

- [System Boundaries](../architecture/system-boundaries.md)
- [System Interactions](../architecture/system-interactions.md)
- [Development Roadmap](../development/roadmap.md)
- [A.S.I.S. Integration (asis.md#6)](../systems/asis.md#6)
