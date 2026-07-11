from pathlib import Path
from app.core.constants import WorkspaceFolders

class DatasetRegistry:
    """
    Responsible for generating dataset IDs
    inside a workspace.
    """

    DATASET_PREFIX = "ds_"

    def generate_dataset_id(self, workspace_path: Path) -> str:
        """
        Generates the next dataset ID.

        Example:
        ds_001
        ds_002
        ds_003
        """

        datasets_path = workspace_path / WorkspaceFolders.DATASETS

        datasets_path.mkdir(exist_ok=True)

        existing = sorted(
            [
                folder.name
                for folder in datasets_path.iterdir()
                if folder.is_dir()
                and folder.name.startswith(self.DATASET_PREFIX)
            ]
        )

        if not existing:
            return "ds_001"

        last_dataset = existing[-1]

        number = int(last_dataset.split("_")[1]) + 1

        return f"ds_{number:03d}"