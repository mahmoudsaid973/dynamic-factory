# CI/CD and Docker Build Plan

## Goal
Add the complete GitHub Actions CI/CD pipeline and Docker build configuration per AGENTS.md mandatory requirements for the Dynamic Factory monorepo.

## Deliverables
1. `.github/workflows/test.yml` — pytest + vitest, Codecov upload.
2. `.github/workflows/lint.yml` — ruff + `tsc --noEmit`, no `next lint`.
3. `.github/workflows/security.yml` — Semgrep, Bandit, Trivy, TruffleHog, pip-audit, npm audit, weekly schedule.
4. `.github/workflows/quality.yml` — PR size, conventional commits, bundle size.
5. `.github/workflows/deploy.yml` — Docker builds for api/web with GHA cache, GHCR push on tags.
6. `.github/dependabot.yml` — weekly pip/npm/github-actions updates.
7. `.github/workflows/stale.yml` — auto-close stale issues/PRs.
8. `.github/workflows/release.yml` — GitHub Release on tags, placeholder PyPI publish.
9. `services/api/Dockerfile` and `apps/web/Dockerfile` — multi-stage, secure, minimal images.
10. Validate YAML syntax and run `docker compose build` locally.

## Constraints
- Trigger on `push` and `pull_request` to `main`/`master`.
- `tsc --noEmit` only; exclude `*.test.ts`/`*.test.tsx` via existing tsconfig.
- No `next lint` in CI.
- Use root `package-lock.json` because the repo is an npm workspace; run web commands with `-w apps/web`.
- Web Dockerfile uses root context so `npm ci` works with the workspace lockfile; update `docker-compose.yml` and `deploy.yml` accordingly.
- Use `uv run --with <tool>` for Bandit and pip-audit so they don't need to be added to project dev dependencies.

## Validation
- Parse all YAML with Python.
- Run `docker compose build` (build only, no runtime start).
- Commit to feature branch and open PR; do not push to `main`.

## Risks
- `services/api` has no `main.py` module, so the API container image builds but will fail at runtime. This is existing app logic and outside CI/CD scope.
- No frontend tests exist yet; vitest will pass with zero tests.
- `package-lock.json` at root exists and includes the workspace, so web CI and Docker builds can use it.
