import pandas as pd

from pandas.api.types import (
    is_datetime64_any_dtype,
    is_numeric_dtype,
)

from app.core.enums import (
    TrendDirection,
)

from app.schemas.analytics import (
    TrendMetric,
    TrendResult,
)

from app.schemas.context import (
    KnowledgeContext,
)

from app.services.analytics.helpers.etl_schema_helper import (
    ETLSchemaHelper,
)


class TrendService:
    """
    Service responsible for analyzing trends
    in time-series data.

    Responsibilities
    ----------------
    - Detect datetime column
    - Analyze trends for numeric columns
    - Calculate change and percentage change
    - Determine trend direction

    This service contains NO persistence logic.
    """

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def run(
        self,
        dataframe: pd.DataFrame,
        knowledge: KnowledgeContext,
    ) -> TrendResult:
        """
        Generate trends for numeric columns.
        """

        datetime_column = (
            ETLSchemaHelper.get_datetime_column(
                knowledge.etl_profile,
            )
        )

        if datetime_column is None:

            return TrendResult()

        sorted_dataframe = dataframe.sort_values(
            by=datetime_column,
        )

        trends = self._build_trends(
            sorted_dataframe,
            datetime_column,
        )

        return TrendResult(
            datetime_column=datetime_column,
            trends=trends,
        )

    # ==========================================================
    # PRIVATE
    # ==========================================================


    def _build_trends(
        self,
        dataframe: pd.DataFrame,
        datetime_column: str,
    ) -> list[TrendMetric]:
        """
        Build trend metrics for numeric columns.
        """

        trends: list[
            TrendMetric
        ] = []

        for column in dataframe.columns:

            if column == datetime_column:
                continue

            if not is_numeric_dtype(
                dataframe[column]
            ):
                continue

            series = dataframe[column]

            first_value = self._safe_float(
                series.iloc[0]
            )

            last_value = self._safe_float(
                series.iloc[-1]
            )

            change = last_value - first_value

            if first_value == 0:

                percentage_change = 0.0

            else:

                percentage_change = (
                    (change / first_value) * 100
                )

            trends.append(
                TrendMetric(
                    metric_name=column,
                    first_value=first_value,
                    last_value=last_value,
                    change=change,
                    percentage_change=percentage_change,
                    direction=self._get_direction(
                        change,
                    ),
                )
            )

        return trends

    def _get_direction(
        self,
        change: float,
    ) -> TrendDirection:
        """
        Determine trend direction.
        """

        if change > 0:
            return TrendDirection.INCREASING

        if change < 0:
            return TrendDirection.DECREASING

        return TrendDirection.STABLE

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