from app.schemas.context import KnowledgeContext
from app.schemas.pipeline import PlatformPipelineResult
from app.services.analytics.analytics_engine import AnalyticsEngine
from app.services.etl.pipeline.etl_pipeline import ETLPipeline
from app.services.ml.engine import MLEngine


class PlatformPipeline:
    """
    Application-level orchestrator for the analytics platform.

    Coordinates the ETL, Analytics, and ML engines without
    implementing domain-specific logic itself.
    """

    def __init__(
        self,
        etl_pipeline: ETLPipeline | None = None,
        analytics_engine: AnalyticsEngine | None = None,
        ml_engine: MLEngine | None = None,
    ) -> None:
        self._etl_pipeline = etl_pipeline or ETLPipeline()
        self._analytics_engine = analytics_engine or AnalyticsEngine()
        self._ml_engine = ml_engine or MLEngine()

    def run(
        self,
        workspace_id: str,
        dataset_id: str,
        target_column: str,
    ) -> PlatformPipelineResult:
        """
        Execute the complete platform pipeline.

        Flow:
            ETL → Analytics → KnowledgeContext → ML
        """

        # Stage 1: ETL
        etl_result = self._etl_pipeline.run(
            workspace_id=workspace_id,
            dataset_id=dataset_id,
        )

        # Stage 2: Analytics
        analytics_result = self._analytics_engine.run(
            workspace_id=workspace_id,
            dataset_id=dataset_id,
        )

        # Build shared knowledge for downstream ML
        knowledge = KnowledgeContext(
            etl_profile=etl_result,
            analytics_result=analytics_result,
        )

        # Stage 3: Machine Learning
        ml_result = self._ml_engine.run(
            workspace_id=workspace_id,
            dataset_id=dataset_id,
            target_column=target_column,
            knowledge=knowledge,
        )

        return PlatformPipelineResult(
            etl=etl_result,
            analytics=analytics_result,
            ml=ml_result,
        )