import pandas as pd

from app.schemas.analytics import (
    KPI,
    KPIResult,
)


class KPIService:
    """
    Service responsible for generating generic KPIs
    for any dataset.

    Responsibilities
    ----------------
    - Dataset KPIs
    - Numeric column KPIs

    This service contains NO persistence logic.
    """

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def run(
        self,
        dataframe: pd.DataFrame,
    ) -> KPIResult:
        """
        Generate KPIs for the dataset.
        """

        metrics: list[KPI] = []

        metrics.extend(
            self._build_dataset_kpis(
                dataframe,
            )
        )

        metrics.extend(
            self._build_numeric_kpis(
                dataframe,
            )
        )

        return KPIResult(
            metrics=metrics,
        )

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _build_dataset_kpis(
        self,
        dataframe: pd.DataFrame,
    ) -> list[KPI]:
        """
        Generate dataset-level KPIs.
        """

        return [

            KPI(
                name="Total Rows",
                value=len(dataframe),
                description="Total number of rows in the dataset.",
            ),

            KPI(
                name="Total Columns",
                value=len(dataframe.columns),
                description="Total number of columns in the dataset.",
            ),

            KPI(
                name="Missing Cells",
                value=int(
                    dataframe.isna().sum().sum()
                ),
                description="Total number of missing values.",
            ),

            KPI(
                name="Duplicate Rows",
                value=int(
                    dataframe.duplicated().sum()
                ),
                description="Total number of duplicate rows.",
            ),

        ]

    def _build_numeric_kpis(
        self,
        dataframe: pd.DataFrame,
    ) -> list[KPI]:
        """
        Generate KPIs for every numeric column.
        """

        metrics: list[KPI] = []

        numeric_dataframe = dataframe.select_dtypes(
            include=["number"],
        )

        for column in numeric_dataframe.columns:

            series = numeric_dataframe[column]

            metrics.extend(

                [

                    KPI(
                        name=f"{column} Sum",
                        value=self._safe_float(
                            series.sum()
                        ),
                        description=(
                            f"Sum of values in '{column}'."
                        ),
                    ),

                    KPI(
                        name=f"{column} Average",
                        value=self._safe_float(
                            series.mean()
                        ),
                        description=(
                            f"Average value of '{column}'."
                        ),
                    ),

                    KPI(
                        name=f"{column} Minimum",
                        value=self._safe_float(
                            series.min()
                        ),
                        description=(
                            f"Minimum value in '{column}'."
                        ),
                    ),

                    KPI(
                        name=f"{column} Maximum",
                        value=self._safe_float(
                            series.max()
                        ),
                        description=(
                            f"Maximum value in '{column}'."
                        ),
                    ),

                ]

            )

        return metrics

    def _safe_float(
        self,
        value: object,
    ) -> float:
        """
        Convert NaN values to 0.0.
        """

        if pd.isna(value):
            return 0.0

        return float(value)