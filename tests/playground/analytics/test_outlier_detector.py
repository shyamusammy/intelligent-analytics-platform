import pandas as pd

from app.services.etl.quality.outlier_detector import OutlierDetector


def test_outlier_detector():
    dataframe = pd.DataFrame(
        {
            "age": [1, 2, 3, 4, 5, 100],
            "price": [10, 11, 12, 13, 14, 15],
            "category": ["A", "A", "B", "B", "C", "C"],
        }
    )

    result = OutlierDetector().detect(dataframe)

    assert result.total_outliers == 1

    assert result.outliers_by_column == {
        "age": 1
    }

    assert result.affected_rows == 1

    print("✓ OutlierDetector test passed")


if __name__ == "__main__":
    test_outlier_detector()