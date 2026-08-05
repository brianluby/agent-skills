---
name: python-engineering
description: Use when implementing, reviewing, or debugging Python applications, libraries, CLIs, data services, or async code with typing, packaging, and environment concerns.
---

# Python engineering

Discover the supported Python versions, `pyproject.toml`, lockfile, environment manager, source layout, type-checker settings, and repository commands before importing a library or changing packaging metadata.

## Implementation principles

- Make boundaries explicit with typed domain objects, validation, and narrow protocols. Do not use `Any` to silence uncertainty that should be resolved.
- Raise or return domain-relevant errors with causal chaining (`raise ... from ...`). Catch exceptions at the layer that can recover, translate, or add meaningful context—not around arbitrary blocks.
- Avoid mutable default arguments and hidden module-global state. Make clocks, randomness, clients, and side effects injectable where deterministic testing matters.
- Use context managers for files, locks, transactions, temporary resources, and clients. Define resource ownership so callers know who closes what.
- Keep async paths non-blocking, cancellation-safe, and bounded. Move CPU/blocking work through the framework's supported mechanism; do not swallow `CancelledError`.
- Preserve import and packaging boundaries. Avoid runtime imports used only for typing, import-time network/filesystem side effects, and accidental changes to public exports.
- Validate untrusted JSON, environment, paths, subprocess arguments, SQL parameters, and serialized data. Never use `eval`, unsafe deserialization, or `shell=True` with interpolated input.
- Prefer clear iteration and standard-library constructs over clever metaprogramming. Optimize only after measuring representative workloads.

## Change workflow

1. Trace the symbol through imports, protocols/ABCs, framework registration, serialization, tests, and CLI/API entry points.
2. Define error, resource-lifetime, sync/async, and typing contracts.
3. Add focused tests for success, failure, and regression behavior; use property-based tests for parsers or broad invariants when already supported.
4. Run formatter/linter, type checker, and focused tests using the locked project environment.
5. Widen across supported Python versions or packages when public APIs, shared models, packaging, or integrations changed.

Load `references/verification.md` for environment-safe commands, test isolation, typing, packaging, and compatibility checks.
