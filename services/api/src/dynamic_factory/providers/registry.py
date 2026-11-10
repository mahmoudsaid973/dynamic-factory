"""Provider registry that materializes DB rows into clients."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dynamic_factory.providers.client import OpenAIClient, ProviderClient
from dynamic_factory.providers.models import Provider
from dynamic_factory.providers.security import decrypt_secret


class ProviderRegistry:
    """Load configured providers and vend typed clients."""

    def __init__(self) -> None:
        self._clients: dict[uuid.UUID, ProviderClient] = {}

    async def load(self, session: AsyncSession) -> "ProviderRegistry":
        """Load all providers from the database into memory."""
        result = await session.execute(select(Provider))
        for provider in result.scalars().all():
            self._clients[provider.id] = self._build_client(provider)
        return self

    def get_client(self, provider_id: uuid.UUID) -> ProviderClient | None:
        """Return the client for a provider id, if loaded."""
        return self._clients.get(provider_id)

    @staticmethod
    def _build_client(provider: Provider) -> ProviderClient:
        api_key = decrypt_secret(provider.encrypted_api_key)
        if provider.kind == "openai":
            return OpenAIClient(
                base_url=provider.base_url,
                api_key=api_key,
                default_model=provider.model_default,
            )
        raise ValueError(f"Unsupported provider kind: {provider.kind}")
