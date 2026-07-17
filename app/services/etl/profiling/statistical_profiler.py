import pandas as pd

from app.schemas.etl import StatisticsProfile


class StatisticalProfiler:
    """
    Generates descriptive statistics
    for numeric columns.
    """

    def profile(
        self,
        dataframe: pd.DataFrame,
    ) -> StatisticsProfile:

        numeric = dataframe.select_dtypes(
            include="number",
        )

        statistics = {}

        for column in numeric.columns:

            series = numeric[column]

            statistics[column] = {

                "count": float(series.count()),

                "mean": float(series.mean()),

                "std": float(series.std()),

                "min": float(series.min()),

                "25%": float(series.quantile(.25)),

                "50%": float(series.median()),

                "75%": float(series.quantile(.75)),

                "max": float(series.max()),
            }

        return StatisticsProfile(
            statistics=statistics
        )