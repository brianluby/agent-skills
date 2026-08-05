# Contributing

## Package boundaries

A package should deliver one coherent capability. Prefer `rust`, `code-review`, or `terraform` to a broad `engineering` package, and avoid creating a package for every tiny variation of the same workflow.

Use a new package when its skills have different consumers, release cadence, owners, or security requirements.

## Skill quality

- Give every skill an intent-first `description` that names when it should be used.
- Keep `SKILL.md` to the always-relevant workflow. Put deep material in `references/` and load it only when needed.
- Make tool commands safe, scoped, and easy to verify.
- Do not include secrets, production identifiers, customer data, internal URLs, or organization-specific processes.
- Test every command and reference a skill asks an agent to use.
- Keep each package self-contained. Do not rely on maintainer-local skills, stale external collections, or undeclared companion instructions for required behavior.

## Validation and releases

Run `bash scripts/validate.sh` before proposing a change. The marketplace uses lockstep releases while it is small: the root version and every local package version must agree.

Maintainers should release a tagged version only after validation passes and generated marketplace files have been reviewed.

## Private skills

Company-only skills belong in a private overlay repository. The public repository must not reference private packages or contain private content, even in examples, issues, or Git history. See [private overlays](docs/private-overlays.md).
