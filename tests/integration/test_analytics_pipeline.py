from pathlib import Path

from app.services.etl.pipeline.etl_pipeline import (
    ETLPipeline,
)

from app.services.analytics.analytics_engine import (
    AnalyticsEngine,
)

from tests.integration.pipeline_test_helper import (
    PipelineTestHelper,
)


def main() -> None:

    workspace_id, dataset_id = (
        PipelineTestHelper.prepare_workspace(
            workspace_id="ws_analytics",
            workspace_name="Analytics Integration Test",
            dataset_id="ds_sales",
            dataset_path=Path(
                "tests/data/sales.xlsx"
            ),
        )
    )

    # ======================================================
    # STEP 1 : ETL PIPELINE
    # ======================================================

    print()
    print("=" * 70)
    print("STEP 1 : ETL PIPELINE")
    print("=" * 70)

    etl = ETLPipeline()

    profile = etl.run(
        workspace_id=workspace_id,
        dataset_id=dataset_id,
    )

    print(
        f"Quality Score : {profile.quality.quality_score}"
    )

    print(
        f"Detected Columns : {profile.schema_profile.total_columns}"
    )

    print()

    # ======================================================
    # STEP 2 : ANALYTICS ENGINE
    # ======================================================

    print("=" * 70)
    print("STEP 2 : ANALYTICS ENGINE")
    print("=" * 70)

    engine = AnalyticsEngine()

    result = engine.run(
        workspace_id,
        dataset_id,
    )

    # ======================================================
    # ANALYTICS SUMMARY
    # ======================================================

    print()
    print("=" * 70)
    print("ANALYTICS PIPELINE SUMMARY")
    print("=" * 70)

    summary = result.statistics.dataset_summary

    print()

    print(summary.model_dump())

    print()

    print(
        f"Numeric Columns Analyzed           : {len(result.statistics.numeric_statistics)}"
    )

    print(
        f"Categorical Columns Analyzed       : {len(result.statistics.categorical_statistics)}"
    )

    print(
        f"Key Performance Indicators Created : {len(result.kpis.metrics)}"
    )

    print(
        f"Correlation Pairs Calculated       : {len(result.correlations.correlations)}"
    )

    print(
        f"Detected Datetime Column           : {result.trends.datetime_column}"
    )

    print(
        f"Trend Metrics Generated            : {len(result.trends.trends)}"
    )

    print(
        f"Segments Generated                 : {len(result.segmentation.segments)}"
    )

    print(
        f"Business Insights Generated        : {len(result.insights.insights)}"
    )

    # ======================================================
    # BUSINESS INSIGHTS
    # ======================================================

    print()
    print("=" * 70)
    print("BUSINESS INSIGHTS")
    print("=" * 70)

    for insight in result.insights.insights:

        print(
            insight.model_dump(),
        )

    print()
    print("=" * 70)
    print("ANALYTICS PIPELINE EXECUTED SUCCESSFULLY")
    print("=" * 70)


if __name__ == "__main__":
    main()