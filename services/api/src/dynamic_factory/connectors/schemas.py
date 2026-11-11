"""Connector registry Pydantic schemas."""

import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class ConnectorCreate(BaseModel):
    """Payload to register a connector."""

    name: str
    kind: str
    transport: str
    command: dict[str, Any] | None = None
    config: dict[str, Any] | None = None
    capabilities: list[str] | None = None
    description: str | None = None


class ConnectorUpdate(BaseModel):
    """Payload to update a connector."""

    kind: str | None = None
    transport: str | None = None
    command: dict[str, Any] | None = None
    config: dict[str, Any] | None = None
    status: str | None = None
    capabilities: list[str] | None = None
    description: str | None = None


class ConnectorRead(BaseModel):
    """Public connector representation."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    kind: str
    transport: str
    command: dict[str, Any] | None = None
    config: dict[str, Any] | None = None
    status: str
    capabilities: list[str] | None = None
    description: str | None = None
    created_at: datetime
    updated_at: datetime
