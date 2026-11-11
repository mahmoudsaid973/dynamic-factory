"""Durable run orchestrator that executes a workflow version graph."""

import uuid
from collections import deque
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from dynamic_factory.events.models import Event
from dynamic_factory.providers.registry import ProviderRegistry
from dynamic_factory.runs.models import Attempt, Invocation, Run
from dynamic_factory.workflows.engine.nodes import execute_node
from dynamic_factory.workflows.models import WorkflowVersion


@dataclass
class _GraphNode:
    """Lightweight node view used during durable execution."""

    id: uuid.UUID
    kind: str
    config: dict[str, Any] | None


@dataclass
class _GraphEdge:
    """Lightweight edge view used during durable execution."""

    source_id: uuid.UUID
    target_id: uuid.UUID


def _parse_graph(graph: dict[str, Any]) -> tuple[list[_GraphNode], list[_GraphEdge]]:
    """Parse a workflow version graph dict into node/edge views."""
    nodes: list[_GraphNode] = []
    raw_nodes = graph.get("nodes", {})
    if isinstance(raw_nodes, dict):
        for node_id, node_data in raw_nodes.items():
            data = node_data or {}
            nodes.append(
                _GraphNode(
                    id=uuid.UUID(node_id),
                    kind=data.get("kind", "noop"),
                    config=data.get("config"),
                )
            )
    elif isinstance(raw_nodes, list):
        for item in raw_nodes:
            nodes.append(
                _GraphNode(
                    id=uuid.UUID(item["id"]),
                    kind=item.get("kind", "noop"),
                    config=item.get("config"),
                )
            )

    edges: list[_GraphEdge] = []
    raw_edges = graph.get("edges", {})
    if isinstance(raw_edges, dict):
        for _edge_id, edge_data in raw_edges.items():
            data = edge_data or {}
            edges.append(
                _GraphEdge(
                    source_id=uuid.UUID(data["source_id"]),
                    target_id=uuid.UUID(data["target_id"]),
                )
            )
    elif isinstance(raw_edges, list):
        for item in raw_edges:
            edges.append(
                _GraphEdge(
                    source_id=uuid.UUID(item["source_id"]),
                    target_id=uuid.UUID(item["target_id"]),
                )
            )

    return nodes, edges


def _topological_order(
    node_ids: list[uuid.UUID],
    edge_pairs: list[tuple[uuid.UUID, uuid.UUID]],
) -> list[uuid.UUID]:
    """Return node ids in topological order using Kahn's algorithm."""
    adjacency: dict[uuid.UUID, list[uuid.UUID]] = {node: [] for node in node_ids}
    in_degree: dict[uuid.UUID, int] = dict.fromkeys(node_ids, 0)

    for source_id, target_id in edge_pairs:
        adjacency[source_id].append(target_id)
        in_degree[target_id] += 1

    queue = deque([node for node in node_ids if in_degree[node] == 0])
    order: list[uuid.UUID] = []

    while queue:
        current = queue.popleft()
        order.append(current)
        for neighbor in adjacency[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(order) != len(node_ids):
        raise ValueError("Workflow graph contains a cycle")

    return order


async def execute_run(
    run: Run,
    version: WorkflowVersion,
    registry: ProviderRegistry,
    session: AsyncSession,
) -> Run:
    """Execute a run against an immutable workflow version graph.

    Records invocations, attempts and events. Updates ``run`` status and outputs.
    """
    nodes, edges = _parse_graph(version.graph)
    node_map = {node.id: node for node in nodes}
    node_ids = list(node_map.keys())
    edge_pairs = [(edge.source_id, edge.target_id) for edge in edges]

    run.status = "running"
    run.started_at = datetime.now(UTC)
    await session.flush()

    context: dict[uuid.UUID, str] = {}
    outputs: dict[str, Any] = {}
    failed = False

    try:
        order = _topological_order(node_ids, edge_pairs)
    except ValueError as exc:
        run.status = "failed"
        run.error = str(exc)
        run.ended_at = datetime.now(UTC)
        session.add(
            Event(
                run_id=run.id,
                level="error",
                kind="topological_sort_failed",
                payload={"error": str(exc)},
            )
        )
        await session.commit()
        return run

    for node_id in order:
        node = node_map[node_id]
        invocation = Invocation(
            run_id=run.id,
            node_id=str(node_id),
            kind=node.kind,
            status="running",
            started_at=datetime.now(UTC),
        )
        session.add(invocation)
        await session.flush()

        attempt = Attempt(
            invocation_id=invocation.id,
            attempt_number=1,
            idempotency_key=f"{run.id}:{node_id}:1",
            status="running",
            started_at=datetime.now(UTC),
        )
        session.add(attempt)
        await session.flush()

        try:
            result = await execute_node(node, context, edge_pairs, registry)
            context[node_id] = result
            outputs[str(node_id)] = result

            attempt.status = "completed"
            attempt.outputs = {"result": result}
            attempt.ended_at = datetime.now(UTC)
            invocation.status = "completed"
            invocation.outputs = {"result": result}
            invocation.ended_at = datetime.now(UTC)

            session.add(
                Event(
                    run_id=run.id,
                    invocation_id=invocation.id,
                    attempt_id=attempt.id,
                    level="info",
                    kind="node_completed",
                    payload={"node_id": str(node_id), "kind": node.kind},
                )
            )
        except Exception as exc:  # noqa: BLE001
            failed = True
            error_message = str(exc)
            attempt.status = "failed"
            attempt.error = error_message
            attempt.ended_at = datetime.now(UTC)
            invocation.status = "failed"
            invocation.error = error_message
            invocation.ended_at = datetime.now(UTC)

            session.add(
                Event(
                    run_id=run.id,
                    invocation_id=invocation.id,
                    attempt_id=attempt.id,
                    level="error",
                    kind="node_failed",
                    payload={"node_id": str(node_id), "error": error_message},
                )
            )

            # First-failure preservation: stop the run on the first node failure.
            break

    run.status = "failed" if failed else "completed"
    run.outputs = outputs
    run.ended_at = datetime.now(UTC)
    await session.commit()
    await session.refresh(run)
    return run
