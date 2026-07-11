from fastapi import FastAPI

from app.api.workspace import router as workspace_router
from app.api.data_manager import router as dataset_router


app = FastAPI(
    title="Intelligent Analytics Platform",
    version="0.1.0",
)

app.include_router(workspace_router)
app.include_router(dataset_router)

@app.get("/")
def root():
    return {
        "message": "API is running successfully."
    }