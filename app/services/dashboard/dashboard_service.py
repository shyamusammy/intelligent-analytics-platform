"""Build dashboard-ready chart data from the cleaned dataset."""

from pathlib import Path

import pandas as pd

from app.core.constants import WorkspaceFolders
from app.repositories.dataset_repository import DatasetRepository
from app.schemas.dashboard import DashboardChart, DashboardResult


class DashboardService:
    """
    Build data-driven dashboard payloads from the cleaned dataset.

    The service decides WHAT should be visualized.
    The Streamlit layer decides HOW the charts are rendered.
    """

    MAX_NUMERIC_CHARTS = 3
    MAX_CATEGORICAL_CHARTS = 3
    MAX_CATEGORY_VALUES = 10
    HISTOGRAM_BINS = 10

    def __init__(
        self,
        repository: DatasetRepository | None = None,
    ) -> None:
        self._repository = repository or DatasetRepository()

    def run(
        self,
        workspace_id: str,
        dataset_id: str,
    ) -> DashboardResult:
        """Build dashboard charts from the cleaned dataset."""

        dataframe = self._repository.load_cleaned_dataframe(
            workspace_id,
            dataset_id,
        )

        charts: list[DashboardChart] = []

        # ---------------------------------------------------------
        # 1. Numeric distributions
        # ---------------------------------------------------------
        numeric_columns = dataframe.select_dtypes(
            include="number"
        ).columns

        for column in numeric_columns[
            : self.MAX_NUMERIC_CHARTS
        ]:
            chart = self._build_numeric_distribution(
                dataframe,
                column,
            )

            if chart is not None:
                charts.append(chart)

        # ---------------------------------------------------------
        # 2. Categorical distributions
        # ---------------------------------------------------------
        categorical_columns = dataframe.select_dtypes(
            include=["object", "category", "bool"]
        ).columns

        for column in categorical_columns[
            : self.MAX_CATEGORICAL_CHARTS
        ]:
            chart = self._build_categorical_distribution(
                dataframe,
                column,
            )

            if chart is not None:
                charts.append(chart)

        # ---------------------------------------------------------
        # 3. Save dashboard artifact
        # ---------------------------------------------------------
        result = DashboardResult(
            charts=charts,
        )

        path = (
            Path(WorkspaceFolders.ROOT)
            / workspace_id
            / WorkspaceFolders.ARTIFACTS
            / "dashboard"
        )

        path.mkdir(
            parents=True,
            exist_ok=True,
        )

        (
            path / "dashboard.json"
        ).write_text(
            result.model_dump_json(indent=2),
            encoding="utf-8",
        )

        return result

    # ============================================================
    # NUMERIC CHART
    # ============================================================

    def _build_numeric_distribution(
        self,
        dataframe: pd.DataFrame,
        column: str,
    ) -> DashboardChart | None:
        """Build a histogram-style distribution chart."""

        series = dataframe[column].dropna()

        if series.empty:
            return None

        # A constant column cannot produce a useful histogram.
        if series.nunique() <= 1:
            return None

        binned = pd.cut(
            series,
            bins=self.HISTOGRAM_BINS,
        )

        counts = binned.value_counts(
            sort=False,
        )

        labels = [
            str(interval)
            for interval in counts.index
        ]

        values = [
            int(value)
            for value in counts.values
        ]

        return DashboardChart(
            title=f"Distribution of {column}",
            chart_type="histogram",
            data={
                "x": labels,
                "y": values,
                "x_axis": f"{column} Range",
                "y_axis": "Number of Records",
                "column": column,
            },
        )

    # ============================================================
    # CATEGORICAL CHART
    # ============================================================

    def _build_categorical_distribution(
        self,
        dataframe: pd.DataFrame,
        column: str,
    ) -> DashboardChart | None:
        """Build a top-category count chart."""

        series = dataframe[column].dropna().astype(str)

        if series.empty:
            return None

        values = series.value_counts().head(
            self.MAX_CATEGORY_VALUES
        )

        if values.empty:
            return None

        return DashboardChart(
            title=f"{column} Distribution",
            chart_type="bar",
            data={
                "x": values.index.tolist(),
                "y": [
                    int(value)
                    for value in values.values
                ],
                "x_axis": column,
                "y_axis": "Number of Records",
                "column": column,
            },
        )