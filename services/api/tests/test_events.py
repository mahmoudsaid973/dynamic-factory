"""Event and evidence REST endpoint integration tests."""

import uuid

import pytest
from fastapi.testclient import TestClient

pytestmark = pytest.mark.asyncio


async def _create_run(client: TestClient) -> str:
    project = client.post("/api/v1/projects/", json={"name": "evt-project", "owner_id": "o1"})
    project_id = project.json()["id"]
    workflow = client.post("/api/v1/workflows/", json={"name": "evt-wf", "nodes": [], "edges": []})
    workflow_id = workflow.json()["id"]
    version = client.post(f"/api/v1/workflows/{workflow_id}/versions", json={"graph": {}})
    version_id = version.json()["id"]
    run = client.post(
        "/api/v1/runs/",
        json={"project_id": project_id, "workflow_version_id": version_id},
    )
    return run.json()["id"]


async def test_create_event(client: TestClient) -> None:
    run_id = await _create_run(client)
    response = client.post(
        "/api/v1/events/",
        json={
            "run_id": run_id,
            "level": "info",
            "kind": "node_started",
            "payload": {"node": "n1"},
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["run_id"] == run_id
    assert data["level"] == "info"


async def test_list_events(client: TestClient) -> None:
    run_id = await _create_run(client)
    client.post(
        "/api/v1/events/",
        json={"run_id": run_id, "level": "info", "kind": "a"},
    )
    client.post(
        "/api/v1/events/",
        json={"run_id": run_id, "level": "error", "kind": "b"},
    )

    response = client.get(f"/api/v1/events/?run_id={run_id}")
    assert response.status_code == 200
    assert len(response.json()) == 2


async def test_create_evidence(client: TestClient) -> None:
    run_id = await _create_run(client)
    response = client.post(
        "/api/v1/events/evidence",
        json={
            "run_id": run_id,
            "kind": "log",
            "name": "build.log",
            "storage_key": "s3://bucket/build.log",
            "size_bytes": 1024,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["run_id"] == run_id
    assert data["storage_key"] == "s3://bucket/build.log"


async def test_event_run_not_found(client: TestClient) -> None:
    response = client.post(
        "/api/v1/events/",
        json={
            "run_id": str(uuid.uuid4()),
            "level": "info",
            "kind": "test",
        },
    )
    assert response.status_code == 404
