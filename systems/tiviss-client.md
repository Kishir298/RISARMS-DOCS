# T.I.V.I.S.S. Client — device security client

> [!NOTE] **Status:** v0.2.0 **IMPLEMENTED** (device security client).
> Verified: **72 passed**, `ruff check --select E9,F,I` clean (2026-11-28,
> Windows Python 3.14 when produced; stdlib only, no runtime dependencies).

- **Repository:** `RISARMS/TIVISS-CLIENT/` — remote
  `https://github.com/Kishir298/TIVISS-CLIENT`
- **Distribution:** `tiviss-client` 0.2.0, `requires-python >= 3.10`
- **Console script:** `tiviss-client` → `tiviss_client.cli:main`
- **Counterpart:** [T.I.V.I.S.S. host](tiviss.md) — policy engine, capability
  tokens and local PDP

## Implemented surface

| Module | Responsibility |
| --- | --- |
| `transport.py` | Authenticated HTTPS JSON client (stdlib TLS, verification on by default, bounded streaming download) |
| `policy.py` | Versioned policy bundle, durable cache, revocation handling, deny-wins fail-closed evaluation |
| `events.py` | Bounded durable SQLite security-event queue with idempotent ids, dead letters, overflow reporting, redaction |
| `integrity.py` | Authenticated size + SHA-256 verification, staging, incomplete-download discovery |
| `scanner.py` | `CLEAN` / `DETECTED` / `ERROR` / `NOT_SCANNED` outcomes; ClamAV INSTREAM backend |
| `quarantine.py` | Isolated quarantine with metadata and authorized, hash-reverified release |
| `security.py` | Facade composing the above, including fetch → verify → scan → quarantine policy |
| `cli.py` | `policy show/refresh`, `events list/enqueue/flush`, `transfer fetch`, `quarantine list/release` |

## Policy contract (v1)

`GET /v1/security/policy` returns:

```json
{
  "schema_version": 1,
  "policy_version": "2026-11-28.1",
  "issued_at": 1764374400,
  "expires_at": 1764374700,
  "allow": ["file.read"],
  "deny": ["memory.write"],
  "rules": [{"effect": "allow", "action": "file.read", "subject": "*", "resource": "*"}],
  "revoked_capabilities": [{"jti": "...", "reason": "rotated"}]
}
```

Deny rules win; no matching rule is a denial. A cached policy past
`expires_at` is unusable. The client never treats a failed refresh as a reason
to relax policy.

## Event contract (v1)

`POST /v1/security/events` accepts a bounded batch:

```json
{"schema_version": 1, "device_id": "…", "events": [
  {"event_id": "…", "kind": "transfer.quarantined", "severity": "error",
   "occurred_at": 1764374400.0, "details": {…}}],
 "dropped_since_last_report": 0}
```

`event_id` is stable, so retries are idempotent. A response may list
`accepted` ids and `rejected` entries; rejected events are dead-lettered rather
than retried forever. Details are redacted before they are stored locally.

## Transfer and scanning rules

1. Fetch metadata through the authenticated transport.
2. Stream into a `.part` staging file, bounded by the declared size.
3. Verify byte count and SHA-256; on mismatch delete the staging file.
4. Scan the verified file (if configured) and classify.
5. Only `CLEAN` is accepted by default. `DETECTED`, `ERROR` and
   `NOT_SCANNED` are quarantined unless the operator explicitly passes
   `allow_unscanned` for `NOT_SCANNED`; that opt-in is recorded as a security
   event.

Quarantine release is never automatic: it goes through policy
(`quarantine.release`) and re-verifies the payload hash.

## Not implemented here

Distributed encryption, end-to-end guarantees, and protection from a
compromised server or machine administrator. These are not claimed.
