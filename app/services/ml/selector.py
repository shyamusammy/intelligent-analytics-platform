from app.core.enums import MLEstimator
from app.core.enums import MLTaskType


class ModelSelector:

    def select(
        self,
        task_type: MLTaskType
    ) -> list[MLEstimator]:

        if task_type == MLTaskType.CLASSIFICATION:

            return [
                MLEstimator.LOGISTIC_REGRESSION,
                MLEstimator.RANDOM_FOREST_CLASSIFIER,
            ]

        return [
            MLEstimator.LINEAR_REGRESSION,
            MLEstimator.RANDOM_FOREST_REGRESSOR,
        ]