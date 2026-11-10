# Dynamic Factory — Phase 1 Implementation Plan

> **Goal:** Build the foundation of a visual software/product factory where users compose workflows, generated apps, agents/skills, and reports with pluggable LLM providers. Delivered as a standalone Next.js + FastAPI app and a Hermes skill wrapper.

> **Architecture:** Monorepo with a Next.js 15 (App Router, TypeScript strict) frontend, FastAPI + SQLAlchemy async backend, PostgreSQL + Redis, Docker Compose for local/private-cloud deployment, and GitHub Actions CI/CD. The core abstraction is a node-based workflow engine: nodes = capabilities (LLM, tool, agent, skill, MCP, code-gen), edges = data flow. A pluggable provider registry decouples LLM calls from vendor specifics. A Hermes skill (`/factory`) wraps the backend API so the chat interface can create/run flows.

> **Tech Stack:** Next.js 15, React 19, TypeScript strict, Tailwind CSS v4, Zustand, TanStack Query, ReactFlow, FastAPI, SQLAlchemy 2 async, PostgreSQL, Redis, Docker Compose, pytest, vitest, Playwright.

---

## Phase 1 Scope

1. Repository scaffold and tooling
2. CI/CD pipeline (test, lint, security, quality, deploy, dependabot, stale, release)
3. Backend: provider registry + provider API
4. Backend: workflow engine core (models, serialization, in-memory executor)
5. Backend: one runnable flow endpoint (`POST /api/v1/flows/{id}/run`)
6. Frontend: node editor scaffold (ReactFlow canvas, basic layout)
7. Frontend: provider selector + run button + result panel
8. End-to-end flow: "Prompt → LLM (OpenAI-compatible) → Result"
9. One MCP bridge template (filesystem read/write as a node)
10. One Hermes skill template (`/factory`) that creates and runs a flow via the API
11. Tests: backend unit + integration, frontend component, Playwright smoke test

---

## Task 1: Repository Scaffold

**Objective:** Create the monorepo folder structure and root configuration files.

**Files:**
- Create: `README.md`
- Create: `.gitignore`
- Create: `docker-compose.yml`
- Create: `package.json`
- Create: `pyproject.toml`
- Create: `.env.example`
- Create: `apps/web/package.json`
- Create: `services/api/pyproject.toml`

**Steps:**
1. Create root `package.json` with workspace definition (`apps/web`, `services/api`).
2. Create `docker-compose.yml` with PostgreSQL 16, Redis 7, and placeholder services.
3. Create `pyproject.toml` at root and under `services/api` with FastAPI, SQLAlchemy async, pydantic-settings, pytest, ruff, mypy, httpx.
4. Create `apps/web/package.json` with Next.js 15, React 19, TypeScript, Tailwind v4, Zustand, TanStack Query, ReactFlow, vitest, Playwright.
5. Create `.env.example` with database, Redis, and provider key placeholders.
6. Write `README.md` with setup commands.

**Verification:** `ls apps/web services/api` shows expected files; `docker compose config` parses without error.

**Commit:** `chore: scaffold dynamic-factory monorepo`

---

## Task 2: CI/CD Workflows

**Objective:** Add all mandatory GitHub Actions workflows per project convention.

**Files:**
- Create: `.github/workflows/test.yml`
- Create: `.github/workflows/lint.yml`
- Create: `.github/workflows/security.yml`
- Create: `.github/workflows/quality.yml`
- Create: `.github/workflows/deploy.yml`
- Create: `.github/dependabot.yml`
- Create: `.github/workflows/stale.yml`
- Create: `.github/workflows/release.yml`
- Create: `Dockerfile` (api) and `apps/web/Dockerfile`

**Steps:**
1. `test.yml`: Python pytest + frontend vitest, upload to Codecov.
2. `lint.yml`: ruff + tsc --noEmit (no next lint).
3. `security.yml`: Semgrep, Bandit, Trivy, TruffleHog, pip-audit, npm audit.
4. `quality.yml`: PR size check, conventional commit check, bundle size report.
5. `deploy.yml`: Docker build with GHA cache, push to GHCR on tags.
6. `dependabot.yml`, `stale.yml`, `release.yml` per convention.
7. Add Dockerfiles for both services.

**Verification:** `act -j lint` (or push to feature branch) passes; YAML files validate.

**Commit:** `ci: add github actions workflows and dockerfiles`

---

## Task 3: Backend Provider Registry

**Objective:** Define provider models and a registry that supports OpenAI-compatible, Anthropic, Azure, and local (Ollama) providers dynamically.

**Files:**
- Create: `services/api/src/dynamic_factory/models/provider.py`
- Create: `services/api/src/dynamic_factory/providers/base.py`
- Create: `services/api/src/dynamic_factory/providers/openai_provider.py`
- Create: `services/api/src/dynamic_factory/providers/registry.py`
- Create: `services/api/src/dynamic_factory/api/v1/providers.py`
- Create: `services/api/src/dynamic_factory/main.py`
- Create: `services/api/tests/test_providers.py`

**Steps:**
1. Define `Provider` SQLAlchemy model with id, name, kind, base_url, api_key (encrypted at rest — store ciphertext), model_default, config JSON.
2. Define `ProviderClient` abstract base with `chat(messages, params) -> ChatResponse`.
3. Implement `OpenAICompatibleProvider` using `httpx.AsyncClient`.
4. Build `ProviderRegistry` that loads providers from DB and returns a client by id.
5. Expose `GET /api/v1/providers` and `POST /api/v1/providers`.
6. Add Alembic migration for the provider table.

**Verification:** `pytest services/api/tests/test_providers.py -v` passes.

**Commit:** `feat: add pluggable provider registry`

---

## Task 4: Backend Workflow Engine Core

**Objective:** Implement workflow definitions and an in-memory executor that can run a DAG of nodes.

**Files:**
- Create: `services/api/src/dynamic_factory/models/workflow.py`
- Create: `services/api/src/dynamic_factory/engine/workflow.py`
- Create: `services/api/src/dynamic_factory/engine/nodes/base.py`
- Create: `services/api/src/dynamic_factory/engine/nodes/llm_node.py`
- Create: `services/api/src/dynamic_factory/engine/nodes/prompt_node.py`
- Create: `services/api/src/dynamic_factory/api/v1/flows.py`
- Create: `services/api/tests/test_engine.py`

**Steps:**
1. Define `Workflow`, `Node`, `Edge` models with JSON schema fields.
2. Implement `WorkflowEngine` that topologically sorts nodes, executes async, and stores node outputs in a context dict.
3. Implement `PromptNode` (returns static or templated text) and `LLMNode` (calls provider registry, sends prompt, returns response).
4. Expose `POST /api/v1/flows` (create), `GET /api/v1/flows/{id}`, `POST /api/v1/flows/{id}/run`.

**Verification:** `pytest services/api/tests/test_engine.py -v` passes; a 3-node flow runs end-to-end in-memory.

**Commit:** `feat: add workflow engine with prompt and llm nodes`

---

## Task 5: Frontend Node Editor Scaffold

**Objective:** Create the visual canvas where users build flows.

**Files:**
- Create: `apps/web/src/app/layout.tsx`
- Create: `apps/web/src/app/page.tsx`
- Create: `apps/web/src/components/FlowCanvas.tsx`
- Create: `apps/web/src/components/nodes/PromptNode.tsx`
- Create: `apps/web/src/components/nodes/LLMNode.tsx`
- Create: `apps/web/src/lib/api.ts`
- Create: `apps/web/src/types/flow.ts`

**Steps:**
1. Initialize Next.js App Router with root layout and Tailwind v4 config.
2. Add ReactFlow canvas with custom node types: `prompt`, `llm`.
3. Add toolbar to add nodes and connect edges.
4. Add TanStack Query provider.
5. Create a lightweight API client in `lib/api.ts` pointing at the FastAPI backend.

**Verification:** `npm run dev` starts; browser shows empty canvas with add-node toolbar.

**Commit:** `feat: scaffold reactflow node editor`

---

## Task 6: Frontend Provider Selector + Run + Result Panel

**Objective:** Wire the UI to the backend so a user can configure a provider, build a flow, run it, and see the result.

**Files:**
- Create: `apps/web/src/components/ProviderPanel.tsx`
- Create: `apps/web/src/components/RunPanel.tsx`
- Modify: `apps/web/src/components/FlowCanvas.tsx`
- Modify: `apps/web/src/app/page.tsx`

**Steps:**
1. `ProviderPanel`: list/create providers, select active provider for the LLM node.
2. `RunPanel`: button to POST `/api/v1/flows/{id}/run`, poll/run once, display outputs per node.
3. `FlowCanvas`: persist node positions and edge connections; serialize to workflow JSON on save.
4. `page.tsx`: compose canvas + provider panel + run panel in a 3-column layout.

**Verification:** Playwright smoke test: create provider, add prompt node, add llm node, connect, run, assert result panel shows text.

**Commit:** `feat: wire provider selector and run panel`

---

## Task 7: MCP Bridge Template

**Objective:** Add a filesystem MCP node so the factory can talk to an MCP server.

**Files:**
- Create: `services/api/src/dynamic_factory/engine/nodes/mcp_node.py`
- Create: `services/api/src/dynamic_factory/mcp/client.py`
- Create: `mcp-templates/filesystem/README.md`
- Create: `mcp-templates/filesystem/server.py`
- Create: `services/api/tests/test_mcp_node.py`

**Steps:**
1. Implement a minimal MCP client over stdio that calls `tools/list` and `tools/call`.
2. Add `MCPNode` that reads/writes a file via the filesystem MCP server.
3. Provide a sample filesystem MCP server in `mcp-templates/filesystem/server.py`.
4. Add a node type in the frontend and backend serialization.

**Verification:** `pytest services/api/tests/test_mcp_node.py -v` passes with the sample MCP server.

**Commit:** `feat: add filesystem mcp bridge template`

---

## Task 8: Hermes Skill Template

**Objective:** Add a Hermes skill that lets the chat interface create and run a flow.

**Files:**
- Create: `skills/autonomous-ai-agents/dynamic-factory/SKILL.md`
- Create: `skills/autonomous-ai-agents/dynamic-factory/scripts/create_and_run.py`
- Create: `tests/skills/test_dynamic_factory_skill.py`

**Steps:**
1. Write `SKILL.md` with triggers, prerequisites, and procedure using Hermes tools (`terminal`, `web_search`, `write_file`, etc.).
2. Create a helper script that calls the factory API to create a default flow and run it.
3. Add a test that validates the skill frontmatter and basic procedure.

**Verification:** `pytest tests/skills/test_dynamic_factory_skill.py -v` passes; frontmatter valid.

**Commit:** `feat: add dynamic-factory hermes skill template`

---

## Task 9: Integration + Browser Smoke Test

**Objective:** Prove the full stack works in a browser.

**Files:**
- Create: `apps/web/e2e/smoke.spec.ts`
- Create: `services/api/tests/test_flow_api.py`
- Modify: `docker-compose.yml` to add api and web services

**Steps:**
1. Start PostgreSQL + Redis + API + web via Docker Compose.
2. Backend integration test: create provider, create flow, run flow, assert LLM node output.
3. Playwright test: same happy path in browser; also verify an error state (missing provider) shows an error.
4. Capture screenshots on failure and success.

**Verification:** `pytest services/api/tests/test_flow_api.py` and `npx playwright test apps/web/e2e/smoke.spec.ts` pass.

**Commit:** `test: add integration and browser smoke tests`

---

## Risks and Tradeoffs

| Risk | Mitigation |
|---|---|
| Scope creep into a full no-code IDE | Strictly limit Phase 1 to prompt→LLM→result + one MCP + skill template. |
| Provider key security | Store keys encrypted at rest; never return them in API responses; use `.env.example` only. |
| ReactFlow + Next.js SSR issues | Mark canvas component `'use client'`; load ReactFlow dynamically if needed. |
| MCP stdio lifecycle in container | Use long-running SSE/HTTP MCP server in Phase 1; stdio reserved for local dev. |
| CI minutes on large security scans | Pin images, use GHA cache, run security scans weekly + on PR. |

## Open Questions

1. Which LLM provider should be the default in the sample flow? (Assume OpenAI-compatible base URL + key.)
2. Should the Hermes skill live in this repo or separately? (Decision: in-repo under `skills/`.)
3. Do we need multi-tenant auth in Phase 1? (Decision: no; single-user local dev in Phase 1, auth added later.)

---

## Execution Order

1. Task 1 → Task 2 → Task 3 → Task 4 → Task 5 → Task 6 → Task 7 → Task 8 → Task 9
2. Commit after each task.
3. Open PR to `main` only after all tests pass locally.
