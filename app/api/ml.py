from fastapi import APIRouter

from app.repositories.analytics_repository import AnalyticsRepository
from app.repositories.profiling_repository import ProfilingRepository
from app.schemas.context import KnowledgeContext
from app.schemas.ml import TrainRequest
from app.services.ml.engine import MLEngine

from app.api.serializers import ml_result_response


router = APIRouter(prefix="/ml", tags=["Machine Learning"])
engine = MLEngine()
profiling_repository = ProfilingRepository()
analytics_repository = AnalyticsRepository()


@router.post("/run", summary="Train and evaluate machine-learning models")
def run_ml(request: TrainRequest) -> dict:
    """Train candidate models using artifacts from ETL and analytics."""

    knowledge = KnowledgeContext(
        etl_profile=profiling_repository.load(request.workspace_id),
        analytics_result=analytics_repository.load(request.workspace_id),
    )
    result = engine.run(
        workspace_id=request.workspace_id,
        dataset_id=request.dataset_id,
        target_column=request.target_column,
        knowledge=knowledge,
    )
    return ml_result_response(result)
