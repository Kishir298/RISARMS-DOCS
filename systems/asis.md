# A.S.I.S. — A Smart Intelligence System

> [!NOTE] **Status:** Partial — chat runtime, memory, tool framework, event bus, and part of the voice input pipeline are **IMPLEMENTED**; the voice pipeline is not yet integrated into the chat loop; the Forza→A.S.I.S. rename is **IN DEVELOPMENT**. A.S.I.S. is an **independent project**.

## 1. What A.S.I.S. is

A.S.I.S. is the **primary AI / intelligence layer** of R.I.S.A.R.M.S. It was previously developed under the internal name **Forza-AI**.

### Responsibilities

- Natural-language understanding
- Reasoning
- Response generation
- AI model interaction
- Voice functionality
- System interaction (through C.O.R.E.)
- Using C.O.R.E.
- Using R.E.S.C.S. (through C.O.R.E.)
- Potentially controlling external devices (through C.O.R.E.)

### Non-responsibilities

A.S.I.S. **does not directly own** C.O.R.E.'s responsibilities: message routing, resource registry, runtime orchestration, configuration, health, logging, security infrastructure. It *uses* them.

## 2. Independence

> [!IMPORTANT] A.S.I.S. is an independent project. It must **never** be placed inside CORE. It uses C.O.R.E. through interfaces. Rationale: ADR [0002](../decisions/0002-asis-independent-from-core.md).

- Location: `RISARMS/ASIS/` (sibling of `CORE/`, `RESCS/`, `DOCS/`)
- Own git repository (history includes branches archived for `legacy-before-rebuild` / `pre-cleanup`)
- Stack: Python, setuptools package `asis`; extras for AI (ollama), voice (whisper/torch/silero-vad/sounddevice), dev (pytest/ruff/black)

## 3. What is actually implemented (verified)

### Interactive chat runtime — `main.py` (entry point: `python main.py`)
- Streaming chat with an LLM; persona system prompt; interactive commands (`status`, `clear`, `memory`, `remember`, `forget`, `clear_memory`, `help`, `shutdown`); SIGINT/SIGTERM handling; atomic JSON memory persistence.

### `core/ai` — model interaction
- `OllamaProvider`: real HTTP calls to `/api/tags` and streaming `/api/chat`; `AIManager`; `AIProvider` abstraction; persona prompts.

### `core/memory` — memory system
- SQLite `MemoryDatabase`, `MemoryStorage` CRUD, `MemoryManager`, `MemorySearch` (LIKE-based), bounded `ConversationContext`.

### `core/runtime` — lifecycle
- State-machine runtime (`ForzaRuntime`), `LifecycleManager`, service registry (`RuntimeContext`), component abstraction.

### `core/tools` — tool framework
- Full framework: `Tool` ABC, thread-safe registry, tool router, executor with authorization, result handling. **No concrete tools are registered in the codebase.**

### `core/events`, `core/logging`, `core/security`, `core/config`
- Thread-safe typed `EventBus`; console + rotating file logging (`forza.log`); permission levels, confirmation prompts, sandbox path resolver, secrets/validation helpers; env-driven settings (currently `FORZA_*`).

### `02_voice/` — voice subsystem (standalone, **not wired into `main.py`**)
- **Input** (`input/`): `AudioBuffer`, `Microphone` (sounddevice), `VoiceActivityDetector` (silero-vad), `SpeechDetector` — implemented.
- **Recognition** (`recognition/speech_to_text.py`): real faster-whisper transcription (`SpeechTranscriber`).
- **Processing** (`processing/`): `TranscriptionNormalizer`, `VoicePipeline` — implemented.
- **Speaker, wakeword, TTS, interruptions, audio player, identification:** empty stubs (declared dependencies only).
- `tests/` is empty; a runnable voice smoke test exists at `02_voice/test_cross_platform.py`.

## 4. Known naming/version discrepancies (IN DEVELOPMENT)

Documented here so agents don't mistake them for features:

- Package/docs brand the project **A.S.I.S.**, but code artifacts still say **Forza / Forza AI** (persona prompt, config defaults `APP_NAME = "Forza"`, `FORZA_*` env vars, `forza.log`).
- Version markers disagree: `pyproject.toml` = `0.1.0`; `core/config/defaults.py` = `2.0.0`.
- The console script `asis` → `asis.cli.main:entry` is now functional: a working `asis.cli` package (added with the first test suite) wires identity, local memory, the event bus and an AI provider together, supporting `--version`, `--identify`, `--list-tools`, `--message` and a stdin REPL. `asis.app` was promoted to a proper package (`ProcessResult`, `extract_memories`, `store_auto_memories`). A top-level `tests/` suite (51 tests) now covers ai, app, cli, events, identity, memory and tools.
- `cloud/memory_api` skeleton exists in git history but was deleted from the working tree (deletion not yet committed); it used FastAPI/SQLAlchemy.
- Voice is functional in isolation but disconnected from the chat loop.

## 5. A.S.I.S. within the ecosystem (PLANNED)

The intended integration ([system-interactions](../architecture/system-interactions.md)):

```text
A.S.I.S.
   │ request
   ▼
C.O.R.E.
   │
   ▼
Router → Communication → R.E.S.C.S. adapter / device transport
```

None of this integration is implemented yet. A.S.I.S. currently runs standalone against Ollama.

## Related

- [System Boundaries](../architecture/system-boundaries.md)
- [Data Flow](../architecture/data-flow.md) — A.S.I.S. memory is local today
- [Integration Contracts](../interfaces/integration-contracts.md)
- [Trust Boundaries](../security/trust-boundaries.md)
- ADR [0002](../decisions/0002-asis-independent-from-core.md)