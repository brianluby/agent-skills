---
name: rust-engineering
description: Use when implementing, reviewing, or debugging Rust code that requires idiomatic ownership, error handling, asynchronous behavior, or Cargo-based verification.
---

# Rust engineering

Start by locating the affected crate, feature flags, and existing tests. Follow local conventions before introducing an abstraction.

- Prefer ownership and borrowing that make lifetimes obvious at the API boundary.
- Return domain-relevant errors with context; do not replace recoverable failures with panics.
- Preserve cancellation and error propagation in asynchronous code.
- Avoid broad dependency changes when a standard-library or existing-crate solution is sufficient.

Verify at the narrowest useful scope first, typically with the affected crate's tests. When feasible for the repository, also run formatting and linting through its documented Cargo commands.

Load `references/verification.md` when choosing a verification sequence or when a workspace-wide check is warranted.
