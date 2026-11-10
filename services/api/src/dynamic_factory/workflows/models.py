"""Workflow ORM models with immutable versioning."""
from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import JSON, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from dynamic_factory.db import Base

if TYPE_CHECKING:
    from dynamic_factory.projects.models import ProjectWorkflowBinding
    from dynamic_factory.runs.models import Run


class Workflow(Base):
    """A user-defined workflow graph (editable draft)."""

    __tablename__ = "workflows"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    config: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    is_template: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    nodes: Mapped[list["Node"]] = relationship(
        back_populates="workflow",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    edges: Mapped[list["Edge"]] = relationship(
        back_populates="workflow",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    versions: Mapped[list["WorkflowVersion"]] = relationship(
        back_populates="workflow",
        cascade="all, delete-orphan",
        lazy="selectin",
        order_by="WorkflowVersion.version_number.desc()",
    )


class WorkflowVersion(Base):
    """Immutable published snapshot of a workflow graph."""

    __tablename__ = "workflow_versions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    workflow_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("workflows.id", ondelete="CASCADE"),
        nullable=False,
    )
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    graph: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    published_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))

    workflow: Mapped["Workflow"] = relationship(back_populates="versions")
    bindings: Mapped[list["ProjectWorkflowBinding"]] = relationship(
        back_populates="workflow_version",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    runs: Mapped[list["Run"]] = relationship(
        back_populates="workflow_version",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class Node(Base):
    """A single node inside a workflow draft."""

    __tablename__ = "nodes"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    workflow_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("workflows.id", ondelete="CASCADE"),
        nullable=False,
    )
    kind: Mapped[str] = mapped_column(String(64), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    config: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)

    workflow: Mapped["Workflow"] = relationship(back_populates="nodes")


class Edge(Base):
    """A directed edge between two nodes in a workflow draft."""

    __tablename__ = "edges"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    workflow_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("workflows.id", ondelete="CASCADE"),
        nullable=False,
    )
    source_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("nodes.id", ondelete="CASCADE"),
        nullable=False,
    )
    target_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("nodes.id", ondelete="CASCADE"),
        nullable=False,
    )

    workflow: Mapped["Workflow"] = relationship(back_populates="edges")
