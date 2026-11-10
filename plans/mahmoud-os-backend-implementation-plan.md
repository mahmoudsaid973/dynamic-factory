# Mahmoud OS Backend Implementation Plan

## Scope

Implement the backend and core API for Mahmoud OS, excluding frontend/UI which is handled by ChatGPT.

## Phase 1: Data model foundation

1. `projects` domain — Project, ProjectWorkflowBinding.
2. `workflows` versioning — WorkflowVersion, immutable published snapshots.
3. `runs` domain — Run, Invocation, Attempt with durable identity.
4. `events` domain — Event, Evidence, first-failure preservation.
5. `allowance` domain — Ledger, reservation, exhaustion checks.
6. `connectors` domain — ConnectorRegistry, MCP server records.

## Phase 2: Core engine and gateway

1. The Bridge gateway module — receive requests, classify, correlate.
2. JEV Routing Agent — Tier 1 (lookup/zero-model), Tier 2 (quick/bounded), Tier 3 (planned workflow).
3. Preflight validation — missing credentials, unbound ports, permission blockers.
4. Durable executor — admit run against published version, execute small work items, pause/resume/cancel, produce events.
5. Idempotency — idempotency keys, reconciliation tests.
6. Human approval checkpoint — block consequential actions until approved.
7. Allowance Governor — cap/reserve enforcement before provider calls.
8. Nested workflows — subworkflow calls, conditions, branches, joins.

## Phase 3: API surface

1. Project Hub routes (`/api/v1/projects`).
2. Workflow Studio routes (`/api/v1/workflows`, `/versions`, `/publish`).
3. Bridge routes (`/api/v1/bridge/requests`).
4. Run routes (`/api/v1/runs`, `/runs/{id}/pause`, `/resume`, `/cancel`).
5. Connector routes (`/api/v1/connectors`).
6. Allowance routes (`/api/v1/allowance`).

## Phase 4: Tests and CI

1. Unit tests for engine, gateway, allowance.
2. API tests for projects, workflows, runs, connectors.
3. Ensure `uv run ruff check src tests`, `uv run mypy src`, `uv run pytest` pass.

## Non-goals for this pass

- Frontend/UI changes.
- Obsidian plugin packaging.
- Agent Studio, Skill Channel, LLM Council, Agent Swarm advanced features.
- Commerce/payments, native mobile, design-to-code, support desk.
- Real-time SSE (except durable run records available via polling).
