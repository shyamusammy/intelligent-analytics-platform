from app.repositories.dataset_repository import (
    DatasetRepository,
)

from app.schemas.ml import (
    MLEngineResult,
)

from app.services.ml.detector import (
    MLDetector,
)

from app.services.ml.evaluator import (
    ModelEvaluator,
)

from app.services.ml.selector import (
    ModelSelector,
)

from app.services.ml.trainer import (
    ModelTrainer,
)

from app.services.ml.validator import (
    MLValidator,
)

from app.services.ml.preprocessor import (
    MLPreprocessor,
)

from app.schemas.context import (
    KnowledgeContext,
)

class MLEngine:
    """
    Orchestrates the complete machine learning workflow.

    Responsibilities
    ----------------
    - Load dataset
    - Validate dataset
    - Detect ML task
    - Select candidate models
    - Train models
    - Evaluate trained models

    This engine contains NO business logic.
    """

    def __init__(
        self,
        dataset_repository: DatasetRepository | None = None,
    ) -> None:

        self._dataset_repository = (
            dataset_repository
            or DatasetRepository()
        )

        self._validator = MLValidator()

        self._preprocessor = MLPreprocessor()

        self._detector = MLDetector()

        self._selector = ModelSelector()

        self._trainer = ModelTrainer()

        self._evaluator = ModelEvaluator()

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def run(
        self,
        workspace_id: str,
        dataset_id: str,
        target_column: str,
        knowledge: KnowledgeContext,
    ) -> MLEngineResult:
        """
        Execute the complete machine learning workflow.
        """

        dataframe = self._load_dataset(
            workspace_id,
            dataset_id,
        )

        validation = self._validator.validate(
            dataframe=dataframe,
            target_column=target_column,
        )

        task_type = None

        estimators = []

        train_result = None

        evaluation_result = None

        if validation.valid:

            dataframe = self._preprocessor.prepare(
                dataframe=dataframe,
                target_column=target_column,
                knowledge=knowledge,
            )

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

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _load_dataset(
        self,
        workspace_id: str,
        dataset_id: str,
    ):
        """
        Load the dataset into a pandas DataFrame.
        """

        return self._dataset_repository.load_dataframe(
            workspace_id,
            dataset_id,
        )