"""Project API routes."""

import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dynamic_factory.db import db_dependency
from dynamic_factory.projects.models import Project, ProjectWorkflowBinding
from dynamic_factory.projects.schemas import (
    ProjectCreate,
    ProjectRead,
    ProjectUpdate,
    ProjectWorkflowBindingCreate,
    ProjectWorkflowBindingRead,
)
from dynamic_factory.workflows.models import WorkflowVersion

router = APIRouter(prefix="/api/v1/projects", tags=["projects"])


@router.post("", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
async def create_project(
    data: ProjectCreate,
    db: AsyncSession = Depends(db_dependency),
) -> Project:
    """Create a new project for the current user."""
    project = Project(
        name=data.name,
        description=data.description,
        owner_id=data.owner_id or "current-user",
        config=data.config,
    )
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return project


@router.get("", response_model=list[ProjectRead])
async def list_projects(
    db: AsyncSession = Depends(db_dependency),
) -> list[Project]:
    """List all projects."""
    result = await db.execute(select(Project))
    return list(result.scalars().all())


@router.get("/{project_id}", response_model=ProjectRead)
async def get_project(
    project_id: uuid.UUID,
    db: AsyncSession = Depends(db_dependency),
) -> Project:
    """Fetch a single project."""
    project = await db.get(Project, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project


@router.patch("/{project_id}", response_model=ProjectRead)
async def update_project(
    project_id: uuid.UUID,
    data: ProjectUpdate,
    db: AsyncSession = Depends(db_dependency),
) -> Project:
    """Update a project."""
    project = await db.get(Project, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    updates: dict[str, Any] = data.model_dump(exclude_unset=True)
    for key, value in updates.items():
        setattr(project, key, value)

    await db.commit()
    await db.refresh(project)
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: uuid.UUID,
    db: AsyncSession = Depends(db_dependency),
) -> None:
    """Delete a project and its bindings/runs."""
    project = await db.get(Project, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    await db.delete(project)
    await db.commit()


@router.post(
    "/{project_id}/bindings",
    response_model=ProjectWorkflowBindingRead,
    status_code=status.HTTP_201_CREATED,
)
async def bind_workflow_version(
    project_id: uuid.UUID,
    data: ProjectWorkflowBindingCreate,
    db: AsyncSession = Depends(db_dependency),
) -> ProjectWorkflowBinding:
    """Bind a published workflow version to a project."""
    project = await db.get(Project, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    version = await db.get(WorkflowVersion, data.workflow_version_id)
    if version is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workflow version not found",
        )

    binding = ProjectWorkflowBinding(
        project_id=project_id,
        workflow_version_id=data.workflow_version_id,
        inputs=data.inputs,
        version_policy=data.version_policy,
    )
    db.add(binding)
    await db.commit()
    await db.refresh(binding)
    return binding


@router.get("/{project_id}/bindings", response_model=list[ProjectWorkflowBindingRead])
async def list_bindings(
    project_id: uuid.UUID,
    db: AsyncSession = Depends(db_dependency),
) -> list[ProjectWorkflowBinding]:
    """List workflow bindings for a project."""
    result = await db.execute(
        select(ProjectWorkflowBinding).where(ProjectWorkflowBinding.project_id == project_id)
    )
    return list(result.scalars().all())
