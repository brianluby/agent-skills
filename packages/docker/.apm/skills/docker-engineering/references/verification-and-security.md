# Docker verification and security

Use the repository's exact build command where available. Never pass real secrets to a test build unless the user explicitly authorizes the target and mechanism.

## Build and inspect

```sh
docker build --progress=plain -t local/test-image .
docker image inspect local/test-image
docker history --no-trunc local/test-image
docker run --rm local/test-image <self-check>
```

Inspect effective user, entrypoint/command, environment names (not secret values), labels, architecture, exposed ports, layer history, and final image contents. Confirm excluded source, credentials, caches, and build tools are absent. Treat inspect/history output as sensitive and keep it out of shared logs: legacy images may already contain secrets in layer metadata.

## Runtime behavior

- Start with production-like command, user, mounts, and read-only/resource restrictions.
- Verify expected writable paths explicitly.
- Send the normal stop signal and confirm graceful termination and child cleanup.
- Exercise health/readiness transitions, dependency failure, and restart behavior.
- Confirm published ports and network reachability are no broader than intended.

## Compose and platforms

```sh
docker compose config --quiet
docker compose build
docker compose up --wait
```

Review rendered configuration carefully because interpolation and overrides can alter mounts, ports, privileges, commands, and secret sources. Run `up` only in an isolated non-production project with reviewed environment inputs. For multi-platform images, build/test each supported architecture via the repository's buildx workflow; a manifest alone does not prove the binary runs.

## Supply chain

Generate or inspect the configured SBOM/provenance, scan with the repository's chosen tool, and prioritize exploitable runtime findings. Confirm base-image update policy, digest/signature requirements, license constraints, and reproducible dependency inputs. Do not suppress findings without a documented rationale and expiry.
