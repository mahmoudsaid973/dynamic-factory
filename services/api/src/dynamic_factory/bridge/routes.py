"""Bridge / JEV routing API routes."""

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dynamic_factory.bridge.models import BridgeRequest
from dynamic_factory.bridge.schemas import BridgeRequestCreate, BridgeRequestRead
from dynamic_factory.db import get_db

router = APIRouter(prefix="/api/v1/bridge", tags=["bridge"])


@router.post("/requests", response_model=BridgeRequestRead, status_code=status.HTTP_201_CREATED)
async def create_request(
    data: BridgeRequestCreate,
    session: AsyncSession = Depends(get_db),
) -> BridgeRequest:
    """Record an incoming request and return its durable id."""
    request = BridgeRequest(
        source=data.source,
        workspace_id=data.workspace_id,
        user_id=data.user_id,
        language=data.language,
        correlation_id=data.correlation_id,
        raw_input=data.raw_input,
        request_metadata=data.request_metadata,
    )
    session.add(request)
    await session.commit()
    await session.refresh(request)
    return request


@router.get("/requests", response_model=list[BridgeRequestRead])
async def list_requests(
    source: str | None = None,
    session: AsyncSession = Depends(get_db),
) -> list[BridgeRequest]:
    """List bridge requests."""
    query = select(BridgeRequest)
    if source:
        query = query.where(BridgeRequest.source == source)
    result = await session.execute(query.order_by(BridgeRequest.created_at.desc()))
    return list(result.scalars().all())


@router.get("/requests/{request_id}", response_model=BridgeRequestRead)
async def get_request(
    request_id: uuid.UUID,
    session: AsyncSession = Depends(get_db),
) -> BridgeRequest:
    """Fetch a single bridge request."""
    request = await session.get(BridgeRequest, request_id)
    if request is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")
    return request


@router.patch("/requests/{request_id}/classify", response_model=BridgeRequestRead)
async def classify_request(
    request_id: uuid.UUID,
    classification: str,
    tier: str | None = None,
    explanation: str | None = None,
    planned_workflow_id: uuid.UUID | None = None,
    session: AsyncSession = Depends(get_db),
) -> BridgeRequest:
    """Update the JEV classification of a request."""
    request = await session.get(BridgeRequest, request_id)
    if request is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")

    request.classification = classification
    request.tier = tier
    request.explanation = explanation
    request.planned_workflow_id = planned_workflow_id
    request.status = "classified"

    await session.commit()
    await session.refresh(request)
    return request
