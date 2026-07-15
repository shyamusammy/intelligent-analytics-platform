from pathlib import Path

import pandas as pd

from app.repositories.dataset_repository import DatasetRepository
from app.services.data_manager.readers.factory import ReaderFactory


class DatasetLoaderService:
    """
    Service responsible for loading a registered dataset
    into a pandas DataFrame.

    This service orchestrates the loading workflow by
    delegating filesystem operations to the repository
    and file-format handling to the ReaderFactory.
    """

    def __init__(
        self,
        repository: DatasetRepository | None = None,
    ) -> None:
        """
        Initialize the DatasetLoaderService.

        Parameters
        ----------
        repository : DatasetRepository | None
            Repository used to access dataset files.
        """

        self.repository = repository or DatasetRepository()

    def load(
        self,
        workspace_id: str,
        dataset_id: str,
    ) -> pd.DataFrame:
        """
        Load a dataset into memory.

        Parameters
        ----------
        workspace_id : str
            Workspace identifier.

        dataset_id : str
            Dataset identifier.

        Returns
        -------
        pd.DataFrame
            Loaded dataset.
        """

        metadata = self.repository.load_metadata(
            workspace_id,
            dataset_id,
        )

        dataset_file = self.repository.get_original_file(
            workspace_id,
            dataset_id,
        )

        reader = ReaderFactory.get_reader(
            metadata.extension,
        )

        dataframe = reader.load(dataset_file)

        return dataframe