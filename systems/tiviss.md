# T.I.V.I.S.S. — Though I'm Vanquished, I'm Still Stronger

> [!NOTE] **Status:** Agent **IN DEVELOPMENT** (v0.3 capabilities on GitHub: `https://github.com/Kishir298/TIVISS`, cloned locally at `RISARMS/TIVISS/`). Beyond the v0.1.0 foundation (identity, ownership, runtime, memory, permissions, handover state model), TIVISS now has: an interactive CLI (`tiviss` REPL + `--message`, `python -m tiviss`), **OllamaProvider** (real Ollama HTTP API with streaming and tool calling), **SQLiteMemoryStore** (dual SQLite databases: `conversation_logs.db` for append-only conversation history and `semantic_memory.db` for structured long-term memory with categories, importance, confidence), versioned secret-free state export/import, structured JSON-lines logging, provider timeouts, a replaceable voice abstraction (mocks + real engine hooks), and real stdlib-only transports — `core_tcp` (TCP+TLS external-device protocol) and `rescs_http` (RESCS records API, `tiviss.*` namespaces) — all tested offline against fakes. New configuration for Web/Calculator/Translation/Voice pipelines mirrors ASIS. No live traffic is claimed until exercised against real C.O.R.E./R.E.S.C.S. hosts. The real-world handover mechanism is intentionally not implemented yet.

## 1. What T.I.V.I.S.S. is

T.I.V.I.S.S. is a **separate AI agent** in the R.I.S.A.R.M.S. ecosystem.

Its defining long-term purpose: **T.I.V.I.S.S. may eventually be handed over to another person.** That requires T.I.V.I.S.S. to be a genuinely independent entity — not just another instance of A.S.I.S.

## 2. Design intent

T.I.V.I.S.S. must eventually have its own:

- Identity
- Configuration
- Memory
- Permissions
- Ownership model
- Agent architecture
- Handover mechanism

## 3. The hard rule

> [!IMPORTANT] **T.I.V.I.S.S. must NOT simply become a renamed copy of A.S.I.S.**

The distinction is architectural:

| Aspect | A.S.I.S. | T.I.V.I.S.S. |
|---|---|---|
| Role | Primary assistant / ecosystem intelligence | Personal agent, transferable to a new owner |
| Ownership | R.I.S.A.R.M.S. ecosystem | Its own ownership model (design pending) |
| Handover | N/A | A defined, safe handover mechanism |
| Boundary | Uses C.O.R.E. for coordination | Same boundaries apply, plus identity isolation |

## 4. Open questions (to resolve before development)

- What does "handover" mean operationally? (Transfer of memory, of permissions, of configuration?)
- How is T.I.V.I.S.S.'s identity stored and guaranteed unique/non-fungible with A.S.I.S.?
- Who administers T.I.V.I.S.S.'s permissions after handover, and how do they degrade if unmanaged?
- Does T.I.V.I.S.S. use C.O.R.E. services, the device transport, and R.E.S.C.S. the same way A.S.I.S. does — but with its own identity profile?

Until these are resolved, T.I.V.I.S.S. remains in its remote foundation phase and must not be scaffolded as a copy of A.S.I.S. Track decisions under [Decisions](../decisions/README.md).

## 5. Where the code lives

- GitHub: `https://github.com/Kishir298/TIVISS` (v0.2 capabilities)
- Local workspace: present at `RISARMS/TIVISS/` (full clone, stdlib-only runtime, offline deterministic tests). Live transports exist but are unexercised against real hosts.
- Transports: `tiviss/integrations/core_tcp.py` (real wire protocol, session token RAM-only) and `tiviss/integrations/rescs_http.py` (`X-API-Key`, confined to `tiviss.*` namespaces) sit beside the local/mock adapters; mocks remain the default for tests.
- Storage: TIVISS cloud data lives under `tiviss.*` RESCS namespaces (see `../..`-repo `RESCS/docs/storage-domains.md`); `asis.*` and `personal.*` are never touched.

> [!IMPORTANT] T.I.V.I.S.S. must not be confused with A.S.I.S. or with [A.S.C.S.](asc.md): three distinct systems with distinct identities.

## 6. Implemented Features (v0.3)

### 6.1 OllamaProvider (Real Model Provider)

`OllamaProvider` implements the `ModelProvider` interface with real Ollama HTTP API integration:

- **Endpoint**: Configurable via `TIVISS_OLLAMA_ENDPOINT` (default `http://127.0.0.1:11434`)
- **Model**: Configurable via `TIVISS_MODEL_ID` (default `qwen3:14b`)
- **Streaming**: Native streaming support via `/api/chat`
- **Tool Calling**: Native function calling when model supports it
- **Thinking Tag Stripping**: Automatic removal of `&#8203;...&#8203;` tags for qwen3-class models
- **Timeout**: Configurable per-request timeout via `TIVISS_OLLAMA_TIMEOUT`
- **Parameters**: Temperature, `num_predict`, `keep_alive` configurable

Switch providers via `TIVISS_MODEL_PROVIDER=ollama` (default: `mock`).

### 6.2 SQLiteMemoryStore (Dual SQLite Databases)

`SQLiteMemoryStore` implements the `MemoryBackend` interface with **two separate SQLite databases**:

| Database | Purpose | Table |
|----------|---------|-------|
| `conversation_logs.db` | Append-only conversation history | `conversation_logs` (request_id, request_content, response_content, metadata, created_at) |
| `semantic_memory.db` | Structured long-term memory | `semantic_memory` (record_id, content, category, memory_type, importance, confidence, source, evidence, metadata, created_at, updated_at) |

**Conversation Logs:**
- `append_conversation(request_id, request, response, metadata)` — append exchange
- `get_conversation_history(limit, session_id)` — retrieve recent history
- `search_conversation(query, limit)` — full-text search

**Semantic Memory (implements `MemoryBackend`):**
- `store(record)` — store with category, type, importance, confidence
- `retrieve(record_id)` — retrieve by ID
- `update(record_id, content, metadata)` — update content/metadata
- `delete(record_id)` — delete record
- `search(query, limit, category, memory_type, min_importance)` — filtered search
- `clear()` — clear all memories
- `metadata()` — backend statistics

**Configuration:**
- `memory.backend=sqlite` (new backend option alongside `local` and `rescs`)
- `memory.conversation_db` — path to conversation logs DB
- `memory.semantic_db` — path to semantic memory DB
- Env vars: `TIVISS_MEMORY_CONVERSATION_DB`, `TIVISS_MEMORY_SEMANTIC_DB`

### 6.3 New Configuration Options

TIVISS configuration now mirrors ASIS for Web/Calculator/Translation/Voice:

| Section | Settings (Env Vars) |
|---------|---------------------|
| **Web** | `TIVISS_WEB_ENABLED`, `TIVISS_WEB_SEARCH_PROVIDER`, `TIVISS_WEB_TIMEOUT`, `TIVISS_WEB_MAX_RESULTS`, `TIVISS_WEB_MAX_CHARS` |
| **Calculator** | `TIVISS_CALCULATOR_ENABLED`, `TIVISS_CALCULATOR_MAX_EXPRESSION_CHARS`, `TIVISS_CALCULATOR_MAX_MATRIX_SIZE`, `TIVISS_CALCULATOR_TIMEOUT`, `TIVISS_CALCULATOR_PRECISION`, `TIVISS_CALCULATOR_ANGLE_MODE` |
| **Translation** | `TIVISS_TRANSLATION_ENABLED`, `TIVISS_TRANSLATION_PROVIDER`, `TIVISS_TRANSLATION_MODEL`, `TIVISS_TRANSLATION_MODEL_PATH`, `TIVISS_TRANSLATION_DEVICE`, `TIVISS_TRANSLATION_CACHE_ENABLED`, `TIVISS_TRANSLATION_CACHE_SIZE`, `TIVISS_TRANSLATION_DEFAULT_SOURCE`, `TIVISS_TRANSLATION_DEFAULT_TARGET`, `TIVISS_TRANSLATION_MAX_CHARS` |
| **Voice** | `TIVISS_VOICE_ENABLED`, `TIVISS_VOICE_STT_ENGINE`, `TIVISS_VOICE_STT_MODEL`, `TIVISS_VOICE_STT_DEVICE`, `TIVISS_VOICE_STT_COMPUTE_TYPE`, `TIVISS_VOICE_STT_LANGUAGE`, `TIVISS_VOICE_TTS_ENGINE`, `TIVISS_VOICE_TTS_VOICE`, `TIVISS_VOICE_TTS_SAMPLE_RATE`, `TIVISS_VOICE_SPEAKER_ENGINE`, `TIVISS_VOICE_SPEAKER_MODEL`, `TIVISS_VOICE_SPEAKER_DEVICE`, `TIVISS_VOICE_SPEAKER_CONFIDENCE`, `TIVISS_VOICE_SPEAKER_THRESHOLD`, `TIVISS_VOICE_SPEAKER_METRIC`, `TIVISS_VOICE_WAKE_ENGINE`, `TIVISS_VOICE_WAKE_THRESHOLD`, `TIVISS_VOICE_WAKE_MODEL`, `TIVISS_VOICE_VAD_ENGINE`, `TIVISS_VOICE_VAD_THRESHOLD`, `TIVISS_VOICE_MAX_UTTERANCE_S`, `TIVISS_VOICE_SILENCE_S` |

All settings load from `TIVISS_*` environment variables via `TIVISSConfig.load_env()`.

### 6.4 Provider & Memory Factory Updates

```python
# TIVISSConfig.build_provider()
if provider_id == "ollama":
    return OllamaProvider(endpoint=..., model_id=..., timeout_s=..., ...)

# TIVISSConfig.build_memory()
if backend == "sqlite":
    return SQLiteMemoryStore(conversation_db=..., semantic_db=...)
```

---

## 7. Where the code lives

- [System Boundaries](../architecture/system-boundaries.md) — identity/memory/permissions ownership
- [Trust Boundaries](../security/trust-boundaries.md) — per-agent identity isolation
- [Development Roadmap](../development/roadmap.md)