"""Workflow, node, and edge models used by the execution engine."""
from typing import Any

from pydantic import BaseModel, Field


class Edge(BaseModel):
    """A directed connection between two nodes."""

    id: str
    source: str
    target: str
    source_handle: str | None = None
    target_handle: str | None = None


class Node(BaseModel):
    """A single workflow node."""

    id: str
    type: str
    config: dict[str, Any] = Field(default_factory=dict)


class Workflow(BaseModel):
    """A serializable workflow definition."""

    id: str | None = None
    name: str
    nodes: list[Node]
    edges: list[Edge]
