import pandas as pd

from app.services.analytics.kpi_service import (
    KPIService,
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

    service = KPIService()

    result = service.run(
        dataframe,
    )

    print("=" * 60)
    print("KPIs")
    print("=" * 60)

    for metric in result.metrics:

        print(metric.model_dump())


if __name__ == "__main__":
    main()