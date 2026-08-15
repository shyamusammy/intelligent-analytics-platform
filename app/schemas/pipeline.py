from pydantic import BaseModel

from app.schemas.analytics import AnalyticsEngineResult
from app.schemas.etl import ETLProfile
from app.schemas.ml import MLEngineResult


class PlatformPipelineResult(BaseModel):
    etl: ETLProfile
    analytics: AnalyticsEngineResult
    ml: MLEngineResult | None = None