"""Workflow REST endpoints."""

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from dynamic_factory.db import get_db
from dynamic_factory.providers.registry import ProviderRegistry
from dynamic_factory.workflows.engine.executor import execute_workflow
from dynamic_factory.workflows.models import Edge, Node, Workflow
from dynamic_factory.workflows.schemas import (
    WorkflowCreate,
    WorkflowRead,
    WorkflowRunResponse,
)

router = APIRouter(prefix="/api/v1/flows", tags=["flows"])


async def get_registry(session: AsyncSession = Depends(get_db)) -> ProviderRegistry:
    """Dependency that loads the provider registry from the database."""
    return await ProviderRegistry().load(session)


@router.post("/", response_model=WorkflowRead, status_code=status.HTTP_201_CREATED)
async def create_flow(
    payload: WorkflowCreate,
    session: AsyncSession = Depends(get_db),
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


@router.get("/{flow_id}", response_model=WorkflowRead)
async def get_flow(
    flow_id: uuid.UUID,
    session: AsyncSession = Depends(get_db),
) -> Workflow:
    """Return a workflow by id."""
    workflow = await session.get(Workflow, flow_id)
    if workflow is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flow not found")
    return workflow


@router.post("/{flow_id}/run", response_model=WorkflowRunResponse)
async def run_flow(
    flow_id: uuid.UUID,
    session: AsyncSession = Depends(get_db),
    registry: ProviderRegistry = Depends(get_registry),
) -> WorkflowRunResponse:
    """Execute a workflow and return node outputs."""
    workflow = await session.get(Workflow, flow_id)
    if workflow is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flow not found")

    outputs = await execute_workflow(workflow, registry)
    return WorkflowRunResponse(outputs={str(k): v for k, v in outputs.items()})
