import pandas as pd

from app.services.analytics.correlation_service import (
    CorrelationService,
)


def main() -> None:

    dataframe = pd.DataFrame(
        {
            "Revenue": [
                100,
                200,
                300,
                400,
                500,
            ],
            "Profit": [
                10,
                20,
                30,
                40,
                50,
            ],
            "Quantity": [
                5,
                10,
                15,
                20,
                25,
            ],
            "Discount": [
                10,
                8,
                6,
                4,
                2,
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

    service = CorrelationService()

    result = service.run(
        dataframe,
    )

    print("=" * 70)
    print("CORRELATIONS")
    print("=" * 70)

    for correlation in result.correlations:

        print(
            correlation.model_dump()
        )


if __name__ == "__main__":
    main()