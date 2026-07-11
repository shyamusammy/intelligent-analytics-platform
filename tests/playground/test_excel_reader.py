from pathlib import Path

from app.services.data_manager.readers.excel_reader import ExcelReader


def main():
    reader = ExcelReader()

    file_path = Path("tests/data/sales.xlsx")

    print("Testing Excel Reader...")
    print("-" * 50)

    metadata = reader.extract_metadata(file_path)

    print("Metadata:")
    print(metadata)

    print("\nPreview:")
    print(reader.preview(file_path))


if __name__ == "__main__":
    main()