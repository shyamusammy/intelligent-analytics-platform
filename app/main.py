from fastapi import FastAPI

from app.api.analytics import router as analytics_router
from app.api.workspace import router as workspace_router
from app.api.data_manager import router as dataset_router
from app.api.etl import router as etl_router
from app.api.ml import router as ml_router
from app.api.pipeline import router as pipeline_router
from app.api.analysis import router as analysis_router
from app.core.error_handlers import (
    platform_error_handler,
    value_error_handler,
)
from app.core.exceptions import AnalyticsPlatformError


app = FastAPI(
    title="Intelligent Analytics Platform",
    version="0.1.0",
)

app.add_exception_handler(AnalyticsPlatformError, platform_error_handler)
app.add_exception_handler(ValueError, value_error_handler)

app.include_router(workspace_router)
app.include_router(dataset_router)
app.include_router(etl_router)
app.include_router(analytics_router)
app.include_router(ml_router)
app.include_router(pipeline_router)
app.include_router(analysis_router)

@app.get("/")
def root():
    return {
        "message": "API is running successfully."
    }
