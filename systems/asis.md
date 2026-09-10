# A.S.I.S. — A Smart Intelligence System

> [!NOTE] **Status:** **IN DEVELOPMENT** — rebuilt on a new architecture. The `asis` package (v0.1.0) ships a working CLI, AI provider layer, inference/conversation/context engines, local SQL memory, a tool framework (with two concrete tools), permissions, events, and a pluggable voice pipeline, backed by a first test suite (8 test files). Legacy `Forza`-era trees (`core/`, `02_voice/`, `monitoring/`) still exist beside the new package and are deprecated. C.O.R.E./R.E.S.C.S. integration is contract-defined but **not connected**. A.S.I.S. is an **independent project**.

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

- Location: `RISARMS/ASIS/` (sibling of `CORE/`, `RESCS/`, `ASCS/`, `RISARMS-DOCS/`)
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
- `Tool` base, registry, router, executor with authorization, result handling — **plus two concrete tools** (`EchoTool`, `CurrentTimeTool`).

### `asis/permissions`, `asis/identity`, `asis/events`, `asis/configuration`
- Permission models with confirmation prompts, sandbox path resolution, secrets/validation helpers; `Identity`/`build_identity` and personality; thread-safe event bus; env-driven settings.

### `asis/system` — runtime
- Component model, lifecycle, runtime, state, interrupt handling.

### `asis/voice` — pluggable voice pipeline
- Pipeline/factory abstraction with engines (mock, wakeword) and input/speech/speaker/tts packages. Functional in isolation; **not wired into the chat loop yet**.

### Tests
- Top-level `tests/` suite (8 files: ai, app, cli, events, identity, memory, tools) plus voice tests; runs via `pytest`.

## 4. Legacy material (deprecated, still present)

The repository root still contains pre-rebuild trees that are **not** part of the new architecture:

| Path | Origin | Status |
|---|---|---|
| `core/` (ForzaRuntime, config/defaults, logging) | Forza-AI | Deprecated; superseded by `asis/system` and `asis/configuration` |
| `02_voice/` (input/processing/synthesis/wakeword) | Forza-AI voice work | Deprecated; superseded by `asis/voice` |
| `monitoring/` (macOS collectors) | Forza-AI system monitoring | Deprecated |
| `requirements.txt`, `setup_venv.py`, `ASIS.code-workspace` | Mixed-era tooling | Present; `pyproject.toml` is authoritative |

A `cloud/memory_api` skeleton (FastAPI/SQLAlchemy) existed in history and was deleted in the working tree. Treat deprecated trees as reference material, not as the architecture; do not build on them.

## 5. A.S.I.S. ↔ C.O.R.E. ↔ R.E.S.C.S. integration (defined, not connected)

The `asis/integrations` package defines the integration surface:

- `integrations/core` — `CoreClient` interface (`ServiceRequest`, `CoreResponse`) mirroring the eventual C.O.R.E. communication contract, plus a local `MockCoreAdapter`. **Only the mock runs today.**
- `integrations/rescs` — `StorageClient` interface and a `RESCSAdapter` placeholder that reports R.E.S.C.S. as unavailable; A.S.I.S. uses its local memory provider until integration is established.

None of this is connected to real C.O.R.E. or R.E.S.C.S. code — the interfaces are A.S.I.S.-local abstractions, and no C.O.R.E. adapter for A.S.I.S. exists yet.

```text
A.S.I.S. ──(defined interface, no live traffic)──▶ C.O.R.E.
A.S.I.S. ──(defined interface, no live traffic)──▶ R.E.S.C.S.
```

## Related

- [System Boundaries](../architecture/system-boundaries.md)
- [Data Flow](../architecture/data-flow.md) — A.S.I.S. memory is local today
- [Integration Contracts](../interfaces/integration-contracts.md)
- [Trust Boundaries](../security/trust-boundaries.md)
- ADR [0002](../decisions/0002-asis-independent-from-core.md)
