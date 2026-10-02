import pandas as pd

from app.services.etl.quality.outlier_detector import OutlierDetector


dataframe = pd.DataFrame(
    {
        "age": [20, 21, 22, 23, 24, 100],
        "salary": [30000, 32000, 34000, 36000, 38000, 40000],
        "constant": [1, 1, 1, 1, 1, 1],
        "all_null": [None, None, None, None, None, None],
        "missing_values": [10, 20, None, 30, 40, 50],
    }
)

detector = OutlierDetector()

result = detector.detect(dataframe)

print("=" * 80)
print("OUTLIER DETECTOR — EDGE-CASE TEST")
print("=" * 80)

print(f"Rows              : {len(dataframe)}")
print(f"Total outliers    : {result.total_outliers}")
print(f"Affected rows     : {result.affected_rows}")

print("=" * 80)
print("OUTLIERS BY COLUMN")
print("=" * 80)

if result.outliers_by_column:
    for column, count in result.outliers_by_column.items():
        print(f"{column:<20} | {count}")
else:
    print("No outliers detected.")

print("=" * 80)

# ------------------------------------------------------------
# Assertions
# ------------------------------------------------------------

# The extreme age value should be detected.
assert "age" in result.outliers_by_column

# Missing values must not be counted as outliers.
assert "missing_values" not in result.outliers_by_column

# Constant columns should not produce outliers.
assert "constant" not in result.outliers_by_column

# All-null columns should not produce outliers.
assert "all_null" not in result.outliers_by_column

# Exactly one row contains the obvious age outlier.
assert result.affected_rows == 1

print("✓ All edge-case assertions passed")
print("✓ OutlierDetector edge-case test passed")
print("=" * 80)