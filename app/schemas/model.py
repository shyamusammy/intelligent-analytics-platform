from pydantic import BaseModel


class ModelMetrics(BaseModel):
    mae: float | None = None
    mse: float | None = None
    rmse: float | None = None
    r2: float | None = None

    accuracy: float | None = None
    precision: float | None = None
    recall: float | None = None
    f1_score: float | None = None


class ModelMetadata(BaseModel):
    """
    Metadata describing a persisted machine learning model.
    """

    target_column: str

    task_type: str

    best_model: str

    metrics: ModelMetrics