# Contribution

> [!NOTE] **Purpose:** Rules for human and AI agents working *in this documentation repository* and for agents working *in the ecosystem's code repositories*. The docs are written to be consumable by other coding agents ([How to use this documentation](../README.md#8-how-to-use-this-documentation)).

## 1. Development philosophy

The ecosystem runs on these principles (established in [Architecture Overview](../architecture/overview.md#4-architectural-principles)):

- **Modularity** — systems remain independently developable.
- **Explicit boundaries** — each system has clearly defined responsibilities.
- **No duplicated ownership** — one owner per responsibility.
- **Contract-first integration** — systems communicate through explicit interfaces.
- **Testability** — every major integration testable independently.
- **Observable operation** — state, health, events, failures observable.
- **Controlled dependencies** — no silent dependence on another system's internals.
- **No fake functionality** — documentation never describes planned functionality as implemented.

## 2. Rules for this documentation repository

1. **Never describe planned functionality as implemented.** Use the status markers ([vocabulary](../architecture/overview.md#3-status-vocabulary)); if uncertain, mark **PLANNED** and verify.
2. **Never invent APIs.** Documentation describes architectural requirements and contracts ([interfaces](../interfaces/communication.md)); concrete APIs are locked by the owning code, not by docs.
3. **Keep the ownership table accurate.** Responsibility changes update [System Boundaries](../architecture/system-boundaries.md) first, then the owning system page.
4. **Cross-link.** New/updated docs link to related architecture, interfaces, security, and decisions documents.
5. **Consistent terminology.** Use canonical dotted names (`C.O.R.E.`, `R.E.S.C.S.`, `A.S.I.S.`, `T.I.V.I.S.S.`, `RadarS.A.R.D.`, `A.S.C.S.`) and directory forms in backticks (`CORE/`, `RESCS/`, `ASIS/`, `ASCS/`, `RISARMS-DOCS/`).
6. **Record decisions.** Any meaningful architectural choice becomes an [ADR](../decisions/README.md), even after the fact.

## 3. Rules for ecosystem code agents

1. **Respect the independence rule.** Never place R.E.S.C.S. or A.S.I.S. inside C.O.R.E. code, and never reach into another system's internals ([System Boundaries](../architecture/system-boundaries.md#4-boundary-rules-for-agents)).
2. **Contract-first.** Adding an integration: write the contract ([interfaces](../interfaces/communication.md)), get the [ADR](../decisions/README.md), then implement.
3. **One owner per change.** Route the work to the owning system per the responsibility table.
4. **Tests accompany changes** per [Testing](testing.md).
5. **No drive-by version edits** per [Versioning](versioning.md).
6. **Secrets policy.** Never commit secrets; configuration/environment only.

## 4. Contribution workflow (this repo)

1. Create/update docs in the matching directory (`architecture/`, `systems/`, `interfaces/`, `security/`, `development/`, `decisions/`).
2. Validate links and diagrams before opening a change ([Validation checklist in README](../README.md#8-how-to-use-this-documentation)).
3. Commit in logical bundles with `docs:` prefixed messages (see commit history of this repository for the pattern).

## Related

- [System Boundaries](../architecture/system-boundaries.md)
- [Development Roadmap](roadmap.md)
- [Testing](testing.md)
- [Versioning](versioning.md)
- [Decisions](../decisions/README.md)