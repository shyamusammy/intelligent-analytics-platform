from pandas import DataFrame

from app.core.constants import MLConstants
from app.schemas.ml import ValidationResult


class MLValidator:

    def __init__(self):

        self._validation_checks = [
            self._check_target_exists,
            self._check_minimum_rows,
            self._check_minimum_features,
            self._check_empty_columns,
            self._check_target_nulls,
            self._check_constant_columns,
            self._check_target_uniqueness,
            self._check_duplicate_rows,
        ]

    def validate(
        self,
        dataframe: DataFrame,
        target_column: str
    ) -> ValidationResult:

        result = ValidationResult(
            valid=True,
            errors=[],
            warnings=[]
        )

        for check in self._validation_checks:
            check(
                dataframe,
                target_column,
                result
            )

        result.valid = len(result.errors) == 0

        return result

    def _check_target_exists(
        self,
        dataframe: DataFrame,
        target_column: str,
        result: ValidationResult
    ) -> None:

        if target_column not in dataframe.columns:
            result.errors.append(
                f"Target column '{target_column}' does not exist."
            )

    def _check_minimum_rows(
        self,
        dataframe: DataFrame,
        target_column: str,
        result: ValidationResult
    ) -> None:

        if len(dataframe) < MLConstants.MINIMUM_ROWS:
            result.errors.append(
                f"Dataset must contain at least {MLConstants.MINIMUM_ROWS} rows."
            )

    def _check_minimum_features(
        self,
        dataframe: DataFrame,
        target_column: str,
        result: ValidationResult
    ) -> None:

        if target_column not in dataframe.columns:
            return

        feature_count = len(dataframe.columns) - 1

        if feature_count < MLConstants.MINIMUM_FEATURE_COLUMNS:
            result.errors.append(
                f"Dataset must contain at least {MLConstants.MINIMUM_FEATURE_COLUMNS} feature columns."
            )

    def _check_empty_columns(
        self,
        dataframe: DataFrame,
        target_column: str,
        result: ValidationResult
    ) -> None:

        for column in dataframe.columns:

            if dataframe[column].isna().all():
                result.errors.append(
                    f"Column '{column}' contains only missing values."
                )

    def _check_target_nulls(
        self,
        dataframe: DataFrame,
        target_column: str,
        result: ValidationResult
    ) -> None:

        if target_column not in dataframe.columns:
            return

        if dataframe[target_column].isna().any():
            result.errors.append(
                f"Target column '{target_column}' contains missing values."
            )

    def _check_constant_columns(
        self,
        dataframe: DataFrame,
        target_column: str,
        result: ValidationResult
    ) -> None:

        for column in dataframe.columns:

            if column == target_column:
                continue

            if dataframe[column].isna().all():
                continue

            if dataframe[column].nunique(dropna=True) == 1:
                result.warnings.append(
                    f"Column '{column}' contains only a single unique value."
                )

    def _check_target_uniqueness(
        self,
        dataframe: DataFrame,
        target_column: str,
        result: ValidationResult
    ) -> None:

        if target_column not in dataframe.columns:
            return

        if dataframe[target_column].isna().all():
            return

        if dataframe[target_column].nunique(dropna=True) < 2:
            result.errors.append(
                f"Target column '{target_column}' must contain at least two unique values."
            )

    def _check_duplicate_rows(
        self,
        dataframe: DataFrame,
        target_column: str,
        result: ValidationResult
    ) -> None:

        duplicate_count = dataframe.duplicated().sum()

        if duplicate_count > 0:
            result.warnings.append(
                f"Dataset contains {duplicate_count} duplicate rows."
            )