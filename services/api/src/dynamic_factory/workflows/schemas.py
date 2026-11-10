"""Workflow Pydantic schemas."""

import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class NodeCreate(BaseModel):
    """Payload to create a workflow node."""

    id: uuid.UUID | None = None
    kind: str
    name: str
    config: dict[str, Any] | None = None


class EdgeCreate(BaseModel):
    """Payload to create a workflow edge."""

    source_id: uuid.UUID
    target_id: uuid.UUID


class WorkflowCreate(BaseModel):
    """Payload to create a workflow."""

    name: str
    description: str | None = None
    nodes: list[NodeCreate] = Field(default_factory=list)
    edges: list[EdgeCreate] = Field(default_factory=list)
    config: dict[str, Any] | None = None


class NodeRead(BaseModel):
    """Public node representation."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    kind: str
    name: str
    config: dict[str, Any] | None = None


class EdgeRead(BaseModel):
    """Public edge representation."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    source_id: uuid.UUID
    target_id: uuid.UUID


class WorkflowRead(BaseModel):
    """Public workflow representation."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    description: str | None = None
    config: dict[str, Any] | None = None
    is_template: bool
    created_at: datetime
    updated_at: datetime
    nodes: list[NodeRead]
    edges: list[EdgeRead]


class WorkflowVersionCreate(BaseModel):
    """Payload to publish a workflow version from an explicit graph."""

    graph: dict[str, Any]


class WorkflowVersionRead(BaseModel):
    """Public workflow version representation."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    workflow_id: uuid.UUID
    version_number: int
    graph: dict[str, Any]
    published_at: datetime


class WorkflowRunResponse(BaseModel):
    """Result of executing a workflow."""

    run_id: uuid.UUID
    workflow_id: uuid.UUID
    status: str
    outputs: dict[str, Any]
