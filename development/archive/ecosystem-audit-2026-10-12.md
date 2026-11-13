# RISARMS Ecosystem Audit Report (Historical, 2026-10-12)

> **SUPERSEDED:** RESCS is now implemented, CORE is a bundle, and the
> workspace has seven active repositories. See
> [Build report 2026-11-12](../build-report-2026-11-12.md) and
> [Audit to-do 2026-11-12](../audit-todo-2026-11-12.md) for current status.

## Scope
- Repositories: ASIS, CORE, RESCS, ASCS, TIVISS, RISARMS-DOCS
- Workspace: C:\Users\rishi\Desktop\RISARMS
- Source Revision: Current HEAD (dirty state preserved)

## Findings by Subsystem
### ASIS
- **Status**: Implemented & verified (startup, mock, config, TUI, tools, CORE adapter)
- **Verified**: `npm run asis` boot, mock mode bypass, config precedence, TUI rendering, shutdown cleanup
- **Partially Verified**: Voice hardware (mocks pass), Offline mode (simulated), CORE LAN (requires physical setup)
- **Defects Fixed**: ES module mismatch, null model crash, invalid Textual CSS, .env path, config sync, mock routing, process cleanup, venv repair, missing pytest-asyncio

### CORE
- **Status**: Implemented (optional uplink)
- **Integration**: TCP+TLS, device provisioning, bounded reconnect
- **Limitation**: LAN validation NOT PERFORMED. Requires host/client provisioning.

### RESCS
- **Status**: Future boundary
- **Implementation**: Placeholder adapter only. No active routing or storage categories implemented.

### ASCS & TIVISS
- **Status**: Internal coding mode & identity subsystem
- **Integration**: TIVISS wired into ASIS identity layer. ASCS uses shared provider/workspace.

## Integration Discrepancies
- Node/Python config precedence mismatched (fixed)
- Mock mode previously required Ollama (fixed)
- CORE device provisioning credential runtime-only (documented)

## Verification Performed
- Static audit of startup chain & configuration
- Targeted repairs applied & tested
- Mock mode & shutdown verified
- Physical hardware/Wi-Fi-off/CORE LAN NOT verified

## Documentation Discrepancies
- Outdated startup instructions removed
- Mock mode & config precedence clarified
- RESCS marked as future boundary
- Voice/Offline limitations explicitly stated
