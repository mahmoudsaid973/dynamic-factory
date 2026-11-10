"""Bridge / JEV routing ORM models."""
from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from dynamic_factory.db import Base

if TYPE_CHECKING:
    from dynamic_factory.runs.models import Run


class BridgeRequest(Base):
    """An incoming user request classified by the JEV routing agent."""

    __tablename__ = "bridge_requests"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    source: Mapped[str] = mapped_column(String(32), nullable=False)
    workspace_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    user_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    language: Mapped[str] = mapped_column(String(16), nullable=False, default="en")
    correlation_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    raw_input: Mapped[str] = mapped_column(Text, nullable=False)
    classification: Mapped[str | None] = mapped_column(String(32), nullable=True)
    tier: Mapped[str | None] = mapped_column(String(16), nullable=True)
    explanation: Mapped[str | None] = mapped_column(Text, nullable=True)
    planned_workflow_id: Mapped[uuid.UUID | None] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="received",
    )
    request_metadata: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))

    runs: Mapped[list["Run"]] = relationship(
        back_populates="request",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
