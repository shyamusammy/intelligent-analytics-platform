from sklearn.base import BaseEstimator

from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression

from app.core.constants import MLConstants
from app.core.enums import MLEstimator


class ModelFactory:

    _MODEL_MAPPING = {
        MLEstimator.LINEAR_REGRESSION: LinearRegression,
        MLEstimator.LOGISTIC_REGRESSION: LogisticRegression,
        MLEstimator.RANDOM_FOREST_REGRESSOR: RandomForestRegressor,
        MLEstimator.RANDOM_FOREST_CLASSIFIER: RandomForestClassifier,
    }

    @staticmethod
    def create(
        estimator: MLEstimator
    ) -> BaseEstimator:

        model_class = ModelFactory._MODEL_MAPPING.get(
            estimator
        )

        if model_class is None:
            raise ValueError(
                f"Unsupported estimator: {estimator}"
            )

        if estimator in {
            MLEstimator.RANDOM_FOREST_REGRESSOR,
            MLEstimator.RANDOM_FOREST_CLASSIFIER,
        }:
            return model_class(
                random_state=MLConstants.RANDOM_STATE
            )

        return model_class()