"""Project Pydantic schemas."""

import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ProjectCreate(BaseModel):
    """Payload to create a project."""

    name: str
    description: str | None = None
    owner_id: str | None = None
    config: dict[str, Any] | None = None


class ProjectUpdate(BaseModel):
    """Payload to update a project."""

    name: str | None = None
    description: str | None = None
    config: dict[str, Any] | None = None


class ProjectRead(BaseModel):
    """Public project representation."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    description: str | None = None
    owner_id: str
    config: dict[str, Any] | None = None
    created_at: datetime
    updated_at: datetime


class ProjectWorkflowBindingCreate(BaseModel):
    """Payload to bind a workflow version to a project."""

    workflow_version_id: uuid.UUID
    inputs: dict[str, Any] | None = None
    version_policy: str = Field(default="pinned", pattern="^(pinned|latest-published)$")


class ProjectWorkflowBindingRead(BaseModel):
    """Public binding representation."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    project_id: uuid.UUID
    workflow_version_id: uuid.UUID
    inputs: dict[str, Any] | None = None
    version_policy: str
    created_at: datetime
