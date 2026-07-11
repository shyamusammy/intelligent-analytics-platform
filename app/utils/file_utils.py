from pathlib import Path
from tempfile import NamedTemporaryFile
from time import sleep

from fastapi import UploadFile


class FileUtils:
    """
    Utility functions for working with uploaded files.
    """

    @staticmethod
    async def save_temp_file(file: UploadFile) -> Path:
        suffix = Path(file.filename).suffix

        with NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        ) as temp_file:

            content = await file.read()
            temp_file.write(content)

        await file.seek(0)

        return Path(temp_file.name)

    @staticmethod
    def delete_temp_file(file_path: Path) -> None:
        """
        Delete a temporary file.

        Windows sometimes keeps Excel files locked
        for a short time after pandas/openpyxl closes
        them, so retry a few times.
        """

        if not file_path.exists():
            return

        for _ in range(5):
            try:
                file_path.unlink()
                return
            except PermissionError:
                sleep(0.2)

        print(f"Warning: Could not delete temp file: {file_path}")