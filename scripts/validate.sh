#!/usr/bin/env bash
set -euo pipefail

apm marketplace check
apm pack --check-versions --dry-run

while IFS= read -r instruction_file; do
  apm audit --file "$instruction_file"
done < <(find packages -path '*/.apm/skills/*' -type f -name '*.md' | sort)
