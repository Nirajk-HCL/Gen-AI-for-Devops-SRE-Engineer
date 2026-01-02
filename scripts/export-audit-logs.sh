#!/usr/bin/env bash
set -euo pipefail
if [ -z "${GITHUB_ORG:-}" ] || [ -z "${GITHUB_TOKEN:-}" ]; then
  echo "Set GITHUB_ORG and GITHUB_TOKEN to export audit logs (enterprise required)."
  exit 1
fi

curl -H "Authorization: token $GITHUB_TOKEN" "https://api.github.com/orgs/$GITHUB_ORG/audit-log" -o audit-log.json
echo "Wrote audit-log.json"
