---
name: security-review
description: Use when reviewing a pull request, patch, component, or repository for exploitable application-security defects, trust-boundary failures, unsafe privilege, secret exposure, or missing security verification.
---

# Security review

Read the repository instructions and security policy first. Treat them as the source of project-specific invariants; this skill supplies the reusable review method.

## Review workflow

1. Define the scope and attacker model.
   - Identify the changed or requested surface, entry points, protected assets, identities, and trust boundaries.
   - Distinguish attacker-controlled input from trusted configuration and internal state.
2. Trace security-relevant data and control flow.
   - Follow input through parsing, authorization, storage, subprocesses, network calls, serialization, and output.
   - Inspect callers and callees rather than judging an isolated line.
3. Form concrete vulnerability hypotheses.
   - Prioritize access control, injection, unsafe deserialization, path traversal, SSRF, secret handling, cryptography, race/TOCTOU behavior, and fail-open paths when relevant.
   - Use stack-specific checks only when the implementation exposes that surface.
4. Validate each candidate.
   - Establish reachability, required privileges, attacker control, existing mitigations, and realistic impact.
   - Reproduce safely with focused tests or static inspection when practical. Do not turn a speculative pattern match into a finding.
5. Report actionable results.
   - Give the file and location, triggering conditions, execution path, impact, severity, confidence, and the smallest sound remediation direction.
   - State what was reviewed and what could not be validated.

## Severity guide

- **Critical:** practical compromise with severe cross-user, cross-tenant, or system-wide impact.
- **High:** exploitable loss of confidentiality, integrity, authorization, or availability with meaningful impact.
- **Medium:** real but constrained exploitability or impact, or a missing defense at a meaningful boundary.
- **Low:** limited security impact or hardening with a credible misuse case.

Calibrate severity to the actual deployment and privileges. Do not inflate severity because a weakness resembles a well-known category.

## Review boundaries

- Keep general correctness and style feedback in the normal code-review workflow unless it creates security impact.
- Prefer repository-configured analyzers and focused checks. Do not install or activate broad scanners merely because this skill was invoked.
- Never include live secrets, exploit harmful production systems, or mutate external state during validation.
- When no validated vulnerabilities remain, say so and list residual risk or untested surfaces instead of manufacturing findings.
