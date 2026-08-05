# AWS IAM, operations, and verification

Use the repository's approved SSO/profile/role workflow. Never request, print, paste, or persist access keys or session tokens.

## Establish context

Read-only examples—adapt partition and region:

```sh
aws sts get-caller-identity --profile <profile>
aws configure get region --profile <profile>
aws configure list --profile <profile>
```

Record the account and region in the change evidence. Be alert to commands whose resource is global, region-specific, or replicated. Use explicit profiles/regions in automation rather than ambient defaults.

## IAM review

Evaluate identity policy, resource policy, trust policy, permission boundary, SCP/RCP where applicable, session policy, VPC endpoint policy, and KMS key policy as one authorization path. Scope actions, resources, principals, and conditions; treat `iam:PassRole`, role trust, policy attachment, KMS grants, and wildcard principals as high risk. Use policy simulation/access analysis as supporting evidence, then test the intended principal and denied paths safely.

## Automation behavior

- Use SDK/CLI paginators; a single response is rarely proof of absence.
- Respect throttling with bounded exponential backoff and jitter. Retry only idempotent operations or use service idempotency tokens.
- Wait on service state with bounded waiters and surface timeout diagnostics.
- Avoid parsing human table/text output; request JSON and query stable fields.
- Redact secrets, presigned URLs, authorization headers, user data, policy-sensitive identifiers, and customer data from logs/artifacts.
- Dry-run where the service genuinely supports it, but do not assume dry-run validates all permissions or semantics.

## Mutations and destructive actions

Before deleting, replacing, rotating, revoking, failing over, or changing network/IAM/KMS policy, confirm dependencies, deletion protection, backups, replication, retention, active sessions, IaC ownership, and recovery. Require explicit authorization for production-impacting actions; do not broaden access as a diagnostic shortcut.

After change, verify the intended API and data-plane behavior, denied access, service health, audit events, alarms, backup/replication state, quotas, costs, and IaC drift. For incidents, preserve CloudTrail, Config, service logs, timestamps, and request IDs before remediation changes erase context.
