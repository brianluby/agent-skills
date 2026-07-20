# Rust verification

Choose checks that match the change and repository conventions:

1. Format the changed crate or workspace with the repository's required `cargo fmt` invocation.
2. Run focused tests for the affected package, module, or feature.
3. Run `cargo clippy` when lint policy or public API behavior changed.
4. Use workspace-wide tests only when a shared crate, feature resolution, integration surface, or release artifact changed.

If a command cannot run, record why and do not claim it passed.
