from pathlib import Path
from datetime import datetime

from app.repositories.workspace_repository import WorkspaceRepository
from app.schemas.workspace import WorkspaceResponse
from app.core.constants import (
    WorkspaceFolders,
    WorkspaceStatus,
    APP_VERSION,
)


class WorkspaceService:
    """
    Handles business logic related to workspaces.
    """

    def __init__(self):
        self.repository = WorkspaceRepository()

    def _generate_workspace_id(self) -> str:
        """
        Generate the next workspace ID.

        Example:
        ws_001
        ws_002
        ws_003
        """

        workspace_root = Path(WorkspaceFolders.ROOT)

        workspace_root.mkdir(parents=True, exist_ok=True)

        existing_numbers = [
            int(folder.name.removeprefix("ws_"))
            for folder in workspace_root.iterdir()
            if (
                folder.is_dir()
                and folder.name.startswith("ws_")
                and folder.name.removeprefix("ws_").isdigit()
            )
        ]

        if not existing_numbers:
            return "ws_001"

        number = max(existing_numbers) + 1

        return f"ws_{number:03d}"

    def create_workspace(
        self,
        name: str,
        description: str,
        industry: str,
        objective: str,
    ) -> WorkspaceResponse:

        workspace_id = self._generate_workspace_id()

        current_time = datetime.now().isoformat()

        metadata = {
            "workspace_id": workspace_id,
            "name": name,
            "description": description,
            "industry": industry,
            "objective": objective,

            "status": WorkspaceStatus.ACTIVE,
            "version": APP_VERSION,

            "active_dataset": None,

            "datasets": 0,
            "models": 0,
            "reports": 0,

            "created_at": current_time,
            "last_modified": current_time,
        }

        self.repository.create_workspace(
            workspace_id,
            metadata,
        )

        return WorkspaceResponse(
            workspace_id=workspace_id,
            name=name,
            description=description,
            industry=industry,
            objective=objective,
            status=WorkspaceStatus.ACTIVE,
            version=APP_VERSION,
        )
