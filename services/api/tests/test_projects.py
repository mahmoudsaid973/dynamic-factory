"""Project REST endpoint integration tests."""

import uuid

import pytest
from fastapi.testclient import TestClient

pytestmark = pytest.mark.asyncio


async def test_create_project(client: TestClient) -> None:
    payload = {
        "name": "test-project",
        "description": "integration test",
        "owner_id": "owner-1",
        "config": {"theme": "dark"},
    }
    response = client.post("/api/v1/projects/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "test-project"
    assert data["owner_id"] == "owner-1"
    assert "id" in data


async def test_list_projects(client: TestClient) -> None:
    client.post("/api/v1/projects/", json={"name": "p1", "owner_id": "o1"})
    client.post("/api/v1/projects/", json={"name": "p2", "owner_id": "o2"})

    response = client.get("/api/v1/projects/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    names = {p["name"] for p in data}
    assert {"p1", "p2"}.issubset(names)


async def test_get_project(client: TestClient) -> None:
    create = client.post("/api/v1/projects/", json={"name": "get-me", "owner_id": "o1"})
    project_id = create.json()["id"]

    response = client.get(f"/api/v1/projects/{project_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "get-me"


async def test_update_project(client: TestClient) -> None:
    create = client.post("/api/v1/projects/", json={"name": "old", "owner_id": "o1"})
    project_id = create.json()["id"]

    response = client.patch(
        f"/api/v1/projects/{project_id}",
        json={"name": "new", "description": "updated"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "new"
    assert data["description"] == "updated"


async def test_delete_project(client: TestClient) -> None:
    create = client.post("/api/v1/projects/", json={"name": "delete-me", "owner_id": "o1"})
    project_id = create.json()["id"]

    response = client.delete(f"/api/v1/projects/{project_id}")
    assert response.status_code == 204
    assert client.get(f"/api/v1/projects/{project_id}").status_code == 404


async def test_bind_workflow_version_to_project(client: TestClient) -> None:
    workflow = client.post(
        "/api/v1/workflows/",
        json={"name": "wf", "nodes": [], "edges": []},
    )
    workflow_id = workflow.json()["id"]

    version = client.post(
        f"/api/v1/workflows/{workflow_id}/versions",
        json={"graph": {"nodes": {}, "edges": {}}},
    )
    version_id = version.json()["id"]

    project = client.post("/api/v1/projects/", json={"name": "bound", "owner_id": "o1"})
    project_id = project.json()["id"]

    bind = client.post(
        f"/api/v1/projects/{project_id}/bindings",
        json={"workflow_version_id": version_id, "version_policy": "pinned"},
    )
    assert bind.status_code == 201
    data = bind.json()
    assert data["project_id"] == project_id
    assert data["workflow_version_id"] == version_id
    assert data["version_policy"] == "pinned"


async def test_get_project_not_found(client: TestClient) -> None:
    response = client.get(f"/api/v1/projects/{uuid.uuid4()}")
    assert response.status_code == 404
