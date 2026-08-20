from fastapi import APIRouter

from app.schemas.analytics import AnalyticsEngineResult
from app.schemas.pipeline import DatasetPipelineRequest
from app.services.analytics.analytics_engine import AnalyticsEngine


router = APIRouter(prefix="/analytics", tags=["Analytics"])
engine = AnalyticsEngine()


@router.post("/run", response_model=AnalyticsEngineResult, summary="Generate dataset analytics")
def run_analytics(request: DatasetPipelineRequest) -> AnalyticsEngineResult:
    """Generate and persist analytical results from an ETL profile."""

    return engine.run(
        workspace_id=request.workspace_id,
        dataset_id=request.dataset_id,
    )
