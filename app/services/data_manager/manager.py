from datetime import datetime
from pathlib import Path

from fastapi import UploadFile

from app.core.constants import (
    APP_VERSION,
    DatasetStatus,
    WorkspaceFolders,
)

from app.repositories.dataset_repository import DatasetRepository
from app.services.data_manager.registry import DatasetRegistry
from app.services.data_manager.validator import DatasetValidator
from app.services.data_manager.readers.factory import ReaderFactory
from app.schemas.dataset import DatasetResponse
from app.utils.file_utils import FileUtils


class DataManager:
    """
    Coordinates dataset registration.

    This class contains the workflow but delegates
    the actual work to specialized components.
    """

    def __init__(self):

        self.validator = DatasetValidator()

        self.registry = DatasetRegistry()

        self.repository = DatasetRepository()

    async def register_dataset(
        self,
        workspace_id: str,
        file: UploadFile,
        display_name: str,
    ) -> DatasetResponse:
        workspace_path = (
            Path(WorkspaceFolders.ROOT)
            / workspace_id
        )

        # ---------------------------------------
        # Generic validation
        # ---------------------------------------

        self.validator.validate_filename(file.filename)

        extension = self.validator.validate_extension(
            file.filename
        )

        size_mb = await self.validator.validate_file_size(
            file
        )

        # ---------------------------------------
        # Temporary file
        # ---------------------------------------

        temp_file = await FileUtils.save_temp_file(file)

        try:

            # ---------------------------------------
            # Reader
            # ---------------------------------------

            reader = ReaderFactory.get_reader(extension)

            reader.validate(temp_file)

            metadata = reader.extract_metadata(temp_file)

            # ---------------------------------------
            # Dataset ID
            # ---------------------------------------

            dataset_id = self.registry.generate_dataset_id(
                workspace_path
            )

            # ---------------------------------------
            # Repository
            # ---------------------------------------

            dataset_path = (
                self.repository.create_dataset_structure(
                    workspace_path,
                    dataset_id,
                )
            )

            self.repository.save_original_file(
                source_file=temp_file,
                 dataset_path=dataset_path,
                original_filename=file.filename,
            )

            dataset_metadata = {

                "dataset_id": dataset_id,

                "workspace_id": workspace_id,

                "display_name": display_name,

                "original_filename": file.filename,

                "extension": extension,

                "size_mb": size_mb,

                "rows": metadata["rows"],

                "columns": metadata["columns"],

                "sheet_name": metadata.get(
                    "sheet_name"
                ),

                "active": True,

                "status": DatasetStatus.UPLOADED,

                "uploaded_at": datetime.now().isoformat(),

                "version": APP_VERSION,
            }

            self.repository.save_metadata(
                dataset_path,
                dataset_metadata,
            )

            return DatasetResponse(
                dataset_id=dataset_id,
                workspace_id=workspace_id,
                display_name=display_name,
                original_filename=file.filename,
                extension=extension,
                status=DatasetStatus.UPLOADED,
                uploaded_at=datetime.fromisoformat(
                    dataset_metadata["uploaded_at"]
                ),
            )

        finally:

            #FileUtils.delete_temp_file(temp_file)
            pass