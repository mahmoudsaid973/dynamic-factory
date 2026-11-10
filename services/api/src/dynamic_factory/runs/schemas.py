"""Run Pydantic schemas."""

import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class RunCreate(BaseModel):
    """Payload to start a run."""

    project_id: uuid.UUID
    workflow_version_id: uuid.UUID
    request_id: uuid.UUID | None = None
    inputs: dict[str, Any] | None = None


class RunRead(BaseModel):
    """Public run representation."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    project_id: uuid.UUID
    workflow_version_id: uuid.UUID
    request_id: uuid.UUID | None = None
    status: str
    inputs: dict[str, Any] | None = None
    outputs: dict[str, Any] | None = None
    error: str | None = None
    started_at: datetime | None = None
    ended_at: datetime | None = None
    created_at: datetime


class InvocationRead(BaseModel):
    """Public invocation representation."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    run_id: uuid.UUID
    node_id: str
    kind: str
    status: str
    inputs: dict[str, Any] | None = None
    outputs: dict[str, Any] | None = None
    error: str | None = None
    started_at: datetime | None = None
    ended_at: datetime | None = None
    created_at: datetime


class AttemptRead(BaseModel):
    """Public attempt representation."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    invocation_id: uuid.UUID
    attempt_number: int
    idempotency_key: str | None = None
    status: str
    inputs: dict[str, Any] | None = None
    outputs: dict[str, Any] | None = None
    error: str | None = None
    started_at: datetime | None = None
    ended_at: datetime | None = None
    created_at: datetime
