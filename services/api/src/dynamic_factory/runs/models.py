"""Durable run, invocation and attempt models."""
from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import JSON, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from dynamic_factory.db import Base

if TYPE_CHECKING:
    from dynamic_factory.bridge.models import BridgeRequest
    from dynamic_factory.events.models import Event
    from dynamic_factory.projects.models import Project
    from dynamic_factory.workflows.models import WorkflowVersion


class Run(Base):
    """A durable execution of a workflow version against a project."""

    __tablename__ = "runs"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    project_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
    )
    workflow_version_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("workflow_versions.id", ondelete="CASCADE"),
        nullable=False,
    )
    request_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("bridge_requests.id", ondelete="SET NULL"),
        nullable=True,
    )
    status: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="pending",
    )
    inputs: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    outputs: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(nullable=True)
    ended_at: Mapped[datetime | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))

    project: Mapped["Project"] = relationship(back_populates="runs")
    workflow_version: Mapped["WorkflowVersion"] = relationship(back_populates="runs")
    request: Mapped["BridgeRequest"] = relationship(back_populates="runs")
    invocations: Mapped[list["Invocation"]] = relationship(
        back_populates="run",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    events: Mapped[list["Event"]] = relationship(
        back_populates="run",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class Invocation(Base):
    """A single node or sub-workflow invocation inside a run."""

    __tablename__ = "invocations"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    run_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("runs.id", ondelete="CASCADE"),
        nullable=False,
    )
    node_id: Mapped[str] = mapped_column(String(255), nullable=False)
    kind: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="pending",
    )
    inputs: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    outputs: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(nullable=True)
    ended_at: Mapped[datetime | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))

    run: Mapped["Run"] = relationship(back_populates="invocations")
    attempts: Mapped[list["Attempt"]] = relationship(
        back_populates="invocation",
        cascade="all, delete-orphan",
        lazy="selectin",
        order_by="Attempt.attempt_number.asc()",
    )


class Attempt(Base):
    """One execution attempt of an invocation."""

    __tablename__ = "attempts"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    invocation_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("invocations.id", ondelete="CASCADE"),
        nullable=False,
    )
    attempt_number: Mapped[int] = mapped_column(Integer, nullable=False)
    idempotency_key: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="pending",
    )
    inputs: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    outputs: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(nullable=True)
    ended_at: Mapped[datetime | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))

    invocation: Mapped["Invocation"] = relationship(back_populates="attempts")
    events: Mapped[list["Event"]] = relationship(
        back_populates="attempt",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
