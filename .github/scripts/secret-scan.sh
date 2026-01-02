#!/usr/bin/env bash
set -euo pipefail
if ! command -v trufflehog >/dev/null 2>&1; then
  echo "Install trufflehog or use the GitHub action."
  exit 1
fi

trufflehog filesystem --path . || true
