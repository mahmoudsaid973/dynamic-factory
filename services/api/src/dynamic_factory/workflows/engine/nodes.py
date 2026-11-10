"""Executable workflow node implementations."""

import uuid
from string import Template
from typing import Any, Protocol

from dynamic_factory.providers.registry import ProviderRegistry


class _NodeLike(Protocol):
    """Duck-typed node usable by the executor."""

    id: uuid.UUID
    kind: str
    config: dict[str, Any] | None


def _upstream_outputs(
    node_id: uuid.UUID,
    context: dict[uuid.UUID, str],
    edges: list[tuple[uuid.UUID, uuid.UUID]],
) -> list[str]:
    """Collect outputs from all source nodes connected to ``node_id``."""
    return [
        context[source_id]
        for source_id, target_id in edges
        if target_id == node_id and source_id in context
    ]


async def execute_prompt_node(node: _NodeLike, context: dict[uuid.UUID, str]) -> str:
    """Render a prompt template using upstream outputs."""
    config = node.config or {}
    template = Template(config.get("template", ""))
    inputs = {
        key: context[uuid.UUID(value)]
        for key, value in (config.get("inputs") or {}).items()
    }
    return template.safe_substitute(inputs)


async def execute_llm_node(
    node: _NodeLike,
    context: dict[uuid.UUID, str],
    edges: list[tuple[uuid.UUID, uuid.UUID]],
    registry: ProviderRegistry,
) -> str:
    """Call the configured LLM provider with upstream context."""
    config = node.config or {}
    provider_id = uuid.UUID(config["provider_id"])
    client = registry.get_client(provider_id)
    if client is None:
        raise ValueError(f"Provider {provider_id} not found in registry")

    messages: list[dict[str, str]] = []
    system = config.get("system")
    if system:
        messages.append({"role": "system", "content": system})

    for output in _upstream_outputs(node.id, context, edges):
        messages.append({"role": "user", "content": output})

    return await client.chat(messages, model=config.get("model"))


async def execute_node(
    node: _NodeLike,
    context: dict[uuid.UUID, str],
    edges: list[tuple[uuid.UUID, uuid.UUID]],
    registry: ProviderRegistry,
    **kwargs: Any,
) -> str:
    """Dispatch a node to the correct handler."""
    if node.kind == "prompt":
        return await execute_prompt_node(node, context)
    if node.kind == "llm":
        return await execute_llm_node(node, context, edges, registry)
    if node.kind == "noop":
        return ""
    raise ValueError(f"Unknown node kind: {node.kind}")
