"""Run API routes."""

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dynamic_factory.db import get_db
from dynamic_factory.projects.models import Project
from dynamic_factory.providers.registry import ProviderRegistry
from dynamic_factory.runs.engine import execute_run
from dynamic_factory.runs.models import Attempt, Invocation, Run
from dynamic_factory.runs.schemas import AttemptRead, InvocationRead, RunCreate, RunRead
from dynamic_factory.workflows.models import WorkflowVersion
from dynamic_factory.workflows.routes import get_registry

router = APIRouter(prefix="/api/v1/runs", tags=["runs"])


@router.post("/", response_model=RunRead, status_code=status.HTTP_201_CREATED)
async def create_run(
    data: RunCreate,
    session: AsyncSession = Depends(get_db),
) -> Run:
    """Start a durable run for a project + workflow version."""
    project = await session.get(Project, data.project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    version = await session.get(WorkflowVersion, data.workflow_version_id)
    if version is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workflow version not found",
        )

    run = Run(
        project_id=data.project_id,
        workflow_version_id=data.workflow_version_id,
        request_id=data.request_id,
        status="pending",
        inputs=data.inputs,
    )
    session.add(run)
    await session.commit()
    await session.refresh(run)
    return run


@router.get("/", response_model=list[RunRead])
async def list_runs(
    project_id: uuid.UUID | None = None,
    session: AsyncSession = Depends(get_db),
) -> list[Run]:
    """List runs, optionally filtered by project."""
    query = select(Run)
    if project_id:
        query = query.where(Run.project_id == project_id)
    result = await session.execute(query.order_by(Run.created_at.desc()))
    return list(result.scalars().all())


@router.get("/{run_id}", response_model=RunRead)
async def get_run(
    run_id: uuid.UUID,
    session: AsyncSession = Depends(get_db),
) -> Run:
    """Fetch a single run."""
    run = await session.get(Run, run_id)
    if run is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Run not found")
    return run


@router.get("/{run_id}/invocations", response_model=list[InvocationRead])
async def list_invocations(
    run_id: uuid.UUID,
    session: AsyncSession = Depends(get_db),
) -> list[Invocation]:
    """List invocations inside a run."""
    result = await session.execute(
        select(Invocation).where(Invocation.run_id == run_id).order_by(Invocation.created_at.asc())
    )
    return list(result.scalars().all())


@router.get("/{run_id}/attempts", response_model=list[AttemptRead])
async def list_attempts(
    run_id: uuid.UUID,
    session: AsyncSession = Depends(get_db),
) -> list[Attempt]:
    """List attempts inside a run."""
    result = await session.execute(
        select(Attempt)
        .join(Invocation, Attempt.invocation_id == Invocation.id)
        .where(Invocation.run_id == run_id)
        .order_by(Attempt.created_at.asc())
    )
    return list(result.scalars().all())


@router.post("/{run_id}/start", response_model=RunRead)
async def start_run(
    run_id: uuid.UUID,
    session: AsyncSession = Depends(get_db),
    registry: ProviderRegistry = Depends(get_registry),
) -> Run:
    """Execute a run against its workflow version."""
    run = await session.get(Run, run_id)
    if run is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Run not found")

    version = await session.get(WorkflowVersion, run.workflow_version_id)
    if version is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workflow version not found",
        )

    return await execute_run(run, version, registry, session)
