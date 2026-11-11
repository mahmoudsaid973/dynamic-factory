"""Provider REST endpoints."""

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dynamic_factory.db import db_dependency
from dynamic_factory.providers.models import Provider
from dynamic_factory.providers.registry import ProviderRegistry
from dynamic_factory.providers.schemas import ProviderCreate, ProviderRead
from dynamic_factory.providers.security import encrypt_secret

router = APIRouter(prefix="/api/v1/providers", tags=["providers"])


async def get_registry(session: AsyncSession = Depends(db_dependency)) -> ProviderRegistry:
    """Dependency that loads the provider registry from the database."""
    return await ProviderRegistry().load(session)


@router.get("/", response_model=list[ProviderRead])
async def list_providers(session: AsyncSession = Depends(db_dependency)) -> list[Provider]:
    """Return all configured providers."""
    result = await session.execute(select(Provider))
    return list(result.scalars().all())


@router.post("/", response_model=ProviderRead, status_code=status.HTTP_201_CREATED)
async def create_provider(
    payload: ProviderCreate,
    session: AsyncSession = Depends(db_dependency),
) -> Provider:
    """Create a new provider with an encrypted API key."""
    provider = Provider(
        name=payload.name,
        kind=payload.kind,
        base_url=payload.base_url,
        encrypted_api_key=encrypt_secret(payload.api_key),
        model_default=payload.model_default,
        config=payload.config,
    )
    session.add(provider)
    await session.commit()
    await session.refresh(provider)
    return provider


@router.get("/{provider_id}", response_model=ProviderRead)
async def get_provider(
    provider_id: uuid.UUID,
    session: AsyncSession = Depends(db_dependency),
) -> Provider:
    """Return a single provider by id."""
    provider = await session.get(Provider, provider_id)
    if provider is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Provider not found")
    return provider
