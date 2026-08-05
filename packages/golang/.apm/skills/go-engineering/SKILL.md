---
name: go-engineering
description: Use when implementing, reviewing, or debugging Go code involving package design, interfaces, concurrency, error handling, modules, or production services.
---

# Go engineering

Begin with `go.mod`, the supported Go version, repository instructions, package boundaries, generated-code markers, and nearby tests. Trace callers before changing an exported identifier or interface.

## Implementation principles

- Keep packages cohesive and dependency direction simple. Avoid `util`, import cycles, and abstractions without a concrete second use.
- Accept interfaces where behavior varies; return concrete types unless callers genuinely need substitution. Keep interfaces small and owned by consumers.
- Wrap errors with operation context using `%w`; preserve sentinel and typed-error behavior relied on by `errors.Is` or `errors.As`. Do not log and return the same error at every layer.
- Pass `context.Context` explicitly as the first parameter for request-scoped cancellation and deadlines. Never store it in a struct or replace it with `context.Background()` inside a live request path.
- Give every goroutine an owner, shutdown path, and bounded resource policy. Avoid unbounded fan-out, leaked tickers, blocked sends, and channel closure by receivers.
- Protect shared state deliberately with ownership, channels, atomics, or mutexes. Keep critical sections small and document lock ordering when multiple locks exist.
- Preserve zero values when practical; use constructors when validation, resource acquisition, or mandatory dependencies make a zero value invalid.
- Treat JSON, SQL, HTTP, environment, and filesystem data as untrusted boundaries. Validate before converting to domain types and bound request/body sizes.

## Change workflow

1. Locate the affected package, exported contract, generated files, build tags, and platform-specific variants.
2. Define cancellation, ownership, error, and concurrency behavior before implementation.
3. Add table-driven tests for meaningful cases and a regression test for bugs. Prefer observable behavior over testing private call sequences.
4. Run formatting, focused tests, vet/static analysis, and the race detector when concurrency changed.
5. Inspect module and generated-file diffs; do not run `go mod tidy` or regenerate broad outputs unless the change requires it.

Load `references/verification.md` for focused commands, race/benchmark guidance, module checks, and workspace escalation.
