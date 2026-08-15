from pathlib import Path
from typing import Any

import joblib

from app.core.constants import ArtifactFolders
from app.schemas.model import ModelMetadata


class ModelRepository:
    """
    Repository responsible for persisting and loading
    trained machine learning model artifacts.

    Responsibilities
    ----------------
    - Save candidate models
    - Save the selected best model
    - Load persisted models
    - Save model metadata
    - Keep filesystem logic outside the ML service layer
    """

    # ==========================================================
    # MODEL ARTIFACTS
    # ==========================================================

    def save_model(
        self,
        workspace_id: str,
        model: Any,
        model_name: str,
        best: bool = False,
    ) -> Path:
        """
        Persist a trained model to the workspace model artifacts.
        """

        models_path = self._get_models_path(
            workspace_id
        )

        models_path.mkdir(
            parents=True,
            exist_ok=True,
        )

        if best:
            model_path = (
                models_path
                / "best_model.joblib"
            )
        else:
            model_path = (
                models_path
                / f"{model_name}.joblib"
            )

        joblib.dump(
            model,
            model_path,
        )

        return model_path

    def load_model(
        self,
        workspace_id: str,
        model_name: str = "best_model",
    ) -> Any:
        """
        Load a persisted model from the workspace.
        """

        models_path = self._get_models_path(
            workspace_id
        )

        model_path = (
            models_path
            / f"{model_name}.joblib"
        )

        if not model_path.exists():
            raise FileNotFoundError(
                f"Model artifact not found: "
                f"{model_path}"
            )

        return joblib.load(
            model_path
        )

    # ==========================================================
    # MODEL METADATA
    # ==========================================================

    def save_metadata(
        self,
        workspace_id: str,
        metadata: ModelMetadata,
    ) -> Path:
        """
        Persist model metadata as JSON.
        """

        models_path = self._get_models_path(
            workspace_id
        )

        models_path.mkdir(
            parents=True,
            exist_ok=True,
        )

        metadata_path = (
            models_path
            / "model_metadata.json"
        )

        metadata_path.write_text(
            metadata.model_dump_json(
                indent=4
            ),
            encoding="utf-8",
        )

        return metadata_path

    def load_metadata(
        self,
        workspace_id: str,
    ) -> ModelMetadata:
        """
        Load persisted model metadata.
        """

        models_path = self._get_models_path(
            workspace_id
        )

        metadata_path = (
            models_path
            / "model_metadata.json"
        )

        if not metadata_path.exists():
            raise FileNotFoundError(
                f"Model metadata not found: "
                f"{metadata_path}"
            )

        return ModelMetadata.model_validate_json(
            metadata_path.read_text(
                encoding="utf-8"
            )
        )

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _get_models_path(
        self,
        workspace_id: str,
    ) -> Path:
        """
        Return the model artifact directory
        for the specified workspace.
        """

        return (
            Path("workspaces")
            / workspace_id
            / "artifacts"
            / ArtifactFolders.MODELS
        )