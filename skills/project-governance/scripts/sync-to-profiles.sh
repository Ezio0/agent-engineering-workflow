#!/usr/bin/env bash
# Sync project-governance SKILL.md from ezio-zero to all other profiles.
# Run after ANY patch to this skill.
set -euo pipefail

SRC="/Users/ezio/.hermes/profiles/ezio-zero/skills/software-development/project-governance/SKILL.md"
PROFILES=(ezio-infinite ezio-quarter ezio-half)

for profile in "${PROFILES[@]}"; do
  DST="/Users/ezio/.hermes/profiles/$profile/skills/software-development/project-governance/SKILL.md"
  if [ -d "$(dirname "$DST")" ]; then
    cp "$SRC" "$DST"
    echo "$profile: synced"
  else
    echo "$profile: SKIP (skill dir not found)"
  fi
done

echo "--- MD5 verification ---"
for profile in ezio-zero "${PROFILES[@]}"; do
  DST="/Users/ezio/.hermes/profiles/$profile/skills/software-development/project-governance/SKILL.md"
  if [ -f "$DST" ]; then
    echo "$profile: $(md5 -q "$DST" 2>/dev/null || md5sum "$DST" | cut -d' ' -f1)"
  fi
done
