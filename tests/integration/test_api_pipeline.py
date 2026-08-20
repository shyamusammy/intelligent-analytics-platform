from pathlib import Path
import shutil
import asyncio
import json

from fastapi import UploadFile

from app.api.analytics import run_analytics
from app.api.data_manager import upload_dataset
from app.api.etl import run_etl
from app.api.ml import run_ml
from app.api.pipeline import run_pipeline
from app.api.workspace import create_workspace
from app.schemas.ml import TrainRequest
from app.schemas.pipeline import DatasetPipelineRequest, PlatformRunRequest
from app.schemas.workspace import WorkspaceCreate


def test_complete_pipeline_is_available_through_api() -> None:
    """The public API can execute every backend pipeline stage."""

    workspace_id = None
    try:
        workspace = create_workspace(
            WorkspaceCreate(
                name="API Pipeline Test",
                description="End-to-end API coverage",
                industry="Retail",
                objective="Validate the platform pipeline",
            )
        )
        workspace_id = workspace.workspace_id

        with Path("tests/data/sales.xlsx").open("rb") as dataset:
            upload = asyncio.run(
                upload_dataset(
                    workspace_id=workspace_id,
                    display_name="Sales data",
                    file=UploadFile(dataset, filename="sales.xlsx"),
                )
            )
        dataset_request = DatasetPipelineRequest(
            workspace_id=workspace_id,
            dataset_id=upload.dataset_id,
        )

        etl_response = run_etl(dataset_request)
        assert etl_response.quality.quality_score >= 0

        analytics_response = run_analytics(dataset_request)
        assert analytics_response.statistics.dataset_summary.total_rows > 0

        ml_response = run_ml(
            TrainRequest(
                workspace_id=workspace_id,
                dataset_id=upload.dataset_id,
                target_column="Revenue",
            )
        )
        assert ml_response["best_model"] is not None

        pipeline_response = run_pipeline(
            PlatformRunRequest(
                workspace_id=workspace_id,
                dataset_id=upload.dataset_id,
                target_column="Revenue",
            )
        )
        assert pipeline_response["etl"]["schema_profile"]["total_columns"] > 0
        assert pipeline_response["analytics"]["statistics"]["dataset_summary"]["total_rows"] > 0
        assert pipeline_response["ml"]["best_model"] is not None
        json.dumps(pipeline_response)
    finally:
        if workspace_id:
            shutil.rmtree(Path("workspaces") / workspace_id, ignore_errors=True)
