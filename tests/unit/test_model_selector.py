from app.core.enums import MLEstimator
from app.core.enums import MLTaskType
from app.services.ml.selector import ModelSelector


def test_select_regression_models():
    selector = ModelSelector()

    estimators = selector.select(
        task_type=MLTaskType.REGRESSION
    )

    assert MLEstimator.LINEAR_REGRESSION in estimators

    assert (
        MLEstimator.RANDOM_FOREST_REGRESSOR
        in estimators
    )


def test_select_classification_models():
    selector = ModelSelector()

    estimators = selector.select(
        task_type=MLTaskType.CLASSIFICATION
    )

    assert (
        MLEstimator.LOGISTIC_REGRESSION
        in estimators
    )

    assert (
        MLEstimator.RANDOM_FOREST_CLASSIFIER
        in estimators
    )


def test_regression_does_not_select_classification_models():
    selector = ModelSelector()

    estimators = selector.select(
        task_type=MLTaskType.REGRESSION
    )

    assert (
        MLEstimator.LOGISTIC_REGRESSION
        not in estimators
    )

    assert (
        MLEstimator.RANDOM_FOREST_CLASSIFIER
        not in estimators
    )


def test_classification_does_not_select_regression_models():
    selector = ModelSelector()

    estimators = selector.select(
        task_type=MLTaskType.CLASSIFICATION
    )

    assert (
        MLEstimator.LINEAR_REGRESSION
        not in estimators
    )

    assert (
        MLEstimator.RANDOM_FOREST_REGRESSOR
        not in estimators
    )