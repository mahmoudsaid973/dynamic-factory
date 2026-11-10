"""Workflow engine unit tests."""

import uuid
from typing import Any

import pytest

from dynamic_factory.providers.client import ProviderClient
from dynamic_factory.providers.registry import ProviderRegistry
from dynamic_factory.workflows.engine.executor import execute_workflow
from dynamic_factory.workflows.models import Edge, Node, Workflow

pytestmark = pytest.mark.asyncio


class FakeClient(ProviderClient):
    """Test double that echoes back message metadata."""

    def __init__(self, model: str = "fake-model") -> None:
        self.model = model

    async def chat(
        self,
        messages: list[dict[str, str]],
        model: str | None = None,
        **kwargs: Any,
    ) -> str:
        return f"model={model or self.model}, count={len(messages)}"


def _build_workflow(nodes: list[Node], edges: list[Edge]) -> Workflow:
    return Workflow(id=uuid.uuid4(), name="test", nodes=nodes, edges=edges)


async def test_topological_execution_order() -> None:
    a = Node(id=uuid.uuid4(), kind="prompt", name="a", config={"template": "A"})
    b = Node(
        id=uuid.uuid4(),
        kind="prompt",
        name="b",
        config={"template": "$a", "inputs": {"a": str(a.id)}},
    )
    edge = Edge(id=uuid.uuid4(), source_id=a.id, target_id=b.id, workflow_id=uuid.uuid4())

    workflow = _build_workflow([b, a], [edge])
    outputs = await execute_workflow(workflow, ProviderRegistry())

    assert outputs[a.id] == "A"
    assert outputs[b.id] == "A"


async def test_prompt_node_with_inputs() -> None:
    source = Node(id=uuid.uuid4(), kind="prompt", name="source", config={"template": "World"})
    target = Node(
        id=uuid.uuid4(),
        kind="prompt",
        name="target",
        config={
            "template": "Hello $name",
            "inputs": {"name": str(source.id)},
        },
    )
    edge = Edge(
        id=uuid.uuid4(),
        source_id=source.id,
        target_id=target.id,
        workflow_id=uuid.uuid4(),
    )

    workflow = _build_workflow([source, target], [edge])
    outputs = await execute_workflow(workflow, ProviderRegistry())

    assert outputs[source.id] == "World"
    assert outputs[target.id] == "Hello World"


async def test_llm_node_calls_provider() -> None:
    provider_id = uuid.uuid4()
    prompt = Node(id=uuid.uuid4(), kind="prompt", name="prompt", config={"template": "Hi"})
    llm = Node(
        id=uuid.uuid4(),
        kind="llm",
        name="llm",
        config={"provider_id": str(provider_id), "model": "test-model"},
    )
    edge = Edge(id=uuid.uuid4(), source_id=prompt.id, target_id=llm.id, workflow_id=uuid.uuid4())

    registry = ProviderRegistry()
    registry._clients[provider_id] = FakeClient()

    workflow = _build_workflow([prompt, llm], [edge])
    outputs = await execute_workflow(workflow, registry)

    assert outputs[prompt.id] == "Hi"
    assert outputs[llm.id] == "model=test-model, count=1"


async def test_cycle_detection() -> None:
    a = Node(id=uuid.uuid4(), kind="prompt", name="a", config={"template": "A"})
    b = Node(id=uuid.uuid4(), kind="prompt", name="b", config={"template": "B"})
    edges = [
        Edge(id=uuid.uuid4(), source_id=a.id, target_id=b.id, workflow_id=uuid.uuid4()),
        Edge(id=uuid.uuid4(), source_id=b.id, target_id=a.id, workflow_id=uuid.uuid4()),
    ]

    workflow = _build_workflow([a, b], edges)
    with pytest.raises(ValueError, match="cycle"):
        await execute_workflow(workflow, ProviderRegistry())
