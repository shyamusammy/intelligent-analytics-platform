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