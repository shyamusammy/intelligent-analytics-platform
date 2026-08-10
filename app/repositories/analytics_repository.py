from pathlib import Path
import json

from app.core.constants import (
    WorkspaceFolders,
    ArtifactFolders,
    AnalyticsArtifacts,
)

from app.core.exceptions import (
    AnalyticsArtifactNotFoundError,
    AnalyticsDirectoryNotFoundError,
)

from app.schemas.analytics import AnalyticsEngineResult


class AnalyticsRepository:
    """
    Repository responsible for persisting Analytics Engine artifacts.

    Responsibilities
    ----------------
    - Create analytics artifact directory
    - Persist analytics results
    - Load analytics results

    This repository contains NO business logic.
    """

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def save(
        self,
        workspace_id: str,
        result: AnalyticsEngineResult,
    ) -> Path:
        """
        Save the complete analytics engine result.

        Individual artifacts are also written to disk to
        simplify debugging and future integrations.
        """

        analytics_path = self._create_analytics_folder(
            workspace_id,
        )

        self._save_statistics(
            analytics_path,
            result,
        )

        self._save_kpis(
            analytics_path,
            result,
        )

        self._save_correlations(
            analytics_path,
            result,
        )

        self._save_trends(
            analytics_path,
            result,
        )

        self._save_segmentation(
            analytics_path,
            result,
        )

        self._save_insights(
            analytics_path,
            result,
        )

        analytics_file = (
            analytics_path
            / AnalyticsArtifacts.ANALYTICS_FILE
        )

        self._save_json(
            analytics_file,
            result.model_dump(mode="json"),
        )

        return analytics_file

    def load(
        self,
        workspace_id: str,
    ) -> AnalyticsEngineResult:
        """
        Load the complete analytics engine result.
        """

        analytics_path = self._get_analytics_path(
            workspace_id,
        )

        analytics_file = (
            analytics_path
            / AnalyticsArtifacts.ANALYTICS_FILE
        )

        if not analytics_file.exists():

            raise AnalyticsArtifactNotFoundError(
                AnalyticsArtifacts.ANALYTICS_FILE
            )

        data = self._load_json(
            analytics_file,
        )

        return AnalyticsEngineResult(
            **data,
        )

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _create_analytics_folder(
        self,
        workspace_id: str,
    ) -> Path:
        """
        Create the analytics artifact directory if it
        does not already exist.
        """

        analytics_path = (
            Path(WorkspaceFolders.ROOT)
            / workspace_id
            / WorkspaceFolders.ARTIFACTS
            / ArtifactFolders.ANALYTICS
        )

        analytics_path.mkdir(
            parents=True,
            exist_ok=True,
        )

        return analytics_path

    def _get_analytics_path(
        self,
        workspace_id: str,
    ) -> Path:
        """
        Return the analytics artifact directory.
        """

        analytics_path = (
            Path(WorkspaceFolders.ROOT)
            / workspace_id
            / WorkspaceFolders.ARTIFACTS
            / ArtifactFolders.ANALYTICS
        )

        if not analytics_path.exists():

            raise AnalyticsDirectoryNotFoundError(
                workspace_id,
            )

        return analytics_path

    def _save_statistics(
        self,
        analytics_path: Path,
        result: AnalyticsEngineResult,
    ) -> None:

        self._save_json(
            analytics_path
            / AnalyticsArtifacts.STATISTICS_FILE,
            result.statistics.model_dump(
                mode="json",
            ),
        )

    def _save_kpis(
        self,
        analytics_path: Path,
        result: AnalyticsEngineResult,
    ) -> None:

        self._save_json(
            analytics_path
            / AnalyticsArtifacts.KPIS_FILE,
            result.kpis.model_dump(
                mode="json",
            ),
        )

    def _save_correlations(
        self,
        analytics_path: Path,
        result: AnalyticsEngineResult,
    ) -> None:

        self._save_json(
            analytics_path
            / AnalyticsArtifacts.CORRELATIONS_FILE,
            result.correlations.model_dump(
                mode="json",
            ),
        )

    def _save_trends(
        self,
        analytics_path: Path,
        result: AnalyticsEngineResult,
    ) -> None:

        self._save_json(
            analytics_path
            / AnalyticsArtifacts.TRENDS_FILE,
            result.trends.model_dump(
                mode="json",
            ),
        )

    def _save_segmentation(
        self,
        analytics_path: Path,
        result: AnalyticsEngineResult,
    ) -> None:

        self._save_json(
            analytics_path
            / AnalyticsArtifacts.SEGMENTATION_FILE,
            result.segmentation.model_dump(
                mode="json",
            ),
        )

    def _save_insights(
        self,
        analytics_path: Path,
        result: AnalyticsEngineResult,
    ) -> None:

        self._save_json(
            analytics_path
            / AnalyticsArtifacts.INSIGHTS_FILE,
            result.insights.model_dump(
                mode="json",
            ),
        )

    def _save_json(
        self,
        path: Path,
        data: dict,
    ) -> None:

        with open(
            path,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                data,
                file,
                indent=4,
            )

    def _load_json(
        self,
        path: Path,
    ) -> dict:

        with open(
            path,
            "r",
            encoding="utf-8",
        ) as file:

            return json.load(file)