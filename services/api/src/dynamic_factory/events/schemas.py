"""Event and evidence Pydantic schemas."""

import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class EventCreate(BaseModel):
    """Payload to record an event."""

    run_id: uuid.UUID
    invocation_id: uuid.UUID | None = None
    attempt_id: uuid.UUID | None = None
    level: str
    kind: str
    payload: dict[str, Any] | None = None


class EventRead(BaseModel):
    """Public event representation."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    run_id: uuid.UUID
    invocation_id: uuid.UUID | None = None
    attempt_id: uuid.UUID | None = None
    level: str
    kind: str
    payload: dict[str, Any] | None = None
    created_at: datetime


class EvidenceCreate(BaseModel):
    """Payload to register evidence."""

    run_id: uuid.UUID
    invocation_id: uuid.UUID | None = None
    kind: str
    name: str
    mime_type: str | None = None
    storage_key: str
    size_bytes: int | None = None
    artifact_metadata: dict[str, Any] | None = None


class EvidenceRead(BaseModel):
    """Public evidence representation."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    run_id: uuid.UUID
    invocation_id: uuid.UUID | None = None
    kind: str
    name: str
    mime_type: str | None = None
    storage_key: str
    size_bytes: int | None = None
    artifact_metadata: dict[str, Any] | None = None
    created_at: datetime
