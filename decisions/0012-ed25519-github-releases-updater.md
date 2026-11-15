# 0012 — Ed25519-signed GitHub Releases updates

- Status: Accepted
- Date: 2026-11-15

## Context

Products must update without cloning git repositories or depending on PyPI.
Update metadata and artifacts need an offline-verifiable trust root.

## Decision

Use GitHub Releases as the distribution channel and **Ed25519** as the signing
algorithm for product updates.

- Each release publishes `update.json`, `SHA256SUMS`, an SBOM and the artifacts.
- `update.json` carries version, channel, artifact hashes, compatibility data and
  an Ed25519 signature over the canonical manifest bytes.
- Production clients embed only the public key; the current UI accepts an operator-supplied key until that key is provisioned. The private key is never committed.
- Check and install are separate actions; no silent auto-install.
- CORE and RESCS updates require an owner device, explicit confirmation, a
  backup, service stop, health checks and rollback.
- Stable and beta channels are supported; the default is stable.
- The production public key and SHA-256 fingerprint are supplied out of band before release verification is enabled.

## Consequences

- The updater is inert until the public key is configured.
- Release workflows must publish the manifest and signature atomically.
- Git/pip self-updaters in products are replaced by release manifests.
