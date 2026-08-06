# Technology skill summary

This document records the skills created or substantially expanded for the initial Rust, Go, TypeScript, Python, SQLite, PostgreSQL, Docker, Terraform, and AWS coverage. Release `0.2.0` adds focused security, CodeQL, AI-security, and product-management workflow packages.

## Provenance

Eight skills were authored as new packages in this repository. The existing Rust package was substantially expanded. No skill was copied from the older, unmaintained agents repository, and none depends on skills installed only in a local agent profile. Each package is independently installable and bundles its own deeper reference material.

All packages use the repository's MIT license and lockstep release version.

## Workflow additions in 0.2.0

| Package | Primitive | Purpose |
|---|---|---|
| `security-review` | `security-review` skill and `security-reviewer` agent | Validate exploitable application-security defects and report evidence-based findings |
| `ai-security` | `ai-security-review` skill | Review prompt injection, unsafe agency, sensitive-data flow, output handling, and resource bounds |
| `codeql` | `codeql` skill | Configure and troubleshoot CodeQL workflows, build modes, query scope, and SARIF upload |
| `product-management` | `product-management` skill | Frame customer problems, compare options, and define measurable delivery scope |

These primitives were rewritten for this marketplace rather than copied from repository-local or third-party bundles. The security-reviewer agent deliberately inherits repository instructions so project-specific policies stay with the consuming repository.

### Context counting method

Context is counted over the exact UTF-8 Markdown text bundled with each skill. **Primary context** is `SKILL.md`; **reference context** is every Markdown file under that skill's `references/` directory; **full bundled context** is both joined with one newline. Package manifests and this summary are excluded. Token counts use `tiktoken`'s `o200k_base` encoding and are reproducible reference counts, not a guarantee for every model or provider tokenizer. Word and character counts are exact for the current files. References are normally loaded only when needed, so primary context is the usual initial footprint and full bundled context is the maximum documented footprint for this collection.

## Summary

| Package | Skill | Status | Primary coverage | Context tokens: primary + references = full |
|---|---|---|---|---:|
| `rust` | `rust-engineering` | Existing skill substantially expanded | Ownership, errors, async behavior, unsafe code, Cargo workflows | 465 + 414 = **879** |
| `golang` | `go-engineering` | Created | Packages, interfaces, errors, context, concurrency, modules | 463 + 302 = **765** |
| `typescript` | `typescript-engineering` | Created | Type safety, runtime boundaries, async behavior, modules, monorepos | 466 + 362 = **828** |
| `python` | `python-engineering` | Created | Typing, packaging, resources, async behavior, environments | 472 + 352 = **824** |
| `sqlite` | `sqlite-engineering` | Created | Schema, queries, migrations, concurrency, backup and recovery | 483 + 436 = **919** |
| `postgresql` | `postgresql-engineering` | Created | Schema, queries, indexing, migration, performance and operations | 484 + 456 = **940** |
| `docker` | `docker-engineering` | Created | Dockerfiles, images, BuildKit, Compose, runtime and supply chain | 506 + 377 = **883** |
| `terraform` | `terraform-engineering` | Created | Modules, plans, state, imports, refactoring and applies | 541 + 619 = **1,160** |
| `aws` | `aws-engineering` | Created | Architecture, IAM, networking, service operations and recovery | 600 + 470 = **1,070** |

**Combined footprint:** 4,480 primary tokens + 3,788 reference tokens = **8,268 full bundled tokens**, comprising 5,681 words and 43,299 characters across the nine skills.

## Rust engineering

- **Package:** `rust`
- **Skill:** `rust-engineering`
- **Path:** `packages/rust/.apm/skills/rust-engineering/SKILL.md`
- **Context footprint:** 465 primary tokens + 414 reference tokens = **879 full tokens**; 603 words and 4,458 characters in the full bundle.
- **Status:** Existing minimal package substantially expanded for this collection.
- **Trigger:** Implementing, reviewing, or debugging Rust involving ownership, error handling, asynchronous behavior, or Cargo verification.
- **Purpose:** Guide agents toward idiomatic, contract-preserving Rust changes after inspecting workspace structure, feature flags, MSRV, unsafe code, and repository policy.
- **Core coverage:**
  - Ownership and borrowing without reflexive cloning.
  - Explicit error context and intentional public error types.
  - Async cancellation, blocking work, task lifetime, and backpressure.
  - Unsafe-code invariants and safe-boundary testing.
  - Feature-gated APIs, workspaces, public compatibility, and dependency policy.
- **Bundled reference:** `references/verification.md` covers focused and workspace Cargo checks, feature matrices, tracked lockfiles and `--locked`, Clippy policy, doctests, Miri, loom, fuzzing, audits, and performance checks.
- **Safety emphasis:** Do not weaken unsafe invariants, silently change error semantics, update lockfiles out of scope, or impose a stricter lint policy than the repository uses.
- **Related packages:** Docker for containerized Rust services, SQLite/PostgreSQL for persistence, and AWS/Terraform for deployment.

## Go engineering

- **Package:** `golang`
- **Skill:** `go-engineering`
- **Path:** `packages/golang/.apm/skills/go-engineering/SKILL.md`
- **Context footprint:** 463 primary tokens + 302 reference tokens = **765 full tokens**; 523 words and 3,833 characters in the full bundle.
- **Status:** Created in this repository.
- **Trigger:** Go package design, interfaces, concurrency, errors, context, modules, or production services.
- **Purpose:** Preserve package contracts and concurrency invariants while producing simple, idiomatic Go.
- **Core coverage:**
  - Small consumer-owned interfaces and explicit concrete types.
  - Error wrapping, inspection with `errors.Is`/`errors.As`, and stable caller-visible behavior.
  - Context propagation without storing contexts in long-lived structs.
  - Goroutine ownership, cancellation, channel closure, bounded concurrency, and synchronization.
  - Zero values, copy hazards, allocation awareness, and module boundaries.
- **Bundled reference:** `references/verification.md` covers formatting, focused and full tests, race detection, vet/static analysis, build tags, integration tests, fuzzing, benchmarks, and cross-compilation.
- **Safety emphasis:** Every goroutine needs an owner and exit path; avoid accidental API breakage and broad module/workspace changes.
- **Related packages:** Docker, SQLite/PostgreSQL, AWS, and Terraform.

## TypeScript engineering

- **Package:** `typescript`
- **Skill:** `typescript-engineering`
- **Path:** `packages/typescript/.apm/skills/typescript-engineering/SKILL.md`
- **Context footprint:** 466 primary tokens + 362 reference tokens = **828 full tokens**; 569 words and 4,292 characters in the full bundle.
- **Status:** Created in this repository.
- **Trigger:** TypeScript for Node.js, browser, library, or monorepo code with type-safety or runtime-boundary concerns.
- **Purpose:** Keep compile-time types aligned with runtime behavior across package and module boundaries.
- **Core coverage:**
  - `unknown` plus validation at untrusted boundaries instead of unchecked assertions.
  - Discriminated unions, exhaustive handling, and narrow interfaces.
  - Optional versus absent values under repository compiler settings.
  - Promise ownership, cancellation, error propagation, ESM/CJS behavior, and public declarations.
  - Workspace package boundaries and generated-source ownership.
- **Bundled reference:** `references/verification.md` covers lockfile-selected package managers, repository scripts, focused test argument forwarding, linting, type checking, builds, declarations, browser/Node boundaries, and package export checks.
- **Safety emphasis:** Avoid fetching undeclared latest tooling, bypassing configured test scripts, unsafe casts, and type-only fixes that leave runtime behavior invalid.
- **Related packages:** Docker, SQLite/PostgreSQL, AWS, and Terraform.

## Python engineering

- **Package:** `python`
- **Skill:** `python-engineering`
- **Path:** `packages/python/.apm/skills/python-engineering/SKILL.md`
- **Context footprint:** 472 primary tokens + 352 reference tokens = **824 full tokens**; 565 words and 4,343 characters in the full bundle.
- **Status:** Created in this repository.
- **Trigger:** Python applications, libraries, CLIs, data services, packaging, typing, or async code.
- **Purpose:** Make clear, typed, environment-compatible changes while preserving Python's runtime contracts and resource lifecycles.
- **Core coverage:**
  - Type annotations that narrow contracts without replacing runtime validation.
  - Explicit resource ownership using context managers and structured cleanup.
  - Exception specificity, chaining, and stable public semantics.
  - Async cancellation, blocking-work isolation, task ownership, and backpressure.
  - Import layout, packaging metadata, supported Python versions, and dependency policy.
- **Bundled reference:** `references/verification.md` covers environment-manager discovery, focused tests, formatting/lint/type checks, version matrices, async tests, building wheel/sdist artifacts, clean-environment wheel installation, public-import checks, and CLI smoke tests.
- **Safety emphasis:** Do not mutate the wrong environment, swallow cancellation, hide partial initialization, or consider an uninstalled source-tree test sufficient for packaging changes.
- **Related packages:** Docker, SQLite/PostgreSQL, AWS, and Terraform.

## SQLite engineering

- **Package:** `sqlite`
- **Skill:** `sqlite-engineering`
- **Path:** `packages/sqlite/.apm/skills/sqlite-engineering/SKILL.md`
- **Context footprint:** 483 primary tokens + 436 reference tokens = **919 full tokens**; 629 words and 4,922 characters in the full bundle.
- **Status:** Created in this repository.
- **Trigger:** SQLite schema design, queries, transactions, migrations, indexes, concurrency, or embedded-database operations.
- **Purpose:** Account for SQLite's connection-scoped settings, file-level behavior, type affinity, and application-specific concurrency model.
- **Core coverage:**
  - Parameterized queries, explicit transaction ownership, foreign-key enforcement, and deterministic ordering.
  - Affinity-aware schema design and index selection from real query shapes.
  - Forward-compatible, restartable migrations and table-rebuild verification.
  - WAL, busy handling, checkpoint behavior, network-filesystem constraints, and connection pools.
- **Bundled reference:** `references/operations-and-verification.md` covers connection baselines, query plans, migration checks, integrity screening, online backups, WAL sidecars, and corruption evidence preservation.
- **Safety emphasis:** Full integrity checks may be expensive; corruption evidence requires quiesced writers or an atomic snapshot, with the main database and all sidecars preserved as one consistent set.
- **Related packages:** Python, TypeScript, Go, and Rust application packages; Docker when filesystem semantics remain suitable.

## PostgreSQL engineering

- **Package:** `postgresql`
- **Skill:** `postgresql-engineering`
- **Path:** `packages/postgresql/.apm/skills/postgresql-engineering/SKILL.md`
- **Context footprint:** 484 primary tokens + 456 reference tokens = **940 full tokens**; 625 words and 4,949 characters in the full bundle.
- **Status:** Created in this repository.
- **Trigger:** PostgreSQL schema, queries, transactions, migrations, indexes, extensions, tuning, or production behavior.
- **Purpose:** Produce correct database changes with explicit attention to plans, locks, workload shape, version behavior, and recovery.
- **Core coverage:**
  - Correct constraints and types before indexes and tuning.
  - Parameterized SQL, transaction isolation, lock ordering, retries, and connection-pool limits.
  - Query-plan analysis using representative cardinality and parameter distributions.
  - Backward-compatible expand/contract migrations and bounded backfills.
  - Index maintenance, autovacuum, replication, backup, and restore concerns.
- **Bundled reference:** `references/performance-and-operations.md` covers `EXPLAIN`, PostgreSQL-version-sensitive options, safer schema changes, operational health, PITR, replication, and change verification.
- **Safety emphasis:** `EXPLAIN ANALYZE` executes statements; concurrent index operations and constraints have transaction/lock requirements; backups are not proven until restored.
- **Related packages:** Python, TypeScript, Go, and Rust applications; Docker, AWS, and Terraform for operation and deployment.

## Docker engineering

- **Package:** `docker`
- **Skill:** `docker-engineering`
- **Path:** `packages/docker/.apm/skills/docker-engineering/SKILL.md`
- **Context footprint:** 506 primary tokens + 377 reference tokens = **883 full tokens**; 617 words and 4,714 characters in the full bundle.
- **Status:** Created in this repository.
- **Trigger:** Dockerfiles, images, build contexts, Compose services, runtime behavior, security, or optimization.
- **Purpose:** Build reproducible, minimal images with explicit process, filesystem, networking, and secret-handling behavior.
- **Core coverage:**
  - Multi-stage builds, cache ordering, `.dockerignore`, pinned inputs, and target-platform awareness.
  - BuildKit secret/SSH mounts instead of secret-bearing build arguments or layers.
  - Non-root execution, least privilege, writable-path planning, init/signal handling, and graceful shutdown.
  - Compose interpolation, mounts, health checks, dependencies, and local-development scope.
- **Bundled reference:** `references/verification-and-security.md` covers builds, image inspection, runtime checks, Compose validation, multi-platform testing, vulnerability/SBOM/provenance tooling, and supply-chain review.
- **Safety emphasis:** Treat image history as sensitive, keep credentials out of build contexts and layers, and run Compose only with reviewed inputs in an isolated non-production project.
- **Related packages:** All application-language packages, AWS container services, and Terraform-managed infrastructure.

## Terraform engineering

- **Package:** `terraform`
- **Skill:** `terraform-engineering`
- **Path:** `packages/terraform/.apm/skills/terraform-engineering/SKILL.md`
- **Context footprint:** 541 primary tokens + 619 reference tokens = **1,160 full tokens**; 836 words and 6,240 characters in the full bundle.
- **Status:** Created in this repository.
- **Trigger:** Terraform modules, providers, plans, state, imports, refactoring, tests, or infrastructure changes.
- **Purpose:** Keep configuration, state, provider identity, and real infrastructure aligned without unsafe state surgery or unreviewed mutation.
- **Core coverage:**
  - Cohesive typed modules, stable `for_each` keys, inferred dependencies, and lifecycle restraint.
  - Provider/module pinning and lockfile review.
  - Declarative `moved`, `removed`, and `import` blocks.
  - Identity/workspace/backend verification, saved-plan review, authorized applies, and post-apply checks.
- **Bundled reference:** `references/state-plan-and-verification.md` covers static checks, the mutating potential of `terraform test`, plan sensitivity, state operations, historical moved blocks, apply controls, and recovery.
- **Safety emphasis:** Saved plans and state may contain plaintext sensitive values; `terraform show -json` requires protected handling; apply-mode tests can create billable infrastructure; shared module `moved` blocks should remain for compatibility.
- **Related packages:** AWS for provider-specific architecture and Docker for container infrastructure.

## AWS engineering

- **Package:** `aws`
- **Skill:** `aws-engineering`
- **Path:** `packages/aws/.apm/skills/aws-engineering/SKILL.md`
- **Context footprint:** 600 primary tokens + 470 reference tokens = **1,070 full tokens**; 714 words and 5,548 characters in the full bundle.
- **Status:** Created in this repository.
- **Trigger:** AWS architecture, IAM, networking, compute, storage, databases, observability, automation, or service operations.
- **Purpose:** Design and operate AWS systems from verified account/region identity with least privilege, explicit resilience, and recoverability.
- **Core coverage:**
  - Account, partition, region, organization, data-classification, RTO/RPO, and cost context.
  - Temporary role credentials, least privilege, IAM condition keys, KMS/key-policy analysis, and public-access controls.
  - Multi-AZ/Regional design, quota and retry behavior, idempotency, observability, tagging, and cost ownership.
  - Managed-service, networking, data-store, deployment, and rollback trade-offs.
- **Bundled reference:** `references/iam-operations-and-verification.md` covers identity discovery, IAM policy reasoning, pagination, dry-run limitations, mutation controls, CloudTrail/Config verification, backups, and recovery testing.
- **Safety emphasis:** Never request or persist access keys; verify account and region before mutation; prefer IaC for durable changes; destructive operations require explicit authorization and recovery preparation.
- **Related packages:** Terraform for infrastructure as code, Docker for container workloads, PostgreSQL/SQLite for persistence decisions, and all application-language packages.

## Validation status

The collection was reviewed independently across language, database, container, Terraform, and AWS domains. Review findings were corrected before this summary was finalized.

The repository validation covers:

- Marketplace entry reachability and lockstep package-version alignment.
- Claude and Codex marketplace generation.
- Frontmatter and bundled reference existence.
- Shell validation of the repository validator.
- Hidden-Unicode auditing of every bundled Markdown instruction and reference file.
- Whitespace/error checks with `git diff --check`.

No package in this collection requires the stale agents repository or a skill installed only in the author's local profile.
