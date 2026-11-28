# Completion requirement checklist — 2026-11-28

Every item links to the implementation and the evidence actually run. A
feature is **not** marked complete because an interface or placeholder exists.
Status vocabulary: `IMPLEMENTED` / `IN DEVELOPMENT` / `PLANNED` / `FUTURE`.

## Validation levels

| Level | What was run | Result |
| --- | --- | --- |
| Static / unit | repo test suites + `ruff check --select F` (and `E9,F,I` where configured) | run below |
| Cross-repo integration | fake-transport contract tests inside each suite | run below |
| Container validation | **not run** — no container runtime in this workspace | blocked |
| Booted-system validation | **not run** — no Ubuntu/Void boot environment here | blocked |
| Physical-device validation | **not run** — no HP 14 / client hardware attached | blocked |

## Repository test evidence (2026-11-28)

| Repository | Command | Result |
| --- | --- | --- |
| TIVISS-CLIENT | `python -m pytest -q` | **72 passed** |
| TIVISS-CLIENT | `python -m ruff check tiviss_client tests` | clean |
| ASCS | `python -m pytest` | **1010 passed, 22 skipped** |
| ASCS | `python -m ruff check agent tests --select F` | clean |
| CORE-HOST | `python -m pytest` | **929 passed, 10 skipped** |
| CORE-HOST | `python -m ruff check core/health tests/health --select F` | clean |
| RESCS | `python -m pytest -q` | **338 passed, 4 skipped** |
| RESCS | `python -m ruff check` on new modules/tests `--select F` | clean |
| ASIS | `python -m pytest` | **959 passed, 19 skipped** |
| ASIS | `python -m ruff check asis/integrations tests/test_rescs_memory_sync.py --select F` | clean |
| RISARMS-ui | `python -m pytest` | **298 passed** |

Environment: Windows 11, Python 3.14.7, pytest 9.1.1. `RESCS` integration tests
requiring PostgreSQL/S3 were skipped because those services are not configured.

## 1. Component ownership

| Requirement | Status | Implementation / evidence |
| --- | --- | --- |
| CORE owns accounts/devices/routing/scheduling/coordination | IMPLEMENTED (pre-existing) | `CORE-HOST/core/web/gateway.py`, `core/scheduler`, `core/routing`; CORE suite 929 passed |
| CORE-CLIENT device communication | IMPLEMENTED (pre-existing) | `CORE-CLIENT/client`; repo 30 commits ahead of remote (not force-synced) |
| RISARMS-ui presentation + local launch + offline sync | IMPLEMENTED | `RISARMS-ui/risarms_ui/`; 298 passed |
| RESCS owns storage/namespaces/quotas/accounting | IMPLEMENTED | `RESCS/src/rescs/quota.py`, `provisioning.py`; 20 new tests |
| TIVISS owns security policy/enforcement/reporting | IMPLEMENTED (AI role retired) | `DOCS/systems/tiviss.md`; TIVISS-CLIENT 72 passed |
| ASIS and ASCS independently usable | IMPLEMENTED | ASIS 959 passed; ASCS 1010 passed; `tests/test_security_surface.py` keeps ASIS/ASCS launchable |
| Integration through documented interfaces | IMPLEMENTED | versioned JSON contracts (`security.policy` v1, `security.events` v1, memory v1, health v1) |
| No cross-import of private internals | IMPLEMENTED (new code) | new modules use HTTP/JSON or local interfaces only |

## 2. TIVISS as security subsystem

| Requirement | Status | Implementation / evidence |
| --- | --- | --- |
| Remove active TIVISS personality/conversation/voice/model/handover behaviour from the ecosystem | IMPLEMENTED (UI/routes) / **IN DEVELOPMENT** (host code) | UI navigation, local launch, tasks and settings no longer reference TIVISS AI; `SecurityPage` replaces chat. Legacy modules remain in `TIVISS-HOST/tiviss/` and are not wired anywhere; deletion is follow-up |
| Reuse policy engine, protocol, tokens, PDP daemon/client | IMPLEMENTED | `TIVISS-HOST/security/*`; CORE `core/security/pdp.py` |
| Authenticated device security integration through CORE | IMPLEMENTED | `tiviss_client/transport.py`, `security.py`; 72 passed |
| Policy retrieval + revocation handling | IMPLEMENTED | `tiviss_client/policy.py`; `tests/test_policy.py` |
| Bounded durable offline security-event reporting | IMPLEMENTED | `tiviss_client/events.py`; `tests/test_events.py` (9 tests) |
| Transfer size/hash verification with authenticated metadata | IMPLEMENTED | `tiviss_client/integrity.py`; `tests/test_integrity.py` |
| Incomplete/unverified download handling | IMPLEMENTED | `.part` staging, `incomplete_files`, `discard_incomplete` |
| Optional scanner with CLEAN/DETECTED/ERROR/NOT_SCANNED | IMPLEMENTED | `tiviss_client/scanner.py`; `tests/test_scanner.py` (6 tests) |
| Quarantine + authorized release | IMPLEMENTED | `tiviss_client/quarantine.py`; `tests/test_quarantine.py` (6 tests) |
| Never treat unavailable scan as clean | IMPLEMENTED | `scan_and_classify`; tests assert ERROR/NOT_SCANNED ≠ CLEAN |
| Policy enforcement in protected operations, fail closed | IMPLEMENTED | `PolicyService.authorize`; `DeviceSecurityClient.authorize`; tests |
| Explicit embedded policy mode, no silent permissive fallback | IMPLEMENTED | `PolicyService(embedded=...)` requires explicit construction and expiry |
| Replace TIVISS chat/model controls in CORE and UI with security status/policies/events/admin | IMPLEMENTED (status/events/admin) / **IN DEVELOPMENT** (editable policy UI) | `GET /api/security`; `RISARMS-ui/pages/security.py`. Policy *editing* is not exposed; policy is host configuration |
| Standard TLS/crypto only, no invented cryptography | IMPLEMENTED | stdlib `ssl`, `hmac`, `hashlib`; explicit non-claims in `systems/tiviss.md` |

## 3. RESCS provisioning and quotas

| Requirement | Status | Implementation / evidence |
| --- | --- | --- |
| Idempotent provisioning when an account activates | IMPLEMENTED | `rescs.provisioning.StorageProvisioner.provision`; `tests/unit/test_provisioning.py` (6 tests) |
| Failure/retry without false success | IMPLEMENTED | verifies areas + manifest after create; `ProvisioningError` |
| Three logical areas, document the 3-vs-4 discrepancy | IMPLEMENTED | `StorageArea`; documented in `quota.py` and RESCS README |
| Budget + reserved free-space headroom | IMPLEMENTED | `QuotaPolicy.total_budget_bytes` / `reserved_free_bytes`; RESCS settings |
| Equal default shares over active accounts | IMPLEMENTED | `QuotaPolicy.allocate`; test |
| Explicit administrator overrides | IMPLEMENTED | `QuotaOverride`; clamping is reported, not silent |
| Separate files/messages/AI limits | IMPLEMENTED | area fractions + per-area limits |
| AI cap 20 GB → 15 GB at ≥5 users, budget-bounded | IMPLEMENTED | `ai_memory_cap_bytes`; tests for both thresholds |
| Explicit units/accounting shared by server and UI | IMPLEMENTED (server) / **IN DEVELOPMENT** (UI quota display) | bytes / `BYTES_PER_GB` in reports and docs; no UI quota panel yet |
| Never silently delete on quota shrink | IMPLEMENTED | `QuotaManager.refresh` keeps usage; over-quota reported |
| Over-quota reports + growth restriction | IMPLEMENTED | `QuotaReport`, `growth_allowed=False`, `deletion_allowed=True` |
| Resolve overrides/over-quota vs remaining budget | IMPLEMENTED | overrides applied first from available budget, `override_clamped` flag; over-quota usage remains counted |
| Atomic enforcement across writes/uploads/retries/memory sync | IMPLEMENTED (library) / **IN DEVELOPMENT** (wiring) | `QuotaManager.reserve` under one lock; existing `FileService` has its own race-safe quota. The service has **not** been switched to the new policy object yet |
| Report usage/capacity/readiness/latency to CORE; unavailable ≠ zero | IMPLEMENTED (library) / **IN DEVELOPMENT** (transport) | `report_to_core()` with `None` I/O metrics; HTTP route not added |
| No intrusive continuous disk benchmarks | IMPLEMENTED | no benchmarking loop; only caller-supplied measured metrics |

## 4. Structured AI memory

| Requirement | Status | Implementation / evidence |
| --- | --- | --- |
| Replace ASIS's unavailable adapter with a working optional integration | IMPLEMENTED | `ASIS/asis/integrations/rescs/{remote,adapter}.py`; `tests/test_rescs_memory_sync.py` (11 tests) |
| Account-scoped cloud storage/retrieval | IMPLEMENTED | account id on every request; foreign-account response rejected; test |
| Independent of CORE when unavailable | IMPLEMENTED | `RemoteConfig` unconfigured → `disabled`; local SQLite stays authoritative |
| Durable offline sync | IMPLEMENTED | `MemorySyncStore` SQLite queue survives reopen; test |
| Stable ids/schema versions/idempotent retries | IMPLEMENTED | `schema_version: 1`, `Idempotency-Key` per op; test |
| Conflict handling preserving unsynchronised changes | IMPLEMENTED | conflict record + `#conflict-<id>` copy; test |
| Tombstone propagation | IMPLEMENTED | delete pushes tombstone; pull applies deleted records; tests |
| Quota enforcement + clear sync status | **IN DEVELOPMENT** | `SyncStatus` implemented; RESCS quota check is not yet called from the sync path |
| Explicit local-only vs synchronized control | **IN DEVELOPMENT** | configuration is explicit (opt-in env), no per-memory UI toggle yet |
| Reuse UI transcript/file queues where suitable | PLANNED | not wired; transcripts remain distinct from structured memory |
| Never expose one user's memories to another | IMPLEMENTED | account guard + redaction tests |
| Never forward server credentials to model processes | IMPLEMENTED (design) | credential lives in the integration object; model prompts only receive rendered memory text |

## 5. Per-device enrollment and approval

| Requirement | Status | Implementation / evidence |
| --- | --- | --- |
| Pending enrollment per new device | IMPLEMENTED | `Accounts.issue_device` → `pending`; 9 tests |
| Restricted pending-device access | IMPLEMENTED | `device_status` only; `device_login` rejects; test |
| Owner approval/rejection with reauthentication | IMPLEMENTED | `approve_device`/`reject_device` + gateway `admin_until` check; tests |
| Credentials activated only after approval | IMPLEMENTED (activation model) | credential exists but is inert while pending; documented |
| Credentials bound to account/device, expiry, revocation | IMPLEMENTED | existing expiry 90d + `revoke_device` |
| Immediate session invalidation on revocation | IMPLEMENTED | deletes bound sessions; test |
| Auditable enrollment/approval/revocation events | IMPLEMENTED | `audit()` writes `device_approved`, `device_rejected`, `device_revoked`, `device_bootstrap_approved` |
| Approved account login does not auto-approve a new device | IMPLEMENTED | test `test_approved_account_login_does_not_auto_approve_new_device` |
| Identity from credentials, never client-supplied owner ids | IMPLEMENTED | credential lookup; gateway uses session user |
| Documented bootstrap without weakening later enrollment | IMPLEMENTED | first owner device only; `bootstrap` flag; docs below |

## 6. Supervision and resource coordination

| Requirement | Status | Implementation / evidence |
| --- | --- | --- |
| Shared versioned health/reporting contract | IMPLEMENTED (CORE) / **IN DEVELOPMENT** (client adoption) | `CORE-HOST/core/health/contract.py`; 11 tests |
| Bounded heartbeats/readiness/liveness | IMPLEMENTED | `HealthReport.is_stale`, existing `HealthMonitor` |
| CPU/RAM/storage reporting where supported | IMPLEMENTED | `sample_resources` (Linux `/proc/meminfo`, `getloadavg`, `disk_usage`); unsupported → `None` |
| Failure detection, backoff, restart limits | IMPLEMENTED | `FailureTracker`; test |
| Admin alerts, severity, dedup, retention | IMPLEMENTED | `AlertStore`; tests |
| Client-side offline reporting queues | IMPLEMENTED (security events) / **IN DEVELOPMENT** (general health) | `tiviss_client/events.py`; no health-specific client queue |
| Recovery for approved failure cases | PLANNED | no automatic restart executor; restart policy is advisory only |
| systemd (Ubuntu) + runit (Void) integration | IN DEVELOPMENT | RISARMS-HOST units exist; no changes needed for these contracts; boot validation blocked |
| Resource-aware admission with measured values + reasons | IMPLEMENTED | `admit_job`; tests; unmeasured → queue |
| No claim that Python settings reserve RAM | IMPLEMENTED (documented) | contract docstring and this checklist |
| Preserve capacity for CORE/RESCS/other sites | IMPLEMENTED (mechanism) | configurable `reserve_bytes`; production value requires host measurement (HP 14 RAM unverified) |
| Measured hardware only | IMPLEMENTED | `sample_resources`; no hard-coded RAM assumption |

## 7. ASCS permission model

| Requirement | Status | Implementation / evidence |
| --- | --- | --- |
| Separate PLAN/BUILD/AUTO from permission modes | IMPLEMENTED | `agent/permissions.py`; config; docs |
| ASK: every command approved; other sensitive tools defined | IMPLEMENTED | `PermissionManager`; 16 permission tests |
| ALLOW_FOR_ME: verified read-only + approved rules, else approval | IMPLEMENTED | read-only executable/argv allowlist; rule match; tests |
| FULL_ACCESS: no prompts within workspace, hard denies remain | IMPLEMENTED | hard-deny patterns; test |
| Persistent user-managed rules, revocation, clear scope | IMPLEMENTED | `RuleStore` exact executable+argv+cwd; `revoke`; tests |
| Distinguish one-time/session/persistent approvals | IMPLEMENTED | `approve(persistent=False/True)`; session keys; tests |
| Evaluate executable, args, cwd, shell composition | IMPLEMENTED | `analyze_command`; tests |
| No safe classification by leading word | IMPLEMENTED | `ls; rm -rf build`, pipes, redirection, substitution, env prefix tests |
| Conservative chaining/redirection/substitution/interpreters | IMPLEMENTED | opaque classification; tests |
| Same authorization path for loops/retries/subtasks/UI jobs | IMPLEMENTED | `AgentLoop._run_tool`, `TaskExecutor._check_tool_allowed`, verification; tests |
| Approval dialogs show actual action + arguments | IMPLEMENTED | `run_command: <argv>` display; test |
| Keep workspace selection; document workspace ≠ sandbox | IMPLEMENTED | README section |
| Preserve coding/testing/verification | IMPLEMENTED | ASCS 1010 passed |

## 8. Privacy and contracts

| Requirement | Status | Implementation / evidence |
| --- | --- | --- |
| Per-user isolation across storage/messages/memories/cache/queues | IMPLEMENTED (new code) | account scoping in memory client; RESCS per-owner namespaces; CORE sessions |
| Secrets out of logs/events/prompts/exports | IMPLEMENTED | event/record redaction; device credentials excluded from `repr`; tests |
| Owner reauthentication + server-side authorization | IMPLEMENTED | `admin_until`, device approval, service grants |
| Describe transport/integrity/at-rest separately | IMPLEMENTED | `systems/tiviss.md` non-claims |
| No E2E or admin-protection claims | IMPLEMENTED | documented |
| Versioned contracts + backward-compatible migration | IMPLEMENTED | `schema_version` on policy/events/memory/health; device columns added with `ALTER TABLE` defaults |
| Contract break updates both sides + migration order | IMPLEMENTED (none broken) | additive only; see migration notes |

## 9. Deployment, docs, releases

| Requirement | Status | Implementation / evidence |
| --- | --- | --- |
| Integrate into Ubuntu 24.04 systemd candidate | **IN DEVELOPMENT** | RISARMS-HOST candidate exists; new contracts need no unit change; boot validation blocked |
| Preserve Void runit support | IMPLEMENTED (unchanged) | no changes made to Void deployment |
| Preserve Windows/macOS/Linux UI targets | IMPLEMENTED | UI suite 298 passed; mobile still deferred |
| Update docs | IMPLEMENTED | `DOCS/systems/tiviss.md`, `tiviss-client.md`, `ASIS/docs/integration.md`, repo READMEs |
| Compatibility manifests / dependencies | IMPLEMENTED (no new deps) | all new code is standard library; `DOCS/requirements.txt` unchanged |
| Release assembly / CI / installed-command checks | **IN DEVELOPMENT** | existing workflows untouched; no release published |
| Pinning strategy; no invented hashes | IMPLEMENTED | no pin changes; new commits must be pushed before pinning (see below) |
| Validation-only artifact labels; no publishing | IMPLEMENTED | no release/publish performed |

## 10. Acceptance tests added

| Area | Test file |
| --- | --- |
| ASIS/ASCS independent operation | `RISARMS-ui/tests/test_security_surface.py`, existing ASIS/ASCS suites |
| Pending account/device restrictions + owner approval | `CORE-HOST/tests/test_device_enrollment.py` |
| Expired/revoked credentials, fail-closed PDP | same + `CORE-HOST/tests/security/test_pdp.py` |
| Cross-user access rejection | `ASIS/tests/test_rescs_memory_sync.py`, `CORE-HOST/tests/test_security_status.py` |
| Corrupted transfer + honest scanner outcomes | `TIVISS-CLIENT/tests/test_integrity.py`, `test_scanner.py` |
| Idempotent provisioning/quota changes | `RESCS/tests/unit/test_provisioning.py`, `test_quota.py` |
| Concurrent quota enforcement without deletion | `RESCS/tests/unit/test_quota.py` |
| Memory sync/conflicts/retries/deletion | `ASIS/tests/test_rescs_memory_sync.py` |
| Reconnection without duplicate uploads/events | `TIVISS-CLIENT/tests/test_events.py` (idempotent ids, dead letters) |
| Health failures/recovery/resource pressure | `CORE-HOST/tests/health/test_supervision_contract.py` |
| ASCS permission modes + bypass attempts | `ASCS/tests/test_permissions.py` |
| Security UI + removal of TIVISS AI launch | `RISARMS-ui/tests/test_security_surface.py` |
| Install/backup/restore/upgrade compatibility | **not run** — requires booted deployment; blocked |

## Migration notes

### Device approval (CORE)

1. Existing `devices` rows are migrated with `status='approved'`,
   `approved_at`/`approved_by` NULL, so already-registered devices keep working.
2. New enrollments are `pending` until an owner approves from an already
   approved device after reauthentication (`POST /api/reauth`).
3. **Bootstrap:** the first device of the first owner is auto-approved
   (`bootstrap=True`); this never applies while an approved device exists.
   There is no remote way to bootstrap a later device.
4. Rollout order: upgrade CORE-HOST before RISARMS-ui. Older UI clients ignore
   the new fields; older CORE clients must send `device_credential` on re-login
   or they will enroll a new pending device (which cannot be used until
   approved).
5. Revocation deletes sessions bound to the device immediately.

### RESCS areas and quota

1. Three areas are created under `<storage>/accounts/<account>/` with a
   `provision.json` manifest (`schema_version: 1`). Existing directory layouts
   are untouched; provisioning is additive.
2. Quotas are byte-denominated (`GB = 1024³`). Existing `max_*_per_owner`
   settings still apply and are independent; migrate them only after wiring a
   single policy object into the service.
3. Shrinking a policy never deletes data; over-quota accounts are reported and
   blocked from growth.

### Policy/event/memory contracts

- All are additive `schema_version: 1` documents. Deploy CORE endpoints before
  enabling clients. Unknown fields are ignored; an unknown schema version is
  rejected (fail closed).

## Remaining blockers (explicit)

1. **Container/boot/physical validation** — no container runtime, no booted
   Ubuntu/Void host, no HP 14 hardware in this session.
2. **RISARMS-HOST pin updates** — the changed repositories have new local
   commits; pinning them requires these commits to be pushed first, which is
   only allowed with explicit authorization. No invented hashes were used.
3. **TIVISS-HOST AI modules** — legacy agent/conversation/voice/model code
   remains on disk (unwired). Removal is follow-up and must not delete user
   data.
4. **Quota enforcement wiring** — `QuotaManager` is a library; `FileService`
   still uses its own settings-based checks. A single policy object must be
   wired into files, uploads and memory sync in a follow-up.
5. **CORE-CLIENT** is 30 commits ahead / 2 behind its remote; it was not
   force-synced or pushed.
