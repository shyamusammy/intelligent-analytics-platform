import pandas as pd

from app.schemas.etl import DuplicateSummary


class DuplicateDetector:
    """
    Detect duplicate rows.
    """

    def analyze(
        self,
        dataframe: pd.DataFrame,
    ) -> DuplicateSummary:

        duplicate_rows = int(
            dataframe.duplicated().sum()
        )

        percentage = 0.0

        if len(dataframe):

            percentage = round(
                duplicate_rows
                / len(dataframe)
                * 100,
                2,
            )

        return DuplicateSummary(

            duplicate_rows=duplicate_rows,

            duplicate_percentage=percentage,
        )