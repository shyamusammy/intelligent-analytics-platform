from pydantic import BaseModel

from app.schemas.etl import ETLProfile
from app.schemas.analytics import AnalyticsEngineResult
from app.schemas.ml import MLEngineResult


class KnowledgeContext(BaseModel):
    """
    Shared knowledge generated throughout the platform pipeline.

    This object allows downstream engines and services to consume
    previously generated artifacts without expanding method signatures.
    """

    etl_profile: ETLProfile | None = None

    analytics_result: AnalyticsEngineResult | None = None

    ml_result: MLEngineResult | None = None