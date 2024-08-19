#!/bin/bash
set -e

for file in *.md; do
  if grep -q "_enter" "$file"; then
    echo "Replace all text having _enter with your input"
    exit 1
  fi
done
