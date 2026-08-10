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

    Responsibilities
    ----------------
    - Create workspace directory structure
    - Create artifact subdirectories
    - Persist workspace metadata

    This repository contains NO business logic.
    """

    def __init__(self) -> None:
        self.base_path = Path(
            WorkspaceFolders.ROOT
        )

        self.base_path.mkdir(
            exist_ok=True,
        )

    # ==========================================================
    # CREATE
    # ==========================================================

    def create_workspace(
        self,
        workspace_id: str,
        metadata: dict,
    ) -> Path:
        """
        Create the workspace directory structure and
        save workspace metadata.
        """

        workspace_path = (
            self.base_path
            / workspace_id
        )

        workspace_path.mkdir(
            exist_ok=False,
        )

        # --------------------------------------------------
        # Main folders
        # --------------------------------------------------

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

            (
                workspace_path
                / folder
            ).mkdir()

        # --------------------------------------------------
        # Artifact folders
        # --------------------------------------------------

        artifacts_path = (
            workspace_path
            / WorkspaceFolders.ARTIFACTS
        )

        artifact_folders = [
            ArtifactFolders.PROFILING,
            ArtifactFolders.STATISTICS,
            ArtifactFolders.MODELS,
            ArtifactFolders.FORECASTS,
            ArtifactFolders.EVALUATION,
            ArtifactFolders.AI,
            ArtifactFolders.ANALYTICS,
        ]

        for folder in artifact_folders:

            (
                artifacts_path
                / folder
            ).mkdir()

        # --------------------------------------------------
        # Metadata
        # --------------------------------------------------

        metadata_file = (
            workspace_path
            / DatasetFiles.METADATA
        )

        with open(
            metadata_file,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                metadata,
                file,
                indent=4,
            )

        return workspace_path