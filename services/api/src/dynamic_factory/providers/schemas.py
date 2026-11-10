"""Provider Pydantic schemas."""

import uuid
from typing import Any

from pydantic import BaseModel, ConfigDict


class ProviderCreate(BaseModel):
    """Payload to create a new provider."""

    name: str
    kind: str
    base_url: str
    api_key: str
    model_default: str
    config: dict[str, Any] | None = None


class ProviderRead(BaseModel):
    """Public provider representation."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    kind: str
    base_url: str
    model_default: str
    config: dict[str, Any] | None = None
