import pandas as pd

from app.services.analytics.statistics_service import (
    StatisticsService,
)

from app.services.analytics.kpi_service import (
    KPIService,
)

from app.services.analytics.correlation_service import (
    CorrelationService,
)

from app.services.analytics.trend_service import (
    TrendService,
)

from app.services.analytics.segmentation_service import (
    SegmentationService,
)

from app.services.analytics.insight_service import (
    InsightService,
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
            "Department": [
                "Sales",
                "Sales",
                "HR",
                "Finance",
                "Sales",
            ],
        }
    )

    statistics_service = StatisticsService()
    kpi_service = KPIService()
    correlation_service = CorrelationService()
    trend_service = TrendService()
    segmentation_service = SegmentationService()
    insight_service = InsightService()

    statistics = statistics_service.run(
        dataframe,
    )

    kpis = kpi_service.run(
        dataframe,
    )

    correlations = correlation_service.run(
        dataframe,
    )

    trends = trend_service.run(
        dataframe,
    )

    segmentation = segmentation_service.run(
        dataframe,
    )

    insights = insight_service.run(
        statistics=statistics,
        kpis=kpis,
        correlations=correlations,
        trends=trends,
        segmentation=segmentation,
    )

    print("=" * 70)
    print("INSIGHTS")
    print("=" * 70)
    print()

    for insight in insights.insights:

        print(
            insight.model_dump(
                mode="json",
            )
        )


if __name__ == "__main__":
    main()