"""Abstract and concrete LLM provider clients."""

from abc import ABC, abstractmethod
from typing import Any

import httpx


class ProviderClient(ABC):
    """Abstract client for an LLM provider."""

    @abstractmethod
    async def chat(
        self,
        messages: list[dict[str, str]],
        model: str | None = None,
        **kwargs: Any,
    ) -> str:
        """Send a chat request and return the response content."""


class OpenAIClient(ProviderClient):
    """OpenAI-compatible HTTP client using httpx."""

    def __init__(
        self,
        base_url: str,
        api_key: str,
        default_model: str,
        timeout: float = 60.0,
    ) -> None:
        self.default_model = default_model
        self._client = httpx.AsyncClient(
            base_url=base_url,
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=timeout,
        )

    async def chat(
        self,
        messages: list[dict[str, str]],
        model: str | None = None,
        **kwargs: Any,
    ) -> str:
        """Call the provider chat completions endpoint."""
        payload = {
            "model": model or self.default_model,
            "messages": messages,
            **kwargs,
        }
        response = await self._client.post("/chat/completions", json=payload)
        response.raise_for_status()
        data = response.json()
        return str(data["choices"][0]["message"]["content"])

    async def close(self) -> None:
        await self._client.aclose()
