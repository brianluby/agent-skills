---
name: aws-engineering
description: Use when designing, implementing, reviewing, automating, or troubleshooting AWS architecture, IAM, networking, compute, storage, databases, observability, and service operations.
---

# AWS engineering

Establish the intended account, partition, region, organization constraints, workload criticality, data classification, recovery objectives, deployment owner, and infrastructure-as-code source before acting. Names and profiles are not proof of identity.

## Safety and identity

- Start with read-only discovery. Before any mutation, verify caller identity and region through the approved credential mechanism and compare account IDs/aliases to the stated target without printing credentials.
- Prefer short-lived federated roles, workload identity, and service roles. Never create or embed long-lived access keys when a supported role mechanism exists.
- Treat console, CLI, SDK, and IaC changes as the same production risk. Use explicit authorization, change review, audit logging, and rollback/recovery for mutating operations.
- Never disable logging, encryption, backups, retention, guardrails, or security controls merely to make deployment succeed.

## Architecture principles

- Design for regional service behavior, quotas, failure modes, throttling, eventual consistency, and retry/idempotency semantics—not only the happy path.
- Apply least privilege to identities and resource policies, considering conditions, permission boundaries, SCPs, session policies, KMS key policies, and cross-account trust together.
- Keep workloads private by default. Minimize public endpoints, unrestricted security-group rules, wildcard resource policies, and data-plane access from control networks.
- Encrypt in transit and at rest with a documented ownership/rotation model. Validate that principals can use both the service and KMS key without broadening either policy unnecessarily.
- Make stateful services recoverable: backups, retention, point-in-time recovery, replication, deletion protection, and tested restore/failover aligned to RPO/RTO.
- Build observability around user-impacting signals, structured logs, traces, metrics, health, audit events, and actionable alarms. Account for log cost and sensitive-data redaction.
- Tag and allocate cost consistently. Evaluate data transfer, NAT, logging, storage classes, idle capacity, request patterns, and commitment tradeoffs with measured usage.

## Change workflow

1. Map the resource, dependencies, policies, network path, data flow, quotas, and IaC owner.
2. Inspect current state and recent audit/configuration evidence using read-only calls.
3. Design the smallest reversible change, including IAM and KMS evaluation, blast radius, and recovery.
4. Implement through the repository's IaC/deployment system; avoid console drift unless emergency procedure requires it.
5. Validate configuration plus real service behavior, alarms, logs, access paths, cost impact, and a clean IaC plan.

Load `references/iam-operations-and-verification.md` for CLI identity checks, IAM review, pagination/retries, safe operations, incident evidence, and post-change validation.
