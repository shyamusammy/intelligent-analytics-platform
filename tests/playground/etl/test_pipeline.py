from pathlib import Path

from app.core.constants import (
    WorkspaceFolders,
    ETLArtifacts,
)

from app.services.etl.pipeline.etl_pipeline import (
    ETLPipeline,
)

pipeline = ETLPipeline()

profile = pipeline.run(

    workspace_id="ws_001",

    dataset_id="ds_001",
)

print(profile.model_dump())

profile_file = (

    Path(WorkspaceFolders.ROOT)

    / "ws_001"

    / WorkspaceFolders.ARTIFACTS

    / ETLArtifacts.PROFILING_FOLDER

    / ETLArtifacts.PROFILE_FILE
)

print()

print("Saved to:")

print(profile_file)