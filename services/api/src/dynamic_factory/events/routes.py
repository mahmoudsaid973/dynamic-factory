"""Event and evidence API routes."""

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dynamic_factory.db import db_dependency
from dynamic_factory.events.models import Event, Evidence
from dynamic_factory.events.schemas import EventCreate, EventRead, EvidenceCreate, EvidenceRead
from dynamic_factory.runs.models import Run

router = APIRouter(prefix="/api/v1/events", tags=["events"])


@router.post("/", response_model=EventRead, status_code=status.HTTP_201_CREATED)
async def create_event(
    data: EventCreate,
    session: AsyncSession = Depends(db_dependency),
) -> Event:
    """Record an event against a run/invocation/attempt."""
    run = await session.get(Run, data.run_id)
    if run is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Run not found")

    event = Event(
        run_id=data.run_id,
        invocation_id=data.invocation_id,
        attempt_id=data.attempt_id,
        level=data.level,
        kind=data.kind,
        payload=data.payload,
    )
    session.add(event)
    await session.commit()
    await session.refresh(event)
    return event


@router.get("/", response_model=list[EventRead])
async def list_events(
    run_id: uuid.UUID | None = None,
    invocation_id: uuid.UUID | None = None,
    session: AsyncSession = Depends(db_dependency),
) -> list[Event]:
    """List events, optionally filtered by run or invocation."""
    query = select(Event)
    if run_id:
        query = query.where(Event.run_id == run_id)
    if invocation_id:
        query = query.where(Event.invocation_id == invocation_id)
    result = await session.execute(query.order_by(Event.created_at.desc()))
    return list(result.scalars().all())


@router.post("/evidence", response_model=EvidenceRead, status_code=status.HTTP_201_CREATED)
async def create_evidence(
    data: EvidenceCreate,
    session: AsyncSession = Depends(db_dependency),
) -> Evidence:
    """Register a piece of evidence produced by execution."""
    run = await session.get(Run, data.run_id)
    if run is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Run not found")

    evidence = Evidence(
        run_id=data.run_id,
        invocation_id=data.invocation_id,
        kind=data.kind,
        name=data.name,
        mime_type=data.mime_type,
        storage_key=data.storage_key,
        size_bytes=data.size_bytes,
        artifact_metadata=data.artifact_metadata,
    )
    session.add(evidence)
    await session.commit()
    await session.refresh(evidence)
    return evidence


@router.get("/evidence", response_model=list[EvidenceRead])
async def list_evidence(
    run_id: uuid.UUID | None = None,
    session: AsyncSession = Depends(db_dependency),
) -> list[Evidence]:
    """List evidence, optionally filtered by run."""
    query = select(Evidence)
    if run_id:
        query = query.where(Evidence.run_id == run_id)
    result = await session.execute(query.order_by(Evidence.created_at.desc()))
    return list(result.scalars().all())
