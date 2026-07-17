import pandas as pd

from app.schemas.etl import MissingValueSummary


class MissingValueAnalyzer:
    """
    Analyzes missing values within a dataset.
    """

    def analyze(
        self,
        dataframe: pd.DataFrame,
    ) -> MissingValueSummary:

        missing = dataframe.isna().sum()

        return MissingValueSummary(

            total_missing_values=int(missing.sum()),

            columns_with_missing_values=int(
                (missing > 0).sum()
            ),

            missing_by_column={
                column: int(count)
                for column, count in missing.items()
                if count > 0
            },
        )