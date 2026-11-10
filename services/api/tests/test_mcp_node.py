"""Tests for the filesystem MCP bridge node."""
import sys
import tempfile
from pathlib import Path

import pytest

from dynamic_factory.engine.nodes.mcp_node import MCPNode
from dynamic_factory.models.workflow import Node


@pytest.fixture
def server_path() -> Path:
    test_file = Path(__file__).resolve()
    return test_file.parents[3] / "mcp-templates" / "filesystem" / "server.py"


@pytest.mark.asyncio
async def test_mcp_node_write_read_and_list(server_path: Path) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "hello.txt"

        write_node = Node(
            id="n1",
            type="mcp",
            config={
                "command": [sys.executable, str(server_path)],
                "operation": "write_file",
                "path": str(target),
                "content": "hello mcp",
            },
        )
        write_result = await MCPNode(write_node).execute({})
        assert write_result["output"] == "ok"
        assert target.read_text(encoding="utf-8") == "hello mcp"

        read_node = Node(
            id="n2",
            type="mcp",
            config={
                "command": [sys.executable, str(server_path)],
                "operation": "read_file",
                "path": str(target),
            },
        )
        read_result = await MCPNode(read_node).execute({})
        assert read_result["output"] == "hello mcp"

        list_node = Node(
            id="n3",
            type="mcp",
            config={
                "command": [sys.executable, str(server_path)],
                "operation": "list_dir",
                "path": tmp,
            },
        )
        list_result = await MCPNode(list_node).execute({})
        assert "hello.txt" in list_result["output"]


@pytest.mark.asyncio
async def test_mcp_node_missing_operation_raises(server_path: Path) -> None:
    node = Node(
        id="n1",
        type="mcp",
        config={"command": [sys.executable, str(server_path)], "operation": "unknown"},
    )
    with pytest.raises(ValueError, match="unsupported MCP operation"):
        await MCPNode(node).execute({})
