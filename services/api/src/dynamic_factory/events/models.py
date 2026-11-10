"""Event and evidence ORM models."""
from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import JSON, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from dynamic_factory.db import Base

if TYPE_CHECKING:
    from dynamic_factory.runs.models import Attempt, Invocation, Run


class Event(Base):
    """Durable event for a run, invocation or attempt."""

    __tablename__ = "events"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    run_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("runs.id", ondelete="CASCADE"),
        nullable=False,
    )
    invocation_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("invocations.id", ondelete="CASCADE"),
        nullable=True,
    )
    attempt_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("attempts.id", ondelete="CASCADE"),
        nullable=True,
    )
    level: Mapped[str] = mapped_column(String(16), nullable=False)
    kind: Mapped[str] = mapped_column(String(64), nullable=False)
    payload: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))

    run: Mapped["Run"] = relationship(back_populates="events")
    invocation: Mapped["Invocation"] = relationship()
    attempt: Mapped["Attempt"] = relationship(back_populates="events")


class Evidence(Base):
    """Sanitized artifact produced by an execution."""

    __tablename__ = "evidence"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    run_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("runs.id", ondelete="CASCADE"),
        nullable=False,
    )
    invocation_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("invocations.id", ondelete="CASCADE"),
        nullable=True,
    )
    kind: Mapped[str] = mapped_column(String(64), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    mime_type: Mapped[str | None] = mapped_column(String(255), nullable=True)
    storage_key: Mapped[str] = mapped_column(String(512), nullable=False)
    size_bytes: Mapped[int | None] = mapped_column(nullable=True)
    artifact_metadata: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))

    run: Mapped["Run"] = relationship()
    invocation: Mapped["Invocation"] = relationship()
