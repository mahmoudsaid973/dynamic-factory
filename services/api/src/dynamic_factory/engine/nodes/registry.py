"""Node type registry."""
from dynamic_factory.engine.nodes.base import BaseNode
from dynamic_factory.engine.nodes.mcp_node import MCPNode
from dynamic_factory.models.workflow import Node as WorkflowNode

NODE_TYPES: dict[str, type[BaseNode]] = {
    "mcp": MCPNode,
}


def build_node(node: WorkflowNode) -> BaseNode:
    """Instantiate the node implementation for a workflow node."""
    implementation = NODE_TYPES.get(node.type)
    if implementation is None:
        raise ValueError(f"unknown node type: {node.type}")
    return implementation(node)
