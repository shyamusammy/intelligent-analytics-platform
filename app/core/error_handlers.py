"""HTTP translations for application-domain exceptions."""

from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    AnalyticsArtifactNotFoundError,
    AnalyticsDirectoryNotFoundError,
    AnalyticsPlatformError,
    DatasetMetadataNotFoundError,
    DatasetNotFoundError,
    OriginalDatasetNotFoundError,
    ProfilingArtifactNotFoundError,
    WorkspaceNotFoundError,
)


NOT_FOUND_ERRORS = (
    WorkspaceNotFoundError,
    DatasetNotFoundError,
    DatasetMetadataNotFoundError,
    OriginalDatasetNotFoundError,
    ProfilingArtifactNotFoundError,
    AnalyticsDirectoryNotFoundError,
    AnalyticsArtifactNotFoundError,
)


async def platform_error_handler(
    _: Request,
    exc: AnalyticsPlatformError,
) -> JSONResponse:
    """Return a consistent response for expected application errors."""

    status_code = 404 if isinstance(exc, NOT_FOUND_ERRORS) else 400
    return JSONResponse(status_code=status_code, content={"detail": str(exc)})


async def value_error_handler(_: Request, exc: ValueError) -> JSONResponse:
    """Return client-friendly responses for upload and input validation."""

    return JSONResponse(status_code=400, content={"detail": str(exc)})
