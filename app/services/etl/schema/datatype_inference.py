from __future__ import annotations

import pandas as pd

from pandas.api.types import (
    is_bool_dtype,
    is_datetime64_any_dtype,
    is_float_dtype,
    is_integer_dtype,
    is_string_dtype,
)

from app.core.constants import (
    ETLConstants,
)

from app.schemas.etl import (
    DetectedDataType,
)


class DataTypeInferenceService:
    """
    Infers the semantic data type of a pandas Series.

    This service extends pandas native dtypes by identifying
    business-friendly data types such as categorical,
    datetime and text.
    """

    def infer(
        self,
        series: pd.Series,
    ) -> DetectedDataType:
        """
        Infer the semantic data type of a column.

        Parameters
        ----------
        series : pd.Series

        Returns
        -------
        DetectedDataType
        """

        # --------------------------------------------------
        # Native pandas dtypes
        # --------------------------------------------------

        if is_bool_dtype(series):
            return DetectedDataType.BOOLEAN

        if is_integer_dtype(series):
            return DetectedDataType.INTEGER

        if is_float_dtype(series):
            return DetectedDataType.FLOAT

        if is_datetime64_any_dtype(series):
            return DetectedDataType.DATETIME

        # --------------------------------------------------
        # String / Object columns
        # --------------------------------------------------

        if is_string_dtype(series):
            return self._infer_string_type(series)

        return DetectedDataType.UNKNOWN

    # ==========================================================
    # Private Methods
    # ==========================================================

    def _infer_string_type(
        self,
        series: pd.Series,
    ) -> DetectedDataType:
        """
        Infer the semantic type of a string column.
        """

        clean_series = series.dropna()

        if clean_series.empty:
            return DetectedDataType.UNKNOWN

        # ------------------------------------------
        # Datetime Detection
        # ------------------------------------------

        sample = clean_series.astype(str).head(10)

        looks_like_datetime = sample.str.contains(
             r"[-/:]",
            regex=True,
        ).any()

        if looks_like_datetime:

            converted = pd.to_datetime(
                clean_series,
                errors="coerce",
            )

            success_rate = converted.notna().mean()

            if (
                success_rate
                >= ETLConstants.DATETIME_DETECTION_THRESHOLD
            ):
                return DetectedDataType.DATETIME

        # --------------------------------------------------
        # Categorical Detection
        # --------------------------------------------------

        unique_count = clean_series.nunique()

        unique_ratio = unique_count / len(clean_series)

        if (
            unique_count
            <= ETLConstants.MAX_CATEGORICAL_UNIQUE_VALUES
        ):
            return DetectedDataType.CATEGORICAL

        # --------------------------------------------------
        # Default
        # --------------------------------------------------

        return DetectedDataType.TEXT