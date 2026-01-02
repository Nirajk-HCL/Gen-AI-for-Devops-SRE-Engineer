#!/usr/bin/env bash
set -euo pipefail
if [ -z "${GH_PAT:-}" ]; then
  echo "Set GH_PAT (personal access token with repo:admin permissions) before running this script." >&2
  echo "Example: GH_PAT=ghp_xxx ./setup-branch-protection.sh owner/repo" >&2
  exit 1
fi

repo="${1:-${GITHUB_REPOSITORY:-}}"
if [ -z "$repo" ]; then
  echo "Usage: $0 owner/repo" >&2
  exit 1
fi

branches=("main" "develop" "feature/*")
api_base="https://api.github.com/repos/$repo/branches"

for b in "${branches[@]}"; do
  echo "Applying branch protection to: $b"
  curl -sS -X PUT \
    -H "Authorization: token $GH_PAT" \
    -H "Accept: application/vnd.github+json" \
    "$api_base/$b/protection" \
    -d '{
      "required_status_checks": {
        "strict": true,
        "contexts": ["unit-tests","lint","sast","dast","azure-pipelines","Azure Pipelines"]
      },
      "enforce_admins": true,
      "required_pull_request_reviews": {
        "dismiss_stale_reviews": true,
        "required_approving_review_count": 1
      },
      "restrictions": null
    }' | jq . || true
done

echo "Branch protection requests submitted. Check the repository settings to verify." 
