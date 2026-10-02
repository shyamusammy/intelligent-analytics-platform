import pandas as pd

from app.repositories.dataset_repository import DatasetRepository
from app.services.etl.quality.outlier_detector import OutlierDetector


repository = DatasetRepository()
detector = OutlierDetector()

dataframe = repository.load_dataframe(
    workspace_id="ws_005",
    dataset_id="ds_001",
)

numeric = dataframe.select_dtypes(include="number")

print("=" * 100)
print("OUTLIER DETECTOR — DIAGNOSTIC")
print("=" * 100)

print(f"Rows            : {len(dataframe)}")
print(f"Numeric columns : {len(numeric.columns)}")

print("=" * 100)

for column in numeric.columns:

    series = numeric[column].dropna()

    if series.empty:
        print(f"\n{column}")
        print("  No non-null values")
        continue

    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1

    lower = q1 - (
        OutlierDetector.IQR_MULTIPLIER * iqr
    )

    upper = q3 + (
        OutlierDetector.IQR_MULTIPLIER * iqr
    )

    outlier_mask = (
        (series < lower)
        | (series > upper)
    )

    outlier_count = int(
        outlier_mask.sum()
    )

    outlier_percentage = (
        outlier_count / len(series) * 100
    )

    print(f"\n{column}")
    print(f"  Non-null values : {len(series):,}")
    print(f"  Unique values   : {series.nunique():,}")
    print(f"  Minimum         : {series.min()}")
    print(f"  Q1              : {q1}")
    print(f"  Q3              : {q3}")
    print(f"  Maximum         : {series.max()}")
    print(f"  IQR             : {iqr}")
    print(f"  Lower bound     : {lower}")
    print(f"  Upper bound     : {upper}")
    print(f"  Outliers        : {outlier_count:,}")
    print(f"  Outlier %       : {outlier_percentage:.2f}%")

print("\n" + "=" * 100)
print("✓ Outlier diagnostic completed")
print("=" * 100)