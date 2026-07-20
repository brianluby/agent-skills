---
name: testing-strategy
description: Use when planning, adding, or evaluating automated tests for a behavior change, regression, bug fix, or risky edge case.
---

# Testing strategy

Define the observable behavior before writing a test. Identify the smallest test level that exercises the changed contract: unit, integration, contract, or end-to-end.

Cover the successful path, the failure or boundary condition that motivated the change, and one regression guard when a prior defect exists. Prefer deterministic fixtures and assertions on observable outcomes over implementation details.

Do not inflate coverage with tests that duplicate an existing assertion without protecting a new behavior. Run the focused test first, then the repository's relevant broader suite when the change crosses a component or interface boundary.
