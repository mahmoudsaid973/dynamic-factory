# Dynamic Factory

A visual software/product factory that lets users compose workflows, generated applications, agents, skills, and reports with pluggable LLM providers.

## Architecture

| Component | Stack | Path |
|---|---|---|
| Frontend | Next.js 15, React 19, TypeScript strict, Tailwind CSS v4, ReactFlow | `apps/web` |
| Backend | FastAPI, SQLAlchemy async, Pydantic, PostgreSQL, Redis | `services/api` |
| Hermes Skills | Reusable agent procedures | `skills/` |
| MCP Templates | Sample MCP server bridges | `mcp-templates/` |

## Getting Started

```bash
cp .env.example .env
# Edit .env with your provider keys and database settings.

docker compose up -d db redis

cd services/api
uv sync --all-extras
uv run alembic upgrade head
uv run python -m dynamic_factory.main

cd ../../apps/web
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

## Development

| Task | Command |
|---|---|
| Backend tests | `cd services/api && uv sync --all-extras && uv run pytest` |
| Frontend tests | `cd apps/web && npm test` |
| E2E tests | `cd apps/web && npx playwright test` |
| Lint backend | `cd services/api && uv run ruff check .` |
| Type-check frontend | `cd apps/web && npx tsc --noEmit` |

## CI/CD

All workflows trigger on push and pull requests to `main`. See `.github/workflows/` for test, lint, security, quality, deploy, stale, and release automation.
