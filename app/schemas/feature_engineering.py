from pydantic import BaseModel, Field


class FeatureDecision(BaseModel):
    column: str
    feature_type: str
    decision: str
    reason: str | None = None
    cardinality: int | None = None


class FeatureValidationResult(BaseModel):
    valid: bool
    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class FeatureEngineeringReport(BaseModel):
    target_column: str
    original_feature_count: int
    generated_feature_count: int = 0
    final_feature_count: int = 0
    numeric_features: list[str] = Field(default_factory=list)
    categorical_features: list[str] = Field(default_factory=list)
    datetime_features: list[str] = Field(default_factory=list)
    encoded_features: list[str] = Field(default_factory=list)
    generated_datetime_features: list[str] = Field(default_factory=list)
    removed_columns: list[FeatureDecision] = Field(default_factory=list)
    decisions: list[FeatureDecision] = Field(default_factory=list)
    training_feature_count: int = 0
    testing_feature_count: int = 0
    validation: FeatureValidationResult
