import pandas as pd

from app.core.enums import MLTaskType
from app.services.ml.detector import MLDetector


def test_non_numeric_target_is_classification():
    dataframe = pd.DataFrame(
        {
            "feature": [10, 20, 30, 40, 50],
            "target": ["A", "B", "A", "B", "A"],
        }
    )

    detector = MLDetector()

    result = detector.detect(
        dataframe=dataframe,
        target_column="target",
    )

    assert result == MLTaskType.CLASSIFICATION


def test_numeric_target_with_few_unique_values_is_classification():
    dataframe = pd.DataFrame(
        {
            "feature": [10, 20, 30, 40, 50],
            "target": [0, 1, 0, 1, 0],
        }
    )

    detector = MLDetector()

    result = detector.detect(
        dataframe=dataframe,
        target_column="target",
    )

    assert result == MLTaskType.CLASSIFICATION


def test_numeric_target_with_high_unique_ratio_is_regression():
    dataframe = pd.DataFrame(
        {
            "feature": range(1, 101),
            "target": [float(value) for value in range(1, 101)],
        }
    )

    detector = MLDetector()

    result = detector.detect(
        dataframe=dataframe,
        target_column="target",
    )

    assert result == MLTaskType.REGRESSION


def test_numeric_target_with_low_unique_ratio_is_classification():
    dataframe = pd.DataFrame(
        {
            "feature": range(1, 101),
            "target": [1] * 50 + [2] * 50,
        }
    )

    detector = MLDetector()

    result = detector.detect(
        dataframe=dataframe,
        target_column="target",
    )

    assert result == MLTaskType.CLASSIFICATION


def test_numeric_target_with_exactly_20_unique_values_is_classification():
    dataframe = pd.DataFrame(
        {
            "feature": range(100),
            "target": [
                value
                for value in range(20)
                for _ in range(5)
            ],
        }
    )

    detector = MLDetector()

    result = detector.detect(
        dataframe=dataframe,
        target_column="target",
    )

    assert result == MLTaskType.CLASSIFICATION


def test_numeric_target_with_more_than_20_unique_values_and_high_ratio_is_regression():
    dataframe = pd.DataFrame(
        {
            "feature": range(100),
            "target": range(100),
        }
    )

    detector = MLDetector()

    result = detector.detect(
        dataframe=dataframe,
        target_column="target",
    )

    assert result == MLTaskType.REGRESSION