# T.I.V.I.S.S. — Though I'm Vanquished, I'm Still Stronger

> [!NOTE] **Status:** Foundation **IN DEVELOPMENT** (v0.1.0 on GitHub: `https://github.com/Kishir298/TIVISS`, cloned locally at `RISARMS/TIVISS/`). The standalone `tiviss` codebase has an implemented identity model, ownership state model, agent foundation, memory abstraction, integration adapter interfaces (C.O.R.E./R.E.S.C.S., local/mock only) and a runtime. It is still foundation-only: no live traffic, no real handover. The real-world handover mechanism is intentionally not implemented yet, and the long-term handover model is still to be determined.

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

- GitHub: `https://github.com/Kishir298/TIVISS` (v0.1.0 foundation)
- Local workspace: present at `RISARMS/TIVISS/` (full clone, stdlib-only runtime, 14 offline tests). Still foundation-only — no live traffic.
- Integration adapters (`IntegrationAdapter` plus C.O.R.E./R.E.S.C.S. adapters) are interfaces and local/mock implementations only — they do not connect to the real C.O.R.E. or R.E.S.C.S. yet.

> [!IMPORTANT] T.I.V.I.S.S. must not be confused with A.S.I.S. or with [A.S.C.S.](asc.md): three distinct systems with distinct identities.

## Related

- [System Boundaries](../architecture/system-boundaries.md) — identity/memory/permissions ownership
- [Trust Boundaries](../security/trust-boundaries.md) — per-agent identity isolation
- [Development Roadmap](../development/roadmap.md)