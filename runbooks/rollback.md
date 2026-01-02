Rollback runbook
================

Scope: Steps to rollback a failed release to the previous known-good version.

1. Identify the failing release (CI pipeline ID, image tag, commit SHA).
2. Check health/alerts to confirm rollback is necessary.
3. If using Kubernetes:
   - `kubectl rollout undo deployment/myservice` to revert to previous ReplicaSet.
   - `kubectl rollout status deployment/myservice` to verify.
4. If using artifact registry / pipeline:
   - Trigger pipeline to deploy previous artifact (`artifact: <previous-tag>`).
5. Monitor logs and metrics for 15 minutes. If issue persists, escalate to on-call.
6. Create an incident postmortem with root cause and follow-up actions.
