from fastapi import APIRouter

from app.api.serializers import platform_result_response
from app.schemas.pipeline import PlatformRunRequest
from app.services.pipeline import PlatformPipeline


router = APIRouter(prefix="/pipeline", tags=["Platform Pipeline"])
pipeline = PlatformPipeline()


@router.post("/run", summary="Run the complete analytics pipeline")
def run_pipeline(request: PlatformRunRequest) -> dict:
    """Execute ETL, analytics, and ML in their required order."""

    result = pipeline.run(
        workspace_id=request.workspace_id,
        dataset_id=request.dataset_id,
        target_column=request.target_column,
    )
    return platform_result_response(result)
