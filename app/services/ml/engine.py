from pandas import DataFrame

from app.schemas.ml import MLEngineResult

from app.services.ml.detector import MLDetector
from app.services.ml.evaluator import ModelEvaluator
from app.services.ml.selector import ModelSelector
from app.services.ml.trainer import ModelTrainer
from app.services.ml.validator import MLValidator


class MLEngine:
    """
    Orchestrates the complete machine learning workflow.

    Workflow:
        Validation
            ↓
        Task Detection
            ↓
        Model Selection
            ↓
        Model Training
            ↓
        Model Evaluation
    """

    def __init__(self):

        self._validator = MLValidator()

        self._detector = MLDetector()

        self._selector = ModelSelector()

        self._trainer = ModelTrainer()

        self._evaluator = ModelEvaluator()

    def run(
        self,
        dataframe: DataFrame,
        target_column: str,
    ) -> MLEngineResult:

        validation = self._validator.validate(
            dataframe=dataframe,
            target_column=target_column,
        )

        task_type = None

        estimators = []

        train_result = None

        evaluation_result = None

        if validation.valid:

            task_type = self._detector.detect(
                dataframe=dataframe,
                target_column=target_column,
            )

            estimators = self._selector.select(
                task_type=task_type,
            )

            train_result = self._trainer.train(
                dataframe=dataframe,
                target_column=target_column,
                estimators=estimators,
            )

            evaluation_result = self._evaluator.evaluate(
                task_type=task_type,
                train_result=train_result,
            )

        return MLEngineResult(
            validation=validation,
            task_type=task_type,
            estimators=estimators,
            train_result=train_result,
            evaluation_result=evaluation_result,
        )