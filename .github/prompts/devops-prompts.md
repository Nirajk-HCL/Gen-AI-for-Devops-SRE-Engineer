VS Code Copilot prompts for DevOps tasks
--------------------------------------

- CI Workflow (GitHub Actions):
  "Create a GitHub Actions workflow that runs Node.js unit tests on push to `develop` and `main`, uploads JUnit test results and artifacts, and populates a status context named `unit-tests`."
- CodeQL on PRs:
  "Create a GitHub Actions workflow that runs CodeQL analysis on pull requests targeting `main` and `develop`, and posts findings as check runs."
- Azure DevOps Maven pipeline:
  "Generate an `azure-pipelines.yml` for a Java service using Maven that runs `mvn clean test`, publishes JUnit test results, and uploads the `target` folder as an artifact."
- Branch protection script:
  "Write a script that uses the GitHub REST API to apply branch protection for `main` and `develop`, requiring `unit-tests`, `lint`, `sast`, and `dast` status checks."
- Run tests locally:
  "Generate a `run-tests.sh` that detects Node/Python/Go projects and runs the appropriate test command, returning JUnit XML where possible."
- Run linters locally:
  "Create a `run-lint.sh` that runs `eslint`, `flake8`, or `golangci-lint` depending on repo contents."
- DAST placeholder:
  "Create a `run-dast.sh` that runs OWASP ZAP baseline against a PR preview URL (use `DAST_TARGET` env var)."
- Terraform module:
  "Write a Terraform module scaffold for an AWS VPC with public/private subnets, outputs for IDs, and a usage example."
- Terraform CI:
  "Produce a GitHub Actions workflow that runs `terraform init`, `terraform validate`, and `terraform plan` on PRs, and comments the plan result on the PR."
- Kubernetes manifest generator:
  "Generate a deployment + service manifest for a containerized app with configurable replicas, resource requests/limits, and a readiness probe."
- Helm chart scaffold:
  "Create a minimal Helm chart (Chart.yaml, values.yaml, templates/deployment.yaml) for a web service."
- Dockerfile + multi-stage build:
  "Produce a secure multi-stage Dockerfile for a Node app that minimizes final image size."
- CI secret handling:
  "Create a workflow snippet showing how to use GitHub Actions secrets and the `actions/github-script` for masked printing."
- Canary deploy pipeline:
  "Generate a GitHub Actions workflow to build image, push to registry, and perform a canary rollout in Kubernetes (10%→100%) with manual approval."
- Rollback playbook:
  "Write a concise SRE rollback runbook for a failed deploy (steps: identify release, revert via pipeline, monitor, notify)."
- Monitoring alerts:
  "Create an alert rule example for Prometheus Alertmanager to fire on high error rate (5xx > 5% for 5m) and an alert playbook."
- SAST integration:
  "Provide a workflow integrating CodeQL and fail PRs on high-severity findings."
- Secret scanning:
  "Add a GitHub Actions job that runs `trufflehog` on PRs and posts results as comments."
- Test coverage publishing:
  "Create a workflow to run tests, collect coverage (lcov or cobertura), and upload to Codecov/GitHub Code Scanning."
- Infra drift check:
  "Create a job that runs `terraform plan -detailed-exitcode` to detect drift on a schedule."
- Azure resource deployment:
  "Generate an Azure DevOps job to run `az cli` commands to deploy an ARM/Bicep template and publish deployment logs."
- K8s rollout status check:
  "Make a step that waits for deployment rollout (`kubectl rollout status`) and fails if not healthy within timeout."
- PR checklist automation:
  "Create an Action to ensure PRs have a linked issue, changelog entry, and at least one approval before merging."
- Audit log export:
  "Produce a script that exports GitHub audit logs or Azure Activity Logs for the last 7 days into a CSV."
- On-call escalation:
  "Generate an automated PagerDuty trigger payload example and a playbook step for urgent incidents."
