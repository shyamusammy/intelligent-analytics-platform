from pathlib import Path
from fastapi import UploadFile
from app.core.constants import DatasetValidation    


class DatasetValidator:
    """
    Validates uploaded datasets before they are
    registered in the platform.
    """

    SUPPORTED_EXTENSIONS = DatasetValidation.SUPPORTED_EXTENSIONS

    MAX_FILE_SIZE_MB = DatasetValidation.MAX_UPLOAD_SIZE_MB

    @classmethod
    def validate_extension(cls, filename: str) -> str:
        """
        Validate the uploaded file extension.
        """

        extension = Path(filename).suffix.lower()

        if extension not in cls.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported file type: {extension}"
            )

        return extension

    @classmethod
    async def validate_file_size(cls, file: UploadFile):
        """
        Validate uploaded file size.
        """

        content = await file.read()

        size_mb = len(content) / (1024 * 1024)

        await file.seek(0)

        if size_mb > cls.MAX_FILE_SIZE_MB:
            raise ValueError(
                f"Maximum allowed file size is {cls.MAX_FILE_SIZE_MB} MB."
            )

        return round(size_mb, 2)

    @classmethod
    def validate_filename(cls, filename: str):
        """
        Ensure filename is valid.
        """

        if not filename:
            raise ValueError("Filename cannot be empty.")

        return filename