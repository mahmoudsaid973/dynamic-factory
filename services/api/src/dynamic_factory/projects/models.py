"""Project ORM models."""
from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import JSON, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from dynamic_factory.db import Base

if TYPE_CHECKING:
    from dynamic_factory.runs.models import Run
    from dynamic_factory.workflows.models import WorkflowVersion


class Project(Base):
    """A user-facing project that binds workflows and tracks runs."""

    __tablename__ = "projects"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    owner_id: Mapped[str] = mapped_column(String(255), nullable=False)
    config: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    bindings: Mapped[list["ProjectWorkflowBinding"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    runs: Mapped[list["Run"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class ProjectWorkflowBinding(Base):
    """Links a project to an immutable published workflow version."""

    __tablename__ = "project_workflow_bindings"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    project_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
    )
    workflow_version_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("workflow_versions.id", ondelete="CASCADE"),
        nullable=False,
    )
    inputs: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    version_policy: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="pinned",
    )
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))

    project: Mapped["Project"] = relationship(back_populates="bindings")
    workflow_version: Mapped["WorkflowVersion"] = relationship(
        back_populates="bindings",
        lazy="selectin",
    )
