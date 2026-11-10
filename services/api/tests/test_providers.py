"""Provider endpoint and encryption tests."""

import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from dynamic_factory.providers.models import Provider
from dynamic_factory.providers.security import decrypt_secret

pytestmark = pytest.mark.asyncio


async def test_create_provider(client: TestClient, db_session: AsyncSession) -> None:
    payload = {
        "name": "OpenAI",
        "kind": "openai",
        "base_url": "https://api.openai.com/v1",
        "api_key": "sk-test-secret",
        "model_default": "gpt-4o-mini",
        "config": {"temperature": 0.7},
    }
    response = client.post("/api/v1/providers/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "OpenAI"
    assert data["kind"] == "openai"
    assert "api_key" not in data

    provider = await db_session.get(Provider, uuid.UUID(data["id"]))
    assert provider is not None
    assert decrypt_secret(provider.encrypted_api_key) == "sk-test-secret"


async def test_list_providers(client: TestClient, db_session: AsyncSession) -> None:
    for name in ("OpenAI", "Anthropic"):
        db_session.add(
            Provider(
                name=name,
                kind="openai" if name == "OpenAI" else "anthropic",
                base_url="https://example.com/v1",
                encrypted_api_key="enc",
                model_default="model",
            ),
        )
    await db_session.commit()

    response = client.get("/api/v1/providers/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert {p["name"] for p in data} == {"OpenAI", "Anthropic"}


async def test_get_provider_not_found(client: TestClient) -> None:
    response = client.get(f"/api/v1/providers/{uuid.uuid4()}")
    assert response.status_code == 404
