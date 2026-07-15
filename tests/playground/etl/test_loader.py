from app.services.etl.loader.dataset_loader import DatasetLoaderService

loader = DatasetLoaderService()

df = loader.load(
    workspace_id="ws_001",
    dataset_id="ds_001",
)

print("=" * 80)
print(df.head())
print("=" * 80)
print(df.shape)
print("=" * 80)
print(df.dtypes)