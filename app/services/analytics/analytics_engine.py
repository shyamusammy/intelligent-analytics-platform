import pandas as pd

from app.repositories.profiling_repository import (
    ProfilingRepository,
)

from app.schemas.context import (
    KnowledgeContext,
)

from app.schemas.etl import (
    ETLProfile,
)

from app.repositories.dataset_repository import (
    DatasetRepository,
)

from app.repositories.analytics_repository import (
    AnalyticsRepository,
)

from app.services.analytics.statistics_service import (
    StatisticsService,
)

from app.services.analytics.kpi_service import (
    KPIService,
)

from app.services.analytics.correlation_service import (
    CorrelationService,
)

from app.services.analytics.trend_service import (
    TrendService,
)

from app.services.analytics.segmentation_service import (
    SegmentationService,
)

from app.services.analytics.insight_service import (
    InsightService,
)

from app.schemas.analytics import (
    AnalyticsEngineResult,
)


class AnalyticsEngine:
    """
    Orchestrates the complete analytics workflow.

    Responsibilities
    ----------------
    - Load dataset
    - Execute analytics services
    - Persist analytics artifacts
    - Return aggregated analytics result

    This engine contains NO business logic.
    """

    def __init__(
        self,
        dataset_repository: DatasetRepository | None = None,
        analytics_repository: AnalyticsRepository | None = None,
        profiling_repository: ProfilingRepository | None = None,
    ) -> None:

        self._dataset_repository = (
            dataset_repository or DatasetRepository()
        )

        self._analytics_repository = (
            analytics_repository or AnalyticsRepository()
        )

        self._profiling_repository = (
            profiling_repository or ProfilingRepository()
        )

        self._statistics_service = (
            StatisticsService()
        )

        self._kpi_service = (
            KPIService()
        )

        self._correlation_service = (
            CorrelationService()
        )

        self._segmentation_service = (
            SegmentationService()
        )

        self._trend_service = (
            TrendService()
        )

        self._insight_service = (
            InsightService()
        )

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def run(
        self,
        workspace_id: str,
        dataset_id: str,
        use_cleaned_dataset: bool = False,
    ) -> AnalyticsEngineResult:
        """
        Execute the complete analytics workflow.
        """

        dataframe = self._load_dataset(
            workspace_id,
            dataset_id,
            use_cleaned_dataset,
        )

        etl_profile = self._load_etl_profile(
            workspace_id,
        )

        knowledge = self._create_knowledge_context(
            etl_profile,
        )

        result = self._run_analytics(
            dataframe=dataframe,
            knowledge=knowledge,
        )

        self._save_results(
            workspace_id,
            result,
        )

        return result

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _load_dataset(
        self,
        workspace_id: str,
        dataset_id: str,
        use_cleaned_dataset: bool,
    ) -> pd.DataFrame:
        """
        Load the dataset into a pandas DataFrame.
        """

        if use_cleaned_dataset:
            return self._dataset_repository.load_cleaned_dataframe(
                workspace_id,
                dataset_id,
            )

        return self._dataset_repository.load_dataframe(
            workspace_id,
            dataset_id,
        )

    def _run_analytics(
        self,
        dataframe: pd.DataFrame,
        knowledge: KnowledgeContext,
    ) -> AnalyticsEngineResult:
        """
        Execute all analytics services.
        """
        statistics = (
            self._statistics_service.run(
                dataframe= dataframe,
                knowledge= knowledge,
            )
        )

        kpis = (
            self._kpi_service.run(
                dataframe,
            )
        )

        correlations = (
            self._correlation_service.run(
                dataframe=dataframe,
                knowledge=knowledge,
            )
        )

        trends = (
            self._trend_service.run(
                dataframe=dataframe,
                knowledge=knowledge,
            )
        )

        segmentation = (
            self._segmentation_service.run(
                dataframe=dataframe,
                knowledge=knowledge,
            )
        )

        insights = (
            self._insight_service.run(
                statistics=statistics,
                kpis=kpis,
                correlations=correlations,
                trends=trends,
                segmentation=segmentation,
            )
        )

        return AnalyticsEngineResult(
            statistics=statistics,
            kpis=kpis,
            correlations=correlations,
            trends=trends,
            segmentation=segmentation,
            insights=insights,
        )

    def _save_results(
        self,
        workspace_id: str,
        result: AnalyticsEngineResult,
    ) -> None:
        """
        Persist analytics artifacts.
        """

        self._analytics_repository.save(
            workspace_id,
            result,
        )

    def _load_etl_profile(
        self,
        workspace_id: str,
    ) -> ETLProfile:
        """
        Load the ETL profile generated during the ETL stage.
        """

        return self._profiling_repository.load(
            workspace_id,
        )

    def _create_knowledge_context(
        self,
        etl_profile: ETLProfile,
    ) -> KnowledgeContext:
        """
        Create the shared knowledge context for downstream services.
        """

        return KnowledgeContext(
            etl_profile=etl_profile,
        )
