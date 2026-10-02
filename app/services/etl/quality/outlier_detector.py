"""
Intelligent Analytics Platform
Outlier detection service.

OutlierDetector:
    - Detects numeric outliers using the IQR method.
    - Calculates reusable IQR boundaries.
    - Can detect outliers using either:
        1. boundaries calculated from the current dataset, or
        2. previously calculated boundaries.
    - Missing values are never considered outliers.
    - Constant columns are skipped.
"""

from __future__ import annotations

import pandas as pd

from app.schemas.etl import OutlierSummary


class OutlierDetector:
    """
    Detect outliers using the IQR method.

    The detector supports reusable boundaries so that a cleaned
    dataset can be evaluated against the SAME statistical boundaries
    that were calculated from the original dataset.

    This is important because recalculating Q1/Q3 after cleaning can
    cause the apparent number of outliers to increase even when the
    original outliers were successfully corrected.
    """

    IQR_MULTIPLIER = 1.5

    # ============================================================
    # BOUNDARY CALCULATION
    # ============================================================

    def calculate_boundaries(
        self,
        dataframe: pd.DataFrame,
    ) -> dict[str, dict[str, float]]:
        """
        Calculate IQR boundaries for every numeric column.

        Returns:

            {
                "age": {
                    "q1": ...,
                    "q3": ...,
                    "iqr": ...,
                    "lower": ...,
                    "upper": ...
                },
                ...
            }

        Columns with:
            - no non-null values
            - zero IQR

        are skipped.
        """

        numeric = dataframe.select_dtypes(
            include="number"
        )

        boundaries: dict[str, dict[str, float]] = {}

        for column in numeric.columns:

            series = numeric[column]

            non_null = series.dropna()

            # Nothing to evaluate.
            if non_null.empty:
                continue

            q1 = float(
                non_null.quantile(0.25)
            )

            q3 = float(
                non_null.quantile(0.75)
            )

            iqr = q3 - q1

            # Constant columns do not have a meaningful IQR.
            if iqr == 0:
                continue

            lower = (
                q1
                - self.IQR_MULTIPLIER * iqr
            )

            upper = (
                q3
                + self.IQR_MULTIPLIER * iqr
            )

            boundaries[column] = {
                "q1": q1,
                "q3": q3,
                "iqr": float(iqr),
                "lower": float(lower),
                "upper": float(upper),
            }

        return boundaries

    # ============================================================
    # DETECTION
    # ============================================================

    def detect(
        self,
        dataframe: pd.DataFrame,
        boundaries: dict[str, dict[str, float]]
        | None = None,
    ) -> OutlierSummary:
        """
        Detect outliers in a dataframe.

        If boundaries are not supplied:

            boundaries are calculated from the dataframe.

        If boundaries are supplied:

            those exact boundaries are reused.

        This allows:

            raw dataset
                ↓
            calculate boundaries
                ↓
            clean dataset
                ↓
            detect using original boundaries
        """

        numeric = dataframe.select_dtypes(
            include="number"
        )

        # If no boundaries were supplied, calculate them
        # from the current dataframe.
        if boundaries is None:
            boundaries = self.calculate_boundaries(
                dataframe
            )

        results: dict[str, int] = {}

        total_outliers = 0

        # Track rows containing at least one outlier.
        affected_row_mask = pd.Series(
            False,
            index=dataframe.index,
        )

        for column, stats in boundaries.items():

            # Column may no longer exist in the dataframe.
            if column not in numeric.columns:
                continue

            series = numeric[column]

            lower = stats["lower"]
            upper = stats["upper"]

            outlier_mask = (
                (series < lower)
                | (series > upper)
            )

            # Missing values are never outliers.
            outlier_mask = (
                outlier_mask.fillna(False)
            )

            count = int(
                outlier_mask.sum()
            )

            if count:

                results[column] = count

                total_outliers += count

                # Mark affected rows.
                affected_row_mask |= (
                    outlier_mask
                )

        affected_rows = int(
            affected_row_mask.sum()
        )

        return OutlierSummary(
            total_outliers=total_outliers,
            outliers_by_column=results,
            affected_rows=affected_rows,
        )