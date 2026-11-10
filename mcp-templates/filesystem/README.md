# Filesystem MCP Bridge

A minimal Model Context Protocol (MCP) server that exposes filesystem tools over stdio.

## Tools

| Tool | Arguments | Description |
|---|---|---|
| `read_file` | `path` | Read a file as UTF-8 text. |
| `write_file` | `path`, `content` | Write UTF-8 text to a file. |
| `list_dir` | `path` | List directory entries. |

## Usage

Run the server directly with Python 3.12+:

```bash
python mcp-templates/filesystem/server.py
```

The server speaks JSON-RPC 2.0 over stdio using LSP-style `Content-Length` framing.

## Configure in Dynamic Factory

Use an `mcp` node with a `command` pointing at this server:

```json
{
  "id": "mcp-1",
  "type": "mcp",
  "config": {
    "command": ["python", "mcp-templates/filesystem/server.py"],
    "operation": "read_file",
    "path": "services/api/pyproject.toml"
  }
}
```

Supported `operation` values are `read_file`, `write_file`, and `list_dir`.
When using `write_file`, also provide a `content` field in `config`.

## Testing

The API test suite spins up this server in a temporary directory:

```bash
cd services/api
uv run pytest tests/test_mcp_node.py -v
```
