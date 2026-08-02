from enum import Enum


class MLTaskType(str, Enum):
    CLASSIFICATION = "classification"
    REGRESSION = "regression"

class MLEstimator(str, Enum):
    LINEAR_REGRESSION = "linear_regression"
    RANDOM_FOREST_REGRESSOR = "random_forest_regressor"

    LOGISTIC_REGRESSION = "logistic_regression"
    RANDOM_FOREST_CLASSIFIER = "random_forest_classifier"