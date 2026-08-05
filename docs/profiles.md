# Profile selection

Profiles are curated sets of packages, not a second runtime. A consuming repository selects a profile by declaring the packages it needs in its own `apm.yml`; APM then locks the resolved content for all contributors.

Use the smallest profile that covers the repository and task. Add a task package when the work warrants it, then remove it if it is no longer a durable repository need.

| Profile | Packages | Use when |
| --- | --- | --- |
| Rust minimal | `foundation`, `rust` | Day-to-day work in a Rust repository |
| Rust implementation | `foundation`, `rust`, `testing` | Implementing or materially changing behaviour in a Rust service |
| Rust review | `foundation`, `rust`, `code-review` | Reviewing a Rust change or running review automation |
| Go service | `foundation`, `golang`, `testing` | Implementing or changing a Go service |
| TypeScript application | `foundation`, `typescript`, `testing` | Implementing a TypeScript application or package |
| Python service | `foundation`, `python`, `testing` | Implementing a Python service, library, or CLI |
| SQLite application | `foundation`, one language package, `sqlite`, `testing` | Building an embedded or single-node application backed by SQLite |
| PostgreSQL service | `foundation`, one language package, `postgresql`, `testing` | Building a service backed by PostgreSQL |
| Containerized service | `foundation`, one language package, `docker`, `testing` | Building and verifying a containerized service |
| AWS Terraform | `foundation`, `terraform`, `aws`, `code-review` | Reviewing or changing AWS infrastructure managed by Terraform |
| Generic review | `foundation`, `code-review` | Reviewing a non-Rust repository without stack-specific skills |

## Consumer manifest example

After publishing the marketplace, a Rust implementation repository can declare this focused set:

```yaml
name: payments-service
version: 0.1.0
dependencies:
  apm:
    - brianluby/agent-skills/packages/foundation#v0.1.0
    - brianluby/agent-skills/packages/rust#v0.1.0
    - brianluby/agent-skills/packages/testing#v0.1.0
```

Run `apm install` from the consuming repository and commit the lockfile it creates.

## Why profiles are metadata for now

APM supports transitive package dependencies, but a composite package needs the final public repository source address. This repository intentionally avoids guessing that address before it is published. Once it has a stable owner and release tags, profile packages can be added as normal APM packages that compose the same dependencies shown above.

Until then, this catalogue remains explicit, portable, and reviewable: consumers can see exactly which skills they install.
