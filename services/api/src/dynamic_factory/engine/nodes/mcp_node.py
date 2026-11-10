"""Node that delegates file operations to an MCP stdio server."""
from dynamic_factory.engine.nodes.base import BaseNode
from dynamic_factory.mcp.client import MCPStdioClient


class MCPNode(BaseNode):
    """Execute filesystem operations through a configured MCP server."""

    async def execute(self, context: dict) -> dict:
        """Run the configured MCP tool and return its text output."""
        cfg = self.node.config
        command = cfg.get("command")
        if not command:
            raise ValueError("MCP node requires a 'command' config")

        operation = cfg.get("operation")
        path = cfg.get("path")
        content = cfg.get("content")

        async with MCPStdioClient(command) as client:
            if operation == "list_dir":
                response = await client.call_tool("list_dir", {"path": path})
            elif operation == "read_file":
                response = await client.call_tool("read_file", {"path": path})
            elif operation == "write_file":
                response = await client.call_tool(
                    "write_file",
                    {"path": path, "content": content},
                )
            else:
                raise ValueError(f"unsupported MCP operation: {operation}")

        result = response.get("result", {})
        if result.get("isError"):
            text = result.get("content", [{}])[0].get("text", "unknown error")
            raise RuntimeError(text)
        return {"output": result.get("content", [{}])[0].get("text", "")}
