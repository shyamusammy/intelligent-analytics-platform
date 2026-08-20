from fastapi import APIRouter

from app.schemas.etl import ETLProfile
from app.schemas.pipeline import DatasetPipelineRequest
from app.services.etl.pipeline.etl_pipeline import ETLPipeline


router = APIRouter(prefix="/etl", tags=["ETL"])
pipeline = ETLPipeline()


@router.post("/run", response_model=ETLProfile, summary="Profile a dataset")
def run_etl(request: DatasetPipelineRequest) -> ETLProfile:
    """Run schema detection, profiling, and data-quality analysis."""

    return pipeline.run(
        workspace_id=request.workspace_id,
        dataset_id=request.dataset_id,
    )
