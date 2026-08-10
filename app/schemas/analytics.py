from pydantic import BaseModel
from pydantic import Field

from app.core.enums import (
    CorrelationDirection,
    CorrelationMethod,
    CorrelationStrength,
    InsightCategory,
    InsightSeverity,
    TrendDirection,
)


# ============================================================
# Reusable Models
# ============================================================

class DatasetSummary(BaseModel):
    total_rows: int
    total_columns: int

    numeric_columns: int
    categorical_columns: int
    datetime_columns: int

    text_columns: int
    missing_cells: int
    duplicate_rows: int


class NumericColumnStatistics(BaseModel):
    column_name: str

    mean: float
    median: float

    minimum: float
    maximum: float

    std_dev: float
    variance: float

    skewness: float
    kurtosis: float


class CategoricalColumnStatistics(BaseModel):
    column_name: str

    unique_values: int

    most_frequent: str | None = None

    most_frequent_count: int | None = None


class KPI(BaseModel):
    name: str

    value: float | int | str

    unit: str | None = None

    description: str | None = None


class CorrelationPair(BaseModel):
    column_a: str

    column_b: str

    coefficient: float

    method: CorrelationMethod

    strength: CorrelationStrength

    direction: CorrelationDirection


class TrendMetric(BaseModel):
    metric_name: str

    first_value: float

    last_value: float

    change: float

    percentage_change: float

    direction: TrendDirection


class Segment(BaseModel):
    column_name: str

    category: str

    count: int

    percentage: float


class Insight(BaseModel):
    title: str

    description: str

    category: InsightCategory

    severity: InsightSeverity


# ============================================================
# Service Results
# ============================================================

class StatisticsResult(BaseModel):
    dataset_summary: DatasetSummary

    numeric_statistics: list[NumericColumnStatistics] = Field(
        default_factory=list
    )

    categorical_statistics: list[CategoricalColumnStatistics] = Field(
        default_factory=list
    )


class KPIResult(BaseModel):
    metrics: list[KPI] = Field(
        default_factory=list
    )


class CorrelationResult(BaseModel):
    correlations: list[CorrelationPair] = Field(
        default_factory=list
    )


class TrendResult(BaseModel):
    datetime_column: str | None = None

    trends: list[TrendMetric] = Field(
        default_factory=list
    )


class SegmentationResult(BaseModel):
    segments: list[Segment] = Field(
        default_factory=list
    )


class InsightResult(BaseModel):
    insights: list[Insight] = Field(
        default_factory=list
    )


# ============================================================
# Analytics Engine Result
# ============================================================

class AnalyticsEngineResult(BaseModel):
    
    statistics: StatisticsResult

    kpis: KPIResult

    correlations: CorrelationResult

    trends: TrendResult

    segmentation: SegmentationResult

    insights: InsightResult