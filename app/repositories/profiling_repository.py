from pathlib import Path
import json

from app.core.constants import (
    WorkspaceFolders,
    ETLArtifacts,
)

from app.schemas.etl import ETLProfile

from app.core.exceptions import ProfilingArtifactNotFoundError

class ProfilingRepository:
    """
    Repository responsible for persisting ETL profiling artifacts.
    """

    def save(
        self,
        workspace_id: str,
        profile: ETLProfile,
    ) -> Path:
        """
        Save the ETL profile as JSON.
        """

        artifact_folder = (

            Path(WorkspaceFolders.ROOT)

            / workspace_id

            / WorkspaceFolders.ARTIFACTS

            / ETLArtifacts.PROFILING_FOLDER
        )

        artifact_folder.mkdir(
            parents=True,
            exist_ok=True,
        )

        profile_file = (
            artifact_folder
            / ETLArtifacts.PROFILE_FILE
        )

        with open(
            profile_file,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(

                profile.model_dump(mode="json"),

                file,

                indent=4,
            )

        return profile_file

    def load(
        self,
        workspace_id: str,
    ) -> ETLProfile:
        """
        Load the saved ETL profile.
        """

        profile_file = (

            Path(WorkspaceFolders.ROOT)

            / workspace_id

            / WorkspaceFolders.ARTIFACTS

            / ETLArtifacts.PROFILING_FOLDER

            / ETLArtifacts.PROFILE_FILE
        )

        if not profile_file.exists():

            raise ProfilingArtifactNotFoundError(
                f"Profiling artifact not found for workspace '{workspace_id}'."
            )

        with open(
            profile_file,
            "r",
            encoding="utf-8",
        ) as file:

            data = json.load(file)

        return ETLProfile(**data)