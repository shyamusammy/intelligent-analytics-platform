from app.services.data_manager.readers.factory import ReaderFactory


def main():

    extensions = [
        ".csv",
        ".xlsx",
        ".xls",
    ]

    for extension in extensions:

        reader = ReaderFactory.get_reader(extension)

        print(
            f"{extension} -> {type(reader).__name__}"
        )


if __name__ == "__main__":
    main()