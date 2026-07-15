from __future__ import annotations

import pandas as pd
from pandas.api.types import (
    is_bool_dtype,
    is_datetime64_any_dtype,
    is_float_dtype,
    is_integer_dtype,
)

from app.schemas.etl import DetectedDataType
from app.core.constants import ETLConstants



class DataTypeInferenceService:
    """
    Infers the semantic data type of a pandas Series.

    This service extends pandas' native dtypes by identifying
    business-friendly data types such as categorical and datetime.
    """

    DATETIME_THRESHOLD = 0.95
    CATEGORICAL_THRESHOLD = 0.05
    MAX_CATEGORICAL_UNIQUE = 50

    def infer(
        self,
        series: pd.Series,
    ) -> DetectedDataType:
        """
        Infer the semantic type of a column.

        Parameters
        ----------
        series : pd.Series
            Column to analyze.

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
        # Object columns
        # --------------------------------------------------

        if series.dtype == "object":

            return self._infer_object_type(series)

        return DetectedDataType.UNKNOWN

    # ======================================================

    # Private helpers

    # ======================================================

    def _infer_object_type(
        self,
        series: pd.Series,
    ) -> DetectedDataType:
        """
        Infer semantic type for object columns.
        """

        clean_series = series.dropna()

        if clean_series.empty:
            return DetectedDataType.UNKNOWN

        # ------------------------------------------
        # Datetime Detection
        # ------------------------------------------

        converted = pd.to_datetime(
            clean_series,
            errors="coerce",
        )

        success_rate = converted.notna().mean()

        if success_rate >= ETLConstants.DATETIME_DETECTION_THRESHOLD:
            return DetectedDataType.DATETIME

        # ------------------------------------------
        # Categorical Detection
        # ------------------------------------------

        unique_count = clean_series.nunique()

        unique_ratio = unique_count / len(clean_series)

        if (
            unique_count <= ETLConstants.MAX_CATEGORICAL_UNIQUE_VALUES
            and unique_ratio <= ETLConstants.CATEGORICAL_UNIQUE_RATIO
        ):
            return DetectedDataType.CATEGORICAL

        # ------------------------------------------
        # Default
        # ------------------------------------------

        return DetectedDataType.TEXT