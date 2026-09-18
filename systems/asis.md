# A.S.I.S. — A Smart Intelligence System

> [!NOTE] **Status:** **IN DEVELOPMENT** — rebuilt `asis` package ships CLI (stateful multi-turn), Ollama provider, inference/conversation/context engines, local SQLite memory (query-scoped recall), tool system (calculator 30 ops, 136-lang translation, web search/fetch, coding tools, 7 CORE tools; native function-calling primary, up to ASIS_TOOL_MAX_CALLS_PER_TURN per turn), permissions (confirmation-gated), events, and voice pipeline sharing app chat loop. Suite: 42 files / 693 passed (2026-09-18, verify with pytest -q). Legacy Forza trees removed. C.O.R.E. uplink is a real optional adapter (via CORE-CLIENT, standalone by default; physical LAN validation NOT PERFORMED). R.E.S.C.S. remains future/placeholder. A.S.I.S. is an **independent project**.

## 1. What A.S.I.S. is

A.S.I.S. is the **primary AI / intelligence layer** of R.I.S.A.R.M.S. It was previously developed under the internal name **Forza-AI**; the git history records an explicit reset (`chore: reset ASIS scaffolding for A.S.I.S. rebuild`) followed by a staged rebuild of the `asis` package.

### Responsibilities

- Natural-language understanding
- Reasoning
- Response generation
- AI model interaction
- Voice functionality
- System interaction (through C.O.R.E., once integrated)
- Using C.O.R.E.
- Using R.E.S.C.S. (through C.O.R.E.)
- Potentially controlling external devices (through C.O.R.E.)

### Non-responsibilities

A.S.I.S. **does not directly own** C.O.R.E.'s responsibilities: message routing, resource registry, runtime orchestration, configuration, health, logging, security infrastructure. It *uses* them.

## 2. Independence

> [!IMPORTANT] A.S.I.S. is an independent project. It must **never** be placed inside CORE. It uses C.O.R.E. through interfaces. Rationale: ADR [0002](../decisions/0002-asis-independent-from-core.md).

- Location: `RISARMS/ASIS/` (sibling of `CORE-HOST/`, `CORE-CLIENT/`, `RESCS/`, `ASCS/`, `RISARMS-DOCS/`)
- Own git repository (origin `https://github.com/Kishir298/ASIS.git`, branch `main`; `legacy-before-rebuild` branch preserves the pre-rebuild state)
- Stack: Python ≥ 3.11, setuptools package `asis`; extras for AI (`ollama`, `requests`), voice (`faster-whisper`, `silero-vad`, `sounddevice`, torch stack, openwakeword), dev (pytest/ruff/black)
- Entry points: `asis` console script (`asis.cli.main:entry`) and `python -m asis`

## 3. What is actually implemented (the `asis` package)

### `asis/cli` — console entry point
- Wires identity, local memory, the event bus and an AI provider together. Subcommands: `--version`, `--identify`, `--list-tools`, `--message`, and a stdin REPL.

### `asis/ai` — model interaction
- `AIManager`, `AIMessage`/`MessageRole`, conversation and context engines, inference engine; providers: `OllamaProvider` (real) and `MockAIProvider`.

### `asis/memory` — local memory
- SQL file database (`MemoryDatabase`), `MemoryStorage` CRUD, `MemoryManager`, `MemorySearch`. Local-only: A.S.I.S. memory does not persist through R.E.S.C.S. today.

### `asis/tools` — tool framework
- `Tool` base, shared registry, router, executor with authorization, native function-calling primary + heuristic fallback. Concrete tools: offline calculator (30 ops, SymPy-verified), offline translation (136 langs), web search/fetch (SSRF-guarded, opt-in ASIS_WEB_ENABLED), coding workspace tools (A.S.C.S. modes), 7 CORE tools (discover/info/status/data/service/agent/send, HIGH confirmation-gated). Dangerous tools ship gated — none ungated.

### `asis/permissions`, `asis/identity`, `asis/events`, `asis/configuration`
- Permission models with confirmation prompts, sandbox path resolution, secrets/validation helpers; `Identity`/`build_identity` and personality; thread-safe event bus; env-driven settings.

### `asis/system` — runtime
- Component model, lifecycle, runtime, state, interrupt handling.

### `asis/voice` — pluggable voice pipeline
- Pipeline/factory abstraction (mock default; faster-whisper/STT, pyttsx3/TTS, Silero VAD, wake-word optional). Shares `AssistantApp.chat()`; real-engine hardware validation NOT PERFORMED.

### Tests
- Top-level `tests/` suite (42 files, 693 passed 2026-09-18): config, ai/conversation/memory, calculator (62), translation (54), web (89), tools/permissions, coding, voice, CLI/interactive, offline, CORE adapter/tools (7 files); runs via `python3 -m pytest -q`.

## 4. Legacy material (removed)

Pre-rebuild Forza-era trees (`core/`, `02_voice/`, `monitoring/`) were **removed** from the working tree (history only). Do not build on them; `pyproject.toml` + `requirements/` are authoritative.

## 5. A.S.I.S. ↔ C.O.R.E. ↔ R.E.S.C.S. integration (CORE real-optional, RESCS future)

- `integrations/core` — `RealCoreAdapter` + `CoreConnectionManager` over `CORE-CLIENT/CoreDeviceClient` (TCP+TLS, `CORE_HANDSHAKE`→auth→`DEVICE_REGISTER`→online). Opt-in via `ASIS_CORE_ENABLED=true`; standalone by default. Local operation survives host loss; reconnect bounded/stop-aware; `CORE_UNAVAILABLE` on failure. Physical LAN validation NOT PERFORMED.
- `integrations/rescs` — placeholder adapter (`available()->False`); future storage flows via C.O.R.E., never direct.

```text
A.S.I.S. ──(optional uplink, standalone by default)──▶ CORE-HOST (via CORE-CLIENT)
A.S.I.S. ──(future, via C.O.R.E.)──▶ R.E.S.C.S.
```

## Related

- [System Boundaries](../architecture/system-boundaries.md)
- [Data Flow](../architecture/data-flow.md) — A.S.I.S. memory is local today
- [Integration Contracts](../interfaces/integration-contracts.md)
- [Trust Boundaries](../security/trust-boundaries.md)
- ADR [0002](../decisions/0002-asis-independent-from-core.md)
