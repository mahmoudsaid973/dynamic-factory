"""Connector registry REST endpoint integration tests."""

import uuid

import pytest
from fastapi.testclient import TestClient

pytestmark = pytest.mark.asyncio


async def test_create_connector(client: TestClient) -> None:
    response = client.post(
        "/api/v1/connectors/",
        json={
            "name": "slack-bot",
            "kind": "mcp",
            "transport": "stdio",
            "command": {"binary": "npx", "args": ["-y", "@modelcontextprotocol/server-slack"]},
            "capabilities": ["chat.postMessage"],
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "slack-bot"
    assert data["status"] == "disconnected"


async def test_update_connector(client: TestClient) -> None:
    created = client.post(
        "/api/v1/connectors/",
        json={"name": "update-me", "kind": "http", "transport": "rest"},
    )
    connector_id = created.json()["id"]

    response = client.patch(
        f"/api/v1/connectors/{connector_id}",
        json={"status": "connected", "description": "live"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "connected"
    assert data["description"] == "live"


async def test_delete_connector(client: TestClient) -> None:
    created = client.post(
        "/api/v1/connectors/",
        json={"name": "delete-me", "kind": "http", "transport": "rest"},
    )
    connector_id = created.json()["id"]

    response = client.delete(f"/api/v1/connectors/{connector_id}")
    assert response.status_code == 204
    assert client.get(f"/api/v1/connectors/{connector_id}").status_code == 404


async def test_connector_not_found(client: TestClient) -> None:
    response = client.get(f"/api/v1/connectors/{uuid.uuid4()}")
    assert response.status_code == 404
