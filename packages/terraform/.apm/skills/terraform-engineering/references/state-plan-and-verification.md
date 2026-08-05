# Terraform state, plan, and verification

Terraform commands can contact providers, refresh state, reveal sensitive data, or mutate infrastructure. Confirm the root module, backend, workspace, credentials, and authorization before running them.

## Static and module checks

```sh
terraform fmt -check -recursive
terraform init -backend=false
terraform validate
```

Use a disposable directory or documented test harness when `init -backend=false` would alter a working directory. Run configured `tflint`, policy, security, and docs checks with pinned versions.

`terraform test` is not inherently static: test files can use apply-mode runs that create, modify, and destroy real, billable infrastructure. Inspect every test file and run mode first; prefer `command = plan` when non-mutating verification is sufficient. Require explicit authorization, isolated test credentials/account or project, bounded cost and quotas, and verified cleanup before running apply-mode tests. Treat plan-mode tests as provider-connected plans with the same identity and data-handling precautions described below.

## Plan discipline

```sh
terraform init
terraform workspace show
terraform plan -out=tfplan
terraform show tfplan
```

A normal plan refreshes remote objects and needs read permissions. Store plans as sensitive, short-lived artifacts: they can contain credentials/secrets and are only valid for the exact configuration, state, providers, variables, and target environment. Avoid `-target` except bounded recovery because it can produce incomplete convergence.

Review plan output locally or in an access-controlled CI view; do not paste it into tickets or public logs without redaction. Never use `terraform show -json` on state or plans in an unprotected log path because sensitive values can be emitted in plaintext.

## State and refactoring

Back up and lock state before manual operations. Prefer declarative `moved`, `removed`, and `import` blocks where supported. Before `state mv/rm`, import, force-unlock, backend migration, or workspace deletion:

1. Resolve the exact resource addresses and provider aliases.
2. Confirm no concurrent run exists; never force-unlock an active operation.
3. Capture a protected state backup and backend recovery procedure.
4. Dry-run/list where supported, execute the minimum operation, then plan immediately.
5. Verify no unintended create/destroy. Keep historical `moved` blocks indefinitely in shared/versioned modules. Remove them only as an intentional breaking change, or in a controlled private module after proving every consumer has applied the migration; remove other migration declarations only under an explicit compatibility policy.

Never hand-edit state JSON. Do not use `terraform refresh` as generic drift repair; diagnose configuration, provider, import, or lifecycle mismatch and produce a reviewed plan.

## Apply and recovery

Apply the reviewed saved plan—not a newly generated implicit plan—only when authorized. Monitor provider/API errors and partial completion; do not blindly retry. Afterward, verify outputs without printing secrets, check service health and policy, and run a clean follow-up plan. Roll forward or use provider-specific recovery when rollback would itself destroy data.
