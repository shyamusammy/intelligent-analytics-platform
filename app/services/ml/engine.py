from app.repositories.dataset_repository import (
    DatasetRepository,
)

from app.repositories.model_repository import (
    ModelRepository,
)

from app.schemas.ml import (
    MLEngineResult,
)

from app.schemas.model import (
    ModelMetadata,
    ModelMetrics,
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
    - Evaluate models
    - Persist trained models
    - Persist best model
    - Persist model metadata

    This engine contains NO business logic.
    """

    def __init__(
        self,
        dataset_repository: DatasetRepository | None = None,
        model_repository: ModelRepository | None = None,
    ) -> None:

        self._dataset_repository = (
            dataset_repository
            or DatasetRepository()
        )

        self._model_repository = (
            model_repository
            or ModelRepository()
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

            self._persist_models(
                workspace_id=workspace_id,
                target_column=target_column,
                task_type=task_type.value,
                train_result=train_result,
                evaluation_result=evaluation_result,
            )

        return MLEngineResult(
            validation=validation,
            task_type=task_type,
            estimators=estimators,
            train_result=train_result,
            evaluation_result=evaluation_result,
        )

    # ==========================================================
    # MODEL PERSISTENCE
    # ==========================================================

    def _persist_models(
        self,
        workspace_id: str,
        target_column: str,
        task_type: str,
        train_result,
        evaluation_result,
    ) -> None:
        """
        Persist all trained models and the selected best model.
        """

        # ------------------------------------------------------
        # Save every trained model
        # ------------------------------------------------------

        for trained_model in train_result.models:

            model_name = (
                trained_model.estimator.value
            )

            self._model_repository.save_model(
                workspace_id=workspace_id,
                model=trained_model.model,
                model_name=model_name,
            )

        # ------------------------------------------------------
        # Best model
        # ------------------------------------------------------

        best_model = (
            evaluation_result.best_model
        )

        best_estimator = (
            best_model.trained_model.estimator
        )

        self._model_repository.save_model(
            workspace_id=workspace_id,
            model=best_model.trained_model.model,
            model_name=best_estimator.value,
            best=True,
        )

        # ------------------------------------------------------
        # Metadata
        # ------------------------------------------------------

        metrics = self._build_model_metrics(
            best_model.metrics
        )

        metadata = ModelMetadata(
            target_column=target_column,
            task_type=task_type,
            best_model=best_estimator.value,
            metrics=metrics,
        )

        self._model_repository.save_metadata(
            workspace_id=workspace_id,
            metadata=metadata,
        )

    # ==========================================================
    # METRICS
    # ==========================================================

    def _build_model_metrics(
        self,
        metrics,
    ) -> ModelMetrics:
        """
        Convert evaluation metrics into the
        persistence schema.
        """

        return ModelMetrics(
            mae=getattr(
                metrics,
                "mae",
                None,
            ),
            mse=getattr(
                metrics,
                "mse",
                None,
            ),
            rmse=getattr(
                metrics,
                "rmse",
                None,
            ),
            r2=getattr(
                metrics,
                "r2",
                None,
            ),
            accuracy=getattr(
                metrics,
                "accuracy",
                None,
            ),
            precision=getattr(
                metrics,
                "precision",
                None,
            ),
            recall=getattr(
                metrics,
                "recall",
                None,
            ),
            f1_score=getattr(
                metrics,
                "f1_score",
                None,
            ),
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