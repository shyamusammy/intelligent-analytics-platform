from app.services.data_manager.readers.base_reader import BaseReader
from app.services.data_manager.readers.csv_reader import CSVReader
from app.services.data_manager.readers.excel_reader import ExcelReader


class ReaderFactory:
    """
    Factory responsible for returning the correct
    reader implementation based on file extension.
    """

    READERS = {}

    for reader in (
        CSVReader,
        ExcelReader,
    ):
        for extension in reader.SUPPORTED_EXTENSIONS:
            READERS[extension] = reader

    @classmethod
    def get_reader(cls, extension: str) -> BaseReader:
        """
        Return the appropriate reader instance.
        """

        reader_class = cls.READERS.get(extension.lower())

        if reader_class is None:
            raise ValueError(
                f"No reader available for '{extension}'."
            )

        return reader_class()