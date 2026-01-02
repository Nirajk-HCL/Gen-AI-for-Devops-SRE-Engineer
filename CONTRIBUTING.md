Branching model
----------------

We follow a simple git branching model:

- `main`: production-ready code. Protected; merges via pull request only.
- `develop`: integration branch for ongoing work; protected.
- `feature/*`: feature branches created from `develop` (e.g. `feature/awesome`).

Protection & required checks
---------------------------

Required checks for protected branches:

- `unit-tests` — run your project's unit tests.
- `lint` — run linters.
- `sast` — static application security testing (CodeQL).
- `dast` — dynamic application security testing (e.g., OWASP ZAP).

Additional CI integrations
-------------------------

- `azure-pipelines` / `Azure Pipelines` — If you use Azure DevOps pipelines, include the pipeline status as a required check. The branch protection helper (`.github/scripts/setup-branch-protection.sh`) includes both `azure-pipelines` and `Azure Pipelines` contexts by default; adjust if your pipeline reports a different status context name.

How to enable protections (admin)
--------------------------------

1. Customize the CI scripts in `.github/scripts/` for your project's test and lint commands.
2. Run the branch protection helper (requires a personal access token with repo admin rights):

   GH_PAT=ghp_xxx .github/scripts/setup-branch-protection.sh owner/repo

3. Verify settings in Repository → Settings → Branches.

Notes
-----

- The CI workflow `.github/workflows/ci.yml` contains jobs for those checks. Adjust job commands as needed for your language/tooling.
- The `setup-branch-protection.sh` script uses the GitHub REST API and will try to apply protections for `main`, `develop`, and the `feature/*` pattern. Ensure the token has sufficient permissions.
