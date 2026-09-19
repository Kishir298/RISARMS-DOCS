# T.I.V.I.S.S. — Though I'm Vanquished, I'm Still Stronger

> [!NOTE] **Status:** Agent **IN DEVELOPMENT** (v0.2 capabilities on GitHub: `https://github.com/Kishir298/TIVISS`, cloned locally at `RISARMS/TIVISS/`). Beyond the v0.1.0 foundation (identity, ownership, runtime, memory, permissions, handover state model), TIVISS now has: an interactive CLI (`tiviss` REPL + `--message`, `python -m tiviss`), versioned secret-free state export/import, structured JSON-lines logging, provider timeouts, a replaceable voice abstraction (mocks only), and real stdlib-only transports — `core_tcp` (TCP+TLS external-device protocol) and `rescs_http` (RESCS records API, `tiviss.*` namespaces) — all tested offline against fakes. No live traffic is claimed until exercised against real C.O.R.E./R.E.S.C.S. hosts. The real-world handover mechanism is intentionally not implemented yet.

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

## Related

- [System Boundaries](../architecture/system-boundaries.md) — identity/memory/permissions ownership
- [Trust Boundaries](../security/trust-boundaries.md) — per-agent identity isolation
- [Development Roadmap](../development/roadmap.md)