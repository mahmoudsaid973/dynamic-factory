#!/usr/bin/env python3
"""Minimal filesystem MCP server over stdio.

Implements JSON-RPC 2.0 over standard input/output with LSP-style
``Content-Length`` framing. Exposes three tools:

* ``read_file(path)`` - read a file as UTF-8 text
* ``write_file(path, content)`` - write UTF-8 text to a file
* ``list_dir(path)`` - list directory entries
"""
import json
import sys
from pathlib import Path

PROTOCOL_VERSION = "2024-11-05"


def _send(message: dict) -> None:
    data = json.dumps(message, ensure_ascii=False)
    header = f"Content-Length: {len(data.encode('utf-8'))}\r\n\r\n"
    sys.stdout.write(header + data)
    sys.stdout.flush()


def _read() -> dict | None:
    header = sys.stdin.readline()
    if not header:
        return None
    if not header.startswith("Content-Length:"):
        return None
    length = int(header.split(":", 1)[1].strip())
    sys.stdin.readline()  # blank separator
    body = sys.stdin.read(length)
    return json.loads(body)


def _tool_result(text: str, is_error: bool = False) -> dict:
    return {"content": [{"type": "text", "text": text}], "isError": is_error}


def _handle(request: dict) -> dict:
    method = request.get("method")
    params = request.get("params", {})

    if method == "initialize":
        return {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "filesystem", "version": "0.1.0"},
        }

    if method == "tools/list":
        return {
            "tools": [
                {
                    "name": "read_file",
                    "description": "Read a file as UTF-8 text.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {"path": {"type": "string"}},
                        "required": ["path"],
                    },
                },
                {
                    "name": "write_file",
                    "description": "Write UTF-8 text to a file.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string"},
                            "content": {"type": "string"},
                        },
                        "required": ["path", "content"],
                    },
                },
                {
                    "name": "list_dir",
                    "description": "List directory entries.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {"path": {"type": "string"}},
                        "required": ["path"],
                    },
                },
            ]
        }

    if method == "tools/call":
        name = params.get("name")
        arguments = params.get("arguments", {})
        path = Path(arguments.get("path", "")).resolve()
        try:
            if name == "read_file":
                return _tool_result(path.read_text(encoding="utf-8"))
            if name == "write_file":
                path.write_text(arguments.get("content", ""), encoding="utf-8")
                return _tool_result("ok")
            if name == "list_dir":
                entries = sorted(entry.name for entry in path.iterdir())
                return _tool_result(json.dumps(entries))
        except FileNotFoundError:
            return _tool_result(f"not found: {path}", is_error=True)
        except PermissionError:
            return _tool_result(f"permission denied: {path}", is_error=True)
        except Exception as exc:  # noqa: BLE001
            return _tool_result(str(exc), is_error=True)
        return _tool_result(f"unknown tool: {name}", is_error=True)

    return {"error": {"code": -32601, "message": f"method not found: {method}"}}


def main() -> None:
    while True:
        request = _read()
        if request is None:
            break
        response = {"jsonrpc": "2.0", "id": request.get("id"), "result": _handle(request)}
        _send(response)


if __name__ == "__main__":
    main()
