from pathlib import Path

from app.services.etl.pipeline.etl_pipeline import (
    ETLPipeline,
)

from tests.integration.pipeline_test_helper import (
    PipelineTestHelper,
)


def main() -> None:

    workspace_id, dataset_id = (
        PipelineTestHelper.prepare_workspace(
            workspace_id="ws_etl",
            workspace_name="ETL Integration Test",
            dataset_id="ds_sales",
            dataset_path=Path(
                "tests/data/sales.xlsx"
            ),
        )
    )

    # ======================================================
    # Execute ETL Pipeline
    # ======================================================

    print()
    print("=" * 70)
    print("STEP 1 : ETL PIPELINE")
    print("=" * 70)

    pipeline = ETLPipeline()

    profile = pipeline.run(
        workspace_id=workspace_id,
        dataset_id=dataset_id,
    )

    # ======================================================
    # ETL SUMMARY
    # ======================================================

    print()
    print("=" * 70)
    print("ETL PIPELINE SUMMARY")
    print("=" * 70)

    print()

    print(
        f"Total Columns Detected          : {profile.schema_profile.total_columns}"
    )

    print(
        f"Missing Values Found            : {profile.missing_values.total_missing_values}"
    )

    print(
        f"Duplicate Rows Found            : {profile.duplicates.duplicate_rows}"
    )

    print(
        f"Total Outliers Detected         : {profile.outliers.total_outliers}"
    )

    print(
        f"Overall Dataset Quality Score   : {profile.quality.quality_score}"
    )

    # ======================================================
    # DETECTED SCHEMA
    # ======================================================

    print()
    print("=" * 70)
    print("DETECTED DATASET SCHEMA")
    print("=" * 70)

    for column in profile.schema_profile.columns:

        print(
            f"{column.name:<20}"
            f"{column.detected_type.value:<15}"
            f"Null Count : {column.null_count}"
        )

    # ======================================================
    # MISSING VALUES
    # ======================================================

    print()
    print("=" * 70)
    print("MISSING VALUE ANALYSIS")
    print("=" * 70)

    print(
        profile.missing_values.model_dump()
    )

    # ======================================================
    # DUPLICATES
    # ======================================================

    print()
    print("=" * 70)
    print("DUPLICATE ROW ANALYSIS")
    print("=" * 70)

    print(
        profile.duplicates.model_dump()
    )

    # ======================================================
    # NUMERIC STATISTICS
    # ======================================================

    print()
    print("=" * 70)
    print("NUMERIC COLUMN STATISTICS")
    print("=" * 70)

    for column, statistics in (
        profile.statistics.statistics.items()
    ):

        print()

        print(column)

        for metric, value in statistics.items():

            print(
                f"    {metric:<12}: {value}"
            )

    # ======================================================
    # OUTLIERS
    # ======================================================

    print()
    print("=" * 70)
    print("OUTLIER ANALYSIS")
    print("=" * 70)

    print(
        profile.outliers.model_dump()
    )

    # ======================================================
    # DATASET QUALITY
    # ======================================================

    print()
    print("=" * 70)
    print("DATASET QUALITY")
    print("=" * 70)

    print(
        profile.quality.model_dump()
    )

    print()
    print("=" * 70)
    print("ETL PIPELINE EXECUTED SUCCESSFULLY")
    print("=" * 70)


if __name__ == "__main__":
    main()