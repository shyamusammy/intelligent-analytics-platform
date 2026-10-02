from app.services.etl.pipeline.etl_pipeline import ETLPipeline
from app.services.cleaning.cleaning_engine import CleaningEngine


def test_cleaning_engine():
    workspace_id = "ws_005"
    dataset_id = "ds_001"

    # ---------------------------------------------------------
    # 1. Generate the real ETL profile
    # ---------------------------------------------------------
    profile = ETLPipeline().run(
        workspace_id=workspace_id,
        dataset_id=dataset_id,
    )

    # ---------------------------------------------------------
    # 2. Run CleaningEngine
    # ---------------------------------------------------------
    report = CleaningEngine().run(
        workspace_id=workspace_id,
        dataset_id=dataset_id,
        profile=profile,
    )

    # ---------------------------------------------------------
    # 3. Basic validation
    # ---------------------------------------------------------
    assert report.original_row_count > 0

    assert (
        report.cleaned_row_count
        <= report.original_row_count
    )

    # Duplicates should be removed.
    assert report.duplicates_removed >= 0
    assert report.duplicate_rows_after == 0

    # Missing values must be completely removed.
    assert report.missing_values_before >= 0
    assert report.missing_values_after == 0

    # Cleaning must produce a quality score.
    assert report.quality_score_before >= 0
    assert report.quality_score_before <= 100

    assert report.quality_score_after >= 0
    assert report.quality_score_after <= 100

    # A cleaned dataset must have been saved.
    assert report.cleaned_dataset_path

    # Actions should be recorded for columns that required cleaning.
    assert isinstance(report.columns_affected, list)
    assert isinstance(report.actions, list)

    print("=" * 80)
    print("CleaningEngine test passed")
    print("=" * 80)

    print(f"Original rows : {report.original_row_count}")
    print(f"Cleaned rows  : {report.cleaned_row_count}")
    print(f"Duplicates removed : {report.duplicates_removed}")
    print(f"Missing before : {report.missing_values_before}")
    print(f"Missing after  : {report.missing_values_after}")
    print(f"Quality before : {report.quality_score_before}")
    print(f"Quality after  : {report.quality_score_after}")
    print(f"Columns affected : {report.columns_affected}")
    print("=" * 80)

    # ============================================================
    # CLEANING ACTIONS
    # ============================================================

    print("=" * 80)
    print("CLEANING ACTIONS")
    print("=" * 80)

    for action in report.actions:
        print(
            f"{action.column_name:15} | "
            f"{action.strategy:35} | "
            f"values replaced: {action.values_replaced}"
    )


    print("=" * 80)
    print("OUTLIERS")
    print("=" * 80)

    print(
        f"Before cleaning : "
        f"{report.outliers_before.total_outliers}"
    )

    print(
        f"Affected rows   : "
        f"{report.outliers_before.affected_rows}"
    )

    print(
        f"After cleaning  : "
        f"{report.outliers_after.total_outliers}"
    )

    print(
        f"Affected rows   : "
        f"{report.outliers_after.affected_rows}"
    )

    print("-" * 80)

    for column, count in (
        report.outliers_before.outliers_by_column.items()
    ):
        print(
            f"{column:<20} | {count}"
        )

if __name__ == "__main__":
    test_cleaning_engine()