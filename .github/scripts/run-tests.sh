#!/usr/bin/env bash
set -euo pipefail
echo "Detecting test runner..."
if [ -f package.json ]; then
  echo "Running npm tests"
  npm ci
  npm test
  exit 0
fi
if [ -f pyproject.toml ] || [ -f requirements.txt ] || [ -d tests ]; then
  echo "Running pytest"
  python -m pip install -r requirements.txt || true
  pytest -q
  exit 0
fi
if [ -f go.mod ]; then
  echo "Running go test"
  go test ./...
  exit 0
fi
echo "No supported test runner detected. Please customize .github/scripts/run-tests.sh to run your project's tests." >&2
exit 1
