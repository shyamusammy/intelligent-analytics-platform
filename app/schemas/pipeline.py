from pydantic import BaseModel

from app.schemas.analytics import AnalyticsEngineResult
from app.schemas.etl import ETLProfile
from app.schemas.ml import MLEngineResult
from app.schemas.cleaning import CleaningReport
from app.schemas.dashboard import DashboardResult


class PlatformPipelineResult(BaseModel):
    etl: ETLProfile
    cleaning: CleaningReport | None = None
    analytics: AnalyticsEngineResult
    ml: MLEngineResult | None = None
    dashboard: DashboardResult | None = None
    status: str = "success"
    warnings: list[str] = []


class DatasetPipelineRequest(BaseModel):
    """Identifies a dataset to process within a workspace."""

    workspace_id: str
    dataset_id: str


class PlatformRunRequest(DatasetPipelineRequest):
    """Request for a complete ETL, analytics, and ML run."""

    target_column: str | None = None
