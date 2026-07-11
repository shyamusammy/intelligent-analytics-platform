from pathlib import Path
import json
from app.core.constants import (
    WorkspaceFolders,
    ArtifactFolders,
    DatasetFiles,
)


class WorkspaceRepository:
    """
    Handles all filesystem operations related to workspaces.
    """

    def __init__(self):
        self.base_path = Path(WorkspaceFolders.ROOT)
        self.base_path.mkdir(exist_ok=True)

    def create_workspace(self, workspace_id: str, metadata: dict) -> Path:
        """
        Creates the workspace folder structure and saves metadata.json.

        Parameters
        ----------
        workspace_id : str
            Unique workspace identifier (e.g., ws_001)

        metadata : dict
            Workspace metadata prepared by the Service layer.

        Returns
        -------
        Path
            Path to the created workspace.
        """

        workspace_path = self.base_path / workspace_id

        # Create workspace folder
        workspace_path.mkdir(exist_ok=False)

        # Main folders
        folders = [
            WorkspaceFolders.DATASETS,
            WorkspaceFolders.PROCESSED,
            WorkspaceFolders.ARTIFACTS,
            WorkspaceFolders.DASHBOARD,
            WorkspaceFolders.REPORTS,
            WorkspaceFolders.EXPORTS,
            WorkspaceFolders.LOGS,
        ]

        for folder in folders:
            (workspace_path / folder).mkdir()

        # Artifact subfolders
        artifact_folders = [
            ArtifactFolders.PROFILING,
            ArtifactFolders.STATISTICS,
            ArtifactFolders.MODELS,
            ArtifactFolders.FORECASTS,
            ArtifactFolders.EVALUATION,
            ArtifactFolders.AI,
        ]

        artifacts_path = workspace_path / WorkspaceFolders.ARTIFACTS

        for folder in artifact_folders:
            (artifacts_path / folder).mkdir()

        # Save metadata
        metadata_file = workspace_path / DatasetFiles.METADATA

        with open(metadata_file, "w", encoding="utf-8") as file:
            json.dump(metadata, file, indent=4)

        return workspace_path