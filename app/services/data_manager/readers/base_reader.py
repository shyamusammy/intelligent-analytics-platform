from abc import ABC, abstractmethod
from pathlib import Path

import pandas as pd


class BaseReader(ABC):
    """
    Abstract base class for all dataset readers.

    Every dataset reader must implement this interface
    so the Data Manager can work with any supported
    file type without knowing its implementation.
    """

    @abstractmethod
    def validate(self, file_path: Path) -> None:
        """
        Perform file-type-specific validation.

        Examples:
        - CSV encoding
        - Excel workbook integrity
        - SQL connection
        """
        pass

    @abstractmethod
    def extract_metadata(self, file_path: Path) -> dict:
        """
        Extract dataset metadata without loading the
        complete dataset into memory.

        Returns:
            Dictionary containing metadata.
        """
        pass

    @abstractmethod
    def preview(
        self,
        file_path: Path,
        rows: int = 10,
    ) -> pd.DataFrame:
        """
        Return the first N rows of the dataset.

        Used for dataset preview.
        """
        pass

    @abstractmethod
    def load(
        self,
        file_path: Path,
    ) -> pd.DataFrame:
        """
        Load the complete dataset into memory.

        Returns:
            Pandas DataFrame
        """
        pass