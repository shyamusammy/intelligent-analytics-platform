"""Product-facing one-request analysis workflow."""

from fastapi import APIRouter, File, Form, UploadFile

from app.api.serializers import platform_result_response
from app.services.data_manager.manager import DataManager
from app.services.pipeline import PlatformPipeline
from app.services.workspace_service import WorkspaceService


router = APIRouter(prefix="/analysis", tags=["Complete Analysis"])
workspace_service = WorkspaceService()
data_manager = DataManager()
pipeline = PlatformPipeline()


@router.post("/run", summary="Upload a dataset and run the complete analysis")
async def run_complete_analysis(
    file: UploadFile = File(...),
    target_column: str | None = Form(default=None),
) -> dict:
    """Create internal workspace/dataset IDs and keep them out of the product flow."""

    display_name = file.filename.rsplit(".", 1)[0] if file.filename else "Uploaded dataset"
    workspace = workspace_service.create_workspace(
        name=f"Analysis: {display_name}",
        description="Automatically generated analysis workspace",
        industry="General",
        objective="Automated dataset analysis",
    )
    dataset = await data_manager.register_dataset(
        workspace_id=workspace.workspace_id,
        file=file,
        display_name=display_name,
    )
    result = pipeline.run(
        workspace_id=workspace.workspace_id,
        dataset_id=dataset.dataset_id,
        target_column=target_column or None,
    )
    return platform_result_response(result)
