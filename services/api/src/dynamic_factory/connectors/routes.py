"""Connector registry API routes."""

import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dynamic_factory.connectors.models import Connector
from dynamic_factory.connectors.schemas import ConnectorCreate, ConnectorRead, ConnectorUpdate
from dynamic_factory.db import get_db

router = APIRouter(prefix="/api/v1/connectors", tags=["connectors"])


@router.post("/", response_model=ConnectorRead, status_code=status.HTTP_201_CREATED)
async def create_connector(
    data: ConnectorCreate,
    session: AsyncSession = Depends(get_db),
) -> Connector:
    """Register a new connector."""
    connector = Connector(
        name=data.name,
        kind=data.kind,
        transport=data.transport,
        command=data.command,
        config=data.config,
        capabilities=data.capabilities,
        description=data.description,
    )
    session.add(connector)
    await session.commit()
    await session.refresh(connector)
    return connector


@router.get("/", response_model=list[ConnectorRead])
async def list_connectors(
    kind: str | None = None,
    session: AsyncSession = Depends(get_db),
) -> list[Connector]:
    """List registered connectors."""
    query = select(Connector)
    if kind:
        query = query.where(Connector.kind == kind)
    result = await session.execute(query.order_by(Connector.created_at.desc()))
    return list(result.scalars().all())


@router.get("/{connector_id}", response_model=ConnectorRead)
async def get_connector(
    connector_id: uuid.UUID,
    session: AsyncSession = Depends(get_db),
) -> Connector:
    """Fetch a single connector."""
    connector = await session.get(Connector, connector_id)
    if connector is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Connector not found")
    return connector


@router.patch("/{connector_id}", response_model=ConnectorRead)
async def update_connector(
    connector_id: uuid.UUID,
    data: ConnectorUpdate,
    session: AsyncSession = Depends(get_db),
) -> Connector:
    """Update a connector's configuration or status."""
    connector = await session.get(Connector, connector_id)
    if connector is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Connector not found")

    updates: dict[str, Any] = data.model_dump(exclude_unset=True)
    for key, value in updates.items():
        setattr(connector, key, value)

    await session.commit()
    await session.refresh(connector)
    return connector


@router.delete("/{connector_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_connector(
    connector_id: uuid.UUID,
    session: AsyncSession = Depends(get_db),
) -> None:
    """Remove a connector from the registry."""
    connector = await session.get(Connector, connector_id)
    if connector is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Connector not found")
    await session.delete(connector)
    await session.commit()
