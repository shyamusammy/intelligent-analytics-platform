from fastapi import (
    APIRouter,
    File,
    Form,
    UploadFile,
)

from app.services.data_manager.manager import DataManager

router = APIRouter(
    prefix="/datasets",
    tags=["Data Manager"],
)

manager = DataManager()


@router.post(
    "/upload",
    summary="Upload a dataset",
)
async def upload_dataset(
    workspace_id: str = Form(...),
    display_name: str = Form(...),
    file: UploadFile = File(...),
):

    return await manager.register_dataset(
        workspace_id=workspace_id,
        file=file,
        display_name=display_name,
    )