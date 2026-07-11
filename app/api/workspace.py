from fastapi import APIRouter

from app.schemas.workspace import (
    WorkspaceCreate,
    WorkspaceResponse,
)

from app.services.workspace_service import WorkspaceService

router = APIRouter(
    prefix="/workspaces",
    tags=["Workspaces"],
)

workspace_service = WorkspaceService()


@router.post(
    "/",
    response_model=WorkspaceResponse,
    summary="Create a new workspace",
)
def create_workspace(workspace: WorkspaceCreate):

    return workspace_service.create_workspace(
        name=workspace.name,
        description=workspace.description,
        industry=workspace.industry,
        objective=workspace.objective,
    )