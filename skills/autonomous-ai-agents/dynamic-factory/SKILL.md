---
name: dynamic-factory
description: "Create and run Dynamic Factory flows via the API."
version: 0.1.0
author: "Mahmoud Hassan, Hermes Agent"
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [dynamic-factory, workflow, llm, mcp]
    related_skills: []
---

# Dynamic Factory Skill

Build and execute visual workflows through the Dynamic Factory backend API. Use this skill when the user wants to create a flow, run an existing flow, or verify that the factory API is reachable from Hermes.

## When to Use

- Create a new prompt-to-LLM flow and run it immediately.
- Run an existing flow by ID after the API is running.
- Verify the factory API is healthy and the default provider is configured.

## Prerequisites

- The Dynamic Factory API is running (`docker compose up api` or `uv run python -m dynamic_factory.main` in `services/api`).
- `FACTORY_API_URL` is set, or the API is reachable at `http://localhost:8000`.
- `OPENAI_API_KEY` (or the configured provider key) is available in the environment.
- Python 3.12+ and `httpx` are installed for the helper script.

## Procedure

1. Confirm the API is healthy with `terminal(command="curl -fsS ${FACTORY_API_URL:-http://localhost:8000}/health")` or an equivalent `httpx` probe.
2. If the user provided a custom prompt, capture it; otherwise use the default from the helper script.
3. Run `terminal(command="python skills/autonomous-ai-agents/dynamic-factory/scripts/create_and_run.py --prompt '...'")`.
4. Inspect the returned run payload. The `outputs` mapping contains results per node ID.
5. If the LLM node reports a provider error, check that the provider key and base URL are exported and retry.

## Pitfalls

- The helper script assumes the API endpoints from the Dynamic Factory Phase 1 plan exist. If they do not, it will fail with a 404; implement the provider registry and workflow engine first.
- The script creates a provider on every invocation. In production, reuse an existing provider ID and call `POST /api/v1/flows/{id}/run` directly.
- Stdio MCP servers spawned by `MCPNode` must be executable from the API's environment; containerized deployments usually prefer HTTP/SSE MCP servers.

## Verification

- The API health endpoint returns HTTP 200.
- The flow run payload contains `status: completed` and an `outputs` dictionary with entries for `prompt-1` and `llm-1`.
