from typing import List
from typing import Any
from pydantic import BaseModel
from app.core.enums import MLEstimator
from pydantic import Field
from app.core.enums import MLTaskType
from app.schemas.feature_engineering import FeatureEngineeringReport


class ValidationResult(BaseModel):
    valid: bool
    errors: List[str]
    warnings: List[str]


class TrainRequest(BaseModel):
    workspace_id: str
    dataset_id: str
    target_column: str


class TrainedModel(BaseModel):
    estimator: MLEstimator
    model: Any
    predictions: Any
    y_test: Any
    training_time: float


class TrainResult(BaseModel):
    models: list[TrainedModel]
    training_rows: int = 0
    testing_rows: int = 0


class RegressionMetrics(BaseModel):
    mae: float
    mse: float
    rmse: float
    r2: float


class ClassificationMetrics(BaseModel):
    accuracy: float
    precision: float
    recall: float
    f1_score: float


class EvaluatedModel(BaseModel):
    trained_model: TrainedModel
    metrics: RegressionMetrics | ClassificationMetrics


class EvaluationResult(BaseModel):
    models: list[EvaluatedModel]
    best_model: EvaluatedModel


class MLEngineResult(BaseModel):

    validation: ValidationResult

    task_type: MLTaskType | None = None

    estimators: list[MLEstimator] = Field(
        default_factory=list
    )

    train_result: TrainResult | None = None

    evaluation_result: EvaluationResult | None = None

    feature_engineering: FeatureEngineeringReport | None = None
