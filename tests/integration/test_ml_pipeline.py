from datetime import datetime
from pathlib import Path
import shutil

from app.repositories.dataset_repository import (
    DatasetRepository,
)

from app.repositories.workspace_repository import (
    WorkspaceRepository,
)

from app.schemas.context import (
    KnowledgeContext,
)

from app.services.analytics.analytics_engine import (
    AnalyticsEngine,
)

from app.services.etl.pipeline.etl_pipeline import (
    ETLPipeline,
)

from app.services.ml.engine import (
    MLEngine,
)


def main() -> None:

    workspace_id = "ws_ml_pipeline"
    dataset_id = "ds_sales"

    sample_dataset = Path(
        "tests/data/sales.xlsx"
    )

    # ======================================================
    # CLEAN PREVIOUS WORKSPACE
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
    # CREATE REPOSITORIES
    # ======================================================

    workspace_repository = (
        WorkspaceRepository()
    )

    dataset_repository = (
        DatasetRepository()
    )

    # ======================================================
    # CREATE WORKSPACE
    # ======================================================

    workspace_metadata = {
        "workspace_id": workspace_id,
        "name": "ML Pipeline Test Workspace",
    }

    workspace_path = (
        workspace_repository.create_workspace(
            workspace_id,
            workspace_metadata,
        )
    )

    # ======================================================
    # CREATE DATASET
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
        "display_name": "Sales Dataset",
        "original_filename": sample_dataset.name,
        "extension": sample_dataset.suffix,
        "size_mb": (
            sample_dataset.stat().st_size
            / (1024 * 1024)
        ),
        "active": True,
        "status": "uploaded",
        "uploaded_at": datetime.now().isoformat(),
    }

    dataset_repository.save_metadata(
        dataset_path,
        dataset_metadata,
    )

    # ======================================================
    # STEP 1 : ETL PIPELINE
    # ======================================================

    print("=" * 70)
    print("STEP 1 : ETL PIPELINE")
    print("=" * 70)

    etl_pipeline = ETLPipeline()

    etl_profile = etl_pipeline.run(
        workspace_id=workspace_id,
        dataset_id=dataset_id,
    )

    print(
        f"Quality Score : "
        f"{etl_profile.quality.quality_score}"
    )

    print(
        f"Detected Columns : "
        f"{etl_profile.schema_profile.total_columns}"
    )

    # ======================================================
    # STEP 2 : ANALYTICS PIPELINE
    # ======================================================

    print()
    print("=" * 70)
    print("STEP 2 : ANALYTICS ENGINE")
    print("=" * 70)

    analytics_engine = AnalyticsEngine()

    analytics_result = analytics_engine.run(
        workspace_id=workspace_id,
        dataset_id=dataset_id,
    )

    print(
        f"Numeric Columns : "
        f"{len(analytics_result.statistics.numeric_statistics)}"
    )

    print(
        f"Categorical Columns : "
        f"{len(analytics_result.statistics.categorical_statistics)}"
    )

    print(
        f"Correlation Pairs : "
        f"{len(analytics_result.correlations.correlations)}"
    )

    print(
        f"Trend Metrics : "
        f"{len(analytics_result.trends.trends)}"
    )

    print(
        f"Segments : "
        f"{len(analytics_result.segmentation.segments)}"
    )

    print(
        f"Business Insights : "
        f"{len(analytics_result.insights.insights)}"
    )

    # ======================================================
    # CREATE KNOWLEDGE CONTEXT
    # ======================================================

    knowledge = KnowledgeContext(
        etl_profile=etl_profile,
    )

    # ======================================================
    # STEP 3 : ML ENGINE
    # ======================================================

    print()
    print("=" * 70)
    print("STEP 3 : ML ENGINE")
    print("=" * 70)

    ml_engine = MLEngine()

    ml_result = ml_engine.run(
        workspace_id=workspace_id,
        dataset_id=dataset_id,
        target_column="Revenue",
        knowledge=knowledge,
    )

    # ======================================================
    # ML VALIDATION
    # ======================================================

    print(
        f"Validation Passed : "
        f"{ml_result.validation.valid}"
    )

    if ml_result.validation.errors:

        print("Validation Errors:")

        for error in ml_result.validation.errors:
            print(
                f"  - {error}"
            )

    if ml_result.validation.warnings:

        print("Validation Warnings:")

        for warning in ml_result.validation.warnings:
            print(
                f"  - {warning}"
            )

    # ======================================================
    # ML SUMMARY
    # ======================================================

    print(
        f"Detected ML Task : "
        f"{ml_result.task_type.value}"
    )

    print(
        f"Candidate Models Selected : "
        f"{len(ml_result.estimators)}"
    )

    if ml_result.train_result is not None:

        print(
            f"Models Successfully Trained : "
            f"{len(ml_result.train_result.models)}"
        )

    if ml_result.evaluation_result is not None:

        print(
            f"Models Successfully Evaluated : "
            f"{len(ml_result.evaluation_result.models)}"
        )

        best_model = (
            ml_result.evaluation_result.best_model
        )

        print(
            f"Best Performing Model : "
            f"{best_model.trained_model.estimator.value}"
        )

    # ======================================================
    # MODEL EVALUATION
    # ======================================================

    if ml_result.evaluation_result is not None:

        print()
        print("=" * 70)
        print("MODEL EVALUATION")
        print("=" * 70)

        for evaluated_model in (
            ml_result.evaluation_result.models
        ):

            estimator = (
                evaluated_model
                .trained_model
                .estimator
                .value
            )

            print()
            print(
                f"Estimator : {estimator}"
            )

            if (
                ml_result.task_type.value
                == "regression"
            ):

                metrics = (
                    evaluated_model.metrics
                )

                print(
                    f"R² Score : "
                    f"{metrics.r2:.4f}"
                )

                print(
                    f"RMSE     : "
                    f"{metrics.rmse:.4f}"
                )

            else:

                metrics = (
                    evaluated_model.metrics
                )

                print(
                    f"Accuracy : "
                    f"{metrics.accuracy:.4f}"
                )

                print(
                    f"F1 Score : "
                    f"{metrics.f1_score:.4f}"
                )

    # ======================================================
    # FINAL PIPELINE VALIDATION
    # ======================================================

    assert etl_profile is not None

    assert analytics_result is not None

    assert ml_result is not None

    assert ml_result.validation.valid

    assert ml_result.task_type is not None

    assert len(
        ml_result.estimators
    ) > 0

    assert ml_result.train_result is not None

    assert len(
        ml_result.train_result.models
    ) > 0

    assert ml_result.evaluation_result is not None

    assert len(
        ml_result.evaluation_result.models
    ) > 0

    assert (
        ml_result.evaluation_result.best_model
        is not None
    )

    print()
    print("=" * 70)
    print("ML PIPELINE EXECUTED SUCCESSFULLY")
    print("=" * 70)


if __name__ == "__main__":
    main()