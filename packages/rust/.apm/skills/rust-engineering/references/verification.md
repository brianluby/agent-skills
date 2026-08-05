# Rust verification

Use repository-provided task runners when present. Otherwise choose from this sequence and preserve the project's toolchain and feature policy.

## Focused loop

```sh
cargo fmt --all -- --check
cargo check -p <package>
cargo test -p <package> <test-filter>
cargo clippy -p <package> --all-targets
```

Do not add `--all-features` blindly: mutually exclusive or production-only features may make it invalid. Derive meaningful combinations from CI, `Cargo.toml`, and `cfg` usage.

When the repository commits `Cargo.lock`, use `--locked` (or the repository's equivalent CI command) for verification that must not change dependency resolution. Libraries that intentionally do not commit a lockfile need a different policy.

## Escalate when boundaries changed

```sh
cargo check --workspace --all-targets
cargo test --workspace
cargo clippy --workspace --all-targets
cargo test --doc --workspace
```

Use the repository's documented Clippy flags and lint policy. Add `-- -D warnings` only when CI or workspace policy already requires warnings to be denied; do not turn unrelated existing warnings into a new failure policy.

Run additional checks when relevant:

- Feature changes: test default, no-default, and supported feature combinations.
- Unsafe code: run the repository's Miri, sanitizer, fuzz, or loom jobs where available.
- Async/concurrency: add timeout and cancellation tests; use loom for synchronization primitives when the project already supports it.
- Public libraries: run doctests and semver/API checks configured by the repository.
- Dependencies: inspect `Cargo.lock`, `cargo tree -d`, advisories, licenses, and newly enabled transitive features.
- Performance-sensitive paths: benchmark representative workloads; do not infer improvement from code shape alone.

Never run `cargo fix`, update the lockfile, or rewrite the full workspace without confirming that scope is intended. If a command cannot run, record why and do not claim it passed.
