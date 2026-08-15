from pathlib import Path
import shutil
from datetime import datetime
from app.repositories.dataset_repository import DatasetRepository
from app.repositories.workspace_repository import WorkspaceRepository
from app.services.ml.engine import MLEngine
from app.services.etl.pipeline.etl_pipeline import ETLPipeline
from app.services.analytics.analytics_engine import AnalyticsEngine
from app.schemas.context import KnowledgeContext


def prepare_workspace() -> tuple[str, str]:
    workspace_id = "ws_ml_engine_test"
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
            workspace_root
        )

    # ======================================================
    # CREATE WORKSPACE
    # ======================================================

    workspace_repository = WorkspaceRepository()
    dataset_repository = DatasetRepository()

    workspace_metadata = {
        "workspace_id": workspace_id,
        "name": "ML Engine Unit Test",
    }

    workspace_path = (
        workspace_repository.create_workspace(
            workspace_id,
            workspace_metadata,
        )
    )

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
        "display_name": sample_dataset.stem,
        "original_filename": sample_dataset.name,
        "extension": sample_dataset.suffix,
        "size_mb" : (sample_dataset.stat().st_size/(1024*1024)),
        "active": True,
        "status" : "uploaded",
        "uploaded_at" : datetime.now().isoformat(),
    }

    dataset_repository.save_metadata(
        dataset_path,
        dataset_metadata,
    )

    return workspace_id, dataset_id


def build_knowledge_context(
    workspace_id: str,
    dataset_id: str,
) -> KnowledgeContext:

    etl_pipeline = ETLPipeline()

    etl_result = etl_pipeline.run(
        workspace_id=workspace_id,
        dataset_id=dataset_id,
    )

    analytics_engine = AnalyticsEngine()

    analytics_result = analytics_engine.run(
        workspace_id,
        dataset_id,
    )

    return KnowledgeContext(
        etl_profile=etl_result,
        analytics_result=analytics_result,
    )


def test_ml_engine_complete_workflow():

    workspace_id, dataset_id = prepare_workspace()

    knowledge = build_knowledge_context(
        workspace_id,
        dataset_id,
    )

    engine = MLEngine()

    result = engine.run(
        workspace_id=workspace_id,
        dataset_id=dataset_id,
        target_column="Revenue",
        knowledge=knowledge,
    )

    # ======================================================
    # ENGINE RESULT
    # ======================================================

    assert result is not None

    # ======================================================
    # VALIDATION
    # ======================================================

    assert result.validation.valid is True

    # ======================================================
    # TASK DETECTION
    # ======================================================

    assert result.task_type is not None

    assert result.task_type.value == "regression"

    # ======================================================
    # MODEL SELECTION
    # ======================================================

    assert len(result.estimators) == 2

    # ======================================================
    # TRAINING
    # ======================================================

    assert result.train_result is not None

    assert len(
        result.train_result.models
    ) == 2

    # ======================================================
    # EVALUATION
    # ======================================================

    assert result.evaluation_result is not None

    assert len(
        result.evaluation_result.models
    ) == 2

    assert (
        result.evaluation_result.best_model
        is not None
    )

    # ======================================================
    # BEST MODEL
    # ======================================================

    best_model = (
        result.evaluation_result.best_model
    )

    assert (
        best_model.trained_model.estimator
        in result.estimators
    )

    # ======================================================
    # MODEL ARTIFACTS
    # ======================================================

    models_path = (
        Path("workspaces")
        / workspace_id
        / "artifacts"
        / "models"
    )

    assert (
        models_path
        / "linear_regression.joblib"
    ).exists()

    assert (
        models_path
        / "random_forest_regressor.joblib"
    ).exists()

    assert (
        models_path
        / "best_model.joblib"
    ).exists()

    # ======================================================
    # METADATA
    # ======================================================

    metadata_path = (
        models_path
        / "model_metadata.json"
    )

    assert metadata_path.exists()

    metadata = MLEngine()._model_repository.load_metadata(
        workspace_id
    )

    assert metadata.target_column == "Revenue"

    assert metadata.task_type == "regression"

    assert (
        metadata.best_model
        == best_model.trained_model.estimator.value
    )