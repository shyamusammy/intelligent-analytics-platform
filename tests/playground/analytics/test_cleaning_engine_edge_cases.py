from app.services.etl.pipeline.etl_pipeline import ETLPipeline
from app.services.cleaning.cleaning_engine import CleaningEngine


WORKSPACE_ID = "ws_006"
DATASET_ID = "ds_001"


# ============================================================
# BUILD ETL PROFILE
# ============================================================

pipeline = ETLPipeline()

profile = pipeline.run(
    workspace_id=WORKSPACE_ID,
    dataset_id=DATASET_ID,
)


# ============================================================
# RUN CLEANING ENGINE
# ============================================================

engine = CleaningEngine()

report = engine.run(
    workspace_id=WORKSPACE_ID,
    dataset_id=DATASET_ID,
    profile=profile,
)


# ============================================================
# RESULTS
# ============================================================

print("=" * 80)
print("CLEANING ENGINE EDGE-CASE TEST")
print("=" * 80)

print(f"Original rows       : {report.original_row_count}")
print(f"Cleaned rows        : {report.cleaned_row_count}")
print(f"Duplicates removed  : {report.duplicates_removed}")
print(f"Missing before      : {report.missing_values_before}")
print(f"Missing after       : {report.missing_values_after}")
print(f"Quality before      : {report.quality_score_before}")
print(f"Quality after       : {report.quality_score_after}")

print("=" * 80)
print("CLEANING ACTIONS")
print("=" * 80)

for action in report.actions:
    print(
        f"{action.column_name:15} | "
        f"{action.strategy:35} | "
        f"values replaced: {action.values_replaced}"
    )

print("=" * 80)


# ============================================================
# ASSERTIONS
# ============================================================

assert report.missing_values_after == 0
assert report.cleaned_row_count > 0

print("✓ CleaningEngine edge-case test passed")
print("=" * 80)