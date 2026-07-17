import pandas as pd

from app.schemas.etl import OutlierSummary


class OutlierDetector:
    """
    Detect outliers using the IQR method.
    """

    IQR_MULTIPLIER = 1.5

    def detect(
        self,
        dataframe: pd.DataFrame,
    ) -> OutlierSummary:

        numeric = dataframe.select_dtypes(
            include="number"
        )

        results = {}

        total = 0

        for column in numeric.columns:

            series = numeric[column]

            q1 = series.quantile(0.25)
            q3 = series.quantile(0.75)

            iqr = q3 - q1

            lower = q1 - (
                self.IQR_MULTIPLIER * iqr
            )

            upper = q3 + (
                self.IQR_MULTIPLIER * iqr
            )

            count = int(
                (
                    (series < lower)
                    | (series > upper)
                ).sum()
            )

            if count:

                results[column] = count

                total += count

        return OutlierSummary(

            total_outliers=total,

            outliers_by_column=results,
        )