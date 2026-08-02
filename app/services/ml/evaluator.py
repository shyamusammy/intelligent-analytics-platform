import math

from numpy import ndarray
from pandas import Series

from sklearn.metrics import (
    accuracy_score,
    f1_score,
    mean_absolute_error,
    mean_squared_error,
    precision_score,
    r2_score,
    recall_score,
)

from app.core.enums import MLTaskType
from app.schemas.ml import (
    ClassificationMetrics,
    EvaluatedModel,
    EvaluationResult,
    RegressionMetrics,
    TrainResult,
    TrainedModel,
)


class ModelEvaluator:

    def evaluate(
        self,
        task_type: MLTaskType,
        train_result: TrainResult,
    ) -> EvaluationResult:

        evaluated_models = self._evaluate_models(
            task_type,
            train_result,
        )

        best_model = self._select_best_model(
            task_type,
            evaluated_models,
        )

        return EvaluationResult(
            models=evaluated_models,
            best_model=best_model,
        )

    def _evaluate_models(
        self,
        task_type: MLTaskType,
        train_result: TrainResult,
    ) -> list[EvaluatedModel]:

        evaluated_models: list[EvaluatedModel] = []

        for trained_model in train_result.models:

            evaluated_models.append(
                self._evaluate_model(
                    task_type,
                    trained_model,
                )
            )

        return evaluated_models

    def _evaluate_model(
        self,
        task_type: MLTaskType,
        trained_model: TrainedModel,
    ) -> EvaluatedModel:

        if task_type == MLTaskType.REGRESSION:

            metrics = self._evaluate_regression(
                trained_model.y_test,
                trained_model.predictions,
            )

        else:

            metrics = self._evaluate_classification(
                trained_model.y_test,
                trained_model.predictions,
            )

        return EvaluatedModel(
            trained_model=trained_model,
            metrics=metrics,
        )

    def _evaluate_regression(
        self,
        y_test: Series,
        predictions: ndarray,
    ) -> RegressionMetrics:

        mae = mean_absolute_error(
            y_test,
            predictions,
        )

        mse = mean_squared_error(
            y_test,
            predictions,
        )

        rmse = math.sqrt(mse)

        r2 = r2_score(
            y_test,
            predictions,
        )

        return RegressionMetrics(
            mae=mae,
            mse=mse,
            rmse=rmse,
            r2=r2,
        )

    def _evaluate_classification(
        self,
        y_test: Series,
        predictions: ndarray,
    ) -> ClassificationMetrics:

        accuracy = accuracy_score(
            y_test,
            predictions,
        )

        precision = precision_score(
            y_test,
            predictions,
            average="weighted",
            zero_division=0,
        )

        recall = recall_score(
            y_test,
            predictions,
            average="weighted",
            zero_division=0,
        )

        f1 = f1_score(
            y_test,
            predictions,
            average="weighted",
            zero_division=0,
        )

        return ClassificationMetrics(
            accuracy=accuracy,
            precision=precision,
            recall=recall,
            f1_score=f1,
        )

    def _select_best_model(
        self,
        task_type: MLTaskType,
        evaluated_models: list[EvaluatedModel],
    ) -> EvaluatedModel:

        if task_type == MLTaskType.REGRESSION:

            return max(
                evaluated_models,
                key=lambda model: model.metrics.r2,
            )

        return max(
            evaluated_models,
            key=lambda model: model.metrics.accuracy,
        )