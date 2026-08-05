# TypeScript verification

Use the package manager selected by the repository lockfile and its existing scripts. Do not substitute `npm`, `pnpm`, `yarn`, or `bun`, and do not install globally.

## Discover scripts

Read the nearest `package.json`, workspace configuration, and CI workflow. Typical checks are invoked through scripts rather than raw tools:

```sh
<pm> run format:check
<pm> run lint
<pm> run typecheck
<pm> run test -- <focused-filter>
<pm> run build
```

Argument-forwarding syntax differs across package managers and test runners; derive the exact focused-test form from repository scripts instead of assuming the placeholder is portable. In particular, `bun test` invokes Bun's test runner, while `bun run test` invokes a package script. Use the package manager's non-installing executor mode if a raw binary is required; avoid commands that fetch an undeclared latest package.

## Scope and escalation

- Start with the owning workspace/package and affected test file.
- Widen typechecking when shared types, path mappings, project references, package exports, or generated clients changed.
- Run build/bundle checks for module-format, conditional-export, tree-shaking, browser/Node boundary, or declaration-output changes.
- Use type-level tests (`tsd`, `expect-type`, compile fixtures, or repository equivalent) for public generics and inference behavior.
- Run tests in every supported runtime when code depends on DOM, Node, edge, worker, or test-environment globals.
- Inspect lockfile changes and lifecycle scripts after dependency updates; do not regenerate the lockfile with a different package manager.

A passing typecheck does not prove runtime input safety. Include malformed and missing boundary data in tests when validation changed.
