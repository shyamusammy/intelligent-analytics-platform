from app.services.etl.loader.dataset_loader import (
    DatasetLoaderService,
)

from app.services.etl.schema.schema_detector import (
    SchemaDetector,
)


loader = DatasetLoaderService()

detector = SchemaDetector()

df = loader.load(
    workspace_id="ws_001",
    dataset_id="ds_001",
)

schema = detector.detect(df)

print()

print("=" * 80)

print(schema.model_dump())

print("=" * 80)