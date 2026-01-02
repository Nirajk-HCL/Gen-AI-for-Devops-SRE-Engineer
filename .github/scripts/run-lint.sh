#!/usr/bin/env bash
set -euo pipefail
echo "Detecting linters..."
if [ -f package.json ] && grep -q "eslint" package.json 2>/dev/null; then
  echo "Running eslint"
  npm ci
  npm run lint --if-present
  exit 0
fi
if command -v flake8 >/dev/null 2>&1; then
  echo "Running flake8"
  flake8 || true
  exit 0
fi
if command -v golangci-lint >/dev/null 2>&1; then
  echo "Running golangci-lint"
  golangci-lint run ./...
  exit 0
fi
echo "No supported linter detected. Please customize .github/scripts/run-lint.sh to run your project's linter." >&2
exit 1
