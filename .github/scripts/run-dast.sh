#!/usr/bin/env bash
set -euo pipefail
echo "Running DAST placeholder — customize to scan your running app"
echo "If you have an app deployed for PR preview, run OWASP ZAP baseline here."
if command -v zap-baseline.py >/dev/null 2>&1; then
  zap-baseline.py -t "${DAST_TARGET:-http://localhost:8080}" || true
  exit 0
fi
echo "No DAST scanner configured. Install OWASP ZAP or update this script." >&2
exit 1
