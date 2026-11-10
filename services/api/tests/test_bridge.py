"""Bridge / JEV routing REST endpoint integration tests."""

import uuid

import pytest
from fastapi.testclient import TestClient

pytestmark = pytest.mark.asyncio


async def test_create_bridge_request(client: TestClient) -> None:
    response = client.post(
        "/api/v1/bridge/requests",
        json={
            "source": "slack",
            "raw_input": "build a workflow",
            "user_id": "u1",
            "request_metadata": {"channel": "#ops"},
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["source"] == "slack"
    assert data["raw_input"] == "build a workflow"
    assert data["status"] == "received"


async def test_classify_bridge_request(client: TestClient) -> None:
    created = client.post(
        "/api/v1/bridge/requests",
        json={"source": "email", "raw_input": "deploy"},
    )
    request_id = created.json()["id"]

    response = client.patch(
        f"/api/v1/bridge/requests/{request_id}/classify?classification=automated&tier=p2",
    )
    assert response.status_code == 200
    data = response.json()
    assert data["classification"] == "automated"
    assert data["tier"] == "p2"
    assert data["status"] == "classified"


async def test_list_bridge_requests(client: TestClient) -> None:
    client.post("/api/v1/bridge/requests", json={"source": "api", "raw_input": "x"})
    client.post("/api/v1/bridge/requests", json={"source": "api", "raw_input": "y"})

    response = client.get("/api/v1/bridge/requests?source=api")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2


async def test_bridge_request_not_found(client: TestClient) -> None:
    response = client.get(f"/api/v1/bridge/requests/{uuid.uuid4()}")
    assert response.status_code == 404
