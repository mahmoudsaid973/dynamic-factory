"""Dynamic Factory FastAPI application."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dynamic_factory.config import settings
from dynamic_factory.db import Base, engine
from dynamic_factory.providers.routes import router as providers_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create tables when running in development without Alembic."""
    if settings.app_env == "development":
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="Dynamic Factory API",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(providers_router)


@app.get("/health")
async def health() -> dict:
    """Simple health check."""
    return {"status": "ok"}
