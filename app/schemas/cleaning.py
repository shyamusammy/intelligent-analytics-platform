from pydantic import BaseModel, Field


class CleaningAction(BaseModel):
    column_name: str
    strategy: str
    values_replaced: int = 0


class CleaningReport(BaseModel):
    original_row_count: int
    cleaned_row_count: int
    duplicates_removed: int
    missing_values_before: int
    missing_values_after: int
    duplicate_rows_after: int
    quality_score_before: float
    quality_score_after: float
    columns_affected: list[str] = Field(default_factory=list)
    actions: list[CleaningAction] = Field(default_factory=list)
    cleaned_dataset_path: str
