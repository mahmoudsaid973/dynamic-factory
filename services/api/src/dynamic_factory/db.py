"""Database engine and session management."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from dynamic_factory.config import settings

engine = create_async_engine(settings.database_url, future=True, echo=False)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    """Declarative base for all ORM models."""


async def _get_db() -> AsyncIterator[AsyncSession]:
    """Yield an async database session."""
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


get_db = asynccontextmanager(_get_db)


async def db_dependency() -> AsyncIterator[AsyncSession]:
    """Unwrapped async generator for FastAPI Depends."""
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
