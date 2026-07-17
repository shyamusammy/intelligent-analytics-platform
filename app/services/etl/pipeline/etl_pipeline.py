from app.schemas.etl import ETLProfile

from app.services.etl.loader.dataset_loader import (
    DatasetLoaderService,
)

from app.services.etl.schema.schema_detector import (
    SchemaDetector,
)

from app.services.etl.profiling.missing_value_analyzer import (
    MissingValueAnalyzer,
)

from app.services.etl.profiling.duplicate_detector import (
    DuplicateDetector,
)

from app.services.etl.profiling.statistical_profiler import (
    StatisticalProfiler,
)

from app.services.etl.quality.outlier_detector import (
    OutlierDetector,
)

from app.services.etl.quality.quality_score import (
    QualityScoreService,
)

from app.repositories.profiling_repository import (
    ProfilingRepository,
)


class ETLPipeline:
    """
    Executes the complete ETL profiling pipeline.
    """

    def __init__(self):

        self.loader = DatasetLoaderService()

        self.schema_detector = SchemaDetector()

        self.missing_analyzer = MissingValueAnalyzer()

        self.duplicate_detector = DuplicateDetector()

        self.statistics_profiler = StatisticalProfiler()

        self.outlier_detector = OutlierDetector()

        self.quality_service = QualityScoreService()

        self.profiling_repository = ProfilingRepository()

    def run(
        self,
        workspace_id: str,
        dataset_id: str,
    ) -> ETLProfile:
        """
        Execute the ETL profiling pipeline.
        """

        dataframe = self.loader.load(
            workspace_id,
            dataset_id,
        )

        schema = self.schema_detector.detect(
            dataframe,
        )

        missing = self.missing_analyzer.analyze(
            dataframe,
        )

        duplicates = self.duplicate_detector.analyze(
            dataframe,
        )

        statistics = self.statistics_profiler.profile(
            dataframe,
        )

        outliers = self.outlier_detector.detect(
            dataframe,
        )

        quality = self.quality_service.calculate(
            total_rows=len(dataframe),
            total_columns=len(dataframe.columns),
            missing=missing,
            duplicates=duplicates,
            outliers=outliers,
        )

        profile = ETLProfile(

            schema_profile=schema,

            missing_values=missing,

            duplicates=duplicates,

            statistics=statistics,

            outliers=outliers,

            quality=quality,
        )

        self.profiling_repository.save(

            workspace_id,

            profile,
        )

        return profile