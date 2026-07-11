from pathlib import Path

import pandas as pd

from app.services.data_manager.readers.base_reader import BaseReader


class CSVReader(BaseReader):

    SUPPORTED_EXTENSIONS = {
        ".csv",
    }
    
    """
    Reader implementation for CSV files.
    """

    DEFAULT_ENCODING = "utf-8"

    def validate(self, file_path: Path) -> None:
        """
        Validate that the CSV file can be opened.
        """

        try:
            pd.read_csv(
                file_path,
                nrows=1,
                encoding=self.DEFAULT_ENCODING,
            )

        except Exception as exc:
            raise ValueError(
                f"Invalid CSV file: {exc}"
            )

    def extract_metadata(self, file_path: Path) -> dict:
        """
        Extract basic metadata from the CSV file.
        """

        df = pd.read_csv(
            file_path,
            encoding=self.DEFAULT_ENCODING,
        )

        size_mb = round(
            file_path.stat().st_size / (1024 * 1024),
            2,
        )

        return {
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": list(df.columns),
            "size_mb": size_mb,
        }

    def preview(
        self,
        file_path: Path,
        rows: int = 10,
    ) -> pd.DataFrame:
        """
        Return the first N rows.
        """

        return pd.read_csv(
            file_path,
            nrows=rows,
            encoding=self.DEFAULT_ENCODING,
        )

    def load(
        self,
        file_path: Path,
    ) -> pd.DataFrame:
        """
        Load the entire CSV dataset.
        """

        return pd.read_csv(
            file_path,
            encoding=self.DEFAULT_ENCODING,
        )