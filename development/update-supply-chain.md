# Update supply chain

## Channel

GitHub Releases only. No product self-updates from git, PyPI or a mutable branch.

Every release publishes:

| Asset | Purpose |
|---|---|
| Platform installers/archives | Signed application artifacts |
| `update.json` | Version, channel, compatibility and artifact hashes |
| `SHA256SUMS` | Human-readable artifact digests |
| `sbom.cdx.json` | CycloneDX dependency inventory |

## Manifest

`update.json` is canonical JSON with sorted keys and compact separators. The
`signature` field is Ed25519 over the manifest with `signature` removed.

```json
{
  "schema": 1,
  "product": "RISARMS-UI",
  "version": "0.7.0",
  "channel": "stable",
  "min_version": "0.6.0",
  "artifacts": [
    {
      "name": "RISARMS-Portal-0.7.0-windows-x86_64.msi",
      "url": "https://github.com/Kishir298/RISARMS-ui/releases/download/v0.7.0/RISARMS-Portal-0.7.0-windows-x86_64.msi",
      "sha256": "…64 hex characters…",
      "size": 12345678
    }
  ],
  "signature": "base64-ed25519"
}
```

Rules:

- The production public key must be embedded in the client before release; until
  it is provisioned, Settings accepts an operator-supplied key for testing. The
  private key lives only in CI secrets (`UPDATE_SIGNING_KEY`, base64 raw Ed25519
  seed).
- An unsigned, mis-signed, wrong-product or wrong-channel manifest is rejected.
- URLs must be HTTPS; loopback HTTP is allowed only in tests.
- Downloads are size-capped and verified against the signed SHA-256 before use.
- Check and install are separate. No update installs silently.
- Stable is the default; beta requires explicit opt-in.
- CORE/RESCS installs require a registered owner device, explicit approval, a
  backup and health-gated rollback.

## Current state

RISARMS-UI has manifest verification, artifact download verification, a
Settings check action, a release publishing job and a CycloneDX SBOM build step.
There is no install/apply UI yet. The production public key and fingerprint are
still required before a release check can work without manual key entry.
CORE/RESCS/ASIS/ASCS/TIVISS remain on their existing release process until their
updater clients are migrated.
