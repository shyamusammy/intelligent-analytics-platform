import pandas as pd

from app.services.analytics.statistics_service import (
    StatisticsService,
)


def main() -> None:

    dataframe = pd.DataFrame(
        {
            "Product": [
                "Laptop",
                "Laptop",
                "Mouse",
                "Keyboard",
                "Mouse",
            ],
            "Category": [
                "Electronics",
                "Electronics",
                "Accessories",
                "Accessories",
                "Accessories",
            ],
            "Quantity": [
                10,
                15,
                8,
                20,
                12,
            ],
            "Price": [
                800.0,
                820.0,
                25.0,
                45.0,
                30.0,
            ],
            "Profit": [
                120.0,
                140.0,
                8.0,
                12.0,
                10.0,
            ],
        }
    )

    service = StatisticsService()

    result = service.run(
        dataframe,
    )

    print("=" * 60)
    print("DATASET SUMMARY")
    print("=" * 60)

    print(
        result.dataset_summary.model_dump()
    )

    print()

    print("=" * 60)
    print("NUMERIC STATISTICS")
    print("=" * 60)

    for statistic in result.numeric_statistics:

        print()

        print(
            statistic.model_dump()
        )

    print()

    print("=" * 60)
    print("CATEGORICAL STATISTICS")
    print("=" * 60)

    for statistic in result.categorical_statistics:

        print()

        print(
            statistic.model_dump()
        )


if __name__ == "__main__":
    main()