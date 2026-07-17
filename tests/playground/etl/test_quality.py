from app.services.etl.loader.dataset_loader import DatasetLoaderService

from app.services.etl.profiling.missing_value_analyzer import (
    MissingValueAnalyzer,
)

from app.services.etl.profiling.duplicate_detector import (
    DuplicateDetector,
)

from app.services.etl.quality.outlier_detector import (
    OutlierDetector,
)

from app.services.etl.quality.quality_score import (
    QualityScoreService,
)

loader = DatasetLoaderService()

df = loader.load(
    "ws_001",
    "ds_001",
)

missing = MissingValueAnalyzer().analyze(df)

duplicates = DuplicateDetector().analyze(df)

outliers = OutlierDetector().detect(df)

quality = QualityScoreService().calculate(

    total_rows=len(df),

    total_columns=len(df.columns),

    missing=missing,

    duplicates=duplicates,

    outliers=outliers,
)

print("=" * 80)

print(outliers.model_dump())

print("=" * 80)

print(quality.model_dump())