"""Workflow versioning REST endpoint integration tests."""

import uuid

import pytest
from fastapi.testclient import TestClient

pytestmark = pytest.mark.asyncio


async def test_create_workflow(client: TestClient) -> None:
    payload = {
        "name": "versioned-wf",
        "description": "has versions",
        "nodes": [],
        "edges": [],
    }
    response = client.post("/api/v1/workflows/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "versioned-wf"
    assert "id" in data


async def test_publish_workflow_version(client: TestClient) -> None:
    create = client.post("/api/v1/workflows/", json={"name": "pub", "nodes": [], "edges": []})
    workflow_id = create.json()["id"]

    response = client.post(
        f"/api/v1/workflows/{workflow_id}/versions",
        json={"graph": {"nodes": {"n1": {"kind": "noop"}}, "edges": []}},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["version_number"] == 1
    assert data["workflow_id"] == workflow_id
    assert data["graph"]["nodes"]["n1"]["kind"] == "noop"


async def test_list_workflow_versions(client: TestClient) -> None:
    create = client.post("/api/v1/workflows/", json={"name": "multi", "nodes": [], "edges": []})
    workflow_id = create.json()["id"]

    client.post(f"/api/v1/workflows/{workflow_id}/versions", json={"graph": {}})
    client.post(f"/api/v1/workflows/{workflow_id}/versions", json={"graph": {}})

    response = client.get(f"/api/v1/workflows/{workflow_id}/versions")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["version_number"] == 2


async def test_get_workflow_version(client: TestClient) -> None:
    create = client.post("/api/v1/workflows/", json={"name": "getv", "nodes": [], "edges": []})
    workflow_id = create.json()["id"]

    version = client.post(f"/api/v1/workflows/{workflow_id}/versions", json={"graph": {}})
    version_id = version.json()["id"]

    response = client.get(f"/api/v1/workflows/{workflow_id}/versions/{version_id}")
    assert response.status_code == 200
    assert response.json()["id"] == version_id


async def test_workflow_not_found(client: TestClient) -> None:
    response = client.post(f"/api/v1/workflows/{uuid.uuid4()}/versions", json={"graph": {}})
    assert response.status_code == 404


async def test_old_flow_endpoint_still_works(client: TestClient) -> None:
    payload = {
        "name": "legacy-flow",
        "nodes": [{"kind": "prompt", "name": "greeting", "config": {}}],
        "edges": [],
    }
    response = client.post("/api/v1/flows/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "legacy-flow"
    assert len(data["nodes"]) == 1
