---
name: code-review
description: Use when reviewing a pull request, patch, or proposed implementation for correctness, security, regressions, and missing verification.
---

# Code review

Review the change in context: read the surrounding implementation, affected callers, tests, and repository rules before drawing conclusions.

Prioritize findings that are actionable and supported by a concrete execution path:

1. Incorrect behavior, data loss, or security exposure
2. Regressions at API, concurrency, error-handling, or compatibility boundaries
3. Missing tests for a changed contract or credible edge case
4. Maintainability concerns that materially raise future change risk

For each finding, identify the location, triggering conditions, consequence, and a concise remediation direction. Do not report style preferences as defects when existing tooling or project convention already governs them.
