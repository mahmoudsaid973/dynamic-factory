"""Base node class for the workflow execution engine."""
from abc import ABC, abstractmethod

from dynamic_factory.models.workflow import Node


class BaseNode(ABC):
    """Abstract base for all executable node types."""

    def __init__(self, node: Node) -> None:
        self.node = node

    @abstractmethod
    async def execute(self, context: dict) -> dict:
        """Execute the node and return its output dictionary."""
        ...
