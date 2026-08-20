import asyncio
import json

from starlette.requests import Request

from app.core.error_handlers import platform_error_handler, value_error_handler
from app.core.exceptions import DatasetNotFoundError


def _request() -> Request:
    return Request({"type": "http", "method": "POST", "path": "/test"})


def test_missing_resource_is_returned_as_404() -> None:
    response = asyncio.run(
        platform_error_handler(_request(), DatasetNotFoundError("ds_missing"))
    )

    assert response.status_code == 404
    assert json.loads(response.body) == {"detail": "Dataset 'ds_missing' was not found."}


def test_invalid_input_is_returned_as_400() -> None:
    response = asyncio.run(value_error_handler(_request(), ValueError("Invalid file")))

    assert response.status_code == 400
    assert json.loads(response.body) == {"detail": "Invalid file"}
