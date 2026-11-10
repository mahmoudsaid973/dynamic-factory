#!/usr/bin/env python3
"""Create and run a default prompt-to-LLM flow via the Dynamic Factory API."""
import argparse
import asyncio
import os
import sys

import httpx

DEFAULT_BASE_URL = os.environ.get("FACTORY_API_URL", "http://localhost:8000")
DEFAULT_PROMPT = "Explain the Dynamic Factory in one sentence."


async def create_provider(client: httpx.AsyncClient) -> str:
    """Create the default provider and return its ID."""
    payload = {
        "name": "default-openai",
        "kind": "openai-compatible",
        "base_url": os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        "model_default": os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
        "api_key": os.environ.get("OPENAI_API_KEY", ""),
    }
    response = await client.post("/api/v1/providers", json=payload)
    response.raise_for_status()
    return response.json()["id"]


async def create_flow(client: httpx.AsyncClient, provider_id: str, prompt: str) -> str:
    """Create the default flow and return its ID."""
    payload = {
        "name": "default-prompt-llm",
        "nodes": [
            {
                "id": "prompt-1",
                "type": "prompt",
                "config": {"template": prompt},
            },
            {
                "id": "llm-1",
                "type": "llm",
                "config": {
                    "provider_id": provider_id,
                    "model": os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
                },
            },
        ],
        "edges": [{"id": "e1", "source": "prompt-1", "target": "llm-1"}],
    }
    response = await client.post("/api/v1/flows", json=payload)
    response.raise_for_status()
    return response.json()["id"]


async def run_flow(client: httpx.AsyncClient, flow_id: str) -> dict:
    """Run a flow and return the run payload."""
    response = await client.post(f"/api/v1/flows/{flow_id}/run")
    response.raise_for_status()
    return response.json()


async def main(base_url: str, prompt: str) -> int:
    """Create provider, flow, and run; print the result."""
    async with httpx.AsyncClient(base_url=base_url, timeout=30) as client:
        provider_id = await create_provider(client)
        flow_id = await create_flow(client, provider_id, prompt)
        result = await run_flow(client, flow_id)

    print(result)
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create and run a default factory flow.")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--prompt", default=DEFAULT_PROMPT)
    args = parser.parse_args()
    sys.exit(asyncio.run(main(args.base_url, args.prompt)))
