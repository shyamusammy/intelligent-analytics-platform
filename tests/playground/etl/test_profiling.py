from app.services.etl.loader.dataset_loader import DatasetLoaderService

from app.services.etl.profiling.missing_value_analyzer import (
    MissingValueAnalyzer,
)

from app.services.etl.profiling.duplicate_detector import (
    DuplicateDetector,
)

from app.services.etl.profiling.statistical_profiler import (
    StatisticalProfiler,
)

loader = DatasetLoaderService()

df = loader.load(
    "ws_001",
    "ds_001",
)

print("=" * 80)

print(
    MissingValueAnalyzer().analyze(df)
)

print("=" * 80)

print(
    DuplicateDetector().analyze(df)
)

print("=" * 80)

print(
    StatisticalProfiler().profile(df)
)