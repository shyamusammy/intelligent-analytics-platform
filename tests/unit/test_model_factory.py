from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier

from app.core.enums import MLEstimator
from app.services.ml.factory import ModelFactory


def test_create_linear_regression():
    model = ModelFactory.create(
        MLEstimator.LINEAR_REGRESSION
    )

    assert isinstance(
        model,
        LinearRegression,
    )


def test_create_logistic_regression():
    model = ModelFactory.create(
        MLEstimator.LOGISTIC_REGRESSION
    )

    assert isinstance(
        model,
        LogisticRegression,
    )


def test_create_random_forest_regressor():
    model = ModelFactory.create(
        MLEstimator.RANDOM_FOREST_REGRESSOR
    )

    assert isinstance(
        model,
        RandomForestRegressor,
    )


def test_create_random_forest_classifier():
    model = ModelFactory.create(
        MLEstimator.RANDOM_FOREST_CLASSIFIER
    )

    assert isinstance(
        model,
        RandomForestClassifier,
    )


def test_random_forest_regressor_uses_random_state():
    model = ModelFactory.create(
        MLEstimator.RANDOM_FOREST_REGRESSOR
    )

    assert model.random_state == 42


def test_random_forest_classifier_uses_random_state():
    model = ModelFactory.create(
        MLEstimator.RANDOM_FOREST_CLASSIFIER
    )

    assert model.random_state == 42