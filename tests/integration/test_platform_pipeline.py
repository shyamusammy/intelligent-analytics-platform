from pathlib import Path

from app.services.pipeline import PlatformPipeline

from tests.integration.pipeline_test_helper import (
    PipelineTestHelper,
)


def main() -> None:

    # ======================================================
    # PREPARE TEST WORKSPACE
    # ======================================================

    workspace_id, dataset_id = (
        PipelineTestHelper.prepare_workspace(
            workspace_id="ws_platform_pipeline",
            workspace_name="Platform Pipeline Integration Test",
            dataset_id="ds_sales",
            dataset_path=Path(
                "tests/data/sales.xlsx"
            ),
        )
    )

    target_column = "Revenue"

    # ======================================================
    # EXECUTE PLATFORM PIPELINE
    # ======================================================

    print()
    print("=" * 70)
    print("PLATFORM PIPELINE")
    print("=" * 70)

    pipeline = PlatformPipeline()

    result = pipeline.run(
        workspace_id=workspace_id,
        dataset_id=dataset_id,
        target_column=target_column,
    )

    # ======================================================
    # RESULT VALIDATION
    # ======================================================

    assert result is not None

    # ------------------------------------------------------
    # ETL
    # ------------------------------------------------------

    assert result.etl is not None

    assert result.etl.schema_profile is not None

    assert result.etl.quality is not None

    # ------------------------------------------------------
    # ANALYTICS
    # ------------------------------------------------------

    assert result.analytics is not None

    assert result.analytics.statistics is not None

    assert result.analytics.correlations is not None

    assert result.analytics.trends is not None

    assert result.analytics.segmentation is not None

    assert result.analytics.insights is not None

    # ------------------------------------------------------
    # ML
    # ------------------------------------------------------

    assert result.ml is not None

    assert result.ml.validation.valid

    assert result.ml.task_type is not None

    assert result.ml.train_result is not None

    assert result.ml.evaluation_result is not None

    assert (
        result.ml.evaluation_result.best_model
        is not None
    )

    # ======================================================
    # SUMMARY
    # ======================================================

    print()
    print("=" * 70)
    print("PLATFORM PIPELINE SUMMARY")
    print("=" * 70)

    print(
        f"ETL Result              : PASSED"
    )

    print(
        f"Analytics Result        : PASSED"
    )

    print(
        f"ML Validation           : PASSED"
    )

    print(
        f"ML Training             : PASSED"
    )

    print(
        f"ML Evaluation           : PASSED"
    )

    print(
        f"Best Model              : "
        f"{result.ml.evaluation_result.best_model.trained_model.estimator.value}"
    )

    print()
    print("=" * 70)
    print("PLATFORM PIPELINE EXECUTED SUCCESSFULLY")
    print("=" * 70)


if __name__ == "__main__":
    main()