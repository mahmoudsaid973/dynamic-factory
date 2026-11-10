"""Workflow REST endpoint integration tests."""

import uuid
from typing import Any

import pytest
from fastapi.testclient import TestClient

from dynamic_factory.main import app
from dynamic_factory.providers.client import ProviderClient
from dynamic_factory.providers.registry import ProviderRegistry
from dynamic_factory.workflows.routes import get_registry

pytestmark = pytest.mark.asyncio


class FakeClient(ProviderClient):
    """Test double for LLM calls."""

    async def chat(
        self,
        messages: list[dict[str, str]],
        model: str | None = None,
        **kwargs: Any,
    ) -> str:
        return f"response with {len(messages)} message(s)"


def _build_registry(provider_id: uuid.UUID) -> ProviderRegistry:
    registry = ProviderRegistry()
    registry._clients[provider_id] = FakeClient()
    return registry


async def test_create_and_get_flow(client: TestClient) -> None:
    payload = {
        "name": "test-flow",
        "description": "integration test",
        "nodes": [
            {"kind": "prompt", "name": "greeting", "config": {"template": "Hello"}},
        ],
        "edges": [],
        "config": {},
    }
    create_response = client.post("/api/v1/flows/", json=payload)
    assert create_response.status_code == 201
    created = create_response.json()
    assert created["name"] == "test-flow"
    assert len(created["nodes"]) == 1

    get_response = client.get(f"/api/v1/flows/{created['id']}")
    assert get_response.status_code == 200
    fetched = get_response.json()
    assert fetched["id"] == created["id"]
    assert fetched["nodes"][0]["name"] == "greeting"


async def test_run_flow(client: TestClient) -> None:
    provider_id = uuid.uuid4()
    app.dependency_overrides[get_registry] = lambda: _build_registry(provider_id)

    prompt_id = uuid.uuid4()
    llm_id = uuid.uuid4()
    payload = {
        "name": "llm-flow",
        "nodes": [
            {
                "id": str(prompt_id),
                "kind": "prompt",
                "name": "prompt",
                "config": {"template": "Say hello"},
            },
            {
                "id": str(llm_id),
                "kind": "llm",
                "name": "llm",
                "config": {"provider_id": str(provider_id)},
            },
        ],
        "edges": [{"source_id": str(prompt_id), "target_id": str(llm_id)}],
    }
    create_response = client.post("/api/v1/flows/", json=payload)
    assert create_response.status_code == 201
    flow_id = create_response.json()["id"]

    run_response = client.post(f"/api/v1/flows/{flow_id}/run")
    assert run_response.status_code == 200
    data = run_response.json()
    assert data["outputs"][str(prompt_id)] == "Say hello"
    assert data["outputs"][str(llm_id)] == "response with 1 message(s)"

    app.dependency_overrides.pop(get_registry, None)


async def test_run_flow_not_found(client: TestClient) -> None:
    response = client.post(f"/api/v1/flows/{uuid.uuid4()}/run")
    assert response.status_code == 404
