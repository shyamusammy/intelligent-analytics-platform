from app.services.etl.loader.dataset_loader import DatasetLoaderService
from app.services.etl.schema.datatype_inference import (
    DataTypeInferenceService,
)

loader = DatasetLoaderService()
inferencer = DataTypeInferenceService()

df = loader.load(
    workspace_id="ws_001",
    dataset_id="ds_001",
)

print("\nDetected Data Types")
print("-" * 50)

for column in df.columns:
    detected = inferencer.infer(df[column])

    print(f"{column:<20} -> {detected.value}")