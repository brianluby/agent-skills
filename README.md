# Agent Skills Marketplace

A public, MIT-licensed APM marketplace for small, composable skills used in agentic software work.

The goal is deliberately modest: a repository installs only the skills relevant to its stack and current work. A Rust service should not receive front-end or Terraform expertise merely because those skills exist in the catalogue.

## What is here

| Package | Purpose | Install by default? |
| --- | --- | --- |
| `foundation` | Safe repository orientation and verification workflow | Yes, for most repositories |
| `rust` | Rust implementation and Cargo workflow | Only for Rust repositories |
| `testing` | Test strategy and targeted verification | Only for testing work or test-heavy repositories |
| `code-review` | Evidence-based review process | Only for review work or review automation |

Each package is an independently versioned APM package under `packages/`. The root `apm.yml` is a marketplace catalogue, not an all-skills bundle.

## Install a focused set

Once this repository is published, register its marketplace and install only the packages required by the consuming repository:

```sh
apm marketplace add YOUR_ORG/agent-skills
apm install foundation@agent-skills
apm install rust@agent-skills
```

Commit the resulting consuming repository's `apm.yml`, `apm.lock.yaml`, and generated harness files. The lockfile pins the exact skill content used by every contributor.

For a direct Git dependency, use APM's monorepo subpath form:

```yaml
dependencies:
  apm:
    - YOUR_ORG/agent-skills/packages/foundation#v0.1.0
    - YOUR_ORG/agent-skills/packages/rust#v0.1.0
```

See [profile selection](docs/profiles.md) for intentionally small starting sets and [private overlays](docs/private-overlays.md) for company-only skills.

## Contributing

Author skills under `.apm/skills/<skill-name>/SKILL.md` inside one package. Keep a package focused on one capability and keep each skill's top-level instructions concise; move rare details into `references/` within that skill bundle.

Before opening a pull request, run:

```sh
bash scripts/validate.sh
```

The validation process checks marketplace metadata, validates lockstep versions, and scans every skill for hidden Unicode. It does not publish or install skills globally.

## Visibility model

This is a public repository. Do not commit internal architecture, customer data, secrets, private URLs, or company-only procedures here. Put those in a separate private overlay repository that may depend on this public marketplace, never the reverse.

The [private overlay template](templates/company-overlay/README.md) is safe to copy into a new private repository.
