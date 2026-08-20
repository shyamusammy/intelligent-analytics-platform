from app.schemas.context import KnowledgeContext
from app.schemas.pipeline import PlatformPipelineResult
from app.services.analytics.analytics_engine import AnalyticsEngine
from app.services.etl.pipeline.etl_pipeline import ETLPipeline
from app.services.ml.engine import MLEngine
from app.services.cleaning import CleaningEngine
from app.services.dashboard.dashboard_service import DashboardService
from app.services.ml.target_selector import TargetSelector
from app.repositories.dataset_repository import DatasetRepository


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
        cleaning_engine: CleaningEngine | None = None,
        dashboard_service: DashboardService | None = None,
    ) -> None:
        self._etl_pipeline = etl_pipeline or ETLPipeline()
        self._analytics_engine = analytics_engine or AnalyticsEngine()
        self._ml_engine = ml_engine or MLEngine()
        self._cleaning_engine = cleaning_engine or CleaningEngine()
        self._dashboard_service = dashboard_service or DashboardService()
        self._target_selector = TargetSelector()
        self._dataset_repository = DatasetRepository()

    def run(
        self,
        workspace_id: str,
        dataset_id: str,
        target_column: str | None = None,
    ) -> PlatformPipelineResult:
        """
        Execute the complete platform pipeline.

        Flow:
            ETL → Cleaning → Analytics → ML
        """

        # Stage 1: ETL
        etl_result = self._etl_pipeline.run(
            workspace_id=workspace_id,
            dataset_id=dataset_id,
        )

        target_column = target_column or self._target_selector.select(
            self._dataset_repository.load_dataframe(workspace_id, dataset_id)
        )

        cleaning_result = self._cleaning_engine.run(
            workspace_id=workspace_id,
            dataset_id=dataset_id,
            profile=etl_result,
            target_column=target_column,
        )

        # Stage 2: Analytics
        analytics_result = self._analytics_engine.run(
            workspace_id=workspace_id,
            dataset_id=dataset_id,
            use_cleaned_dataset=True,
        )

        # Build shared knowledge for downstream ML
        knowledge = KnowledgeContext(
            etl_profile=etl_result,
            analytics_result=analytics_result,
        )

        # Stage 3: Machine Learning
        ml_result = None
        warnings: list[str] = []
        if target_column:
            ml_result = self._ml_engine.run(
                workspace_id=workspace_id,
                dataset_id=dataset_id,
                target_column=target_column,
                knowledge=knowledge,
                use_cleaned_dataset=True,
            )
            if not ml_result.validation.valid:
                warnings.append("ML skipped because target validation failed.")
        else:
            warnings.append("ML skipped because no suitable target column was detected.")

        dashboard_result = self._dashboard_service.run(workspace_id, dataset_id)

        return PlatformPipelineResult(
            etl=etl_result,
            cleaning=cleaning_result,
            analytics=analytics_result,
            ml=ml_result,
            dashboard=dashboard_result,
            status="success_with_warnings" if warnings else "success",
            warnings=warnings,
        )
