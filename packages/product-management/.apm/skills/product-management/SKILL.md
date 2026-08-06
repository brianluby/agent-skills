---
name: product-management
description: Use when framing a product problem, prioritizing opportunities, defining outcomes and metrics, scoping an MVP or experiment, writing user stories and acceptance criteria, or turning ambiguous requests into a testable delivery plan.
---

# Product management

Begin with the target user, observed problem, and customer-facing result. Do not turn an unvalidated solution idea directly into a roadmap commitment.

## Workflow

1. Frame the opportunity.
   - Identify the user segment, current behavior or workaround, pain, frequency, constraints, and evidence.
   - Separate known facts, assumptions, and open questions.
2. Define the outcome.
   - State the user and business result in plain language.
   - Choose a primary success metric, guardrails, baseline, target, evaluation window, and decision threshold when evidence supports them.
3. Compare options.
   - Include doing nothing or running a smaller experiment.
   - Evaluate user value, strategic fit, evidence strength, effort, dependencies, risk, reversibility, and opportunity cost.
   - Use RICE, value-versus-effort, or MoSCoW only when its inputs clarify the decision; label estimates rather than presenting them as facts.
4. Scope the smallest useful test.
   - Define who is in scope, the end-to-end outcome, explicit non-goals, failure modes, instrumentation, and feedback channel.
   - Prefer a reversible experiment or narrow vertical slice over a broad feature inventory.
5. Prepare delivery.
   - Break work into independently verifiable slices.
   - Write observable acceptance criteria, dependencies, rollout and rollback considerations, and unresolved decisions.

## Output

Match the artifact to the decision: a concise opportunity brief, option table, experiment plan, roadmap slice, or engineering-ready story. Include a recommendation and why, the evidence behind it, what would change the decision, and the next smallest action.

For user stories, use `As a <user>, I want <capability>, so that <outcome>` only when it adds clarity. Acceptance criteria should use concrete inputs and observable results rather than restating implementation tasks.

Challenge scope that lacks evidence, duplicates an existing capability, or delays a more important customer outcome. Preserve promising ideas in a clearly separated later/not-now section instead of silently expanding the current commitment.
