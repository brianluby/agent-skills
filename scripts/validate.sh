#!/usr/bin/env bash
set -euo pipefail

apm marketplace check
apm pack --check-versions --dry-run

while IFS= read -r skill; do
  apm audit --file "$skill"
done < <(find packages -path '*/.apm/skills/*/SKILL.md' -type f | sort)
