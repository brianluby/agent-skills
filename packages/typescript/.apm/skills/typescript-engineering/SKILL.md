---
name: typescript-engineering
description: Use when implementing, reviewing, or debugging TypeScript across Node.js, browser, library, or monorepo codebases with type-safety and runtime-boundary concerns.
---

# TypeScript engineering

Identify the package manager and lockfile, workspace boundaries, `tsconfig` inheritance, module format, runtime target, framework conventions, and repository scripts before editing. Do not assume TypeScript types validate runtime data.

## Implementation principles

- Keep strictness intact. Prefer `unknown` plus narrowing over `any`, and model state with discriminated unions rather than combinations of optional booleans.
- Validate data at network, storage, environment, message, and deserialization boundaries. Infer static types from the runtime schema when the project already uses a schema library.
- Preserve ESM/CJS and package `exports` behavior. Include file extensions or type-only imports according to the repository's compiler and runtime rules—not generic advice.
- Make nullability and ownership explicit. Avoid non-null assertions unless an invariant is locally proven; avoid mutating inputs unless the API contract says so.
- Propagate async failures and cancellation. Await or intentionally detach every promise, attach rejection handling to detached work, and use `AbortSignal` where the surrounding API supports it.
- Keep public types intentional. Avoid leaking framework internals, inferred implementation details, or broad index signatures across package boundaries.
- Use exhaustive checks for closed unions and preserve error causes when translating failures. Do not catch errors merely to discard type or stack information.
- Treat DOM sinks, shell commands, SQL, paths, URLs, and template rendering as security boundaries; use the platform's safe APIs and project sanitization conventions.

## Change workflow

1. Trace the symbol through imports, project references, generated clients/types, tests, and package exports.
2. Separate compile-time guarantees from required runtime validation.
3. Add focused tests for behavior and type tests for public generic or inference contracts when the repository supports them.
4. Run the package's formatter/linter, typecheck, and focused tests through existing scripts.
5. Review lockfile, generated output, declaration files, and bundle/runtime compatibility before widening verification.

Load `references/verification.md` for package-manager-safe commands, type testing, build checks, and monorepo escalation.
