# T.I.V.I.S.S. — security subsystem

> [!NOTE] **Status:** **IN DEVELOPMENT → security-only (2026-11-28).**
> T.I.V.I.S.S. is the **security subsystem** of R.I.S.A.R.M.S. Its previous
> independent AI-agent role — personality, conversation, voice, model
> provider and ownership handover — is **retired**. Security policy,
> enforcement, integrity checking and security reporting remain and are
> **IMPLEMENTED** across `TIVISS-HOST` (policy engine, capability tokens, local
> PDP) and `TIVISS-CLIENT` v0.2.0 (device security client, 72 tests).
>
> Legacy AI modules still exist in `TIVISS-HOST/tiviss/` for history and were
> not deleted. They are **not** wired into CORE or RISARMS-ui, have no launch
> path in the desktop client, and must not be described as the TIVISS role.
> Removing them is tracked as follow-up work; no user data is deleted by this
> change.

## 1. Role and ownership

| Aspect | Owner | Notes |
| --- | --- | --- |
| Security policy evaluation | `TIVISS-HOST` | `tiviss_security_host.engine.PolicyEngine` — deny-wins, fail-closed default |
| Capability tokens | `TIVISS-HOST` | `tiviss_security_protocol.tokens` — HMAC-SHA256, expiry, constant-time compare |
| Local PDP daemon / IPC | `TIVISS-HOST` | `tiviss_security_host`, `tiviss_security_ipc` |
| Device security client | `TIVISS-CLIENT` | policy retrieval/revocation, offline events, verified transfers, scanning, quarantine |
| Security status UI | `RISARMS-ui` | Security page: posture, pending devices, events. No chat or model controls |
| Security API surface | `CORE-HOST` | `GET /api/security` (read-only posture), device approval routes |

T.I.V.I.S.S. connects through documented interfaces (JSON over authenticated
HTTPS/Unix sockets). It does not import another subsystem's private internals.

## 2. Implemented behaviour

### Host

- `PolicyEngine` with explicit allow/deny rules, action-pattern grammar and a
  deny-by-default posture.
- Capability tokens with required minimum secret length, expiry and tamper
  rejection.
- PDP framing and decision schema (`allow` / `deny`, request ids, obligations).
- Local PDP daemon reachable over a Unix-domain socket; unsupported platforms
  fail with an actionable message and never fall back to permissive mode.

### Client (`TIVISS-CLIENT` v0.2.0)

- Authenticated HTTPS transport with TLS verification on by default; plain
  HTTP requires an explicit opt-out.
- Versioned policy retrieval (`schema_version: 1`), durable cache and
  revocation handling. Missing/expired/malformed policy is a denial.
- Bounded, durable SQLite security-event queue: stable event ids (idempotent
  delivery), bounded capacity with honest dropped counts, dead-lettering,
  secret redaction before storage.
- Transfers verified against authenticated size + SHA-256 metadata, staged in
  `.part` files; incomplete or mismatched downloads never reach the download
  directory.
- Optional ClamAV integration with four outcomes: `CLEAN`, `DETECTED`,
  `ERROR`, `NOT_SCANNED`. Unavailable scanning is **never** treated as clean.
- Quarantine store with metadata and release that requires an explicit policy
  authorization and re-verifies the payload hash.

### Enforcement in protected operations

Authorization checks fail closed when the policy service is unavailable. An
explicitly configured embedded policy is supported; there is no silent
fallback from a failed remote fetch to a permissive default.

## 3. Explicit non-claims

- No invented cryptography and no distributed encryption offloading.
- Transport encryption (TLS), integrity checking (SHA-256) and encryption at
  rest are separate properties, described separately.
- No claim that a device cannot be affected by server compromise.
- No end-to-end encryption claim.

## 4. Configuration

| Variable | Purpose |
| --- | --- |
| `TIVISS_CORE_URL` | C.O.R.E. base URL |
| `TIVISS_DEVICE_ID` | Registered device id (issued by CORE after approval) |
| `TIVISS_DEVICE_CREDENTIAL` / `TIVISS_CREDENTIAL_FILE` | Device credential (secret) |
| `TIVISS_STATE_DIR` | Local state directory (default `~/.tiviss`) |
| `TIVISS_TLS_VERIFY` | `0` only for explicit test endpoints |
| `TIVISS_CA_FILE` | Optional private CA bundle |
| `CORE_SECURITY_MODE` | `embedded` (default) or `daemon` for the CORE PDP |

## 5. Repositories

- `https://github.com/Kishir298/TIVISS-HOST` — host security packages (and
  legacy AI modules pending removal).
- `https://github.com/Kishir298/TIVISS-CLIENT` — device security client
  (`tiviss-client` 0.2.0).
