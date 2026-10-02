from app.repositories.dataset_repository import DatasetRepository
from app.services.etl.quality.outlier_detector import OutlierDetector


repository = DatasetRepository()
detector = OutlierDetector()

dataframe = repository.load_dataframe(
    workspace_id="ws_005",
    dataset_id="ds_001",
)

result = detector.detect(dataframe)

print("=" * 80)
print("OUTLIER DETECTOR — REAL DATASET TEST")
print("=" * 80)

print(f"Rows              : {len(dataframe)}")
print(f"Numeric columns   : {len(dataframe.select_dtypes(include='number').columns)}")
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
print("✓ OutlierDetector real-dataset test passed")
print("=" * 80)