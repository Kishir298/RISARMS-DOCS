# A.S.C.S. — A Smart Coding System

> [!NOTE] **File note:** this page lives at `systems/asc.md` (abbreviation `asc`) for historical link stability; it documents **A.S.C.S.**

> [!NOTE] **Status:** **IMPLEMENTED as a standalone tool** (`requires_core: false`, v0.3.0; Python 3.12+; Windows/macOS/Linux x86_64+arm64). Historical evidence: **996 passed / 16 skipped** on macOS Python 3.14, 2026-11-15 (opt-in live tests). A.S.C.S. is a local, private, autonomous coding agent with **multi-provider model support** — ollama (default), openai, anthropic, grok, google, deepseek (LiteLLM/OpenCode opt-in) — that plans, writes, runs and verifies code inside an explicit workspace, with three session modes, a web UI, a terminal TUI, and a Linux/Pi headless generation-only path. **C.O.R.E. integration is DECLARED, NOT IMPLEMENTED** — `compatibility.json` marks it optional (protocol 0.3.0/0.4.0, `ASCS_CORE_CREDENTIAL` / `ASCS_CORE_ENABLED`) and `COMPATIBILITY.md` describes it, but **no runtime C.O.R.E. client code exists in `ASCS/`**; ASCS therefore always runs standalone and falls back offline when C.O.R.E. is absent. C.O.R.E.-mediated use remains **FUTURE**. **ASIS integration is IMPLEMENTED** — ASIS can invoke ASCS via `ascs_integration` with handover; ASCS exposes `export_handover_state()`. Full C.O.R.E.-mediated integration remains **PLANNED/FUTURE**. Source of truth: `ASCS/compatibility.json` + `ASCS/README.md`.

## 1. What A.S.C.S. is

A.S.C.S. is the ecosystem's **autonomous coding agent**: a local, privacy-first developer tool. It drives a locally-running Ollama model by default (default `qwen3-coder:30b`, fallback `qwen2.5-coder:14b`) and supports optional cloud providers (OpenAI, Anthropic, Grok, Google, DeepSeek via config — LiteLLM/OpenCode opt-in; these do leave the machine). Ollama-local mode sends no code off-machine; otherwise the only runtime dependency is Python 3.12+ and the standard library.

Its declared long-term role in R.I.S.A.R.M.S. is as a coding capability that A.S.I.S. and T.I.V.I.S.S. can eventually use. Today it runs entirely standalone.

## 2. Project facts

- Location: `RISARMS/ASCS/` (sibling of `CORE/`, `RESCS/`, `ASIS/`, `TIVISS/`, `RISARMS-DOCS/`); mirrored at `CORE/services/ASCS/` for the combined release
- Own git repository (origin `https://github.com/Kishir298/ASCS.git`, branch `main`)
- Package: `agent` (distribution name `coding-agent`), version `0.3.0`; console scripts `ascs`, `risa`
- Entry point: `risa` (e.g. `risa --auto "…"`, `risa --tasks "…"`, `risa --ui`, `risa --tui`, `risa --doctor`, `risa --pi`)
- Runtime: **Python 3.12+** (`requires-python >=3.12`); supported OS per `ASCS/compatibility.json`: **Windows, macOS and Linux on x86_64 and arm64** (Windows 10 22H2+, macOS 12.0+, Linux glibc 2.28+). Desktop web UI/TUI is Windows-primary (32 GB target); the Pi path is **Linux ARM64 headless generation-only** (no tools/TUI); **dev testing is cross-platform**
- Standalone: **`requires_core: false`** — C.O.R.E. integration is optional (protocol 0.3.0/0.4.0, `ASCS_CORE_CREDENTIAL`, `ASCS_CORE_ENABLED`, offline fallback)
- Model providers: **ollama, openai, anthropic, grok, google, deepseek** (LiteLLM/OpenCode opt-in)
- Tests: **996 passed / 16 skipped** on macOS Python 3.14 (recorded 2026-11-15, **re-verified 2026-11-20** on macOS Python 3.14.7; live Ollama tests opt-in via `RISALIVE=1`, skipped by default). An earlier 991 passed / 6 skipped on 2026-11-09 is preserved in ADR 0007 — two dated measurements, not a conflict. Exact counts vary with platform/plugins.

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
| Multi-provider model support (ollama, openai, anthropic, grok, google, deepseek; LiteLLM/OpenCode opt-in) | IMPLEMENTED (per `compatibility.json`) |
| Optional C.O.R.E. integration — declared in `compatibility.json` (protocol 0.3.0/0.4.0, `ASCS_CORE_CREDENTIAL`, `ASCS_CORE_ENABLED`, offline fallback; ASCS keeps running when CORE is unavailable) | **Declared / optional** (manifest only; CORE is never required — see `ASCS/COMPATIBILITY.md`) |
| Project context (workspace, toolchain, context index; dual chunk limits 30B/14B) | IMPLEMENTED |
| Experience store (phase 5 learning groundwork) | IMPLEMENTED (early) |
| Verification engine (tool success vs objective success) | IMPLEMENTED |

### Pi headless path (v0.3.0 update)

`risa --pi` adds an experimental Linux ARM64 generation-only path with admission
policy (`agent/pi.py`): cgroup v2 memory checks, model digest/quantization
approval, a single inference slot, no tools and no TUI. It is intended for the
Pi deployment, not for desktop use. macOS/Linux unit tests mock the platform
guard; real cgroup/systemd/ARM64 behavior is unvalidated.

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
- [A.S.I.S. Integration (asis.md §6)](../systems/asis.md#6-asis--ascs-integration-implemented)
