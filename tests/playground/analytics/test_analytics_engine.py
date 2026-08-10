from pathlib import Path
import shutil

from app.repositories.workspace_repository import (
    WorkspaceRepository,
)

from app.repositories.dataset_repository import (
    DatasetRepository,
)

from app.services.etl.etl_pipeline import (
    ETLPipeline,
)

from app.services.analytics.analytics_engine import (
    AnalyticsEngine,
)


def main() -> None:

    workspace_id = "ws_analytics"

    dataset_id = "ds_sales"

    sample_dataset = Path(
        "tests/data/sales.xlsx"
    )

    # ======================================================
    # Clean Previous Workspace
    # ======================================================

    workspace_root = (
        Path("workspaces")
        / workspace_id
    )

    if workspace_root.exists():

        shutil.rmtree(
            workspace_root,
        )

    # ======================================================
    # Create Workspace
    # ======================================================

    workspace_repository = (
        WorkspaceRepository()
    )

    dataset_repository = (
        DatasetRepository()
    )

    workspace_metadata = {
        "workspace_id": workspace_id,
        "name": "Analytics Test Workspace",
    }

    workspace_path = (
        workspace_repository.create_workspace(
            workspace_id,
            workspace_metadata,
        )
    )

    # ======================================================
    # Register Dataset
    # ======================================================

    dataset_path = (
        dataset_repository.create_dataset_structure(
            workspace_path,
            dataset_id,
        )
    )

    dataset_repository.save_original_file(
        source_file=sample_dataset,
        dataset_path=dataset_path,
        original_filename=sample_dataset.name,
    )

    dataset_metadata = {
        "dataset_id": dataset_id,
        "workspace_id": workspace_id,
        "original_filename": sample_dataset.name,
        "file_extension": sample_dataset.suffix,
        "file_size": sample_dataset.stat().st_size,
    }

    dataset_repository.save_metadata(
        dataset_path,
        dataset_metadata,
    )

    # ======================================================
    # Execute ETL Pipeline
    # ======================================================

    print()
    print("=" * 70)
    print("STEP 1 : ETL PIPELINE")
    print("=" * 70)

    etl_pipeline = ETLPipeline()

    etl_profile = etl_pipeline.run(
        workspace_id=workspace_id,
        dataset_id=dataset_id,
    )

    print(
        f"Dataset Quality Score : {etl_profile.quality.quality_score}"
    )

    print(
        f"Datetime Columns      : "
        f"{len([c for c in etl_profile.schema_profile.columns if c.detected_type.value == 'datetime'])}"
    )

    print()

    # ======================================================
    # Execute Analytics Engine
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

    summary = result.statistics.dataset_summary

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
        f"Trend Analysis Results Generated   : {len(result.trends.trends)}"
    )

    print(
        f"Segment Summaries Generated        : {len(result.segmentation.segments)}"
    )

    print(
        f"Business Insights Generated        : {len(result.insights.insights)}"
    )

    # ======================================================
    # NUMERIC STATISTICS
    # ======================================================

    print()
    print("=" * 70)
    print("NUMERIC STATISTICS")
    print("=" * 70)

    for statistic in result.statistics.numeric_statistics:

        print(
            statistic.model_dump(),
        )

    # ======================================================
    # CATEGORICAL STATISTICS
    # ======================================================

    print()
    print("=" * 70)
    print("CATEGORICAL STATISTICS")
    print("=" * 70)

    for statistic in result.statistics.categorical_statistics:

        print(
            statistic.model_dump(),
        )

    # ======================================================
    # KPIs
    # ======================================================

    print()
    print("=" * 70)
    print("KEY PERFORMANCE INDICATORS")
    print("=" * 70)

    for metric in result.kpis.metrics:

        print(
            metric.model_dump(),
        )

    # ======================================================
    # CORRELATIONS
    # ======================================================

    print()
    print("=" * 70)
    print("CORRELATION ANALYSIS")
    print("=" * 70)

    for correlation in result.correlations.correlations:

        print(
            correlation.model_dump(),
        )

    # ======================================================
    # TRENDS
    # ======================================================

    print()
    print("=" * 70)
    print("TREND ANALYSIS")
    print("=" * 70)

    print(
        f"Detected Datetime Column : {result.trends.datetime_column}"
    )

    print()

    for trend in result.trends.trends:

        print(
            trend.model_dump(),
        )

    # ======================================================
    # SEGMENTATION
    # ======================================================

    print()
    print("=" * 70)
    print("SEGMENTATION")
    print("=" * 70)

    for segment in result.segmentation.segments:

        print(
            segment.model_dump(),
        )

    # ======================================================
    # INSIGHTS
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
    print("PIPELINE EXECUTED SUCCESSFULLY")
    print("=" * 70)


if __name__ == "__main__":
    main()