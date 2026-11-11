"""Workflow REST endpoints (legacy + versioned)."""

import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from dynamic_factory.db import db_dependency
from dynamic_factory.providers.registry import ProviderRegistry
from dynamic_factory.workflows.engine.executor import execute_workflow
from dynamic_factory.workflows.models import Edge, Node, Workflow, WorkflowVersion
from dynamic_factory.workflows.schemas import (
    WorkflowCreate,
    WorkflowRead,
    WorkflowRunResponse,
    WorkflowVersionCreate,
    WorkflowVersionRead,
)

legacy_router = APIRouter(prefix="/api/v1/flows", tags=["flows"])
router = APIRouter(prefix="/api/v1/workflows", tags=["workflows"])


async def get_registry(session: AsyncSession = Depends(db_dependency)) -> ProviderRegistry:
    """Dependency that loads the provider registry from the database."""
    return await ProviderRegistry().load(session)


def _serialize_workflow(workflow: Workflow) -> dict[str, Any]:
    return {
        "id": str(workflow.id),
        "name": workflow.name,
        "description": workflow.description,
        "config": workflow.config,
        "nodes": [
            {"id": str(node.id), "kind": node.kind, "name": node.name, "config": node.config}
            for node in workflow.nodes
        ],
        "edges": [
            {
                "id": str(edge.id),
                "source_id": str(edge.source_id),
                "target_id": str(edge.target_id),
            }
            for edge in workflow.edges
        ],
    }


async def _publish_version(
    workflow_id: uuid.UUID,
    graph: dict[str, Any],
    session: AsyncSession,
) -> WorkflowVersion:
    workflow = await session.get(Workflow, workflow_id)
    if workflow is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workflow not found")

    max_version = await session.execute(
        select(func.max(WorkflowVersion.version_number)).where(
            WorkflowVersion.workflow_id == workflow_id
        )
    )
    next_version = (max_version.scalar() or 0) + 1

    version = WorkflowVersion(
        workflow_id=workflow_id,
        version_number=next_version,
        graph=graph,
    )
    session.add(version)
    await session.commit()
    await session.refresh(version)
    return version


# ---- New /api/v1/workflows routes ----


@router.post("/", response_model=WorkflowRead, status_code=status.HTTP_201_CREATED)
async def create_workflow(
    payload: WorkflowCreate,
    session: AsyncSession = Depends(db_dependency),
) -> Workflow:
    """Create a workflow with its nodes and edges."""
    workflow = Workflow(
        name=payload.name,
        description=payload.description,
        config=payload.config,
    )
    session.add(workflow)
    await session.flush()

    for node_payload in payload.nodes:
        node = Node(
            id=node_payload.id or uuid.uuid4(),
            workflow_id=workflow.id,
            kind=node_payload.kind,
            name=node_payload.name,
            config=node_payload.config,
        )
        session.add(node)

    for edge_payload in payload.edges:
        edge = Edge(
            workflow_id=workflow.id,
            source_id=edge_payload.source_id,
            target_id=edge_payload.target_id,
        )
        session.add(edge)

    await session.commit()
    await session.refresh(workflow)
    return workflow


@router.get("/{workflow_id}", response_model=WorkflowRead)
async def get_workflow(
    workflow_id: uuid.UUID,
    session: AsyncSession = Depends(db_dependency),
) -> Workflow:
    """Return a workflow by id."""
    workflow = await session.get(Workflow, workflow_id)
    if workflow is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workflow not found")
    return workflow


@router.post(
    "/{workflow_id}/versions",
    response_model=WorkflowVersionRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_workflow_version(
    workflow_id: uuid.UUID,
    payload: WorkflowVersionCreate,
    session: AsyncSession = Depends(db_dependency),
) -> WorkflowVersion:
    """Publish an explicit graph as a new immutable workflow version."""
    return await _publish_version(workflow_id, payload.graph, session)


@router.get("/{workflow_id}/versions", response_model=list[WorkflowVersionRead])
async def list_workflow_versions(
    workflow_id: uuid.UUID,
    session: AsyncSession = Depends(db_dependency),
) -> list[WorkflowVersion]:
    """Return all published versions of a workflow."""
    result = await session.execute(
        select(WorkflowVersion)
        .where(WorkflowVersion.workflow_id == workflow_id)
        .order_by(WorkflowVersion.version_number.desc())
    )
    return list(result.scalars().all())


@router.get("/{workflow_id}/versions/{version_id}", response_model=WorkflowVersionRead)
async def get_workflow_version(
    workflow_id: uuid.UUID,
    version_id: uuid.UUID,
    session: AsyncSession = Depends(db_dependency),
) -> WorkflowVersion:
    """Return a single published version."""
    version = await session.get(WorkflowVersion, version_id)
    if version is None or version.workflow_id != workflow_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Version not found")
    return version


# ---- Legacy /api/v1/flows routes (kept for backward compatibility) ----


@legacy_router.post("/", response_model=WorkflowRead, status_code=status.HTTP_201_CREATED)
async def create_flow(
    payload: WorkflowCreate,
    session: AsyncSession = Depends(db_dependency),
) -> Workflow:
    """Create a workflow with its nodes and edges (legacy prefix)."""
    return await create_workflow(payload, session)


@legacy_router.get("/{flow_id}", response_model=WorkflowRead)
async def get_flow(
    flow_id: uuid.UUID,
    session: AsyncSession = Depends(db_dependency),
) -> Workflow:
    """Return a workflow by id (legacy prefix)."""
    return await get_workflow(flow_id, session)


@legacy_router.post("/{flow_id}/publish", response_model=WorkflowVersionRead)
async def publish_flow(
    flow_id: uuid.UUID,
    session: AsyncSession = Depends(db_dependency),
) -> WorkflowVersion:
    """Publish the current draft as an immutable workflow version (legacy)."""
    workflow = await session.get(Workflow, flow_id)
    if workflow is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flow not found")

    graph = _serialize_workflow(workflow)
    return await _publish_version(flow_id, graph, session)


@legacy_router.get("/{flow_id}/versions", response_model=list[WorkflowVersionRead])
async def list_flow_versions(
    flow_id: uuid.UUID,
    session: AsyncSession = Depends(db_dependency),
) -> list[WorkflowVersion]:
    """Return all published versions of a workflow (legacy prefix)."""
    return await list_workflow_versions(flow_id, session)


@legacy_router.post("/{flow_id}/run", response_model=WorkflowRunResponse)
async def run_flow(
    flow_id: uuid.UUID,
    session: AsyncSession = Depends(db_dependency),
    registry: ProviderRegistry = Depends(get_registry),
) -> WorkflowRunResponse:
    """Execute a workflow and return node outputs (legacy prefix)."""
    workflow = await session.get(Workflow, flow_id)
    if workflow is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flow not found")

    outputs = await execute_workflow(workflow, registry)
    return WorkflowRunResponse(
        run_id=uuid.uuid4(),
        workflow_id=workflow.id,
        status="completed",
        outputs={str(k): v for k, v in outputs.items()},
    )
