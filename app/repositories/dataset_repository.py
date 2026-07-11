from pathlib import Path
import json
import shutil
from app.core.constants import (
    WorkspaceFolders,
    DatasetFolders,
    DatasetFiles,
)


class DatasetRepository:
    """
    Handles all filesystem operations related to datasets.
    """

    ORIGINAL_FOLDER = DatasetFolders.ORIGINAL
    METADATA_FILE = DatasetFiles.METADATA

    def create_dataset_structure(
        self,
        workspace_path: Path,
        dataset_id: str,
    ) -> Path:
        """
        Creates the dataset folder structure.

        Example:

        datasets/
            ds_001/
                original/
                metadata.json
        """

        dataset_path = (
            workspace_path
            / WorkspaceFolders.DATASETS
            / dataset_id
        )

        dataset_path.mkdir(parents=True, exist_ok=False)

        (dataset_path / self.ORIGINAL_FOLDER).mkdir()

        return dataset_path

    def save_original_file(
        self,
        source_file: Path,
        dataset_path: Path,
        original_filename: str,
    ) -> Path:
        """
        Copies the uploaded file into the
        dataset's original folder while preserving
        the user's original filename.
        """

        destination = (
        dataset_path
        / self.ORIGINAL_FOLDER
        / original_filename
        )

        shutil.copy2(
            source_file,
            destination,
        )

        return destination

    def save_metadata(
        self,
        dataset_path: Path,
        metadata: dict,
    ) -> None:
        """
        Saves dataset metadata.
        """

        metadata_file = (
            dataset_path
            / self.METADATA_FILE
        )

        with open(
            metadata_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                metadata,
                file,
                indent=4,
            )