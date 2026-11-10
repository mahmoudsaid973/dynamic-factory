"""Workflow Pydantic schemas."""

import uuid
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
    nodes: list[NodeRead]
    edges: list[EdgeRead]
    config: dict[str, Any] | None = None


class WorkflowRunResponse(BaseModel):
    """Result of executing a workflow."""

    outputs: dict[str, str]
