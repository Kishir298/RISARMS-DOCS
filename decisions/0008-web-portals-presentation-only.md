# Web portals are presentation-only control planes

## Context

C.O.R.E.-HOST and C.O.R.E.-CLIENT need human-operable dashboards (device
visibility, health, capability/AI offload, R.E.S.C.S. access) without
forcing all management through terminal commands. The risk is a third
subsystem that duplicates C.O.R.E.: its own registries, schedulers,
persistence, or security model.

## Decision

Host and client portals are **presentation/control interfaces only**:

- They consume existing authorities (DeviceRegistry, ResourceRegistry,
  OrganizationEngine, Router, ServiceManager, AgentScheduler,
  HealthMonitor, Runtime, RESCS adapter) through public APIs and never
  manipulate internal dictionaries, sockets, or persistence files.
- No duplicate scheduler, registry, database, or auth model is introduced.
- Both bind `127.0.0.1` by default; remote administration is explicit
  opt-in. No authentication on the portal itself: localhost reach is the
  boundary, and the browser never becomes an alternate auth channel
  (no credentials in URLs, storage, or logs; session tokens render only
  as `ACTIVE`).
- Stack stays minimal: stdlib HTTP servers + plain HTML/CSS/JS with
  polling (no frontend framework, no WebSockets in v0.4.0); the client
  stays stdlib-only with no CORE-HOST imports.

## Alternatives

- **Full admin framework / SPA build** — rejected: dependency and build
  burden disproportionate to dashboard needs.
- **Portal-owned state and direct registry writes** — rejected: would fork
  the authorities the portal is meant to display.
- **Remote-by-default binding** — rejected: expands the trust boundary
  without an explicit decision.

## Consequences

- Positive: uniform, testable dashboards on both sides with zero new
  runtime dependencies; all portal behavior covered by automated tests
  including secret-redaction negatives.
- Cost: UI richness is bounded by hand-written HTML/JS; live updates are
  poll-based.
- Guardrail: any portal feature that needs new state must add it to the
  owning authority first, never to the portal.

## Status

Accepted. Implemented in v0.4.0 (`CORE-HOST/core/portal/`,
`CORE-CLIENT/client/portal/`).
