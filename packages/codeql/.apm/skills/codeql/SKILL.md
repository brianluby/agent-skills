---
name: codeql
description: Use when configuring, reviewing, or troubleshooting GitHub CodeQL code scanning, advanced-setup workflows, language and build-mode selection, query suites, monorepo scope, SARIF upload, or CodeQL CLI analysis.
---

# CodeQL

Inspect the repository languages, build system, existing security workflow, GitHub permissions, and current CodeQL configuration before proposing changes. Preserve the repository-pinned action major unless an upgrade is part of the task; verify current GitHub documentation before introducing a new major or relying on a language-specific capability.

## Configure GitHub Actions

1. Decide whether default setup is sufficient. Use advanced setup only when the repository needs custom triggers, matrices, build steps, query suites, categories, or path configuration.
2. Select CodeQL language identifiers from the files actually built. Avoid scanning generated, vendored, or example trees unless they are in scope.
3. Choose a build mode per language.
   - Prefer `none` when GitHub documents it for the language and repository layout.
   - Use `autobuild` when CodeQL can discover the real build.
   - Use `manual` when generated code, custom tooling, or repository structure requires an explicit build between initialization and analysis.
   - For Rust `none` builds, confirm the repository exposes Cargo metadata and the runner has the required Rust tooling; build scripts and macros still need analysis support.
4. Grant least privilege: normally `contents: read`, `security-events: write`, and only the additional read permissions required by the event and repository visibility.
5. Use stable analysis categories when separate matrix entries or components upload results.
6. Keep pull-request scanning for changed-code feedback and schedule a default-branch scan when delayed dependency or query updates matter.

## Diagnose failures

- Verify the action and CLI versions before interpreting an error.
- Inspect initialization, extraction/build, finalize, and SARIF upload as separate phases.
- Confirm runner OS and architecture support, toolchain availability, checkout depth, submodules, generated sources, and memory/disk limits.
- Check whether path filters prevented the workflow from running; workflow trigger filters do not restrict which source CodeQL analyzes.
- For missing results, confirm query suite, source scope, extraction logs, analysis category, upload permissions, and whether another configuration overwrote the category.
- For monorepos, test one language/component first, then expand the matrix without changing category identity.

## CodeQL CLI

Use a compatible CodeQL bundle, create a database from the intended source root and build, analyze it with an explicit query suite, and write SARIF to a protected temporary location. Treat SARIF as potentially sensitive source-derived data. Upload only to the intended repository, commit, ref, and category.

Report the configuration changed, why the build mode is appropriate, what was validated, and any coverage gaps. Do not claim that a green CodeQL run proves the absence of vulnerabilities.
