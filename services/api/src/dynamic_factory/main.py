"""Dynamic Factory FastAPI application."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import model modules to register all tables with SQLAlchemy metadata.
from dynamic_factory.allowance import models as _allowance_models  # noqa: F401
from dynamic_factory.allowance.routes import router as allowance_router
from dynamic_factory.bridge import models as _bridge_models  # noqa: F401
from dynamic_factory.bridge.routes import router as bridge_router
from dynamic_factory.config import settings
from dynamic_factory.connectors import models as _connectors_models  # noqa: F401
from dynamic_factory.connectors.routes import router as connectors_router
from dynamic_factory.db import Base, engine
from dynamic_factory.events import models as _events_models  # noqa: F401
from dynamic_factory.events.routes import router as events_router
from dynamic_factory.projects import models as _projects_models  # noqa: F401
from dynamic_factory.projects.routes import router as projects_router
from dynamic_factory.providers.routes import router as providers_router
from dynamic_factory.runs import models as _runs_models  # noqa: F401
from dynamic_factory.runs.routes import router as runs_router
from dynamic_factory.workflows.routes import legacy_router as workflows_legacy_router
from dynamic_factory.workflows.routes import router as workflows_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
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
app.include_router(workflows_router)
app.include_router(workflows_legacy_router)
app.include_router(projects_router)
app.include_router(runs_router)
app.include_router(bridge_router)
app.include_router(events_router)
app.include_router(allowance_router)
app.include_router(connectors_router)


@app.get("/health")
async def health() -> dict[str, str]:
    """Simple health check."""
    return {"status": "ok"}
