"""Bridge / JEV routing Pydantic schemas."""

import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class BridgeRequestCreate(BaseModel):
    """Payload to submit a request to the Bridge/JEV classifier."""

    source: str
    workspace_id: str | None = None
    user_id: str | None = None
    language: str = "en"
    correlation_id: str | None = None
    raw_input: str
    request_metadata: dict[str, Any] | None = None


class BridgeRequestRead(BaseModel):
    """Public bridge request representation."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    source: str
    workspace_id: str | None = None
    user_id: str | None = None
    language: str
    correlation_id: str | None = None
    raw_input: str
    classification: str | None = None
    tier: str | None = None
    explanation: str | None = None
    planned_workflow_id: uuid.UUID | None = None
    status: str
    request_metadata: dict[str, Any] | None = None
    created_at: datetime
