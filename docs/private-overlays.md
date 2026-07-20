# Private company overlays

Public and company-only skills are separate trust boundaries.

Create a second, private Git repository for every organization that needs internal skills. The private repository may depend on public packages from this marketplace; this public marketplace must never depend on, install, or mention private skill content.

```text
public agent-skills marketplace
        ^
        |
private company-agent-skills marketplace
        ^
        |
company application repository
```

## What belongs in an overlay

- Internal architecture and service ownership
- Private APIs, tools, and deployment conventions
- Company security controls and incident procedures
- Customer-specific or regulated workflows

## What does not

Do not use a `private/` directory in this repository. Git and GitHub access are repository-level boundaries; a file committed here is public, including its history.

## Setup

1. Copy `templates/company-overlay` into a new private repository.
2. Replace the placeholder owner, repository names, and descriptions.
3. Add company-only skills under `packages/<package>/.apm/skills/`.
4. Register the private marketplace in company repositories, then install its packages alongside public packages.
5. Use GitHub organization access control, `gh auth login`, or a fine-grained read-only `GITHUB_APM_PAT` to authorize APM installs.

The private repository should validate every skill, use its own review requirements, and pin public package versions through each consumer's lockfile.
