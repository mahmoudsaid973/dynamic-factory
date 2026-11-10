"""MCP stdio client implementing JSON-RPC 2.0 with LSP-style framing."""
import asyncio
import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class MCPStdioClient:
    """Async MCP client that talks to a server over stdio."""

    def __init__(
        self,
        command: list[str],
        cwd: str | Path | None = None,
    ) -> None:
        self.command = command
        self.cwd = Path(cwd) if cwd else None
        self._proc: asyncio.subprocess.Process | None = None
        self._lock = asyncio.Lock()
        self._counter = 0

    async def __aenter__(self) -> "MCPStdioClient":
        await self.start()
        return self

    async def __aexit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        await self.stop()

    async def start(self) -> dict:
        """Start the server and perform MCP initialization."""
        self._proc = await asyncio.create_subprocess_exec(
            *self.command,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=self.cwd,
        )
        init_response = await self._request(
            "initialize",
            {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "dynamic-factory", "version": "0.1.0"},
            },
        )
        await self._notification("notifications/initialized")
        return init_response

    async def stop(self) -> None:
        """Terminate the server process."""
        if self._proc is None:
            return
        self._proc.terminate()
        try:
            await asyncio.wait_for(self._proc.wait(), timeout=5)
        except TimeoutError:
            self._proc.kill()
            await self._proc.wait()
        self._proc = None

    async def list_tools(self) -> dict:
        """Call ``tools/list`` and return the server response."""
        return await self._request("tools/list", {})

    async def call_tool(self, name: str, arguments: dict) -> dict:
        """Call ``tools/call`` for the named tool."""
        return await self._request("tools/call", {"name": name, "arguments": arguments})

    async def _request(self, method: str, params: dict) -> dict:
        async with self._lock:
            if self._proc is None or self._proc.stdin is None:
                raise RuntimeError("MCP client is not started")
            self._counter += 1
            request = {
                "jsonrpc": "2.0",
                "id": self._counter,
                "method": method,
                "params": params,
            }
            await self._write(request)
            return await self._read_response()

    async def _notification(self, method: str) -> None:
        async with self._lock:
            if self._proc is None or self._proc.stdin is None:
                raise RuntimeError("MCP client is not started")
            await self._write({"jsonrpc": "2.0", "method": method, "params": {}})

    async def _write(self, message: dict) -> None:
        data = json.dumps(message, ensure_ascii=False)
        payload = f"Content-Length: {len(data.encode('utf-8'))}\r\n\r\n{data}"
        self._proc.stdin.write(payload.encode("utf-8"))
        await self._proc.stdin.drain()

    async def _read_response(self) -> dict:
        if self._proc is None or self._proc.stdout is None:
            raise RuntimeError("MCP client is not started")
        header = await self._proc.stdout.readline()
        if not header:
            raise RuntimeError("MCP server closed stdout before returning a response")
        if not header.startswith(b"Content-Length:"):
            raise RuntimeError(f"unexpected MCP header: {header!r}")
        length = int(header.decode().split(":", 1)[1].strip())
        await self._proc.stdout.readline()  # blank separator line
        body = await self._proc.stdout.read(length)
        return json.loads(body.decode("utf-8"))
