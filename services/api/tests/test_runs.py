"""Run REST endpoint integration tests."""

import uuid

import pytest
from fastapi.testclient import TestClient

pytestmark = pytest.mark.asyncio


async def test_create_run(client: TestClient) -> None:
    project = client.post("/api/v1/projects/", json={"name": "run-project", "owner_id": "o1"})
    project_id = project.json()["id"]

    workflow = client.post("/api/v1/workflows/", json={"name": "run-wf", "nodes": [], "edges": []})
    workflow_id = workflow.json()["id"]
    version = client.post(
        f"/api/v1/workflows/{workflow_id}/versions",
        json={"graph": {"nodes": {}, "edges": {}}},
    )
    version_id = version.json()["id"]

    response = client.post(
        "/api/v1/runs/",
        json={
            "project_id": project_id,
            "workflow_version_id": version_id,
            "inputs": {"query": "hello"},
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["project_id"] == project_id
    assert data["workflow_version_id"] == version_id
    assert data["status"] == "pending"


async def test_list_and_get_run(client: TestClient) -> None:
    project = client.post("/api/v1/projects/", json={"name": "run-project-2", "owner_id": "o1"})
    project_id = project.json()["id"]

    workflow = client.post(
        "/api/v1/workflows/",
        json={"name": "run-wf-2", "nodes": [], "edges": []},
    )
    workflow_id = workflow.json()["id"]
    version = client.post(f"/api/v1/workflows/{workflow_id}/versions", json={"graph": {}})
    version_id = version.json()["id"]

    created = client.post(
        "/api/v1/runs/",
        json={"project_id": project_id, "workflow_version_id": version_id},
    )
    run_id = created.json()["id"]

    response = client.get("/api/v1/runs/")
    assert response.status_code == 200
    assert any(r["id"] == run_id for r in response.json())

    response = client.get(f"/api/v1/runs/{run_id}")
    assert response.status_code == 200
    assert response.json()["id"] == run_id


async def test_start_run(client: TestClient) -> None:
    project = client.post("/api/v1/projects/", json={"name": "run-project-3", "owner_id": "o1"})
    project_id = project.json()["id"]

    workflow = client.post(
        "/api/v1/workflows/",
        json={"name": "run-wf-3", "nodes": [], "edges": []},
    )
    workflow_id = workflow.json()["id"]
    version = client.post(
        f"/api/v1/workflows/{workflow_id}/versions",
        json={
            "graph": {
                "nodes": {
                    str(uuid.uuid4()): {"kind": "noop", "config": {}},
                },
                "edges": {},
            }
        },
    )
    version_id = version.json()["id"]

    run = client.post(
        "/api/v1/runs/",
        json={"project_id": project_id, "workflow_version_id": version_id},
    )
    run_id = run.json()["id"]

    response = client.post(f"/api/v1/runs/{run_id}/start")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in {"completed", "failed"}

    invocations = client.get(f"/api/v1/runs/{run_id}/invocations")
    assert invocations.status_code == 200
    assert len(invocations.json()) >= 1

    events = client.get(f"/api/v1/events/?run_id={run_id}")
    assert events.status_code == 200
    assert len(events.json()) >= 1


async def test_run_not_found(client: TestClient) -> None:
    response = client.get(f"/api/v1/runs/{uuid.uuid4()}")
    assert response.status_code == 404
