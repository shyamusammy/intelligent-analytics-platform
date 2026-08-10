from pathlib import Path
import shutil
from datetime import datetime

from app.repositories.workspace_repository import (
    WorkspaceRepository,
)

from app.repositories.dataset_repository import (
    DatasetRepository,
)


class PipelineTestHelper:
    """
    Helper responsible for preparing
    integration test workspaces.

    Responsibilities
    ----------------
    - Clean previous workspace
    - Create workspace
    - Register dataset
    - Save dataset metadata

    This helper contains NO pipeline logic.
    """

    @staticmethod
    def prepare_workspace(
        workspace_id: str,
        workspace_name: str,
        dataset_id: str,
        dataset_path: Path,
    ) -> tuple[str, str]:

        PipelineTestHelper._clean_workspace(
            workspace_id,
        )

        workspace_repository = (
            WorkspaceRepository()
        )

        dataset_repository = (
            DatasetRepository()
        )

        workspace_metadata = {
            "workspace_id": workspace_id,
            "name": workspace_name,
        }

        workspace_path = (
            workspace_repository.create_workspace(
                workspace_id,
                workspace_metadata,
            )
        )

        dataset_folder = (
            dataset_repository.create_dataset_structure(
                workspace_path,
                dataset_id,
            )
        )

        dataset_repository.save_original_file(
            source_file=dataset_path,
            dataset_path=dataset_folder,
            original_filename=dataset_path.name,
        )

        dataset_metadata = {
            "dataset_id": dataset_id,
            "workspace_id": workspace_id,

            "display_name": dataset_path.stem,

            "original_filename": dataset_path.name,

            "extension": dataset_path.suffix,

            "size_mb": round(
                dataset_path.stat().st_size / (1024 * 1024),
                4,
            ),

            "rows": None,

            "columns": None,

            "sheet_name": None,

            "active": True,

            "status": "registered",

            "uploaded_at": datetime.now().isoformat(),
        }

        dataset_repository.save_metadata(
            dataset_folder,
            dataset_metadata,
        )

        return (
            workspace_id,
            dataset_id,
        )

    @staticmethod
    def _clean_workspace(
        workspace_id: str,
    ) -> None:
        """
        Delete an existing workspace before
        running an integration test.
        """

        workspace_root = (
            Path("workspaces")
            / workspace_id
        )

        if workspace_root.exists():

            shutil.rmtree(
                workspace_root,
            )