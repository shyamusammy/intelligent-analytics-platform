import pandas as pd

from app.services.analytics.trend_service import (
    TrendService,
)


def main() -> None:

    dataframe = pd.DataFrame(
        {
            "Date": pd.to_datetime(
                [
                    "2024-01-01",
                    "2024-02-01",
                    "2024-03-01",
                    "2024-04-01",
                    "2024-05-01",
                ]
            ),
            "Revenue": [
                100,
                150,
                180,
                220,
                300,
            ],
            "Profit": [
                20,
                35,
                45,
                55,
                70,
            ],
            "Inventory": [
                500,
                470,
                440,
                420,
                400,
            ],
            "Target": [
                100,
                100,
                100,
                100,
                100,
            ],
            "Category": [
                "A",
                "A",
                "B",
                "B",
                "C",
            ],
        }
    )

    service = TrendService()

    result = service.run(
        dataframe,
    )

    print("=" * 70)
    print("TREND RESULT")
    print("=" * 70)

    print()

    print(
        f"Datetime Column: {result.datetime_column}"
    )

    print()

    for trend in result.trends:

        print(
            trend.model_dump(
                mode="json",
            )
        )


if __name__ == "__main__":
    main()