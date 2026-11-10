"""Shared test fixtures."""

import os
import uuid
from collections.abc import AsyncIterator, Iterator

os.environ.setdefault("APP_ENV", "test")
os.environ.setdefault("SECRET_KEY", "test-secret-key-for-encryption")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from dynamic_factory.db import Base, get_db
from dynamic_factory.main import app


@pytest.fixture
async def db_session() -> AsyncIterator[AsyncSession]:
    """Create a fresh SQLite database and yield an async session."""
    db_path = f"./test_{uuid.uuid4().hex}.db"
    engine = create_async_engine(f"sqlite+aiosqlite:///{db_path}", future=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with session_factory() as session:
        yield session

    await engine.dispose()
    os.remove(db_path)


@pytest.fixture
def client(db_session: AsyncSession) -> Iterator[TestClient]:
    """Build a TestClient using the test database session."""

    def override_get_db() -> Iterator[AsyncSession]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.pop(get_db, None)
