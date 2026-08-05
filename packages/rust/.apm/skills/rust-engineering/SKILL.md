---
name: rust-engineering
description: Use when implementing, reviewing, or debugging Rust code that requires idiomatic ownership, error handling, asynchronous behavior, or Cargo-based verification.
---

# Rust engineering

Start by locating the workspace root, affected crate, edition/MSRV, enabled features, public API, and nearby tests. Read `Cargo.toml`, workspace lint policy, and repository instructions before changing dependencies or feature resolution.

## Implementation principles

- Model invariants with enums, newtypes, and validated constructors instead of comments or sentinel values.
- Borrow at API boundaries when the caller retains ownership; own data when it must outlive the call. Do not clone merely to satisfy the borrow checker—first reconsider scopes and data flow.
- Return domain-relevant `Result` errors with context. Reserve `panic!`, `unwrap`, and indexing for proven invariants, tests, or process-fatal startup conditions with a clear explanation.
- Keep public traits and generics no broader than required. Prefer concrete internal types until multiple real implementations justify abstraction.
- Preserve cancellation, backpressure, and error propagation in async code. Never hold a synchronous lock across `.await`, and isolate blocking work from the async executor.
- Treat `unsafe` as an audited boundary: state its safety invariant, keep the block minimal, and add tests or Miri coverage that exercise the invariant.
- Avoid broad dependency or feature changes when the standard library or an existing crate is sufficient. Check duplicate versions and feature unification before adding a crate.

## Change workflow

1. Trace the affected symbol through callers, trait implementations, feature gates, and serialization or FFI boundaries.
2. Make ownership, thread-safety, and error contracts explicit before implementation.
3. Add focused tests for success, expected failure, and the reported regression. Use integration tests for public behavior and unit tests for private invariants.
4. Run the narrowest relevant formatter, check, lint, and test commands first; widen to the workspace when shared crates, features, proc macros, build scripts, or public APIs changed.
5. Inspect the final diff for accidental lockfile churn, new default features, hidden panics, and unnecessary allocations.

Load `references/verification.md` for command selection, feature-matrix checks, unsafe/async validation, and workspace escalation guidance.
