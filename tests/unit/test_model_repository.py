from pathlib import Path

import pytest
from sklearn.linear_model import LinearRegression

from app.repositories.model_repository import ModelRepository
from app.schemas.model import ModelMetadata


def test_save_and_load_model(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    repository = ModelRepository()

    model = LinearRegression()

    model_path = repository.save_model(
        workspace_id="ws_test",
        model=model,
        model_name="linear_regression",
    )

    assert model_path.exists()

    assert (
        model_path.name
        == "linear_regression.joblib"
    )

    loaded_model = repository.load_model(
        workspace_id="ws_test",
        model_name="linear_regression",
    )

    assert isinstance(
        loaded_model,
        LinearRegression,
    )


def test_save_best_model(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    repository = ModelRepository()

    model = LinearRegression()

    model_path = repository.save_model(
        workspace_id="ws_test",
        model=model,
        model_name="linear_regression",
        best=True,
    )

    assert model_path.exists()

    assert (
        model_path.name
        == "best_model.joblib"
    )


def test_load_best_model(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    repository = ModelRepository()

    model = LinearRegression()

    repository.save_model(
        workspace_id="ws_test",
        model=model,
        model_name="linear_regression",
        best=True,
    )

    loaded_model = repository.load_model(
        workspace_id="ws_test",
    )

    assert isinstance(
        loaded_model,
        LinearRegression,
    )


def test_load_missing_model_raises_error(
    tmp_path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)

    repository = ModelRepository()

    with pytest.raises(FileNotFoundError):
        repository.load_model(
            workspace_id="ws_test",
            model_name="missing_model",
        )


def test_save_and_load_metadata(
    tmp_path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)

    repository = ModelRepository()

    metadata = ModelMetadata(
        target_column="Revenue",
        task_type="regression",
        best_model="linear_regression",
        metrics={
            "mae": 100.0,
            "mse": 10000.0,
            "rmse": 100.0,
            "r2": 0.95,
            "accuracy": None,
            "precision": None,
            "recall": None,
            "f1_score": None,
        },
    )

    metadata_path = repository.save_metadata(
        workspace_id="ws_test",
        metadata=metadata,
    )

    assert metadata_path.exists()

    assert (
        metadata_path.name
        == "model_metadata.json"
    )

    loaded_metadata = repository.load_metadata(
        workspace_id="ws_test",
    )

    assert (
        loaded_metadata.target_column
        == "Revenue"
    )

    assert (
        loaded_metadata.task_type
        == "regression"
    )

    assert (
        loaded_metadata.best_model
        == "linear_regression"
    )

    assert (
        loaded_metadata.metrics.rmse
        == 100.0
    )

    assert (
        loaded_metadata.metrics.r2
        == 0.95
    )


def test_load_missing_metadata_raises_error(
    tmp_path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)

    repository = ModelRepository()

    with pytest.raises(FileNotFoundError):
        repository.load_metadata(
            workspace_id="ws_test",
        )