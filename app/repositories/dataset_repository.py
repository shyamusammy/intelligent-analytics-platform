from pathlib import Path
import json
import shutil

import pandas as pd

from app.core.constants import (
    WorkspaceFolders,
    DatasetFolders,
    DatasetFiles,
)

from app.core.exceptions import (
    DatasetNotFoundError,
    DatasetMetadataNotFoundError,
    OriginalDatasetNotFoundError,
    UnsupportedDatasetFormatError,
)

from app.schemas.dataset import DatasetMetadata


class DatasetRepository:
    """
    Handles all filesystem operations related to datasets.

    Responsibilities
    ----------------
    - Create dataset directory structure
    - Save original uploaded files
    - Save dataset metadata
    - Load dataset metadata
    - Load dataset as DataFrame
    - Locate dataset directories
    - Locate original dataset files

    This repository should contain NO business logic.
    """

    ORIGINAL_FOLDER = DatasetFolders.ORIGINAL
    METADATA_FILE = DatasetFiles.METADATA

    # ==========================================================
    # CREATE
    # ==========================================================

    def create_dataset_structure(
        self,
        workspace_path: Path,
        dataset_id: str,
    ) -> Path:
        """
        Creates the dataset folder structure.

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

        dataset_path.mkdir(
            parents=True,
            exist_ok=False,
        )

        (
            dataset_path
            / self.ORIGINAL_FOLDER
        ).mkdir()

        return dataset_path

    def save_original_file(
        self,
        source_file: Path,
        dataset_path: Path,
        original_filename: str,
    ) -> Path:
        """
        Saves the uploaded file inside the dataset's
        original directory while preserving its filename.
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
        Saves dataset metadata to metadata.json.
        """

        metadata_file = (
            dataset_path
            / self.METADATA_FILE
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

    # ==========================================================
    # READ
    # ==========================================================

    def get_dataset_path(
        self,
        workspace_id: str,
        dataset_id: str,
    ) -> Path:
        """
        Returns the dataset directory.

        Raises
        ------
        DatasetNotFoundError
            If the dataset directory does not exist.
        """

        dataset_path = (
            Path(WorkspaceFolders.ROOT)
            / workspace_id
            / WorkspaceFolders.DATASETS
            / dataset_id
        )

        if not dataset_path.exists():
            raise DatasetNotFoundError(
                dataset_id,
            )

        return dataset_path

    def load_metadata(
        self,
        workspace_id: str,
        dataset_id: str,
    ) -> DatasetMetadata:
        """
        Loads metadata.json and returns a DatasetMetadata object.
        """

        dataset_path = self.get_dataset_path(
            workspace_id,
            dataset_id,
        )

        metadata_file = (
            dataset_path
            / self.METADATA_FILE
        )

        if not metadata_file.exists():
            raise DatasetMetadataNotFoundError(
                dataset_id,
            )

        with open(
            metadata_file,
            "r",
            encoding="utf-8",
        ) as file:

            metadata = json.load(file)

        return DatasetMetadata(**metadata)

    def get_original_file(
        self,
        workspace_id: str,
        dataset_id: str,
    ) -> Path:
        """
        Returns the original uploaded dataset file.
        """

        dataset_path = self.get_dataset_path(
            workspace_id,
            dataset_id,
        )

        original_folder = (
            dataset_path
            / self.ORIGINAL_FOLDER
        )

        files = [
            file
            for file in original_folder.iterdir()
            if file.is_file()
        ]

        if not files:
            raise OriginalDatasetNotFoundError(
                dataset_id,
            )

        if len(files) > 1:
            raise OriginalDatasetNotFoundError(
                dataset_id,
            )

        return files[0]

    def load_dataframe(
        self,
        workspace_id: str,
        dataset_id: str,
    ) -> pd.DataFrame:
        """
        Loads the original dataset into a pandas DataFrame.
        """

        dataset_file = self.get_original_file(
            workspace_id,
            dataset_id,
        )

        return self._read_dataframe(
            dataset_file,
        )

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _read_dataframe(
        self,
        dataset_file: Path,
    ) -> pd.DataFrame:
        """
        Reads a dataset file into a pandas DataFrame.
        """

        suffix = dataset_file.suffix.lower()

        if suffix == ".csv":

            return pd.read_csv(
                dataset_file,
            )

        if suffix in (
            ".xlsx",
            ".xls",
        ):

            return pd.read_excel(
                dataset_file,
            )

        raise UnsupportedDatasetFormatError(
            suffix,
        )