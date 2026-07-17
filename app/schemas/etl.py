from enum import Enum

from pydantic import BaseModel


class DetectedDataType(str, Enum):
    """
    Semantic data types recognized by the ETL Engine.
    """

    INTEGER = "integer"

    FLOAT = "float"

    BOOLEAN = "boolean"

    DATETIME = "datetime"

    CATEGORICAL = "categorical"

    TEXT = "text"

    MIXED = "mixed"

    UNKNOWN = "unknown"


class ColumnProfile(BaseModel):
    """
    Describes a single dataset column.
    """

    name: str

    pandas_dtype: str

    detected_type: DetectedDataType

    nullable: bool

    unique: bool

    null_count: int


class SchemaProfile(BaseModel):
    """
    Represents the detected schema of a dataset.
    """

    total_columns: int

    columns: list[ColumnProfile]


class MissingValueSummary(BaseModel):
    """
    Summary of missing values in a dataset.
    """

    total_missing_values: int

    columns_with_missing_values: int

    missing_by_column: dict[str, int]


class DuplicateSummary(BaseModel):
    """
    Summary of duplicate rows.
    """

    duplicate_rows: int

    duplicate_percentage: float


class StatisticsProfile(BaseModel):
    """
    Summary statistics for numeric columns.
    """

    statistics: dict[str, dict[str, float]]


class OutlierSummary(BaseModel):
    """
    Summary of detected outliers.
    """

    total_outliers: int

    outliers_by_column: dict[str, int]


class QualityProfile(BaseModel):
    """
    Overall dataset quality.
    """

    quality_score: float

    missing_penalty: float

    duplicate_penalty: float

    outlier_penalty: float


class ETLProfile(BaseModel):
    """
    Complete ETL profiling result for a dataset.
    """

    schema_profile: SchemaProfile

    missing_values: MissingValueSummary

    duplicates: DuplicateSummary

    statistics: StatisticsProfile

    outliers: OutlierSummary

    quality: QualityProfile