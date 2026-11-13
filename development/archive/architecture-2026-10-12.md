# RISARMS Architecture (Historical, 2026-10-12)

> **SUPERSEDED:** This snapshot predates the seven-system layout, the CORE
> bundle, and the RESCS implementation. See
> [Architecture Overview](../../architecture/overview.md) for current content.

## Overview
R.I.S.A.R.M.S. is a modular AI ecosystem with ASIS as the primary intelligence/assistant layer. CORE provides optional device uplink. RESCS is a future storage boundary. ASCS handles internal coding. TIVISS manages identity/timeline.

## Subsystem Relationships
- `ASIS` ↔ `CORE`: Optional TCP+TLS uplink. ASIS remains standalone if CORE disabled.
- `ASIS` ↔ `RESCS`: Placeholder adapter. No active integration.
- `ASIS` ↔ `ASCS`: Shared provider/model. Workspace-bound tools.
- `ASIS` ↔ `TIVISS`: Identity analysis & persona simulation wired into ASIS.

## Startup Chain
`npm run asis` → Node launcher (`scripts/asis.mjs`) → `.venv` Python → `python -m asis` → CLI entry → Textual TUI → Boot orchestrator.

## Configuration Precedence
1. Explicit CLI overrides (`--model`, `--provider`)
2. Process environment variables (`ASIS_AI_MODEL`, `ASIS_AI_PROVIDER`)
3. `.env` file (resolved from repository root)
4. Built-in defaults (`qwen3:14b`, `ollama`)

## AI Providers & Routing
- `ollama`: Default. Local inference. Health-checked on boot.
- `mock`: Bypasses Ollama. Uses simulated responses. Works offline.
- `core`: Optional uplink to CORE-HOST. Fails cleanly if unavailable.

## Tools & Permissions
- Native function calling primary. Heuristic fallback.
- HIGH/CRITICAL tools gated by confirmation.
- Web tools SSRF-guarded. Calculator offline (SymPy). Translation offline (MADLAD-400 optional).

## Voice Pipeline
- Pluggable: audio input → VAD → wake-word → STT → speaker ID → TTS → output.
- Heavy dependencies optional. Mocks in `asis/voice/engines/mock.py`.
- Hardware NOT PERFORMED.
