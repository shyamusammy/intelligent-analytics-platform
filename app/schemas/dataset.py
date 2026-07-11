from pydantic import BaseModel
from datetime import datetime


class DatasetResponse(BaseModel):
    """
    Response returned after a dataset
    has been successfully registered.
    """

    dataset_id: str

    workspace_id: str

    display_name: str

    original_filename: str

    extension: str

    status: str

    uploaded_at: datetime


class DatasetMetadata(BaseModel):
    """
    Metadata stored for every dataset.
    """

    dataset_id: str

    workspace_id: str

    display_name: str

    original_filename: str

    extension: str

    size_mb: float

    rows: int | None = None

    columns: int | None = None

    sheet_name: str | None = None

    active: bool

    status: str

    uploaded_at: datetime