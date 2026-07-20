---
name: repository-workflow
description: Use when beginning work in an unfamiliar repository or making a scoped change that needs safe inspection, minimal edits, and proportionate verification.
---

# Repository workflow

1. Read the repository instructions and inspect the relevant code before proposing an edit.
2. Check the working tree and preserve unrelated user changes.
3. Make the smallest change that satisfies the request. Do not refactor adjacent code without a stated reason.
4. Run the narrowest relevant formatter, test, or static check. Expand verification when the change affects a boundary, security property, or release path.
5. Report the changed files, verification performed, and any meaningful remaining risk.

Treat generated files as build output unless the repository documents otherwise. Never add secrets, credentials, or private service details to source control.
