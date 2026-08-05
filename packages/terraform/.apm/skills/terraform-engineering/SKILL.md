---
name: terraform-engineering
description: Use when implementing, reviewing, testing, importing, refactoring, or troubleshooting Terraform modules, providers, plans, state, and infrastructure changes.
---

# Terraform engineering

Read the required Terraform/OpenTofu version, provider constraints and lockfile, backend, workspace/environment model, module sources, CI policy, and repository commands before editing. Inspect current configuration and state addresses; never infer production resources from names alone.

## Configuration principles

- Keep modules cohesive with typed, documented inputs and outputs. Add validation and pre/postconditions for enforceable contracts; avoid pass-through wrappers with no durable abstraction.
- Pin providers and external modules according to repository policy. Review lockfile and transitive module changes; never replace a trusted source casually.
- Use stable `for_each` keys derived from durable identity. Avoid count/index churn and keys containing values unknown until apply.
- Prefer references over manual `depends_on`; add explicit dependencies only for real behavioral relationships Terraform cannot infer.
- Model renames with `moved` blocks and existing resources with reviewed `import` blocks or documented import commands. Do not destroy/recreate merely to align state addresses.
- Assume state contains secrets even when outputs are marked sensitive. Use encrypted, access-controlled remote state with locking and recovery appropriate to the backend.
- Do not hardcode credentials or secrets in configuration, committed tfvars, command history, logs, or outputs. Recognize that state and saved plans can necessarily contain sensitive or unmarked secret values; encrypt them, restrict access, keep them short-lived, and exclude them from version control and shared logs.
- Use lifecycle rules sparingly. `ignore_changes` can conceal drift; `prevent_destroy` is a guardrail, not a recovery strategy; replacement ordering must fit quota and uniqueness constraints.

## Change workflow

1. Identify the exact root module, backend/workspace, account/project/subscription, region, and state addresses.
2. Read provider documentation for the pinned version and inspect existing plans/state without exposing sensitive values.
3. Make the smallest configuration change and add module tests/checks where the repository supports them.
4. Run formatting, initialization in the appropriate mode, validation, lint/policy/security checks, and a saved plan using documented variable sources.
5. Review every create/update/replace/destroy, unknown value, provider change, output, and state move. Treat unexpected change as a blocker.
6. Apply only with explicit authorization, the reviewed saved plan, correct target identity, locking, and rollback/recovery preparation. Verify real infrastructure afterward.

Load `references/state-plan-and-verification.md` for safe commands, state surgery, imports, plans, testing, and apply controls.
