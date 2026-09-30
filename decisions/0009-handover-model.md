# 0009 — Handover Model for T.I.V.I.S.S.

**Status:** Accepted
**Date:** 2026-09-30
**Deciders:** T.I.V.I.S.S. team
**Technical Story:** TIVISS-009

## Context

T.I.V.I.S.S. (TIVISS) is a separate AI agent in the R.I.S.A.R.M.S. ecosystem that needs to support session handover -- the ability to transfer an active conversation session (including context, history, and state) to another agent or to persist it for later resumption.

The handover mechanism must:
1. Be interoperable with other R.I.S.A.R.M.S. agents (especially A.S.C.S. for coding tasks)
2. Use the R.E.S.C.S. storage system for persistence
3. Maintain audit trail and ownership semantics
4. Support both explicit handover requests and automatic checkpointing

## Decision

We adopt a **state-machine-based handover model** with the following characteristics:

### Handover State Machine

The handover progresses through defined states:
- REQUESTED -> APPROVED -> COMPLETED
- REQUESTED -> REJECTED
- REQUESTED -> CANCELLED

Transitions are validated and require explicit approval from the current owner.


### Data Model

**HandoverRequest** (stored in R.E.S.C.S. namespace 	iviss.handover.{session_id}):

`json
{
  "task": "original task description",
  "plan": { ... },
  "completed_actions": [...],
  "observations": [...],
  "partial_results": { ... },
  "context_index_ref": "tiviss.context_index.{session_id}",
  "experience_tags": ["tag1", "tag2"],
  "workspace": "/absolute/path",
  "timestamp": "2026-09-30T14:17:50.171458+00:00",
  "from_agent": "tiviss",
  "to_agent": "ascs"
}
`

**ConversationLogStore** (R.E.S.C.S. namespace "tiviss.chat_logs.{session_id}"):
- Append-only log of request/response pairs
- Includes metadata: timestamp, tool calls, permissions
- Queryable by session_id prefix

### Ownership Integration

Handovers are coupled with the ownership system (N14):
- Handover request must be approved by current owner
- On approval, ownership of session resources transfers to target agent
- Audit trail records all transitions (HANDOVER_REQUESTED, APPROVED, REJECTED, CANCELLED, COMPLETED, OWNERSHIP_CHANGED)

### R.E.S.C.S. Namespace Conventions

| Resource | Namespace |
|----------|-----------|
| Handover state | "tiviss.handover.{session_id}" |
| Conversation logs | "tiviss.chat_logs.{session_id}" |
| Context index | "tiviss.context_index.{session_id}" |
| Experience tags | "tiviss.experience.{session_id}" |

All namespaces are device-scoped via R.E.S.C.S. device validation (N13).

## Consequences

### Positive
- Clear state machine prevents ambiguous handover states
- R.E.S.C.S. integration provides durable, queryable storage
- Ownership coupling ensures security
- Interoperable with A.S.C.S. handover protocol

### Negative
- Adds complexity to session management
- Requires R.E.S.C.S. to be available for handovers

## Implementation Notes

- `tiviss/handover/state.py` -- State machine definitions
- `tiviss/handover/handover.py` -- Handover coordinator
- `tiviss/conversation/log_store.py` -- ConversationLogStore implementation
- `tiviss/memory/sqlite.py` -- SQLiteMemoryStore with `conversation_logs` table

## References

- [0007 -- A.S.C.S. Standalone Coding Agent](0007-ascs-standalone-coding-agent.md)
- [N13 -- Device-Scoped Validation](https://github.com/.../N13)
- [N14 -- Ownership Integration](https://github.com/.../N14)
