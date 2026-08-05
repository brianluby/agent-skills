---
name: docker-engineering
description: Use when creating, reviewing, debugging, securing, or optimizing Dockerfiles, container images, build contexts, Compose services, and container runtime behavior.
---

# Docker engineering

Read the Dockerfile syntax directive, build context, `.dockerignore`, Compose files, CI build command, target platforms, runtime orchestrator, and application shutdown/health behavior before editing. Reproduce with the same BuildKit, targets, arguments, and platform assumptions used by CI.

## Image construction

- Use multi-stage builds to separate toolchains from runtime artifacts. Copy only required outputs into the final stage.
- Pin base images according to repository policy; use immutable digests where reproducibility or supply-chain policy requires them, with an explicit update process.
- Order layers for useful cache reuse without copying secrets or the whole repository prematurely. Use BuildKit secret/SSH mounts for credentials—never `ARG`, `ENV`, or copied files.
- Combine package installation and cleanup in one layer, use noninteractive flags, and avoid unverified remote `curl | sh` installers.
- Run as a non-root user unless the workload has a documented requirement. Make ownership correct at build time rather than broad runtime `chmod`.
- Use exec-form `ENTRYPOINT`/`CMD` and ensure PID 1 receives signals, reaps children when necessary, and exits within the platform's grace period.
- Keep health checks meaningful, cheap, and independent of optional external dependencies. A container health check is not a substitute for service readiness design.
- Do not bake environment-specific configuration, tokens, certificates, SSH keys, cloud credentials, or `.env` files into layers.

## Runtime and Compose

Define persistent data, read-only configuration, secrets, ports, networks, dependencies, resource expectations, and restart behavior explicitly. Avoid privileged mode, host namespaces, Docker socket mounts, broad capabilities, and writable root filesystems unless justified by a reviewed threat model.

## Change workflow

1. Inspect every stage and what enters the build context.
2. Build the exact target/platform without secret material and review the resulting history and contents.
3. Run as the configured user, exercise startup, health, signal-driven shutdown, and failure behavior.
4. Test Compose configuration and dependency behavior when changed.
5. Scan image packages/configuration using repository tooling and evaluate findings against reachability and base-image update policy.

Load `references/verification-and-security.md` for concrete build, inspection, Compose, multi-platform, SBOM, and runtime checks.
