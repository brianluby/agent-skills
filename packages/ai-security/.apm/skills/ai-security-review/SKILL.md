---
name: ai-security-review
description: Use when reviewing LLM, agent, RAG, tool-calling, memory, or AI-assisted workflows for prompt injection, unsafe agency, sensitive-data exposure, insecure output handling, or unbounded resource use.
---

# AI security review

Review the surrounding system, not only the prompt. Model instructions are probabilistic controls; authorization and data protection must be enforced outside the model.

## Threat analysis

1. Map the AI data flow.
   - Identify system and developer instructions, user input, retrieved content, tool results, memory, model output, and downstream consumers.
   - Mark every source that an attacker or external publisher can influence, including indirect content from documents, web pages, issue text, and repositories.
2. Map authority and consequences.
   - List tools, credentials, network destinations, files, records, and actions the model can reach.
   - Verify that each action is authorized by deterministic code at execution time, not inferred from model text.
3. Test instruction-boundary failures.
   - Exercise direct and indirect prompt injection, instruction conflicts, encoded or split payloads, forged tool output, and poisoned retrieved content.
   - Treat delimiters, filtering, RAG, and fine-tuning as partial defenses rather than proof that injection is impossible.
4. Review data handling.
   - Minimize sensitive context, redact before model access where possible, constrain retention, and check logs, traces, caches, memory, and outputs.
   - Do not treat a hidden system prompt as a secret or security boundary.
5. Review outputs and resource limits.
   - Validate and encode model output before SQL, HTML, shell, code, policy, or API use.
   - Bound iterations, tokens, concurrency, tool calls, spend, and retry behavior; define cancellation and failure behavior.

## Safer agent design

- Give the model the least privilege and fewest tools required for the task.
- Separate planning from execution and validate typed tool arguments.
- Require explicit user confirmation for consequential, destructive, financial, or externally visible actions.
- Scope credentials and network access per tool; use allowlists where the destination set is known.
- Make tool results untrusted data and prevent them from silently changing policy.
- Record security-relevant decisions without logging sensitive prompt contents by default.

## Findings

For each finding, provide the attack source, trust-boundary crossing, required capability, concrete consequence, existing defenses, confidence, and a testable remediation. Distinguish architectural control gaps from prompt-quality suggestions.
