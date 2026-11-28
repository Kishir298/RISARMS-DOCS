# Implementation Plan — 2026-11-28

Two sequenced plans, executed in order:

1. **Plan A** — execute `AGENT.md` (operating guide / workspace protocol).
2. **Plan B** — execute the RISARMS completion brief. Plan B starts only after
   Plan A is fully complete.

`DOCS/` is the local checkout of `Kishir298/RISARMS-DOCS`; `RISARMS-HO/` is the
local checkout of `Kishir298/RISARMS-HOST`.

---

## Plan A — Execute `AGENT.md`

Source: root `AGENT.md` → canonical `DOCS/AGENT.md`.

### A1. Repository sync protocol (§7)

1. Confirm all ten in-scope directories are Git work trees with the expected
   `Kishir298/<name>` origin.
2. Record working-tree state **before** pulling so unrelated local changes are
   never lost. Do not pull over dirty trees; report instead.
3. Pull each repository; accept only "Already up to date" / fast-forward.
   `integration-tests/` is local-only and has no remote, so it is skipped.
4. Record revision + branch per repository for the final report.

### A2. Scope and ownership check (§1)

5. Confirm the ten directories exist and are the in-scope roots.
6. Confirm out-of-scope entries (`Flavora/`, `.incoming/`, `.backups/`,
   `old-versions/`, `integration-tests/`) are untouched.
7. Do not touch `.git/` history in any repository.

### A3. Method (§2) — parallel worker fan-out

8. Run the ecosystem work as ten logical workers, one per root, with no
   cross-writes: each worker inspects → edits → runs scoped tests → reports.
   Concurrency is achieved by batching independent tool calls per stage.
9. Coordinator (this session) merges reports and runs cross-system checks.

### A4. Taxonomy and truthfulness (§3)

10. Use only `IMPLEMENTED` / `IN DEVELOPMENT` / `PLANNED` / `FUTURE`.
11. Never describe a placeholder/interface as complete.
12. Apply the stale-tree and orphan-venv rules only after verifying `*.py`
    counts; never delete `.git/`.

### A5. Edit discipline (§2, §4)

13. Prefer file tools for edits; shell only for `pytest`, `ruff`, `git
    status/diff`, and existence checks.
14. Minimal edits; preserve unrelated local changes.
15. After each new/edited module, run the narrowest relevant test immediately
    (immediate debugging requirement).

### A6. Build handoff (§5) — adapted for this run

16. The guide says "do not commit". The user's instruction for this task
    explicitly overrides that: commit and push in stages. Record the override
    in the final report.
17. Each stage ends with: files changed, tests run with counts, and remaining
    known non-blocking lint items (E501/SIM117; `F401` must be zero).
18. Finish with a `risarms-host`-independent verification pass: `ruff check`
    (F rules) and scoped `pytest` per repository.

### A7. Safety/privacy (§3, §8 of brief)

19. Scan edits for secrets; never log credentials, tokens or prompt bodies.
20. Add ignore entries for any file that must not be committed (local DBs,
    caches, virtualenvs, scratch artifacts) before staging.

---

## Plan B — Execute the completion brief

Ordered by dependency, not by brief numbering. Plan A completes first.

### B1. Establish ownership + interfaces (brief §1, §8)

1. Record the authoritative ownership matrix in `DOCS/architecture/` and link
   it from `DOCS/systems/`.
2. Verify no subsystem imports another's private internals for the new code:
   integration only through HTTP/JSON contracts with versioned schemas.

### B2. TIVISS becomes security-only (brief §2)

3. Keep the existing policy engine (`tiviss_security_host.engine`), capability
   tokens (`tiviss_security_protocol.tokens`), framing and the local PDP.
4. Implement `TIVISS-CLIENT` beyond its scaffold:
   - authenticated transport to CORE (bearer credential from env/file, TLS
     verification on by default, credentials never logged);
   - versioned policy bundle retrieval + local cache + revocation handling;
   - bounded, durable, idempotent offline security-event queue;
   - transfer verification (authenticated size + SHA-256), staged temp files,
     incomplete/unverified handling;
   - optional scanner integration with distinct CLEAN / DETECTED / ERROR /
     NOT_SCANNED outcomes (unavailable ≠ clean);
   - quarantine and authorized release.
5. Add CLI subcommands and tests using hashing fixtures and a mock scanner.
6. Security status/policy/event surfaces replace TIVISS chat controls in CORE
   and RISARMS-ui (document; remove launch paths where present).

### B3. RESCS provisioning + quota (brief §3)

7. New `rescs.quota`: byte-denominated policy with budget, reserved headroom,
   equal shares over active eligible accounts, explicit admin overrides,
   per-area limits (files / messages / AI memory), AI-memory cap 20 GB → 15 GB
   at ≥5 active users, over-quota reporting that never deletes data.
8. New `rescs.provisioning`: idempotent three-area provisioning
   (user storage, inter-device chat logs, AI chat logs + structured memory).
   Document the brief's three-vs-four discrepancy.
9. Atomic-ish enforcement behind a lock shared by normal writes, resumable
   uploads and retries; over-quota blocks growth.
10. Usage/capacity/quota status reporting to CORE with unavailable ≠ zero.

### B4. Structured AI memory (brief §4)

11. Replace ASIS's unavailable adapter with an optional authenticated CORE
   client; keep local persistence when CORE is unreachable.
12. Versioned memory schema, stable ids, idempotent retries, tombstones,
   conflict preservation, explicit local-only vs synchronized control.

### B5. Device enrollment/approval (brief §5)

13. Split account approval from device approval: new devices start `pending`
    and cannot authenticate until owner approval; approval requires
    reauthentication; rejection and revocation are audited; revocation
    invalidates sessions immediately.
14. Identity always derived from the presented credential, never request body.
15. Document bootstrap (initial owner) without weakening later enrollment.

### B6. Supervision + resources (brief §6)

16. Shared versioned health/reporting contract (heartbeat, readiness/liveness,
    CPU/RAM/storage where measured, unavailable as `null`).
17. Bounded failure detection/backoff/restart limits, deduplicated alerts with
    severity and retention; resource-aware admission using measured values.
18. systemd/runit integration stays in RISARMS-HOST; avoid competing restart
    loops; do not claim Python settings reserve RAM.

### B7. ASCS permission model (brief §7)

19. New `agent.permissions`: `ASK` / `ALLOW_FOR_ME` / `FULL_ACCESS` separate
    from `PLAN`/`BUILD`/`AUTO`.
20. Real command analysis (executable + argv + cwd + shell composition),
    conservative handling of `;`, `&&`, `|`, redirection, substitution and
    interpreters; persistent user rules with scope (once/session/persistent).
21. Same authorization path for the main loop, task executor, verification and
    UI-launched jobs; approval dialogs carry the actual action + arguments.
22. Preserve workspace containment; document workspace ≠ sandbox.

### B8. Tests, docs, deployment (brief §9, §10)

23. Tests per area (see the checklist), run scoped suites, record commands and
    results; separate static/unit vs booted-system vs physical-device checks.
24. Update `DOCS/` (architecture, systems, interfaces, security, development),
    component compatibility manifests and release instructions.
25. Update `DOCS/requirements.txt` with any new third-party dependency; install
    with pip from that file.
26. Flag pin updates that need later authorized commits; do not invent hashes;
    do not publish releases.

### B9. Commit and push in stages

27. Stage commits per repository/area, verify `git status`/diff first, add
    ignore rules for files that must not be committed, then push only after
    the stage's tests pass.

### B10. Final audit

28. Produce one requirement checklist mapping each brief item to implementation
    + evidence, with explicit blockers. Open a follow-up audit list for
    anything still incomplete.
