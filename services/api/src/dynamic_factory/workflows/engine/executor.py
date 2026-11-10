"""In-memory async workflow executor."""

import uuid
from collections import deque

from dynamic_factory.providers.registry import ProviderRegistry
from dynamic_factory.workflows.engine.nodes import execute_node
from dynamic_factory.workflows.models import Workflow


def _topological_order(
    nodes: list[uuid.UUID],
    edges: list[tuple[uuid.UUID, uuid.UUID]],
) -> list[uuid.UUID]:
    """Return node ids in topological order using Kahn's algorithm."""
    adjacency: dict[uuid.UUID, list[uuid.UUID]] = {node: [] for node in nodes}
    in_degree: dict[uuid.UUID, int] = dict.fromkeys(nodes, 0)

    for source_id, target_id in edges:
        adjacency[source_id].append(target_id)
        in_degree[target_id] += 1

    queue = deque([node for node in nodes if in_degree[node] == 0])
    order: list[uuid.UUID] = []

    while queue:
        current = queue.popleft()
        order.append(current)
        for neighbor in adjacency[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(order) != len(nodes):
        raise ValueError("Workflow contains a cycle")

    return order


async def execute_workflow(
    workflow: Workflow,
    registry: ProviderRegistry,
) -> dict[uuid.UUID, str]:
    """Execute a workflow and return the output of every node."""
    node_ids = [node.id for node in workflow.nodes]
    edge_pairs = [(edge.source_id, edge.target_id) for edge in workflow.edges]
    node_map = {node.id: node for node in workflow.nodes}

    order = _topological_order(node_ids, edge_pairs)
    context: dict[uuid.UUID, str] = {}

    for node_id in order:
        context[node_id] = await execute_node(
            node_map[node_id],
            context,
            edge_pairs,
            registry,
        )

    return context
