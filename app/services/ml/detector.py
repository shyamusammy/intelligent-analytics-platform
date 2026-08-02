from pandas import DataFrame
from pandas.api.types import is_numeric_dtype

from app.core.constants import MLConstants
from app.core.enums import MLTaskType


class MLDetector:

    def detect(
        self,
        dataframe: DataFrame,
        target_column: str
    ) -> MLTaskType:

        if self._is_classification(
            dataframe,
            target_column
        ):
            return MLTaskType.CLASSIFICATION

        return MLTaskType.REGRESSION

    def _is_numeric_target(
        self,
        dataframe: DataFrame,
        target_column: str
    ) -> bool:

        return is_numeric_dtype(
            dataframe[target_column]
        )

    def _get_unique_values(
        self,
        dataframe: DataFrame,
        target_column: str
    ) -> int:

        return dataframe[target_column].nunique(
            dropna=True
        )

    def _get_unique_ratio(
        self,
        dataframe: DataFrame,
        target_column: str
    ) -> float:

        unique_values = self._get_unique_values(
            dataframe,
            target_column
        )

        total_rows = len(dataframe)

        return unique_values / total_rows

    def _is_classification(
        self,
        dataframe: DataFrame,
        target_column: str
    ) -> bool:

        if not self._is_numeric_target(
            dataframe,
            target_column
        ):
            return True

        unique_values = self._get_unique_values(
            dataframe,
            target_column
        )

        if (
            unique_values
            <=
            MLConstants.MAX_CLASSIFICATION_UNIQUE_VALUES
        ):
            return True

        unique_ratio = self._get_unique_ratio(
            dataframe,
            target_column
        )

        if (
            unique_ratio
            <=
            MLConstants.CLASSIFICATION_UNIQUE_RATIO
        ):
            return True

        return False