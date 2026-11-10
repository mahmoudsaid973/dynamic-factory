"""Allowance ledger REST endpoint integration tests."""

import uuid
from datetime import UTC, datetime, timedelta

import pytest
from fastapi.testclient import TestClient

pytestmark = pytest.mark.asyncio


async def test_create_ledger(client: TestClient) -> None:
    response = client.post(
        "/api/v1/allowance/ledgers",
        json={
            "scope": "project",
            "scope_id": "proj-1",
            "window_start": datetime.now(UTC).isoformat(),
            "window_end": (datetime.now(UTC) + timedelta(days=1)).isoformat(),
            "max_units": 100,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["scope"] == "project"
    assert data["max_units"] == 100


async def test_reserve_and_release(client: TestClient) -> None:
    ledger = client.post(
        "/api/v1/allowance/ledgers",
        json={
            "scope": "user",
            "scope_id": "u1",
            "window_start": datetime.now(UTC).isoformat(),
            "window_end": (datetime.now(UTC) + timedelta(days=1)).isoformat(),
            "max_units": 10,
        },
    )
    ledger_id = ledger.json()["id"]

    reserve = client.post(
        f"/api/v1/allowance/ledgers/{ledger_id}/reserve",
        json={"ledger_id": ledger_id, "units": 4},
    )
    assert reserve.status_code == 201
    reservation_id = reserve.json()["id"]

    ledger_after = client.get(f"/api/v1/allowance/ledgers/{ledger_id}")
    assert ledger_after.json()["reserved_units"] == 4

    release = client.post(f"/api/v1/allowance/reservations/{reservation_id}/release")
    assert release.status_code == 200
    assert release.json()["status"] == "released"

    ledger_final = client.get(f"/api/v1/allowance/ledgers/{ledger_id}")
    assert ledger_final.json()["reserved_units"] == 0


async def test_over_reserve_fails(client: TestClient) -> None:
    ledger = client.post(
        "/api/v1/allowance/ledgers",
        json={
            "scope": "user",
            "scope_id": "u2",
            "window_start": datetime.now(UTC).isoformat(),
            "window_end": (datetime.now(UTC) + timedelta(days=1)).isoformat(),
            "max_units": 5,
        },
    )
    ledger_id = ledger.json()["id"]

    response = client.post(
        f"/api/v1/allowance/ledgers/{ledger_id}/reserve",
        json={"ledger_id": ledger_id, "units": 10},
    )
    assert response.status_code == 422


async def test_ledger_not_found(client: TestClient) -> None:
    response = client.get(f"/api/v1/allowance/ledgers/{uuid.uuid4()}")
    assert response.status_code == 404
