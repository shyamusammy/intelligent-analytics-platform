from pathlib import Path

import pandas as pd

from app.services.data_manager.readers.base_reader import BaseReader


class ExcelReader(BaseReader):
    """
    Reader implementation for Excel (.xlsx and .xls) files.
    """

    SUPPORTED_EXTENSIONS = {
        ".xlsx",
        ".xls",
    }

    def validate(self, file_path: Path) -> None:
        """
        Validate that the Excel workbook can be opened.
        """

        try:
            with pd.ExcelFile(file_path):
                pass

        except Exception as exc:
            raise ValueError(
                f"Invalid Excel file: {exc}"
            )

    def extract_metadata(
        self,
        file_path: Path,
    ) -> dict:
        """
        Extract workbook metadata.
        """

        with pd.ExcelFile(file_path) as excel:
            first_sheet = excel.sheet_names[0]
            sheet_count = len(excel.sheet_names)

        df = pd.read_excel(
            file_path,
            sheet_name=first_sheet,
        )

        size_mb = round(
            file_path.stat().st_size / (1024 * 1024),
            2,
        )

        return {
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": list(df.columns),
            "sheet_name": first_sheet,
            "sheet_count": sheet_count,
            "size_mb": size_mb,
        }

    def preview(
        self,
        file_path: Path,
        rows: int = 10,
    ) -> pd.DataFrame:
        """
        Return the first N rows from the first worksheet.
        """

        return pd.read_excel(
            file_path,
            nrows=rows,
        )

    def load(
        self,
        file_path: Path,
    ) -> pd.DataFrame:
        """
        Load the first worksheet.
        """

        return pd.read_excel(file_path)