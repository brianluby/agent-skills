#!/usr/bin/env bash
set -euo pipefail

apm marketplace check
apm pack --check-versions --dry-run

while IFS= read -r primitive_file; do
  apm audit --file "$primitive_file"
done < <(find packages -path '*/.apm/*' -type f -name '*.md' | sort)
