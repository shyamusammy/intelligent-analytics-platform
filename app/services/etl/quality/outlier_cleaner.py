"""Outlier cleaning using non-destructive statistical strategies."""

import pandas as pd


class OutlierCleaner:
    """
    Clean numeric outliers without deleting rows.

    Supported strategies
    --------------------
    keep:
        Keep detected outliers unchanged.

    cap:
        Replace values outside the IQR bounds with the
        corresponding lower or upper IQR boundary.

    median:
        Replace detected outlier values with the median
        of the non-outlier values.

    protected_columns:
        Columns that must never be modified by the cleaner.

    Notes
    -----
    - Only numeric columns are processed.
    - Missing values are never treated as outliers.
    - Columns with zero IQR are skipped.
    - Protected columns are skipped.
    - Rows are never deleted.
    - Numeric columns are converted to float only when
      an actual outlier replacement is required.
    """

    IQR_MULTIPLIER = 1.5

    SUPPORTED_STRATEGIES = {
        "keep",
        "cap",
        "median",
    }

    def clean(
        self,
        dataframe: pd.DataFrame,
        strategy: str = "keep",
        protected_columns: set[str] | list[str] | tuple[str, ...] | None = None,
    ) -> pd.DataFrame:
        """
        Clean outliers in a DataFrame.

        Parameters
        ----------
        dataframe:
            Input dataset.

        strategy:
            Outlier treatment strategy.

            "keep"
                Keep outliers unchanged.

            "cap"
                Cap outliers at their IQR lower/upper bounds.

            "median"
                Replace outliers with the median of
                non-outlier observations.

        protected_columns:
            Columns that must never be modified.

            Protected columns are skipped completely by the
            outlier cleaning process.

        Returns
        -------
        pd.DataFrame
            A cleaned copy of the input DataFrame.

        Raises
        ------
        ValueError
            If an unsupported strategy is supplied.
        """

        # ---------------------------------------------------------
        # 1. Validate strategy
        # ---------------------------------------------------------
        if strategy not in self.SUPPORTED_STRATEGIES:
            raise ValueError(
                f"Unsupported outlier cleaning strategy: "
                f"'{strategy}'. "
                f"Supported strategies: "
                f"{sorted(self.SUPPORTED_STRATEGIES)}"
            )

        # ---------------------------------------------------------
        # 2. Never mutate the original DataFrame
        # ---------------------------------------------------------
        cleaned = dataframe.copy()

        # ---------------------------------------------------------
        # 3. Normalize protected columns
        #
        # Use a set for efficient membership checks.
        # ---------------------------------------------------------
        protected = set(protected_columns or [])

        # ---------------------------------------------------------
        # 4. "keep" means no values should be modified.
        #
        # Return immediately and preserve the original DataFrame
        # structure and dtypes.
        # ---------------------------------------------------------
        if strategy == "keep":
            return cleaned

        # ---------------------------------------------------------
        # 5. Identify numeric columns
        # ---------------------------------------------------------
        numeric_columns = cleaned.select_dtypes(
            include="number"
        ).columns

        # ---------------------------------------------------------
        # 6. Process numeric columns independently
        # ---------------------------------------------------------
        for column in numeric_columns:

            # -----------------------------------------------------
            # Protected columns must NEVER be modified.
            # -----------------------------------------------------
            if column in protected:
                continue

            series = cleaned[column]

            # -----------------------------------------------------
            # Ignore missing values when calculating statistics.
            # -----------------------------------------------------
            non_null = series.dropna()

            if non_null.empty:
                continue

            # -----------------------------------------------------
            # Calculate quartiles
            # -----------------------------------------------------
            q1 = non_null.quantile(0.25)
            q3 = non_null.quantile(0.75)

            # -----------------------------------------------------
            # Calculate IQR
            # -----------------------------------------------------
            iqr = q3 - q1

            # -----------------------------------------------------
            # Zero IQR columns are skipped.
            #
            # Example:
            #
            #     [5, 5, 5, 5]
            #
            # There is no meaningful statistical range.
            # -----------------------------------------------------
            if iqr == 0:
                continue

            # -----------------------------------------------------
            # Calculate IQR bounds
            # -----------------------------------------------------
            lower_bound = (
                q1 - self.IQR_MULTIPLIER * iqr
            )

            upper_bound = (
                q3 + self.IQR_MULTIPLIER * iqr
            )

            # -----------------------------------------------------
            # Detect outliers.
            #
            # Missing values are explicitly excluded.
            # -----------------------------------------------------
            outlier_mask = (
                (series < lower_bound)
                | (series > upper_bound)
            ).fillna(False)

            # -----------------------------------------------------
            # Nothing to clean.
            #
            # Do not change the dtype if there are no outliers.
            # -----------------------------------------------------
            if not outlier_mask.any():
                continue

            # -----------------------------------------------------
            # Actual replacement is required.
            #
            # IQR boundaries and medians can be fractional even
            # when the original column is integer typed.
            #
            # Convert ONLY the affected column to float.
            # -----------------------------------------------------
            if not pd.api.types.is_float_dtype(
                cleaned[column]
            ):
                cleaned[column] = cleaned[column].astype(float)

            # Re-read after dtype conversion.
            series = cleaned[column]

            # -----------------------------------------------------
            # Strategy: CAP
            #
            # Lower outliers → lower IQR boundary
            # Upper outliers → upper IQR boundary
            #
            # No rows are deleted.
            # -----------------------------------------------------
            if strategy == "cap":

                lower_outliers = (
                    outlier_mask
                    & (series < lower_bound)
                )

                upper_outliers = (
                    outlier_mask
                    & (series > upper_bound)
                )

                cleaned.loc[
                    lower_outliers,
                    column,
                ] = lower_bound

                cleaned.loc[
                    upper_outliers,
                    column,
                ] = upper_bound

            # -----------------------------------------------------
            # Strategy: MEDIAN
            #
            # Replace outliers with the median of the values
            # that were not identified as outliers.
            # -----------------------------------------------------
            elif strategy == "median":

                non_outlier_values = series.loc[
                    ~outlier_mask
                ].dropna()

                if non_outlier_values.empty:
                    continue

                median = non_outlier_values.median()

                cleaned.loc[
                    outlier_mask,
                    column,
                ] = median

        return cleaned