from pathlib import Path

from app.repositories.model_repository import (
    ModelRepository,
)

from app.services.pipeline import (
    PlatformPipeline,
)

from tests.integration.pipeline_test_helper import (
    PipelineTestHelper,
)


def main() -> None:

    # ======================================================
    # PREPARE TEST WORKSPACE
    # ======================================================

    workspace_id, dataset_id = (
        PipelineTestHelper.prepare_workspace(
            workspace_id="ws_ml_persistence",
            workspace_name="ML Persistence Integration Test",
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
    print("ML MODEL PERSISTENCE")
    print("=" * 70)

    pipeline = PlatformPipeline()

    result = pipeline.run(
        workspace_id=workspace_id,
        dataset_id=dataset_id,
        target_column=target_column,
    )

    # ======================================================
    # PIPELINE VALIDATION
    # ======================================================

    assert result is not None

    assert result.ml is not None

    assert result.ml.validation.valid

    assert result.ml.evaluation_result is not None

    best_model = (
        result.ml.evaluation_result.best_model
    )

    assert best_model is not None

    expected_best_model = (
        best_model
        .trained_model
        .estimator
        .value
    )

    print()
    print(
        f"Best Model Selected : "
        f"{expected_best_model}"
    )

    # ======================================================
    # MODEL REPOSITORY
    # ======================================================

    repository = ModelRepository()

    models_path = (
        Path("workspaces")
        / workspace_id
        / "artifacts"
        / "models"
    )

    # ======================================================
    # VERIFY CANDIDATE MODELS
    # ======================================================

    print()
    print("=" * 70)
    print("MODEL ARTIFACT VALIDATION")
    print("=" * 70)

    for trained_model in (
        result.ml.train_result.models
    ):

        model_name = (
            trained_model
            .estimator
            .value
        )

        model_path = (
            models_path
            / f"{model_name}.joblib"
        )

        assert model_path.exists()

        print(
            f"{model_name:<30}: PASSED"
        )

    # ======================================================
    # VERIFY BEST MODEL
    # ======================================================

    best_model_path = (
        models_path
        / "best_model.joblib"
    )

    assert best_model_path.exists()

    print(
        f"{'best_model.joblib':<30}: PASSED"
    )

    # ======================================================
    # LOAD BEST MODEL
    # ======================================================

    loaded_model = repository.load_model(
        workspace_id=workspace_id,
    )

    assert loaded_model is not None

    print(
        f"{'Best model loading':<30}: PASSED"
    )

    # ======================================================
    # VERIFY MODEL TYPE
    # ======================================================

    expected_model_type = (
        best_model
        .trained_model
        .model
        .__class__
    )

    assert (
        type(loaded_model)
        is expected_model_type
    )

    print(
        f"{'Best model type':<30}: PASSED"
    )

    # ======================================================
    # LOAD METADATA
    # ======================================================

    metadata = repository.load_metadata(
        workspace_id=workspace_id,
    )

    assert metadata is not None

    print(
        f"{'Metadata loading':<30}: PASSED"
    )

    # ======================================================
    # VERIFY METADATA
    # ======================================================

    assert (
        metadata.target_column
        == target_column
    )

    assert (
        metadata.task_type
        == result.ml.task_type.value
    )

    assert (
        metadata.best_model
        == expected_best_model
    )

    print(
        f"{'Target column':<30}: PASSED"
    )

    print(
        f"{'Task type':<30}: PASSED"
    )

    print(
        f"{'Best model metadata':<30}: PASSED"
    )

    # ======================================================
    # VERIFY METRICS
    # ======================================================

    evaluated_metrics = (
        best_model.metrics
    )

    assert (
        metadata.metrics.rmse
        == evaluated_metrics.rmse
    )

    assert (
        metadata.metrics.r2
        == evaluated_metrics.r2
    )

    print(
        f"{'RMSE metadata':<30}: PASSED"
    )

    print(
        f"{'R2 metadata':<30}: PASSED"
    )

    # ======================================================
    # FINAL VALIDATION
    # ======================================================

    print()
    print("=" * 70)
    print("ML MODEL PERSISTENCE VALIDATION")
    print("=" * 70)

    print(
        "Candidate Models       : PASSED"
    )

    print(
        "Best Model Artifact    : PASSED"
    )

    print(
        "Model Loading          : PASSED"
    )

    print(
        "Model Type Validation  : PASSED"
    )

    print(
        "Metadata Loading       : PASSED"
    )

    print(
        "Metadata Validation    : PASSED"
    )

    print(
        "Metrics Validation     : PASSED"
    )

    print()
    print("=" * 70)
    print(
        "ML MODEL PERSISTENCE "
        "EXECUTED SUCCESSFULLY"
    )
    print("=" * 70)


if __name__ == "__main__":
    main()