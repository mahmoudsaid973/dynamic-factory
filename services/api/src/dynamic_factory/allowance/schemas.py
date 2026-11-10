"""Allowance Pydantic schemas."""

import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class AllowanceLedgerCreate(BaseModel):
    """Payload to create an allowance ledger."""

    scope: str
    scope_id: str
    window_start: datetime
    window_end: datetime
    max_units: int
    extra: dict[str, Any] | None = None


class AllowanceLedgerRead(BaseModel):
    """Public allowance ledger representation."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    scope: str
    scope_id: str
    window_start: datetime
    window_end: datetime
    max_units: int
    used_units: int
    reserved_units: int
    extra: dict[str, Any] | None = None
    created_at: datetime


class AllowanceReservationCreate(BaseModel):
    """Payload to reserve allowance units."""

    ledger_id: uuid.UUID
    run_id: uuid.UUID | None = None
    invocation_id: uuid.UUID | None = None
    units: int


class AllowanceReservationRead(BaseModel):
    """Public reservation representation."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    ledger_id: uuid.UUID
    run_id: uuid.UUID | None = None
    invocation_id: uuid.UUID | None = None
    units: int
    status: str
    created_at: datetime
    released_at: datetime | None = None
